from typing import Callable, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent
import inspect


class EvaluationFunction:
    def __init__(self, evaluation_function: Callable[["LunaticAgent"], bool], name="EvaluationFunction"):
        self.evaluation_function = evaluation_function
        self.name = name if name != "EvaluationFunction" else evaluation_function.__name__

    def __call__(self, agent: "LunaticAgent", *args, **kwargs) -> bool:
        return self.evaluation_function(agent, *args, **kwargs)

    @staticmethod
    def _complete_func_to_string(func):
        func_lines = inspect.getsourcelines(func)[0]
        func_string = "".join(func_lines).strip()
        return func_string

    @staticmethod
    def _func_to_string(func):
        if func.__name__ == "<lambda>":
            return EvaluationFunction._complete_func_to_string(func)
        return func.__name__

    def __str__(self):
        return self.name

    @classmethod
    def AND(cls, func1, func2):
        def combined_func(agent: "LunaticAgent", *args, **kwargs):
            return func1(agent, *args, **kwargs) and func2(agent, *args, **kwargs)

        return cls(combined_func, name=f"{func1.name}_and_{func2.name}")

    @classmethod
    def OR(cls, func1, func2):
        def combined_func(agent: "LunaticAgent", *args, **kwargs):
            return func1(agent, *args, **kwargs) or func2(agent, *args, **kwargs)

        return cls(combined_func, name=f"{func1.name}_or_{func2.name}")

    @classmethod
    def NOT(cls, func):
        def combined_func(agent: "LunaticAgent", *args, **kwargs):
            return not func(agent, *args, **kwargs)

        return cls(combined_func, name=f"not_{func.name}")

    def __add__(self, other):
        return self.AND(self, other)

    def __or__(self, other):
        return self.OR(self, other)

    def __invert__(self):
        return self.NOT(self)


class ActionFunction(EvaluationFunction):
    def __init__(self, action_function: Callable[["LunaticAgent"], Any], name="ActionFunction"):
        super().__init__(action_function, name)

    # Overriding the NOT method isn't appropriate here since this class is for actions, not evaluations.
    # If you wish to have a NOT like functionality, it should be clearly defined what "NOT" an action means.

    def __call__(self, agent: "LunaticAgent", *args, **kwargs) -> Any:
        return self.action_function(agent, *args, **kwargs)