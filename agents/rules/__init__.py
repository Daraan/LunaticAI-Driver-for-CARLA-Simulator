
from agents.rules.behaviour_templates import SetNextWaypointNearby, SlowDownAtIntersectionRule, NormalSpeedRule, ConfigBasedRSSUpdates, DEBUG_RULES
from agents.rules.lane_changes import *
from agents.rules.obstacles import *
from agents.rules.stopped_long_trigger import StoppedTooLongTrigger

from agents.tools.logging import logger

from typing import TYPE_CHECKING, Optional

from classes.rule import BlockingRule
if TYPE_CHECKING:
    from classes.worldmodel import GameFramework

def create_default_rules(gameframework: Optional["GameFramework"]=None):

    random_lane_change_rule = RandomLaneChangeRule()
    avoid_tailgator_rule = AvoidTailgatorRule()
    simple_overtake_rule = SimpleOvertakeRule()
    
    set_close_waypoint_when_done = SetNextWaypointNearby()
    normal_intersection_speed_rule = SlowDownAtIntersectionRule()
    normal_speed_rule = NormalSpeedRule()
    config_based_rss_updates = ConfigBasedRSSUpdates()
    
    slow_towards_traffic_light = DriveSlowTowardsTrafficLight(gameframework=gameframework)

    default_rules = [normal_intersection_speed_rule, normal_speed_rule, avoid_tailgator_rule, simple_overtake_rule, set_close_waypoint_when_done, config_based_rss_updates, random_lane_change_rule, slow_towards_traffic_light]
    if DEBUG_RULES:
        default_rules.append(StoppedTooLongTrigger())
        from agents.rules.behaviour_templates import SimpleRule1, SimpleRule1B, debug_rules
        default_rules.extend([SimpleRule1, SimpleRule1B])
        default_rules.extend(debug_rules)
    if not gameframework and any(isinstance(rule, BlockingRule) for rule in default_rules):
        logger.warning("A BlockingRule is in the default rules but no GameFramework instance is provided.")
        
    return default_rules
