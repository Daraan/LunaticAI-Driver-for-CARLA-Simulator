from dataclasses import dataclass
from typing import NoReturn, TYPE_CHECKING

import carla
from omegaconf import II

from agents.tools.config_creation import RuleConfig
from agents.tools.logs import logger
from agents.tools.misc import get_closest_tl_trigger_wp
from classes.constants import Hazard, Phase, RulePriority
from classes.evaluation_function import ConditionFunction
from classes.exceptions import SkipInnerLoopException
from classes.rule import BlockingRule, Context, Rule

if TYPE_CHECKING:
    from agents.tools.hints import TrafficLightDetectionResult

__all__ = ["DriveSlowTowardsTrafficLight", "PassYellowTrafficLightRule"]


class PassYellowTrafficLightRule(Rule):
    priority = RulePriority.HIGH
    
    phase = Phase.DETECT_TRAFFIC_LIGHTS | Phase.END
    
    @dataclass
    class self_config(RuleConfig):
        try_to_pass : bool = False
        """If the agent should try to pass the yellow light."""
        
        passing_speed : float = II("max:${mul:${live_info.current_speed_limit},1.33},${speed.target_speed}")
        """The speed the agent should try to pass the yellow light."""
    
    @ConditionFunction
    @staticmethod
    def condition(ctx: Context) -> "None | carla.TrafficLightState":
        """Executes if a traffic light is the only hazard"""
        if not ctx.agent.current_traffic_light:
            return None
        return ctx.agent.current_traffic_light.state
    
    
    @condition.register_action(carla.TrafficLightState.Yellow)
    def yellow_action(self, ctx: Context):
        logger.info("Entering IsAtYellowTrafficLight rule.")
        if self.self_config.try_to_pass:
            ctx.config.speed.follow_speed_limits = False
            ctx.config.speed.target_speed = self.self_config.passing_speed
            ctx.discard_hazard(Hazard.TRAFFIC_LIGHT_YELLOW, match="exact")
        else:
            ctx.add_hazard(Hazard.TRAFFIC_LIGHT_YELLOW)  # -> Emergency Rules
                      
        

