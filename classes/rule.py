from enum import Enum
from typing import Any, Set, Union, Iterable, Callable, Optional, Dict, TYPE_CHECKING
from collections.abc import Iterable

from agents.tools.lunatic_agent_tools import Phases
from utils.evaluation_function import EvaluationFunction

if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent

class Rule:
    def __init__(self, 
                 phases : Union[Phases, Iterable], #￿iterable of Phases
                 rule : Callable[["LunaticAgent"], bool], 
                 action: Union[Callable, Dict[Any, Callable]] = None, 
                 false_action = None,
                 *, 
                 actions : Dict[Any, Callable] = None,
                 description: str = "What does this rule do?",
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 ignore_chance=0.2,
                 ) -> None:
        if not isinstance(phases, set):
            if isinstance(phases, Iterable):
                phases = set(phases)
            else:
                phases = {phases}
        for p in phases:
            if not isinstance(p, Phases):
                raise ValueError(f"phase must be of type Phases, not {type(p)}")
        
        self.apply_in_phases = phases # TODO: CRITICAL: 
        if isinstance(action, dict):
            self.actions = action
            if false_action is not None or actions is not None:
                raise ValueError("When passing a dict to action, false_action and actions must be None")
        else:
            self.actions = {}
            if action is not None:
                self.actions[True] = action
            if false_action is not None:
                self.actions[False] = false_action
        
        self.rule = rule
        self.description = description
        self.overwrite_settings = overwrite_settings or {}

    def evaluate(self, agent: "LunaticAgent", overwrite: Optional[Dict[str, Any]] = None) -> bool:
        settings = self.overwrite_settings.copy()
        if overwrite is not None:
            settings.update(overwrite)
        result = self.rule(agent, settings)
        return result

    def __call__(self, agent: "LunaticAgent", overwrite: Optional[Dict[str, Any]] = None) -> Any:
        # Check phase
        if agent.current_phase not in self.apply_in_phases:
            return None # not applicable for this phase
        result = self.evaluate(agent, overwrite)
        if result in self.actions:
            return self.actions[result](agent, overwrite)
        return None



