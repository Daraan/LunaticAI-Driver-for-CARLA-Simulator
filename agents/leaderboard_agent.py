from agents.lunatic_agent import LunaticAgent

from leaderboard.autoagents.autonomous_agent import AutonomousAgent
from leaderboard.autoagents.autonomous_agent import Track

def get_entry_point():
    return LunaticChallenger

class LunaticChallenger(LunaticAgent, AutonomousAgent):
    pass

    def setup(self, path_to_conf_file):
        self.track = Track.MAP