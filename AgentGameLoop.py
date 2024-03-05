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
    
from agents.tools.misc import draw_waypoints
from classes.rule import Context, Rule

from conf.agent_settings import LunaticAgentSettings
import utils
from utils.keyboard_controls import PassiveKeyboardControl, RSSKeyboardControl

from classes.constants import Phase
from classes.HUD import HUD
from classes.worldmodel import WorldModel, AD_RSS_AVAILABLE
from classes.vehicle import Vehicle

from agents.navigation.basic_agent import BasicAgent  
from agents.navigation.behavior_agent import BehaviorAgent 
from agents.navigation.constant_velocity_agent import ConstantVelocityAgent 

from agents.lunatic_agent import LunaticAgent
from agents import behaviour_templates

# ==============================================================================
# TEMP # Remove

PRINT_CONFIG = False
PRINT_RULES = False

# ==============================================================================
# -- Game Loop ---------------------------------------------------------
# ==============================================================================

def game_loop(args : argparse.ArgumentParser):
    """
    Main loop of the simulation. It handles updating all the HUD information,
    ticking the agent and, if needed, the world.
    """
    world_model : WorldModel = None # Set for finally block
    agent : LunaticAgent = None # Set for finally block

    args.seed = 631 # TEMP
    
    if args.seed:
        random.seed(args.seed)
        np.random.seed(args.seed)

    pygame.init()
    pygame.font.init()

    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(20.0)

        sim_world = client.get_world()

        if args.sync:
            logging.log(logging.DEBUG, "Using synchronous mode.")
            # apply synchronous mode if wanted
            world_settings = sim_world.get_settings()
            world_settings.synchronous_mode = True
            world_settings.fixed_delta_seconds = 0.05
            sim_world.apply_settings(world_settings)
            traffic_manager = client.get_trafficmanager()
            traffic_manager.set_synchronous_mode(True)
        else:
            traffic_manager = client.get_trafficmanager()
            logging.log(logging.DEBUG, "Might be using asynchronous mode if not changed.")
            world_settings = sim_world.get_settings()
        print("World Settings:", world_settings)

        sim_map = sim_world.get_map()
        
        clock = pygame.time.Clock()
        display = pygame.display.set_mode(
            (args.width, args.height),
            pygame.HWSURFACE | pygame.DOUBLEBUF)

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
        behavior = LunaticAgentSettings(
            {'controls':{ "max_brake" : 1.0, 
                        'max_steering' : 0.25},
            'speed': {'target_speed': 33.0,
                        'max_speed' : 50,
                        'follow_speed_limits' : False,
                        'speed_decrease' : 15,
                            'safety_time' : 7,
                            'min_speed' : 0 },
            'lane_change' : {
                "random_left_lanechange_percentage": 0.45,
                "random_right_lanechange_percentage": 0.45,
            },
            'rss': {'enabled': False, 
                    'use_stay_on_road_feature': False},
            "planner": {
                "dt" : world_settings.fixed_delta_seconds or 1/20,
                "min_distance_next_waypoint" : 2.0,
                
             }
            })
        # TEMP
        import classes.worldmodel
        classes.worldmodel.AD_RSS_AVAILABLE = behavior.rss.enabled
        
        print("Set dt to", world_settings.fixed_delta_seconds)
        if PRINT_CONFIG:
            print("    \n\n\n")
            pprint(behavior)
            print(behavior.to_yaml())
        
            
        config = behavior.make_config()
        # Test 1
        world_model = WorldModel(sim_world, config, args, player=ego.actor, map_inst=sim_map, agent=agent) # NOTE: # CRITICAL: Here an important tick happens that should be before the local planner initialization
        
        agent = LunaticAgent(ego.actor, world_model, config, map_inst=sim_map, overwrite_options={'distance':{
                "min_proximity_threshold": 12.0,
                "emergency_braking_distance": 6.0,
                "distance_to_leading_vehicle": 8.0},})
        del config
        del agent
        del world_model
        # Test 2
        agent, world_model, global_planner = LunaticAgent.create_world_and_agent(ego.actor, sim_world, args, map_inst=sim_map, overwrites={'distance':{
                "min_proximity_threshold": 12.0,
                "emergency_braking_distance": 6.0,
                "distance_to_leading_vehicle": 8.0},})
        config = agent.config
        
        print("DT is", agent.config.planner.dt)
        
        # Add Rules:
        agent.add_rules(behaviour_templates.default_rules)
        if PRINT_RULES: # TEMP
            print("Lunatic Agent Rules")
            pprint(agent.rules)
        
        wp_start = world_model.map.get_waypoint(start.location)
        all_spawn_points = world_model.map.get_spawn_points()

        next_wps: List[carla.Waypoint] = wp_start.next(25)
        last_wp = next_wps[-1]
        left_last_wp = last_wp.get_left_lane()
        print(left_last_wp, sim_map.get_waypoint(left_last_wp.transform.location))
        # destination = random.choice(all_spawn_points).location
        destination = left_last_wp.transform.location
        
        agent.set_destination(left_last_wp)

        #agent.set_target_speed(33.0)
        #agent.ignore_vehicles(agent._behavior.ignore_vehicles)
        
        controller = RSSKeyboardControl(agent.config, world_model, start_in_autopilot=False)

        # spawn others
        for sp in spawn_points[1:4]:
            v = Vehicle(world_model, car_bp)
            v.spawn(sp)
            world_model.actors.append(v.actor)
            v.actor.set_target_velocity(carla.Vector3D(-2, 0, 0))
            v.actor.set_autopilot(True)
            print("Spawned", v.actor)

        def loop():
            if args.sync:
                # Assure that dt is set
                OmegaConf.select(agent.config,
                    "planner.dt",
                    throw_on_missing=True
                )
            destination = agent._local_planner._waypoints_queue[-1][0].transform.location # TODO find a nicer way
            agent._road_matrix_updater.start()  # TODO find a nicer way
            
            # TEMP
            agent._road_matrix_updater.stop()
            
            ctx : Context = None
            while True:
                with Rule.CooldownFramework():
                    clock.tick()
                    if args.sync:
                        world_model.world.tick()
                    else:
                        world_model.world.wait_for_tick()
                    ctx = agent.make_context(last_context=ctx)
                    
                    if not isinstance(controller, RSSKeyboardControl):
                        controller.parse_events()

                    # TODO: Make this a rule and/or move inside agent
                    # TODO: make a Phases.DONE
                    if not controller._autopilot_enabled:
                        if agent.done():
                            # NOTE: Might be in NONE phase here.
                            agent.execute_phase(Phase.DONE| Phase.BEGIN, prior_results=None)
                            if args.loop and agent.done():
                                # TODO: Rule / Action to define next waypoint
                                print("The target has been reached, searching for another target")
                                world_model.hud.notification("Target reached", seconds=4.0)
                                wp = agent._current_waypoint.next(50)[-1]
                                next_wp = random.choice((wp, wp.get_left_lane(), wp.get_right_lane()))
                                if next_wp is None:
                                    next_wp = wp
                                #destination = random.choice(spawn_points).location
                                destination = next_wp.transform.location
                                agent.set_destination(destination)
                            elif agent.done():
                                print("The target has been reached, stopping the simulation")
                                agent.execute_phase(Phase.TERMINATING | Phase.BEGIN, prior_results=None)
                                break
                            agent.execute_phase(Phase.DONE| Phase.END, prior_results=None)
                        
                        # ----------------------------
                        # Phase NONE - Before Running step
                        # ----------------------------
                        planned_control = agent.run_step(debug=True)  # debug=True draws waypoints
                        assert planned_control is agent.ctx.control # TEMP
                        # ----------------------------
                        # No known Phase multiple exit points
                        # ----------------------------
                        
                        # ----------------------------
                        # Phase RSS - Check RSS
                        # ----------------------------
                        planned_control.manual_gear_shift = False # TODO: turn into a rule
                        
                        ctx = agent.execute_phase(Phase.RSS_EVALUATION | Phase.BEGIN, prior_results=None, control=planned_control)
                        #if isinstance(controller, RSSKeyboardControl):
                        #    if controller.parse_events(clock, ctx.control):
                        #        return
                        # Todo: Remove
                        if AD_RSS_AVAILABLE:
                            rss_updated_controls = world_model.rss_check_control(ctx.control)
                        else:
                            rss_updated_controls = None
                        assert rss_updated_controls is not planned_control
                        #if rss_updated_controls and rss_updated_controls is not control:
                            #if rss_updated_controls != control:
                                #print("RSS updated controls\n"
                                #     f"throttle: {control.throttle} -> {rss_updated_controls.throttle}, steer: {control.steer} -> {rss_updated_controls.steer}, brake: {control.brake} -> {rss_updated_controls.brake}")
                            
                        ctx = agent.execute_phase(Phase.RSS_EVALUATION | Phase.END, prior_results=rss_updated_controls) # NOTE: rss_updated_controls could be None
                        # ----------------------------
                        # Phase 5 - Apply Control to Vehicle
                        # ----------------------------

                        ctx = agent.execute_phase(Phase.EXECUTION | Phase.BEGIN, prior_results=rss_updated_controls)
                        final_control = ctx.control
                        assert final_control is planned_control
                        if isinstance(controller, RSSKeyboardControl):
                            if controller.parse_events(clock, final_control):
                                return
                        # Set automatic control-related vehicle lights
                        world_model.update_lights(final_control)
                        world_model.player.apply_control(final_control)
                        agent.execute_phase(Phase.EXECUTION | Phase.END, prior_results=None, control=final_control)
                        
                        sim_world.debug.draw_point(destination, life_time=0.5)
                        # Update render and hud
                        world_model.tick(clock) # TODO # CRITICAL maybe has to tick later
                        world_model.render(display)
                        controller.render(display)
                        pygame.display.flip()
                        
                        matrix = agent.road_matrix  # TEMP
                        if matrix is not None:
                            pprint(matrix) # TEMP   
                        
            agent.execute_phase(Phase.TERMINATING | Phase.END, prior_results=None) # final phase of agents lifetime

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
        print("Quitting. - Destroying actors and stopping world.")
        if agent is not None:
            agent._road_matrix_updater.stop()
        if world_model is not None:
            world_settings = world_model.world.get_settings()
            world_settings.synchronous_mode = False
            world_settings.fixed_delta_seconds = None
            world_model.world.apply_settings(world_settings)
            traffic_manager.set_synchronous_mode(False)
            world_model.destroy()
            ego = None
        
        try:
            if ego is not None and ego.actor is not None:
                ego.actor.destroy()
        except (NameError, AttributeError) as e:
            print("Ego actor not found", e)
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
