
"""
Helper functions and methods for the :py:class:`.LunaticAgent`, some methods are variants
from the original CARLA agents that have been simplified and outsourced to this
module.
"""
# pyright: strict
# pyright: reportUnnecessaryIsInstance=information
# pyright: reportPrivateUsage=false
# pyright: reportTypeCommentUsage=none

from __future__ import annotations

import sys
from functools import partial, wraps
from inspect import isclass
from operator import attrgetter
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Sequence, Tuple, Union
from typing import cast as assure_type

import carla
from omegaconf import DictConfig
from shapely.geometry import Polygon
from typing_extensions import Concatenate, Literal, ParamSpec, TypeVar, assert_never

from agents.tools.config_creation import AgentConfig
from agents.tools.hints import ObstacleDetectionResult
from agents.tools.logging import logger
from agents.tools.misc import is_within_distance
from classes.constants import Phase, RoadOption
from classes.exceptions import EmergencyStopException, LunaticAgentException
from launch_tools import CarlaDataProvider

if TYPE_CHECKING:
    from classes.type_protocols import (
        AgentConfigT,
        CallableT,
        CanDetectNearbyObstacles,
        CanDetectObstacles,
        HasBaseSettings,
        HasConfig,
    )
    from agents.lunatic_agent import LunaticAgent
    from agents.tools.config_creation import BehaviorAgentSettings, LunaticAgentSettings
    from classes.worldmodel import WorldModel

_T = TypeVar("_T")
_P = ParamSpec('_P')
if sys.version_info >= (3, 8):
    _AgentFunction = Callable[Concatenate["LunaticAgent", _P], _T]
else:
    _AgentFunction = Callable[[Concatenate["LunaticAgent", _P]], _T]

# ------------------------------
# Decorators
# ------------------------------
    
    
def result_to_context(key: str) -> Callable[[CallableT], CallableT]:
    """
    Decorator to use for the agent. Sets the **key** attribute of the
    :py:class:`.Context`.
    """
    def decorator(func: CallableT) -> CallableT:
        @wraps(func)
        def wrapper(self : "LunaticAgent", *args: _P.args, **kwargs: _P.kwargs):
            result = func(self, *args, **kwargs)
            setattr(self.ctx, key, result)
            return result
        return wrapper  # type: ignore[return-value]
        
    return decorator

def must_clear_hazard(func: CallableT) -> CallableT:
    """
    Decorator which raises an EmergencyStopException if self.detected_hazards
    is not empty after the function call.
    
    Raises:
        EmergencyStopException: If self.detected_hazards is not empty after the function call.
    """
    @wraps(func)
    def wrapper(self : "LunaticAgent", *args: _P.args, **kwargs: _P.kwargs):
        result = func(self, *args, **kwargs)
        if self.detected_hazards:
            raise EmergencyStopException(self.detected_hazards)
        return result
    return wrapper  # type: ignore[return-value]

