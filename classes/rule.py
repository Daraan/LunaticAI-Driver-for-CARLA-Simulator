from typing import Any, Callable, Optional, Dict
from agents.lunatic_agent import LunaticAgent
from utils.evaluation_function import EvaluationFunction

class Rule:
    ...
    # TODO:

    def __init__(self, rule : Callable[[LunaticAgent], bool], action, description:str="What does this rule do?", overwrite_settings:Optional[Dict[str]]=None) -> None:
        self.rule = rule
        pass

    def evaluate(self, agent:LunaticAgent, overwrite:dict=None) -> bool:
        if overwrite is not None:
            overwrite = {**self.overwrite_settings, **overwrite}
        else:
            overwrite = self.overwrite_settings
        result = self.rule(agent, overwrite)
        return result

    def __call__(self, agent, overwrite=None) -> Any:
        self.evaluate(agent, overwrite)

    function = EvaluationFunction # This is allows to use "@Rule.function" as well as "@EvaluationFunction"   # TODO: Discuss if this is a good idea or the contrary.