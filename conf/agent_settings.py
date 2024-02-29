import sys
if __name__ == "__main__": # TEMP clean at the end, only here for testing
    import os
    sys.path.append(os.path.abspath("../"))

from enum import Enum
from functools import partial, wraps
from dataclasses import dataclass, field, asdict
import typing
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Tuple, Type, Union, cast

# from typing import ParamSpec, Concatenate, TypeAlias
#Param = ParamSpec("Param")
ConfigType = typing.TypeVar("ConfigType", bound="AgentConfig")
ReturnType = typing.TypeVar("ReturnType")

#import attr

from omegaconf import DictConfig, MISSING, SI, II, ListConfig, OmegaConf, SCMode
from omegaconf.errors import InterpolationToMissingValueError
# NOTE:
"""
# For type hints when interpolating

II : Equivalent to ${interpolation}
SI Use this for String interpolation, for example "http://${host}:${port}"
"""

import carla

from agents.navigation.local_planner import RoadOption
from classes.rss_sensor import AD_RSS_AVAILABLE

# Helper methods

class class_or_instance_method:
    """Decorator to transform a method into both a regular and class method"""
    
    def __init__(self, call):
        self.__wrapped__ = call
        self._wrapper = lambda x : x

    def __get__(self, instance : Union[None,"AgentConfig"], owner : Type["AgentConfig"]):
        if instance is None:  # called on class 
            return self._wrapper(partial(self.__wrapped__, owner))
        #if isinstance(instance, AgentConfig):  # called on instance
        return self._wrapper(partial(self.__wrapped__, instance))


OmegaConf.register_new_resolver("sum", lambda x, y: x + y)
OmegaConf.register_new_resolver("subtract", lambda x, y: x + y)
OmegaConf.register_new_resolver("min", lambda *els: min(els))

def set_readonly_interpolations(conf : Union[DictConfig, ListConfig]):
    """
    Sets all interpolations to readonly.
    
    See: https://github.com/omry/omegaconf/issues/1161
    """
    if conf._is_interpolation():
        OmegaConf.set_readonly(conf, True)
    elif isinstance(conf, DictConfig):
        for key in conf:
            set_readonly_interpolations(conf._get_node(key))
    elif isinstance(conf, ListConfig):
        for key in range(len(conf)):
            set_readonly_interpolations(conf._get_node(key))
            
def set_readonly_keys(conf : Union[DictConfig, ListConfig], keys : List[str]):
    for key in keys:
        OmegaConf.set_readonly(conf._get_node(key), True)

# Configs

