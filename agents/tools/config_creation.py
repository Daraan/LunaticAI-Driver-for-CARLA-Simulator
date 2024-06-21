# DO NOT USE from __future__ import annotations ! This would break the dataclass interface.

import os
import sys
from collections.abc import Mapping


from classes.camera_manager import CameraBlueprint
from classes.rss_visualization import RssDebugVisualizationMode
if __name__ == "__main__": # TEMP clean at the end, only here for testing
    import os
    sys.path.append(os.path.abspath("../"))

from enum import Enum, IntEnum
from functools import partial, wraps
from dataclasses import dataclass, field, asdict, is_dataclass
import typing
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Dict, List, Optional, Tuple, Type, Union, cast

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

import ast
import inspect
from agents.navigation.local_planner import RoadOption
from classes.rss_sensor import AD_RSS_AVAILABLE

__all__ = ["AgentConfig", 
           "SimpleConfig", 
           "BasicAgentSettings", 
           "BehaviorAgentSettings", 
           "SimpleBasicAgentSettings", 
           "SimpleBehaviorAgentSettings",
           "LunaticAgentSettings",
           "SimpleLunaticAgentSettings",
           "AutopilotBehavior",
           
           "CameraConfig",
           "LaunchConfig",
        ]

_class_annotations = None
_file_path = __file__

# ---------------------
# Helper methods
# ---------------------

# need this check for readthedocs
if os.environ.get("_OMEGACONF_RESOLVERS_REGISTERED", "0") == "0":
    OmegaConf.register_new_resolver("sum", lambda x, y: x + y)
    OmegaConf.register_new_resolver("subtract", lambda x, y: x + y)
    OmegaConf.register_new_resolver("min", lambda *els: min(els))
    os.environ["_OMEGACONF_RESOLVERS_REGISTERED"] = "1"

class class_or_instance_method:
    """Decorator to transform a method into both a regular and class method"""
    
    def __init__(self, call):
        self.__wrapped__ = call
        self._wrapper = lambda x : x # TODO: functools.partial and functools.wraps shadow the signature, this reveals it again.

    def __get__(self, instance : Union[None, "AgentConfig"], owner : Type["AgentConfig"]):
        if instance is None:  # called on class 
            return self._wrapper(partial(self.__wrapped__, owner))
        return self._wrapper(partial(self.__wrapped__, instance)) # called on instance


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

# ---------------------
# Base Classes
# ---------------------

