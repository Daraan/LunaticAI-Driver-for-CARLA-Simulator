"""Contains the base settings of CARLA's BasicAgent and LocalPlanner."""
# helper class, similar to @ property but which works on classes directly

from omegaconf import OmegaConf, DictConfig
from dataclasses import dataclass, field

from typing import Dict, TYPE_CHECKING

import conf.settings_base_class
from conf.settings_base_class import BaseCategories, _AnnotationChecker
from conf.settings_base_class import live_info, speed, distance, lane_change, obstacles, vehicle_control_constraints, planner, other, unknown

if TYPE_CHECKING:
    from agents.navigation.local_planner import RoadOption

assert speed is conf.settings_base_class.speed

class BasicAgentSettings(BaseCategories): # _AnnotationChecker, 
    """
    Default values and parameters
    used by the default CARLA agents, local planner and PIDController (via planner)
    """

    # Used as step_distance in basic_agent's lane change: next_wps = plan[-1][0].next(step_distance)
    planner.sampling_resolution : int = 2.0
    """
    Distance between waypoints in `BasicAgent._generate_lane_change_path`
    and GlobalRoutePlanner to build the topology and path planning.
    
    Used with the Waypoint.next(sampling_radius)
    """
    
    planner.sampling_radius : float = 2.0
    """
    Distance between waypoints when planning a path in `local_planner._compute_next_waypoints`
    
    Used with Waypoint.next(sampling_radius)
    """

    # --------------------------
    # Live Information, updated from different sources, e.g. from vehicle current speed limit.
    
    live_info.current_speed : float = None
    live_info.current_speed_limit : float = None
    live_info.incoming_direction : "RoadOption" = None 

    # --------------------------
    # Agent Level
    # see _affected_by_traffic_light and _affected_by_vehicle in basic_agent.py
    # --------------------------
    # Agents is aware of the vehicles and traffic lights within its distance parameters
    # optionally can always ignore them.
    obstacles.ignore_vehicles : bool = False
    obstacles.ignore_traffic_lights : bool = False
    obstacles.ignore_stop_signs : bool = False  # NOTE: Not implemented by default agent
    obstacles.use_bbs_detection : bool = False  # Bounding BoxeS
    """ If true uses more sophisticated detection of obstacles."""


    # Distance to traffic lights or vehicles to check if they affect the vehicle
    obstacles.base_tlight_threshold : float = 5.0
    obstacles.base_vehicle_threshold : float = 5.0

    obstacles.detection_speed_ratio : float = 1.0  # Increases detection range based on speed
    # USAGE: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
    # USAGE: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed

    """
    obstacles.detection_angles = {} 
    # angles are [low_angle_th, up_angle_th]
    obstacles.detection_angles.walkers_lane_change = [0., 90.]
    obstacles.detection_angles.walkers_same_lane = [0., 60.]
    obstacles.detection_angles.cars_lane_change = [0., 180.]
    obstacles.detection_angles.cars_same_lane = [0., 30.]
    """

    # --------------------------
    # Planner Level
    # --------------------------
    speed.current_speed = "${live_info.current_speed}" # This is a reference to live_info.current_speed, which is updated by the agent
    speed.current_speed_limit = "${live_info.current_speed_limit}" # This is a reference to live_info.current_speed_limit, which is updated by the agent
    
    speed.target_speed : float = 20  # desired cruise speed in Km/h; overwritten by SpeedLimit if follow_speed_limit is True
    speed.follow_speed_limits : bool = False  # NOTE: SpeedLimit overwrites target_speed if True (local_planner.py)

    # TODO: Better understand these parameters, make some experiments,
    # COMMENT: I think this is the minimal distance to drive before targeting a new waypoint in the path
    distance.base_min_distance : float = 3.0
    distance.distance_ratio : float = 0.5  # increases distance based on speed
    # USAGE: min_distance = base_min_distance + distance_ratio * vehicle_speed # see local_planner.py run_step()

    # --------------------------
    # PIDController Level (called from planner)
    # --------------------------
    vehicle_control_constraints.max_brake : float = 0.5  # vehicle control how strong the brake is used, # NOTE: Also used in emergency stop
    vehicle_control_constraints.max_throttle : float = 0.75  # maximum throttle applied to the vehicle
    vehicle_control_constraints.max_steering : float = 0.8  # maximum steering applied to the vehicle
    vehicle_control_constraints.offset : float = 0  # distance between the route waypoints and the center of the lane

    planner.dt : float = 1.0 / 20.0  # time between simulation steps. # TODO: Should set from main script. Maybe set this to None
    
    # TODO: Understand these parameters
    """
    PID controller using the following semantics:
            K_P -- Proportional term
            K_D -- Differential term
            K_I -- Integral term
    offset: If different than zero, the vehicle will drive displaced from the center line.
    Positive values imply a right offset while negative ones mean a left one. 
    Numbers high enough to cause the vehicle to drive through other lanes might break the controller.
    """
    # values of the lateral PID controller
    planner.lateral_control_dict = {'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2, 'dt': "${..dt}"} # original values
    planner.args_lateral_dict = "${.lateral_control_dict}"

    # values of the longitudinal PID controller
    planner.longitudinal_control_dict = {'K_P': 1.0, 'K_I': 0.05, 'K_D': 0, 'dt': "${..dt}"} # Note: ${..dt} points to planner.dt, similar to a directory
    planner.args_longitudinal_dict = "${.longitudinal_control_dict}" # points to the variable above

    # --------------------------
    # Extras
    # --------------------------
    
    lane_change.same_lane_time : float = 0.0
    lane_change.other_lane_time : float = 0.0
    lane_change.lane_change_time : float = 2.0


    # ---------------------
    # End of settings
    # ---------------------

    # ---------------------
    # Aliases
    # ---------------------
    # NOTE: below are aliases for settings which are sometimes used in different contexts,
    # or because they are more intuitive.
    # ---------------------

    # Different names for access
    # TODO: replace these with <category>.alternative_name = "${category}.original_name"

    @property
    def args_longitudinal_dict(self) -> dict:
        return self.planner.longitudinal_control_dict

    @property
    def args_lateral_dict(self) -> dict:
        return self.planner.lateral_control_dict

    @property
    def traffic_light_threshold(self):
        return self.obstacles.base_tlight_threshold

    @property
    def speed_ratio(self):  #
        return self.obstacles.detection_speed_ratio

    @property
    def max_throt(self):
        return self.speed.max_throttle

    @property
    def max_steer(self):
        return self.controls.max_steering

    @property
    def step_distance(self):
        return self.planner.sampling_resolution # TODO:update
    

basic_options = BasicAgentSettings()
basic_options._options = basic_options._init_default_options(reinit=True).copy()
basic_options.export_options("conf/default_options/basic_agent_settings.yaml")    


class BehaviorAgentSettings(BasicAgentSettings):
    """
    Class to be used with BehaviorAgents
    """

    # Speed -------
    """The maximum speed in km/h your vehicle will be able to reach."""
    # deprecated max_speed = 40 use target_speed instead   # NOTE: Behavior agents are more flexible in their speed. 

    # The three situations they adjust their speed; # SEE: behavior_agent.car_following_manager
    #
    # Case A car in front and getting closer : slow down; slower than car in front
    #       Take minium from, speed decrease, speed limit adjustment and target_speed
    #       target_speed = min( other_vehicle_speed - self._behavior.speed_decrease, # <-- slow down BELOW the other car
    #                           self._behavior.max_speed # use target_speed instead
    #                           self._speed_limit - self._behavior.speed_lim_dist])
    # Case B car in front but safe distance : match speed
    #       target_speed = min([
    #                 max(self._min_speed, other_vehicle_speed),  # <- match speed
    #                 self._behavior.max_speed,
    #                 self._speed_limit - self._behavior.speed_lim_dist])
    # Case C front is clear
    #       target_speed = min([
    #                 self._behavior.max_speed,
    #                 self._speed_limit - self._behavior.speed_lim_dist])

    speed.max_speed : float = 50 # from normal behavior. This supersedes the target_speed when following the BehaviorAgent logic

    # CASE A
    """How quickly in km/h your vehicle will slow down when approaching a slower vehicle ahead."""
    speed.speed_decrease : float = 12  # other_vehicle_speed - self._behavior.speed_decrease
    speed.safety_time : float = 3      # Time in s before a collision at the same speed -> apply speed_decrease

    # CASE B
    speed.min_speed : float = 5        # TODO: Implement als variable, currently hard_coded

    # All Cases
    speed.speed_lim_dist : float = 6   # NOTE: negative values => car drives above speed limit

    # Collision Avoidance -----

    # Distance in which for vehicles are checked
    # max(min_proximity_threshold, self._speed_limit / (2 if LANE CHANGE else 3 ) )
    # TODO: The secondary speed limit is hardcoded, make adjustable and optional
    # automatic_proximity_threshold = {RoadOption.CHANGELANELEFT: 2, "same_lane" : 3, "right_lane" : 2}
    distance.min_proximity_threshold : float = 12 # range in which cars are detected. # NOTE: Speed limit overwrites

    distance.braking_distance : float = 6  # Emergency Stop Distance Trigger

    # Tailgate
    other.tailgate_counter : int = 0  # in world_ticks (e.g. 20p second), # todo: cannot get this to work

behavior_agent_options = BehaviorAgentSettings()
behavior_agent_options._options = behavior_agent_options._init_default_options(reinit=True).copy()
behavior_agent_options.export_options("conf/default_options/behavior_agent_settings.yaml")
conf.settings_base_class.default_options = None