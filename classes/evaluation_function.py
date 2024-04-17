from functools import partial, update_wrapper, wraps

try: # Python 3.8+
    from functools import singledispatchmethod
except ImportError:
    from launch_tools import singledispatchmethod


from typing import Callable, Any, ClassVar, Dict, Hashable, TYPE_CHECKING, Optional, Union
from collections import abc

import inspect

if TYPE_CHECKING:
    from classes.rule import Context, Rule # circular import
# NOTE: to prevent this circular import when classes.rule are imported Rule and Context are set accordingly for this module


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
    
    actions: ClassVar[Dict[Hashable, Callable[["Union[Context, Rule]"], Any]]] = {}
    
    def __new__(cls, first_argument: Optional[Union[str, Callable[["Context"], Hashable]]]=None, name="EvaluationFunction", *, truthy=False, use_self=None) -> "type[EvaluationFunction]":
        # @EvaluationFunction("name")
        if isinstance(first_argument, str):
            return partial(cls, name=first_argument, truthy=truthy, use_self=use_self) # Calling decorator with a string
        # @EvaluationFunction(name="name") or @EvaluationFunction(truthy=True)
        if first_argument is None:
            return partial(cls, name=name, truthy=truthy, use_self=use_self)
        assert isinstance(first_argument, Callable), f"First argument must be a callable, not {type(first_argument)}"
        # @EvaluationFunction or EvaluationFunction(function)
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, evaluation_function: Callable[["Context"], Hashable], name="EvaluationFunction", *, truthy=False, use_self: Optional[bool]=None):
        update_wrapper(self, evaluation_function, assigned=("__qualname__", "__module__", "__annotations__", "__doc__"))
        self.evaluation_function = evaluation_function
        self.truthy = truthy
        if name != "EvaluationFunction":
            self.name = name
        elif hasattr(evaluation_function, "__name__"):
            self.name = evaluation_function.__name__
        else:
            self.name = str(evaluation_function)
        self.use_self = use_self
        self.actions = self.actions.copy()

    def __call__(self, ctx: "Context | Rule", *args, **kwargs) -> Hashable:
        """
        NOTE: CRITICAL: 
        To handle the method vs. function difference depending on __get__ 
        `ctx` can be either a Context (rule as function) or a Rule (rule as method),
        In the method case the real Context object is args[0]
        """
        try:
            rule_result = self.evaluation_function(ctx, *args, **kwargs)
        except Exception:
            print(f"ERROR: in rule {self.name} with function {self.evaluation_function}")
            raise
        # Handle function vs. method
        if not isinstance(ctx, Context):
            ctx = args[0]
            assert isinstance(ctx, Context), f"This should not happen: In the method case the argument must be a Context object, not {type(ctx)}"
        ctx.rule_result = rule_result
        if self.truthy:
            return bool(rule_result)
        assert isinstance(rule_result, Hashable), f"evaluation_function must return a hashable type, not {type(rule_result)}"
        return rule_result
    
    def __get__(self, instance: "Optional[Rule]", owner): # pylint: disable=unused-argument # for in class usage like Rule.rule
        # NOTE: instance.rule is not an EvaluationFunction, it is a partial of one.
        if instance is None:
            return self # called on class
        return partial(self, instance) # NOTE: This fixes "ctx" to instance in __call__, the real "ctx" in __call__ is provided through *args
    
    def copy(self, copy_actions=False):
        """
        Copies the class by creating a new instance.
        
        If copy_actions is True, the actions dictionary is copied as well. 
        Be aware that the actions themselves are not copied they identical and shared.
        """
        instance = super().__new__(self.__class__)
        self.__class__.__init__(instance, self.evaluation_function, self.name, truthy=self.truthy, use_self=self.use_self)
        if copy_actions:
            instance.actions = self.actions.copy()
        return instance

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
            s = self.__class__.__name__ + f"({self.evaluation_function}"
        else:
            s = self.__class__.__name__ + f'(name="{self.name}", evaluation_function={self.evaluation_function}'
        if self.truthy:
            s += ", truthy=True"
        s += ")"
        return s

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
    
    _INVALID_NAMES: "ClassVar[set[str]]" = {'action', 'actions', 'false_action'}
    
    def _check_action(self, action_function: Callable[["Union[Context, Rule]"], Any], key, **kwargs):
        if action_function.__name__ in EvaluationFunction._INVALID_NAMES:
            raise ValueError(f"When using EvaluationFunction.add_action, the action function's name may not be in {EvaluationFunction._INVALID_NAMES}, got '{action_function.__name__}'.")
        if key in self.actions:
            print("Warning: Overwriting already registered action", self.actions[key], "with key", f"'{key}'", "in", self.name)
        if kwargs:
            # TODO: # CRITICAL: are args problematic? 
            action_function = partial(action_function, **kwargs)
        return action_function
    
    @singledispatchmethod
    def register_action(self, key: Hashable=True, **kwargs):
        def decorator(action_function):
            action_function = self._check_action(action_function, key, **kwargs)
            self.actions[key] = action_function # register action
            return action_function
        return decorator
    
    @register_action.register(abc.Callable)
    def _register_action_directly(self, action_function: Callable[["Union[Context, Rule]"], Any], key: Hashable=True, **kwargs):
        action_function = self._check_action(action_function, key, **kwargs)
        self.actions[key] = action_function # register action

def TruthyEvaluationFunction(func: Callable) -> EvaluationFunction:
    """
    Allows a rule to return any value, but will be converted to a boolean.
    
    TODO: Still does "store the result". Add a attribute to ctx that stores the last rule result.
    
    todo (low priority): instead of extra function make this a parameter of EvaluationFunction
    """
    return EvaluationFunction(func, truthy=True)
    
    @EvaluationFunction
    @wraps(func)
    def wrapper(self: "Rule", ctx : "Context"): 
        result = func(self, ctx) # TODO: not method vs. function aware
        ctx.rule_result = result # TODO: add to context
        return bool(result)
    return wrapper

class ActionFunction(EvaluationFunction):
    def __init__(self, action_function: Callable[["Context"], Any], name="ActionFunction"):
        super().__init__(action_function, name)

    # Overriding the NOT method isn't appropriate here since this class is for actions, not evaluations.
    # If you wish to have a NOT like functionality, it should be clearly defined what "NOT" an action means.

    def __call__(self, ctx: "Context", *args, **kwargs) -> Any:
        return self.evaluation_function(ctx, *args, **kwargs)

