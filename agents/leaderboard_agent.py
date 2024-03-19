import os
import pygame
from omegaconf import OmegaConf
from hydra import compose, initialize_config_dir

from leaderboard.autoagents.autonomous_agent import AutonomousAgent
from leaderboard.autoagents.autonomous_agent import Track
from srunner.scenariomanager.carla_data_provider import CarlaDataProvider

from agents.lunatic_agent import LunaticAgent

from classes.constants import Phase
from classes.keyboard_controls import RSSKeyboardControl
from classes.worldmodel import GameFramework, WorldModel, AD_RSS_AVAILABLE
from agents.tools.logging import logger
from agents.tools.config_creation import LaunchConfig, LunaticAgentSettings


hydra_initalized = False
import logging
logger.setLevel(logging.DEBUG)


def get_entry_point():
    print("Getting entry point")
    return "LunaticChallenger"

# TODO: Pack this in an extra config
WORLD_MODEL_DESTROY_SENSORS = True
ENABLE_RSS = True and AD_RSS_AVAILABLE
ENABLE_DATA_MATRIX = True

DATA_MATRIX_ASYNC = True
DATA_MATRIX_TICK_SPEED = 60

class UserInterruption(Exception):
    """
    Terminate the run_step loop if user input is detected.
    
    Allow the scenario runner and leaderboard to exit gracefully.
    """

args: LaunchConfig 
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
        global args
        if not hydra_initalized:
            initialize_config_dir(version_base=None, 
                                    config_dir=config_dir, 
                                    job_name="test_app")
            args = compose(config_name=config_name)
            hydra_initalized = True
            # Let scenario manager decide
            args.map = None
            args.sync = None
            args.handle_ticks = False # Assure that this is false
            args.gamma = 3.3
            
            args.agent.data_matrix.enabled = ENABLE_DATA_MATRIX
            args.agent.data_matrix.sync = not DATA_MATRIX_ASYNC
            args.agent.data_matrix.sync_interval = DATA_MATRIX_TICK_SPEED
            args.agent.rss.enabled = ENABLE_RSS
            print(OmegaConf.to_yaml(args))
        self.args = args
        
        sim_world = CarlaDataProvider.get_world()
        map_inst = CarlaDataProvider.get_map()
        
        config = LunaticAgentSettings.create_from_args(self.args.agent, assure_copy=True)
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
        self._destroyed = False
        
    def sensors(self):
        sensors: list = super().sensors()
        sensors.extend([
            {'type': 'sensor.opendrive_map', 'reading_frequency': 1, 'id': 'OpenDRIVE'},
        ])
        return sensors

    @staticmethod
    def _print_input_data(input_data):
        if not input_data:
            print("No input data:", input_data)
            return
        print("=====================>")
        for key, val in input_data.items():
            if hasattr(val[1], 'shape'):
                shape = val[1].shape
                print("[{} -- {:06d}] with shape {}".format(key, val[0], shape))
            else:
                print("[{} -- {:06d}] ".format(key, val[0]))
        print("<=====================")

    def run_step(self, input_data, timestamp):
        try:
            self._print_input_data(input_data)
            self.agent_engaged = True
            with self.game_framework:
                control = super(AutonomousAgent, self).run_step(debug=self.args.debug) # Call Lunatic Agent run_step
            # Handle render updates
            
            self.execute_phase(Phase.APPLY_MANUAL_CONTROLS | Phase.BEGIN, prior_results=control)
            if self.controller.parse_events(self.get_control()):
                print("Exiting by user input.")
                raise UserInterruption("Exiting by user input.")
            self.execute_phase(Phase.APPLY_MANUAL_CONTROLS | Phase.END, prior_results=None)
            
            self.execute_phase(Phase.EXECUTION | Phase.BEGIN, prior_results=control)
            return control
        except Exception as e:
            if not isinstance(e, UserInterruption):
                logger.error("Error in LunaticChallenger.run_step:", exc_info=True)
            self.destroy()
            raise e
    
    def destroy(self):
        self._destroyed = True
        print("Destroying Lunatic Challenger")
        self._road_matrix_updater.stop()
        super().destroy()
        if self.world_model:
            if not WORLD_MODEL_DESTROY_SENSORS:
                self.world_model.actors.clear()
            self.world_model.destroy()
            self.world_model = None
        if self.game_framework:
            self.game_framework.agent = None
            self.game_framework = None
        pygame.quit()
        print("Destroyed", self)
        
    def __del__(self):
        if not self._destroyed:
            self.destroy()
