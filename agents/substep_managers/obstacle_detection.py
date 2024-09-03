


from typing import TYPE_CHECKING

from agents.tools.lunatic_agent_tools import detect_obstacles_in_path

if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent

# TODO: Unify distance and obstacle thresholds

def collision_detection_manager(self : "LunaticAgent"):
    """
    This module is in charge of warning in case of a collision
    with vehicles or static obstacles.

        :param location: current location of the agent
        :return vehicle_state: True if there is a vehicle nearby, False if not
        :return vehicle: nearby vehicle
        :return distance: distance to nearby vehicle

    # NOTE: Former collision_and_car_avoid_manager, which evaded car via the tailgating function
    now rule based.
    """

    vehicle_detection_result = detect_obstacles_in_path(self, self.vehicles_nearby)
    static_obstacle_detection_result = detect_obstacles_in_path(self, self.static_obstacles_nearby)
    
    return vehicle_detection_result, static_obstacle_detection_result