class DriveSlowTowardsTrafficLight(BlockingRule):
    """
    When the agent is at a red traffic light and it is red drive forward slowly.
    """
    
    priority = RulePriority.LOW
    
    phase = Phase.EMERGENCY | Phase.BEGIN
    
    MAX_TICKS = 2000  # 2000 * 0.05 = 100 seconds
    
    DEFAULT_COOLDOWN_RESET = 500
    
    @ConditionFunction
    def condition(self, ctx: Context):
        """Executes if a traffic light is the only hazard"""
        # Prevent recursive calls
        if self in ctx.active_blocking_rules:
            return
        # Checks for yellow and red lights
        return ctx.has_hazard(Hazard.TRAFFIC_LIGHT, "intersection") and not ctx.has_hazard(Hazard.OBSTACLE)
    
    # Important need to turn this of to have custom speed limits.
    overwrite_settings = {"speed" : {"follow_speed_limits" : False}, }
    
    @dataclass
    class self_config(RuleConfig):
        max_brake : float = II("divide:${controls.max_brake},8")
        """Max break that should be applied when above the target speed."""
        
        max_throttle : float = II("divide:${controls.max_throttle},4")
        """Max throttle that should be applied when below the target speed."""
    
    #@phase_callback(on_exit=Phase.CUSTOM_CYCLE | Phase.END, on_exit_exceptions=LunaticAgentException)
    def action(self, ctx: Context):
        # Remove triggering hazard
        logger.info("Entering DriveSlowTowardsTrafficLight rule.")
        
        # Remove the hazard as we handle it below; removes yellow and red light hazards
        ctx.discard_hazard(Hazard.TRAFFIC_LIGHT, "intersection")

        last_traffic_light = ctx.agent.current_traffic_light
        if not last_traffic_light:
            return  # should not happen
        
        # We do not accidentally want to drive away from the traffic light
        # Problems:
        #  Trigger Waypoint is before the traffic light, need an alternative
        clostest_wp, distance = get_closest_tl_trigger_wp(ctx.live_info.current_location, last_traffic_light)
        traffic_light_group = last_traffic_light.get_group_traffic_lights()
        last_distance = float("inf")
        
        # Smaller list of lights to check, however calls the simulator!
        
        affected: TrafficLightDetectionResult | bool = True
        while affected and distance <= last_distance + 1 / 1000:
            # You should always use ctx.agent.calculate_control() before self.loop_agent
            # This will move the planned waypoint queue forward.
            # However, the rule might be after the step was already calculated.
            
            # -------------------------------------------
            # Get the current control object of this step
            # -------------------------------------------
            # if you use loop_agent(ctx, execute_planner=True)
            # this will be the same as the next_control object acquired below.
            
            if distance < ctx.config.obstacles.base_tlight_threshold + 0.5:
                break  # End loop -> Other Emergency Rule
            
            if not ctx.control:  # Not yet set; this is the expected case
                # Change settings before calculating the control object
                ctx.config.speed.target_speed = min(ctx.config.speed.target_speed, distance * 2)
                ctx.config.controls.max_brake = self.self_config.max_brake
                ctx.config.controls.max_throttle = self.self_config.max_throttle
                #print("Target Speed: ", ctx.config.speed.target_speed,
                #      "current speed: ", ctx.live_info.current_speed)
                # # calculate it now
                control = ctx.get_or_calculate_control()
            else:
                logger.debug("Control is already set in DriveSlowTowardsTrafficLight rule. Skipping calculation.")
            
            # ------------ Loop Agent -------------------
            # Logic:
            # - ctx.get_or_calculate_control()
            #
            # - ctx.agent.parse_keyboard_input
            # - ctx.agent.apply_control
            # - self.update_world
            #
            # Are nearly equivalent to `BlockingRule.loop_agent`
            # which encapsulates the above functions, the only difference is
            # that BlockingRule.loop_agent will calculate the next control object at the end
            # for the end of the tick when this rule is done.
            # ------------------------------------------
            
            print("Control: ", control)
            
            # It is up to the user wether or not to apply controls inside a blocking rule
            ctx.agent.parse_keyboard_input(control=control)  # NOTE: if skipped the user has no option to stop the agent
            ctx.agent.apply_control(control)
            
            # NOTE: This ticks the world forward by one step
            # The ctx.control is reset to None
            # > Phase.UPDATE_INFORMATION | Phase.BEGIN
            self.update_world(ctx)
            # > Phase.UPDATE_INFORMATION | Phase.END
            
            # ------------------ Check if we should continue -----------------
            
            # Remove the traffic light hazard and check again
            ctx.discard_hazard(Hazard.TRAFFIC_LIGHT, "intersection")
            
            # Other obstacles we do not want to hit
            obstacle = ctx.agent.detect_obstacles_in_path("all")
            
            # TODO: should be a function
            if obstacle.obstacle_was_found:
                if isinstance(obstacle.obstacle, carla.Vehicle):
                    ctx.agent.add_hazard(Hazard.CAR)
                elif isinstance(obstacle.obstacle, carla.Walker):
                    ctx.agent.add_hazard(Hazard.PEDESTRIAN)
                else:
                    ctx.agent.add_hazard(Hazard.OBSTACLE)
                break  # End loop -> Other Emergency Rule
            
            affected = ctx.agent.detect_traffic_light(traffic_light_group)
            if affected.traffic_light_was_found:
                ctx.add_hazard(Hazard.TRAFFIC_LIGHT)
                affected = True
            else:
                affected = False
            last_distance = distance
            distance = ctx.live_info.current_location.distance(clostest_wp.transform.location)
        
        logger.info("Exiting DriveSlowTowardsTrafficLight rule after %s ticks.", self.ticks_passed)
        if ctx.control:  # NOTE: This is unset with self.update_world
            raise SkipInnerLoopException(ctx.control)

    def max_tick_callback(self, ctx: Context) -> NoReturn:
        if ctx.control:
            ctx.control.brake = 1.0
            ctx.control.throttle = 0.0
        else:
            ctx.config.speed.target_speed = 0.0
            ctx.get_or_calculate_control()
        raise SkipInnerLoopException(ctx.control)  # type: ignore[arg-type]
