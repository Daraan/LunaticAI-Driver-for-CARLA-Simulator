

# pyright: strict
# pyright: reportInconsistentConstructor=information
# pyright: reportGeneralTypeIssues=warning
# pyright: reportAttributeAccessIssue=warning

from __future__ import annotations

import sys
import inspect
from collections import abc
from functools import partial, update_wrapper, wraps

from launch_tools import singledispatchmethod

import typing
from typing import Callable, Any, ClassVar, Dict, Generic, Hashable, TYPE_CHECKING, Optional, Union, TypeVar
from typing_extensions import overload, Self, ParamSpec, Concatenate, TypeAlias, TypeGuard, Never

from classes.constants import READTHEDOCS

if TYPE_CHECKING:
    from typing import NoReturn
    # NOTE: to prevent this circular import when classes.rule are imported Rule and Context are set accordingly for this module
    from classes.rule import Context, Rule # circular import
    from functools import _Wrapped  # noqa # type: ignore


_T = TypeVar("_T")
_H = TypeVar("_H", bound=Hashable)   # Free
_CH = TypeVar("_CH", bound=Hashable) # Generic of ConditionFunction

_P = ParamSpec("_P")   # Free, e.g. for action function.
_CP = ParamSpec("_CP") # Generic of ConditionFunction

_Rule = TypeVar("_Rule", bound="Rule")

_ConditionWithRule : TypeAlias = Callable[Concatenate[_Rule, "Context", _CP], _CH]
_ConditionOnlyCtx : TypeAlias = Callable[Concatenate["Context", _CP], _CH]
_ConditionType : TypeAlias = Union[_ConditionWithRule[_Rule, _CP, _CH], _ConditionOnlyCtx[_CP, _CH]]
_AnyCondition : TypeAlias = Callable[_CP, _CH]  # noqa 

_ActionWithRule : TypeAlias = Callable[Concatenate[_Rule, "Context", _P], _T]
_ActionOnlyCtx : TypeAlias = Callable[Concatenate["Context", _P], _T]
_ActionType : TypeAlias = Union[_ActionWithRule[_Rule, _P, _T], _ActionOnlyCtx[_P, _T]]
_AnyAction : TypeAlias = Callable[_P, _T]

# Non Generic Type Alias
# cannot use ... in <3.9 for Generic types
if not TYPE_CHECKING and sys.version_info < (3, 10):
    __dummy = ParamSpec("__dummy")
    _ActionTypeAlias = _ActionType["Rule", __dummy, Any]
    _ConditionTypeAlias = _ConditionType["Rule", __dummy, Hashable]
    _ConditionTypeAlias.__parameters__ = _ConditionTypeAlias.__args__[0].__parameters__ = \
        _ConditionTypeAlias.__args__[1].__parameters__ = _ActionTypeAlias.__parameters__ = \
        _ActionTypeAlias.__args__[0].__parameters__ = _ActionTypeAlias.__args__[1].__parameters__ = ()
    _ConditionTypeAlias.__args__[0].__args__ = tuple(p for p in _ConditionTypeAlias.__args__[0].__args__ if p is not __dummy)
    _ConditionTypeAlias.__args__[1].__args__ = tuple(p for p in _ConditionTypeAlias.__args__[1].__args__ if p is not __dummy)
    _ActionTypeAlias.__args__[0].__args__ = tuple(p for p in _ActionTypeAlias.__args__[0].__args__ if p is not __dummy)
    _ActionTypeAlias.__args__[1].__args__ = tuple(p for p in _ActionTypeAlias.__args__[1].__args__ if p is not __dummy)
else:
    _ActionTypeAlias = _ActionType["Rule", [...], Any]
    _ConditionTypeAlias = _ConditionType["Rule", [...], Hashable]

if TYPE_CHECKING:
    # Condition.functions can be might be wrapped.
    _W = Union[_Wrapped[Concatenate["Rule", "Context", ...], Any, Concatenate["Rule", "Context", ...], Any], 
                _Wrapped[Concatenate["Context", ...], Any, Concatenate["Context", ...], Any]]
    _ActionsDictValues = Union[_ActionTypeAlias, _W]
else:
    _ActionsDictValues = _ActionTypeAlias



