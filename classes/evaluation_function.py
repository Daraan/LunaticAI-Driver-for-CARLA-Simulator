# pyright: reportInconsistentConstructor=information

import inspect
from collections import abc
from functools import partial, update_wrapper

try: # Python 3.8+
    from functools import singledispatchmethod
except ImportError:
    from launch_tools import singledispatchmethod

from typing import Callable, Any, ClassVar, Dict, Hashable, TYPE_CHECKING, Optional, Union
from typing_extensions import overload, Self, TypeAlias

if TYPE_CHECKING:
    from classes.rule import Context, Rule # circular import
    from typing import NoReturn
# NOTE: to prevent this circular import when classes.rule are imported Rule and Context are set accordingly for this module

_Callable_Any : TypeAlias = Callable[..., Any]    # type: ignore[unused-variable]
_Callable_H : TypeAlias = Callable[..., Hashable] # type: ignore[unused-variable]

class ConditionFunction:
    """
    Implements a decorator to wrap function to be used with :any:`Rule` classes.
    The function must return a hashable type, which is used to access the action to be taken 
    by the :any:`Rule.condition` function of the rule.
    
    Evaluation functions can be combined using the AND, OR and NOT operators to build up more complex rules
    from simpler ones.
    The operators :code:`+, &`, :code:`|` and :code:`~` are aliases for :code:`AND, OR` and :code:`NOT` respectively.
    e.g.  with these two functions:
    :python:`func1 = ConditionFunction(lambda ctx: ctx.speed > 10)`
    :python:`func2 = ConditionFunction(lambda ctx: ctx.speed < 20)`

    These statements are all equivalent:
        * :python:`ConditionFunction(lambda ctx: 10 < ctx.speed < 20)`
        * :python:`func1 + func2`
        * :python:`func1 & func2`
        * :python:`func1.AND(func2)`
        * :python:`ConditionFunction.AND(func1, func2)`
    
    Hint:
        ConditionFunctions also allow for more specific returns types
        
        ..  code-block:: python
        
            @ConditionFunction
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

            Rule(is_speeding, 
                 action={
                    "very fast": lambda ctx: ctx.agent.config.follow_speed_limits(), 
                    "fast" : lambda ctx: ctx.agent.config.set_target_speed(ctx.speed_limit+5) 
                 })
    Parameters:
        first_argument : A callable to be decorated or a string to be used as the name of the function.
        name : The name to represent the function. Defaults to :python:`"ConditionFunction"`.
        truthy : If True, the function will always cast the return value to a boolean value. Defaults to :code:`False`.
        use_self : If :python:`True`, the function will be treated as a method and the first argument will be the instance of the :any:`Rule` that uses this function.
            If :python:`None`, the decision depends on the signature of the function, if it has only one argument only the :any:`Context` object is passed,
            if it has two or more arguments the first argument that is passed is the instance of the :any:`Rule`.
            Use :python:`False` to not use the instance of the :any:`Rule` as the first argument.
            Defaults to :python:`None`.
            
    Returns:
        ConditionFunction | type[ConditionFunction] : 
            A :py:class:`ConditionFunction` or a partially initialized version to be used as a decorator 
            when the :code:`first_argument` is not a callable.

    """
    
    actions: Dict[Hashable, Callable[["Union[Context, Rule]"], Any]] = {}
    """
    Mapping of return values to actions to be executed.
    If this dictionary is not empty it will be used as the :py:attr:`Rule.actions` dictionary.
    """
    
    _INVALID_NAMES: "ClassVar[set[str]]" = {'action', 'actions', 'false_action'}
    """Forbidden names for action functions."""
    
    @overload
    def __new__(cls, first_argument: Union[None, str], name:str="ConditionFunction", *, truthy:bool=False, use_self: Optional[bool]=None) -> "type[Self]":
        ...
        
    @overload
    def __new__(cls, first_argument: Callable[..., Hashable], name:str="ConditionFunction", *, truthy:bool=False, use_self: Optional[bool]=None) -> Self:
        ...
    
    def __new__(cls, first_argument: Optional[Union[str, Callable[["Context"], Hashable]]]=None, name:str="ConditionFunction", *, truthy:bool=False, use_self: Optional[bool]=None) -> Union["type[Self]", Self]:
        # example usage: @ConditionFunction("name")
        if isinstance(first_argument, str):
            # Calling decorator with a string
            return partial(cls, name=first_argument, truthy=truthy, use_self=use_self) # pyright: ignore[reportReturnType], duck type
        # example_usage: @ConditionFunction(name="name") or @ConditionFunction(truthy=True)
        if first_argument is None:
            return partial(cls, name=name, truthy=truthy, use_self=use_self)           # pyright: ignore[reportReturnType], duck type
        assert isinstance(first_argument, Callable), f"First argument must be a callable, not {type(first_argument)}"
        # @ConditionFunction or ConditionFunction(function)
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, evaluation_function: Callable[["Context"], Hashable], name:str="ConditionFunction", *, truthy:bool=False, use_self: Optional[bool]=None):
        update_wrapper(self, evaluation_function, assigned=("__qualname__", "__module__", "__annotations__", "__doc__"))
        self.evaluation_function = evaluation_function
        self.truthy = truthy
        if name != "ConditionFunction":
            self.name = name
        elif hasattr(evaluation_function, "__name__"):
            self.name = evaluation_function.__name__
        else:
            self.name = str(evaluation_function)
        self.use_self = use_self
        self.actions = self.actions.copy()

    def __call__(self, ctx: "Rule | Context", *args: Any, **kwargs: Any) -> Hashable:
        """
        Note:
            To handle the method vs. function difference depending on __get__ 
            `ctx` can be either a Context (condition as function) or a Rule (condition as method),
            In the method case the real Context object is args[0]!
        """
        try:
            rule_result = self.evaluation_function(ctx, *args, **kwargs)    # type: ignore
        except Exception:
            print(f"ERROR: in Rule {self.name} with function {self.evaluation_function}")
            raise
        # Handle function vs. method
        if not isinstance(ctx, Context):
            ctx = args[0]                # type: ignore
            assert isinstance(ctx, Context), f"This should not happen: In the method case the argument must be a Context object, not {type(ctx)}"
        ctx.rule_result = rule_result
        if self.truthy:
            return bool(rule_result)
        assert isinstance(rule_result, Hashable), f"evaluation_function must return a hashable type, not {type(rule_result)}"
        return rule_result
    
    def __get__(self, instance: "Optional[Rule]", objtype:Optional["type[Rule]"]=None): # pylint: disable=unused-argument
        """
        :term:`Descriptor Protocol <descriptor>`, for in class usage like Rule.condition
        """
        # NOTE: instance.condition is not an ConditionFunction, it is a partial of one.
        if instance is None:
            return self # called on class Rule.condition
        return partial(self, instance) # NOTE: This fixes "ctx" to instance in __call__, the real "ctx" in __call__ is provided through *args
    
    def copy(self, copy_actions:bool=False):
        """
        Copies the class by creating a new instance.
        
        Parameters:
            copy_actions : If :python:`True`, the :py:attr:`actions` dictionary is copied as well. Defaults to :python:`False`.
                
                Warning:
                    Be aware that the actions themselves are not copied; they are identical and shared.
        """
        instance = super().__new__(self.__class__)
        self.__class__.__init__(instance, self.evaluation_function, self.name, truthy=self.truthy, use_self=self.use_self)
        if copy_actions:
            instance.actions = self.actions.copy()
        return instance

    #Helpers to extract a useful string representation of the function
    @staticmethod
    def _complete_func_to_string(func: Callable[..., Any]) -> str:
        func_lines = inspect.getsourcelines(func)[0]
        func_string = "".join(func_lines).strip()
        return func_string

    @staticmethod
    def _func_to_string(func : Callable[..., Any]) -> str:
        if not hasattr(func, "__name__"):
            return str(func)
        if func.__name__ == "<lambda>":
            return ConditionFunction._complete_func_to_string(func)
        return func.__name__
    
    def _check_action(self, action_function: Callable[["Union[Context, Rule]"], Any], 
                      key: Hashable, **kwargs: Any) -> Callable[["Context | Rule"], Any]:
        if action_function.__name__ in ConditionFunction._INVALID_NAMES:
            raise ValueError(f"When using ConditionFunction.add_action, the action function's name may not be in {ConditionFunction._INVALID_NAMES}, got '{action_function.__name__}'.")
        if key in self.actions:
            print("Warning: Overwriting already registered action", self.actions[key], "with key", f"'{key}'", "in", self.name)
        if kwargs:
            # TODO: # CRITICAL: are args problematic?
            action_function = partial(action_function, **kwargs)
        return action_function
    
    @singledispatchmethod
    def register_action(self, key: Hashable=True, **kwargs: Any):
        """
        Add an action to be executed when the condition function returns a specific value.
        
        This function can be used as a decorator or as a method:
        
        .. code-block:: python
        
            # As decorator
            @ConditionFunction
            def is_speeding(ctx: Context) -> Literal["very fast", "fast", "normal", "slow"]:
                ...
            
            @is_speeding.register_action(key="very fast")
            def very_fast_action(ctx: Context):
                ctx.agent.set_target_speed(ctx.config.target_speed-5)
            
            # Or functionally
            def fast_action(ctx: Context):
                ctx.agent.set_target_speed(ctx.config.target_speed+1)
                
            is_speeding.register_action(key="fast", fast_action)
        
        Parameters:
            key: If the condition function returns this value, this action will be executed. Defaults to :python:`True`.
            kwargs : Additional keyword arguments to be passed to the action function when it is executed.
            
        Note:
            Only one action is allowed per key. If an action is already registered for the key, it will be overwritten.
        """
        def decorator(action_function: Callable[["Union[Context, Rule]"], Any]):
            action_function = self._check_action(action_function, key, **kwargs)
            self.actions[key] = action_function # register action
            return action_function
        return decorator
    
    @register_action.register(abc.Callable)
    def _register_action_directly(self, action_function: Callable[["Union[Context, Rule]"], Any], key: Hashable=True, **kwargs: Any):
        # Functional use
        action_function = self._check_action(action_function, key, **kwargs)
        self.actions[key] = action_function # register action
        
    
    # ----------------------    
    
    if not TYPE_CHECKING:
        # This is shadowed as pyright interprets self.__class__.__name__ as this function
        @property
        def __name__(self) -> str: # noqa
            """
            Returns the name of the function.
            """
            return self.name
    else:
        __name__ : str

    def __str__(self):
        return self.name
    
    def __repr__(self) -> str:        
        if self.name == "ConditionFunction":
            s = self.__class__.__name__ + f"({self.evaluation_function}"
        else:
            s = self.__class__.__name__ + f'(name="{self.name}", evaluation_function={self.evaluation_function}'
        if self.truthy:
            s += ", truthy=True"
        s += ")"
        return s

    @classmethod
    def AND(cls, func1 : "ConditionFunction", func2 : "ConditionFunction") -> "ConditionFunction":
        """Combine two functions to return True if both return True."""
        def combined_func(ctx: "Context", *args: Any, **kwargs: Any):
            return func1(ctx, *args, **kwargs) and func2(ctx, *args, **kwargs)
        return cls(combined_func, name=f"{func1.name}_and_{func2.name}")

    @classmethod
    def OR(cls, func1 : "ConditionFunction", func2 : "ConditionFunction") -> "ConditionFunction":
        """Combine two functions to return True if either returns True."""
        def combined_func(ctx: "Context", *args: Any, **kwargs: Any):
            return func1(ctx, *args, **kwargs) or func2(ctx, *args, **kwargs)

        return cls(combined_func, name=f"{func1.name}_or_{func2.name}")

    @classmethod
    def NOT(cls, func: "ConditionFunction") -> "ConditionFunction":
        """Invert the return value of a function."""
        def combined_func(ctx: "Context", *args : Any, **kwargs: Any):
            return not func(ctx, *args, **kwargs)

        return cls(combined_func, name=f"not_{func.name}")

    def __add__(self, other: "ConditionFunction") -> "ConditionFunction":
        """Combine with another function using :py:meth:`AND`."""
        return self.AND(self, other)
    
    def __and__(self, other: "ConditionFunction") -> "ConditionFunction":
        """Combine with another function using :py:meth:`AND`."""
        return self.AND(self, other)

    def __or__(self, other: "ConditionFunction") -> "ConditionFunction":
        """Combine with another function using :py:meth:`OR`."""
        return self.OR(self, other)

    def __invert__(self) -> "ConditionFunction":
        """
        Invert the return value of the function.
        """
        return self.NOT(self)


