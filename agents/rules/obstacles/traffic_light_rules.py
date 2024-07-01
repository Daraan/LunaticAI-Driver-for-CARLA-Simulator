from dataclasses import dataclass
import carla
from omegaconf import II, SI

from agents.rules.behaviour_templates import DEBUG_RULES
from agents.tools.hints import TrafficLightDetectionResult
from agents.tools.lunatic_agent_tools import phase_callback
from agents.tools.logging import logger

from classes.constants import Hazard, Phase, RulePriority
from classes.evaluation_function import ConditionFunction
from classes.exceptions import LunaticAgentException, SkipInnerLoopException
from classes.rule import BlockingRule, Context

from agents.tools.config_creation import RuleConfig

__all__ = ["DriveSlowTowardsTrafficLight"]   
    
class DriveSlowTowardsTrafficLight(BlockingRule):
    """
    When the agent is at a red traffic light and it is red drive forward slowly.
    """
    
    priority = RulePriority.LOW
    
    phase = Phase.EMERGENCY | Phase.BEGIN
    
    MAX_TICKS = 2000 # 2000 * 0.05 = 100 seconds
    
    DEFAULT_COOLDOWN_RESET = 500
    
    @ConditionFunction
    def condition(self, ctx: Context):
        """Executes if a traffic light is the only hazard"""
        # Prevent recursive calls
        if self in ctx.active_blocking_rules:
            return
        return Hazard.TRAFFIC_LIGHT in ctx.detected_hazards and not {Hazard.OBSTACLE} & ctx.detected_hazards
    
    @dataclass
    class self_config(RuleConfig):
        # When being too fast -> slow down
        max_brake : float = II("controls.max_brake")            # This refers to the agent
        normal_brake : float = II("min:0.2,${self.max_brake}")  # This to self_config.max_brake
        min_brake : float = 0.1
        
        # When being slow -> speed up slowly
        throttle : float = 0.25
        
    

    @phase_callback(on_exit = Phase.CUSTOM_CYCLE | Phase.END, on_exit_exceptions=LunaticAgentException)
    def action(self, ctx: Context):
        # Remove triggering hazard
        logger.info("Entering DriveSlowTowardsTrafficLight rule.")
        ctx.detected_hazards = {h for h in ctx.detected_hazards if Hazard.TRAFFIC_LIGHT not in h}

        last_traffic_light = ctx.agent._last_traffic_light
        if not last_traffic_light:
            return
        
        # We do not accidentally want to drive away from the traffic light
        # Problems:
        #  Trigger Waypoint is before the traffic light, need an alternative
        affected_wps = last_traffic_light.get_affected_lane_waypoints()
        distance = last_distance =float("inf")
        for wp in affected_wps:
            test_distance = ctx.live_info.current_location.distance(wp.transform.location)
            if test_distance < distance:
                clostest_wp = wp
                distance = test_distance
        
        affected = True
        
        # Smaller list of lights to check, however calls the simulator!
        traffic_light_group = last_traffic_light.get_group_traffic_lights()
        
        while affected and distance <= last_distance + 1/10000:
            #if self.ticks_passed % 10 == 0:
            #    logger.ifno("DriveSlowTowardsTrafficLight: distance: %f", distance)
            #if self.ticks_passed % 50 == 1:
            #    breakpoint()
            
            # You should always use ctx.agent.calculate_control() before self.loop_agent
            # This will move the planned waypoint queue forward.
            # However, the rule might be after the step was already calculated.
            
            # -------------------------------------------
            # Get the current control object of this step
            # -------------------------------------------
            # if you use loop_agent(ctx, execute_planner=True)
            # this will be the same as the next_control object acquired below.
            control = ctx.get_or_calculate_control()
            
            # However there is the problem that not all traffic lights seem to be
            # equal
            
            # This should be some configs
            if distance < ctx.config.obstacles.base_tlight_threshold + 0.2:
                return # Handle by Emergency End
            elif distance < 8 and ctx.live_info.current_speed / 3.6 > distance:
                control.brake = max(self.self_config.max_brake, control.brake)
                control.throttle = 0
            elif ctx.live_info.current_speed > 40 or ctx.live_info.current_speed / 1.8 > distance:
                control.brake = max(self.self_config.normal_brake, control.brake)
                control.throttle = 0
            elif 15 < ctx.live_info.current_speed < 40:
                control.brake = max(self.self_config.min_brake, control.brake)
                control.throttle = 0
            else:
                 # The local planner is not aware of a red light, it will likely be higher
                 # take the minimum instead
                control.throttle = min(self.self_config.throttle, control.throttle, distance / 10)
                if control.throttle > 0.05:
                    control.brake = 0

            # PROBLEM if triggered a second, the agent might drive to fast.
            # Need better distance checking.
                
            # -------------------------------------------
            # 
            #  - ctx.get_or_calculate_control()
            # 
            # - ctx.agent.parse_keyboard_input
            # - ctx.agent.apply_control
            # - self.update_world
            # 
            # Are nearly equivalent to BlockingRule.loop_agent
            # which encapsulates the above functions, the only difference is
            # that BlockingRule.loop_agent will calculate the next control object at the end
            # for the end of the tick when this rule is done.
            # ------------------------------------------
            
            print("Control: ", control)
            
            # It is up to the user wether or not to apply controls inside a blocking rule
            ctx.agent.parse_keyboard_input(control=control) # NOTE: if skipped the user has no option to stop the agent
            ctx.agent.apply_control(control)
            
            # NOTE: This ticks the world forward by one step
            # The ctx.control is reset to None
            
            # > Phase.UPDATE_INFORMATION | Phase.BEGIN
            self.update_world(ctx)
            # > Phase.UPDATE_INFORMATION | Phase.END
            
            # Remove the traffic light hazard and check again
            ctx.detected_hazards = {h for h in ctx.detected_hazards if Hazard.TRAFFIC_LIGHT not in h}
            # Other obstacles we do not want to hit
            obstacle = ctx.agent.detect_obstacles_in_path("all")
            if obstacle.obstacle_was_found:
                if isinstance(obstacle.obstacle, carla.Vehicle):
                    ctx.agent.add_hazard(Hazard.CAR)
                elif isinstance(obstacle.obstacle, carla.Walker):
                    ctx.agent.add_hazard(Hazard.PEDESTRIAN)
                else:
                    ctx.agent.add_hazard(Hazard.OBSTACLE)
                break
            affected: TrafficLightDetectionResult = ctx.agent.traffic_light_manager(traffic_light_group)
            if affected.traffic_light_was_found:
                ctx.agent.add_hazard(Hazard.TRAFFIC_LIGHT)
                affected = True
            else:
                affected = False
            last_distance = distance
            distance = ctx.live_info.current_location.distance(clostest_wp.transform.location)
        logger.info("Exiting DriveSlowTowardsTrafficLight rule after %s ticks.", self.ticks_passed)
        if ctx.control: # NOTE: This is unset with self.update_world
            raise SkipInnerLoopException(ctx.control)

    def max_tick_callback(self, ctx: Context):
        ctx.control = carla.VehicleControl(brake=1)
        raise SkipInnerLoopException(ctx.control)