def phase_callback(*, on_enter: Union[Phase, Callable[['LunaticAgent'], Any], None] = None,
                      on_exit: Union[Phase, Callable[['LunaticAgent'], Any], None] = None,
                      on_exit_exceptions: Union[Sequence["type[BaseException]"], bool, None] = (),
                      prior_result_getter: Optional[Union[Callable[['LunaticAgent'], Any], str]] = None):
    """
    Decorator function for defining phase callbacks that are executed at the start and end of a function.

    Args:
        on_enter (Phase, optional):
            The phase to execute before the decorated function.
            Defaults to None.
        on_exit:
            Either the phase to execute after the decorated function or a callable.
            Defaults to None.
        on_exit_exceptions (Tuple[BaseException] | bool)):
            If a non-empty sequence of exceptions is provided, the **on_exit** phase will
            **only be executed if one of the exceptions is raised.**
            
            If :python:`True`, the **on_exit** phase will be executed if any
            :py:exc:`LunaticAgentException` are raised.
            Defaults to :code:`False`.
            
            Attention:
                - The **on_exit** phase will *only* be executed if and only if one of the exceptions
                  is raised.
                - The **exception will be re-raised** after executing **on_exit**.
            
        prior_result_getter: Can be the name of an attribute of the agent. If the
            attribute is a callable, it will be called without arguments. Alternatively
            a callable can be passed. The result will be used as the **prior_results**
            argument for the :py:meth:`.LunaticAgent.execute_phase` method.
    
    Warns:
        If **on_enter** and **on_exit** are not set, the decorator will print a
        warning and ignore the decorator.
    """
    # Validate exception -> Tuple
    _on_exit_exceptions_ : Tuple["type[BaseException]", ...]
    if on_exit_exceptions is True:
        _on_exit_exceptions_ = (LunaticAgentException,)
    elif isclass(on_exit_exceptions) and issubclass(on_exit_exceptions, BaseException):
        # This allows to pass a single exception, and is actually Never
        _on_exit_exceptions_ = assure_type(Tuple["type[BaseException]", ...], (on_exit_exceptions,))
    elif not on_exit_exceptions:
        _on_exit_exceptions_ = ()
    else:
        _on_exit_exceptions_ = tuple(on_exit_exceptions)
    
    # Validate prior_result -> Callable
    if prior_result_getter and not callable(prior_result_getter):
        prior_result_getter = attrgetter(prior_result_getter) # raises Type Error if not string

    # Pay attention to prior_result which should not be prior_result
    def decorator(func : _AgentFunction[_P, _T]):
        if on_enter is None and on_exit is None:
            print("WARNING: No `on_enter`, `on_exit` phase set for `phase_callback` "
                    f"decorator for function {func.__name__}. Ignoring decorator.")
            if TYPE_CHECKING:
                assert_never(func) # we ignore this # pyright: ignore
            return func
        @wraps(func)
        def wrapper(self: "LunaticAgent", *args: _P.args, **kwargs: _P.kwargs):
            if on_enter:
                # Careful do not set prior_result else it is not nonlocal
                prior_result = prior_result_getter(self) if prior_result_getter else None
                # if the attribute is a callable, e.g. get_control(), call it
                if callable(prior_result):
                    # Call attribute of the agent
                    prior_result = prior_result()
                if isinstance(on_enter, Phase):
                    self.execute_phase(on_enter, prior_results=prior_result)
                else:
                    on_enter(self)
            
            # Call with exception handling
            if _on_exit_exceptions_:
                try:
                    result = func(self, *args, **kwargs)
                except _on_exit_exceptions_ as e:
                    if on_exit is not None:
                        if isinstance(on_exit, Phase):
                            self.execute_phase(on_exit, prior_results=e)
                        else:
                            on_exit(self)
                    raise
            else:
                result = func(self, *args, **kwargs)
            
            if on_exit:
                if callable(on_exit):
                    on_exit(self)
                else:
                    self.execute_phase(on_exit, prior_results=result)
            
            return result

        return wrapper

    return decorator

# ------------------------------
# Obstacle Detection
# ------------------------------

def max_detection_distance(self: HasConfig["BehaviorAgentSettings | LunaticAgentSettings"],
                           lane: Literal["same_lane", "other_lane", "overtaking", "tailgating"]) -> float:
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
               self.config.live_info.current_speed_limit / self.config.obstacles.speed_detection_downscale[lane])