class AgentConfig:
    overwrites : Optional[Dict[str, dict]] = None
    
    @classmethod
    def get_defaults(cls) -> "AgentConfig":
        """Returns the global default options."""
        return cls
    
    @class_or_instance_method
    def export_options(cls_or_self, path, category=None, resolve=False) -> None:
        """Exports the options to a yaml file."""
        if category is None:
            options = cls_or_self
        else:
            options = cls_or_self[category]
        OmegaConf.save(options, path, resolve=resolve)
        
    @class_or_instance_method
    def simplify_options(cls_or_self, category=None, *, resolve, yaml=False, **kwargs):
        """
        Returns a dictionary of all options or a string in yaml format.
        
        :param category: The category of options to retrieve. If None, retrieves all options.
        :param resolve: Whether to resolve and interpolate values.
        :param yaml: Whether to return the options as YAML formatted string
        :param kwargs: Additional keyword arguments to pass to OmegaConf.to_container or OmegaConf.to_yaml.
        
        :return: The dictionary or str of options.
        """
        if category is None:
            options = cls_or_self
        else:
            options = getattr(cls_or_self, category)
        if not isinstance(options, DictConfig) and not resolve:
            return asdict(options)
        if not isinstance(options, DictConfig):
            options = OmegaConf.structured(options)
        if yaml:
            return OmegaConf.to_yaml(options, resolve=resolve, **kwargs)
        return OmegaConf.to_container(options, resolve=resolve, **kwargs)
    
    @class_or_instance_method
    def to_yaml(cls_or_self, resolve=False) ->  str:
        return cls_or_self.simplify_options(resolve=resolve, yaml=True)
    
    @classmethod
    def from_yaml(cls, path, category : Optional[str]=None, *, merge=True):
        """Loads the options from a yaml file."""
        if merge:
            options : cls = OmegaConf.merge(cls(), OmegaConf.load(path))
        else:
            options : cls = OmegaConf.load(path)
        if category is None:
            return options
        r : DictConfig = cast(AgentConfig, options[category])
        return r
    

    @class_or_instance_method
    def get_options(cls_or_self : ConfigType, category:Optional[str]=None, *, lock_interpolations=True, lock_fields:Optional[List[str]]=None) -> ConfigType:
        """
        Returns a dictionary of all options.
        
        Interpolations will be locked to prevent them from being overwritten.
        E.g. speed.current_speed does cannot diverge from live_info.current_speed.
        """
        if category is None:
            options = cls_or_self
        else:
            options = getattr(cls_or_self, category)
        conf : ConfigType = OmegaConf.structured(options, flags={"allow_objects": True})
        # This pre
        if lock_interpolations:
            set_readonly_interpolations(conf)
        if lock_fields:
            set_readonly_keys(conf, lock_fields)
        return conf
    
    
    @staticmethod
    def _flatten_dict(source : DictConfig, target):
        for k, v in source.items():
            if isinstance(v, dict):
                AgentConfig._flatten_dict(v, target)
            else:
                target[k] = v
    
    @class_or_instance_method
    def get_flat_options(cls_or_self, *, resolve=True) -> dict:
        """
        Note these return a copy of the data but in a flat hierarchy.
        Also note interpolations are replaced by default.
        E.g. target_speed and max_speed are two different references.
        """
        try:
            resolved = OmegaConf.to_container(OmegaConf.create(cls_or_self), resolve=resolve, throw_on_missing=False)
        except InterpolationToMissingValueError:
            print("Resolving has failed because a missing value has been accessed. Fill all missing values before calling this function or set `resolve=False`.")
            # NOTE: alternatively call again with resolve=False
            raise
        options = {}
        cls_or_self._flatten_dict(resolved, options)
        return options
    
    def update(self, options : dict, clean=True):
        """Updates the options with a new dictionary."""
        for k, v in options.items():
            if isinstance(getattr(self, k), AgentConfig):
                getattr(self, k).update(v)
            else:
                setattr(self, k, v)
        if clean:
            self._clean_options()

    def _clean_options(self):
        """Postprocessing of possibly wrong values"""
        NotImplemented

    def __post_init__(self):
        """
        Assures that if a dict is passed the values overwrite the defaults.
        
        # NOTE: Will be used for dataclass derived children
        """
        self._clean_options()
        if self.overwrites is None:
            return
        for key, value in self.overwrites.items():
            if key in self.__annotations__:
                if issubclass(self.__annotations__[key], AgentConfig):
                    getattr(self, key).update(value)
                else:
                    print("is not a Config")
                    setattr(self, key, value)
            else:
                print(f"Key {key} not found in {self.__class__.__name__} options.")
        return 
        for name, _type in self.__annotations__.items(): # NOTE: AttributeError: if an attribute error points here type hints might have been forgotten.
            if isinstance(_type, typing._GenericAlias):
                continue
            if issubclass(_type, AgentConfig) \
                and not isinstance(getattr(self, name), _type):
                    setattr(self, name, _type.get_defaults()(**getattr(self, name)))

# ---------------------
# Live Info
# ---------------------

@dataclass
class LiveInfo(AgentConfig):
    current_speed : float = MISSING
    current_speed_limit : float = MISSING
    velocity_vector : carla.Vector3D = MISSING
    direction : RoadOption = MISSING
    
    # NOTE: Not ported to OmegaConf
    @property
    def speed(self):
        return self.current_speed

    @property
    def speed_limit(self):
        return self.current_speed_limit
    
    # NOTE: not wr
    #current_speed : float = II(".speed") # alias for convenience
    #current_speed_limit : float = II(".speed_limit")

# ---------------------
# Speed
# ---------------------    
    
    
@dataclass
class BasicAgentSpeedSettings(AgentConfig):
    current_speed: float = II("live_info.current_speed")
    """This is a reference to live_info.current_speed, which is updated by the agent"""
    
    current_speed_limit: float = II("live_info.current_speed_limit")
    """This is a reference to live_info.current_speed_limit, which is updated by the agent"""
    
    target_speed: float = 20
    """desired cruise speed in Km/h; overwritten by SpeedLimit if follow_speed_limit is True"""
    
    follow_speed_limits: bool = False
    """If the agent should follow the speed limit. *NOTE:* SpeedLimit overwrites target_speed if True (local_planner.py)"""

