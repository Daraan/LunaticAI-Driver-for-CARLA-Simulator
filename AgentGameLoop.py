#!/usr/bin/env python
"""
Example of a game loop for the :py:class:`.LunaticAgent` class.
"""

import random
from pprint import pprint

import hydra
from omegaconf import OmegaConf

# When you use an .egg file be sure to add it to your $PYTHONPATH
try:
    import carla
except ImportError:
    from launch_tools import carla
import pygame

import launch_tools
from agents.lunatic_agent import LunaticAgent
from agents.rules import create_default_rules
from agents.tools.config_creation import AsDictConfig, LaunchConfig, LunaticAgentSettings
from agents.tools.debug_drawing import debug_drawing
from agents.tools.logs import logger
from classes import exceptions
from classes.constants import Phase
from classes.ui.keyboard_controls import RSSKeyboardControl  # Alternative: PassiveKeyboardControl
from classes.worldmodel import GameFramework, WorldModel

# ==============================================================================
# Globals
# ==============================================================================

AMOUNT_ACTORS = 12
"""How many other actors to spawn"""

EGO_SPAWN_IDX = 3
"""Changes the start position of the ego vehicle"""

PRINT_RULES = False
"""Print the rules to the console. This is messy."""

# ==============================================================================
# -- Game Loop ---------------------------------------------------------
# ==============================================================================


def game_loop(args: LaunchConfig):
    r"""
    Main loop of the simulation.
    
    It sets up the simulation, spawns the vehicles, and initializes the agent.
    In the :python:`while` loop, the agent calculates one `\`carla.VehicleControl\`:py:class:`:external-icon-parse:
    every iteration.
    
    The `.GameFramework`:py:class: context manager takes care of the simulation tick,
    and camera updates.
    """
    # Avoid name errors in final block
    game_framework: GameFramework = None
    world_model: WorldModel = None
    agent: LunaticAgent = None
    ego: carla.Vehicle = None

    # -- Load Settings Agent --

    print("--- Creating settings ---")
    # Validates and creates the agent settings. Sidenote: agent_config a copy of args.agent,
    # you can access args.agent as copy of the original settings
    # To not validate the config against LunaticAgentSettings use OmegaConf.create(args.agent)
    # to create a copy.

    agent_config: AsDictConfig[LunaticAgentSettings] = LunaticAgentSettings.create(settings=args.agent)
    
    try:
        logger.info("Creating Game Framework ...")
        game_framework = GameFramework(args)
        
        # -- Spawn Vehicles --
        spawn_points = launch_tools.csv_tools.csv_to_transformations("examples/highway_example_car_positions.csv")
        
        ego_bp, car_bp = launch_tools.blueprint_helpers.get_contrasting_blueprints()
        
        # Spawn Others
        GameFramework.request_new_batch_actors("vehicle.tesla.model3",
                                                    AMOUNT_ACTORS,
                                                    spawn_points=[sp for i, sp in enumerate(spawn_points[:AMOUNT_ACTORS + 1])
                                                                     if i != EGO_SPAWN_IDX],
                                                    autopilot=True,
                                                    tick=False)
        
        # Spawn Ego
        start: carla.libcarla.Transform = spawn_points[EGO_SPAWN_IDX]
        ego = game_framework.spawn_actor(ego_bp, start, must_spawn=True)  # type: ignore[assignment]
        
        logger.info("Creating agent and WorldModel ...")

        agent, world_model, global_planner, controller \
            = game_framework.init_agent_and_interface(ego=None if args.externalActor else ego,  # Test externalActor
                                                      agent_class=LunaticAgent,
                                                      config=agent_config)
        logger.debug("Created agent and WorldModel.\n")
        
        # Add Rules:
        #agent.add_rules(create_default_rules(game_framework))
        
        # NOTE: the default rules can be added over the yaml interface. To add them in a functional way, use the following code:
        if not any("create_default_rules" in rule_config._target_ for rule_config in agent_config.rules):
            default_rules = create_default_rules()
            agent.add_rules(default_rules)
                
        if PRINT_RULES:  # NOTE: this can be a bit messy as some attributes have a long repr
            print("Lunatic Agent Rules")
            pprint(agent.rules)
        
        # -- Scenario --
        
        # Set initial destination
        wp_start = world_model.map.get_waypoint(start.location)

        next_wps: "list[carla.Waypoint]" = wp_start.next(50)
        last_wp = next_wps[-1]
        left_last_wp = last_wp.get_left_lane()
        if left_last_wp is not None:
            print(left_last_wp, world_model.map.get_waypoint(left_last_wp.transform.location))
            
            # destination = random.choice(all_spawn_points).location
            destination = left_last_wp.transform.location
        else:
            destination = last_wp.transform.location
        
        agent.set_destination(last_wp.transform.location)
        
        """
        An example how to construct a loop for the agent.
        """
        agent.verify_settings()  # Validate if the planner.dt is set up, should match the simulation time delta.
        
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
                planned_control = agent.run_step(debug=True)  # noqa: F841
                
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
                if game_framework.launch_config.debug:
                    try:
                        debug_drawing(agent, game_framework, destination)
                    except Exception:
                        logger.debug("Error in debug drawing", exc_info=True)
            
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
                game_framework.continue_loop = True  # if not set to True we will exit the loop
                agent.execute_phase(Phase.DONE | Phase.END, prior_results=None)
        
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
        if agent is not None:
            agent.destroy()
        if world_model is not None:
            world_model.destroy(destroy_ego=False)
        if game_framework is not None:
            # save world for usage after CDP cleanup
            game_framework.cleanup()    # includes/or is CarlaDataProvider.cleanup()

        pygame.quit()

# ==============================================================================
# -- main() --------------------------------------------------------------
# ==============================================================================


@hydra.main(version_base=None, config_path="./conf", config_name="launch_config")
def main(args: LaunchConfig):
    """
    This is the main function wrapped with the `@hydra <https://hydra.cc/docs/intro/>`_ method that takes care of the configuration
    merge and sets up logging.
    
    Args:
        args : The configuration object that is created by Hydra_, it
            contains all the settings from the YAML files merged with the command line
            arguments. From a high-level perspective is it a dictionary that also allows
            dot access to its keys, e.g. :python:`args.host` instead of :python:`args["host"]`.
    
    See Also:
        - https://hydra.cc/
        - `Hydra Config Intro <https://hydra.cc/docs/configure_hydra/intro/>`_
        - `Default List - How config files are merged <https://hydra.cc/docs/advanced/defaults_list/>`_
        - `Override Grammar <https://hydra.cc/docs/advanced/override_grammar/basic/>`_
        - `Hydra Tab Completion <https://hydra.cc/docs/tutorials/basic/running_your_app/tab_completion/>`_
    """
    logger.info('listening to server %s:%s', args.host, args.port)
        
    print(__doc__)
    print(RSSKeyboardControl.get_docstring())
    print("Launch Arguments:\n", OmegaConf.to_yaml(args), sep="")

    # Validate the config for keys
    args = LaunchConfig.check_config(args, args.get("strict_config", 3), as_dict_config=True)
    
    try:
        # Optional: If you return a result object it will be logged by Hydra's on_job_end callback
        result = game_loop(args)
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    else:
        return result


# pyright: reportAssignmentType=none
if __name__ == '__main__':
    main()