class ConditionFunction(Generic[_Rule, _CP, _CH]):
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
        
        Example:
        
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
        first_argument : 
            If :code:`None` or a string, the class will create a :term:`decorator`
            that expects a callable as the first argument.
            If a string is passed it substitutes as the **name** argument.
            Otherwise a callable is expected like in the snippet used above.
        name : The name to represent the function. Defaults to :python:`"ConditionFunction"`.
        truthy : If True, the function will always cast the return value to a boolean value. Defaults to :code:`False`.
        use_self : If :python:`True`, the function will be treated as a method and the first argument will be the instance of the :py:class:`.Rule` that uses this function.
            If :code:`None`, the decision depends on the signature of the function, if it has only one argument only the :py:class:`.Context` object is passed,
            if it has two or more arguments the first argument that is passed is the instance of the :py:class:`.Rule`.
            Use :code:`False` to not use the instance of the :py:class:`.Rule` as the first argument.
            Defaults to :code:`None`.
            
    Returns:
        ConditionFunction | partial[type[ConditionFunction]] : 
            A :py:class:`ConditionFunction` or a partially initialized version to be used as a decorator 
            when the **first_argument** is not a callable.
            
    Generics:
        - _Rule : Generic :py:class:`.Rule` type.
        - _CP : :py:class:`typing.ParamSpec` of the passed :py:attr:`evaluation_function`.
        - _H : The :term:`Hashable` return type of the :py:attr:`evaluation_function`.
    """
    
    actions: Dict[Hashable, _ActionsDictValues] = {}
    """
    Mapping of return values to actions to be executed.
    If this dictionary is not empty it will be used as the :py:attr:`.Rule.actions` dictionary.
    """
    
    _INVALID_NAMES: "ClassVar[set[str]]" = {'action', 'actions', 'false_action'}
    """Forbidden names for action functions."""
    
    @overload
    def __new__(cls, first_argument: Optional[str]=None, name:str="ConditionFunction", *, 
                truthy:bool=False, use_self: Optional[bool]=None) -> "partial[type[Self]]":
        ...
        
    @overload
    def __new__(cls, first_argument: _ConditionType[_Rule, _CP, _CH], name:str="ConditionFunction", *, 
                truthy:bool=False, use_self: Optional[bool]=None) -> Self:
        ...
    
    def __new__(cls, 
                first_argument: Optional[Union[str, _ConditionType[_Rule, _CP, _CH]]]=None,
                name:str="ConditionFunction", 
                *, 
                truthy: bool=False, 
                use_self: Optional[bool]=None) -> partial[type[Self]] | Self:
        # example usage: @ConditionFunction("name")
        if isinstance(first_argument, str):
            # Calling decorator with a string @ConditionFunction("name")
            assert name == "ConditionFunction", "The `name` argument must be the default."
            return partial(cls, name=first_argument, truthy=truthy, use_self=use_self) # pyright: ignore[reportReturnType], duck type
        # example_usage: @ConditionFunction(name="name") or @ConditionFunction(truthy=True)
        if first_argument is None:
            return partial(cls, name=name, truthy=truthy, use_self=use_self)           # pyright: ignore[reportReturnType], duck type
        assert isinstance(first_argument, Callable), f"First argument must be a callable, not {type(first_argument)}"
        # @ConditionFunction or ConditionFunction(function)
        instance = super().__new__(cls)
        return instance
    
    evaluation_function : _ConditionType[_Rule, _CP, _CH]
    """
    The function that is wrapped by the :py:class:`ConditionFunction`.
    Uses the generic type hints :py:obj:`_Rule`, :py:obj:`_CP`, :py:obj:`_CH` of the class.
    """
    
    if READTHEDOCS and not TYPE_CHECKING:
        __new__.__annotations__["first_argument"] = Optional["name" | _ConditionTypeAlias]
        evaluation_function : typing.Callable[[_Rule, "Context", _CP], _CH] | typing.Callable[["Context", _CP], _CH]
    
    def __init__(self, 
                 evaluation_function: _ConditionType[_Rule, _CP, _CH], 
                 name:str="ConditionFunction", 
                 *, 
                 truthy: bool=False, 
                 use_self: Optional[bool]=None):
        update_wrapper(self, evaluation_function, assigned=("__qualname__", "__module__", "__annotations__", "__doc__"))
        self.evaluation_function = evaluation_function
        self.truthy: bool = truthy
        if name != "ConditionFunction":
            self.name = name
        elif hasattr(evaluation_function, "__name__"):
            self.name = evaluation_function.__name__
        else:
            self.name = str(evaluation_function)
        self.use_self: bool | None = use_self
        self.actions = self.actions.copy()

    @overload
    def __call__(self, ctx: "Rule", arg1: "Context", *args:_CP.args, **kwargs:_CP.kwargs) -> _CH: ...
    
    @overload
    def __call__(self, ctx: "Context", *args:_CP.args, **kwargs:_CP.kwargs) -> _CH: ...
    
    @overload
    def __call__(self, ctx: "Rule | Context", *args:_CP.args, **kwargs:_CP.kwargs) -> _CH: ...
    
    def __call__(self, ctx: "Rule | Context", *args:_CP.args, **kwargs:_CP.kwargs) -> _CH: # pyright: ignore[reportInconsistentOverload]
        """
        Note:
            To handle the method vs. function difference depending on __get__ 
            `ctx` can be either a Context (condition as function) or a Rule (condition as method),
            In the method case the real Context object is args[0]!
        """
        try:
            rule_result = self.evaluation_function(ctx, *args, **kwargs) # type: ignore[arg-type]
        except Exception:
            print(f"ERROR: in Rule {self.name} with function {self.evaluation_function}")
            raise
        # Handle function vs. method
        if not isinstance(ctx, Context):
            ctx = args[0]                # type: ignore
            assert isinstance(ctx, Context), f"This should not happen: In the method case the argument must be a Context object, not {type(ctx)}"
        ctx.rule_result = rule_result
        if self.truthy:
            return bool(rule_result)  # type: ignore
        assert isinstance(rule_result, Hashable), f"evaluation_function must return a hashable type, not {type(rule_result)}" # type: ignore
        return rule_result
    
    def __get__(self, instance: "Optional[Rule]", objtype: Optional["type[Rule]"]=None) -> "Self | partial[_CH]": # noqa
        """
        :term:`Descriptor Protocol <descriptor>`, for in class usage like Rule.condition
        """
        # NOTE: instance.condition is not an ConditionFunction, it is a partial of one.
        if instance is None:
            return self # called on class Rule.condition
        return partial(self, instance) # NOTE: This fixes "ctx" to instance in __call__, the real "ctx" in __call__ is provided through *args
    
    def copy(self, copy_actions: bool=False):
        """
        Copies the class by creating a new instance.
        
        Parameters:
            copy_actions: If :python:`True`, the :py:attr:`.ConditionFunction.actions` 
                dictionary is copied as well. 
                Defaults to :code:`False`.
                    
        Returns: 
            ConditionFunction: A new instance, with the same :python:`__init__` arguments.
            
        Warning:
            Be aware that when using **copy_actions** the actions themselves are not copied; 
            they are identical and shared.
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
    
    @staticmethod
    def _is_partial_action(action_function: Callable[_P, _T]) -> TypeGuard["partial[_T] | Callable[_P, _T]"]:
        return isinstance(action_function, partial)
        
    def _check_action(self, action_function: _AnyAction[_P, _T],
                      key: Hashable,
                      **preset_kwargs: _P.kwargs
                      ) -> "_AnyAction[_P, _T] | _Wrapped[_P, _T, _P, _T]": 
        """
        Checks if an action has an invalid name, a key is already registered.
        If kwargs are passed these will be fixed for the returned action.
        """
        if action_function.__name__ in ConditionFunction._INVALID_NAMES:
            raise ValueError(f"When using ConditionFunction.add_action, the action function's name "
                             "may not be in {ConditionFunction._INVALID_NAMES}, "
                             "got '{action_function.__name__}'.")
        if key in self.actions:
            print("Warning: Overwriting already registered action", self.actions[key], "with key", f"'{key}'", "in", self.name)
        if not preset_kwargs:
            return action_function # return original function
        
        # Preset kwargs.
        @wraps(action_function)
        def action_function_with_kwargs(*args: _P.args, **kwargs: _P.kwargs) -> _T:
             # inserts args when called and kwargs from check action
             # allows overrides
            return action_function(*args, **preset_kwargs, **kwargs) # type: ignore
        return action_function_with_kwargs
    
    
    @singledispatchmethod
    def register_action(self, key: typing.Hashable=True, **kwargs: _P.kwargs) \
            -> typing.Callable[[_ActionType[_Rule, _P, _T]], _ActionType[_Rule, _P, _T]]:
        """
        Add an action to be executed when the condition function returns a specific value.
        
        This function can be used as a decorator or as a method:
        
        .. code-block:: python
        
            # As decorator
            @ConditionFunction
            def is_speeding(ctx: Context) -> Literal["very fast", "fast", "normal", "slow", True]:
                ...
            
            @is_speeding.register_action(key="very fast")
            # or
            @is_speeding.register_action # default key is True
            def very_fast_action(ctx: Context):
                ctx.agent.set_target_speed(ctx.config.target_speed-5)
            
            # Or as function
            def fast_action(ctx: Context):
                ctx.agent.set_target_speed(ctx.config.target_speed+1)
                
            is_speeding.register_action(key="fast", fast_action)
        
        Parameters:
            key: If the condition function returns this value, this action will be executed. Defaults to :python:`True`.
            kwargs : Additional keyword arguments to be passed to the action function when it is executed.
            action_function: The action to be executed.
            
        Returns:
                typing.Callable[[Rule, Context, ...], typing.Any] | typing.Callable[[Context, ...], typing.Any] : The decorated action function.
            
        Note:
            Only one action is allowed per key. If an action is already registered for the key, it will be overwritten.
        """
        def decorator(action_function: _ActionType[_Rule, _P, _T]) -> _ActionType[_Rule, _P, _T]:
            checked_action = self._check_action(action_function, key, **kwargs) # type: ignore[arg-type]
            self.actions[key] = checked_action # register action # type: ignore
            return checked_action
        return decorator
    
    @register_action.register(abc.Callable) # type: ignore
    def _register_action_directly(self, action_function: _ActionTypeAlias, key: Hashable=True, **kwargs: _P.kwargs) -> _ActionTypeAlias:
        """
        # Case 1
        @register_action # key is True
        def action_function(ctx: Context):
            ...
            
        # Case 2
        register_action(action_function, key="very fast", **action_function_kwargs)
        """
        checked_action = self._check_action(action_function, key, **kwargs) # type: ignore[arg-type]
        # Case 1 and 2 (without kwargs): checked_action is the action function, else wrapped.
        self.actions[key] = checked_action # register action # type: ignore
        return checked_action
    
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
    def AND(cls, func1 : "ConditionFunction[_Rule, _CP, _CH]", func2 : "ConditionFunction[_Rule, _CP, _H]") -> "ConditionFunction[_Rule, _CP, _CH | _H]":
        """Combine two functions with :python:`and`, i.e. to return True if both return True."""
        # NOTE: arguments are, lost. For type hints need to make ConditionFunction generic
        def combined_func(ctx: "Context", *args: _CP.args, **kwargs: _CP.kwargs):
            return func1(ctx, *args, **kwargs) and func2(ctx, *args, **kwargs)
        return cls(combined_func, name=f"{func1.name}_and_{func2.name}") # type: ignore

    @classmethod
    def OR(cls, func1 : "ConditionFunction[_Rule, _CP, _CH]", func2 : "ConditionFunction[_Rule, _CP, _H]") -> "ConditionFunction[_Rule, _CP, _CH | _H]":
        """Combine two functions to return True if either returns True."""
        def combined_func(ctx: "Context", *args: _CP.args, **kwargs: _CP.kwargs):
            return func1(ctx, *args, **kwargs) or func2(ctx, *args, **kwargs)

        return cls(combined_func, name=f"{func1.name}_or_{func2.name}")  # type: ignore

    @classmethod
    def NOT(cls, func: "ConditionFunction[_Rule, _CP, _CH]") -> "ConditionFunction[_Rule, _CP, bool]":
        """Invert the return value of a function."""
        def combined_func(ctx: "Context | Rule", *args: _CP.args, **kwargs: _CP.kwargs):
            return not func(ctx, *args, **kwargs)
        return cls(combined_func, name=f"not_{func.name}") # type: ignore

    def __add__(self, other: "ConditionFunction[_Rule, _CP, _H]") -> "ConditionFunction[_Rule, _CP, _CH | _H]":
        """Combine with another function using :py:meth:`AND`."""
        return self.AND(self, other)
    
    def __and__(self, other: "ConditionFunction[_Rule, _CP, _H]") -> "ConditionFunction[_Rule, _CP, _CH | _H]":
        """Combine with another function using :py:meth:`AND`."""
        return self.AND(self, other)

    def __or__(self, other: "ConditionFunction[_Rule, _CP, _H]") -> "ConditionFunction[_Rule, _CP, _CH | _H]":
        """Combine with another function using :py:meth:`OR`."""
        return self.OR(self, other)

    def __invert__(self) -> "ConditionFunction[_Rule, _CP, bool]":
        """
        Invert the return value of the function.
        """
        return self.NOT(self)


    
class ActionFunction(ConditionFunction[_Rule, _P, _T]):
    """
    A decorator that can be used with :any:`Rule.action`. It is nearly equivalent to :any:`ConditionFunction`, 
    only calling the function is more simple, i.e. does not assert a Hashable return type.
    
    .. deprecated::
        Will likely be removed as no strong use case.
    
    :meta private:
    """
    
    def __init__(self, action_function: _ActionType[_Rule, _P, _T], name: str="ActionFunction", *, use_self: Optional[bool]=None):
        super().__init__(action_function, name, use_self=use_self)

    @classmethod
    def NOT(cls, _ : Never) -> "NoReturn":  # type: ignore
        """
        Raises:
            NotImplementedError: NOT is not implemented for ActionFunction.
        """
        raise NotImplementedError("NOT is not implemented for ActionFunction")

    def __call__(self, ctx: "Rule | Context", *args: _P.args, **kwargs: _P.kwargs) -> _T:
        return self.evaluation_function(ctx, *args, **kwargs)  # type: ignore[arg-type]