@dataclass
class BehaviorAgentSpeedSettings(BasicAgentSpeedSettings):
    """
    The three situations they adjust their speed; # SEE: `behavior_agent.car_following_manager`
    
    Case A car in front and getting closer : slow down; slower than car in front
          Take minium from, speed decrease, speed limit adjustment and target_speed
          `target_speed` = min( other_vehicle_speed - self._behavior.speed_decrease, # <-- slow down BELOW the other car
                              self._behavior.max_speed # use target_speed instead
                              self._speed_limit - self._behavior.speed_lim_dist])
    Case B car in front but safe distance : match speed
          `target_speed` = min([
                    max(self._min_speed, other_vehicle_speed),  # <- match speed
                    self._behavior.max_speed,
                    self._speed_limit - self._behavior.speed_lim_dist])
    Case C front is clear
          `target_speed` = min([
                    self._behavior.max_speed,
                    self._speed_limit - self._behavior.speed_lim_dist])
    """
    # TODO:  deprecated max_speed use target_speed instead   # NOTE: Behavior agents are more flexible in their speed. 
    max_speed : float = 50 
    """The maximum speed in km/h your vehicle will be able to reach.
    From normal behavior. This supersedes the target_speed when following the BehaviorAgent logic."""
    
    # CASE A
    speed_decrease : float = 12
    """other_vehicle_speed"""
    
    safety_time : float = 3
    """Time in s before a collision at the same speed -> apply speed_decrease"""

    # CASE B
    min_speed : float = 5
    """Implement als variable, currently hard_coded"""

    # All Cases
    speed_lim_dist : float = 6
    """
    Difference to speed limit.
    NOTE: For negative values the car drives above speed limit
    """

    intersection_speed_decrease: float = 5.0
    """Reduction of the targeted_speed when approaching an intersection"""
    
    
@dataclass
class AutopilotSpeedSettings(AgentConfig):
    vehicle_percentage_speed_difference : float = 30 # in percent
    """
    Sets the difference the vehicle's intended speed and its current speed limit. 
    Speed limits can be exceeded by setting the percentage to a negative value. 
    Default is 30.
    
    Exceeding a speed limit can be done using negative percentages.
    """
    
@dataclass
class LunaticAgentSpeedSettings(AutopilotSpeedSettings, BehaviorAgentSpeedSettings):
    vehicle_percentage_speed_difference : float = MISSING # 30
    """
    TODO: Port from traffic manager.
    
    Sets the difference the vehicle's intended speed and its current speed limit. 
    Speed limits can be exceeded by setting the perc to a negative value. 
    Default is 30. 
    Exceeding a speed limit can be done using negative percentages.
    """
    
    intersection_target_speed: float = SI("${min:${.max_speed}, ${subtract:${.current_speed_limit}, ${.intersection_speed_decrease}}}")
    """Formula or value to calculate the target speed when approaching an intersection"""
    
    
# ---------------------
# Distance
# ---------------------


@dataclass
class BasicAgentDistanceSettings(AgentConfig):
    """
    Calculation of the minimum distance for # XXX
    min_distance = base_min_distance + distance_ratio * vehicle_speed 
    
    see local_planner.py `run_step`
    """
    
    base_min_distance : float = 3.0
    """
    Base value of the distance to keep
    """
    
    distance_ratio : float = 0.5
    """Increases minimum distance multiplied by speed"""
    

@dataclass
class BehaviorAgentDistanceSettings(BasicAgentDistanceSettings):
    """
    Collision Avoidance -----

    Distance in which for vehicles are checked
    max(min_proximity_threshold, self._speed_limit / (2 if LANE CHANGE else 3 ) )
    TODO: The secondary speed limit is hardcoded, make adjustable and optional
    automatic_proximity_threshold = {RoadOption.CHANGELANELEFT: 2, "same_lane" : 3, "right_lane" : 2}
    """
    
    min_proximity_threshold : float = 12
    """Range in which cars are detected. NOTE: Speed limit overwrites"""
    
    braking_distance : float = 6
    """Emergency Stop Distance Trigger"""
    