def TruthyConditionFunction(func: Callable[..., Hashable]) -> ConditionFunction:
    """
    Allows a condition to return any value, but will be converted to a boolean.
    
    Note:
        This is equivalent to :python:`ConditionFunction(func, truthy=True)`.
        
    .. deprecated:: x
    
    :meta private:
    """
    return ConditionFunction(func, truthy=True)
    
class ActionFunction(ConditionFunction):
    """
    A decorator that can be used with :any:`Rule.action`. It is nearly equivalent to :any:`ConditionFunction`, 
    only calling the function is more simple, i.e. does not assert a Hashable return type.
    
    .. deprecated:: x
    
    :meta private:
    """
    
    def __init__(self, action_function: Callable[["Context"], Any], name: str="ActionFunction", *, use_self: Optional[bool]=None):
        super().__init__(action_function, name, use_self=use_self)

    @classmethod
    def NOT(cls, func : Any) -> "NoReturn":  # pylint: disable=unused-argument
        """
        Raises:
            NotImplementedError: NOT is not implemented for ActionFunction.
        """
        raise NotImplementedError("NOT is not implemented for ActionFunction")

    def __call__(self, ctx: "Context", *args: Any, **kwargs: Any) -> Any:
        return self.evaluation_function(ctx, *args, **kwargs)

