from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple, Union
from omegaconf import DictConfig, MISSING, SI, II, OmegaConf

#import attr
import carla

# NOTE:
"""
II : Equivalent to ${interpolation}
SI Use this for String interpolation, for example "http://${host}:${port}"

:param interpolation:
:return: input ${node} with type Any

"""

from agents.navigation.local_planner import RoadOption


class Config:
    pass


@dataclass
class LiveInfo(Config):
    current_speed : float = MISSING
    current_speed_limit : float = MISSING
    direction : RoadOption = MISSING
    
# ---------------------
# Speed
# ---------------------    
    
    
@dataclass
class BasicAgentSpeedSettings(Config):
    current_speed: float = II("live_info.current_speed")
    """This is a reference to live_info.speed, which is updated by the agent"""
    
    current_speed_limit: float = II("live_info.current_speed_limit")
    """This is a reference to live_info.speed_limit, which is updated by the agent"""
    
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
class AutopilotSpeedSettings(Config):
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
class BasicAgentDistanceSettings(Config):
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
class AutopilotDistanceSettings(Config):
    distance_to_leading_vehicle : float = 5.0
    """
    Sets the minimum distance in meters that a vehicle has to keep with the others. 
    The distance is in meters and will affect the minimum moving distance. It is computed from front to back of the vehicle objects.
    """

@dataclass
class LunaticAgent_Distance(AutopilotDistanceSettings, BehaviorAgentDistanceSettings):
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
class BasicAgentLaneChangeSettings(Config):
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
class AutopilotLaneChangeSettings(Config):
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
class BasicAgentObstacleSettings(Config):
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

@dataclass
class BehaviorAgentObstacleSettings(BasicAgentObstacleSettings):
    pass

@dataclass
class AutopilotObstacleSettings(Config):
    ignore_lights_percentage : float = 0.0
    ignore_signs_percentage : float = 0.0
    ignore_walkers_percentage : float = 0.0
    """
    Percentage of time to ignore traffic lights, signs and pedestrians
    """
    
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
class BasicAgentControllerSettings(Config):
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
class AutopilotControllerSettings(Config):
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
class BasicAgentPlannerSettings(Config):
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
class BasicAgentEmergencySettings(Config):
    throttle = 0.0
    brake = II("controls.max_brake")
    hand_brake = False
    
    
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

@dataclass
class RSSSettings(Config):
    enabled : bool = True
    """
    Use the RSS sensor.
    
    NOTE: Initializing with False and changing it to True is not supported.
    If RSS is not available (no ad-rss library) this will be set to False.
    """
    
    use_stay_on_road_feature : carla.RssRoadBoundariesMode = carla.RssRoadBoundariesMode.On
    """Use the RssRoadBoundariesMode. NOTE: A call to `rss_set_road_boundaries_mode` is necessary"""
    
    log_level : carla.RssLogLevel = carla.RssLogLevel.info
    """Set the initial log level of the RSSSensor"""
    

# ---------------------

@dataclass
class AutopilotBehavior(Config):
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
    
from pprint import pprint
pprint(LunaticAgentObstacleSettings())

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
class SimpleLunaticAgentSettings(LiveInfo, LunaticAgentSpeedSettings, LunaticAgent_Distance, LunaticAgentLaneChangeSettings, LunaticAgentObstacleSettings, LunaticAgentControllerSettings, LunaticAgentPlannerSettings, LunaticAgentEmergencySettings, RSSSettings):
    pass


@dataclass
class BasicAgentSettings(Config):
    live_info : LiveInfo = field(default_factory=LiveInfo)
    speed : BasicAgentSpeedSettings = field(default_factory=BasicAgentSpeedSettings)
    distance : BasicAgentDistanceSettings = field(default_factory=BasicAgentDistanceSettings)
    lane_change : BasicAgentLaneChangeSettings = field(default_factory=BasicAgentLaneChangeSettings)
    obstacles : BasicAgentObstacleSettings = field(default_factory=BasicAgentObstacleSettings)
    controls : BasicAgentControllerSettings = field(default_factory=BasicAgentControllerSettings)
    planner : BasicAgentPlannerSettings = field(default_factory=BasicAgentPlannerSettings)
    emergency : BasicAgentEmergencySettings = field(default_factory=BasicAgentEmergencySettings)
    
@dataclass
class BehaviorAgentSettings(Config):
    speed : BehaviorAgentSpeedSettings = field(default_factory=BehaviorAgentSpeedSettings)
    distance : BehaviorAgentDistanceSettings = field(default_factory=BehaviorAgentDistanceSettings)
    lane_change : BehaviorAgentLaneChangeSettings = field(default_factory=BehaviorAgentLaneChangeSettings)
    obstacles : BehaviorAgentObstacleSettings = field(default_factory=BehaviorAgentObstacleSettings)
    controls : BehaviorAgentControllerSettings = field(default_factory=BehaviorAgentControllerSettings)
    planner : BehaviorAgentPlannerSettings = field(default_factory=BehaviorAgentPlannerSettings)
    emergency : BehaviorAgentEmergencySettings = field(default_factory=BehaviorAgentEmergencySettings)
    
@dataclass
class LunaticAgentSettings(Config):
    live_info : LiveInfo = field(default_factory=LiveInfo)
    speed : LunaticAgentSpeedSettings = field(default_factory=LunaticAgentSpeedSettings)
    distance : LunaticAgent_Distance = field(default_factory=LunaticAgent_Distance)
    lane_change : LunaticAgentLaneChangeSettings = field(default_factory=LunaticAgentLaneChangeSettings)
    obstacles : LunaticAgentObstacleSettings = field(default_factory=LunaticAgentObstacleSettings)
    controls : LunaticAgentControllerSettings = field(default_factory=LunaticAgentControllerSettings)
    planner : LunaticAgentPlannerSettings = field(default_factory=LunaticAgentPlannerSettings)
    emergency : LunaticAgentEmergencySettings = field(default_factory=LunaticAgentEmergencySettings)
    rss : RSSSettings = field(default_factory=RSSSettings)
    
    
basic_agent_settings = OmegaConf.structured(BasicAgentSettings)
behavior_agent_settings = OmegaConf.structured(BehaviorAgentSettings)
lunatic_agent_settings = OmegaConf.structured(LunaticAgentSettings, flags=dict(allow_objects=True))

#  Using OmegaConf.set_struct, it is possible to prevent the creation of fields that do not exist:

"""
class Test(Enum):
    a = 1
    b = 2
    c = "hmm"
"""