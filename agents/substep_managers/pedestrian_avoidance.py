from agents.tools.hints import ObstacleDetectionResult
from classes.constants import RoadOption
from agents.tools.lunatic_agent_tools import detect_vehicles

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent

# TODO: Despite a few constants very similar to vehicle to the collision_detection_manager,
# might be fusable

def pedestrian_detection_manager(self : "LunaticAgent") -> ObstacleDetectionResult:
    """
    This module is in charge of warning in case of a collision
    with any pedestrian.

        :param location: current location of the agent
        :return vehicle_state: True if there is a walker nearby, False if not
        :return vehicle: nearby walker
        :return distance: distance to nearby walker
    """
    walker_list = self.walkers_nearby

    if self.config.live_info.incoming_direction == RoadOption.CHANGELANELEFT:
        detection_result = detect_vehicles(self, walker_list, 
                                           self.max_detection_distance("other_lane"), 
                                            up_angle_th=self.config.obstacles.detection_angles.walkers_lane_change[1], 
                                            lane_offset=-1)
    elif self.config.live_info.incoming_direction == RoadOption.CHANGELANERIGHT:
        detection_result = detect_vehicles(self, walker_list, 
                                            self.max_detection_distance("other_lane"),
                                            up_angle_th=self.config.obstacles.detection_angles.walkers_lane_change[1],
                                            lane_offset=1)
    else:
        detection_result = detect_vehicles(self, walker_list, 
                                           self.max_detection_distance("same_lane"),           
                                            up_angle_th=self.config.obstacles.detection_angles.walkers_same_lane[1])
    return detection_result