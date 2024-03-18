import os
import pygame
from omegaconf import OmegaConf
from hydra import compose, initialize_config_dir

from agents.lunatic_agent import LunaticAgent

from classes.constants import Phase
from classes.keyboard_controls import RSSKeyboardControl
from classes.worldmodel import GameFramework, WorldModel
from agents.tools.logging import logger
from agents.tools.config_creation import LaunchConfig, LunaticAgentSettings
from leaderboard.autoagents.autonomous_agent import AutonomousAgent
from leaderboard.autoagents.autonomous_agent import Track

from srunner.scenariomanager.carla_data_provider import CarlaDataProvider

def get_entry_point():
    print("Getting entry point")
    return "LunaticChallenger"

hydra_initalized = False
import logging
logger.setLevel(logging.DEBUG)


class LunaticChallenger(AutonomousAgent, LunaticAgent):
    
    def __init__(self, carla_host, carla_port, debug=False):
        print("Initializing LunaticChallenger")
        self.world_model: WorldModel = None
        self.game_framework: GameFramework = None
        super().__init__(carla_host, carla_port, debug)

    def setup(self, path_to_conf_file):
        self.track = Track.MAP
        print("Setup with conf file", path_to_conf_file)
        logger.info("Setup with conf file %s", path_to_conf_file)
        config_dir, config_name = os.path.split(path_to_conf_file)
        global hydra_initalized
        if not hydra_initalized:
            initialize_config_dir(version_base=None, 
                                    config_dir=config_dir, 
                                    job_name="test_app")
            self.args: LaunchConfig = compose(config_name=config_name)
            print(OmegaConf.to_yaml(self.args))
            hydra_initalized = True
            self.args.map = None # Let scenario manager decide
            self.args.sync = None
        
        sim_world = CarlaDataProvider.get_world()
        map_inst = CarlaDataProvider.get_map()
        
        config = LunaticAgentSettings.create_from_args(self.args.agent)
        config.planner.dt = 1/20 # TODO: maybe get from somewhere
        
        self.game_framework = GameFramework(self.args, config)
        print("Game framework setup")
        # TODO: How to make args optioal
        self.world_model = WorldModel(config, args=self.args)
        self.game_framework.world_model = self.world_model
        print("World Model setup")
        self.controller = self.game_framework.make_controller(self.world_model, RSSKeyboardControl, start_in_autopilot=False) # Note: stores weakref to controller
        print("Initializing agent")
        LunaticAgent.__init__(self, config, self.world_model, map_inst=map_inst, grp_inst=CarlaDataProvider.get_global_route_planner())
        self.game_framework.agent = self # TODO: Remove this circular reference
        self.agent_engaged = False

    def run_step(self, input_data, timestamp):
        try:
            print("Running step")
            print("Input data", input_data)
            self.agent_engaged = True
            with self.game_framework:
                control = super(AutonomousAgent, self).run_step(debug=self.args.debug) # Call Lunatic Agent run_step
            # Handle render updates
            self.execute_phase(Phase.EXECUTION | Phase.BEGIN, prior_results=control)
            return control
        except Exception as e:
            logger.error("Error in LunaticChallenger.run_step:", exc_info=True)
            self.destroy()
            raise e
    
    def destroy(self):
        print("Destroying")
        super().destroy()
        if self.world_model:
            self.world_model.destroy()
            self.world_model = None
        if self.game_framework:
            self.game_framework.agent = None
            self.game_framework = None
        pygame.quit()
        print("Destroyed", self)
