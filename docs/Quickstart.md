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
    
    1. Alternatively you can use the provided `run_leaderboard_agent.sh` script to test the `LunaticChallenger`.
        :::warning
        :bulb: The default route (Town10HD) is loaded faster, however its speed is sometimes worse than the big Town12 that takes longer to load.
        Consider turning off `ENABLE_DATA_MATRIX` or `ENABLE_RSS` to gain performance.

Additionally, for controlling the driving AI during simulation, you can utilize the hotkeys implemented using Pygame. In-game, you can press the 'H' key to view the controls or refer to the full list of keyboard controls the [Appendix](#Keyboard-Controls).