def detect_obstacles_in_path(self: "CanDetectNearbyObstacles",
                             obstacle_list: Optional[Union[Sequence[carla.Actor], carla.ActorList,\
                                                           Literal['all']]]) -> ObstacleDetectionResult:
    """
    This module is in charge of warning in case of a collision
    and managing possible tailgating chances.

    Args:
        self : The agent
        obstacle_list : The list of obstacles that should be checked

    Note:
        - Distance to detect vehicles that hinder a lance change are calculated with the
          :py:func:`max_detection_distance` function.
        - Former :code:`BehaviorAgent.collision_and_car_avoid_manager`, which evaded cars via the
          tailgating function; this is now rule based.
        
    Tip:
        As the first argument is the agent, this function can be used as a method, i.e
        it can be added / imported directly into the agent class' body.
    """

    if obstacle_list in (None, 'all'):
        obstacle_list = self.all_obstacles_nearby

    # Triple (<is there an obstacle> , <the actor> , <distance to the actor>)
    if self.config.live_info.incoming_direction == RoadOption.CHANGELANELEFT:
        detection_result : ObstacleDetectionResult = detect_obstacles(self, obstacle_list,
                                                        self.max_detection_distance("other_lane"),
                                                        up_angle_th=self.config.obstacles.detection_angles.cars_lane_change[1],
                                                        lane_offset=-1)
    elif self.config.live_info.incoming_direction == RoadOption.CHANGELANERIGHT:
        detection_result : ObstacleDetectionResult = detect_obstacles(self, obstacle_list,
                                                        self.max_detection_distance("other_lane"),
                                                        up_angle_th=self.config.obstacles.detection_angles.cars_lane_change[1],
                                                        lane_offset=1)
    else:
        detection_result : ObstacleDetectionResult = detect_obstacles(self, obstacle_list,
                                                        self.max_detection_distance("same_lane"),
                                                        up_angle_th=self.config.obstacles.detection_angles.cars_same_lane[1],)
    return detection_result


def detect_obstacles(self: "CanDetectObstacles",
                    actor_list: Optional[Sequence[carla.Actor] | carla.ActorList]=None,
                    max_distance: Optional[float]=None,
                    up_angle_th: float=90,
                    low_angle_th: float=0,
                    *,
                    lane_offset: int=0) -> ObstacleDetectionResult:
    """
    Method to check if there is a vehicle in front or around the agent blocking its path.

    Parameters:

        self: The agent
        actor_list: list containing relevant actors to check.
            If :code:`None`, all vehicle in the scene are used.
        max_distance: max free-space to check for obstacles.
            If :code:`None`, the :py:attr:`.LunaticAgentSettings.obstacles.base_vehicle_threshold` value
            is used.
        lane_offset: check a different lane than the one the agent is currently in.

    The angle between the location and reference transform will also be taken into account.
    Being 0 a location in front and 180, one behind, i.e, the vector between has to satisfy:
    **low_angle_th** < angle < **up_angle_th**.
    
    Tip:
        As the first argument is the agent, this function can be used as a method, i.e
        it can be added / imported directly into the agent class' body.
    """
    
    # See also scenario_runner scenario_helper.detect_lane_obstacle

    if self.config.obstacles.ignore_vehicles:
        return ObstacleDetectionResult(False, None, -1)
    
    if actor_list is None:
        # NOTE: If empty list is passed e.g. for walkers this pulls all vehicles
        # TODO: Propose update to original carla
        actor_list = self._vehicle.get_world().get_actors().filter("*vehicle*")
    elif len(actor_list) == 0: # Case for no pedestrians
        return ObstacleDetectionResult(False, None, -1)

    if not max_distance:
        max_distance = self.config.obstacles.base_vehicle_threshold # TODO: This is not modified with the dynamic threshold
    
    def get_route_polygon() -> None | Polygon:
        # Note nested functions can access variables from the outer scope
        route_bb = [] # type: list[list[float]]
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
    ego_location = ego_transform.location  # NOTE: property access creates a new location object, i.e. ego_location != ego_front_transform
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

    for target_vehicle in actor_list:
        if target_vehicle.id == self._vehicle.id:
            continue

        target_transform = target_vehicle.get_transform()
        if target_transform.location.distance(ego_location) > max_distance:
            continue

        target_wpt = CarlaDataProvider.get_map().get_waypoint(target_transform.location, lane_type=carla.LaneType.Any)
        if not target_wpt:
            logger.warning("No waypoint found for the checked obstacle."
                           "This might be a bug in the map but ok for static obstacles.")
            continue

        # General approach for junctions and vehicles invading other lanes due to the offset
        if (use_bbs or target_wpt.is_junction) and route_polygon:

            target_bb = target_vehicle.bounding_box
            target_vertices = target_bb.get_world_vertices(target_vehicle.get_transform())
            target_list = [[v.x, v.y, v.z] for v in target_vertices]
            target_polygon = Polygon(target_list)

            if route_polygon.intersects(target_polygon):
                return ObstacleDetectionResult(True,
                                               target_vehicle,
                                               target_vehicle.get_location().distance(ego_location))

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
                                               target_rear_transform.location.distance(
                                                                ego_front_transform.location))

    return ObstacleDetectionResult(False, None, -1)


