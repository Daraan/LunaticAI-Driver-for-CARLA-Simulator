#!/usr/bin/env python
"""

Example of the agent system

Based on German Ros's (german.ros@intel.com) example of automatic_control shipped with carla.
"""
from __future__ import print_function  # for python 2.7 compatibility

import signal
import sys
import argparse
import logging
import threading
from typing import List
import pygame

import random
import numpy.random as random # TODO: fix import

#try:
#    import carla
#except ImportError as e:
#    from utils.egg_import import carla
import carla 
    
from classes.rule import Rule

import utils
from utils.keyboard_controls import PassiveKeyboardControl, RSSKeyboardControl

from agents.tools.lunatic_agent_tools import Phase
from agents.navigation.basic_agent import BasicAgent  
from agents.navigation.behavior_agent import BehaviorAgent 
from agents.navigation.constant_velocity_agent import ConstantVelocityAgent 

from agents.lunatic_agent import LunaticAgent
from conf.lunatic_behavior_settings import LunaticBehaviorSettings

from classes.HUD import HUD
from classes.worldmodel import WorldModel
from classes.vehicle import Vehicle


# ==============================================================================
# -- Game Loop ---------------------------------------------------------
# ==============================================================================

def game_loop(args : argparse.ArgumentParser):
    """
    Main loop of the simulation. It handles updating all the HUD information,
    ticking the agent and, if needed, the world.
    """

    pygame.init()
    pygame.font.init()
    world_model : WorldModel = None

    try:
        vehicle = []
        if args.seed:
            random.seed(args.seed)

        client = carla.Client(args.host, args.port)
        client.set_timeout(60.0)

        traffic_manager = client.get_trafficmanager()
        sim_world = client.get_world()

        if args.sync:
            logging.log(logging.DEBUG, "Using synchronous mode.")
            # apply synchronous mode if wanted
            settings = sim_world.get_settings()
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = 0.05
            sim_world.apply_settings(settings)
            traffic_manager.set_synchronous_mode(True)
        else:
            logging.log(logging.DEBUG, "Might be using asynchronous mode if not changed.")

        display = pygame.display.set_mode(
            (args.width, args.height),
            pygame.HWSURFACE | pygame.DOUBLEBUF)

        hud = HUD(args.width, args.height, sim_world)

        # carlaService = CarlaService("Town04", "127.0.0.1", 2000)

        # Set the agent destination
        # import os
        #print(os.path.exists("examples/highway_example_car_positions.csv"))
        #print(os.getcwd())
        #import time
        #time.sleep(1.5)
        try:
            spawn_points = utils.general.csv_to_transformations("../examples/highway_example_car_positions.csv")
        except FileNotFoundError:
            spawn_points = utils.general.csv_to_transformations("examples/highway_example_car_positions.csv")
        # car1 = carlaService.createCar("model3")

        # Spawn Ego
        ego_bp, car_bp = utils.blueprint_helpers.get_contrasting_blueprints(sim_world)
        ego = Vehicle(sim_world, ego_bp)
        start : carla.libcarla.Transform = spawn_points[0]
        ego.spawn(start)

        world_model = WorldModel(client.get_world(), hud, args, player=ego.actor)
        wp_start = world_model.map.get_waypoint(start.location)
        all_spawn_points = world_model.map.get_spawn_points()
        # destination = random.choice(all_spawn_points).location

        controller = RSSKeyboardControl(world_model, start_in_autopilot=False)
        #controller._autopilot_enabled = False
        # world.set_actor(ego.actor)

        # carlaService.assignDriver(ego, driver1)
        args.agent = "Lunatic"

        if True or args.agent == "Lunatic":
            behavior = LunaticBehaviorSettings({'distance':
               { "base_min_distance": 5.0,
                "min_proximity_threshold": 12.0,
                "braking_distance": 6.0,
                "distance_to_leading_vehicle": 8.0},
                'controls':{ "max_brake" : 1.0, 
                            'max_steering' : 0.25},
                'speed': {'target_speed': 33.0,
                          'max_speed' : 50,
                           'follow_speed_limits' : False,
                            'speed_decrease' : 15,
                             'safety_time' : 7,
                              'min_speed' : 0 }
            } 
                )
            from omegaconf import OmegaConf
            print(OmegaConf.to_yaml(behavior.options))
            agent = LunaticAgent(world_model.player, behavior)


        next_wps: List[carla.Waypoint] = wp_start.next(45)
        last = next_wps[-1]
        left = last.get_left_lane()

        destination = left.transform.location

        agent.set_destination(destination)
        #agent.ignore_vehicles(agent._behavior.ignore_vehicles)

        clock = pygame.time.Clock()

        # spawn others
        for sp in spawn_points[1:4]:
            v = Vehicle(world_model, car_bp)
            v.spawn(sp)
            world_model.actors.append(v)
            # v.setVelocity(1)
            v.actor.set_autopilot(True)
            v.actor.set_target_velocity(carla.Vector3D(-2, 0, 0))
            print(v.actor)
            #ap = TrafficManagerD(client, v.actor)
            #ap.init_passive_driver()
            #ap.start_drive()

        ego.set_target_velocity(carla.Vector3D(-7.5, 0, 0))

        def loop():
            args.loop = True

            i = 0
            while True:
                with Rule.CooldownFramework(): # todo: low prio, make cooldown dependant on the tick speed.
                    clock.tick()
                    if args.sync:
                        world_model.world.tick()
                    else:
                        world_model.world.wait_for_tick()
                    if isinstance(controller, RSSKeyboardControl):
                        if controller.parse_events(world_model, clock):
                            return
                    else:
                        controller.parse_events()

                    world_model.tick(clock)
                    world_model.render(display)
                    pygame.display.flip()

                    # TODO: Make this a rule and/or move inside agent
                    # TODO: make a Phases.DONE
                    if not controller._autopilot_enabled:
                        if agent.done():
                            # NOTE: Might be in NONE phase here.
                            agent.execute_phase(Phase.DONE| Phase.BEGIN, prior_results=None, control=control)
                            if args.loop:
                                # TODO: Rule / Action to define next waypoint
                                agent.set_destination(random.choice(spawn_points).location)
                                world_model.hud.notification("Target reached", seconds=4.0)
                                print("The target has been reached, searching for another target")
                            else:
                                print("The target has been reached, stopping the simulation")
                                agent.execute_phase(Phase.TERMINATING | Phase.BEGIN)
                                break
                            agent.execute_phase(Phase.DONE| Phase.END, prior_results=None, control=control)
                        
                        # ----------------------------
                        # Phase NONE - Before Running step
                        # ----------------------------
                        control = agent.run_step(debug=True)  # debug=True draws waypoints

                        # ----------------------------
                        # Phase 5 - Apply Control to Vehicle
                        # ----------------------------

                        agent.execute_phase(Phase.EXECUTION | Phase.BEGIN, prior_results=None, control=control)
                        control.manual_gear_shift = False # TODO: turn into a rule
                        # Set automatic control-related vehicle lights
                        world_model.update_lights(control)
                        world_model.player.apply_control(control)
                        agent.execute_phase(Phase.EXECUTION | Phase.END, prior_results=None, control=control)
                        
            agent.execute_phase(Phase.TERMINATING | Phase.END) # final phase of agents lifetime

        # Interactive
        if "-I" in sys.argv:
            thread = threading.Thread(target=loop)
            thread.start()
            # goes into interactive mode here
            import code
            v = globals().copy()
            v.update(locals())
            code.interact(local=v)
            thread.join()
        else:
            loop()


    finally:

        if world_model is not None:
            settings = world_model.world.get_settings()
            settings.synchronous_mode = False
            settings.fixed_delta_seconds = None
            world_model.world.apply_settings(settings)
            traffic_manager.set_synchronous_mode(True)

            world_model.destroy()
        try:
            ego.destroy()
        except:
            pass

        pygame.quit()


# ==============================================================================
# -- main() --------------------------------------------------------------
# ==============================================================================


def main():
    """Main method"""

    args = utils.argument_parsing.main_parser().parse_args()

    args.width, args.height = [int(x) for x in args.res.split('x')]

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    print(__doc__)

    signal.signal(signal.SIGINT, RSSKeyboardControl.signal_handler)

    try:
        game_loop(args)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':
    main()
