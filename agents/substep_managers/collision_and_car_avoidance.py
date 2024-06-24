import carla

from agents.dynamic_planning.dynamic_local_planner import RoadOption

from agents.tools.hints import ObstacleDetectionResult
from agents.tools.lunatic_agent_tools import detect_vehicles

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    import carla
    from agents.lunatic_agent import LunaticAgent

# TODO: Unify distance and obstacle thresholds

def collision_detection_manager(self : "LunaticAgent") -> ObstacleDetectionResult:
        """
        This module is in charge of warning in case of a collision
        and managing possible tailgating chances.

            :param location: current location of the agent
            :return vehicle_state: True if there is a vehicle nearby, False if not
            :return vehicle: nearby vehicle
            :return distance: distance to nearby vehicle

        # NOTE: Former collision_and_car_avoid_manager, which evaded car via the tailgating function
        now rule based.
        """
        vehicle_list = self.vehicles_nearby

        # Triple (<is there an obstacle> , <the actor> , <distance to the actor>)
        if self.live_info.incoming_direction == RoadOption.CHANGELANELEFT:
            detection_result : ObstacleDetectionResult = detect_vehicles(self, vehicle_list, 
                                                                max(self.config.distance.min_proximity_threshold, 
                                                                    self.config.live_info.current_speed_limit / 2), 
                                                                up_angle_th=self.config.obstacles.detection_angles.cars_lane_change[1], 
                                                                lane_offset=-1)
        elif self.live_info.incoming_direction == RoadOption.CHANGELANERIGHT:
            detection_result : ObstacleDetectionResult = detect_vehicles(self, vehicle_list,
                                                                max(self.config.distance.min_proximity_threshold, 
                                                                    self.config.live_info.current_speed_limit / 2), 
                                                                up_angle_th=self.config.obstacles.detection_angles.cars_lane_change[1], 
                                                                lane_offset=1)
        else: 
            detection_result : ObstacleDetectionResult = detect_vehicles(self, vehicle_list, 
                                                                max(self.config.distance.min_proximity_threshold, 
                                                                    self.config.live_info.current_speed_limit / 3), 
                                                                up_angle_th=self.config.obstacles.detection_angles.cars_same_lane[1],)
        return detection_result