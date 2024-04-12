
from agents.rules.behaviour_templates import SetNextWaypointNearby, SlowDownAtIntersectionRule, NormalSpeedRule, ConfigBasedRSSUpdates, DEBUG_RULES
from agents.rules.lane_changes import *

def create_default_rules():

    random_lane_change_rule = RandomLaneChangeRule()
    avoid_tailgator_rule = AvoidTailgatorRule()
    #simple_overtake_rule = SimpleOvertakeRule()
    
    set_close_waypoint_when_done = SetNextWaypointNearby()
    normal_intersection_speed_rule = SlowDownAtIntersectionRule()
    normal_speed_rule = NormalSpeedRule()
    config_based_rss_updates = ConfigBasedRSSUpdates()

    default_rules = [normal_intersection_speed_rule, normal_speed_rule, avoid_tailgator_rule, set_close_waypoint_when_done, config_based_rss_updates, random_lane_change_rule]
    if DEBUG_RULES:
        from agents.rules.behaviour_templates import SimpleRule1, SimpleRule1B, simple_ruleB, new_rule, another_rule, simple_rule, custom_rule
        default_rules.extend([SimpleRule1, SimpleRule1B, simple_ruleB, new_rule, another_rule, simple_rule,  custom_rule])
    return default_rules