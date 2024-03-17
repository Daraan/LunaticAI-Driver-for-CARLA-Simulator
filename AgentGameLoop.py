#!/usr/bin/env python
"""

Example of the agent system

Based on German Ros's (german.ros@intel.com) example of automatic_control shipped with carla.
"""
from __future__ import print_function  # for python 2.7 compatibility

from collections.abc import Mapping
import signal
import sys
import argparse
import logging
import threading
import random
from typing import List
from pprint import pprint

import pygame
import numpy as np

import hydra
from omegaconf import DictConfig, OmegaConf

# Use this when carla is not installed
#try:
#    import carla
#except ImportError as e:
#    from utils.egg_import import carla
import carla 
    
import launch_tools
from conf.agent_settings import LunaticAgentSettings

from classes.rule import Context, Rule

from classes.keyboard_controls import PassiveKeyboardControl, RSSKeyboardControl

from classes.constants import Phase
from classes.HUD import HUD
from classes.worldmodel import GameFramework, WorldModel, AD_RSS_AVAILABLE
from classes.vehicle import Vehicle

from agents.tools.logging import logger
from agents.tools.misc import draw_waypoints
from agents.navigation.basic_agent import BasicAgent  
from agents.navigation.behavior_agent import BehaviorAgent 
from agents.navigation.constant_velocity_agent import ConstantVelocityAgent 

from agents.lunatic_agent import LunaticAgent
from agents import behaviour_templates

# ==============================================================================
# TEMP # Remove

PRINT_CONFIG = False
PRINT_RULES = False
FPS = 10

# ==============================================================================
# -- Game Loop ---------------------------------------------------------
# ==============================================================================

