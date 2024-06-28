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
from typing import List, Union
from pprint import pprint

import numpy as np

import hydra
from omegaconf import MISSING, DictConfig, OmegaConf

# Use this when carla is not installed
#try:
#    import carla
#except ImportError as e:
#    from utils.egg_import import carla
import carla 
import pygame
import launch_tools
    
from launch_tools import CarlaDataProvider

from agents.tools.config_creation import LaunchConfig, LunaticAgentSettings

from classes.keyboard_controls import PassiveKeyboardControl, RSSKeyboardControl

from classes.constants import Phase
from classes.worldmodel import GameFramework, WorldModel, AD_RSS_AVAILABLE

from agents.tools.logging import logger
from agents.tools.misc import draw_waypoints

from agents.lunatic_agent import LunaticAgent
from agents.rules import create_default_rules

# ==============================================================================
# DEBUG

PRINT_CONFIG = False
PRINT_RULES = False
FPS = 10

# ==============================================================================
# -- Game Loop ---------------------------------------------------------
# ==============================================================================

def game_loop(args: Union[argparse.ArgumentParser, LaunchConfig]):
    """
    Main loop of the simulation. It handles updating all the HUD information,
    ticking the agent and, if needed, the world.
    """
    game_framework : GameFramework = None # Set for finally block
    traffic_manager : carla.TrafficManager = None # Set for finally block
    world_model : WorldModel = None # Set for finally block
    agent : LunaticAgent = None # Set for finally block
    ego : carla.Vehicle = None # Set for finally block
    spawned_vehicles : List[carla.Actor] = [] # Set for finally block
    
    args.seed = 631 # TEMP

    # -- Load Settings Agent --

    print("Creating settings")
    # Validates and creates the agent settings. Sidenote: agent_config a copy of args.agent,
    # you can access args.agent as copy of the original settings
    # To not validate the config against LunaticAgentSettings, you can use OmegaConf.create(args.agent)
    # to create a copy.
    agent_config = LunaticAgentSettings.create_from_args(args.agent)

    # TEMP
    import classes.worldmodel
    classes.worldmodel.AD_RSS_AVAILABLE = classes.worldmodel.AD_RSS_AVAILABLE and agent_config.rss and agent_config.rss.enabled
    
    if PRINT_CONFIG:
        print("    \n\n\n")
        pprint(agent_config)
        from agents.tools.config_creation import AgentConfig
        if isinstance(agent_config, AgentConfig):
            print(agent_config.to_yaml())
        else:
            try:
                print(OmegaConf.to_yaml(agent_config))
            except Exception as e:
                pprint(agent_config)
    
    try:
        logger.info("Creating Game Framework ...")
        game_framework = GameFramework(args)
        logger.info("Created Game Framework.\n")
        
        # -- Spawn Vehicles --
        all_spawn_points = game_framework.map.get_spawn_points()
        spawn_points = launch_tools.csv_tools.csv_to_transformations("examples/highway_example_car_positions.csv")
        
        ego_bp, car_bp = launch_tools.blueprint_helpers.get_contrasting_blueprints(game_framework.world)
        
        # Spawn Others
        how_many = 33
        ego_spawn_idx = 3
        traffic_manager = game_framework.init_traffic_manager(CarlaDataProvider.get_traffic_manager_port())
        spawned_vehicles = CarlaDataProvider.request_new_batch_actors("vehicle.tesla.model3", 
                                                                      how_many, 
                                                                      spawn_points=[sp for i, sp in enumerate(spawn_points[:how_many+1]) if i != ego_spawn_idx], 
                                                                      autopilot=True, 
                                                                      tick=False)
        
        # Spawn Ego
        start : carla.libcarla.Transform = spawn_points[ego_spawn_idx]
        ego = game_framework.spawn_actor(ego_bp, start, must_spawn=True)
        spawned_vehicles.append(ego)
        
        
        logger.info("Creating agent and WorldModel ...")
        agent, world_model, global_planner, controller \
            = game_framework.init_agent_and_interface(ego=None if args.externalActor else ego, # TEMP # Test external actor, do not pass ego
                                                      agent_class=LunaticAgent, 
                                                      config=agent_config)
        logger.debug("Created agent and WorldModel.\n")
        
        # Add Rules:
        default_rules = create_default_rules()
        from agents.rules.lane_changes import RandomLaneChangeRule
        for rule in default_rules:
            if isinstance(rule, RandomLaneChangeRule):
                rule.enabled = False
        agent.add_rules(default_rules)
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
        
        agent.set_destination(last_wp.transform.location)
        
        def loop():
            agent.verify_settings()
            while game_framework.continue_loop:
                
                # Do not use LunaticAgent but traffic manager
                if controller._autopilot_enabled:
                    if controller.parse_events(None):
                        return
                    continue
                
                # Agent Loop
                with game_framework:
                    # ------ Run step ------
                    planned_control = agent.run_step(debug=True)
                    
                    # ------ Apply / Handle User Input ------
                    
                    # Controls can be updated by the user.
                    try:
                        # -> Phase.APPLY_MANUAL_CONTROLS | Phase.BEGIN
                        agent.parse_keyboard_input(allow_user_updates=True)
                        # -> Phase.APPLY_MANUAL_CONTROLS | Phase.END
                    except GameFramework.exceptions.UserInterruption:
                        return    
                    
                    # ------ Apply Control ------
                    
                    # > Phase.EXECUTION | Phase.BEGIN
                    agent.apply_control()
                    # > Phase.EXECUTION | Phase.END
                    
                    # ------ End of Loop ------
                    
                    # Debug drawing of the route
                    try:
                        destination = agent._local_planner._waypoints_queue[-1][0].transform.location # TODO find a nicer way
                        destination = destination + carla.Vector3D(0, 0, 1.5) # elevate to be not in road
                    except IndexError:
                        pass
                    game_framework.debug.draw_point(destination, life_time=0.5)
                
                # -- Stop Loop or Continue when agent is done --
                
                if args.loop and not game_framework.continue_loop and agent.done():
                    # TODO: Rule / Action to define next waypoint
                    print("The target has been reached, searching for another target")
                    world_model.hud.notification("Target reached", seconds=4.0)
                    
                    # Set new destination
                    # Choose a random point anywhere
                    #destination = random.choice(spawn_points).location
                    
                    # Choose a random point nearby.
                    wp = agent._current_waypoint.next(50)[-1]
                    next_wp = random.choice((wp, wp.get_left_lane(), wp.get_right_lane()))
                    if next_wp is None:
                        next_wp = wp
                    destination = next_wp.transform.location
                    
                    # Set new destination and indicate that we continue
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
        raise
    finally:
        print("Quitting. - Destroying actors and stopping world.")
        pygame.quit()
        if agent is not None:
            agent.destroy()
        if world_model is not None:
            world_model.destroy(destroy_ego=False)
        if game_framework is not None:
            # save world for usage after CDP cleanup
            game_framework.cleanup() # includes/or is CarlaDataProvider.cleanup()
        else:
            CarlaDataProvider.cleanup() # NOTE: unsets world, map, client, destroys actors
        agent = None
        world_model = None
        game_framework = None


# ==============================================================================
# -- main() --------------------------------------------------------------
# ==============================================================================

@hydra.main(version_base=None, config_path="./conf", config_name="launch_config")
def main(args: LaunchConfig):
    """Main method"""

    log_level = logging.DEBUG if args.debug else logging.INFO
    
    logger.setLevel(log_level)
    logger.info('listening to server %s:%s', args.host, args.port)
        
    print(__doc__)
    print(RSSKeyboardControl.get_docstring())
    print("Launch Arguments:\n", OmegaConf.to_yaml(args), sep="")

    args = LaunchConfig.check_config(args, args.get("strict_config", 3), as_dict_config=True)
    
    signal.signal(signal.SIGINT, RSSKeyboardControl.signal_handler)

    try:
        game_loop(args)
        
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')

if __name__ == '__main__':
    main()
