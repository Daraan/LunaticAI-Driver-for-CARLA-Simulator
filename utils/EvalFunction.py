from agents.lunatic_agent import LunaticAgent
from utils.evaluation_function import EvaluationFunction


class EvalFunction:
    def __init__(self, function: EvaluationFunction):
        self.function = function

    def and_(self, other):
        return EvalFunction(EvaluationFunction.AND(self.function, other.function))

    def or_(self, other):
        return EvalFunction(EvaluationFunction.OR(self.function, other.function))

    def not_(self):
        return EvalFunction(EvaluationFunction.NOT(self.function))

    def __call__(self, agent: LunaticAgent, *args, **kwargs) -> bool:
        return self.function(agent, *args, **kwargs)
