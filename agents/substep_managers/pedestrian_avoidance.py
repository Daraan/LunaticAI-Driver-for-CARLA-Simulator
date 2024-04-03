from agents.tools.misc import ObstacleDetectionResult
from agents.navigation.local_planner import RoadOption
from agents.tools.lunatic_agent_tools import detect_vehicles

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    import carla
    from agents.lunatic_agent import LunaticAgent

# TODO: Despite a few constants very similar to vehicle to the collision_detection_manager,
    # might be fusable

def pedestrian_detection_manager(self : "LunaticAgent", waypoint : "carla.Waypoint") -> ObstacleDetectionResult:
    """
    This module is in charge of warning in case of a collision
    with any pedestrian.

        :param location: current location of the agent
        :param waypoint: current waypoint of the agent
        :return vehicle_state: True if there is a walker nearby, False if not
        :return vehicle: nearby walker
        :return distance: distance to nearby walker
    """
    def dist(w):
        return w.get_location().distance(waypoint.transform.location)

    # TODO: Make this a parameter
    walker_list = [w for w in self.walkers_nearby if dist(w) < 10]

    if self.config.live_info.incoming_direction == RoadOption.CHANGELANELEFT:
        detection_result = detect_vehicles(self, walker_list, 
                                           max(self.config.distance.min_proximity_threshold, 
                                               self.config.live_info.current_speed_limit / 2), 
                                            up_angle_th=self.config.obstacles.detection_angles.walkers_lane_change[1], 
                                            lane_offset=-1)
    elif self.config.live_info.incoming_direction == RoadOption.CHANGELANERIGHT:
        detection_result = detect_vehicles(self, walker_list, 
                                            max(self.config.distance.min_proximity_threshold, 
                                                self.config.live_info.current_speed_limit / 2), 
                                            up_angle_th=self.config.obstacles.detection_angles.walkers_lane_change[1],
                                            lane_offset=1)
    else:
        detection_result = detect_vehicles(self, walker_list, 
                                           max(self.config.distance.min_proximity_threshold, 
                                               self.config.live_info.current_speed_limit / 3),             
                                            up_angle_th=self.config.obstacles.detection_angles.walkers_same_lane[1])
    return detection_result