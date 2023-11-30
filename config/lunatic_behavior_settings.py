from omegaconf import DictConfig, OmegaConf 

from config.settings_base_class import new_config, obstacles
from config.default_options.original_behavior import BehaviorAgentSettings
from config.default_options.original_autopilot_behavior import AutopilotBehavior


# TODOs: implement 
# lunatic_agent._vehicle_obstacle_detected, 
# pedestrian_avoid_manager, 
# collision_and_car_avoid_manager

# ideas cold have full vision and fail randomly
# or have bad vision from time to time
# alternatively mange collision avoidance elsewhere

detection_angles = new_config("detection_angles", parent=obstacles)
# angles are [low_angle_th, up_angle_th]
detection_angles.walkers_lane_change = [0., 90.]
detection_angles.walkers_same_lane = [0., 60.]

detection_angles.cars_lane_change = [0., 180.]
detection_angles.cars_same_lane = [0., 30.]

# Have bad vision from time to time
detection_angles.walkers_angle_adjust_chance = 0.0
detection_angles.walkers_adjust_angle =[20, -20] 
detection_angles.cars_angle_adjust_chance = 0.0
detection_angles.cars_adjust_angle =[20, -50]


# Implemented -----
emergency = new_config("emergency")

emergency.ignore_percentage : float = 0.0
emergency.do_random_steering : bool = False
emergency.random_steering_range : float = (-0.25, 0.25) # angle in radians
emergency.use_hand_brake : bool = False # always use
emergency.hand_brake_modify_chance : float = 0.0 # to use hand brake with some chance 
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