@dataclass
class AutopilotDistanceSettings(AgentConfig):
    distance_to_leading_vehicle : float = 5.0
    """
    Sets the minimum distance in meters that a vehicle has to keep with the others. 
    The distance is in meters and will affect the minimum moving distance. It is computed from front to back of the vehicle objects.
    """

@dataclass
class LunaticAgentDistanceSettings(AutopilotDistanceSettings, BehaviorAgentDistanceSettings):
    distance_to_leading_vehicle : float = MISSING # 5.0
    """
    PORT from TrafficManager # TODO:
    
    Sets the minimum distance in meters that a vehicle has to keep with the others. 
    The distance is in meters and will affect the minimum moving distance. It is computed from front to back of the vehicle objects.
    """
    
# ---------------------
# Lane Change
# ---------------------

@dataclass
class BasicAgentLaneChangeSettings(AgentConfig):
    """
    XXX
    
    see: `BasicAgent.lane_change` and `BasicAgent._generate_lane_change_path`
    """
    same_lane_time : float = 0.0
    other_lane_time : float = 0.0
    lane_change_time : float = 2.0

@dataclass
class BehaviorAgentLaneChangeSettings(BasicAgentLaneChangeSettings):
    pass

@dataclass
class AutopilotLaneChangeSettings(AgentConfig):
    auto_lane_change: bool = True
    """Turns on or off lane changing behavior for a vehicle."""
    
    random_left_lanechange_percentage: float = 0.1
    """
    Adjust probability that in each timestep the actor will perform a left/right lane change, 
    dependent on lane change availability.
    """
    random_right_lanechange_percentage : float = 0.1
    """
    Adjust probability that in each timestep the actor will perform a left/right lane change, 
    dependent on lane change availability.
    """

    keep_right_rule_percentage: float = 0.7
    """
    During the localization stage, this method sets a percent chance that vehicle will follow the keep right rule, 
    and stay in the right lane.
    """
    

@dataclass
class LunaticAgentLaneChangeSettings(AutopilotLaneChangeSettings, BasicAgentLaneChangeSettings):
    """
    Lane Change -----

    Adjust probability that in each timestep the actor will perform a left/right lane change, 
    dependent on lane change availability. 
    """
    
    random_lane_change_interval : int = 200
    """Cooldown value for a lane change in the 'lane_change' group."""
    
# ---------------------
# Obstacles
# ---------------------

@dataclass
class BasicAgentObstacleDetectionAngles(AgentConfig):
    """
    Detection Angles for the BasicAgent used in the `BasicAgent._vehicle_obstacle_detected` method.
    
    The angle between the location and reference object.
    Being 0 a location in front and 180, one behind, i.e, the vector between has to satisfy: 
    low_angle_th < angle < up_angle_th.
    """
    
    walkers_lane_change : Tuple[float, float] = (0., 90.)
    """Detection angle of walkers when staying in the same lane"""
    
    walkers_same_lane : Tuple[float, float] = (0., 60.)
    """Detection angle of walkers when changing lanes"""
    
    cars_lane_change : Tuple[float, float] = (0., 180.)
    """Detection angle of cars when staying in the same lane"""
    
    cars_same_lane : Tuple[float, float] = (0., 30.)
    """Detection angle of cars when changing lanes"""
    
@dataclass
class BasicAgentObstacleSettings(AgentConfig):
    """
    --------------------------
    Agent Level
    see _affected_by_traffic_light and _affected_by_vehicle in basic_agent.py
    --------------------------
    Agents is aware of the vehicles and traffic lights within its distance parameters
    optionally can always ignore them.
    """
    
    ignore_vehicles : bool = False
    """Whether the agent should ignore vehicles"""
    
    ignore_traffic_lights : bool = False
    """Whether the agent should ignore traffic lights"""
    
    ignore_stop_signs : bool = False
    """
    Whether the agent should ignore stop signs
    
    NOTE: No usage implemented!
    """
    
    use_bbs_detection : bool = False
    """
    True: Whether to use a general approach to detect vehicles invading other lanes due to the offset.

    False: Simplified approach, using only the plan waypoints (similar to TM)
    
    See `BasicAgent._vehicle_obstacle_detected`
    """
    
    base_tlight_threshold : float = 5.0
    """
    Base distance to traffic lights to check if they affect the vehicle
        
    USAGE: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
    USAGE: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed
    """
    
    base_vehicle_threshold : float = 5.0
    """
    Base distance to vehicles to check if they affect the vehicle
            
    USAGE: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
    USAGE: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed
    """

    detection_speed_ratio : float = 1.0
    """
    Increases detection range based on speed
    
    USAGE: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
    USAGE: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed
    """
    
    detection_angles : BasicAgentObstacleDetectionAngles = field(default_factory=BasicAgentObstacleDetectionAngles)

