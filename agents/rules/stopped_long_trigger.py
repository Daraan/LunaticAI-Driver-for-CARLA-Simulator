
from agents.rules.behaviour_templates import DEBUG_RULES

from classes.constants import AgentState, Phase
from classes.rule import Rule, MultiRule, EvaluationFunction, Context

from agents.tools.logging import logger

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from agents import LunaticAgent
    
class StoppedTooLongTrigger(MultiRule):
    """Triggers child rules if the agent has stopped for a too long time"""
    phase = Phase.UPDATE_INFORMATION | Phase.END
    
    _warning_given = False
    
    stop_time_threshold = 60
    """Time in seconds the agent is allowed to stop before triggering the rule."""
    
    @EvaluationFunction
    def rule(self, ctx: Context) -> bool:
        # time stopped in seconds # NOTE: Only in sync mode!
        s_stopped = ctx.agent.current_states[AgentState.STOPPED] * ctx.config.planner.dt
        if s_stopped < self.stop_time_threshold:
            self._warning_given = False
            return False
        return True
    
    def action(self, ctx: Context):
        if not self._warning_given:
            self._warning_given = True
            logger.warning("Agent has stopped for too long.")
        
    # ... Child rules to be executed
    rules: List[Rule] = []

if __name__ == "__main__" or DEBUG_RULES:

    StoppedTooLongTrigger()