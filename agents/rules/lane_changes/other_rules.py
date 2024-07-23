from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.rule import Context
    from classes.rule import Rule

def rule_lane_change(self: "Rule", ctx: "Context", order=("left", "right"), **kwargs):
    """Helper function to execute lane changes"""
    # TODO: Currently need self, function with kwargs does not work yet
    assert 0 <= len(order) <= 2
    changed = ctx.agent.make_lane_change(order, **kwargs)
    if not changed:
        self.reset_cooldown(0) # resets the whole group
