from functools import partial
import random

from omegaconf._impl import select_node

import carla

from launch_tools import CarlaDataProvider

from classes.constants import Phase
from classes.rule import Rule, EvaluationFunction, TruthyEvaluationFunction, Context, always_execute
from agents.tools.lunatic_agent_tools import detect_vehicles
from agents.tools.logging import logger

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from agents import LunaticAgent

DEBUG_RULES = True

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
    return EvaluationFunction(partial(_if_config_checker, config_path=config_path, value=value), 
                              name=f"Checks if {config_path} is {value}", 
                              use_self=False #NOTE: Has to be used as _if_config_checker has > 1 argument and no self usage.
                              )

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

class SlowDownAtIntersectionRule(Rule):
    """
    Slow down the car when turning at a junction.
    """
    phases = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    rule = always_execute
    action = set_default_intersection_speed
    overwrite_settings = {"speed": {"intersection_speed_decrease": 10}}
    description = "Set speed to intersection speed"

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

class NormalSpeedRule(Rule):
    """
    Speed to apply when the car drives under normal circumstances, 
    i.e. no junctions, no obstacles, etc. detected.
    """
    phases = Phase.TAKE_NORMAL_STEP | Phase.BEGIN
    rule = always_execute
    action = set_default_speed
    description = "Set speed to normal speed"

# ----

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




# ----------- Plan next waypoint -----------

def random_spawnpoint_destination(ctx: "Context", waypoints: List[carla.Waypoint]=None):
    """
    Set a random waypoint as the next target.
    """
    print("The target has been reached, searching for another target")
    ctx.agent._world_model.hud.notification("Target reached", seconds=4.0)
    if waypoints is None:
        waypoints = ctx.get_map().get_spawn_points()
    ctx.agent.set_destination(random.choice(waypoints))
    
@EvaluationFunction
def is_agent_done(ctx: Context) -> bool:
    """
    Agent has reached its destination.
    """
    return ctx.agent.done()

class TargetRandomSpawnpointWhenDone(Rule):
    """
    Sets random waypoint when done
    """
    phases = Phase.DONE | Phase.BEGIN
    rule = is_agent_done
    action = random_spawnpoint_destination
    description = "Sets random waypoint when done"

# ---

def set_next_waypoint_nearby(ctx : "Context"):
    ctx.agent._world_model.hud.notification("Target reached", seconds=4.0)
    wp = ctx.agent._current_waypoint.next(150)[-1]
    next_wp = random.choice((wp, wp.get_left_lane(), wp.get_right_lane()))
    if next_wp is None:
        next_wp = wp
    #destination = random.choice(spawn_points).location
    destination = next_wp.transform.location
    ctx.agent.set_destination(destination)
    
class SetNextWaypointNearby(Rule):
    "Sets random waypoint when done to a nearby point ahead" 
    phases = Phase.DONE | Phase.BEGIN
    rule = is_agent_done
    action = set_next_waypoint_nearby



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

class AlwaysAcceptRSSUpdates(Rule):
    phases = Phase.RSS_EVALUATION | Phase.END
    rule = always_execute
    action = accept_rss_updates
    description = "Always accepts the updates calculated by the RSS System."
    
assert isinstance(if_config("rss.enabled", True), EvaluationFunction)

class AlwaysAcceptRSSUpdates(AlwaysAcceptRSSUpdates):
    phases = Phase.RSS_EVALUATION | Phase.END
    rule=if_config("rss.enabled", True)
    action = accept_rss_updates
    description = "Always accepts the updates calculated by the RSS System."

class ConfigBasedRSSUpdates(Rule):
    phases = Phase.RSS_EVALUATION | Phase.END
    rule = if_config("rss.always_accept_update", True)
    action = accept_rss_updates
    description = "Accepts RSS updates depending on the value of `config.rss.always_accept_update`"



if __name__ == "__main__" or DEBUG_RULES:
    
    test = AlwaysAcceptRSSUpdates()
    
    # Check static type hints
    class_like = EvaluationFunction(truthy=True) # this is actually a partial[type[EvaluationFunction]]
    assert issubclass(class_like.func, EvaluationFunction)
    instance = EvaluationFunction(int)
    assert isinstance(instance, EvaluationFunction)
    
    def assert_type(instance, cls):
        assert isinstance(instance, cls)
        return instance
    
    def context_method(self, ctx : "Context") -> bool:
        assert isinstance(self, Rule)
        assert isinstance(ctx, Context)
        return True

    def context_function(ctx : "Context") -> bool:
        assert isinstance(ctx, Context)
        return True
    
    @EvaluationFunction
    def eval_context_method(self, ctx : "Context") -> bool:
        assert isinstance(self, Rule)
        assert isinstance(ctx, Context)
        return True

    @EvaluationFunction
    def eval_context_function(ctx : "Context") -> bool:
        assert isinstance(ctx, Context)
        return True

    @Rule
    class SimpleRule1:
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        rule = context_function
        action = lambda ctx: assert_type(ctx, Context)
    
    class SimpleRule(Rule):
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        rule = context_method
        action = lambda self, ctx: (assert_type(self, Rule), assert_type(ctx, Context))

    class ReverseWhenCollide(Rule):
        phases = Phase.COLLISION | Phase.END
        rule = context_method
        def action(ctx : Context): 
            assert_type(ctx, Context)
            ctx.control.reverse = True
    
    @Rule
    class SimpleRule1B:
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        rule = eval_context_function
        action = lambda ctx: assert_type(ctx, Context)
    
    class SimpleRuleB(Rule):
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        rule = eval_context_method
        action = lambda self, ctx: (assert_type(self, Rule), assert_type(ctx, Context))


    class DebugRuleWithEval(Rule):
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        
        @EvaluationFunction("AlwaysTrue")
        def rule(self, ctx : "Context") -> bool:
            assert isinstance(ctx, Context)
            assert isinstance(self, DebugRuleWithEval)
        
        @rule.register_action(True)
        def true_action(self, ctx : "Context"):
            assert isinstance(ctx, Context)
            assert isinstance(self, DebugRuleWithEval)

        
    class Another(Rule):
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        
        rule = always_execute
        
        actions = {True: lambda self, ctx: (assert_type(self, Rule), assert_type(ctx, Context)),
                False: lambda ctx: assert_type(ctx, Context)}
        
    class Another(Rule):
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        
        rule = always_execute
        
        actions = {True: lambda self, ctx: (assert_type(self, Rule), assert_type(ctx, Context)),
                False: lambda ctx: assert_type(ctx, Context)}
        
    class CustomInitRule(Rule):
        def __init__(self, phases=None):
            # NOTE: The 
            super().__init__(phases=phases or Phase.UPDATE_INFORMATION | Phase.BEGIN, rule=always_execute, action=lambda ctx: assert_type(ctx, Context))
            self._custom = True
        
        phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
        
        _cooldown = 0
        rule = lambda ctx: [][1] # This should not be executed
        
        actions = {True: lambda self, ctx: (assert_type(self, Rule), assert_type(ctx, Context)),
                False: lambda ctx: assert_type(ctx, Context)}

    new_rule = DebugRuleWithEval()
    #new_rule.action
    simple_rule = SimpleRule()
    simple_ruleB = SimpleRuleB()
    another_rule = Another()
    custom_rule = CustomInitRule()
    
    # Check Doc -> Descritpion
    
    class CheckDescription(Rule):
        """This is my description"""
        
    assert CheckDescription.description == """This is my description"""
    assert CheckDescription().description == """This is my description"""

