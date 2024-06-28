import os, sys
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
            agent.run_step()
            # Use the mouse to override the agents controls; use ESC to quit
            if game_framework.controller.parse_events(agent.get_control()):
                break
            agent.apply_control()
except:
    game_framework.cleanup()
    raise