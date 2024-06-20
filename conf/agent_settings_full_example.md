# Example of full Agent Settings

Note: This file is a documentation only, it describes the full merge of the different setting files in the *./agent* folder.

```yaml
# LunaticAgentSettings
overwrites: {}


# Keeps track of information that changes during the simulation.
live_info:

  # If enabled makes use of the scenario_runner CarlaDataProvider assuming 
  # that its information is up to date and complete, e.g. tracks all actors.
  #  
  # NOTE: Turning this off is not fully supported.
  use_srunner_data_provider: true
  # 3D Vector of the current velocity of the vehicle.
  velocity_vector: ???

  # Velocity of the vehicle in km/h.
  #  
  # Note if use_srunner_data_provider is True the z component is ignored.
  current_speed: ???
  current_transform: ???
  current_location: ???
  current_speed_limit: ???

  # Direction that was executed in the last step by the local planner
  #  
  # planner.target_road_option is the option last executed by the planner (constant)
  # incoming direction is the next *planned* direction subject to change (variable)
  executed_direction: ???
  # RoadOption that will used for the current step
  incoming_direction: ???
  # Waypoint that is planned to be targeted in this step.
  incoming_waypoint: ???
  # incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)
  is_taking_turn: ???
  # incoming_direction in (RoadOption.CHANGELANELEFT, RoadOption.CHANGELANERIGHT)
  is_changing_lane: ???

  # Traffic light that is closest to the next intersection.
  #  
  # Is `None` if the agent is at an intersection.
  #  
  # + NOTE: This might not be in the path or infront of the vehicle.
  next_traffic_light: ???
  # Distance to the assumed next traffic light.
  next_traffic_light_distance: ???
  # VehicleControls 
  last_applied_controls: ???


# The three situations they adjust their speed; # SEE: `behavior_agent.car_following_manager`
#  
# Case A car in front and getting closer : slow down; slower than car in front
#       Take minium from, speed decrease, speed limit adjustment and target_speed
#       `target_speed` = min( other_vehicle_speed - self._behavior.speed_decrease, # <-- slow down BELOW the other car
#                           self._behavior.max_speed # use target_speed instead
#                           self._speed_limit - self._behavior.speed_lim_dist])
# Case B car in front but safe distance : match speed
#       `target_speed` = min([
#                 max(self._min_speed, other_vehicle_speed),  # <- match speed
#                 self._behavior.max_speed,
#                 self._speed_limit - self._behavior.speed_lim_dist])
# Case C front is clear
#       `target_speed` = min([
#                 self._behavior.max_speed,
#                 self._speed_limit - self._behavior.speed_lim_dist])
speed:
  # This is a reference to live_info.current_speed, which is updated by the agent
  current_speed: ${live_info.current_speed}
  # This is a reference to live_info.current_speed_limit, which is updated by the agent
  current_speed_limit: ${live_info.current_speed_limit}
  # desired cruise speed in Km/h; overwritten by SpeedLimit if follow_speed_limit is True
  target_speed: 20.0
  # If the agent should follow the speed limit. *NOTE:* SpeedLimit overwrites target_speed if True (local_planner.py)
  follow_speed_limits: false

  # The maximum speed in km/h your vehicle will be able to reach.
  # From normal behavior. This supersedes the target_speed when following the BehaviorAgent logic.
  max_speed: 50.0
  # other_vehicle_speed
  speed_decrease: 10.0
  # Time in s before a collision at the same speed -> apply speed_decrease
  safety_time: 3.0
  # Implement als variable, currently hard_coded
  min_speed: 5.0

  # Difference to speed limit.
  # NOTE: For negative values the car drives above speed limit
  speed_lim_dist: 3.0
  # Reduction of the targeted_speed when approaching an intersection
  intersection_speed_decrease: 5.0

  # TODO: Port from traffic manager.
  #  
  # Sets the difference the vehicle's intended speed and its current speed limit. 
  # Speed limits can be exceeded by setting the perc to a negative value. 
  # Default is 30. 
  # Exceeding a speed limit can be done using negative percentages.
  vehicle_percentage_speed_difference: ???
  # Formula or value to calculate the target speed when approaching an intersection
  intersection_target_speed: ${min:${.max_speed}, ${subtract:${.current_speed_limit},
    ${.intersection_speed_decrease}}}


# Collision Avoidance
# -------------------
#  
# Distance in which for vehicles are checked.
#  
# Usage: max_distance = max(min_proximity_threshold, self._speed_limit / (2 if <LANE CHANGE> else 3 ) )
distance:
  # Range in which cars are detected. NOTE: Speed limit overwrites
  min_proximity_threshold: 10.0
  # Emergency Stop Distance Trigger
  emergency_braking_distance: 5.0

  # PORT from TrafficManager # TODO:
  #  
  # Sets the minimum distance in meters that a vehicle has to keep with the others. 
  # The distance is in meters and will affect the minimum moving distance. It is computed from front to back of the vehicle objects.
  distance_to_leading_vehicle: ???


# Lane Change -----
#  
# Adjust probability that in each timestep the actor will perform a left/right lane change, 
# dependent on lane change availability. 
lane_change:
  same_lane_time: 0.0
  other_lane_time: 0.0
  lane_change_time: 2.0
  # Turns on or off lane changing behavior for a vehicle.
  auto_lane_change: true

  # Adjust probability that in each timestep the actor will perform a left/right lane change, 
  # dependent on lane change availability.
  random_left_lanechange_percentage: 0.1

  # Adjust probability that in each timestep the actor will perform a left/right lane change, 
  # dependent on lane change availability.
  random_right_lanechange_percentage: 0.1

  # During the localization stage, this method sets a percent chance that vehicle will follow the keep right rule, 
  # and stay in the right lane.
  keep_right_rule_percentage: 0.7
  # Cooldown value for a lane change in the 'lane_change' group.
  random_lane_change_interval: 200


# --------------------------
# Agent Level
# see _affected_by_traffic_light and _affected_by_vehicle in basic_agent.py
# --------------------------
# Agents is aware of the vehicles and traffic lights within its distance parameters
# optionally can always ignore them.
obstacles:
  # Whether the agent should ignore vehicles
  ignore_vehicles: false
  # Whether the agent should ignore traffic lights
  ignore_traffic_lights: false

  # Whether the agent should ignore stop signs
  #  
  # NOTE: No usage implemented!
  ignore_stop_signs: false

  # True: Whether to use a general approach to detect vehicles invading other lanes due to the offset.
  #  
  # False: Simplified approach, using only the plan waypoints (similar to TM)
  #  
  # See `BasicAgent._vehicle_obstacle_detected`
  use_bbs_detection: false

  # Base distance to traffic lights to check if they affect the vehicle
  #     
  # Usage: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
  # Usage: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed
  base_tlight_threshold: 5.0

  # Base distance to vehicles to check if they affect the vehicle
  #         
  # Usage: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
  # Usage: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed
  base_vehicle_threshold: 5.0

  # Increases detection range based on speed
  #  
  # Usage: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
  # Usage: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed
  detection_speed_ratio: 1.0

  # Whether to add a dynamic threshold based on the vehicle speed to the base threshold.
  #  
  # Usage: base_threshold + detection_speed_ratio * vehicle_speed
  #  
  # #NOTE: Currently only applied to traffic lights
  dynamic_threshold: true
  # Defines detection angles used when checking for obstacles.
  detection_angles:
    walkers_lane_change:
    - 0.0
    - 90.0
    walkers_same_lane:
    - 0.0
    - 60.0
    cars_lane_change:
    - 0.0
    - 180.0
    cars_same_lane:
    - 0.0
    - 30.0
    walkers_angle_adjust_chance: 0.0
    walkers_adjust_angle:
    - 20.0
    - -20.0
    cars_angle_adjust_chance: 0.0
    cars_adjust_angle:
    - 20.0
    - -50.0
  # For performance filters out vehicles that are further away than this distance in meters
  nearby_vehicles_max_distance: 45.0
  # For performance filters out pedestrians that are further away than this distance in meters
  nearby_walkers_max_distance: 10.0
  # Percentage of time to ignore traffic lights
  ignore_lights_percentage: 0.0
  # Percentage of time to ignore stop signs
  ignore_signs_percentage: 0.0
  # Percentage of time to ignore pedestrians
  ignore_walkers_percentage: 0.0


# Limitations of the controls used one the PIDController Level
controls:

  # Vehicle control how strong the brake is used, 
  #  
  # NOTE: Also used in emergency stop
  max_brake: 0.5
  # maximum throttle applied to the vehicle
  max_throttle: 0.75
  # maximum steering applied to the vehicle
  max_steering: 0.8

  # Sets a lane offset displacement from the center line. Positive values imply a right offset while negative ones mean a left one.
  # Default is 0. Numbers high enough to cause the vehicle to drive through other lanes might break the controller.
  vehicle_lane_offset: 0.0


# PID controller using the following semantics:
#         K_P -- Proportional term
#         K_D -- Differential term
#         K_I -- Integral term
#         dt -- time differential in seconds
# offset: If different than zero, the vehicle will drive displaced from the center line.
# Positive values imply a right offset while negative ones mean a left one. 
# Numbers high enough to cause the vehicle to drive through other lanes might break the controller.
#  
# Notes:
# `sampling_resolution` is used by the global planner to build a graph of road segments, also to get a path of waypoints from A to B
#  
# `sampling_radius` is similar but only used only by the local_planner to compute the next waypoints forward. The distance of those is the sampling_radius.
planner:

  # time differential in seconds
  #  
  # NOTE: Should set from main script.
  dt: ???
  # values of the lateral PID controller
  lateral_control_dict:
    K_P: 1.95
    K_D: 0.2
    K_I: 0.05
    dt: ${${..dt}}
  # values of the longitudinal PID controller
  longitudinal_control_dict:
    K_P: 1.0
    K_D: 0.0
    K_I: 0.05
    dt: ${${..dt}}

  # If different than zero, the vehicle will drive displaced from the center line.
  #  
  # Positive values imply a right offset while negative ones mean a left one. Numbers high enough
  # to cause the vehicle to drive through other lanes might break the controller.
  offset: ${controls.vehicle_lane_offset}

  # Distance between waypoints when planning a path in `local_planner._compute_next_waypoints`
  #  
  # Used with Waypoint.next(sampling_radius)
  sampling_radius: 2.0

  # Distance between waypoints in `BasicAgent._generate_lane_change_path`
  # and GlobalRoutePlanner to build the topology and path planning.
  #  
  # Used with the Waypoint.next(sampling_radius)
  sampling_resolution: 4.5

  # Removes waypoints from the queue that are too close to the vehicle.
  #  
  # Usage: min_distance = min_distance_next_waypoint + next_waypoint_distance_ratio * vehicle_speed 
  min_distance_next_waypoint: 3.0
  # Increases the minimum distance to the next waypoint based on the vehicles speed.
  next_waypoint_distance_ratio: 0.5

emergency:
  throttle: 0.0
  max_emergency_brake: ${controls.max_brake}
  hand_brake: false
  # Percentage of time to ignore an emergency situation and proceed as normal
  ignore_percentage: 0.0
  # Chance to choose the opposite of hand_break
  hand_brake_modify_chance: 0.0
  # Whether to do random steering
  do_random_steering: false
  # Range of random steering that is applied
  random_steering_range:
  - -0.25
  - 0.25

rss:

  # Use the RSS sensor.
  #  
  # NOTE: Initializing with False and changing it to True is not supported.
  # If RSS is not available (no ad-rss library) this will be set to False.
  enabled: true
  use_stay_on_road_feature: 1
  log_level: 3
  # Sets the visualization mode that should be rendered on the screen.
  debug_visualization_mode: RouteOnly
  # Setting for the default rule to always accept RSS updates if they are valid
  always_accept_update: false
  # For fast vehicles RSS currently is unreliable, disables rss updates when the vehicle is faster than this.
  rss_max_speed: ???

data_matrix:
  # Use the DataMatrix
  enabled: true

  # When the world uses synchronous mode and sync is true, the data matrix will be updated every sync_interval ticks.
  # A low value will have a negative impact on the fps.
  # If the world uses asynchronous mode or sync is False the data matrix will be updated by a different thread.
  # This increases the fps but updates will be less frequent.
  sync: true
  # The interval in frames after which the data matrix should be updated. Sync must be true.
  sync_interval: 5

  # XXX
  #  
  # TODO: do not have this in Agent config but in
  # hud : ${camera.hud.data_matrix}
  #  #drawing_options -> see camera.yaml
  #  #NOTE: this interpolation might fail if the parent has been removed!
  #  
  # ---
  #     
  # Keyword arguments for `DataMatrix.render`
  # NOTE: The default_settings substitute this with an interpolation that might not work,
  # as it relies on the parent LaunchConfig that is currently removed.
  #  
  # `camera.hud.data_matrix` is preferred.
  hud:
    draw: true
    values: true
    vertical: true
    imshow_settings:
      cmap: jet
    text_settings:
      color: orange
```
