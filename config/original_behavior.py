"""Contains the base settings of CARLA's BasicAgent and LocalPlanner."""
# helper class, similar to @ property but which works on classes directly
class _classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)

# TODO: Using a a json/yaml file in the future
class BasicBehavior:
    """
    Default values and parameters
    used by the default CARLA agents, local planner and PIDController (via planner)
    """
    # TODO: Explain unclear parameters
    use_bbs_detection = False  # Bounding BoxeS # Likely more sophisticated detection of obstacles. # TODO understand better
    sampling_resolution = 2.0  # TODO: What is this? # BasicAgent uses 2.0 Behavior ones 4.5 Sampling of waypoints related
                                # Used as step_distance in basic_agent's lane change: next_wps = plan[-1][0].next(step_distance)
    sampling_radius = 2.0  # TODO: What is this? Used by local_planner.py

    # --------------------------
    # Agent Level
    # see _affected_by_traffic_light and _affected_by_vehicle in basic_agent.py
    # --------------------------
    # Agents is aware of the vehicles and traffic lights within its distance parameters
    # optionally can always ignore them.
    ignore_vehicles = False
    ignore_traffic_lights = False
    ignore_stop_signs = False  # NOTE: Not implemented by default agent

    # Distance to traffic lights or vehicles to check if they affect the vehicle
    base_tlight_threshold = 5.0
    base_vehicle_threshold = 5.0

    detection_speed_ratio = 1  # Increases detection range based on speed
    # USAGE: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
    # USAGE: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed

    # --------------------------
    # Planer Level
    # --------------------------
    target_speed = 20  # desired cruise speed in Km/h; overwritten by SpeedLimit if follow_speed_limit is True
    follow_speed_limit = False  # NOTE: SpeedLimit overwrites target_speed if True (local_planner.py)

    # TODO: Better understand these parameters, make some experiments,
    # COMMENT: I think this is the minimal distance to drive before targeting a new waypoint in the path
    base_min_distance = 3.0
    distance_ratio = 0.5  # increases distance based on speed
    # USAGE: min_distance = base_min_distance + distance_ratio * vehicle_speed # see local_planner.py run_step()

    # --------------------------
    # PIDController Level (called from planer)
    # --------------------------
    max_brake = 0.5  # vehicle control how strong the brake is used, # NOTE: Also used in emergency stop
    max_throttle = 0.75  # maximum throttle applied to the vehicle
    max_steering = 0.8  # maximum steering applied to the vehicle
    offset = 0  # distance between the route waypoints and the center of the lane

    dt = 1.0 / 20.0  # time between simulation steps. # TODO: Should set from main script. Maybe set this to None
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
    _lateral_control_dict = {'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2, 'dt': None}
    # values of the longitudinal PID controller
    _longitudinal_control_dict = {'K_P': 1.0, 'K_I': 0.05, 'K_D': 0, 'dt': None}

    # ---------------------
    # End of settings
    # ---------------------

    # aliases for better understanding or because differently used by the agents
    @_classproperty
    def lateral_control_dict(cls) -> dict:
        cls._lateral_control_dict["dt"] = cls.dt  # cannot set this at init
        return cls._lateral_control_dict

    @_classproperty
    def longitudinal_control_dict(cls) -> dict:
        cls._longitudinal_control_dict["dt"] = cls.dt
        return cls._longitudinal_control_dict

    @_classproperty
    def args_longitudinal_dict(cls) -> dict:
        return cls.longitudinal_control_dict

    @_classproperty
    def args_lateral_dict(cls) -> dict:
        return cls.lateral_control_dict

    @_classproperty
    def traffic_light_threshold(cls):
        return cls.base_tlight_threshold

    @_classproperty
    def speed_ratio(cls):  #
        return cls.detection_speed_ratio

    @_classproperty
    def max_throt(cls):
        return cls.max_throttle

    @_classproperty
    def max_steer(cls):
        return cls.max_steering

    @_classproperty
    def step_distance(cls):
        return cls.sampling_resolution

    @_classproperty
    def _deprecated_options(cls):  # TODO remove this
        """Returns the dictionary used by the basic agents & local planner"""
        # DONE: Make this automatic -> get_options() -> dict
        return {'target_speed': cls.target_speed,
                'ignore_traffic_lights': cls.ignore_traffic_lights,
                'ignore_stop_signs': cls.ignore_stop_signs,
                'ignore_vehicles': cls.ignore_vehicles,
                'use_bbs_detection': cls.use_bbs_detection,
                'sampling_resolution': cls.sampling_resolution,
                'base_tlight_threshold': cls.base_tlight_threshold,
                'base_vehicle_threshold': cls.base_vehicle_threshold,
                'detection_speed_ratio': cls.detection_speed_ratio,
                'max_brake': cls.max_brake,
                'max_throttle': cls.max_throttle,
                'max_steering': cls.max_steering,
                'offset': cls.offset,
                'dt': cls.dt,
                }

    @classmethod
    def _filter_options(cls, key, value):
        """Filters out private and callable attributes. Replaces classproperty with its value."""
        if key.startswith('_') or isinstance(value, classmethod) or isinstance(value, staticmethod) or callable(value):
            return None, None
        if isinstance(value, _classproperty):
            return key, value.f(cls)  # call the classproperty
        return key, value

    @classmethod
    def get_options(cls) -> dict:
        """
        Returns the all options as a dictionary.
        NOTE: Attribute access is cheaper, however dict can be created once and reused.
        """
        variables: dict = vars(cls)
        remapped = dict(map(cls._filter_options, variables.keys(), variables.values()))
        remapped.pop(None, None)  # remove filtered out values
        return remapped


class Behavior(BasicBehavior):
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

    # CASE A
    """How quickly in km/h your vehicle will slow down when approaching a slower vehicle ahead."""
    speed_decrease = 12  # other_vehicle_speed - self._behavior.speed_decrease
    safety_time = 3      # Time in s before a collision at the same speed -> apply speed_decrease

    # CASE B
    min_speed = 5        # TODO: Implement als variable, currently hard_coded

    # All Cases
    speed_lim_dist = 6   # NOTE: negative values => car drives above speed limit

    # Collision Avoidance -----

    # Distance in which for vehicles are checked
    # max(min_proximity_threshold, self._speed_limit / (2 if LANG CHANGE else 3 ) )
    # TODO: The secondary speed limit is hardcoded, make adjustable and optional
    # automatic_proximity_threshold = {RoadOption.CHANGELANELEFT: 2, "same_lane" : 3, "right_lane" : 2}
    min_proximity_threshold = 12 # range in which cars are detected. # NOTE: Speed limit overwrites

    braking_distance = 6  # Emergency Stop Distance Trigger

    # Tailgate
    tailgate_counter = 0  # in world_ticks (e.g. 20p second), # todo: cannot get this to work

    @_classproperty
    def max_speed(cls):
        return cls.target_speed
