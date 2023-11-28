from omegaconf import DictConfig, OmegaConf 

from config.settings_base_class import new_config
from config.default_options.original_behavior import BehaviorAgentSettings
from config.default_options.original_autopilot_behavior import AutopilotBehavior


emergency = new_config("emergency")

emergency.ignore_percentage : float = 0.0
emergency.do_random_steering : bool = False
emergency.random_steering_range : float = (-0.25, 0.25) # angle in radians
emergency.use_hand_brake : bool = False # always use
emergency.use_hand_brake_chance : float = 0.0 # to use hand brake with some chance 
# ...
# TODO: Come up with further ideas for emergency behavior, look at the agent.emergency_stop function

class LunaticBehaviorSettings(AutopilotBehavior):

    # Here we can add new options. BUT do NOT overwrite existing options.

    def __init__(self, overwrites=None):
        super().__init__()
        if overwrites is not None:
            self._options = OmegaConf.merge(self._options, overwrites)
        #self._options = self.init_default_options.copy()

    @classmethod
    def from_file(cls, file_path: str):
        """Creates a new instance from a yaml file and overwrites the default options."""
        return cls(OmegaConf.load(file_path))
