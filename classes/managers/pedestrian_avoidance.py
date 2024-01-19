from agents.tools.misc import ObstacleDetectionResult
from agents.navigation.local_planner import RoadOption
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    import carla

def pedestrian_avoid_manager(self, waypoint : carla.Waypoint) -> ObstacleDetectionResult:
    """
    This module is in charge of warning in case of a collision
    with any pedestrian.

        :param location: current location of the agent
        :param waypoint: current waypoint of the agent
        :return vehicle_state: True if there is a walker nearby, False if not
        :return vehicle: nearby walker
        :return distance: distance to nearby walker
    """

    walker_list = self._world.get_actors().filter("*walker.pedestrian*")

    def dist(w):
        return w.get_location().distance(waypoint.transform.location)

    walker_list = [w for w in walker_list if dist(w) < 10]

    if self.config.live_info.direction == RoadOption.CHANGELANELEFT:
        walker_state, walker, distance = self._vehicle_obstacle_detected(walker_list, max(
            self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=90, lane_offset=-1)
    elif self.config.live_info.direction == RoadOption.CHANGELANERIGHT:
        walker_state, walker, distance = self._vehicle_obstacle_detected(walker_list, max(
            self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=90, lane_offset=1)
    else:
        walker_state, walker, distance = self._vehicle_obstacle_detected(walker_list, max(
            self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 3), up_angle_th=60)

    return ObstacleDetectionResult(walker_state, walker, distance)