from functools import partial

import carla
from agents.navigation.local_planner import RoadOption

from classes.constants import Phase
from classes.rule import Rule, EvaluationFunction, Context, always_execute
from agents.tools.lunatic_agent_tools import detect_vehicles
from agents.tools.misc import get_speed

from typing import TYPE_CHECKING, List

from classes.rule import always_execute
if TYPE_CHECKING:
    from agents import LunaticAgent

#TODO: maybe create some omega conf dict creator that allows to create settings more easily
# e.g. CreateOverwriteDict.speed.max_speed = 60, yields such a subdict.
# QUESTION: How to merge more than one entry?

def if_config_checker(ctx : "Context", config_path : str, value) -> bool:
    """
    Check if a value in the config is set to a certain value.
    """
    return ctx.config[config_path] == value

def if_config(config_path, value):
    """
    Returns a partial function that checks if a value in the config is set to a certain value.
    """
    return partial(if_config_checker, config_path=config_path, value=value)

# ------ Speed Rules ------

def set_default_intersection_speed(agent):
    """
    Slow down the car when turning at a junction.
    """
    target_speed = min([
            agent.config.speed.max_speed,
            agent.config.live_info.current_speed_limit - agent.config.speed.intersection_speed_decrease]
            ) 
    # NOTE: could interpolate this in omega conf
    agent.config.speed.target_speed = target_speed
    
normal_intersection_speed_rule = Rule(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, 
                                      rule=always_execute, 
                                      action=set_default_intersection_speed, 
                                      overwrite_settings= {"speed": {"intersection_speed_decrease": 10}},
                                      description="Set speed to intersection speed")

# -----

def set_default_speed(agent):
    """
    Speed to apply when the car drives under normal circumstances, 
    i.e. no junctions, no obstacles, etc. detected.
    """
    target_speed = min([
            agent.config.speed.max_speed,
            agent.config.live_info.current_speed_limit - agent.config.speed.speed_lim_dist])
    agent.config.speed.target_speed = target_speed

normal_speed_rule = Rule(Phase.TAKE_NORMAL_STEP | Phase.BEGIN,
                        rule=always_execute,
                        action=set_default_speed,
                        description="Set speed to normal speed")

# ----------- Avoid Beeing tailgated -----------

def avoid_tailgator(agent : "LunaticAgent"):
    """
    If a tailgator is detected, move to the left/right lane if possible

        :param waypoint: current waypoint of the agent
        :param vehicle_list: list of all the nearby vehicles
    """
    vehicle_list = agent.nearby_vehicles
    waypoint = agent._current_waypoint # todo use a getter

    behind_vehicle_state, behind_vehicle, _ = detect_vehicles(vehicle_list, max(
        agent.config.distance.min_proximity_threshold, agent.config.live_info.current_speed_limit / 2), up_angle_th=180, low_angle_th=160)
    if behind_vehicle_state and agent.config.live_info.current_speed < get_speed(behind_vehicle):
        # There is a faster car behind us

        left_turn = waypoint.left_lane_marking.lane_change
        right_turn = waypoint.right_lane_marking.lane_change

        left_wpt = waypoint.get_left_lane()
        right_wpt = waypoint.get_right_lane()

        if (right_turn == carla.LaneChange.Right or right_turn ==
            carla.LaneChange.Both) and waypoint.lane_id * right_wpt.lane_id > 0 and right_wpt.lane_type == carla.LaneType.Driving:
            
            detection_result = detect_vehicles(vehicle_list, max(
                agent.config.distance.min_proximity_threshold, agent.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=1)
            if not detection_result.obstacle_was_found:
                print("Tailgating, moving to the right!")
                end_waypoint = agent._local_planner.target_waypoint
                agent.config.other.tailgate_counter = 200
                agent.set_destination(end_waypoint.transform.location,
                                        right_wpt.transform.location)
        
        elif left_turn == carla.LaneChange.Left and waypoint.lane_id * left_wpt.lane_id > 0 and left_wpt.lane_type == carla.LaneType.Driving:
            detection_result = detect_vehicles(vehicle_list, max(
                agent.config.distance.min_proximity_threshold, agent.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=-1)
            
            if  not detection_result.obstacle_was_found:
                print("Tailgating, moving to the left!")
                end_waypoint = agent._local_planner.target_waypoint
                agent.config.other.tailgate_counter = 200  # TODO: Hardcoded
                agent.set_destination(end_waypoint.transform.location,
                                        left_wpt.transform.location)

@EvaluationFunction            
def avoid_tailgator_check(ctx : "Context") -> bool:
    """
    Vehicle wants to stay in lane, is not at a junction, and has a minimum speed
    and did not avoided tailgating in the last 200 steps

    ASSUMES: No car in front/side (which is a hazard in itself) found in DETECT_CARS phase
    
    # TODO: add option in rule to receive the result of the DETECT_CARS phase
    """
    waypoint = ctx.agent._current_waypoint

    return (ctx.agent.config.live_info.direction == RoadOption.LANEFOLLOW \
            and not waypoint.is_junction and ctx.agent.config.live_info.current_speed > 10  #TODO Hardcoded
            and ctx.agent.config.other.tailgate_counter == 0 # Counter to not change lane too often
            )

avoid_tailgator_rule = Rule(Phase.DETECT_CARS | Phase.END,
                            rule=avoid_tailgator_check,
                            action=avoid_tailgator,
                            description="Avoid tailgating when followed by a faster car that is quite close.")


# ----------- Plan next waypoint -----------

def set_random_waypoint(ctx : "Context", waypoints : List[carla.Waypoint]=None):
    """
    Set a random waypoint as the next target.
    """
    if waypoints is None:
        waypoints = ctx.agent._map.get_spawn_points()
    import random
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

# ----------- RSS Rules -----------

def accept_rss_updates(ctx : Context):
    """
    Accept RSS updates from the RSS manager.
    """
    if ctx.prior_result is None:
        return None
    assert isinstance(ctx.prior_result, carla.VehicleControl)
    ctx.control = ctx.prior_result

always_accept_rss_updates = Rule(Phase.RSS_EVALUATION | Phase.END,
                                     rule=always_execute,
                                     action=accept_rss_updates,
                                     description="Sets random waypoint when done")

config_based_rss_updates = Rule(Phase.RSS_EVALUATION | Phase.END,
                                rule=if_config("rss.enabled", True),
                                action=accept_rss_updates,
                                description="Sets random waypoint when done")

default_rules = [normal_intersection_speed_rule, normal_speed_rule, avoid_tailgator_rule, set_random_waypoint_when_done, config_based_rss_updates]