@dataclass
class BehaviorAgentObstacleSettings(BasicAgentObstacleSettings):
    pass

@dataclass
class AutopilotObstacleSettings(AgentConfig):
    ignore_lights_percentage : float = 0.0
    ignore_signs_percentage : float = 0.0
    ignore_walkers_percentage : float = 0.0
    """
    Percentage of time to ignore traffic lights, signs and pedestrians
    """
    
@dataclass
class LunaticAgentObstacleDetectionAngles(BasicAgentObstacleDetectionAngles):
    """
    Detection Angles for the BasicAgent used in the `BasicAgent._vehicle_obstacle_detected` method.
    
    The angle between the location and reference object.
    Being 0 a location in front and 180, one behind, i.e, the vector between has to satisfy: 
    low_angle_th < angle < up_angle_th.
    
    NotImplemented
    """
    
    walkers_angle_adjust_chance : float = 0.0
    """Chance that the detection angle for walkers is adjusted"""
    
    walkers_adjust_angle : Tuple[float, float] = (20, -20)
    """XXX"""
    
    cars_angle_adjust_chance : float = 0.0
    """Chance that the detection angle for vehicles is adjusted"""
    
    cars_adjust_angle : Tuple[float, float] = (20, -50)
    """XXX"""
    

@dataclass
class LunaticAgentObstacleSettings(AutopilotObstacleSettings, BehaviorAgentObstacleSettings):
    dynamic_threshold_by_speed : bool = True
    """
    Whether or not to add `detection_speed_ratio * vehicle_speed` to `base_vehicle_threshold`
    
    # NOTE: Part of BasicAgent overhaul
    """
    
# ---------------------
# Emergency
# ---------------------

# ---------------------
# Controller
# TODO: Maybe a different name
# ---------------------

@dataclass
class BasicAgentControllerSettings(AgentConfig):
    """PIDController Level (called from planner)"""
    
    max_brake : float = 0.5
    """
    Vehicle control how strong the brake is used, 
    
    NOTE: Also used in emergency stop
    """
    max_throttle : float = 0.75
    """maximum throttle applied to the vehicle"""
    max_steering : float = 0.8
    """maximum steering applied to the vehicle"""
    offset : float = 0
    """distance between the route waypoints and the center of the lane"""
    
    # Aliases used:
    @property
    def max_throt(self):
        return self.max_throttle

    @property
    def max_steer(self):
        return self.max_steering

@dataclass
class BehaviorAgentControllerSettings(BasicAgentControllerSettings):
    pass

@dataclass
class AutopilotControllerSettings(AgentConfig):
    vehicle_lane_offset : float = 0
    """
    Sets a lane offset displacement from the center line. Positive values imply a right offset while negative ones mean a left one.
    Default is 0. Numbers high enough to cause the vehicle to drive through other lanes might break the controller.
    """
    
@dataclass
class LunaticAgentControllerSettings(AutopilotControllerSettings, BehaviorAgentControllerSettings):
    vehicle_lane_offset : float = II("controls.offset")
    """distance between the route waypoints and the center of the lane"""

# ---------------------
# PlannerSettings
# ---------------------

