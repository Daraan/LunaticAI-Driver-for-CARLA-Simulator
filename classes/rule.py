from typing import Any, Callable, Optional, Dict
from agents.lunatic_agent import LunaticAgent
from utils.evaluation_function import EvaluationFunction


class Rule:
    def __init__(self, rule: Callable[[LunaticAgent], bool], action: Callable,
                 description: str = "What does this rule do?",
                 overwrite_settings: Optional[Dict[str, Any]] = None) -> None:
        self.rule = rule
        self.action = action
        self.description = description
        self.overwrite_settings = overwrite_settings or {}

    def evaluate(self, agent: LunaticAgent, overwrite: Optional[Dict[str, Any]] = None) -> bool:
        settings = self.overwrite_settings.copy()
        if overwrite is not None:
            settings.update(overwrite)
        result = self.rule(agent, settings)
        return result

    def __call__(self, agent: LunaticAgent, overwrite: Optional[Dict[str, Any]] = None) -> Any:
        if self.evaluate(agent, overwrite):
            return self.action(agent)
        return None

    function = EvaluationFunction
