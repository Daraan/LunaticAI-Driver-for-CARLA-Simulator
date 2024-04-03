from functools import partial
import random

from omegaconf._impl import select_node

import carla
import numpy as np
from agents.navigation.local_planner import RoadOption

from classes.constants import Phase
from classes.rule import Rule, EvaluationFunction, TruthyEvaluationFunction, Context, RulePriority, always_execute
from agents.tools.lunatic_agent_tools import detect_vehicles
from agents.tools.misc import ObstacleDetectionResult, get_speed
from agents.tools.logging import logger

from typing import TYPE_CHECKING, List

from classes.rule import always_execute
if TYPE_CHECKING:
    from agents import LunaticAgent

DEBUG_RULES = False

#TODO: maybe create some omega conf dict creator that allows to create settings more easily
# e.g. CreateOverwriteDict.speed.max_speed = 60, yields such a subdict.
# QUESTION: How to merge more than one entry?

# ------ Rule Helpers ------

def _if_config_checker(ctx : "Context", config_path : str, value) -> bool:
    """
    Check if a value in the config is set to a certain value.
    """
    return select_node(ctx.config, config_path, absolute_key=True) == value

def if_config(config_path, value):
    """
    Returns a partial function that checks if a value in the config is set to a certain value.
    """
    return EvaluationFunction(partial(_if_config_checker, config_path=config_path, value=value), name=f"Checks if {config_path} is {value}")

# ---

# Make random based on probabilistic config
 

# ------ Speed Rules ------

def set_default_intersection_speed(ctx : "Context"):
    """
    Slow down the car when turning at a junction.
    """
    target_speed = min([
            ctx.config.speed.max_speed,
            ctx.config.live_info.current_speed_limit - ctx.config.speed.intersection_speed_decrease]
            ) 
    # NOTE: could interpolate this in omega conf
    ctx.agent.config.speed.target_speed = target_speed
    
normal_intersection_speed_rule = Rule(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, 
                                      rule=always_execute, 
                                      action=set_default_intersection_speed, 
                                      overwrite_settings= {"speed": {"intersection_speed_decrease": 10}},
                                      description="Set speed to intersection speed")

# -----

def set_default_speed(ctx : "Context"):
    """
    Speed to apply when the car drives under normal circumstances, 
    i.e. no junctions, no obstacles, etc. detected.
    """
    # Read from config
    target_speed = min([
            ctx.config.speed.max_speed,
            ctx.config.live_info.current_speed_limit - ctx.config.speed.speed_lim_dist])
    # Set on Agent
    ctx.agent.config.speed.target_speed = target_speed

normal_speed_rule = Rule(Phase.TAKE_NORMAL_STEP | Phase.BEGIN,
                        rule=always_execute,
                        action=set_default_speed,
                        description="Set speed to normal speed")

# ----------- Avoid Beeing tailgated -----------


@TruthyEvaluationFunction
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