class AgentConfig:
    """
    Base interface for the agent settings. 
    
    Handling the initialization from a nested dataclass and merges in the changes
    from the overwrites options.
    """
    overwrites: "Optional[Dict[str, Union[dict, AgentConfig]]]" = None
    
    @classmethod
    def get_defaults(cls) -> "AgentConfig":
        """Returns the global default options."""
        return cls()
    
    @class_or_instance_method
    def export_options(cls_or_self, path, category=None, resolve=False, with_comments=False) -> None:
        """Exports the options to a yaml file."""
        if inspect.isclass(cls_or_self):
            cls_or_self = cls_or_self()
        if category is None:
            options = cls_or_self
        else:
            options = cls_or_self[category]
        if with_comments:
            string = cls_or_self.to_yaml(resolve=resolve, yaml_commented=True)
            with open(path, "w") as f:
                f.write(string)
            return
        if not isinstance(options, DictConfig): 
            # TODO: look how we can do this directly from dataclass
            options = OmegaConf.create(options, flags={"allow_objects": True})
        OmegaConf.save(options, path, resolve=resolve) # NOTE: This might raise if options is structured, for export structured this is actually not necessary.
        
    @class_or_instance_method
    def simplify_options(cls_or_self, category=None, *, resolve, yaml=False, yaml_commented=True, **kwargs):
        """
        Returns a dictionary of all options or a string in yaml format.
        
        :param category: The category of options to retrieve. If None, retrieves all options.
        :param resolve: Whether to resolve and interpolate values.
        :param yaml: Whether to return the options as YAML formatted string
        :param kwargs: Additional keyword arguments to pass to OmegaConf.to_container or OmegaConf.to_yaml.
        
        :return: The dictionary or str of options.
        """
        if inspect.isclass(cls_or_self):
            cls_or_self = cls_or_self()
        if category is None:
            options = cls_or_self
        else:
            options = getattr(cls_or_self, category)
        if not isinstance(options, DictConfig) and not resolve and not yaml:
            return asdict(options)
        if not isinstance(options, DictConfig):
            options = OmegaConf.structured(options, flags={"allow_objects": True})
        if yaml:
            return OmegaConf.to_yaml(options, resolve=resolve, **kwargs)
        return OmegaConf.to_container(options, resolve=resolve, **kwargs)
    
    @class_or_instance_method
    def to_yaml(cls_or_self, resolve=False, yaml_commented=True) ->  str:
        return cls_or_self.simplify_options(resolve=resolve, yaml=True, yaml_commented=yaml_commented)
    
    @classmethod
    def from_yaml(cls, path, category : Optional[str]=None, *, merge=True):
        """Loads the options from a yaml file."""
        if merge:
            options : cls = OmegaConf.merge(OmegaConf.create(cls, flags={"allow_objects":True}), OmegaConf.load(path))
        else:
            options : cls = OmegaConf.load(path)
        if category is None:
            return options
        r : cls = cast(cls, options[category])
        return r
    
    @classmethod
    def create_from_args(cls, args_agent:"Union[os.PathLike, dict, DictConfig, Mapping]", 
                         overwrites:"Optional[Mapping]"=None, 
                         *,
                         assure_copy : bool = False,
                         dict_config_no_parent:bool = True,
                         config_mode:Optional[SCMode]=None # SCMode.DICT_CONFIG # NOTE: DICT_CONFIG is only good when we have a structured config 
                         ):
        """
        Creates the agent settings based on the provided arguments.

        Args:
            cls (ConfigType): The type of the agent settings.
            args_agent (Union[os.PathLike, dict, DictConfig, dataclass]): The argument specifying the agent settings. It can be a path to a YAML file, a dictionary, a dataclass, or a DictConfig.
            overwrites (Optional[Mapping]): Optional mapping containing additional settings to overwrite the default agent settings.
            config_mode (omegaconf.SCMode, optional): 
                Optional configuration mode for structured config. 
                If None the return type might not be a DictConfig.
                Defaults to SCMode.DICT_CONFIG.

        Returns:
            ConfigType: The created agent settings.

        Raises:
            Exception: If the overwrites cannot be merged into the agent settings.

        """
        from agents.tools.logging import logger
        behavior : cls
        if isinstance(args_agent, dict):
            logger.debug("Using agent settings from dict with LunaticAgentSettings. Note settings are NOT a dict config. Interpolations not available.")
            behavior = cls(**args_agent) # NOTE: Not a dict config
        elif isinstance(args_agent, str):
            logger.info("Using agent settings from file `%s`", args_agent)
            behavior = cls.from_yaml(args_agent)
        elif is_dataclass(args_agent) or isinstance(args_agent, DictConfig):
            logger.info("Using agent settings as is, as it is a dataclass or DictConfig.")
            if assure_copy:
                behavior : cls = OmegaConf.create(args_agent, flags={"allow_objects": True})
            elif isinstance(args_agent, type):
                behavior = args_agent()
            else:
                behavior = args_agent
        else:
            if config_mode is None or config_mode == SCMode.DICT:
                logger.warning("Type `%s` of launch argument type `agent` not supported, trying to use it anyway. Expected are (str, dataclass, DictConfig)", type(args_agent))
            if isinstance(args_agent, type):
                behavior = args_agent() # be sure to have an instance
            if assure_copy:
                from copy import deepcopy
                behavior = deepcopy(args_agent)
            else:
                behavior = args_agent
        if config_mode is not None:
            logger.debug("Converting agent settings (type: %s) to to container via %s", type(behavior), config_mode)
            if not isinstance(behavior, DictConfig):
                behavior = OmegaConf.create(behavior, flags={"allow_objects": True})
            behavior = OmegaConf.to_container(behavior, structured_config_mode=config_mode)
        
        if overwrites:
            if isinstance(behavior, DictConfig):
                behavior = OmegaConf.merge(behavior, OmegaConf.create(overwrites, flags={"allow_objects": True}))
            else:
                try:
                    behavior.update(overwrites)
                except:
                    logger.error("Overwrites could not be merged into the agent settings with `base_config.update(overwrites)`. config_mode=SCMode.DICT_CONFIG is recommended for this to work.")
                    raise
        if isinstance(behavior, DictConfig):
            behavior._set_flag("allow_objects", True)
            if dict_config_no_parent:
                # Dict config interpolations always use the full path, interpolations might go from the root of the config.
                # If there is launch_config.agent, with launch config as root, the interpolations will not work.
                behavior.__dict__["_parent"] = None # Remove parent from
        
        return cast(cls, behavior)
        
    
    @class_or_instance_method
    def make_config(cls_or_self : ConfigType, category:Optional[str]=None, *, lock_interpolations=True, lock_fields:Optional[List[str]]=None) -> ConfigType:
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
    
    def update(self, options : "Union[dict, AgentConfig]", clean=True):
        """Updates the options with a new dictionary."""
        if isinstance(options, AgentConfig):
            key_values = options.__dataclass_fields__.items()
        else:
            key_values = options.items()
        for k, v in key_values:
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
        # Merge the overwrite dict into the correct ones.
        for key, value in self.overwrites.items():
            if key in self.__annotations__:
                if issubclass(self.__annotations__[key], AgentConfig):
                    getattr(self, key).update(value)
                else:
                    print("is not a Config")
                    setattr(self, key, value)
            else:
                print(f"Warning: Key '{key}' not found in {self.__class__.__name__} default options. Consider updating or creating a new class to avoid this message.")


