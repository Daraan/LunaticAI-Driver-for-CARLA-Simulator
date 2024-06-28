from shapely.geometry import Polygon
from functools import partial, wraps

import carla
from agents.navigation.local_planner import RoadOption
from agents.tools.hints import ObstacleDetectionResult
from agents.tools.misc import (is_within_distance,
                               compute_distance)

from launch_tools import CarlaDataProvider, Literal
from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent
    from classes.rule import Context

# ------------------------------
# Exceptions
# ------------------------------


class AgentDoneException(Exception):
    """
    Raised when there is no more waypoint in the queue to follow and no rule set a new destination.
    
    When the a GameFramework instance is used as context manager will set game_framework.continue_loop to False.
    """

class ContinueLoopException(Exception):
    """
    Raise when `run_step` action of the agent should not be continued further.

    The agent returns the current ctx.control to the caller of run_step.
    
    Note:
        Handled in Agent.run_step, this exception should not propagate outside.
        It can be caught by GameFramework and skip the current loop, but it will
        log an error.
    """

class UserInterruption(Exception):
    """
    Terminate the loop if user input is detected.
    Allows the scenario runner and leaderboard to exit gracefully, if 
    handled appropriately, e.g. by directly returning.
    
    Thrown by [LunaticAgent.parse_keyboard_controls](#agents.lunatic_agent.LunaticAgent.parse_keyboard_controls).
    """

class UpdatedPathException(Exception):
    """
    Should be raised when the path has been updated and the agent should replan.
    
    Rules that replan on Phase.DONE | END, should throw this exception at the end.
    """


# ------------------------------
# Obstacle Detection
# ------------------------------

def max_detection_distance(self: Union["Context", "LunaticAgent"], lane:Literal["same_lane", "other_lane", "overtaking", "tailgating"]):
    """
    Convenience function to be used with `detect_vehicles` and `detect_obstacles_in_path`.
    
    The max distance to consider an obstacle is calculated as:
    
    :: 
        .. code-block:: python
    max(obstacles.min_proximity_threshold,
        live_info.current_speed_limit / obstacles.speed_detection_downscale.[same|other]_lane)
    
    Args:
        self (Union[Context, LunaticAgent]): An object that implements the `config` and `live_info` attributes
        lane (Literal["same_lane", "other_lane", "overtake"]): The lane to consider.
            Note:
                Key must be in `BehaviorAgentObstacleSettings.SpeedLimitDetectionDownscale`.
    """
    
    return max(self.config.obstacles.min_proximity_threshold,
               self.live_info.current_speed_limit / self.config.obstacles.speed_detection_downscale[lane])


def detect_obstacles_in_path(self : "LunaticAgent", obstacle_list: List[carla.Actor], min_detection_threshold: float, speed_limit_divisors=(2,3)) -> ObstacleDetectionResult:
    """
    This module is in charge of warning in case of a collision
    and managing possible tailgating chances.

    Args:
        self (LunaticAgent): The agent
        obstacle_list (List[carla.Actor]): The list of obstacles that should be checked
        min_detection_threshold (float): The minimum distance to consider an obstacle.
            The max_distance to consider an obstacle is:
            `max(min_detection_threshold, self.config.live_info.current_speed_limit / n)`
            where `n` is speed_limit_divisors[0] for incoming lane change 
            and speed_limit_divisors[1] when the agent stays on the lane.
        speed_limit_divisors (Tuple[float, float], optional): 
            Two divisors for the speed limit to calculate the max distance.
            Defaults to (2, 3).

    Note: 
        Former collision_and_car_avoid_manager, which evaded car via the tailgating function
        now rule based.
        
    Tip: 
        As the first argument is the agent, this function can be used as a method, i.e
        it can be added / imported directly into the agent class' body.
    """

    # Triple (<is there an obstacle> , <the actor> , <distance to the actor>)
    if self.live_info.incoming_direction == RoadOption.CHANGELANELEFT:
        detection_result : ObstacleDetectionResult = detect_vehicles(self, obstacle_list,
                                                            self.max_detection_distance("other_lane"),
                                                            up_angle_th=self.config.obstacles.detection_angles.cars_lane_change[1],
                                                            lane_offset=-1)
    elif self.live_info.incoming_direction == RoadOption.CHANGELANERIGHT:
        detection_result : ObstacleDetectionResult = detect_vehicles(self, obstacle_list,
                                                            self.max_detection_distance("other_lane"),
                                                            up_angle_th=self.config.obstacles.detection_angles.cars_lane_change[1],
                                                            lane_offset=1)
    else:
        detection_result : ObstacleDetectionResult = detect_vehicles(self, obstacle_list,
                                                            self.max_detection_distance("same_lane"),
                                                            up_angle_th=self.config.obstacles.detection_angles.cars_same_lane[1],)
    return detection_result


