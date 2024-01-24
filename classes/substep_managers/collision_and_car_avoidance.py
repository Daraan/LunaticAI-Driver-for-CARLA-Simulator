import carla

from agents.dynamic_planning.dynamic_local_planner import RoadOption

from agents.tools.misc import get_speed, ObstacleDetectionResult
from agents.tools.lunatic_agent_tools import detect_vehicles

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    import carla
    from agents import LunaticAgent

 # ported from behavior_agent, maybe we can make a # updated behaviorAgent class
    # Todo port settings to property and this can be removed (if not adjusted)
    #@override
def _tailgating(self : "LunaticAgent", waypoint : carla.Waypoint, vehicle_list : List[carla.Vehicle]):
    """
    This method is in charge of tailgating behaviors.

        :param waypoint: current waypoint of the agent
        :param vehicle_list: list of all the nearby vehicles
    """
    behind_vehicle_state, behind_vehicle, _ = detect_vehicles(vehicle_list, 
                                                              max_distance=max(self.config.distance.min_proximity_threshold, 
                                                                               self.config.live_info.current_speed_limit / 2), 
                                                              up_angle_th=180, low_angle_th=160)
    # There is a vehicle behind us that is faster than we are
    if behind_vehicle_state and self.config.live_info.current_speed < get_speed(behind_vehicle):
        
        left_turn = waypoint.left_lane_marking.lane_change
        right_turn = waypoint.right_lane_marking.lane_change

        left_wpt = waypoint.get_left_lane()
        right_wpt = waypoint.get_right_lane()

        if ((right_turn == carla.LaneChange.Right 
            or right_turn == carla.LaneChange.Both) 
            and waypoint.lane_id * right_wpt.lane_id > 0 
            and right_wpt.lane_type == carla.LaneType.Driving
            ):
            new_vehicle_state, _, _ = detect_vehicles(vehicle_list, max(
                self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=1)
            if not new_vehicle_state:
                print("Tailgating, moving to the right!")
                end_waypoint = self._local_planner.target_waypoint
                self.config.other.tailgate_counter = 200
                self.set_destination(end_waypoint.transform.location,
                                        right_wpt.transform.location)
        elif left_turn == carla.LaneChange.Left and waypoint.lane_id * left_wpt.lane_id > 0 and left_wpt.lane_type == carla.LaneType.Driving:
            new_vehicle_state, _, _ = detect_vehicles(vehicle_list, max(
                self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=-1)
            if not new_vehicle_state:
                print("Tailgating, moving to the left!")
                end_waypoint = self._local_planner.target_waypoint
                self.config.other.tailgate_counter = 200
                self.set_destination(end_waypoint.transform.location,
                                        left_wpt.transform.location)

def collision_and_car_avoid_manager(self : "LunaticAgent", waypoint: carla.Waypoint):
        """
        This module is in charge of warning in case of a collision
        and managing possible tailgating chances.

            :param location: current location of the agent
            :param waypoint: current waypoint of the agent
            :return vehicle_state: True if there is a vehicle nearby, False if not
            :return vehicle: nearby vehicle
            :return distance: distance to nearby vehicle
        """

        # TODO: should do this in update_information -> agents.nearby_vehicles
        vehicle_list : List[carla.Vehicle] = self._world.get_actors().filter("*vehicle*")

        def dist(v : carla.Actor): # is it more efficient to use an extra function here, why not utils.dist_to_waypoint(v, waypoint)?
            return v.get_location().distance(waypoint.transform.location)

        vehicle_list = [v for v in vehicle_list if dist(v) < 45 and v.id != self._vehicle.id]

        # Triple (<is there an obstacle> , )
        if self.config.live_info.direction == RoadOption.CHANGELANELEFT:
            vehicle_state, vehicle, distance = self._vehicle_obstacle_detected(
                vehicle_list, max(
                    self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=-1)
        elif self.config.live_info.direction == RoadOption.CHANGELANERIGHT:
            vehicle_state, vehicle, distance = self._vehicle_obstacle_detected(
                vehicle_list, max(
                    self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=1)
        else:
            vehicle_state, vehicle, distance = self._vehicle_obstacle_detected(
                vehicle_list, max(
                    self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 3), up_angle_th=30)

        return ObstacleDetectionResult(vehicle_state, vehicle, distance)