class SimpleConfig(object):
    """
    A class that allows a more simple way to initialize settings.
    Initializing an instance changes the type the the given base class, defined via `_base_settings`.
    
    :param _base_settings: The base class to port the settings to.
    
    TODO: NOTE: This class assumes that there are NO DUPLICATE keys in the underlying base
    """
    
    _base_settings: ClassVar["AgentConfig"] = None
    
    def __new__(cls, overwrites:Optional[Dict[str, Union[dict, AgentConfig]]]=None) -> "AgentConfig":
        """
        Transforms a SimpleConfig class into the given _base_settings
        
        :param overwrites: That allow overwrites during initialization.
        """
        if cls._base_settings is None:
            raise TypeError("{cls.__name__} must have a class set in the `_base_settings` to initialize to.")
        if cls is SimpleConfig:
            raise TypeError("SimpleConfig class may not be instantiated")
        simple_settings = {k:v for k,v  in cls.__dict__.items() if not k.startswith("_") } # Removes all private attributes
        if overwrites:
            simple_settings.update(overwrites) 
        return super().__new__(cls).to_nested_config(simple_settings) # call from a pseudo instance.
    
    @class_or_instance_method
    def to_nested_config(self, simple_overwrites:dict=None) -> AgentConfig:
        """
        Initializes the _base_settings with the given overwrites.
        
        Maps the keys of simple_overwrites to the base settings.
        
        More specifically builds a overwrites dict that is compatible with the nested configuration versions.
        
        NOTE: Assumes unique keys over all settings!
        # TODO: add a warning if a non-unique key is found in the overwrites.
        """
        if isinstance(self, type): # called on class
            return self()
        keys = set(simple_overwrites.keys())
        removed_keys = set() # to check for duplicated keys that cannot be set via SimpleConfig unambiguously
        overwrites = {}
        for name, base in self._base_settings.__annotations__.items():
            if not isinstance(base, type) or not issubclass(base, AgentConfig): # First out non AgentConfig attributes
                if name in keys:
                    overwrites[name] = simple_overwrites[name] # if updating a top level attribute
                    keys.remove(name)
                    removed_keys.add(name)
                continue
            matching = keys.intersection(base.__dataclass_fields__.keys()) # keys that match from the simple config to the real nested config
            if len(matching) > 0:
                if removed_keys.intersection(matching):
                    print("WARNING: Ambiguous key", removed_keys.intersection(matching), "in the SimpleConfig", str(self), "that occurs multiple times in its given base", self._base_settings.__name__+".", "Encountered at", name, base) # TODO: remove later, left here for testing.")
                overwrites[name] = {k: getattr(self, k) for k in matching}
                keys -= matching
                removed_keys.update(matching)
        if len(keys) != 0:
            overwrites.update({k: v for k,v in simple_overwrites.items() if k in keys}) # Add them to the top level
            print("Warning: Unmatched keys", keys, "in", self.__class__.__name__, "not contained in base", self._base_settings.__name__+".", "Adding them to the top-level of the settings.") # TODO: remove later, left here for testing.
        return self._base_settings(overwrites=overwrites)
        # TODO: could add new keys after post-processing.
        
        
# ---------------------

# ---------------------
# Live Info
# ---------------------

@dataclass
class LiveInfo(AgentConfig):
    """Keeps track of information that changes during the simulation."""
    
    use_srunner_data_provider : bool = True
    """
    If enabled makes use of the scenario_runner CarlaDataProvider assuming 
    that its information is up to date and complete, e.g. tracks all actors.
    
    NOTE: Turning this off is not fully supported.
    """
    
    velocity_vector : carla.Vector3D = MISSING
    """
    3D Vector of the current velocity of the vehicle.
    """
    
    current_speed : float = MISSING
    """
    Velocity of the vehicle in km/h.
    
    Note if use_srunner_data_provider is True the z component is ignored.
    """
    
    current_transform : carla.Transform = MISSING
    current_location : carla.Location = MISSING
    
    current_speed_limit : float = MISSING
    
    executed_direction : RoadOption = MISSING
    """
    Direction that was executed in the last step by the local planner
    
    planner.target_road_option is the option last executed by the planner (constant)
    incoming direction is the next *planned* direction subject to change (variable)
    """
    
    incoming_direction : RoadOption = MISSING
    """
    RoadOption that will used for the current step
    """
    
    incoming_waypoint : carla.Waypoint = MISSING
    """
    Waypoint that is planned to be targeted in this step.
    """
    
    is_taking_turn : bool = MISSING
    """
    incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)
    """
    
    is_changing_lane : bool = MISSING
    """
    incoming_direction in (RoadOption.CHANGELANELEFT, RoadOption.CHANGELANERIGHT)
    """
    
    next_traffic_light : Union[carla.TrafficLight, None] = MISSING
    """
    Traffic light that is closest to the next intersection.
    
    Is `None` if the agent is at an intersection.
    
    + NOTE: This might not be in the path or infront of the vehicle.
    """
    
    next_traffic_light_distance : Union[float, None] = MISSING
    """
    Distance to the assumed next traffic light.
    """
    
    last_applied_controls: carla.VehicleControl = MISSING
    """
    VehicleControls 
    """
    
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
    speed_decrease : float = 10
    """other_vehicle_speed"""
    
    safety_time : float = 3
    """Time in s before a collision at the same speed -> apply speed_decrease"""

    # CASE B
    min_speed : float = 5
    """Implement als variable, currently hard_coded"""

    # All Cases
    speed_lim_dist : float = 3
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
    pass
    