def detect_vehicles(self: "LunaticAgent", vehicle_list=None, max_distance=None, up_angle_th=90, low_angle_th=0,
                                lane_offset=0):
    """
    Method to check if there is a vehicle in front or around the agent blocking its path.

        :param vehicle_list (list of carla.Vehicle): list containing vehicle objects.
            If None, all vehicle in the scene are used
        :param max_distance: max free-space to check for obstacles.
            If None, the base threshold value is used
        :param lane_offset: check a different lane than the one the agent is currently in.

    The angle between the location and reference transform will also be taken into account. 
    Being 0 a location in front and 180, one behind, i.e, the vector between has to satisfy: 
    low_angle_th < angle < up_angle_th.
    
    Tip: 
        As the first argument is the agent, this function can be used as a method, i.e
        it can be added / imported directly into the agent class' body.
    """

    if self.config.obstacles.ignore_vehicles:
        return ObstacleDetectionResult(False, None, -1)
    
    if vehicle_list is None:
        # NOTE: If empty list is passed e.g. for walkers this pulls all vehicles
        # TODO: Propose update to original carla
        vehicle_list = self._world.get_actors().filter("*vehicle*")
    elif len(vehicle_list) == 0: # Case for no pedestrians
        return ObstacleDetectionResult(False, None, -1)

    def get_route_polygon():
        # Note nested functions can access variables from the outer scope
        route_bb = []
        extent_y = self._vehicle.bounding_box.extent.y
        r_ext = extent_y + self.config.planner.offset
        l_ext = -extent_y + self.config.planner.offset
        r_vec = ego_transform.get_right_vector()
        p1 = ego_location + carla.Location(r_ext * r_vec.x, r_ext * r_vec.y)
        p2 = ego_location + carla.Location(l_ext * r_vec.x, l_ext * r_vec.y)
        route_bb.extend([[p1.x, p1.y, p1.z], [p2.x, p2.y, p2.z]])

        for wp, _ in self._local_planner.get_plan():
            if ego_location.distance(wp.transform.location) > max_distance:
                break

            r_vec = wp.transform.get_right_vector()
            p1 = wp.transform.location + carla.Location(r_ext * r_vec.x, r_ext * r_vec.y)
            p2 = wp.transform.location + carla.Location(l_ext * r_vec.x, l_ext * r_vec.y)
            route_bb.extend([[p1.x, p1.y, p1.z], [p2.x, p2.y, p2.z]])

        # Two points don't create a polygon, nothing to check
        if len(route_bb) < 3:
            return None

        return Polygon(route_bb)

    if not max_distance:
        max_distance = self.config.obstacles.base_vehicle_threshold

    # TODO: can get this from CDP
    ego_transform = self._vehicle.get_transform()
    ego_location = ego_transform.location # NOTE: property access creates a new location object, i.e. ego_location != ego_front_transform
    ego_wpt = CarlaDataProvider.get_map().get_waypoint(ego_location)

    # Get the right offset
    if ego_wpt.lane_id < 0 and lane_offset != 0:
        lane_offset *= -1

    # Get the transform of the front of the ego
    ego_front_transform = ego_transform
    ego_front_transform.location += carla.Location(
        self._vehicle.bounding_box.extent.x * ego_transform.get_forward_vector())

    opposite_invasion = abs(self.config.planner.offset) + self._vehicle.bounding_box.extent.y > ego_wpt.lane_width / 2
    use_bbs = self.config.obstacles.use_bbs_detection or opposite_invasion or ego_wpt.is_junction

    # Get the route bounding box
    route_polygon = get_route_polygon()

    for target_vehicle in vehicle_list:
        if target_vehicle.id == self._vehicle.id:
            continue

        target_transform = target_vehicle.get_transform()
        if target_transform.location.distance(ego_location) > max_distance:
            continue

        target_wpt = CarlaDataProvider.get_map().get_waypoint(target_transform.location, lane_type=carla.LaneType.Any)

        # General approach for junctions and vehicles invading other lanes due to the offset
        if (use_bbs or target_wpt.is_junction) and route_polygon:

            target_bb = target_vehicle.bounding_box
            target_vertices = target_bb.get_world_vertices(target_vehicle.get_transform())
            target_list = [[v.x, v.y, v.z] for v in target_vertices]
            target_polygon = Polygon(target_list)

            if route_polygon.intersects(target_polygon):
                return ObstacleDetectionResult(True, target_vehicle, compute_distance(target_vehicle.get_location(), ego_location))

        # Simplified approach, using only the plan waypoints (similar to TM)
        else:

            if target_wpt.road_id != ego_wpt.road_id or target_wpt.lane_id != ego_wpt.lane_id + lane_offset:
                next_wpt = self._local_planner.get_incoming_waypoint_and_direction(steps=3)[0]
                if not next_wpt:
                    continue
                if target_wpt.road_id != next_wpt.road_id or target_wpt.lane_id != next_wpt.lane_id + lane_offset:
                    continue

            target_forward_vector = target_transform.get_forward_vector()
            target_extent = target_vehicle.bounding_box.extent.x
            target_rear_transform = target_transform
            target_rear_transform.location -= carla.Location(
                x=target_extent * target_forward_vector.x,
                y=target_extent * target_forward_vector.y,
            )

            if is_within_distance(target_rear_transform, ego_front_transform, max_distance,
                                    [low_angle_th, up_angle_th]):
                return ObstacleDetectionResult(True, target_vehicle, compute_distance(target_rear_transform.location, ego_front_transform.location))

    return ObstacleDetectionResult(False, None, -1)

