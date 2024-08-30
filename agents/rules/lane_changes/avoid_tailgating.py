"""Rule that avoids a tailgator by changing lanes."""

from agents.rules.lane_changes.other_rules import rule_lane_change
from agents.tools.hints import ObstacleDetectionResult
from agents.tools.lunatic_agent_tools import detect_vehicles
from agents.tools.misc import get_speed
from classes.constants import Phase, RoadOption, RulePriority
from classes.rule import ConditionFunction, Context, Rule


@ConditionFunction(truthy=True)
def avoid_tailgator_check(self: "AvoidTailgatorRule", ctx : "Context") -> bool:
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
    # Detect if there is a car behind
    vehicle_list = ctx.agent.vehicles_nearby
    check_behind: ObstacleDetectionResult = detect_vehicles(ctx.agent, vehicle_list,
                                   ctx.max_detection_distance("tailgating"),
                                   up_angle_th=180, low_angle_th=160)

    # If there is a tailgator check if faster
    # TODO: or evaluation a bit faster
    if check_behind.obstacle_was_found and ctx.live_info.current_speed < get_speed(check_behind.obstacle):
        return check_behind
    return False

class AvoidTailgatorRule(Rule):
    phase = Phase.DETECT_CARS | Phase.END
    condition = avoid_tailgator_check.copy()
    condition.register_action(rule_lane_change, True, order=("right", "left"))
    #action = make_lane_change # NOTE: when using register_action you can omit this.
    cooldown_reset_value = 200
    group = "lane_change"
    priority = RulePriority.HIGH
    description = "Avoid tailgating when followed by a faster car that is quite close."
