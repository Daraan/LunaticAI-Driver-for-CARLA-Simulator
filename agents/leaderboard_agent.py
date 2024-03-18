import os
from omegaconf import OmegaConf
from hydra import compose, initialize_config_dir

from agents.lunatic_agent import LunaticAgent

from classes.keyboard_controls import RSSKeyboardControl
from classes.worldmodel import GameFramework, WorldModel
from agents.tools.config_creation import LaunchConfig, LunaticAgentSettings
from leaderboard.autoagents.autonomous_agent import AutonomousAgent
from leaderboard.autoagents.autonomous_agent import Track

from srunner.scenariomanager.carla_data_provider import CarlaDataProvider


def get_entry_point():
    return "LunaticChallenger"

class LunaticChallenger(AutonomousAgent, LunaticAgent):
    
    def __init__(self, carla_host, carla_port, debug=False):
        super().__init__(carla_host, carla_port, debug)

    def setup(self, path_to_conf_file):
        self.track = Track.MAP
        print("Setup with conf file", path_to_conf_file)
        config_dir, config_name = os.path.split(path_to_conf_file)
        with initialize_config_dir(version_base=None, 
                                   config_dir=config_dir, 
                                   job_name="test_app"):
            args: LaunchConfig = compose(config_name=config_name)
            print(OmegaConf.to_yaml(args))
        
        
        sim_world = CarlaDataProvider.get_world()
        map_inst = CarlaDataProvider.get_map()
        
        #args = OmegaConf.load("/home/dsperber/TeamProject/LunaticAI-Driver-for-CARLA-Simulator/conf/launch_config.yaml")
        args.map = None # Let scenario manager decide
        args.sync = None
        
        #behavior = LunaticAgentSettings()#.from_yaml(path_to_conf_file)
        #config = behavior.make_config()
        config = LunaticAgentSettings.create_from_args(args.agent)
        self.game_framework = GameFramework(args, config)
        print("Game framework setup")
        # TODO: How to make args optioal
        world_model = WorldModel(config, args=args)
        print("World Model setup")
        controller = self.game_framework.make_controller(self.world_model, RSSKeyboardControl, start_in_autopilot=False) # Note: stores weakref to controller
        print("Initializing agent")
        LunaticAgent.__init__(self, config, world_model, map_inst=map_inst, grp_inst=CarlaDataProvider.get_global_route_planner())
        self.agent_engaged = False

    def run_step(self, input_data, timestamp):
        print("Running step")
        print("Input data", input_data)
        self.agent_engaged = True
        with self.game_framework:
            control = super().run_step(debug=True)
        # Handle render updates
        return control
    
    def destroy(self):
        super().destroy()
        #self.