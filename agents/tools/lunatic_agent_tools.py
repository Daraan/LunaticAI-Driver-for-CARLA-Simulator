from inspect import isclass
from operator import attrgetter
from omegaconf import DictConfig
from shapely.geometry import Polygon
from functools import partial, wraps

import carla
from classes.constants import RoadOption
from agents.tools.config_creation import AgentConfig
from agents.tools.hints import ObstacleDetectionResult
from agents.tools.misc import (is_within_distance,
                               compute_distance)
from agents.tools.logging import logger

from classes.constants import Phase
from classes.exceptions import EmergencyStopException, LunaticAgentException, SkipInnerLoopException
from launch_tools import CarlaDataProvider, Literal
from typing import TYPE_CHECKING, Any, Callable, Dict, Sequence, Optional, Tuple, Union, cast as assure_type

if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent
    from classes.worldmodel import WorldModel
    from classes.rule import Context


# ------------------------------
# Decorators
# ------------------------------    
    
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

def must_clear_hazard(func):
    """
    Decorator which raises an EmergencyStopException if self.detected_hazards
    is not empty after the function call.
    
    Raises:
        EmergencyStopException: If self.detected_hazards is not empty after the function call.
    """
    @wraps(func)
    def wrapper(self: "LunaticAgent", *args, **kwargs):
        result = func(self, *args, **kwargs)
        if self.detected_hazards:
            raise EmergencyStopException(self.detected_hazards)
        return result
    return wrapper

def phase_callback(*, on_enter: Optional[Phase] = None, 
                      on_exit: Union[Phase, Callable, None] = None, 
                      on_exit_exceptions: Union[Tuple["type[BaseException]"], bool, None] = (),
                      prior_result: Optional["Callable | str"] = None):
        """
        Decorator function for defining phase callbacks that are executed at the start and end of a function.

        Args:
            on_enter (Phase, optional): 
                The phase to execute before the decorated function.
                Defaults to None.
            on_exit (Phase, optional): 
                The phase to execute after the decorated function.
                Defaults to None.
            on_exit_exceptions (Tuple[BaseException] | bool), optional):
                If True, the on_exit phase will still be executed if any 
                :py:exc:`LunaticAgentException` are raised.
                If a tuple of exceptions is provided, the on_exit phase will only be executed if one of the exceptions is raised.
                The exception will be re-raised after the on_exit phase is executed.
                Defaults to empty tuple().

        Warning:
            If **on_enter** and **on_exit** are not set, the decorator will print a 
            warning and ignore the decorator.
        """
        # Validate exception -> Tuple
        if on_exit_exceptions is True:
            on_exit_exceptions = (LunaticAgentException,)
        elif isclass(on_exit_exceptions) and issubclass(on_exit_exceptions, BaseException):
            on_exit_exceptions = (on_exit_exceptions,)
        else:
            on_exit_exceptions = tuple(on_exit_exceptions)
        # Validate prior_result -> Callable
        if prior_result and not callable(prior_result):
            prior_result = attrgetter(prior_result) # raises Type Error if not string

        def decorator(func):
            if not on_enter and not on_exit:
                print("WARNING: No `on_enter`, `on_exit` phase set for `phase_callback` "
                      "decorator for function %s. Ignoring decorator." % func.__name__)
                return func
            @wraps(func)
            def wrapper(self: "LunaticAgent", *args, **kwargs):
                if on_enter:
                    prior_result = prior_result(self) if prior_result else None
                    # if the attribute is a callable, e.g. get_control(), call it
                    if callable(prior_result):
                        prior_result = prior_result()
                    self.execute_phase(on_enter, prior_results=prior_result)
                if on_exit_exceptions:
                    try:
                        result = func(self, *args, **kwargs)
                    except on_exit_exceptions as e:
                        if on_exit:
                            if isinstance(on_exit, Phase):
                                self.execute_phase(on_exit, prior_results=e)
                            else:
                                on_exit(self)
                        raise
                else:
                    result = func(self, *args, **kwargs)
                if on_exit:
                    self.execute_phase(on_exit, prior_results=result)
                return result

            return wrapper

        return decorator

# ------------------------------
# Obstacle Detection
# ------------------------------

