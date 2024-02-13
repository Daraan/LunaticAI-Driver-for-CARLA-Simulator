import carla

from agents.dynamic_planning.dynamic_local_planner import RoadOption

from agents.tools.misc import get_speed, ObstacleDetectionResult
from agents.tools.lunatic_agent_tools import detect_vehicles

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    import carla
    from agents import LunaticAgent

def collision_detection_manager(self : "LunaticAgent", waypoint: carla.Waypoint) -> ObstacleDetectionResult:
        """
        This module is in charge of warning in case of a collision
        and managing possible tailgating chances.

            :param location: current location of the agent
            :param waypoint: current waypoint of the agent
            :return vehicle_state: True if there is a vehicle nearby, False if not
            :return vehicle: nearby vehicle
            :return distance: distance to nearby vehicle

        # NOTE: Former collision_and_car_avoid_manager, which evaded car via the tailgating function
        now rule based.
        """
        # NOTE: # is it more efficient to use an extra function here, why not utils.dist_to_waypoint(v, waypoint)?
        def dist(v : carla.Actor): 
            return v.get_location().distance(waypoint.transform.location)

        # TODO: Expose constant or do not filter, if we assume vehicle_list is already filtered
        vehicle_list : List[carla.Vehicle] = [v for v in self.vehicles_nearby if dist(v) < 45 and v.id != self._vehicle.id]

        # Triple (<is there an obstacle> , )
        if self.config.live_info.direction == RoadOption.CHANGELANELEFT:
            detection_result : ObstacleDetectionResult = detect_vehicles(self, vehicle_list, 
                                                                max(self.config.distance.min_proximity_threshold, 
                                                                    self.config.live_info.current_speed_limit / 2), 
                                                                up_angle_th=180, 
                                                                lane_offset=-1)
        elif self.config.live_info.direction == RoadOption.CHANGELANERIGHT:
            detection_result : ObstacleDetectionResult = detect_vehicles(self, vehicle_list,
                                                                max(self.config.distance.min_proximity_threshold, 
                                                                    self.config.live_info.current_speed_limit / 2), 
                                                                up_angle_th=180, 
                                                                lane_offset=1)
        else: 
            detection_result : ObstacleDetectionResult = detect_vehicles(self, vehicle_list, 
                                                                max(self.config.distance.min_proximity_threshold, 
                                                                    self.config.live_info.current_speed_limit / 3), 
                                                                up_angle_th=30)
        return detection_result