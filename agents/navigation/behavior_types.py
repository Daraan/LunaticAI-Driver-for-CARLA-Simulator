# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

""" This module contains the different parameters sets for each behavior. """


class CarlaOriginalBehavior:
    pass


class Cautious(CarlaOriginalBehavior):
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


class Normal(CarlaOriginalBehavior):
    """Class for Normal agent."""
    max_speed = 50
    speed_lim_dist = 3
    speed_decrease = 10
    safety_time = 3
    min_proximity_threshold = 10
    braking_distance = 5
    tailgate_counter = 0


class Aggressive(CarlaOriginalBehavior):
    """Class for Aggressive agent."""
    max_speed = 70
    speed_lim_dist = 1
    speed_decrease = 8
    safety_time = 3
    min_proximity_threshold = 8
    braking_distance = 4
    tailgate_counter = -1


# Experiments (not really successful)

class Tailgating2(CarlaOriginalBehavior):
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


# Gather all classes in this file

behavior_types = dict(filter(lambda kv: not kv[0].startswith("_"), vars().items()))  # type: dict[str, CarlaOriginalBehavior]
