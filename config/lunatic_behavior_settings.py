from config.default_options.original_behavior import BehaviorAgentSettings
from config.default_options.original_autopilot_behavior import AutopilotBehavior

from omegaconf import DictConfig, OmegaConf 

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