def detect_vehicles(self: "CanDetectObstacles",
                    vehicle_list: Optional[Sequence[carla.Actor] | carla.ActorList]=None,
                    max_distance: Optional[float]=None,
                    up_angle_th: float=90,
                    low_angle_th: float=0,
                    lane_offset: int=0) -> ObstacleDetectionResult:
    """
    Method to check if there is a vehicle in front or around the agent blocking its path.

    Parameters:

        self: The agent
        vehicle_list: list containing vehicle objects.
            If :code:`None`, all vehicle in the scene are used.
        max_distance: max free-space to check for obstacles.
            If :code:`None`, the :py:attr:`.LunaticAgentSettings.obstacles.base_vehicle_threshold` value
            is used.
        lane_offset: check a different lane than the one the agent is currently in.

    The angle between the location and reference transform will also be taken into account.
    Being 0 a location in front and 180, one behind, i.e, the vector between has to satisfy:
    **low_angle_th** < angle < **up_angle_th**.
    
    Tip:
        As the first argument is the agent, this function can be used as a method, i.e
        it can be added / imported directly into the agent class' body.
        
    .. deprecated::
        Use :py:func:`.detect_obstacles` instead.
    """
    return detect_obstacles(self, vehicle_list, max_distance,
                            up_angle_th, low_angle_th,
                            lane_offset=lane_offset)

# Untested
detect_obstacles_in_front = partial(detect_vehicles, up_angle_th=90, low_angle_th=0)
"""
:py:func:`.detect_vehicles` with the default parameters for detecting vehicles in front of the agent.
"""

detect_obstacles_behind = partial(detect_vehicles, up_angle_th=180, low_angle_th=160)
"""
:py:func:`.detect_vehicles` with the default parameters for detecting vehicles behind the agent.
"""


# ------------------------------
# Path Planning
# ------------------------------

def generate_lane_change_path(waypoint : carla.Waypoint,
                              direction: Literal['left', 'right']='left',
                              distance_same_lane: float=10,
                              distance_other_lane: float=25,
                              lane_change_distance: float=25,
                              check: bool=True,
                              lane_changes: int=1,
                              step_distance: float=2) -> "list[tuple[carla.Waypoint, RoadOption]]":
    """
    This method generates a path that results in a lane change.
    Use the different distances to fine-tune the maneuver.
    If the lane change is impossible, the returned path will be empty.
    
    Distance traveled:
        1. **distance_same_lane** in the same lane.
        2. **lane_change_distance** while reaching the other lane.
        3. **distance_other_lane** in the other lane.
    
    Parameters:
        waypoint: The starting waypoint.
        direction: The direction of the lane change, either 'left' or 'right'.
            Defaults to 'left'.
        distance_same_lane: The distance to follow the same lane before the lane change.
        distance_other_lane: The distance to follow the other lane after the lane change.
        lane_change_distance: The distance to reach the center of the last lane.
            A low value will make a fast lane change, while a high value will make slow lane change.
        check: If :python:`True`, the method will check if the lane change is possible, i.e. that
            there is a valid lane that the vehicle can change to.
            This ignores :py:attr:`carla.Waypoint.lane_change`.
    """
    distance_same_lane = max(distance_same_lane, 0.1)
    distance_other_lane = max(distance_other_lane, 0.1)
    lane_change_distance = max(lane_change_distance, 0.1)

    plan: "list[tuple[carla.Waypoint, RoadOption]]" = [(waypoint, RoadOption.LANEFOLLOW)]
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

        if not side_wp or (check and side_wp.lane_type != carla.LaneType.Driving):
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
    