def max_detection_distance(self: Union["Context", "LunaticAgent"], lane:Literal["same_lane", "other_lane", "overtaking", "tailgating"]):
    """
    Convenience function to be used with :py:func:`lunatic_agent_tools.detect_vehicles` and :any:`LunaticAgent.detect_obstacles_in_path`.
    
    The max distance to consider an obstacle is calculated as:
    
    .. code-block:: python

        max(obstacles.min_proximity_threshold, 
            live_info.current_speed_limit / obstacles.speed_detection_downscale.[same|other]_lane)
    
    Args:
        self : An object that implements the `config` and `live_info` attributes
        lane : The lane to consider.
    
    Note:
        **lane** must be a key in :code:`BehaviorAgentObstacleSettings.SpeedLimitDetectionDownscale`.

    """
    
    return max(self.config.obstacles.min_proximity_threshold,
               self.live_info.current_speed_limit / self.config.obstacles.speed_detection_downscale[lane])


def detect_obstacles_in_path(self : "LunaticAgent", 
                             obstacle_list: Optional[Union[Literal['all'],
                                                           Sequence[carla.Actor]]]) -> ObstacleDetectionResult:
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

    if obstacle_list in (None, 'all'):
        obstacle_list = self.all_obstacles_nearby

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


def detect_vehicles(self: "LunaticAgent", 
                    vehicle_list:Optional[Sequence[carla.Actor]]=None,
                    max_distance:Optional[float]=None, 
                    up_angle_th:float=90, 
                    low_angle_th:float=0,
                    *, 
                    lane_offset:int=0):
    """
    Method to check if there is a vehicle in front or around the agent blocking its path.

        :param vehicle_list list containing vehicle objects.
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
    
    # See also scenario_runner scenario_helper.detect_lane_obstacle

    if self.config.obstacles.ignore_vehicles:
        return ObstacleDetectionResult(False, None, -1)
    
    if vehicle_list is None:
        # NOTE: If empty list is passed e.g. for walkers this pulls all vehicles
        # TODO: Propose update to original carla
        vehicle_list = self._world.get_actors().filter("*vehicle*") # type: Sequence[carla.Actor] # type: ignore
    elif len(vehicle_list) == 0: # Case for no pedestrians
        return ObstacleDetectionResult(False, None, -1)

    if not max_distance:
        max_distance = self.config.obstacles.base_vehicle_threshold # TODO: This is not modified with the dynamic threshold
    
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
        ego_transform.get_forward_vector() * self._vehicle.bounding_box.extent.x)

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
                return ObstacleDetectionResult(True, 
                                               target_vehicle, 
                                               compute_distance(target_rear_transform.location,
                                                                ego_front_transform.location)) # type: ignore[arg-type]

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

    
def create_agent_config(self: "LunaticAgent", 
                        behavior: Union[AgentConfig, DictConfig, str, None, "type[AgentConfig]"]=None, 
                        world_model: Optional["WorldModel"]=None, 
                        overwrite_options: Optional[Dict[str, Any]]=None):
    """
    Method to create the agent config from different input types.
    """
    if behavior is None and world_model and world_model._config is not None:
        logger.debug("Using world model config")
        opt_dict = world_model._config
    elif behavior is None:
        raise ValueError("Must pass a valid config as behavior or a world model with a set config.")
    elif isinstance(behavior, str): # Assuming Path
        logger.debug("Creating config from yaml file")
        opt_dict = self.BASE_SETTINGS.from_yaml(behavior)
    elif isinstance(behavior, AgentConfig) or isclass(behavior) and issubclass(behavior, AgentConfig):
        logger.info("Config is a dataclass / AgentConfig")
        _cfg = behavior.to_dict_config()
        _cfg.merge_with(overwrite_options) # Note uses DictConfig.update
        opt_dict = assure_type(behavior.__class__, _cfg)
    elif isinstance(behavior, DictConfig):
        logger.info("Config is a DictConfig")
        behavior.merge_with(overwrite_options)
        opt_dict = self.BASE_SETTINGS.cast(behavior)
    elif isclass(behavior):
        logger.info("Config is a class using, instance of it")
        opt_dict  = assure_type(behavior, behavior(**overwrite_options))
    elif not overwrite_options:
        logger.warning("Warning: Settings are not a supported Config class")
        opt_dict = behavior  # assume the user passed something appropriate
    else:
        logger.warning("Warning: Settings are not a supported Config class. Trying to apply overwrite options.")
        behavior.update(overwrite_options) 
        opt_dict = behavior  # assume the user passed something appropriate
    if isinstance(opt_dict, DictConfig):
        opt_dict._set_flag("allow_objects", True)
        opt_dict.__dict__["_parent"] = None # Remove parent from the config, i.e. make it a top-level config.  
    cfg = opt_dict
    return self.BASE_SETTINGS.cast(cfg)