"""Contains options which are not built-in to the original carla agents and are used by our agent classes."""

from config.default_options.original_behavior import BehaviorAgentSettings
from config.default_options.original_behavior import speed, distance, lane_change, planner, obstacles, other, unknown
import config.settings_base_class

class AutopilotBehavior(BehaviorAgentSettings):
    """
    These are settings from the autopilot carla.TrafficManager which are not exposed or not used by the original carla agents.
    NOTE: That default values do not exist for most settings; we should set it to something reasonable.
    """

    lane_change.auto_lange_change: bool = True  # Turns on or off lane changing behaviour for a vehicle. 
    
    # "Sets a lane offset displacement from the center line. Positive values imply a right offset while negative ones mean a left one. 
    # Default is 0. Numbers high enough to cause the vehicle to drive through other lanes might break the controller."
    other.vehicle_lane_offset : str = "${..planer.offset}"

    #Adjust probability that in each timestep the actor will perform a left/right lane change, 
    # dependent on lane change availability. 
    lane_change.random_left_lanechange_percentage: float = 0.1
    lane_change.random_right_lanechange_percentage : float = 0.1

    # "During the localization stage, this method sets a percent chance that vehicle will follow the keep right rule, 
    # and stay in the right lane.""
    lane_change.keep_right_rule_percentage: float = 0.7

    # Sets the minimum distance in meters that a vehicle has to keep with the others. 
    # The distance is in meters and will affect the minimum moving distance. It is computed from front to back of the vehicle objects. 
    distance.distance_to_leading_vehicle : float = 5.0

    # Sets the difference the vehicle's intended speed and its current speed limit. 
    # Speed limits can be exceeded by setting the perc to a negative value. 
    # Default is 30. Exceeding a speed limit can be done using negative percentages.
    speed.vehicle_percentage_speed_difference : float = 30 # in percent

    #
    obstacles.ignore_lights_percentage : float = 0.0
    obstacles.ignore_signs_percentage : float = 0.0
    obstacles.ignore_walkers_percentage : float = 0.0

    # "Sets if the Traffic Manager is responsible of updating the vehicle lights, or not."
    other.update_vehicle_lights : bool = False


carla_default_options = AutopilotBehavior()
carla_default_options._options = carla_default_options._init_default_options(reinit=True).copy()
carla_default_options.export_options("config/default_options/carla_default_options.yaml")
config.settings_base_class.default_options = None