def create_agent_config(self: HasBaseSettings[AgentConfigT],
                        source: Union["type[AgentConfigT]", AgentConfigT, DictConfig, str, None]=None,
                        world_model: Optional["WorldModel"]=None,
                        overwrite_options: Optional[Dict[str, Any]]=None) -> AgentConfigT:
    """
    Method to create the :py:class:`.AgentConfig` from different input types.
    
    Parameters:
        self (LunaticAgent): The agent
        source:
            - :code:`None` takes the config from the **world model** if available.
            - :py:class:`.AgentConfig` (class or instance) to be used.
            - :py:class:`omegaconf.DictConfig`, a dictionary with the configuration,
              i.e. duck-typed as :py:class:`.AgentConfig`.
              
    Returns:
        :py:attr:`self.BASE_SETTINGS <.LunaticAgent.BASE_SETTINGS>` (duck-typed):
            The configuration object. The actual type depends on **source**.
            If it is a :python:`str`, :py:class:`.AgentConfig` or :py:class:`.DictConfig`, the actual
            return type will be a :py:class:`omegaconf.DictConfig`.
    """
    if overwrite_options is None:
        overwrite_options = {}
    if source is None and world_model and world_model._config is not None: # pyright: ignore[reportUnnecessaryComparison]
        logger.debug("Using world model config")
        opt_dict = world_model._config
    elif source is None:
        raise ValueError("Must pass a valid config as behavior or a world model with a set config.")
    elif isinstance(source, str): # Assuming Path
        logger.debug("Creating config from yaml file")
        opt_dict = self.BASE_SETTINGS.from_yaml(source)
    elif isinstance(source, AgentConfig) or isclass(source) and issubclass(source, AgentConfig): # pyright: ignore[reportUnnecessaryIsInstance]
        logger.debug("Config is a dataclass / AgentConfig")
        _cfg = source.to_dict_config()
        _cfg.merge_with(overwrite_options) # Note uses DictConfig.update
        opt_dict = assure_type(source.__class__, _cfg)
    elif isinstance(source, DictConfig):  # pyright: ignore[reportUnnecessaryIsInstance]
        logger.debug("Config is a DictConfig")
        source.merge_with(overwrite_options)
        opt_dict = self.BASE_SETTINGS.cast(source)
    elif isclass(source):
        logger.warning("Config is a class of type %s but not an AgentConfig, this is unexpected.",
                       type(source))
        opt_dict  = assure_type(source, source(**overwrite_options))
    elif not overwrite_options:
        logger.warning("Settings of type %s are not a supported Config class", type(source))
        opt_dict = source  # assume the user passed something appropriate
    else:
        logger.warning("Warning: Settings of type %s are not an instance of a supported class. "
                       "Trying to apply overwrite options.", type(source))
        source.update(overwrite_options)
        opt_dict = source  # assume the user passed something appropriate
    if isinstance(opt_dict, DictConfig):
        opt_dict._set_flag("allow_objects", True)  # pyright: ignore[reportPrivateUsage]
        opt_dict.__dict__["_parent"] = None  # Remove parent from the config, i.e. make it a top-level config.
    cfg = opt_dict  # pyright: ignore[reportUnknownVariableType]
    return self.BASE_SETTINGS.cast(cfg)  # duck-type it