@dataclass
class BehaviorAgentDistanceSettings(BasicAgentDistanceSettings):
    """
    Collision Avoidance
    -------------------

    Distance in which for vehicles are checked.
    
    Usage: max_distance = max(min_proximity_threshold, self._speed_limit / (2 if <LANE CHANGE> else 3 ) )
    """
    
    min_proximity_threshold : float = 10
    """Range in which cars are detected. NOTE: Speed limit overwrites"""
    
    emergency_braking_distance : float = 5
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
    Timings in seconds to finetune the lane change behavior.
    
    NOTE: see: `BasicAgent.lane_change` and `BasicAgent._generate_lane_change_path`
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
        
    Usage: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
    Usage: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed
    """
    
    base_vehicle_threshold : float = 5.0
    """
    Base distance to vehicles to check if they affect the vehicle
            
    Usage: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
    Usage: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed
    """

    detection_speed_ratio : float = 1.0
    """
    Increases detection range based on speed
    
    Usage: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
    Usage: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed
    """
    
    dynamic_threshold : bool = True
    """
    Whether to add a dynamic threshold based on the vehicle speed to the base threshold.
    
    Usage: base_threshold + detection_speed_ratio * vehicle_speed
    
    + NOTE: Currently only applied to traffic lights
    
    + NOTE: Part of the agent overhaul
    """
    
    detection_angles : BasicAgentObstacleDetectionAngles = field(default_factory=BasicAgentObstacleDetectionAngles)
    """Defines detection angles used when checking for obstacles."""


@dataclass
class BehaviorAgentObstacleSettings(BasicAgentObstacleSettings):
    nearby_vehicles_max_distance: float = 45
    """For performance filters out vehicles that are further away than this distance in meters"""
    
    nearby_walkers_max_distance: float = 10
    """For performance filters out pedestrians that are further away than this distance in meters"""


@dataclass
class AutopilotObstacleSettings(AgentConfig):
    ignore_lights_percentage : float = 0.0
    """
    Percentage of time to ignore traffic lights
    """
    
    ignore_signs_percentage : float = 0.0
    """
    Percentage of time to ignore stop signs
    """
    
    ignore_walkers_percentage : float = 0.0
    """
    Percentage of time to ignore pedestrians
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
    dynamic_threshold : bool = True
    """
    Whether to add a dynamic threshold based on the vehicle speed to the base threshold.
    
    Usage: base_threshold + detection_speed_ratio * vehicle_speed
    
    #NOTE: Currently only applied to traffic lights
    """
    
    detection_angles: LunaticAgentObstacleDetectionAngles = field(default_factory=LunaticAgentObstacleDetectionAngles)
    
# ---------------------
# Emergency
# ---------------------

# ---------------------
# ControllerSettings
# ---------------------

@dataclass
class BasicAgentControllerSettings(AgentConfig):
    """Limitations of the controls used one the PIDController Level"""
    
    max_brake : float = 0.5
    """
    Vehicle control how strong the brake is used, 
    
    NOTE: Also used in emergency stop
    """
    max_throttle : float = 0.75
    """maximum throttle applied to the vehicle"""
    max_steering : float = 0.8
    """maximum steering applied to the vehicle"""
    
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
    pass

# ---------------------
# PlannerSettings
# ---------------------

@dataclass
class PIDControllerDict:
    """
    PID controller using the following semantics:
        K_P -- Proportional term
        K_D -- Differential term
        K_I -- Integral term
        dt -- time differential in seconds
    """
            
    K_P : float = MISSING
    K_D : float = MISSING
    K_I : float = 0.05
    dt : float = 1.0 / 20.0
    """time differential in seconds"""

