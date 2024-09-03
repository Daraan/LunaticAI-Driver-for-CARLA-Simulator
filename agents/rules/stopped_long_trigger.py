"""Example of a :py:class:`MultiRule` if the agent does not perform any actions for a certain time."""

from typing import List

from agents.rules.behaviour_templates import DEBUG_RULES
from agents.tools.logs import logger
from classes.constants import AgentState, Phase
from classes.rule import ConditionFunction, Context, MultiRule, Rule


class StoppedTooLongTrigger(MultiRule):
    """Triggers child rules if the agent has stopped for a too long time"""
    phase = Phase.UPDATE_INFORMATION | Phase.END
    
    _warning_given = False
    
    stop_time_threshold = 60
    """Time in seconds the agent is allowed to stop before triggering the rule."""
    
    @ConditionFunction
    def condition(self, ctx: Context) -> bool:
        # time stopped in seconds # NOTE: Only in sync mode!
        s_stopped = ctx.agent.current_states[AgentState.STOPPED] * ctx.config.planner.dt
        if s_stopped < self.stop_time_threshold:
            self._warning_given = False
            return False
        return True
    
    def action(self, ctx: Context) -> None:
        if not self._warning_given:
            self._warning_given = True
            logger.warning("Agent has stopped for too long.")
        
    # ... Child rules to be executed
    rules: List[Rule] = []

if __name__ == "__main__" or DEBUG_RULES:

    StoppedTooLongTrigger()
