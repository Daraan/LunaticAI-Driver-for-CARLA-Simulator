from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.rule import Context, Rule

__all__ = [
    'rule_lane_change'
]


def rule_lane_change(self: "Rule", ctx: "Context", order=("left", "right"), **kwargs):
    """
    Helper function to execute lane changes
    
    Assumes:
        - For tailgator check:
            - `(self.config.live_info.incoming_direction == RoadOption.LANEFOLLOW \
                and not waypoint.is_junction and self.config.live_info.current_speed > 10)`:python:
            - `check_behind.obstacle_was_found and self.config.live_info.current_speed < get_speed(check_behind.obstacle)`:python:
    """
    # TODO: Currently need self, function with kwargs does not work yet
    assert 0 <= len(order) <= 2
    changed = ctx.agent.make_lane_change(order, **kwargs)
    if not changed:
        # The rule has triggered but the action was not successful
        self.reset_cooldown(0)  # resets the whole group
