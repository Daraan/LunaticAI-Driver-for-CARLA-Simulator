from agents.lunatic_agent import LunaticAgent

from classes.worldmodel import GameFramework, WorldModel
from conf.agent_settings import LunaticAgentSettings
from leaderboard.autoagents.autonomous_agent import AutonomousAgent
from leaderboard.autoagents.autonomous_agent import Track

from scenario_runner.srunner.scenariomanager.carla_data_provider import CarlaDataProvider

def get_entry_point():
    return "LunaticChallenger"

class LunaticChallenger(LunaticAgent, AutonomousAgent):
    
    
    def __init__(self, carla_host, carla_port, debug=False):
        super(LunaticAgent, self).__init__(carla_host, carla_port, debug)


    def setup(self, path_to_conf_file):
        self.track = Track.MAP
        sim_world = CarlaDataProvider.get_world()
        map_inst = CarlaDataProvider.get_map()
        
        behavior = LunaticAgentSettings()#.from_yaml(path_to_conf_file)
        config = behavior.make_config()
        # TODO: How to make args optioal
        world_model = WorldModel(sim_world, config, args, player=None, map_inst=map_inst)
        LunaticAgent.__init__(self, world_model, config, map_inst=map_inst, grp_inst=CarlaDataProvider.get_global_route_planner())


    def run_step(self, debug=False):
        
        return super().run_step(debug)