@dataclass
class BasicAgentPlannerSettings(AgentConfig):
    """
    PID controller using the following semantics:
            K_P -- Proportional term
            K_D -- Differential term
            K_I -- Integral term
    offset: If different than zero, the vehicle will drive displaced from the center line.
    Positive values imply a right offset while negative ones mean a left one. 
    Numbers high enough to cause the vehicle to drive through other lanes might break the controller.
    
    Notes:
    `sampling_resolution` is used by the global planner to build a graph of road segments, also to get a path of waypoints from A to B

    `sampling_radius` is similar but only used only by the local_planner to compute the next waypoints forward. The distance of those is the sampling_radius.
    
    """
    
    dt : float = 1.0 / 20.0
    """time between simulation steps."""
    
    sampling_radius : float = 2.0
    """
    Distance between waypoints when planning a path in `local_planner._compute_next_waypoints`
    
    Used with Waypoint.next(sampling_radius)
    """
    
    sampling_resolution : float = 2.0
    """
    Distance between waypoints in `BasicAgent._generate_lane_change_path`
    Furthermore in the GlobalRoutePlanner to build the topology and for path planning.
    
    Used with the Waypoint.next(sampling_radius) and distance between waypoints.
    """
    # Alias
    #step_distance : float = II(".sampling_resolution")
    @property
    def step_distance(self):
        return self.sampling_resolution # TODO:update
    
    # NOTE: two variables because originally used with two different names in different places
    lateral_control_dict : Dict[str, float] = field(default_factory=lambda:{'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2, 'dt': II("..dt")})
    """values of the lateral PID controller"""
    args_lateral_dict : Dict[str, float] = II("${.lateral_control_dict}")
    """values of the lateral PID controller"""

    # NOTE: two variables because originally used with two different names in different places
    longitudinal_control_dict : Dict[str, float]  = field(default_factory=lambda:{'K_P': 1.0, 'K_I': 0.05, 'K_D': 0, 'dt': II("..dt")}) # Note: ${..dt} points to planner.dt, similar to a directory
    """values of the longitudinal PID controller"""
    args_longitudinal_dict : Dict[str, float] = II("${.longitudinal_control_dict}") # points to the variable above
    """values of the longitudinal PID controller"""
    
    

@dataclass
class BehaviorAgentPlannerSettings(BasicAgentPlannerSettings):
    sampling_resolution : float = 4.5
    """
    Distance between waypoints in `BasicAgent._generate_lane_change_path`
    and GlobalRoutePlanner to build the topology and path planning.
    
    Used with the Waypoint.next(sampling_radius)
    """
    
@dataclass
class LunaticAgentPlannerSettings(BehaviorAgentPlannerSettings):
    dt : float = MISSING # 1.0 / 20.0 # Note: Set this from main script and do not assume it.
    """
    Time between simulation steps.
    
    NOTE: Should set from main script.
    """

# ---------------------
# Emergency
# ---------------------
    
@dataclass
class BasicAgentEmergencySettings(AgentConfig):
    throttle : float = 0.0
    brake : float = II("controls.max_brake")
    hand_brake : bool = False
    
    
@dataclass
class BehaviorAgentEmergencySettings(BasicAgentEmergencySettings):
    pass


@dataclass
class LunaticAgentEmergencySettings(BehaviorAgentEmergencySettings):
    ignore_percentage : float = 0.0
    """Percentage of time to ignore an emergency situation and proceed as normal"""
    
    hand_brake_modify_chance: float = 0.0
    """Chance to choose the opposite of hand_break"""
    
    do_random_steering : bool = False # TODO: Should be evasive steering
    """Whether to do random steering"""
    
    random_steering_range : Tuple[float, float] = (-0.25, 0.25)
    """Range of random steering that is applied"""

# ---------------------
# RSS
# --------------------- 

# Boost.Python.enum cannot be used as annotations for omegaconf, replacing them by real enums,
# Functional API is easier to create but cannot be used as type hints
if AD_RSS_AVAILABLE:
    RssRoadBoundariesMode = Enum("RssRoadBoundariesMode", {str(name):value for value, name in carla.RssRoadBoundariesMode.values.items()}, module=__name__)
    RssLogLevel = Enum("RssLogLevel", {str(name):value for value, name in carla.RssLogLevel.values.items()}, module=__name__)
elif TYPE_CHECKING and sys.version_info >= (3, 10):
    from typing import TypeAlias
    RssLogLevel : TypeAlias = Union[int, str]
    RssRoadBoundariesMode : TypeAlias = Union[int, str, bool]
else:
    RssLogLevel = Union[int, str]
    RssRoadBoundariesMode = Union[int, str, bool]
    
@dataclass
class RssSettings(AgentConfig):
    enabled : bool = True
    """
    Use the RSS sensor.
    
    NOTE: Initializing with False and changing it to True is not supported.
    If RSS is not available (no ad-rss library) this will be set to False.
    """
    
    if AD_RSS_AVAILABLE:
        use_stay_on_road_feature : RssRoadBoundariesMode = carla.RssRoadBoundariesMode.On # type: ignore
        """Use the RssRoadBoundariesMode. NOTE: A call to `rss_set_road_boundaries_mode` is necessary"""
        
        log_level : RssLogLevel = carla.RssLogLevel.info # type: ignore
        """Set the initial log level of the RSSSensor"""
    else:
        use_stay_on_road_feature : "RssRoadBoundariesMode" = True # type: ignore
        """Use the RssRoadBoundariesMode. NOTE: A call to `rss_set_road_boundaries_mode` is necessary"""
        
        log_level : "RssLogLevel" = "info" # type: ignore
        """Set the initial log level of the RSSSensor"""
        
        
        
    
    def _clean_options(self):
        if AD_RSS_AVAILABLE:
            if not isinstance(self.use_stay_on_road_feature, RssRoadBoundariesMode):
                self.use_stay_on_road_feature = int(self.use_stay_on_road_feature)
            if not isinstance(self.log_level, RssLogLevel):
                self.log_level = int(self.log_level)
        else:
            if not isinstance(self.use_stay_on_road_feature, (bool, str)):
                self.log_level = bool(self.use_stay_on_road_feature)
    

# ---------------------

@dataclass
class AutopilotBehavior(AgentConfig):
    """
    These are settings from the autopilot carla.TrafficManager which are not exposed or not used by the original carla agents.
    NOTE: That default values do not exist for most settings; we should set it to something reasonable.
    """

    auto_lane_change: bool = True
    """Turns on or off lane changing behavior for a vehicle."""
    
    vehicle_lane_offset : str = II("controls.offset")
    """
    Sets a lane offset displacement from the center line.
    
    Positive values imply a right offset while negative ones mean a left one. 
    Default is 0. 
    
    NOTE: Numbers high enough to cause the vehicle to drive through other lanes might break the controller.
    """

    random_left_lanechange_percentage: float = 0.1
    """
    Adjust probability that in each timestep the actor will perform a left/right lane change, 
    dependent on lane change availability.
    """
    random_right_lanechange_percentage : float = 0.1
    """
    Adjust probability that in each timestep the actor will perform a left/right lane change, 
    dependent on lane change availability.
    """

    keep_right_rule_percentage: float = 0.7
    """
    During the localization stage, this method sets a percent chance that vehicle will follow the keep right rule, 
    and stay in the right lane.
    """

    distance_to_leading_vehicle : float = 5.0
    """
    Sets the minimum distance in meters that a vehicle has to keep with the others. 
    The distance is in meters and will affect the minimum moving distance. It is computed from front to back of the vehicle objects. 
    """

    vehicle_percentage_speed_difference : float = 30 # in percent
    """
    NOTE: in percent.
    Sets the difference the vehicle's intended speed and its current speed limit. 
    Speed limits can be exceeded by setting the perc to a negative value. 
    Default is 30. Exceeding a speed limit can be done using negative percentages.
    """
    
    ignore_lights_percentage : float = 0.0
    ignore_signs_percentage : float = 0.0
    ignore_walkers_percentage : float = 0.0

    update_vehicle_lights : bool = False
    """Sets if the Traffic Manager is responsible of updating the vehicle lights, or not."""
    

@dataclass
class SimpleBasicAgentSettings(LiveInfo, BasicAgentSpeedSettings, BasicAgentDistanceSettings, BasicAgentLaneChangeSettings, BasicAgentObstacleSettings, BasicAgentControllerSettings, BasicAgentPlannerSettings, BasicAgentEmergencySettings):
    pass

@dataclass
class SimpleBehaviorAgentSettings(LiveInfo, BehaviorAgentSpeedSettings, BehaviorAgentDistanceSettings, BehaviorAgentLaneChangeSettings, BehaviorAgentObstacleSettings, BehaviorAgentControllerSettings, BehaviorAgentPlannerSettings, BehaviorAgentEmergencySettings):
    pass

@dataclass
class SimpleAutopilotAgentSettings(AutopilotSpeedSettings, AutopilotDistanceSettings, AutopilotLaneChangeSettings, AutopilotObstacleSettings, AutopilotControllerSettings):
    pass

@dataclass
class SimpleLunaticAgentSettings(LiveInfo, LunaticAgentSpeedSettings, LunaticAgentDistanceSettings, LunaticAgentLaneChangeSettings, LunaticAgentObstacleSettings, LunaticAgentControllerSettings, LunaticAgentPlannerSettings, LunaticAgentEmergencySettings, RssSettings):
    pass


@dataclass
class BasicAgentSettings(AgentConfig):
    overwrites : Optional[Dict[str, dict]] = field(default_factory=dict, repr=False)
    live_info : LiveInfo = field(default_factory=LiveInfo, init=False)
    speed : BasicAgentSpeedSettings = field(default_factory=BasicAgentSpeedSettings, init=False)
    distance : BasicAgentDistanceSettings = field(default_factory=BasicAgentDistanceSettings, init=False)
    lane_change : BasicAgentLaneChangeSettings = field(default_factory=BasicAgentLaneChangeSettings, init=False)
    obstacles : BasicAgentObstacleSettings = field(default_factory=BasicAgentObstacleSettings, init=False)
    controls : BasicAgentControllerSettings = field(default_factory=BasicAgentControllerSettings, init=False)
    planner : BasicAgentPlannerSettings = field(default_factory=BasicAgentPlannerSettings, init=False)
    emergency : BasicAgentEmergencySettings = field(default_factory=BasicAgentEmergencySettings, init=False)
        
    
@dataclass
class BehaviorAgentSettings(AgentConfig):
    overwrites : Optional[Dict[str, dict]] = field(default_factory=dict, repr=False)
    live_info : LiveInfo = field(default_factory=LiveInfo, init=False)
    speed : BehaviorAgentSpeedSettings = field(default_factory=BehaviorAgentSpeedSettings, init=False)
    distance : BehaviorAgentDistanceSettings = field(default_factory=BehaviorAgentDistanceSettings, init=False)
    lane_change : BehaviorAgentLaneChangeSettings = field(default_factory=BehaviorAgentLaneChangeSettings, init=False)
    obstacles : BehaviorAgentObstacleSettings = field(default_factory=BehaviorAgentObstacleSettings, init=False)
    controls : BehaviorAgentControllerSettings = field(default_factory=BehaviorAgentControllerSettings, init=False)
    planner : BehaviorAgentPlannerSettings = field(default_factory=BehaviorAgentPlannerSettings, init=False)
    emergency : BehaviorAgentEmergencySettings = field(default_factory=BehaviorAgentEmergencySettings, init=False)
    
@dataclass
class LunaticAgentSettings(AgentConfig):
    overwrites : Optional[Dict[str, dict]] = field(default_factory=dict, repr=False)
    live_info : LiveInfo = field(default_factory=LiveInfo, init=False)
    speed : LunaticAgentSpeedSettings = field(default_factory=LunaticAgentSpeedSettings, init=False)
    distance : LunaticAgentDistanceSettings = field(default_factory=LunaticAgentDistanceSettings, init=False)
    lane_change : LunaticAgentLaneChangeSettings = field(default_factory=LunaticAgentLaneChangeSettings, init=False)
    obstacles : LunaticAgentObstacleSettings = field(default_factory=LunaticAgentObstacleSettings, init=False)
    controls : LunaticAgentControllerSettings = field(default_factory=LunaticAgentControllerSettings, init=False)
    planner : LunaticAgentPlannerSettings = field(default_factory=LunaticAgentPlannerSettings, init=False)
    emergency : LunaticAgentEmergencySettings = field(default_factory=LunaticAgentEmergencySettings, init=False)
    rss : RssSettings = field(default_factory=RssSettings, init=False)
    

if __name__ == "__main__":
    #basic_agent_settings = OmegaConf.structured(BasicAgentSettings)
    #behavior_agent_settings = OmegaConf.structured(BehaviorAgentSettings)
    lunatic_agent_settings = OmegaConf.structured(LunaticAgentSettings, flags={"allow_objects": True})
    
    c : LunaticAgentSettings = LunaticAgentSettings().get_options()
    d : LunaticAgentSettings = LunaticAgentSettings.get_options()
    try:
        c.rss.log_level = "asda"
        raise TypeError("Should only raise if AD_RSS_AVAILABLE is False")
    except ValueError as e:
        print("Correct ValueError", e)
        pass
    #  Using OmegaConf.set_struct, it is possible to prevent the creation of fields that do not exist: