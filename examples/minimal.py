"""A minimal example to show how to initialize the agent."""
import os
import sys

# Be sure to be in the root-folder of the project
if "agents" not in os.getcwd():
    print(os.getcwd())
    sys.path.insert(0, os.getcwd())

from agents.lunatic_agent import LunaticAgent
from classes.worldmodel import GameFramework

# Sets up Carla and Pygame, and Hydra in a minimal way
game_framework = GameFramework.quickstart()
ego = GameFramework.request_new_actor("car", rolename="hero", random_location=True)

# Create a lunatic agent, it will look for a vehicle named 'hero' automatically
agent = LunaticAgent(game_framework.agent_config)

try:
    while game_framework.continue_loop:
        with game_framework(agent):
            # run_step() returns the control
            # update it inplace or use agent.set_control(control) to replace it.
            control = agent.run_step()
            # Use the mouse to override the agents controls; use ESC to quit
            agent.parse_keyboard_input()
            agent.apply_control()
except GameFramework.exceptions.UserInterruption:
    pass
finally:
    game_framework.cleanup()