@avoid_tailgator_check.register_action(True)
def make_lane_change(ctx : "Context"):
    """
    If a tailgator is detected, move to the left/right lane if possible

        :param waypoint: current waypoint of the agent
        :param vehicle_list: list of all the nearby vehicles
        
    Assumes:
         (ctx.agent.config.live_info.incoming_direction == RoadOption.LANEFOLLOW \
            and not waypoint.is_junction and ctx.agent.config.live_info.current_speed > 10)
        check_behind.obstacle_was_found and ctx.agent.config.live_info.current_speed < get_speed(check_behind.obstacle)
    """
    vehicle_list = ctx.agent.vehicles_nearby
    waypoint = ctx.agent._current_waypoint # todo use a getter

    # There is a faster car behind us

    left_turn = waypoint.left_lane_marking.lane_change
    right_turn = waypoint.right_lane_marking.lane_change

    left_wpt = waypoint.get_left_lane()
    right_wpt = waypoint.get_right_lane()

    if (right_turn == carla.LaneChange.Right or right_turn ==
        carla.LaneChange.Both) and waypoint.lane_id * right_wpt.lane_id > 0 and right_wpt.lane_type == carla.LaneType.Driving:
        
        # Detect if right lane is free
        detection_result = detect_vehicles(ctx.agent, vehicle_list, max(
            ctx.agent.config.distance.min_proximity_threshold, ctx.agent.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=1)
        if not detection_result.obstacle_was_found:
            print("Tailgating, moving to the right!")
            end_waypoint = ctx.agent._local_planner.target_waypoint
            ctx.agent.set_destination(end_waypoint.transform.location,
                                    right_wpt.transform.location)
    
    elif left_turn == carla.LaneChange.Left and waypoint.lane_id * left_wpt.lane_id > 0 and left_wpt.lane_type == carla.LaneType.Driving:
        # Check if left lane is free
        detection_result = detect_vehicles(ctx.agent, vehicle_list, max(
            ctx.agent.config.distance.min_proximity_threshold, ctx.agent.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=-1)
        if  not detection_result.obstacle_was_found:
            print("Tailgating, moving to the left!")
            end_waypoint = ctx.agent._local_planner.target_waypoint
            ctx.agent.set_destination(end_waypoint.transform.location,
                                    left_wpt.transform.location)



class AvoidTailgatorRule(Rule):
    phase = Phase.DETECT_CARS | Phase.END
    rule = avoid_tailgator_check
    action = make_lane_change # NOTE: when using register_action you can omit this.
    cooldown_reset_value = 200
    group = "lane_change"
    priority = RulePriority.HIGH
    description = "Avoid tailgating when followed by a faster car that is quite close."
    _check_result: ObstacleDetectionResult = None

avoid_tailgator_rule = AvoidTailgatorRule()
#avoid_tailgator_rule = Rule(Phase.DETECT_CARS | Phase.END,
#                            rule=avoid_tailgator_check,
#                            action=avoid_tailgator,
#                            cooldown_reset_value=200,
#                            group="lane_change",
#                            priority=RulePriority.HIGH,
#                            description="Avoid tailgating when followed by a faster car that is quite close.")


# ----------- Plan next waypoint -----------

def set_random_waypoint(ctx : "Context", waypoints : List[carla.Waypoint]=None):
    """
    Set a random waypoint as the next target.
    """
    print("The target has been reached, searching for another target")
    ctx.agent._world_model.hud.notification("Target reached", seconds=4.0)
    if waypoints is None:
        waypoints = ctx.agent._map.get_spawn_points()
    ctx.agent.set_destination(random.choice(waypoints))
    
@EvaluationFunction
def is_agent_done(ctx : Context) -> bool:
    """
    Agent has reached its destination.
    """
    return ctx.agent.done()

set_random_waypoint_when_done = Rule(Phase.DONE | Phase.BEGIN,
                                     rule=is_agent_done,
                                     action=set_random_waypoint,
                                     description="Sets random waypoint when done")

def set_next_waypoint_nearby(ctx : "Context"):
    ctx.agent._world_model.hud.notification("Target reached", seconds=4.0)
    wp = ctx.agent._current_waypoint.next(150)[-1]
    next_wp = random.choice((wp, wp.get_left_lane(), wp.get_right_lane()))
    if next_wp is None:
        next_wp = wp
    #destination = random.choice(spawn_points).location
    destination = next_wp.transform.location
    ctx.agent.set_destination(destination)
    
set_close_waypoint_when_done = Rule(Phase.DONE | Phase.BEGIN,
                                     rule=is_agent_done,
                                     action=set_next_waypoint_nearby,
                                     description="Sets random waypoint when done to a nearby point ahead")
    
# ----------- Lane Change Rules -----------

class RandomLaneChangeRule(Rule):
    phases = Phase.TAKE_NORMAL_STEP | Phase.BEGIN
    rule = always_execute # TODO: Could implement check here, instead of relying on `lane_change`
    cooldown_reset_value = None
    
    priority = RulePriority.LOWEST
    group = "lane_change"
    description = "Randomly change lane"
    start_cooldown = 25
    
    def action(self, ctx: "Context"):
        """
        Change lane to the left or right.
        """
        print("Changing Lane randomly")
        p_left = ctx.config.lane_change.random_left_lanechange_percentage
        p_right = ctx.config.lane_change.random_right_lanechange_percentage
        p_stay = max(0, 1 - p_left - p_right) # weight to stay in the same lane
        direction : carla.LaneChange = carla.LaneChange(np.random.choice( (1, 0, 2), p=(p_left, p_stay, p_right)))
        print("Direction: ", direction)
        if direction == 0:
            self.reset_cooldown(ctx.config.lane_change.random_lane_change_interval)
            return
        ctx.agent.lane_change("left" if direction == 1 else "right", 
                            same_lane_time=ctx.config.lane_change.same_lane_time,
                            other_lane_time=ctx.config.lane_change.other_lane_time,
                            lane_change_time=ctx.config.lane_change.lane_change_time)
        
        print("Resetting cooldown")
        self.reset_cooldown(ctx.config.lane_change.random_lane_change_interval)

random_lane_change_rule = RandomLaneChangeRule()


# TODO: Create a stay right rule!    


# ----------- RSS Rules -----------

def accept_rss_updates(ctx : Context):
    """
    Accept RSS updates from the RSS manager.
    """
    if ctx.prior_result is None:
        return None
    assert isinstance(ctx.prior_result, carla.VehicleControl)
    logger.debug("Accepting RSS updates %s", ctx)
    ctx.control = ctx.prior_result

always_accept_rss_updates = Rule(Phase.RSS_EVALUATION | Phase.END,
                                     rule=always_execute,
                                     action=accept_rss_updates,
                                     description="Sets random waypoint when done")

config_based_rss_updates = Rule(Phase.RSS_EVALUATION | Phase.END,
                                rule=if_config("rss.enabled", True),
                                action=accept_rss_updates,
                                description="Sets random waypoint when done")

config_based_rss_updates = Rule(Phase.RSS_EVALUATION | Phase.END,
                                rule=if_config("rss.always_accept_update", True),
                                action=accept_rss_updates,
                                description="Sets random waypoint when done")



default_rules = [normal_intersection_speed_rule, normal_speed_rule, avoid_tailgator_rule, set_close_waypoint_when_done, config_based_rss_updates, random_lane_change_rule]


if __name__ == "__main__" or DEBUG_RULES:
    def context_method(self, ctx : "Context") -> bool:
        return True

    def context_function(ctx : "Context") -> bool:
        return True
    
    @EvaluationFunction
    def eval_context_method(self, ctx : "Context") -> bool:
        return True

    @EvaluationFunction
    def eval_context_function(ctx : "Context") -> bool:
        return True

    @Rule
    class SimpleRule1:
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        rule = context_function
        action = lambda ctx: print("ONLY CTX", ctx)
    
    class SimpleRule(Rule):
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        rule = context_method
        action = lambda self, ctx: print("NO AND CTX", self, "with context", ctx)

    class ReverseWhenCollide(Rule):
        phases = Phase.COLLISION | Phase.END
        rule = context_method
        def action(ctx : Context): 
            ctx.control.reverse = True
    
    @Rule
    class SimpleRule1B:
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        rule = eval_context_function
        action = lambda ctx: print("ONLY CTX", ctx)
    
    class SimpleRuleB(Rule):
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        rule = eval_context_method
        action = lambda self, ctx: print("NO AND CTX", self, "with context", ctx)


    class DebugRuleWithEval(Rule):
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        
        @EvaluationFunction("AlwaysTrue")
        def rule(self, ctx : "Context") -> bool:
            print("Called rule", "self:", type(self), "ctx:", ctx)
            return True
        
        @rule.register_action(True)
        def true_action(self, ctx : "Context"):
            print("Executing NEW RULE action of", self)
            print("Context", ctx)
        
    class Another(Rule):
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        
        rule = always_execute
        
        actions = {True: lambda self, ctx: print("ANOTHER FROM DICT Executing action of", self, "with context", ctx),
                False: lambda ctx: print("ANOTHER False function.", ctx)}

    new_rule = DebugRuleWithEval()
    #new_rule.action
    simple_rule = SimpleRule()
    simple_ruleB = SimpleRuleB()
    another_rule = Another()

    default_rules.extend([SimpleRule1, SimpleRule1B, simple_ruleB, new_rule, another_rule, simple_rule])