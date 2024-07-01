#!/usr/bin/env python
"""

Example of the agent system

Based on German Ros's (german.ros@intel.com) example of automatic_control shipped with carla.
"""
from __future__ import print_function  # for python 2.7 compatibility

import argparse
import random
from typing import List, Union
from pprint import pprint

import hydra
from omegaconf import OmegaConf

"""When you use an .egg file be sure to add it to your $PYTHONPATH"""
try:
    import carla
except ImportError as e:
    from launch_tools import carla

import pygame
from classes import exceptions
import launch_tools
    
from launch_tools import CarlaDataProvider

from agents.tools.config_creation import LaunchConfig, LunaticAgentSettings

from classes.keyboard_controls import PassiveKeyboardControl, RSSKeyboardControl

from classes.constants import Phase
from classes.worldmodel import GameFramework, WorldModel, AD_RSS_AVAILABLE

from agents.tools.logging import logger
from agents.tools.misc import debug_drawing

from agents.lunatic_agent import LunaticAgent
from agents.rules import create_default_rules

# ==============================================================================
# DEBUG
# ==============================================================================
PRINT_RULES = True

# ==============================================================================
# -- Game Loop ---------------------------------------------------------
# ==============================================================================

def game_loop(args: Union[argparse.ArgumentParser, LaunchConfig]):
    """
    Main loop of the simulation. It handles updating all the HUD information,
    ticking the agent and, if needed, the world.
    """
    # Avoid name errors
    game_framework : GameFramework = None         # Set for finally block
    world_model : WorldModel = None               # Set for finally block
    agent : LunaticAgent = None                   # Set for finally block
    ego : carla.Vehicle = None                    # Set for finally block

    # -- Load Settings Agent --

    print("--- Creating settings ---")
    # Validates and creates the agent settings. Sidenote: agent_config a copy of args.agent,
    # you can access args.agent as copy of the original settings
    # To not validate the config against LunaticAgentSettings, you can use OmegaConf.create(args.agent)
    # to create a copy.
    agent_config = LunaticAgentSettings.create_from_args(args.agent)
    
    try:
        logger.info("Creating Game Framework ...")
        game_framework = GameFramework(args)
        
        # -- Spawn Vehicles --
        spawn_points = launch_tools.csv_tools.csv_to_transformations("examples/highway_example_car_positions.csv")
        
        ego_bp, car_bp = launch_tools.blueprint_helpers.get_contrasting_blueprints(game_framework.world)
        
        # Spawn Others
        how_many = 4
        ego_spawn_idx = -12
        CarlaDataProvider.request_new_batch_actors("vehicle.tesla.model3", 
                                                                      how_many, 
                                                                      spawn_points=[sp for i, sp in enumerate(spawn_points[:how_many+1]) if i != ego_spawn_idx], 
                                                                      autopilot=True, 
                                                                      tick=False)
        
        # Spawn Ego
        start : carla.libcarla.Transform = spawn_points[ego_spawn_idx]
        ego = game_framework.spawn_actor(ego_bp, start, must_spawn=True)
        
        logger.info("Creating agent and WorldModel ...")
        agent, world_model, global_planner, controller \
            = game_framework.init_agent_and_interface(ego=None if args.externalActor else ego, # TEMP # Test external actor, do not pass ego
                                                      agent_class=LunaticAgent, 
                                                      config=agent_config)
        logger.debug("Created agent and WorldModel.\n")
        
        # Add Rules:
        #agent.add_rules(create_default_rules(game_framework))
        
        # NOTE: the default rules can be added over the yaml interface. To add them in a functional way, use the following code:
        if not any("create_default_rules" in rule_config._target_ for rule_config in agent_config.rules):
            default_rules = create_default_rules()
            agent.add_rules(default_rules)
                
        if PRINT_RULES: # Note: this can be a bit messy as some attributes have a long repr
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
        
        """
        An example how to construct a loop for the agent.
        """
        agent.verify_settings() # Validate if the planner.dt is set up, should match the simulation time delta.
        
        """
        This is the main loop, raising for example a AgentDoneException inside the
        with game_framework context will set game_frame.continue_loop to False.
        """
        while game_framework.continue_loop:
            
            """
            The `with game_framework` context manager takes care of background tasks
            like world tick, HUD update, and is an exception handler for the agent.
            """
            with game_framework:
                # ------ Run step ------
                
                """
                The agent.run_step is the main method in which the agent
                calculates the next vehicle control object.
                """
                planned_control = agent.run_step(debug=True)
                
                # ------ Apply / Handle User Input ------
                
                """
                Afterwards the user can manipulate these controls.
                If this is not wanted set allow_user_updates=False.
                
                The user will then only be able to use the other keyboard
                hotkeys like quitting the game or changing other settings.
                
                See the documentation of the keyboard controls for more information.
                """
                try:
                    # -> Phase.APPLY_MANUAL_CONTROLS | Phase.BEGIN
                    agent.parse_keyboard_input(allow_user_updates=True)
                    # -> Phase.APPLY_MANUAL_CONTROLS | Phase.END
                except exceptions.UserInterruption:
                    return    
                
                # ------ Apply Control ------
                
                """
                The final step is to apply the controls to the vehicle.
                Rules that execute at Phase.EXECUTION | Phase.BEGIN can
                still manipulate or exchange the final controls.
                """
                # > Phase.EXECUTION | Phase.BEGIN
                agent.apply_control()
                # > Phase.EXECUTION | Phase.END
                
                # ------ End of Loop ------
                
                """Draw route information and junctions"""
                if game_framework._args.debug:
                    debug_drawing(agent, game_framework, destination)
            
            # -- Stop Loop or Continue when agent is done --
            
            """
            Here is checked if the agent has reached its destination and has no
            no rule or other function has done a replanning. A custom new destination 
            can be set here.
            """
            if args.loop and not game_framework.continue_loop and agent.done():
                print("The target has been reached, searching for another target")
                world_model.hud.notification("Target reached", seconds=4.0)
                
                # Option 1 : Choose a random point anywhere
                #destination = random.choice(spawn_points).location
                
                # Option 2 : Choose a random point nearby.
                wp = agent._current_waypoint.next(50)[-1]
                next_wp = random.choice((wp, wp.get_left_lane(), wp.get_right_lane()))
                if next_wp is None:
                    next_wp = wp
                destination = next_wp.transform.location
                
                """
                After a new destination has been set, these steps should be executed
                to allow a smooth continuation of the agent.
                """
                agent.set_destination(destination)
                game_framework.continue_loop = True # if not set to True we will exit the loop
                agent.execute_phase(Phase.DONE| Phase.END, prior_results=None)
        
            # Optional: final phase of agents lifetime; could be used for cleanup tasks.
        agent.execute_phase(Phase.TERMINATING | Phase.END, prior_results=None)

    # Adding exception block   
    except Exception as e:
        print("ERROR, exception in game loop", e)
        logger.error("Exception in game loop", exc_info=True)
        raise
    finally:
        """Cleanup the simulation by removing the used actors"""
        print("Quitting. - Destroying actors and stopping world.")
        pygame.quit()
        if agent is not None:
            agent.destroy()
        if world_model is not None:
            world_model.destroy(destroy_ego=False)
        if game_framework is not None:
            # save world for usage after CDP cleanup
            game_framework.cleanup()    # includes/or is CarlaDataProvider.cleanup()
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
    """
    This is the main function wrapped py @hydra that takes care of the configuration
    merge and sets up logging.
    
    Args:
        args (LaunchConfig): The configuration object that is created by Hydra, it
            contains all the settings from the yaml files merged with the command line
            arguments. From a high-level perspective is it a dictionary that also allows
            dot access to its keys, e.g. args.host instead of args["host"].
    
    See Also:
        - https://hydra.cc/
        - [Tab Completion](https://hydra.cc/docs/tutorials/basic/running_your_app/tab_completion/)
        - [Hydra Config](https://hydra.cc/docs/configure_hydra/intro/)
        - [Default List - How config files are merged](https://hydra.cc/docs/advanced/defaults_list/)
        - [Override Grammar](https://hydra.cc/docs/advanced/override_grammar/basic/)
    """

    logger.info('listening to server %s:%s', args.host, args.port)
        
    print(__doc__)
    print(RSSKeyboardControl.get_docstring())
    print("Launch Arguments:\n", OmegaConf.to_yaml(args), sep="")

    # Validate the config for keys
    args = LaunchConfig.check_config(args, args.get("strict_config", 3), as_dict_config=True)
    
    try:
        game_loop(args)
        
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')

if __name__ == '__main__':
    main()
