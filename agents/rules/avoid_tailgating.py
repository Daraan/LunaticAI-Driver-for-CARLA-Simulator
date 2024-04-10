# ----------- Avoid Beeing tailgated -----------

from agents.navigation.local_planner import RoadOption
from agents.rules.behaviour_templates import make_lane_change
from agents.tools.lunatic_agent_tools import detect_vehicles
from agents.tools.misc import ObstacleDetectionResult, get_speed
from classes.constants import Phase
from classes.rule import Context, EvaluationFunction, Rule, RulePriority


@EvaluationFunction(truthy=True)
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
    pre_conditions = (ctx.agent.config.live_info.incoming_direction == RoadOption.LANEFOLLOW \
            and not waypoint.is_junction and ctx.agent.config.live_info.current_speed > 10  #TODO Hardcoded
            )
    if not pre_conditions:
        return False
    # Detect if there is a car behind
    vehicle_list = ctx.agent.vehicles_nearby
    check_behind = detect_vehicles(ctx.agent, vehicle_list,
                                   max(ctx.agent.config.distance.min_proximity_threshold,
                                       ctx.agent.config.live_info.current_speed_limit / 2),
                                   up_angle_th=180, low_angle_th=160)

    # If there is a tailgator check if faster
    # TODO: or evaluation a bit faster
    if check_behind.obstacle_was_found and ctx.agent.config.live_info.current_speed < get_speed(check_behind.obstacle):
        return check_behind
    return False


class AvoidTailgatorRule(Rule):
    phase = Phase.DETECT_CARS | Phase.END
    rule = avoid_tailgator_check
    avoid_tailgator_check.register_action(make_lane_change, True)
    #action = make_lane_change # NOTE: when using register_action you can omit this.
    cooldown_reset_value = 200
    group = "lane_change"
    priority = RulePriority.HIGH
    description = "Avoid tailgating when followed by a faster car that is quite close."
    _check_result: ObstacleDetectionResult = None
    
#avoid_tailgator_rule = Rule(Phase.DETECT_CARS | Phase.END,
#                            rule=avoid_tailgator_check,
#                            action=avoid_tailgator,
#                            cooldown_reset_value=200,
#                            group="lane_change",
#                            priority=RulePriority.HIGH,
#                            description="Avoid tailgating when followed by a faster car that is quite close.")