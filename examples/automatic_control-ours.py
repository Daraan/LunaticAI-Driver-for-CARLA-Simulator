#!/usr/bin/env python
"""

Example of the agent system

Based on German Ros's (german.ros@intel.com) example of automatic_control shipped with carla.
"""
from __future__ import print_function  # for python 2.7 compatibility
import __allow_imports_from_root

import logging
import random
import sys
import threading

import carla
import numpy.random as random
import pygame
from agents.tools.lunatic_agent_tools import Phase
from config.lunatic_behavior_settings import LunaticBehaviorSettings

import utils
from agents.navigation.basic_agent import BasicAgent  # pylint: disable=import-error
from agents.navigation.behavior_agent import BehaviorAgent  # pylint: disable=import-error
from agents.navigation.constant_velocity_agent import ConstantVelocityAgent  # pylint: disable=import-error

from agents.lunatic_agent import LunaticAgent

from classes.carla_originals.HUD import HUD
from classes.carla_originals.world import World
from classes.vehicle import Vehicle
from utils.keyboard_controls import PassiveKeyboardControl as KeyboardControl


# ==============================================================================
# -- Game Loop ---------------------------------------------------------
# ==============================================================================


def game_loop(args):
    """
    Main loop of the simulation. It handles updating all the HUD information,
    ticking the agent and, if needed, the world.
    """

    pygame.init()
    pygame.font.init()
    world = None

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

        hud = HUD(args.width, args.height)

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
        start: carla.Transform = spawn_points[0]
        ego.spawn(start)

        world = World(client.get_world(), hud, args, player=ego.actor)
        wp_start = world.map.get_waypoint(start.location)
        all_spawn_points = world.map.get_spawn_points()
        # destination = random.choice(all_spawn_points).location

        controller = KeyboardControl(world)
        # world.set_actor(ego.actor)

        # carlaService.assignDriver(ego, driver1)
        args.agent = "Lunatic"

        if args.agent == "Lunatic":
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
            agent = LunaticAgent(world.player, behavior)
        elif args.agent == "Basic":
            agent = BasicAgent(world.player, 30)
            agent.follow_speed_limits(True)
        elif args.agent == "Constant":
            agent = ConstantVelocityAgent(world.player, 30)
            ground_loc = world.world.ground_projection(world.player.get_location(), 5)
            if ground_loc:
                world.player.set_location(ground_loc.location + carla.Location(z=0.01))
            agent.follow_speed_limits(True)
        elif args.agent == "Behavior":
            agent = BehaviorAgent(world.player, behavior=args.behavior)
            from pprint import pprint
            pprint(vars(agent._behavior))
        else:
            raise ValueError(args.agent)

        next_wps: list = wp_start.next(45)
        last = next_wps[-1]
        left = last.get_left_lane()

        destination = left.transform.location

        agent.set_destination(destination)
        #agent.ignore_vehicles(agent._behavior.ignore_vehicles)

        clock = pygame.time.Clock()

        # spawn others
        for sp in spawn_points[1:]:
            v = Vehicle(world, car_bp)
            v.spawn(sp)
            world.actors.append(v)
            # v.setVelocity(1)
            v.actor.set_autopilot(True)
            print(v.actor)
            #ap = TrafficManagerD(client, v.actor)
            #ap.init_passive_driver()
            #ap.start_drive()

        ego.set_target_velocity(carla.Vector3D(-7.5, 0, 0))

        def loop():
            args.loop = True

            i = 0
            while True:
                clock.tick()
                if args.sync:
                    world.world.tick()
                else:
                    world.world.wait_for_tick()
                if controller.parse_events():
                    return

                world.tick(clock)
                world.render(display)
                pygame.display.flip()

                # TODO: Make this a rule and/or move inside agent
                # TODO: make a Phases.DONE
                if agent.done():
                    agent.execute_phase(Phase.DONE| Phase.BEGIN, prior_results=None, control=control)
                    if args.loop:
                        agent.set_destination(random.choice(spawn_points).location)
                        world.hud.notification("Target reached", seconds=4.0)
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

                # TODO: Remove phase > EXECUTION | BEGIN 
                agent.execute_phase(Phase.MODIFY_FINAL_CONTROLS | Phase.BEGIN, prior_results=None, control=control)
                control.manual_gear_shift = False # TODO: turn into a rule
                agent.execute_phase(Phase.MODIFY_FINAL_CONTROLS | Phase.END, prior_results=None, control=control)
                #print("Appling control", control)

                agent.execute_phase(Phase.EXECUTION | Phase.BEGIN, prior_results=None, control=control)
                world.player.apply_control(control)
                agent.execute_phase(Phase.EXECUTION | Phase.END, prior_results=None, control=control)
                
                # if i % 50 == 0:
                #    print("Tailgate Counter", agent._behavior.tailgate_counter)
                i += 1
            agent.execute_phase(Phase.TERMINATING | Phase.END) # final phase of agents lifetime

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

        if world is not None:
            settings = world.world.get_settings()
            settings.synchronous_mode = False
            settings.fixed_delta_seconds = None
            world.world.apply_settings(settings)
            traffic_manager.set_synchronous_mode(True)

            world.destroy()

        pygame.quit()


# ==============================================================================
# -- main() --------------------------------------------------------------
# ==============================================================================


def main():
    """Main method"""

    args = utils.argument_parsing.automatic_control_example.parse_args()

    args.width, args.height = [int(x) for x in args.res.split('x')]

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    print(__doc__)

    try:
        game_loop(args)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':
    main()
