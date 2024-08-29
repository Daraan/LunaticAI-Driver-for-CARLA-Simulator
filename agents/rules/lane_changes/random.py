from dataclasses import dataclass
from agents.rules.behaviour_templates import DEBUG_RULES
from agents.tools.config_creation import RuleConfig
from classes.constants import Phase, RulePriority
from classes.rule import Context, Rule, always_execute

import carla
import numpy as np

__all__ = ["RandomLaneChangeRule"]

class RandomLaneChangeRule(Rule):
    phases = Phase.TAKE_NORMAL_STEP | Phase.BEGIN
    condition = always_execute # TODO: Could implement check here, instead of relying on `lane_change`
    cooldown_reset_value = None

    priority = RulePriority.LOWEST
    group = "lane_change"
    description = "Randomly change lane"
    start_cooldown = 25
    
    # ----------- Lane Change Rules -----------
    # self_config can be defined as a normal dict,
    # to have type-hint, auto-completion use a setup like this:
    # When the rule is initialized, the values are copied to the instance
    
    @dataclass # <-- NOTE: DO NOT FORGET TO ADD, else the keys will be missing
    class self_config(RuleConfig):
        random_lane_change_interval : int = 200
        """Cooldown value for a lane change in the 'lane_change' group."""
        
        random_right_lanechange_percentage : float = 0.1
        """
        Adjust probability that in each timestep the actor will perform a left/right lane change,
        dependent on lane change availability.
        """
        
        random_left_lanechange_percentage: float = 0.1
        """
        Adjust probability that in each timestep the actor will perform a left/right lane change,
        dependent on lane change availability.
        """

    def action(self, ctx: "Context"):
        """
        Change lane to the left or right.
        """
        print("Changing Lane randomly")
        p_left = self.self_config.random_left_lanechange_percentage
        p_right = self.self_config.random_right_lanechange_percentage
        p_stay = max(0, 1 - p_left - p_right) # weight to stay in the same lane
        direction : carla.LaneChange = carla.LaneChange(np.random.choice( (1, 0, 2), p=(p_left, p_stay, p_right)))
        print("Direction: ", direction)
        if direction == 0:
            self.reset_cooldown(self.self_config.random_lane_change_interval)
            return
        ctx.agent.lane_change("left" if direction == 1 else "right",
                            same_lane_time=ctx.config.lane_change.same_lane_time,
                            other_lane_time=ctx.config.lane_change.other_lane_time,
                            lane_change_time=ctx.config.lane_change.lane_change_time)

        self.reset_cooldown(self.self_config.random_lane_change_interval)


if __name__ == "__main__" or DEBUG_RULES:
    RandomLaneChangeRule()

