from functools import partial
from typing import Callable, Any, Hashable, TYPE_CHECKING, Union, cast

import inspect

if TYPE_CHECKING:
    from classes.rule import Context

class EvaluationFunction:
    """
    Implements a decorator to wrap function to be used with rule classes.
    The function must return a hashable type, which is used to access the action to be taken by the rule.

    Evaluation functions can be combined using the AND, OR and NOT operators to build up more complex rules
    from simpler ones.
    The operators + or &, | and ~ are aliases for AND, OR and NOT respectively.
    e.g. 
    func1 = EvaluationFunction(lambda ctx: ctx.speed > 10)
    func2 = EvaluationFunction(lambda ctx: ctx.speed < 20)

    These statements are all equivalent:
        * EvaluationFunction(lambda ctx: 10 < ctx.speed < 20)
        * func1 + func2
        * func1 & func2
        * func1.AND(func2)
        * EvaluationFunction.AND(func1, func2)

    EvaluationFunctions also allow for more specific returns types:
        @EvaluationFunction
        def is_speeding(ctx: Context) -> Hashable:
            config = ctx.agent.config
            if config.speed > config.speed_limit+20:
                return "very fast"
            elif config.speed > config.speed_limit+5:
                return "fast"
            elif: config.speed < config.speed_limit-20:
                return "very slow"
            else:
                return "normal"

        Rule(is_speeding, action={
                                "very fast": lambda ctx: ctx.agent.config.follow_speed_limits()
                                "fast" : lambda ctx: ctx.agent.config.set_target_speed(ctx.speed_limit+5)
                                })
    """
    
    def __new__(cls, first_argument: Union[str, Callable[["Context"], Hashable]], name="EvaluationFunction"):
        if isinstance(first_argument, str):
            return partial(cls, name=first_argument) # Calling decorator with a string
        
        instance = super().__new__(cls)
        instance.__init__(first_argument, name)
        return instance
    
    def __init__(self, evaluation_function: Callable[["Context"], Hashable], name="EvaluationFunction"):
        self.evaluation_function = evaluation_function
        if name != "EvaluationFunction":
            self.name = name
        elif hasattr(evaluation_function, "__name__"):
            self.name = evaluation_function.__name__
        else:
            self.name = str(evaluation_function)
        self.actions = {}

    def __call__(self, ctx: "Context", *args, **kwargs) -> Hashable:
        result = self.evaluation_function(ctx, *args, **kwargs)
        assert isinstance(result, Hashable), f"evaluation_function must return a hashable type, not {type(result)}"
        return result
    
    def __get__(self, instance, owner): # for in class usage class.rule
        # NOTE: instance.rule is not an EvaluationFunction, it is a partial of one.
        if instance is None:
            return self # called on class
        return partial(self, instance) # NOTE: This fixes "ctx" to instance in __call__, the real "ctx" in __call__ is provided through *args

    #Helpers to extract a useful string representation of the function
    @staticmethod
    def _complete_func_to_string(func) -> str:
        func_lines = inspect.getsourcelines(func)[0]
        func_string = "".join(func_lines).strip()
        return func_string

    @staticmethod
    def _func_to_string(func):
        if not hasattr(func, "__name__"):
            return str(func)
        if func.__name__ == "<lambda>":
            return EvaluationFunction._complete_func_to_string(func)
        return func.__name__

    @property
    def __name__(self):
        return self.name

    def __str__(self):
        return self.name
    
    def __repr__(self):
        if self.name == "EvaluationFunction":
            return self.__class__.__name__ + f"({self.evaluation_function})"
        return self.__class__.__name__ + f'(name="{self.name}", evaluation_function={self.evaluation_function})'

    @classmethod
    def AND(cls, func1, func2):
        def combined_func(ctx: "Context", *args, **kwargs):
            return func1(ctx, *args, **kwargs) and func2(ctx, *args, **kwargs)
        return cls(combined_func, name=f"{func1.name}_and_{func2.name}")

    @classmethod
    def OR(cls, func1, func2):
        def combined_func(ctx: "Context", *args, **kwargs):
            return func1(ctx, *args, **kwargs) or func2(ctx, *args, **kwargs)

        return cls(combined_func, name=f"{func1.name}_or_{func2.name}")

    @classmethod
    def NOT(cls, func):
        def combined_func(ctx: "Context", *args, **kwargs):
            return not func(ctx, *args, **kwargs)

        return cls(combined_func, name=f"not_{func.name}")

    def __add__(self, other):
        return self.AND(self, other)
    
    def __and__(self, other):
        return self.AND(self, other)

    def __or__(self, other):
        return self.OR(self, other)

    def __invert__(self):
        return self.NOT(self)
    
    def register_action(self, key:Hashable=True):
        def decorator(action_function):
            if action_function.__name__ in ('action', 'actions', 'false_action'):
                raise ValueError(f"When using EvaluationFunction.add_action, the action function's name may not be in ('action', 'actions', 'false_action'), got '{action_function.__name__}'.")
            if key in self.actions:
                print("Warning: Overwriting already registered action", self.actions[key], "with key", f"'{key}'", "in", self.name)
            self.actions[key] = action_function # register action
            return action_function
        return decorator


class ActionFunction(EvaluationFunction):
    def __init__(self, action_function: Callable[["Context"], Any], name="ActionFunction"):
        super().__init__(action_function, name)

    # Overriding the NOT method isn't appropriate here since this class is for actions, not evaluations.
    # If you wish to have a NOT like functionality, it should be clearly defined what "NOT" an action means.

    def __call__(self, ctx: "Context", *args, **kwargs) -> Any:
        return self.evaluation_function(ctx, *args, **kwargs)
