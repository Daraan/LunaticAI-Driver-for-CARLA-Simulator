import random
from functools import partial, update_wrapper
from typing import List, Optional

import carla
from omegaconf._impl import select_node # noqa: PLC2701

from classes.constants import READTHEDOCS, Phase
from classes.rule import ConditionFunction, Context, Rule, always_execute

_use_debug_rules = True # TODO: Turn off again #XXX
DEBUG_RULES: bool = not READTHEDOCS and _use_debug_rules

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
    func = partial(_if_config_checker, config_path=config_path, value=value)
    func = update_wrapper(func, _if_config_checker)
    return ConditionFunction(func,
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
    phase = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    condition = always_execute
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
    phases = Phase.TAKE_NORMAL_STEP | Phase.BEGIN # type: ignore[assignment]
    condition = always_execute
    action = set_default_speed
    description = "Set speed to normal speed"

# ----------- Plan next waypoint -----------

def random_spawnpoint_destination(ctx: "Context", waypoints: Optional[List[carla.Waypoint]]=None):
    """
    Set a random waypoint as the next target.
    """
    print("The target has been reached, searching for another target")
    ctx.agent._world_model.hud.notification("Target reached", seconds=4.0)
    if waypoints is None:
        transforms = ctx.get_map().get_spawn_points()
        loc = random.choice(transforms).location
    else:
        loc = random.choice(waypoints).transform.location
    ctx.agent.set_destination(loc)
    
@ConditionFunction
def is_agent_done(ctx: Context) -> bool:
    """
    Agent has reached its destination.
    """
    return ctx.agent.done()

class TargetRandomSpawnpointWhenDone(Rule):
    """
    Sets random waypoint when done
    """
    phases = Phase.DONE | Phase.BEGIN  # type: ignore[assignment]
    condition = is_agent_done
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
    phases = Phase.DONE | Phase.BEGIN  # type: ignore[assignment]
    condition = is_agent_done
    action = set_next_waypoint_nearby

# ----------- RSS Rules -----------

def accept_rss_updates(ctx : Context):
    """
    Accept RSS updates from the RSS manager.
    """
    if ctx.prior_result is None:
        return None
    assert isinstance(ctx.prior_result, carla.VehicleControl)
    ctx.control = ctx.prior_result
    
assert isinstance(if_config("rss.enabled", True), ConditionFunction)

class AlwaysAcceptRSSUpdates(Rule):
    """
    Always accept RSS updates if rss is enabled in the config.
    
    """
    phases = Phase.RSS_EVALUATION | Phase.END # type: ignore[assignment]
    condition=if_config("rss.enabled", True)
    action = accept_rss_updates
    description = "Always accepts the updates calculated by the RSS System."

class ConfigBasedRSSUpdates(Rule):
    """Always accept RSS updates if :any:`rss.always_accept_update <LunaticAgentSettings.rss>` is set to True in the config."""
    phases = Phase.RSS_EVALUATION | Phase.END # type: ignore[assignment]
    condition = if_config("rss.always_accept_update", True)
    action = accept_rss_updates
    #description = "Accepts RSS updates depending on the value of `config.rss.always_accept_update`"


# ----------- Tests -----------

if __name__ == "__main__" or DEBUG_RULES:
    from ._debug_rules import debug_rules as debug_rules # mark as reexport # noqa: PLC0414
