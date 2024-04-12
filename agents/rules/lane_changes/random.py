from classes.constants import Phase
from classes.rule import Context, Rule, RulePriority, always_execute

import carla
import numpy as np

__all__ = ["RandomLaneChangeRule"]

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

        self.reset_cooldown(ctx.config.lane_change.random_lane_change_interval)


# TODO: Create a stay right rule!    
# ----------- Lane Change Rules -----------
