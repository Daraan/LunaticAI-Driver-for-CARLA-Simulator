# Quickstart

To quickly start using the project with the LunaticAI Driver for CARLA simulator, follow these initial steps:

1. Begin by launching the CARLA simulator environment. Ensure it is properly configured and running on your system. 

2. Next, navigate to the project directory where you have cloned the repository. Use the provided scripts and configurations to initiate the driving AI within CARLA. For a quickstart run this minimal setup script:
    
    ```shell
    python examples/minimal.py
    ```
    
    Alternatively you can construct a minimal example in the following way:
    
    ```python
    from agents.lunatic_agent import LunaticAgent
    from classes.worldmodel import GameFramework

    # Sets up Carla and Pygame, and Hydra in a limited way
    game_framework = GameFramework.quickstart()

    ego = GameFramework.request_new_actor("car", rolename="hero", random_location=True)

    # Create a lunatic agent
    agent = LunaticAgent(game_framework.agent_config, vehicle=ego)

    try:
        while game_framework.continue_loop:
            with game_framework(agent):
                agent.run_step()
                # Use the mouse to override the agents controls; use ESC to quit
                if game_framework.controller.parse_events(agent.get_control()):
                    break
                agent.apply_control()
    except:
        # Destroy spawned actors
        game_framework.cleanup()
        raise
    ```
    
    ```{warning}
    :warning: Note that this setup omits some steps and does not provide access too all features. Look into [AgentGameLoop.py](https://github.com/Daraan/LunaticAI-Driver-for-CARLA-Simulator/blob/main/AgentGameLoop.py) for a comprehensive setup.
    ```
    
    3. Alternatively you can use the provided `run_leaderboard_agent.sh` script to test the `LunaticChallenger`.
        ```{warning}
        :bulb: The default route (Town10HD) is loaded faster, however its speed is sometimes worse than the big Town12 that takes longer to load.
        Consider turning off `ENABLE_DATA_MATRIX` or `ENABLE_RSS` to gain performance, inside the `leaderboard_agent.py` or `conf/agent/leaderboard.yaml`.
        ```

Additionally, for controlling the driving AI during simulation, you can utilize the hotkeys implemented using Pygame. In-game, you can press the 'H' key to view the controls or refer to the full list of keyboard controls the [Keyboard Controls](#Keyboard-Controls).

## External Setup: Using the ScenarioRunner and other Initializations

During the agents creation the script waits until an external actor is found, by default named `hero`. This allows the `LunaticAgent` to be used with other scripts that set up the scenario and spawn this special actor. To initialize a route the agent should follow call:

```python!
# CARLA's BasicAgent interface
# plan: list of [carla.Waypoint, RoadOption] representing the route to be followed
lunatic_agent.set_global_plan(plan, clean_queue=True):

# leaderboard AutonomousAgent interface
# global_plan_gps: "tuple[Dict[str, float], RoadOption]"
# global_plan_world_coord: "tuple[carla.Transform, RoadOption]"
lunatic_challenger.set_global_plan(global_plan_gps, global_plan_world_coord)
```

```{danger}
:warning: For performance and interface reasons the LunaticAgent uses the [`CarlaDataProvider`](https://github.com/carla-simulator/scenario_runner/blob/master/srunner/scenariomanager/carla_data_provider.py) from the [scenario runner](https://github.com/carla-simulator/scenario_runner) as a backbone to access global information.

**To detect actors, all actors must be spawned over the CarlaDataProvider and the LunaticAgent must have access to the same CarlaDataProvider object**
```


## Keyboard Controls

Depending on the setup certain keys, e.g. *WASD* or user input, will not work, also user input can be disabled when calling `agent.parse_keyboard_input(False)`.

```
Use ARROWS or WASD keys for control.

        W            : throttle
        S            : brake
        AD           : steer
        Q            : toggle reverse
        Space        : hand-brake
        P            : toggle autopilot (depends on setup)

        TAB          : change view
        Backspace    : change vehicle

        R            : toggle recording images to disk

        F2           : toggle RSS visualization mode
        F3           : increase log level
        F4           : decrease log level
        F5           : increase map log level
        F6           : decrease map log level
        B            : toggle RSS Road Boundaries Mode
        G            : RSS check drop current route (experimental)
        T            : toggle RSS (NotImplemented)
        N            : pause simulation (only slow down)

        F1           : toggle HUD
        H/?          : toggle help
        ESC          : quit
```