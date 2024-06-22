
from agents.rules.behaviour_templates import DEBUG_RULES, normal_intersection_speed_rule, normal_speed_rule, avoid_tailgator_rule, set_close_waypoint_when_done, config_based_rss_updates, random_lane_change_rule

from agents.rules.lane_changes import *


def create_default_rules():
    """
    NOTE: This not yet update version that does not allow for multiple calls.
    See the development branch if you need support of it.
    """

    default_rules = [normal_intersection_speed_rule, normal_speed_rule, avoid_tailgator_rule, set_close_waypoint_when_done, config_based_rss_updates, random_lane_change_rule]
    if DEBUG_RULES:
        from agents.rules.behaviour_templates import SimpleRule1, SimpleRule1B
        default_rules.extend([SimpleRule1, SimpleRule1B])
    return default_rules