import carla
from agents.navigation.local_planner import RoadOption

from classes.rule import Rule, EvaluationFunction
from agents.tools.lunatic_agent_tools import Phases, detect_vehicles
from agents.tools.misc import get_speed

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from agents import LunaticAgent

@EvaluationFunction
def always_execute(agent):
    return True

def set_default_intersection_speed(agent):
    target_speed = min([
            agent.config.speed.max_speed,
            agent.config.live_info.current_speed_limit - agent.config.speed.intersection_speed_decrease]
            ) 
    # NOTE: could interpolate this in omega conf
    agent.config.speed.target_speed = target_speed
    
normal_intersection_speed_rule = Rule(Phases.TURNING_AT_JUNCTION | Phases.BEGIN, 
                                      rule=always_execute, 
                                      action=set_default_intersection_speed, 
                                      description="Set speed to intersection speed")

def set_default_speed(agent):
    target_speed = min([
            agent.config.speed.max_speed,
            agent.config.live_info.current_speed_limit - agent.config.speed.speed_lim_dist])
    agent.config.speed.target_speed = target_speed

normal_speed_rule = Rule(Phases.TAKE_NORMAL_STEP | Phases.BEGIN,
                        rule=always_execute,
                        action=set_default_speed,
                        description="Set speed to normal speed")

# ----------- Avoid Beeing tailgated -----------

def avoid_tailgator(agent : "LunaticAgent"):
    """
    This method is in charge of tailgating behaviors.

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
                agent.config.other.tailgate_counter = 200
                agent.set_destination(end_waypoint.transform.location,
                                        left_wpt.transform.location)

@EvaluationFunction            
def avoid_tailgator_check(agent : "LunaticAgent") -> bool:
    """
    Vehicle wants to stay in lane, is not at a junction, and has a minimum speed
    and did not avoided tailgating in the last 200 steps

    Assumes: No car in front/side (which is a hazard in itself)
    """
    waypoint = agent._current_waypoint

    return (agent.config.live_info.direction == RoadOption.LANEFOLLOW \
            and not waypoint.is_junction and agent.config.live_info.current_speed > 10  #TODO Hardcoded
            and agent.config.other.tailgate_counter == 0)

Rule(Phases.DETECT_CARS | Phases.END,
     rule=avoid_tailgator_check,
     action=avoid_tailgator,
     description="Avoid tailgating when followed by a faster car that is quite close.")