def game_loop(args : argparse.ArgumentParser):
    """
    Main loop of the simulation. It handles updating all the HUD information,
    ticking the agent and, if needed, the world.
    """
    game_framework : GameFramework = None # Set for finally block
    world_model : WorldModel = None # Set for finally block
    agent : LunaticAgent = None # Set for finally block
    ego : carla.Vehicle = None # Set for finally block
    
    args.seed = 631 # TEMP

    # -- Load Settings Agent --

    print("Creating settings")
    # TODO: Pack this in some utility function
    if isinstance(args.agent, dict):
        logger.debug("Using agent settings from dict")
        behavior = LunaticAgentSettings(**args.agent)
    elif isinstance(args.agent, str):
        logger.info("Using agent settings from file `%s`", args.agent)
        behavior = LunaticAgentSettings.from_yaml(args.agent)
        behavior = OmegaConf.merge(behavior,
        #behavior = LunaticAgentSettings(
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
            'rss': {'enabled': True, 
                    'use_stay_on_road_feature': carla.RssRoadBoundariesMode(False) if AD_RSS_AVAILABLE else False},
            "planner": {
                "dt" : game_framework.world_settings.fixed_delta_seconds or 1/args.fps,
                "min_distance_next_waypoint" : 2.0,
            }
            })
    elif is_dataclass(args.agent) or isinstance(args.agent, DictConfig):
        logger.info("Using agent settings hydra interface")
        behavior = args.agent
    else:
        logger.warning("Type `%s` of launch argument type `agent` not supported, trying to use it anyway. Expected are (str, dataclass, DictConfig)", type(args.agent))
        behavior = args.agent
    # TEMP
    import classes.worldmodel
    classes.worldmodel.AD_RSS_AVAILABLE = classes.worldmodel.AD_RSS_AVAILABLE and behavior.rss.enabled
    
    if PRINT_CONFIG:
        print("    \n\n\n")
        pprint(behavior)
        from conf.agent_settings import AgentConfig
        if isinstance(behavior, AgentConfig):
            print(behavior.to_yaml())
        else:
            try:
                print(OmegaConf.to_yaml(behavior))
            except Exception as e:
                pprint(behavior)
    try:
        print("Creating game framework:...", end="")
        game_framework = GameFramework(args)
        print("Done")
        
        # -- Spawn Vehicles --
        all_spawn_points = game_framework.map.get_spawn_points()
        spawn_points = launch_tools.general.csv_to_transformations("examples/highway_example_car_positions.csv")
        
        ego_bp, car_bp = launch_tools.blueprint_helpers.get_contrasting_blueprints(game_framework.world)
        
        # Spawn Others
        traffic_manager = game_framework.init_traffic_manager()
        spawn_commands = []
        for sp in spawn_points[1:4]:
            spawn_commands.append(carla.command.SpawnActor(car_bp, sp).then(
                            carla.command.SetAutopilot(carla.command.FutureActor, True)))

        response = game_framework.client.apply_batch_sync(spawn_commands)
        spawned_vehicles = list(game_framework.world.get_actors([x.actor_id for x in response]))
        
        # Spawn Ego
        start : carla.libcarla.Transform = spawn_points[0]
        ego = game_framework.world.spawn_actor(ego_bp, start)
        spawned_vehicles.append(ego)
        
        # TEMP # Test external actor, do not pass ego
        print("Creating agent and WorldModel:...", end="")
        if args.externalActor:
            agent, world_model, global_planner, controller \
                = game_framework.init_agent_and_interface(None, agent_class=LunaticAgent, 
                    overwrites=behavior)
        else:
            agent, world_model, global_planner, controller \
                = game_framework.init_agent_and_interface(ego, agent_class=LunaticAgent, 
                        overwrites=behavior)
        print("Done")
        
        # Add Rules:
        agent.add_rules(behaviour_templates.default_rules)
        if PRINT_RULES: # TEMP
            print("Lunatic Agent Rules")
            pprint(agent.rules)
        
        # -- Scenario --
        
        # Set initial destination
        wp_start = world_model.map.get_waypoint(start.location)

        next_wps: List[carla.Waypoint] = wp_start.next(25)
        last_wp = next_wps[-1]
        left_last_wp = last_wp.get_left_lane()
        print(left_last_wp, world_model.map.get_waypoint(left_last_wp.transform.location))
        # destination = random.choice(all_spawn_points).location
        destination = left_last_wp.transform.location
        
        agent.set_destination(left_last_wp)
        
        def loop():
            agent.verify_settings()
            while game_framework.continue_loop:
                # Loop with traffic_manager
                if controller._autopilot_enabled:
                    if controller.parse_events(None):
                        return
                    continue
                # Agent Loop
                with game_framework:
                    final_control = agent.run_step(debug=True)
                    
                    agent.execute_phase(Phase.APPLY_MANUAL_CONTROLS | Phase.BEGIN, prior_results=final_control)
                    if isinstance(world_model.controller, RSSKeyboardControl):
                        if controller.parse_events(agent.get_control()):
                            return
                    agent.execute_phase(Phase.APPLY_MANUAL_CONTROLS | Phase.END, prior_results=None)
                    
                    agent.execute_phase(Phase.EXECUTION | Phase.BEGIN, prior_results=final_control)
                    agent.apply_control() # Note Uses control from agent.ctx.control in case of last Phase changed it.
                    agent.execute_phase(Phase.EXECUTION | Phase.END, prior_results=None)
                    
                    try:
                        destination = agent._local_planner._waypoints_queue[-1][0].transform.location # TODO find a nicer way
                        destination = destination + carla.Vector3D(0, 0, 1.5) # elevate to be not in road
                    except IndexError:
                        pass
                    game_framework.debug.draw_point(destination, life_time=0.5)
                    
                    matrix = agent.road_matrix  # TEMP
                    if matrix is not None:
                        pprint(matrix) # TEMP
                
                # Continue the Loop from outside
                if args.loop and not game_framework.continue_loop and agent.done():
                    # TODO: Rule / Action to define next waypoint
                    print("The target has been reached, searching for another target")
                    world_model.hud.notification("Target reached", seconds=4.0)
                    
                    # Set new destination
                    wp = agent._current_waypoint.next(50)[-1]
                    next_wp = random.choice((wp, wp.get_left_lane(), wp.get_right_lane()))
                    if next_wp is None:
                        next_wp = wp
                    #destination = random.choice(spawn_points).location
                    destination = next_wp.transform.location
                    agent.set_destination(destination)
                    game_framework.continue_loop = True
                    agent.execute_phase(Phase.DONE| Phase.END, prior_results=None)
            
             # final phase of agents lifetime                  
            agent.execute_phase(Phase.TERMINATING | Phase.END, prior_results=None)

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
    except Exception as e:
        logger.error("Exception in game loop", exc_info=True)
    finally:
        print("Quitting. - Destroying actors and stopping world.")
        if agent is not None:
            agent.destroy_sensor()
        if game_framework is not None:
            world_settings = game_framework.world.get_settings()
            world_settings.synchronous_mode = False
            world_settings.fixed_delta_seconds = None
            game_framework.world.apply_settings(world_settings)
            traffic_manager.set_synchronous_mode(False)
        if world_model is not None:
            world_model.destroy(destroy_ego=False)
        if game_framework is not None:
            game_framework.client.apply_batch([carla.command.DestroyActor(x) for x in spawned_vehicles])
            ego = None
        
        try: # NOTE: Currently not used
            if ego is not None:
                ego.destroy()
        except (NameError, AttributeError) as e:
            print("Ego actor not found", e)
            pass

        pygame.quit()


# ==============================================================================
# -- main() --------------------------------------------------------------
# ==============================================================================

@hydra.main(version_base=None, config_path="./conf", config_name="launch_config")
def main(args: DictConfig):
    """Main method"""
    print("Launch Arguments\n", OmegaConf.to_yaml(args))  

    log_level = logging.DEBUG if args.debug else logging.INFO
    
    logger.setLevel(log_level)
    logger.info('listening to server %s:%s', args.host, args.port)

    print(__doc__)

    signal.signal(signal.SIGINT, RSSKeyboardControl.signal_handler)

    try:
        game_loop(args)
        
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':
    main()