@dataclass
class BasicAgentPlannerSettings(AgentConfig):
    """
    PID controller using the following semantics:
            K_P -- Proportional term
            K_D -- Differential term
            K_I -- Integral term
            dt -- time differential in seconds
    offset: If different than zero, the vehicle will drive displaced from the center line.
    Positive values imply a right offset while negative ones mean a left one. 
    Numbers high enough to cause the vehicle to drive through other lanes might break the controller.
    
    Notes:
    `sampling_resolution` is used by the global planner to build a graph of road segments, also to get a path of waypoints from A to B

    `sampling_radius` is similar but only used only by the local_planner to compute the next waypoints forward. The distance of those is the sampling_radius.
    
    """
    
    dt : float = 1.0 / 20.0
    """time differential in seconds"""
    
    # NOTE: two variables because originally used with two different names in different places
    #lateral_control_dict : PIDControllerDict = field(default_factory=partial(PIDControllerDict, **{'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2}))
    lateral_control_dict : PIDControllerDict = field(default_factory=lambda:PIDControllerDict(**{'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2}))
    """values of the lateral PID controller"""

    # NOTE: two variables because originally used with two different names in different places
    longitudinal_control_dict : PIDControllerDict  = field(default_factory=lambda:PIDControllerDict(**{'K_P': 1.0, 'K_I': 0.05, 'K_D': 0}))
    """values of the longitudinal PID controller"""
    
    offset : float = 0.0
    """
    If different than zero, the vehicle will drive displaced from the center line.
    
    Positive values imply a right offset while negative ones mean a left one. Numbers high enough
    to cause the vehicle to drive through other lanes might break the controller.
    """
    
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
    
    min_distance_next_waypoint : float = 3.0
    """
    Removes waypoints from the queue that are too close to the vehicle.
    
    Usage: min_distance = min_distance_next_waypoint + next_waypoint_distance_ratio * vehicle_speed 
    """
    
    next_waypoint_distance_ratio : float = 0.5
    """Increases the minimum distance to the next waypoint based on the vehicles speed."""
    
    # Alias
    @property
    def step_distance(self):
        return self.sampling_resolution


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
    time differential in seconds
    
    NOTE: Should set from main script.
    """
    
    # NOTE: two variables because originally used with two different names in different places
    lateral_control_dict : PIDControllerDict = field(default_factory=partial(PIDControllerDict, **{'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2, 'dt': II("${..dt}")}))
    """values of the lateral PID controller"""

    # NOTE: two variables because originally used with two different names in different places
    longitudinal_control_dict : PIDControllerDict  = field(default_factory=partial(PIDControllerDict, **{'K_P': 1.0, 'K_I': 0.05, 'K_D': 0, 'dt': II("${..dt}")}))
    """values of the longitudinal PID controller"""
    
    offset: float = II("controls.vehicle_lane_offset")
    """
    If different than zero, the vehicle will drive displaced from the center line.
    
    Positive values imply a right offset while negative ones mean a left one. Numbers high enough
    to cause the vehicle to drive through other lanes might break the controller.
    """


# ---------------------
# Emergency
# ---------------------
    
@dataclass
class BasicAgentEmergencySettings(AgentConfig):
    throttle : float = 0.0
    max_emergency_brake : float = II("controls.max_brake")
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
    RssRoadBoundariesModeAlias = IntEnum("RssRoadBoundariesModeAlias", {str(name):value for value, name in carla.RssRoadBoundariesMode.values.items()}, module=__name__)
    RssLogLevelAlias = IntEnum("RssLogLevelAlias", {str(name):value for value, name in carla.RssLogLevel.values.items()}, module=__name__)

    for value, name in carla.RssRoadBoundariesMode.values.items():
        assert RssRoadBoundariesModeAlias[str(name)] == value
        
    for value, name in carla.RssLogLevel.values.items():
        assert RssLogLevelAlias[str(name)] == value

elif TYPE_CHECKING and sys.version_info >= (3, 10):
    from typing import TypeAlias
    RssLogLevelAlias : TypeAlias = Union[int, str]
    RssRoadBoundariesModeAlias : TypeAlias = Union[int, str, bool]
else:
    RssLogLevelAlias = Union[int, str]
    RssRoadBoundariesModeAlias = Union[int, str, bool]
    
@dataclass
class RssSettings(AgentConfig):
    
    enabled : bool = True
    """
    Use the RSS sensor.
    
    NOTE: Initializing with False and changing it to True is not supported.
    If RSS is not available (no ad-rss library) this will be set to False.
    """
    
    if AD_RSS_AVAILABLE:
        use_stay_on_road_feature : carla.RssRoadBoundariesMode = carla.RssRoadBoundariesMode.On 
        """Use the RssRoadBoundariesMode. NOTE: A call to `rss_set_road_boundaries_mode` is necessary"""
        
        log_level : carla.RssLogLevel = carla.RssLogLevel.warn 
        """Set the initial log level of the RSSSensor"""
    else:
        enabled = False
        
        use_stay_on_road_feature : "RssRoadBoundariesModeAlias" = "On" # type: ignore
        """Use the RssRoadBoundariesMode. NOTE: A call to `rss_set_road_boundaries_mode` is necessary"""
        
        log_level : "RssLogLevelAlias" = "warn" # type: ignore
        """Set the initial log level of the RSSSensor"""
        
    debug_visualization_mode: RssDebugVisualizationMode = RssDebugVisualizationMode.RouteOnly
    """Sets the visualization mode that should be rendered on the screen."""
    
    always_accept_update: bool = False
    """Setting for the default rule to always accept RSS updates if they are valid"""
    
    rss_max_speed: float = MISSING # NotImplemented
    """For fast vehicles RSS currently is unreliable, disables rss updates when the vehicle is faster than this."""
    
    # ------
    
    def _clean_options(self):
        if AD_RSS_AVAILABLE:
            if not isinstance(self.use_stay_on_road_feature, RssRoadBoundariesModeAlias):
                self.use_stay_on_road_feature = int(self.use_stay_on_road_feature)
            if not isinstance(self.log_level, RssLogLevelAlias):
                self.log_level = int(self.log_level)
        else:
            if not isinstance(self.use_stay_on_road_feature, (bool, str)):
                self.use_stay_on_road_feature = bool(self.use_stay_on_road_feature)
                


@dataclass
class DataMatrixSettings(AgentConfig):
    enabled : bool = True
    """Use the DataMatrix"""
    
    sync: bool = True
    """
    When the world uses synchronous mode and sync is true, the data matrix will be updated every sync_interval ticks.
    A low value will have a negative impact on the fps.
    If the world uses asynchronous mode or sync is False the data matrix will be updated by a different thread.
    This increases the fps but updates will be less frequent.
    """
    
    sync_interval: int = 5
    """
    The interval in frames after which the data matrix should be updated. Sync must be true.
    """

    __hud_default = {
                    'draw': True,
                    'values': True,
                    'vertical' : True,
                    'imshow_settings': {'cmap': 'jet'},
                    'text_settings' : {'color': 'orange'} 
                    }
    hud: Dict[str, Any] = field(default_factory=__hud_default.copy)
    """
    XXX
    
    TODO: do not have this in Agent config but in
    hud : ${camera.hud.data_matrix}
     #drawing_options -> see camera.yaml
     #NOTE: this interpolation might fail if the parent has been removed!
    
    ---
        
    Keyword arguments for `DataMatrix.render`
    NOTE: The default_settings substitute this with an interpolation that might not work,
    as it relies on the parent LaunchConfig that is currently removed.
    
    `camera.hud.data_matrix` is preferred.
    """


# ---------------------
# Final Settings
# ---------------------

@dataclass
class AutopilotBehavior(AgentConfig):
    """
    These are settings from the autopilot carla.TrafficManager which are not exposed or not used by the original carla agents.
    NOTE: That default values do not exist for most settings; we should set it to something reasonable.
    """

    auto_lane_change: bool = True
    """Turns on or off lane changing behavior for a vehicle."""
    
    vehicle_lane_offset : float = 0
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
    Sets the difference the vehicle's intended speed and its current speed limit. 
    Speed limits can be exceeded by setting the percentage to a negative value. 
    Exceeding a speed limit can be done using negative percentages.
    
    NOTE: unit is in percent.
    Default is 30. 
    """
    
    ignore_lights_percentage : float = 0.0
    ignore_signs_percentage : float = 0.0
    ignore_walkers_percentage : float = 0.0

    update_vehicle_lights : bool = False
    """Sets if the Traffic Manager is responsible of updating the vehicle lights, or not."""
 
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
    avoid_tailgators : bool = True


@dataclass
class LunaticAgentSettings(AgentConfig):
    overwrites : Optional[Dict[str, dict]] = field(default_factory=dict, repr=False)
    live_info : LiveInfo = field(default_factory=LiveInfo, init=False)
    """<take doc:LiveInfo>"""
    speed : LunaticAgentSpeedSettings = field(default_factory=LunaticAgentSpeedSettings, init=False)
    """<take doc:LunaticAgentSpeedSettings>"""
    distance : LunaticAgentDistanceSettings = field(default_factory=LunaticAgentDistanceSettings, init=False)
    """<take doc:LunaticAgentDistanceSettings>"""
    lane_change : LunaticAgentLaneChangeSettings = field(default_factory=LunaticAgentLaneChangeSettings, init=False)
    """<take doc:LunaticAgentLaneChangeSettings>"""
    obstacles : LunaticAgentObstacleSettings = field(default_factory=LunaticAgentObstacleSettings, init=False)
    """<take doc:LunaticAgentObstacleSettings>"""
    controls : LunaticAgentControllerSettings = field(default_factory=LunaticAgentControllerSettings, init=False)
    """<take doc:LunaticAgentControllerSettings>"""
    planner : LunaticAgentPlannerSettings = field(default_factory=LunaticAgentPlannerSettings, init=False)
    """<take doc:LunaticAgentPlannerSettings>"""
    emergency : LunaticAgentEmergencySettings = field(default_factory=LunaticAgentEmergencySettings, init=False)
    """<take doc:LunaticAgentEmergencySettings>"""
    rss : RssSettings = field(default_factory=RssSettings, init=False)
    """<take doc:RssSettings>"""
    data_matrix : DataMatrixSettings = field(default_factory=DataMatrixSettings, init=False)
    """<take doc:DataMatrixSettings>"""

@dataclass
class SimpleBasicAgentSettings(SimpleConfig, LiveInfo, BasicAgentSpeedSettings, BasicAgentDistanceSettings, BasicAgentLaneChangeSettings, BasicAgentObstacleSettings, BasicAgentControllerSettings, BasicAgentPlannerSettings, BasicAgentEmergencySettings):
    _base_settings :ClassVar[BasicAgentSettings] = BasicAgentSettings

@dataclass
class SimpleBehaviorAgentSettings(SimpleConfig, LiveInfo, BehaviorAgentSpeedSettings, BehaviorAgentDistanceSettings, BehaviorAgentLaneChangeSettings, BehaviorAgentObstacleSettings, BehaviorAgentControllerSettings, BehaviorAgentPlannerSettings, BehaviorAgentEmergencySettings):
    _base_settings :ClassVar[BehaviorAgentSettings] = BehaviorAgentSettings


@dataclass
class SimpleLunaticAgentSettings(SimpleConfig, LiveInfo, LunaticAgentSpeedSettings, LunaticAgentDistanceSettings, LunaticAgentLaneChangeSettings, LunaticAgentObstacleSettings, LunaticAgentControllerSettings, LunaticAgentPlannerSettings, LunaticAgentEmergencySettings, RssSettings):
    _base_settings :ClassVar[BehaviorAgentSettings] = LunaticAgentSettings

@dataclass
class SimpleAutopilotAgentSettings(SimpleConfig, AutopilotSpeedSettings, AutopilotDistanceSettings, AutopilotLaneChangeSettings, AutopilotObstacleSettings, AutopilotControllerSettings):
    base_settings :ClassVar[AutopilotBehavior] = AutopilotBehavior

# ---------------------

@dataclass
class CameraConfig(AgentConfig):
    """Camera Settings"""
    
    width: int = 1280
    height: int = 720
    gamma: float = 2.2
    """Gamma correction of the camera"""
    
    if TYPE_CHECKING:
        camera_blueprints : List["CameraBlueprint"] = field(default_factory=lambda: [CameraBlueprint("sensor.camera.rgb", carla.ColorConverter.Raw, "RGB camera")])
    else:
        # In structured mode named tuples and carla Types are problematic
        camera_blueprints : list = field(default_factory=lambda: [CameraBlueprint("sensor.camera.rgb", carla.ColorConverter.Raw, "RGB camera")])
    
    hud : dict = "???"
    
    @dataclass
    class RecorderSettings:
        """
        Recorder settings for the camera.
        """
        
        enabled : bool = MISSING
        """
        Whether the recorder is enabled
        
        Set at WorldModel level
        """
        
        output_path : str = '_recorder/session%03d/%08d.bmp'
        """
        Folder to record the camera
        
        Needs two numeric conversion placeholders.
        """
        
        frame_interval : int = 1
        """Interval to record the camera"""
        
    recorder : RecorderSettings = field(default_factory=RecorderSettings)
    """<take doc:RecorderSettings>"""
    
    @dataclass
    class DataMatrixHudConfig:
        """
        Camera configuration for the agent.
        """
        enabled : bool = True
        """Whether the camera is enabled"""
        
        draw : bool = True
        """Whether to draw the camera"""
        
        values : bool = True
        """Whether to draw the values"""
        
        vertical : bool = True
        """Whether to draw the values vertically"""
        
        imshow_settings : dict = field(default_factory=lambda: {'cmap': 'jet'})
        """Settings for the imshow function"""
        
        text_settings : dict = field(default_factory=lambda: {'color': 'orange'})
        """Settings for the text"""

    data_matrix : DataMatrixHudConfig = field(default_factory=DataMatrixHudConfig)
    """<take doc:DataMatrixHudConfig>"""
        
    data_matrix : DataMatrixHudConfig = field(default_factory=DataMatrixHudConfig)
    


@dataclass
class LaunchConfig:
    verbose: bool = True
    debug: bool = True
    interactive: bool = False
    """
    If True will create an interactive session with command line input
    - NOTE: Needs custom code in the main file (Not implemented)
    """
    seed: Optional[int] = None

    # carla_service:
    map: str = "Town04"
    host: str = "127.0.0.1"
    port: int = 2000
    
    fps: int = 20
    sync: Union[bool, None] = True
    """
    If True, the simulation will be set to run in synchronous mode.
    For False, the simulation will be set to run in asynchronous mode.
    If None the world settings for synchronous mode will not be adjusted, 
    assuming this is handled by the user / external system.
    """
    
    handle_ticks: bool = True
    """
    Decide if the GameFramework & WoldModel are allowed to call carla.World.tick()
    or if `False` the ticks should be handled by an outside system.
    """

    loop: bool = True
    """
    If True the agent will look for a new waypoint after the initial route is done.
    - NOTE: Needs custom implementation in the main file.
    """

    # camera:
    width: int = 1280
    height: int = 720
    gamma: float = 2.2
    """
    Gamma correction of the camera.
    Depending on the weather and map this might need to be adjusted.
    """

    # Actor
    externalActor: bool = True
    """
    If False will spawn a vehicle for the agent to control, using the `filter` and `generation` settings.
    Otherwise will not spawn a vehicle but will wait until an actor with the name defined in `rolename` (default: "hero") is found.
    
    This vehicle needs to be spawned by another process, e.g. through the scenario runner.
    """
    rolename: str = "hero"
    """Actor name to wait for if `externalActor` is True."""
    filter: str = "vehicle.*"
    generation: int = 2
    
    autopilot: bool = False
    """
    Whether or not to use the Carla's TraficManager to autpilot  the agent
    - NOTE: This disables the usage of the LunaticAgent
    """
    
    agent : LunaticAgentSettings = MISSING
    """The Settings of the agent"""
    
    camera : CameraConfig = field(default_factory=CameraConfig)
    """The camera settings"""
    


def extract_annotations(parent, docs):
    for main_body in parent.body:
        # Skip non-classes
        if not isinstance(main_body, ast.ClassDef):
            continue
        if main_body.name in ("AgentConfig", "SimpleConfig", "class_or_instance_method"):
            continue
        docs[main_body.name] = {}
        for base in reversed(main_body.bases):
            # Fill in parent information
            docs[main_body.name].update(docs.get(base.id, {}))
        for i, body in enumerate(main_body.body):
            if isinstance(body, ast.ClassDef):
                # Nested classes, extract recursive
                extract_annotations(ast.Module([body]), docs[main_body.name])
                continue
            elif isinstance(body, ast.AnnAssign):
                target = body.target.id
                continue
            elif isinstance(body, ast.Assign):
                target = body.targets[0].id
                continue
            elif isinstance(body, ast.Expr):
                if i == 0: # Docstring of class
                    target = "__doc__"
                try:
                    doc: str = body.value.value # NOTE: This is different for <Python3.8; this is ast.Str
                except AttributeError:
                    # Try < 3.8 code
                    doc = body.value.s
                assert isinstance(doc, str)
            else:
                continue
            
            if doc.startswith("<take doc:") and doc.endswith(">"):
                key = doc[len("<take doc:"):-1]
                try:
                    docs[main_body.name][target] = docs[main_body.name][key]
                except KeyError as e:
                    try:
                        # Do global look up
                        docs[main_body.name][target] = _class_annotations[key]
                        continue
                    except:
                        pass
                    raise NameError(f"{key} needs to be defined before {target} or globally") from e
                continue
            docs[main_body.name][target] = inspect.cleandoc(doc)
            del target # delete to get better errors
            del doc


if __name__ == "__main__":

    if _class_annotations is None:
        _class_annotations = {}
    
    with open(__file__, "r") as f:
        tree = ast.parse(f.read())
    extract_annotations(tree, _class_annotations)
    print(_class_annotations)
        
    with open("conf/config_extensions/live_info.yaml", "w") as f:
        f.write(LiveInfo.to_yaml())
    
#  Using OmegaConf.set_struct, it is possible to prevent the creation of fields that do not exist:
LunaticAgentSettings.export_options("conf/lunatic_agent_settings.yaml", with_comments=True)

if __name__ == "__main__":
    #basic_agent_settings = OmegaConf.structured(BasicAgentSettings)
    #behavior_agent_settings = OmegaConf.structured(BehaviorAgentSettings)
    lunatic_agent_settings = OmegaConf.structured(LunaticAgentSettings, flags={"allow_objects": True})
    
    c : LunaticAgentSettings = LunaticAgentSettings().make_config()
    d : LunaticAgentSettings = LunaticAgentSettings.make_config()
    try:
        c.rss.log_level = "asda"
        raise TypeError("Should only raise if AD_RSS_AVAILABLE is False")
    except ValueError as e:
        print("Correct ValueError", e)
        pass