#TODO: UNCLEAR IF CORRECT -> understand angles
detect_vehicles_in_front = partial(detect_vehicles, up_angle_th=90, low_angle_th=0)
detect_vehicles_behind = partial(detect_vehicles, up_angle_th=180, low_angle_th=160)


# ------------------------------
# Path Planning
# ------------------------------

def generate_lane_change_path(waypoint : carla.Waypoint, direction:"Literal['left'] | Literal['right']"='left', distance_same_lane=10,
                                   distance_other_lane=25, lane_change_distance=25,
                                   check=True, lane_changes=1, step_distance=2):
    """
    This method generates a path that results in a lane change.
    Use the different distances to fine-tune the maneuver.
    If the lane change is impossible, the returned path will be empty.
    """
    distance_same_lane = max(distance_same_lane, 0.1)
    distance_other_lane = max(distance_other_lane, 0.1)
    lane_change_distance = max(lane_change_distance, 0.1)

    plan = [(waypoint, RoadOption.LANEFOLLOW)]
    option = RoadOption.LANEFOLLOW

    # Same lane
    distance = 0
    while distance < distance_same_lane:
        next_wps = plan[-1][0].next(step_distance)  # follow a path of waypoints
        if not next_wps:
            return []
        next_wp = next_wps[0]
        distance += next_wp.transform.location.distance(plan[-1][0].transform.location)
        plan.append((next_wp, RoadOption.LANEFOLLOW))  # next waypoint to the path

    # TEMP
    assert direction in ('left', 'right') # TODO: # END: remove at end of project
    
    if direction == 'left':
        option = RoadOption.CHANGELANELEFT
    elif direction == 'right':
        option = RoadOption.CHANGELANERIGHT
    else:
        # ERROR, input value for change must be 'left' or 'right'
        return []

    lane_changes_done = 0
    lane_change_distance = lane_change_distance / lane_changes

    # Lane change
    while lane_changes_done < lane_changes:

        # Move forward
        next_wps = plan[-1][0].next(lane_change_distance)
        if not next_wps:
            return []
        next_wp = next_wps[0]

        # Get the side lane
        if direction == 'left':
            if check and str(next_wp.lane_change) not in ['Left', 'Both']:
                return []
            side_wp = next_wp.get_left_lane()  # get waypoint on other lane
        else:
            if check and str(next_wp.lane_change) not in ['Right', 'Both']:
                return []
            side_wp = next_wp.get_right_lane()

        if not side_wp or side_wp.lane_type != carla.LaneType.Driving:
            return []

        # Update the plan
        plan.append((side_wp, option))
        lane_changes_done += 1

    # Other lane
    # NOTE: Might force it to follow the other lane for some time
    distance = 0
    while distance < distance_other_lane:
        next_wps = plan[-1][0].next(step_distance)
        if not next_wps:
            return []
        next_wp = next_wps[0]
        distance += next_wp.transform.location.distance(plan[-1][0].transform.location)
        plan.append((next_wp, RoadOption.LANEFOLLOW))

    return plan

    
def result_to_context(key):
    """
    Decorator to insert the result into the context object
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self : "LunaticAgent", *args, **kwargs):
            result = func(self, *args, **kwargs)
            setattr(self.ctx, key, result)
            return result
        return wrapper
        
    return decorator

