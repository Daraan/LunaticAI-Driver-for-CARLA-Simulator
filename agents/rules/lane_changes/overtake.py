# Credits to https://github.com/carla-simulator/carla/commits?author=jackbart94
# https://github.com/carla-simulator/carla/commit/4bc53a7f6c71551b466b8abdb48f24c48b295efc

import carla

from typing import TYPE_CHECKING

from agents.navigation.local_planner import RoadOption
from agents.tools.lunatic_agent_tools import detect_vehicles
from agents.tools.misc import get_speed
from agents.tools.logging import logger
from classes.constants import Phase
from classes.evaluation_function import EvaluationFunction
from classes.rule import Rule, RulePriority

from agents.rules.lane_changes.misc import rule_lane_change

if TYPE_CHECKING:
    from classes.rule import Context
    
@EvaluationFunction(truthy=True)
def overtake_check(self: "SimpleOvertakeRule", ctx: "Context") -> bool:
    """
    Vehicle wants to stay in lane, is not at a junction, and has a minimum speed
    and did not avoided tailgating in the last 200 steps

    ASSUMES: No car in front/side (which is a hazard in itself) found in DETECT_CARS phase

    # TODO: add option in rule to receive the result of the DETECT_CARS phase

    Check if a lane change can happen is done in the action, combine two rules!
    """
    waypoint = ctx.agent._current_waypoint

    # Cheap to get, do we plan to continue in the same lane? We are not at a junction and have some minimum speed
    pre_conditions = (ctx.live_info.incoming_direction == RoadOption.LANEFOLLOW \
            and not waypoint.is_junction and ctx.live_info.current_speed > 10  #TODO Hardcoded
            )
    if not pre_conditions:
        return False
    # Detect if there is a car in front
    vehicle_list = ctx.agent.vehicles_nearby
    
    # TODO: Improve with data Matrix
    # Compared to tailgating we check not so far in front (speed limit / 3)
    check_front = detect_vehicles(ctx.agent, vehicle_list,
                                   ctx.max_detection_distance("overtaking"), # Trigger further ahead
                                   up_angle_th=30,
                                   lane_offset=0)

    # TODO: Check lane marking
    # TODO: Check speed limit
    # TODO: Have some min speed difference to overtake
    #  Make some config to ignore speed limit for overtake
    if check_front.obstacle_was_found and ctx.live_info.current_speed > get_speed(check_front.obstacle):
        return check_front
    return False
                
class SimpleOvertakeRule(Rule):
    group = "lane_changeX"
    phase = Phase.DETECT_CARS | Phase.BEGIN
    
    priority = RulePriority.LOW
    
    rule = overtake_check.copy()
    rule.register_action(rule_lane_change, True, order=("left", "right"), speed_limit_downscale=4) # less strict
    cooldown_reset_value = 200
