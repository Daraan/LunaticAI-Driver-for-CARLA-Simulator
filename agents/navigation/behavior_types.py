# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

""" This module contains the different parameters sets for each behavior. """

class classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)

class BaseBehavior:
    target_speed = 20
    ignore_vehicles = False
    ignore_traffic_lights = False
    ignore_stop_signs = False
    use_bbs_detection = False # TODO: What is this?
    sampling_resolution = 2.0 # TODO: What is this? # BasicAgent uses 2.0 Behaviour ones 4.5 Sampling of waypoitns related
    base_tlight_threshold = 5.0
    base_vehicle_threshold = 5.0
    detection_speed_ratio = 1
    max_brake = 0.5 # vehicle control how strong the brake is used
    offset = 0  # TODO: What is this?

    # aliases for better understanding or because differently used by the agents
    @classproperty
    def traffic_light_threshold(cls): #
        return cls.base_tlight_threshold

    @classproperty
    def speed_ratio(cls):  #
        return cls.detection_speed_ratio

    @classproperty
    def options(cls):
        """Returns the dictionary used by the basic agents"""
        return {'target_speed'          : cls.target_speed,
                'ignore_traffic_lights' : cls.ignore_traffic_lights,
                'ignore_stop_signs'     : cls.ignore_stop_signs,
                'ignore_vehicles'       : cls.ignore_vehicles,
                'use_bbs_detection'     : cls.use_bbs_detection,
                'sampling_resolution'   : cls.sampling_resolution,
                'base_tlight_threshold' : cls.base_tlight_threshold,
                'base_vehicle_threshold' : cls.base_vehicle_threshold,
                'detection_speed_ratio' : cls.detection_speed_ratio,
                'max_brake' : cls.max_brake,
                'offset'    : cls.offset
            }



class Cautious(BaseBehavior):
    """Class for Cautious agent."""

    """The maximum speed in km/h your vehicle will be able to reach."""
    max_speed = 40
    speed_lim_dist = 6
    """How quickly in km/h your vehicle will slow down when approaching a slower vehicle ahead."""
    speed_decrease = 12
    safety_time = 3
    min_proximity_threshold = 12
    braking_distance = 6
    tailgate_counter = 0


class Normal(BaseBehavior):
    """Class for Normal agent."""
    max_speed = 50
    speed_lim_dist = 3
    speed_decrease = 10
    safety_time = 3
    min_proximity_threshold = 10
    braking_distance = 5
    tailgate_counter = 0


class Aggressive(BaseBehavior):
    """Class for Aggressive agent."""
    max_speed = 70
    speed_lim_dist = 1
    speed_decrease = 8
    safety_time = 3
    min_proximity_threshold = 8
    braking_distance = 4
    tailgate_counter = -1

class Tailgating2(BaseBehavior):
    """Class for Aggressive agent."""
    max_speed = 60
    speed_lim_dist = 1
    speed_decrease = 8
    safety_time = 0.5
    min_proximity_threshold = 1
    braking_distance = 0.5
    tailgate_counter = -1

class BadAndRisky(Aggressive):
    max_brake = 0.1
    base_vehicle_threshold = 0.25
    min_proximity_threshold = 0
    safety_time = 0.5
