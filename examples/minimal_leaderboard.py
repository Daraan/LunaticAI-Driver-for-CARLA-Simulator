import os, sys
# Be sure to be in the root-folder of the project
if "agents" not in os.getcwd():
    print(os.getcwd())
    sys.path.insert(0, os.getcwd())

from agents.leaderboard_agent import LunaticChallenger
from classes.worldmodel import GameFramework

# Sets up Carla and Pygame, and Hydra in a minimal way
game_framework = GameFramework.quickstart()

ego = GameFramework.request_new_actor("car", rolename="hero", random_location=True)

# Create a lunatic agent
agent = LunaticChallenger("localhost", carla_port=2000)
agent.setup(game_framework.launch_config) # Do not forget this step!
try:
    while game_framework.continue_loop:
        with game_framework(agent):
            agent.run_step(None, None)
            # Use the mouse to override the agents controls; use ESC to quit
            if game_framework.controller.parse_events(agent.get_control()):
                break
            agent.apply_control()
except:
    game_framework.cleanup()
    raise
