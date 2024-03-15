from omegaconf import OmegaConf
from agents.lunatic_agent import LunaticAgent

from classes.worldmodel import GameFramework, WorldModel
from conf.agent_settings import LunaticAgentSettings
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
        sim_world = CarlaDataProvider.get_world()
        map_inst = CarlaDataProvider.get_map()
        
        args = OmegaConf.load("/home/dsperber/TeamProject/LunaticAI-Driver-for-CARLA-Simulator/conf/launch_config.yaml")
        args.map = None # Let scenario manager decide
        args.sync = None
        
        behavior = LunaticAgentSettings()#.from_yaml(path_to_conf_file)
        config = behavior.make_config()
        self.game_framework = GameFramework(args, config)
        # TODO: How to make args optioal
        world_model = WorldModel(config, args=args)
        LunaticAgent.__init__(self, config, world_model, map_inst=map_inst, grp_inst=CarlaDataProvider.get_global_route_planner())

    def run_step(self, debug=False):
        with self.game_framework:
            control = super().run_step(debug)
        # Handle render updates
        return control