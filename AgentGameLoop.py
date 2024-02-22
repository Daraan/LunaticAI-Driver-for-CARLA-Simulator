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
import random
from typing import List
from pprint import pprint

import pygame
import numpy as np # TODO: fix double random import

from omegaconf import OmegaConf

#try:
#    import carla
#except ImportError as e:
#    from utils.egg_import import carla
import carla 
    
from classes.rule import Rule

import utils
from utils.keyboard_controls import PassiveKeyboardControl, RSSKeyboardControl

from classes.constants import Phase
from classes.HUD import HUD
from classes.worldmodel import WorldModel
from classes.vehicle import Vehicle

from agents.navigation.basic_agent import BasicAgent  
from agents.navigation.behavior_agent import BehaviorAgent 
from agents.navigation.constant_velocity_agent import ConstantVelocityAgent 

from agents.lunatic_agent import LunaticAgent
from agents import behaviour_templates

from conf.lunatic_behavior_settings import LunaticBehaviorSettings



# ==============================================================================
# -- Game Loop ---------------------------------------------------------
# ==============================================================================

def game_loop(args : argparse.ArgumentParser):
    """
    Main loop of the simulation. It handles updating all the HUD information,
    ticking the agent and, if needed, the world.
    """
    world_model : WorldModel = None # Set for finally block

    if args.seed:
        random.seed(args.seed)
        np.random.seed(args.seed)

    pygame.init()
    pygame.font.init()

    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(20.0)

        sim_world = client.get_world()
        sim_map = sim_world.get_map()
        traffic_manager = client.get_trafficmanager()

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

        clock = pygame.time.Clock()
        display = pygame.display.set_mode(
            (args.width, args.height),
            pygame.HWSURFACE | pygame.DOUBLEBUF)

        hud = HUD(args.width, args.height, sim_world)

        try:
            spawn_points = utils.general.csv_to_transformations("../examples/highway_example_car_positions.csv")
        except FileNotFoundError:
            spawn_points = utils.general.csv_to_transformations("examples/highway_example_car_positions.csv")

        # Spawn Ego
        ego_bp, car_bp = utils.blueprint_helpers.get_contrasting_blueprints(sim_world)
        ego = Vehicle(sim_world, ego_bp)
        start : carla.libcarla.Transform = spawn_points[0]
        ego.spawn(start)

        #if True or args.agent == "Lunatic":
        # TODO: # CRITICAL: This should be a dataclass->DictConfig and not its own class!
        # TODO: if DictConfig then World and agent order can be reversed and World initialized with config
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
        })
        print(OmegaConf.to_yaml(behavior.options))
        
        agent = LunaticAgent(ego.actor, sim_world, behavior, map_inst=sim_map)
        world_model = WorldModel(client.get_world(), hud, agent.config, args, player=ego.actor, map_inst=sim_map)
        agent._local_planner._rss_sensor = world_model.rss_sensor # todo: remove later when we have a better ordering of init
        
        # Add Rules:
        agent.add_rules(behaviour_templates.default_rules)
        print("Lunatic Agent Rules")
        pprint(agent.rules)
        
        wp_start = world_model.map.get_waypoint(start.location)
        all_spawn_points = world_model.map.get_spawn_points()

        next_wps: List[carla.Waypoint] = wp_start.next(45)
        last = next_wps[-1]
        left = last.get_left_lane()
        # destination = random.choice(all_spawn_points).location
        destination = left.transform.location
        
        agent.set_destination(destination)
        agent.set_target_speed(33.0)
        #agent.ignore_vehicles(agent._behavior.ignore_vehicles)
        
        controller = RSSKeyboardControl(agent.config, world_model, start_in_autopilot=False)

        # spawn others
        for sp in spawn_points[1:4]:
            v = Vehicle(world_model, car_bp)
            v.spawn(sp)
            world_model.actors.append(v)
            v.actor.set_target_velocity(carla.Vector3D(-2, 0, 0))
            v.actor.set_autopilot(True)
            print(v.actor)


        def loop():

            while True:
                with Rule.CooldownFramework():
                    clock.tick()
                    if args.sync:
                        world_model.world.tick()
                    else:
                        world_model.world.wait_for_tick()
                    if not isinstance(controller, RSSKeyboardControl):
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
                        planned_control = agent.run_step(debug=True)  # debug=True draws waypoints
                        # ----------------------------
                        # Phase RSS - Check RSS
                        # ----------------------------
                        planned_control.manual_gear_shift = False # TODO: turn into a rule
                        
                        ctx = agent.execute_phase(Phase.RSS_EVALUATION | Phase.BEGIN, prior_results=None, control=planned_control)
                        if isinstance(controller, RSSKeyboardControl):
                            if controller.parse_events(clock, ctx.control):
                                return
                        # Todo: Remove
                        assert rss_updated_controls is not planned_control
                        #if rss_updated_controls and rss_updated_controls is not control:
                            #if rss_updated_controls != control:
                                #print("RSS updated controls\n"
                                #     f"throttle: {control.throttle} -> {rss_updated_controls.throttle}, steer: {control.steer} -> {rss_updated_controls.steer}, brake: {control.brake} -> {rss_updated_controls.brake}")
                            
                        ctx = agent.execute_phase(Phase.RSS_EVALUATION | Phase.END, prior_results=rss_updated_controls, control=ctx.control) # NOTE: rss_updated_controls could be None
                        # ----------------------------
                        # Phase 5 - Apply Control to Vehicle
                        # ----------------------------

                        ctx = agent.execute_phase(Phase.EXECUTION | Phase.BEGIN, prior_results=None, control=ctx.control)
                        final_control = ctx.control
                        #if isinstance(controller, RSSKeyboardControl):
                        #    if controller.parse_events(clock, final_control):
                        #        return
                        # Set automatic control-related vehicle lights
                        world_model.update_lights(final_control)
                        world_model.player.apply_control(planned_control)
                        agent.execute_phase(Phase.EXECUTION | Phase.END, prior_results=None, control=final_control)
                        
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
            traffic_manager.set_synchronous_mode(False)
            world_model.destroy()
        else:
            try:
                ego.actor.destroy()
            except (NameError, AttributeError):
                pass

        pygame.quit()


# ==============================================================================
# -- main() --------------------------------------------------------------
# ==============================================================================


def main():
    """Main method"""

    args = utils.argument_parsing.main_parser().parse_args()
    
    # Overrides
    args.loop = True
    args.agent = "Lunatic"

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
