# pyright: strict
# pyright: reportIndexIssue=information, reportCallIssue=information
# pyright: reportGeneralTypeIssues=warning
# pyright: reportUnusedFunction=information, reportUnusedImport=information
# pyright: reportUnnecessaryIsInstance=false, reportUnnecessaryComparison=false
# pyright: reportPrivateUsage=none

from __future__ import annotations

import inspect

import random
from collections.abc import Mapping
from dataclasses import is_dataclass
from functools import partial, update_wrapper, wraps
from inspect import isclass
from itertools import accumulate
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Container,
    Dict,
    Hashable,
    Iterable,
    List,
    NoReturn,
    Optional,
    Set,
    TypeVar,
    Union,
    cast,
)
from weakref import CallableProxyType, WeakSet, proxy

import pygame
from omegaconf import DictConfig, OmegaConf
from typing_extensions import (
    Annotated,
    Concatenate,
    Literal,
    NotRequired,
    ParamSpec,
    Required,
    Self,
    TypedDict,
    Unpack,
    overload,
)

from agents.tools.logs import logger
from classes.constants import READTHEDOCS, Hazard, HazardSeverity, Phase, RulePriority, RuleResult
from classes.evaluation_function import ConditionFunction
from classes.exceptions import DoNotEvaluateChildRules, UnblockRuleException
from classes.worldmodel import GameFramework
from classes.information_manager import InformationManager
from launch_tools import CarlaDataProvider, singledispatchmethod

if TYPE_CHECKING:
    import carla
    from classes.type_protocols import CallableAction, CallableActionT, ConditionFunctionLike, ConditionFunctionLikeT
    from agents.lunatic_agent import LunaticAgent
    from agents.tools.config_creation import ContextSettings, LiveInfo, RuleConfig
    # NOTE: gameframework.py adds GameFramework to this module's variables
    # at this position it would be a circular import

_T = TypeVar("_T")
_P = ParamSpec("_P")
_Rule = TypeVar("_Rule", bound="Rule")


class Context(CarlaDataProvider):
    """
    Object to be passed as the first argument (instead of self) to rules, actions and evaluation functions.
    
    The :py:class:`Context` class derives from the scenario runner's :py:class:`CarlaDataProvider` to allow access to the world, map, etc.
    
    Tip:
        There is normally no need to initialize the context object manually.
        Its recommended to initialize the context object with :py:meth:`.LunaticAgent._make_context`.
    """
    
    agent: "LunaticAgent"
    """Backreference to the agent."""
    
    config: "ContextSettings"
    """A copy of the agents config. Overwritten by the condition's settings."""
    
    evaluation_results: dict[Phase, Hashable]  # ambiguous wording, which result? here evaluation result
    """
    Stores the result from the :py:meth:`Rule.condition` of the last rule that was evaluated in a phase.
    
    .. deprecated:: in consideration
    """
        
    action_results: dict[Phase, Any]
    """
    Stores the result from the :py:meth:`action` of the last rule that was applicable in a phase.
    
    .. deprecated:: in consideration
    """
    
    _control: Optional[carla.VehicleControl]
    """
    Current control the agent should use.
    
    Accessible from the :py:attr:`control` property.
    """
    
    prior_result: Optional[Any]  # TODO: maybe rename
    """Result of the current phase."""
    
    phase_results: dict[Phase, Any]
    """
    Stores the results of the phases the agent has been in.
    By default the keys are set to :py:attr:`Context.PHASE_NOT_EXECUTED`.
    """
    
    last_context: Optional["Context"]
    """The context object of the last tick. Used to access the last phase's results."""
    
    second_pass: Optional[bool] = None
    """
    Whether or not the run_step function performs a second pass, i.e.
    after the route has been replanned.
    
    Warning:
        The correctness should *not* be assumed.
        The user is responsible for setting this value to True if a second pass is required.
    """
    
    _detected_hazards: Set[Hazard]
    """
    Detected hazards in the current phase.
    
    If not empty at the end of the inner step an EmergencyStopException is raised.
    """
    
    detected_hazards_info: dict[Hazard, Union[HazardSeverity, Any]]
    """
    Information about the detected hazards. :py:meth:`add_hazard` inserts the given :py:class:`.HazardSeverity` as value,
    however, note that the values are can be arbitrary if used otherwise.
    """

    PHASE_NOT_EXECUTED: object = object()
    """
    Value in :py:attr:`phase_results` to indicate that :python:`agent.execute_phase(phase)` was called for the respective phase
    
    :meta hide-value:
    """

    def __init__(self, agent: "LunaticAgent", **kwargs: Any):
        """
        Its recommended to initialize the context object with :py:meth:`.LunaticAgent._make_context`.
        """
        self.agent = agent
        self._control = kwargs.pop("control", None)
        self._init_arguments = kwargs
        self.phase_results = dict.fromkeys(Phase.get_phases(), Context.PHASE_NOT_EXECUTED)
        
        self.config: "ContextSettings" = agent.config.copy()  # type: ignore
        self.config._content["live_info"] = agent.live_info  # not a copy! # pyright: ignore
        
        self.detected_hazards = set()
        self.detected_hazards_info = dict.fromkeys(Hazard, HazardSeverity.NONE)
        self.__dict__.update(kwargs)
        
        # Less used attributes
        self.evaluation_results = {}
        self.action_results = {}

    @property
    def current_phase(self) -> Phase:
        """Current :py:class:`Phase` the agent is in."""
        return self.agent.current_phase
    
    @property
    def control(self) -> Union[carla.VehicleControl, None]:
        """
        Current control the agent should use. Set by :py:meth:`execute_phase(update_controls=...) <.LunaticAgent.execute_phase>`.

        Note:
            Safeguarded to be not set to None. Setting it to :code:`None` is discouraged.
            Use :py:meth:`set_control` if setting it to :code:`None` is really needed.
        """
        return self._control
    
    @control.setter
    def control(self, control: carla.VehicleControl):
        if control is None:         # type: ignore[comparison]
            raise ValueError("Context.control must not be None. "
                             "To set it to None explicitly use set_control.")
        self._control = control
        
    def set_control(self, control: Optional[carla.VehicleControl]):
        """Set the control, allows to set it to None."""
        self._control = control
        
    def get_or_calculate_control(self) -> carla.VehicleControl:
        """
        Get the control if it is set, otherwise calculate it by
        executing the local planner.
        
        Returns:
            The control the agent should use.
            
        Note:
            Use this function inside rules to acquire a control object-
            
        Warning:
            This is equivalent to ending the inner step of the agent.
        
        See Also:
            :py:meth:`LunaticAgent._calculate_control`
        """
        if self.control:
            return self.control
        self.control = self.agent._calculate_control()  # pyright: ignore[reportPrivateUsage]
        return self.control  # pyright: ignore[reportReturnType]
        
    @property
    def detected_hazards(self) -> Set[Hazard]:
        """
        Detected hazards in the current phase.
        
        If not empty at the end of the inner step an EmergencyStopException is raised.
        """
        return self._detected_hazards
    
    @detected_hazards.setter
    def detected_hazards(self, hazards: Set[Hazard]):
        if not isinstance(hazards, set):  # type: ignore
            raise TypeError("detected_hazards must be a set of Hazards.")
        self._detected_hazards = hazards
        
    def add_hazard(self, hazard: Hazard, hazard_level: HazardSeverity = HazardSeverity.EMERGENCY):
        """
        Add the specified hazard to the detected hazards, in parallel the `hazard_level` can be set which
        which is stored in :any:`detected_hazards_info`.
        """
        if hazard not in Hazard:
            logger.warning(f"Adding {hazard} to the detected hazards which is not a member of the Hazard enum.")
        self.detected_hazards.add(hazard)
        self.detected_hazards_info[hazard] = hazard_level
        
    def discard_hazard(self, hazard: Hazard, match: Literal["exact", "subset", "intersection"] = "subset"):
        """
        Discards a hazard from the detected hazards.
        
        Parameters:
            hazard: Hazard to remove from :py:attr:`detected_hazards`.
            match: How to match the hazard to remove.
        
                - "exact" removes if the exact :py:class:`~classes.constants.Hazard` flag is present.
                - "subset" removes if the hazard is a subset of the detected hazard, e.g.:
                    
                        - :python:`discard_hazard(Hazard.VEHICLE, match="subset")` would remove
                          :any:`Hazard.OBSTACLE` = ``Hazard.VEHICLE | PEDESTRIAN | STATIC_OBSTACLE``.
                        
                        - :python:`discard_hazard(Hazard.TRAFFIC_LIGHT, match="subset")` would *not* remove
                          :any:`Hazard.TRAFFIC_LIGHT_RED`.
                    
        """
        if match == "subset":
            self.detected_hazards = {h for h in self.detected_hazards if hazard not in h}  # supports flags
        elif match == "exact":
            self.detected_hazards.discard(hazard)
        elif match == "intersection":
            self.detected_hazards = {h for h in self.detected_hazards if not hazard & h}
        else:
            raise ValueError(f"match must be 'exact', 'subset' or 'intersection', not {match}.")
            
    def has_hazard(self, hazard: Hazard, match: Literal["exact", "subset", "intersection"] = "intersection") -> bool:
        """
        Checks if the hazard intersects with any of the detected hazards.
        
        See :py:meth:`discard_hazard` for the different matching options.
        """
        if match == "exact":
            return hazard in self.detected_hazards
        if match == "subset":
            return any(hazard in h for h in self.detected_hazards)
        if match == "intersection":
            return any(hazard & h for h in self.detected_hazards)
        raise ValueError(f"match must be 'exact', 'subset' or 'intersection', not {match}.")

    # Convenience function when using detect_vehicles
    from agents.tools.lunatic_agent_tools import max_detection_distance  # noqa

    @property
    def live_info(self) -> "LiveInfo":
        return self.config.live_info
    
    @property
    def active_blocking_rules(self) -> Set["BlockingRule"]:
        return self.agent._active_blocking_rules  # pyright: ignore[reportPrivateUsage]

    
#@ConditionFunction["Rule", [], Literal[True]] # python 3.9+ syntax
@ConditionFunction
def always_execute(ctx: Context) -> Literal[True]:  # pylint: disable=unused-argument, # noqa: ARG001
    """
    This is an :py:class:`.ConditionFunction` that always returns :python:`True`. It can be used to always execute an action.
    """
    return True


def _use_temporary_config(func: Callable[Concatenate[_Rule,
                                                     "Context",
                                                     Optional[Dict[str, Any]], _P], _T]
    ) -> Callable[Concatenate[_Rule, "Context", Optional[Dict[str, Any]], _P], _T]:
    """
    During the condition evaluation the ctx.config should have the overwrite settings applied
    but not in a permanent way.
    """
    # TODO: To avoid unused argument error, consume the dict; however this might be harder to understand
    
    @wraps(func)
    def wrapper(self: _Rule, ctx: Context, overwrite: Optional[Dict[str, Any]] = None, *args: _P.args, **kwargs: _P.kwargs) -> _T:
        settings = self.overwrite_settings.copy()  # Dict with "self" : SelfConfig
        if overwrite:
            settings.update(overwrite)
        
        original_ctx_config = ctx.config
        ctx.config["self"] = "???"  # do not merge old self_config
        
        temp: "ContextSettings" = OmegaConf.merge(ctx.config, settings)  # type: ignore
        
        OmegaConf.set_readonly(temp, True)
        ctx.config = temp
        self.self_config = self.overwrite_settings["self"] = ctx.config["self"]
        OmegaConf.set_readonly(self.self_config, False)  # The Rule's settings should still be dynamic; expected in overwrite
        try:
            return func(self, ctx, overwrite, *args, **kwargs)
        finally:
            ctx.config = original_ctx_config
    return wrapper


class _CountdownRule:

    # TODO: low prio: make cooldown dependant of tickrate or add a conversion from seconds to ticks OR make time-based
    tickrate: ClassVar[int] = NotImplemented
    """
    :meta private:
    """

    DEFAULT_COOLDOWN_RESET: ClassVar[int] = 0
    """
    Value the cooldown is reset to when :py:meth:`reset_cooldown` is called without a value.
    
    Used *only* when :py:attr:`cooldown_reset_value` is not set.
    """
    
    start_cooldown: ClassVar[int] = 0
    """Initial :py:attr:`cooldown` when initialized. if >0 the rule will not be ready for the first **start_cooldown** ticks."""

    _instances: ClassVar["WeakSet[_CountdownRule]"] = WeakSet()
    """Keep track of all Rule instances for the cooldowns"""
    
    _cooldown: int
    """If 0 the rule is ready to be executed."""
    
    blocked: bool = False  # NOTE: not a property
    """Indicates if the rule is blocked for this tick only. Is reset to False after the tick."""

    if TYPE_CHECKING:
        class _InitParameters(TypedDict):
            """Dict describing the parameters of the __init__ of the class method."""
            cooldown_reset_value: NotRequired[Optional[int]]
            enabled: NotRequired[bool]
        
    def __init__(self, cooldown_reset_value: Optional[int] = None, enabled: bool = True):
        self._instances.add(self)
        self._cooldown = self.start_cooldown
        self.max_cooldown = cooldown_reset_value if cooldown_reset_value is not None else self.DEFAULT_COOLDOWN_RESET
        self._enabled = enabled

    def is_ready(self) -> bool:
        """Group aware check if a rule is ready."""
        return self.cooldown == 0 and self.enabled and not self.blocked  # Note: uses property getters. Group aware for GroupRules
    
    def reset_cooldown(self, value: Optional[int] = None):
        if value is None:
            self._cooldown = self.max_cooldown
        elif value >= 0:
            self._cooldown = int(value)
        else:
            raise ValueError("Cooldown value must be a None or a non-negative integer.")

    @property
    def cooldown(self) -> int:
        """
        Cooldown of the rule in ticks until it can be executed again. Only if 0 the rule can be executed.
        """
        return self._cooldown
    
    @cooldown.setter
    def cooldown(self, value: int):
        self._cooldown = value
    
    def update_cooldown(self):
        """
        Update the :py:attr:`cooldown` of *this* rule.
        
        :meta private:
        """
        if self._cooldown > 0:
            self._cooldown -= 1
    
    @classmethod
    def update_all_cooldowns(cls):
        """Updates the cooldowns of **all** rules."""
        for instance in cls._instances:
            instance.update_cooldown()
            
    @classmethod
    def unblock_all_rules(cls):
        """Unblocks all rules"""
        for instance in cls._instances:
            instance.blocked = False
            
    @property
    def enabled(self) -> bool:
        """If :code:`False` the rule will not be evaluated. Contrary to :py:attr:`blocked` this permanently disables the rule."""
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
    
    def set_active(self, value: bool):
        """Enables or disables the rule. Contrary to :py:attr:`blocked` it will not be reset after the tick."""
        self._enabled = value
    
    class CooldownFramework:
        """
        Context manager that can reduce all cooldowns at the end of a `with` statement.
        """

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):  # type: ignore
            self.tick()
        
        @staticmethod
        def tick():
            """
            Update all cooldowns and unblock all rules.
            
            Calls:
                - :py:meth:`Rule.update_all_cooldowns`
                - :py:meth:`Rule.unblock_all_rules`
            """
            Rule.update_all_cooldowns()
            Rule.unblock_all_rules()
          
          
_GroupInstanceValues = TypedDict('_GroupInstanceValues', {"cooldown": int, "max_cooldown": int, "instances": "WeakSet[_GroupRule]"})
"""TypeHint that describes the values of `_GroupRule._group_instances`."""


class _GroupRule(_CountdownRule):
    group: Optional[str] = None  # group of rules that share a cooldown
    """
    Group name of rules that should share their cooldown.
    
    None for a rule to not share its cooldown.
    """

    # first two values in the list are current and max cooldown, the third is a set of all instances
    _group_instances: ClassVar[Dict[str, _GroupInstanceValues]] = {}
    """
    Dictionary of all group instances.
        Keys:
            The group name.
        Values:
            Is a list of the *current cooldown*, the *max cooldown for reset* and a *WeakSet of all instances*.
    """
    
    if TYPE_CHECKING:
        class _InitParameters(_CountdownRule._InitParameters):  # pyright: ignore[reportPrivateUsage]
            """Dict describing the parameters of the __init__ of the class method."""
            group: NotRequired[Optional[str]]

    def __init__(self, group: Optional[str] = None, cooldown_reset_value: Optional[int] = None, enabled: bool = True):
        super().__init__(cooldown_reset_value, enabled)
        self.group = group
        if group is None:
            return
        if group not in self._group_instances:
            self._group_instances[group] = {'cooldown': 0, 'max_cooldown': 0, 'instances': WeakSet()}
        self._group_instances[group]["instances"].add(self)  # add to weak set

    @property
    def cooldown(self) -> int:
        """
        Cooldown of the rule in ticks until it can be executed again after its action was executed.
        If 0 the rule is ready to be executed.
        """
        if self.group:
            return _GroupRule._group_instances[self.group]["cooldown"]
        return super().cooldown
    
    @property
    def has_group(self) -> bool:
        """Indicates if the rule belongs to a group, i.e. :python:`self.group is not None`."""
        return self.group is not None
    
    @cooldown.setter
    def cooldown(self, value: int):
        if self.group:
            _GroupRule._group_instances[self.group]["cooldown"] = value
            return
        super().cooldown = value
    
    def set_my_group_cooldown(self, value: Optional[int] = None):
        """Update the cooldown of the group this rule belong to"""
        if self.group is None:
            logger.warning("Rule does not belong to a group, but set_my_group_cooldown was called. Ignoring.")
            return
        if value is None:
            self._group_instances[self.group]["cooldown"] = self._group_instances[self.group]["max_cooldown"]  # set to max
        else:
            self._group_instances[self.group]["cooldown"] = value

    def reset_cooldown(self, value: Optional[int] = None):
        """Reset or set the cooldown; for a group rule it resets the group cooldown."""
        if self.group:
            self.set_my_group_cooldown(value)
        else:
            super().reset_cooldown()

    @classmethod
    def set_cooldown_of_group(cls, group: str, value: int):
        """Updates the cooldown of the specified group to a specific value"""
        if group in cls._group_instances:
            cls._group_instances[group]["cooldown"] = value
        else:
            raise ValueError(f"Group {group} does not exist.")

    __filter_not_ready_instances: Callable[["_CountdownRule"], bool] = lambda instance: instance.group is None and instance._cooldown > 0  # pylint: disable=line-too-long # type: ignore[attr-defined]
    """
    Filter function to get all instances that are not ready. see `update_all_cooldowns`
    Group rules should not be affected by this filter.
    """
    
    @classmethod
    def update_all_cooldowns(cls):
        """Globally updates the cooldown of *all* rules."""
        # Update Groups
        for instance_data in cls._group_instances.values():
            if instance_data["cooldown"] > 0:
                instance_data["cooldown"] -= 1
        for instance in filter(cls.__filter_not_ready_instances, cls._instances):
            instance._cooldown -= 1


class Rule(_GroupRule):
    _auto_init_: ClassVar[bool] = True
    """
    If set to False the automatic :code:`__init__` creation is disabled when subclassing.
    This automatic :code:`__init__` will fix parameters like :any:`phases` and :any:`condition` to the class.
    
    Declaring an :code:`__init__` method in the class has the same effect as setting :code:`_auto_init_` to False.
    
    Note:
        Using :python:`class NewRuleType(metarule=Rule)` is nearly equivalent to :python:`_auto_init_=False`, but is not inherited.
    """
    
    NOT_APPLICABLE: ClassVar[Literal[RuleResult.NOT_APPLICABLE]] = RuleResult.NOT_APPLICABLE
    """
    Unique object :py:attr:`.RuleResult.NOT_APPLICABLE` that indicates that no action was executed.
    
    :meta hide-value:
    
    .. deprecated:: Use :py:attr:`.RuleResult.NOT_APPLICABLE` directly
    """
    
    NO_RESULT: ClassVar[Literal[RuleResult.NO_RESULT]] = RuleResult.NO_RESULT
    """
    Unique object :py:attr:`.RuleResult.NO_RESULT` that indicates that the rules :py:meth:`action` did not return a result,
    e.g. because an exception was raised.
    
    :meta hide-value:
    
    .. deprecated:: Use :py:attr:`.RuleResult.NOT_APPLICABLE` directly
    """
    
    _PROPERTY_MEMBERS: ClassVar[Set[str]] = {"cooldown", "has_group", "enabled"}
    """
    A subclass can only overwrite these attributes with properties. This prevents a user accidentally overwriting the property,
    e.g. `cooldown = 20` with a method or variable.
    
    TODO:
        Consider making enabled a variable and not a property.
    """
    
    description: str
    """Description of what this rule should do"""
    
    phases: frozenset[Phase]
    """
    The phase or phases in which the rule should be evaluated.
    For instantiation the phases attribute can be any :term:`Iterable` [:py:class:`.Phase`].
    """
    
    phase: Phase
    """For the Class API the phase attribute be set to a single Phase object."""
    
    if TYPE_CHECKING:
        condition: ConditionFunctionLike[Self, [], Hashable]
        """
        The condition that determines if the rule's actions should be executed.
        
        Simple Variant:
            return True if the action should be executed, False otherwise.
            if :py:attr:`.Rule.false_action` is defined, False will execute :py:attr:`.Rule.false_action`.
            
        Advanced Variant:
            return a :term:`Hashable` value that is used as key in the :py:attr:`actions` dict.
            
        NOTE:
            The readthedocs description is set in the __init__ function.
        """
    
    actions: dict[Any, CallableAction[Self, [], Any]]
    """Dictionary that maps rule results to the action that should be executed."""
    
    action: Annotated[CallableAction[Self, [], Any], "attribute not available on instance -> merged into `actions`"]
    """
    Action that should be executed if the rule is True. If `actions` is set, this is ignored.
    """
    
    false_action: Annotated[CallableAction[Self, [], Any], "attribute not available on instance -> merged into `actions`"]
    """Action that should be executed if the rule is False. May not be set if `actions` is set."""
    
    if READTHEDOCS and not TYPE_CHECKING:
        false_action: Annotated[CallableActionT, "attribute not available on instance -> merged into `actions`"]
        action: Annotated[CallableActionT, "attribute not available on instance -> merged into `actions`"]
        actions: dict[Any, CallableActionT]
    
    #group : Optional[str]
    #"""Group name for rules that should share their cooldown."""
    
    overwrite_settings: dict[str, Any]
    """
    Settings that should overwrite the agent's settings for this rule.
    
    Note:
        The overwrite settings are primitive :py:class:`dict` objects,
        :py:class:`omegaconf.DictConfig` objects are converted.
    """
    
    self_config: "RuleConfig"
    """
    A custom sub-config for the rule that is not included in the agents settings.
    Automatically gets a `instance` key added with the rule instance.
    
    Can be accessed via `ctx.config.current_rule` or `self.config.self`.
    
    Note:
        Internally `self.config` and `ctx.config` is the same object, which makes
        interpolations to the agent's settings possible.
        
    Attention:
        The **self_config object is *not* constant** it is recreated each time the
        rule is evaluated to have the current context available.
    """
    
    priority: Union[float, int, RulePriority] = RulePriority.NORMAL
    """Rules are executed in order of their priority, from high to low."""
    
    # Initialization functions
    
    _ctx: Optional[Context] = None
    """No hard attachment, to not keep the context objects alive, use with care. Check where it is set in a rule."""

    def clone(self):
        """
        Create a new instance of the rule with the same settings.
        
        Note:
            - The current cooldown **is not** taken into account.
            - The current enabled state **is** taken into account.
        """
        return self.__class__(self)  # Make use over overloaded __init__

    @overload
    def __new__(cls, phases: Union[Phase, Iterable[Phase], None] = None) -> "Self": ...
        # No argument call; should be redundant
    
    @overload
    def __new__(cls, phases: Union[Phase, Iterable[Phase], None] = None, **kwargs: Unpack[_InitParameters]) -> "Self": ...
        # argument call
        
    @overload
    def __new__(cls, **kwargs: Unpack[_InitParametersComplete]) -> "Self": ...
        # Normal init
    
    @overload
    def __new__(cls, phases: "type[Any] | Self") -> "Self": ...
        # Rule.copy(other_rule)
    
    def __new__(cls,
                phases: Optional[Union[Phase, Iterable[Phase], None, "type[Any]", Self, str]] = None,
                bases: Optional[tuple[type[Any], ...]] = None,
                clsdict: Optional[dict[str, Any]] = None,
                **kwargs: Any):
        """
        The @Rule decorator allows to instantiate a Rule class directly for easier out-of-the-box usage.
        Further check for metaclass initialization, else this is a normal instance creation.
        
        Parameters:
            kwargs: These will be passed to :python:`__init_subclass__`.
        """
        # @Rule
        # class NewRuleInstance:
        # or Rule(other_rule) -> copy
        if isclass(phases):
            if issubclass(phases, _CountdownRule):
                raise ValueError("When using @Rule the class may not be a subclass of Rule. Do not inherit from rule or subclass from Rule instead with the decorator."
                                 "Do not do:\n\t@Rule\n\tclass MyRule(>>Rule<<): ...\n")
            # cls is the Rule used to decorate the decorated_class
            decorated_class = phases
            
            # Create the new class, # NOTE: goes to __init_subclass_
            new_decorated_class = type(decorated_class.__name__, (cls, ), decorated_class.__dict__.copy(),
                                  _init_by_decorator=True, **kwargs)  # > calls init_subclass; copy() for correct type!
            if TYPE_CHECKING:
                assert issubclass(new_decorated_class, cls) and issubclass(new_decorated_class, decorated_class)
            
            return super().__new__(new_decorated_class)
        
        # class NewRuleType(metaclass=Rule) # deprecated
        if isinstance(phases, str):
            try:
                logger.warning("Using NewRule(metaclass=Rule) is deprecated. Use NewRule(Rule, metarule=True) instead.")
                assert clsdict and isinstance(bases, tuple)
                class_name = phases
                new_rule_class = type(class_name, (cls, *bases), clsdict, metarule=True, **kwargs)
            except Exception:
                print("ERROR: If you want to initialize a rule be sure that you pass a Phase object as the first argument."
                      "A string assumes that you've used class NewSubclass(metaclass=Rule) "
                      "This is DEPRECATED use class NewSubclass(Rule, metarule=True) instead.")
                raise
            else:
                assert issubclass(new_rule_class, cls)  # for type-hints
                return new_rule_class
        # Normal instance
        return super().__new__(cls)

    if TYPE_CHECKING:
        class _InitParameters(_GroupRule._InitParameters, total=False, closed=False):  # pyright: ignore[reportPrivateUsage]
            """Dict describing the parameters of the __init__ of the class method."""
            #phases:    Union[Phase, Iterable[Phase]] # leave this and use explicitly later on
            #condition: Optional[ConditionFunctionLike[Rule, ..., Hashable]]
            action: Optional[Union[CallableAction[Rule, [], Any], Dict[Any, CallableAction[Rule, [], Any]]]]
            false_action: Optional[CallableAction[Rule, [], Any]]
            actions: Optional[Dict[Any, CallableAction[Rule, [], Any]]]
            description: str
            overwrite_settings: Optional[Dict[str, Any]]
            self_config: Optional[Dict[str, Any]]
            priority: RulePriority
            
        class _InitParametersComplete(_InitParameters):
            """Dict describing the parameters of the __init__ of the class method."""
            phases: Required[Union[Phase, Iterable[Phase]]]
            condition: NotRequired[Optional[ConditionFunctionLike[Rule, ..., Hashable]]]
            
        class _CallKwargs(TypedDict, closed=True):
            ignore_phase: bool
            """Default False"""
            ignore_cooldown: bool
            """Default False"""
            
    @singledispatchmethod
    def __init__(self,
                 phases: Union[Phase, Iterable[Phase]],  # iterable of Phases
                 #/, # phases must be positional; python3.8+ only
                 condition: Optional[ConditionFunctionLikeT] = None,
                 action: Optional[Union[CallableAction[Self, []], Dict[Any, CallableAction[Self, []]]]] = None,
                 false_action: Optional[CallableAction[Self, []]] = None,
                 *,
                 actions: Optional[Dict[Any, CallableAction[Self, []]]] = None,
                 description: str = "What does this rule do?",
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 self_config: Optional[Dict[str, Any]] = None,
                 priority: RulePriority = RulePriority.NORMAL,
                 cooldown_reset_value: Optional[int] = None,
                 group: Optional[str] = None,
                 enabled: bool = True,
                 ):
        """
        Initializes a Rule object.

        Parameters:
            phases: The phase(s) when the rule should be evaluated.
                An iterable of Phase objects or a single Phase object.
            condition: A function that takes a Context object as input and returns a Hashable value.
                If not provided, the class must implement a `condition` function.
            action: A function or a dictionary of functions that take a Context object as input.
                If `action` behaves like `actions`.
                Only one of `action` and `actions` can be set.
            false_action: A function that takes a Context object as input and returns any value.
                It is used when `action` is a single function and represents the action to be taken when the condition is False.
            actions: A dictionary of `action` functions
                It should map the return values of `condition` to the corresponding action function.
                If `action` is None, `actions` must be provided.
            description: A string that describes what this rule does.
            overwrite_settings: A dictionary of settings that will overwrite the
                agent's setting for this Rule.
            priority: The priority of the rule. It can be a float, an integer, or a RulePriority enum value.
            cooldown_reset_value: An optional integer value that represents the cooldown reset value for the rule.
                If not provided falls back to the class attribute :py:attr:`.Rule.DEFAULT_COOLDOWN_RESET`.
            group: An optional string that specifies the group to which this rule belongs.
            enabled: A boolean value indicating whether the rule is enabled or not.

        Raises:
            ValueError: If ``phases`` is empty or None, or if ``phases`` contains an object that is not of type Phase.
            TypeError: If ``condition`` is None and the class does not implement a :py:meth:`condition` function,
                or if both ``action`` and ``actions`` are None and the class does not have an :py:attr:`actions` attribute or an :py:meth:`action` function.
            TypeError: if ``actions`` is not a Mapping object.
            ValueError: If both ``action`` and ``actions`` are provided.
            ValueError: If ``action`` is a Mapping and either ``false_action`` or ``actions`` is not None.
            ValueError: If an ``action`` function is not callable.
            ValueError: If ``description`` is not a string.
        """
        
        # Check phases
        if not phases:
            raise ValueError("phases must not be empty or None")
        if not isinstance(phases, frozenset):
            phases = frozenset(phases) if isinstance(phases, Iterable) else frozenset([phases])
        for p in phases:
            if not isinstance(p, Phase):
                raise TypeError(f"phase must be of type Phases, not {type(p)}")
        self.phases = phases
        
        # Check Rule
        if condition is None and not hasattr(self, "condition"):
            raise TypeError(
                f"{self.__class__.__name__}.__init__() missing 1 required positional argument: 'condition'. "
                "Alternatively the class must implement a `condition` function.")
        
        if False and TYPE_CHECKING:
            # Idea have type hint here
            self.condition: Any = ...
            """
            The condition that determines if the rule's actions should be executed.
            
            Simple Variant:
                return True if the action should be executed, False otherwise.
                if :py:attr:`.Rule.false_action` is defined, False will execute :py:attr:`.Rule.false_action`.
                
            Advanced Variant:
                return a :term:`Hashable` value that is used as key in the :py:attr:`actions` dict.
            """
            if condition is not None:
                self.condition = condition
            else:
                self.condition = self.__class__.condition

        if condition is not None:
            if not hasattr(self, "condition"):
                self.condition = condition
            else:
                # Warn if cls.condition and passes condition are different
                self_func = getattr(self.condition,
                                    "__func__",
                                    getattr(self.condition, "func", self.condition))
                if self_func != condition:  # Compare method with function
                    logger.warning(
                        f"Warning 'condition' argument passed but class {self.__class__.__name__} "
                        "already implements a different function 'self.condition'. "
                        f"Overwriting {self.condition} with passed condition {getattr(condition, '__name__', str(condition))}. "
                        "This might lead to undesired results.")
                
                # NOTE: IMPORTANT: self.condition = condition overwrites methods with functions
                # To keep methods as methods the condition parameter is removed with
                # `do_not_overwrite.append("condition")` used during __init_subclass__
                # Could move this check also to here, however, it will then not be checked during class creation
                self.condition = condition
        # else: self.__class__.condition must be true already, which was checked in the subclass initialization
        
        # Check Actions
        if action is not None and actions is not None:
            try:
                if len(actions) == 1 and action is actions[True]:
                    logger.info(
                        "`action` and `actions` have been both been used when initializing %s. "
                         "Did you use `condition.register_action`? Then you can omit the action parameter.",
                         self)
                    action = None
                else:
                    raise ValueError("Only one of 'action' and 'actions' can be set.")
            except (KeyError, ValueError) as e:
                raise ValueError(
                    "Either only one of 'action' and 'actions' can be set, or actions[True] must be the same as action "
                    "- other actions are currently not supported.") from e
        if action is None and actions is None and not hasattr(self, "actions"):
            # NOTE: the k in params check below is essential for this to work correctly.
            raise TypeError(
                f"{self.__class__.__name__}.__init__() arguments `action` and `actions` are both None. "
                "Provide at least one argument alternatively the class must have an `actions` "
                "attribute or an `action` function.")

        if action is None:
            if not isinstance(actions, Mapping):
                raise TypeError(f"actions must be a Mapping, not {type(actions)}")

            self.actions = actions
        elif isinstance(action, Mapping):
            self.actions = action
            if false_action is not None or actions is not None:
                raise ValueError("When passing a dict to action, false_action and actions must be None")
        else:
            # NOTE: Might overwrite actions attribute
            self.actions = {}  # type: ignore
            if action is not None:
                self.actions[True] = action
            if false_action is not None:
                self.actions[False] = false_action
        # actions can be the dict of the class, we do not want the same dict instance
        self.actions = dict(self.actions)
        
        # Assure that method(self, ctx) like functions are accessible like them
        for key, func in self.actions.items():
            if not callable(func):
                raise TypeError(f"Action for key {key} must be callable, not {type(func)}")
            multiple_parameters = len(inspect.signature(func).parameters) >= 2
            if multiple_parameters and getattr(func, "use_self", True):
                # NOTE: could use types.MethodType
                self.actions[key] = partial(func, self)  # bind to self
        
        # Check Description
        if not isinstance(description, str):
            raise TypeError(f"description must be of type str, not {type(description)}")
        self.description = description
        super().__init__(group or self.group, cooldown_reset_value, enabled)  # or self.group for subclassing
        self.priority: float | int | RulePriority = priority  # used by agent.add_rule
        
        self.overwrite_settings = overwrite_settings or {}
        if not isinstance(self.overwrite_settings, dict):
            # NOTE: If DictConfig only the outermost will be a dict,
            # i.e. this could be dict[str, DictConfig]
            self.overwrite_settings = dict(self.overwrite_settings)
        if self_config and "self" in self.overwrite_settings and self.overwrite_settings["self"] != self_config:
            logger.debug("Warning: self_config and self.overwrite_settings['self'] must be the same object.")
        
        default_self_config = cast("RuleConfig", getattr(self, "self_config", getattr(self, "SelfConfig", {})))
        if isclass(default_self_config):
            if not is_dataclass(default_self_config):
                logger.warning(
                    f"Class {self.__class__.__name__} has a self_config class that is not a dataclass. "
                    "This might lead to undesired results, i.e. missing keys in the config.")
            default_self_config = default_self_config()
        if not isinstance(default_self_config, DictConfig):
            default_self_config = cast("RuleConfig", OmegaConf.create(default_self_config, flags={"allow_objects": True}))  # type: ignore
        if self_config:
            self.self_config = cast("RuleConfig", OmegaConf.merge(default_self_config, self_config))
        else:
            self.self_config = default_self_config
        assert self.self_config._get_flag("allow_objects"), "self_config must allow objects to be used as values."  # pyright: ignore[reportPrivateUsage]
        
        self.overwrite_settings["self"] = self.self_config
        self.overwrite_settings["self"]["instance"] = self
    
    # Called on subclass creation. Can be used for class API
    def __init_subclass__(cls, _init_by_decorator: bool = False, metarule: bool = False):
        """
        Automatically creates a :python:`__init__` function to allow for a simple to use
        class-interface to create rule classes.
        
        By setting :python:`_auto_init_ = False` in the class definition, the automatic __init__
        creation is disabled. Similarly, this is also the case if :python:`metarule=Rule` is used
        for the class creation.
        """
        if hasattr(cls, "phases") and hasattr(cls, "phase") and cls.phases and cls.phase:
            raise ValueError(f"Both 'phases' and 'phase' are set in class {cls.__name__}. Use only one. %s, %s" % (cls.phases, cls.phase))
        
        for attr in cls._PROPERTY_MEMBERS:
            if hasattr(cls, attr) and not hasattr(getattr(cls, attr), "__get__"):
                raise ValueError(
                    f"Class {cls.__name__} has overwritten property {attr} with {getattr(cls, attr)}."
                    " You may only overwrite the following attributes with properties: {cls._PROPERTY_MEMBERS}."
                    "Did you mean `start_cooldown` or `cooldown_reset_value` instead of `cooldown`?")
        if not cls._auto_init_ or metarule:
            return
        
        custom_init = cls.__dict__.get("__init__", False)
            
        # Members that are not overwritten and passed as default arguments (None) into the __init__
        do_not_overwrite = ["phases"]
        
        if hasattr(cls, "condition"):
            # Check if the condition should be treated as a method or function
            rule_func: ConditionFunctionLike[Self, ..., Hashable]
            if isinstance(cls.condition, ConditionFunction):
                rule_func = cls.condition.evaluation_function  # pyright: ignore[reportUnknownMemberType, reportAssignmentType]
            else:
                rule_func = cls.condition
            if isinstance(rule_func, staticmethod):
                rule_func = rule_func.__func__
            
            # Decide method(self, ctx) vs. function(ctx)
            if hasattr(cls.condition, "use_self") and cls.condition.use_self is not None:   # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType, reportFunctionMemberAccess,  reportAttributeAccessIssue]
                condition_as_method: bool = cls.condition.use_self  # type: ignore[attr-defined]
            else:
                params = len(inspect.signature(rule_func).parameters)
                if params >= 2:
                    if params > 2:
                        logger.warning(f"Rule {getattr(cls.condition, '__name__', cls.condition)}"  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
                                "has more than 2 parameters. "
                                "Treating it as a method(self, ctx, **kwargs) with self argument!"
                                "To avoid this message or to use it as a function use"
                                "ConditionFunction(use_self=True|False) explicitly.")
                    condition_as_method = True
                else:
                    condition_as_method = False
            if condition_as_method:
                logger.debug("Implementing %s as method(self, ctx) - "
                                "If you need it as a function(ctx, *args) decorate it with "
                                "@ConditionFunction(use_self=False).",
                            getattr(cls.condition, '__name__', cls.condition))  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
                do_not_overwrite.append("condition")
            else:
                # If the signature has only one parameter its a function; else its user decision.
                logger.debug("Implementing %s as function(ctx) without a self argument "
                                "- If you need it as a method(self, ctx, *args) decorate it with "
                                "@ConditionFunction(use_self=True).",
                             getattr(cls.condition, '__name__', cls.condition))  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
            
            # Actions provided by condition.actions, e.g. ConditionFunction.register_action
            if hasattr(cls.condition, "actions") and cls.condition.actions:  # type: ignore[attr-defined]
                if hasattr(cls, "actions") and cls.actions:
                    raise ValueError(f"Class {cls.__name__} already has an 'actions' attribute. "
                                "It will be overwritten by the 'actions' attribute of the condition."
                                " This is the case if ConditionFunction.register_action has been used.")
                cls.actions = cls.condition.actions                     # type: ignore[attr-defined]
                
        if not hasattr(cls, "description"):
            cls.description = cls.__doc__ or "No description provided."
                
        if hasattr(cls, "self_config"):
            do_not_overwrite.append("self_config")
        
        # Create a __init__ function that sets some of the parameters.
        # find overlapping parameters
        params = inspect.signature(cls.__init__).parameters
        
        # TODO: to be lazy Rule arguments need to be added to params so that "k in params" works
        
        def partial_init(self: Self, phases: Optional[Iterable[Phase]] = None, *args, **kwargs: Rule._InitParameters):  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
            # Need phases as first argument
            cls_phases = getattr(cls, "phases", None)  # allow for both wordings
            cls_phase = getattr(cls, "phase", None)
            if _init_by_decorator:
                # Using @Rule phases as first argument is the class
                phases = cls_phases or cls_phase
            else:
                if phases is None:  # NOTE: Could be Phase.NONE
                    phases = cls_phases or cls_phase
            if phases is None:
                raise ValueError(f"`phases` or `phase` must be provided for class {cls.__name__}")
            # Removing condition to not overwrite it
            kwargs.update({k: v for k, v in cls.__dict__.items() if k in params and k not in do_not_overwrite})  # type: ignore
            try:
                if custom_init:
                    custom_init(self, phases, *args, **kwargs)
                else:
                    # note: could be single dispatch function
                    # super will not be _GroupRule but at least Rule
                    super(cls, self).__init__(phases, *args, **kwargs)  # type: ignore[arg-type]
            except IndexError:  # functools <= python3.10
                logger.error("\nError in __init__ of %s. Possible reason: Check if the __init__ method has the correct signature. `phases` must be a positional argument.\n", cls.__name__)
                raise
            except TypeError as e:
                # e.g. forgot a action, or rules attribute (MultiRule)
                if "missing" in str(e):
                    logger.error("Class %s has likely missing attributes that cannot be passed to init. Check if all required attributes are set in the class definition.", cls.__name__)
                raise
        update_wrapper(partial_init, cls.__init__)  # pyright: ignore[reportUnknownArgumentType]
        cls.__init__ = partial_init  # pyright: ignore[reportIncompatibleMethodOverride, reportAttributeAccessIssue]

    @__init__.register(_CountdownRule)
    @__init__.register(type)
    def __init_by_decorating_class(self, cls: "Rule"):  # pyright: ignore[reportUnusedFunction]
        """
        Initialize by passing a Rule or class object to the __init__ method.
        
        This allows the usage of the @Rule decorator and easy copying.
        """
        phases = getattr(cls, "phases", getattr(cls, "phase", None))  # allow for spelling mistake
        cooldown_reset_value = getattr(cls, "cooldown_reset_value", getattr(cls, "max_cooldown", None))
        
        # TODO: Automate this via inspect.signature or TypedDict of the __init__ signature
        self.__init__(phases,
                      cls.condition,
                      getattr(cls, "action", None),
                      getattr(cls, "false_action", None),
                      actions=getattr(cls, "actions", None),
                      description=cls.description,
                      overwrite_settings=getattr(cls, "overwrite_settings", None),
                      self_config=getattr(cls, "self_config", None),
                      priority=getattr(cls, "priority", RulePriority.NORMAL),
                      cooldown_reset_value=cooldown_reset_value,
                      group=getattr(cls, "group", None),
                      enabled=getattr(cls, "enabled", True))
        
    @__init__.register(Mapping)
    def __init_from_mapping(self, source: "_InitParametersComplete"):  # pyright: ignore[reportUnusedFunction]
        # NOTE: This is weakly tested and not much supported.
        condition = source.get("condition", None)
        if condition is not None:
            condition = getattr(self, "condition", None)
        self.__init__(source.get("phases", source.get("phase")),
                      condition,
                      source.get("action"),
                      source.get("false_action"),
                      actions=source.get("actions"),
                      description=source.get("description", self.description),
                      overwrite_settings=source.get("overwrite_settings"),
                      self_config=source.get("self_config"),
                      priority=source.get("priority", RulePriority.NORMAL),
                      cooldown_reset_value=source.get("cooldown_reset_value"),
                      group=source.get("group"),
                      enabled=source.get("enabled", True))

    # -----------------------
    
    @classmethod
    def _get_init_signature(cls):
        """
        Get the signature of the __init__ function.
        
        Returns:
            The signature of the __init__ function.
            
        :meta private:
        """
        return inspect.signature(cls.__init__).parameters.keys()

    def execute_phase(self,
                      phase: Phase, *,
                      prior_results: Any = None,
                      update_controls: Optional[carla.VehicleControl] = None):
        """
        Attention:
            - **Use with care to avoid loops or recursions.**
            
            - If a :py:class:`.Context` is available prefer using
              :py:meth:`ctx.agent.execute_phase <.LunaticAgent.execute_phase>` instead.
        
        Helper function to execute a phase from within a rule,
        wrapper of :py:meth:`agents.lunatic_agent.LunaticAgent.execute_phase`.
            
        Warns:
            ReferenceError: If the weak proxy pointing to the :py:class:`Context` object has been
                deleted. The phase will not be executed.
            
        See Also:
            - :py:meth:`.LunaticAgent.execute_phase`
        """
        try:
            self._ctx.agent.execute_phase(phase=phase,  # pyright: ignore[reportOptionalMemberAccess]
                                          prior_results=prior_results,
                                          update_controls=update_controls)
        except ReferenceError:
            logger.error("ReferenceError in Rule.execute_phase. Weakproxy deleted.")
    
    # -----------------------
    # Evaluation functions
    # -----------------------

    @_use_temporary_config
    def evaluate(self, ctx: Context,
                 overwrite: Optional[Dict[str, Any]] = None  # pylint: ignore=unused-argument # noqa: ARG002
                 ) -> Union[bool, Hashable, "Literal[RuleResult.NO_RESULT]"]:
        """
        Note:
            This is an **interface** function of rules that is executed during :py:meth:`__call__`.
            This method does not check if a rule is applicable.
            i.e. if the rule is in the correct phase of if it py:meth:`is_ready`
            this is done in :py:meth:`__call__`.
            
            Meta rules with children should overwrite this method and call
            :py:meth:`evaluate_children` from here.
        
        Executes the :py:attr:`condition` function of the rule.
        The decorator automatically takes care of temporarily setting the :py:attr:`overwrite_settings`.
        
        Parameters:
            ctx: The context object that is passed to the condition function.
            overwrite: A dictionary of settings that will overwrite the agent's setting for this Rule.
              Used by the :code:`@_use_temporary_config` decorator.
        
        :meta private:
        """
        self._ctx = proxy(ctx)      # use with care and access over function
        return self.condition(ctx)  # pyright: ignore[reportCallIssue]
    
    def evaluate_children(self, ctx: Context) -> "NoReturn":  # pylint: disable=unused-argument
        """
        Not implemented for this rule class.
        
        Note:
            This is an **interface** function of meta rules
            that is executed during :py:meth:`__call__` to call further rules.
        """
        raise NotImplementedError("This method should be implemented in a subclass")

    def __call__(self,
                 ctx: Context,
                 overwrite: Optional[Dict[str, Any]] = None,
                 *,
                 ignore_phase: bool = False,
                 ignore_cooldown: bool = False) -> Union[Any, Literal[RuleResult.NOT_APPLICABLE]]:
        """
        1. First checks if the rule is *applicable*, i.e. is its :py:attr:`cooldown == 0 <cooldown>`,
           if not returns :py:attr:`NOT_APPLICABLE`.
        2. Afterwards evaluates the rules :py:meth:`condition` function.
            - if the result is not in :py:attr:`actions` returns :py:attr:`NOT_APPLICABLE`.
            - otherwise merges the :py:attr:`overwrite_settings` with the py:attr:`.Context.config` and executes the action.
            
        Parameters:
            ctx: The context object that is passed to the condition function.
            overwrite: Extends :py:attr:`overwrite_settings` for this call only. Defaults to :code:`None`.
            ignore_phase: If :python:`True` the phase check is skipped. Defaults to :code:`False`.
            ignore_cooldown: If True the cooldown check is skipped. Defaults to :code:`False`.
        """
        # Check phase
        assert ignore_phase or ctx.agent.current_phase in self.phases
        
        if not self.is_ready() and not ignore_cooldown:
            return RuleResult.NOT_APPLICABLE
        if not ignore_phase and ctx.agent.current_phase not in self.phases:  # NOTE: This is currently never False as checked in execute_phase and the agents dictionary.
            return RuleResult.NOT_APPLICABLE  # not applicable for this phase

        exception = None
        result = Rule.NO_RESULT
        try:
            result = self.evaluate(ctx, overwrite)
        except BaseException as e:
            exception = e
        else:
            ctx.evaluation_results[ctx.agent.current_phase] = result
            if result in self.actions:
                self.reset_cooldown()
                # Apply overwrite settings permanently
                ctx.config.merge_with(self.overwrite_settings)
                if overwrite:
                    ctx.config.merge_with(overwrite)
                
                action_result = self.actions[result](ctx)  # todo allow priority, random chance  # pyright: ignore[reportCallIssue]
                ctx.action_results[ctx.agent.current_phase] = action_result
                return action_result
            return RuleResult.NOT_APPLICABLE  # No action was executed
        finally:
            self._ctx = None
            if exception:
                self.reset_cooldown()  #
                raise exception
    
    def __str__(self) -> str:
        try:
            if isinstance(self.condition, partial):
                return (self.__class__.__name__
                        + f"(description='{self.description}', "
                          f"phases={self.phases}, group={self.group}, "
                          f"priority={self.priority}, "
                          f"actions={self.actions}, "
                          f"condition={self.condition.func}, "  # pyright: ignore[reportUnknownMemberType]
                          f"cooldown={self.cooldown})"
                )
            return (self.__class__.__name__
                        + f"(description='{self.description}', "
                          f"phases={self.phases}, group={self.group}, "
                          f"priority={self.priority}, "
                          f"actions={self.actions}, "
                          f"condition={self.condition.__name__}, "
                          f"cooldown={self.cooldown})"
                )
        except AttributeError as e:
            logger.info("Error during string creation: " + str(e))
            return (self.__class__.__name__
                    + "(Error in condition.__str__: Rule has not been initialized correctly. "
                      "Missing attributes: " + str(e) + ")")

    def __repr__(self) -> str:
        return str(self)


class MultiRule(Rule, metarule=True):
    """
    This metarule allows to execute one or multiple rules if it is applicable.
    Depending on :py:attr:`execute_all_rules` it will either execute all rules or only the first
    applicable rule from its :py:attr:`rules` list.
    """

    rules: List[Rule]
    """The list of child rules to be called if this rule's condition is true."""
    
    def _wrap_action(self, action: Callable[[Context], Any]):
        """
        Wrap the passed action.
        First the action is executed afterwards the child rules are evaluated.
        
        Note:
            There is no extra condition that is checked between the two actions.
        """
        @wraps(action)
        def wrapper(ctx: Context, *args: Any, **kwargs: Any) -> Any:
            try:
                result = action(ctx, *args, **kwargs)
            except DoNotEvaluateChildRules as e:
                return e, None
            else:
                results = self.evaluate_children(ctx)  # execute given rules as well
            return result, results
        return wrapper

    if TYPE_CHECKING:
        class _InitParameters(Rule._InitParameters):  # pyright: ignore[reportPrivateUsage,reportGeneralTypeIssues]
            rules: Required[List[Rule]]
            sort_rules: NotRequired[bool]
            execute_all_rules: NotRequired[bool]
    
    @singledispatchmethod
    def __init__(self,
                 phases: Union[Phase, Iterable[Phase]],
                 #/, # phases must be positional; python3.8+ only
                 rules: List[Rule],
                 condition: Optional[ConditionFunctionLikeT] = None,
                 *,
                 description: str = "If its own condition is true calls the passed rules.",
                 priority: RulePriority = RulePriority.NORMAL,
                 sort_rules: bool = True,
                 execute_all_rules: bool = False,
                 action: Optional[Callable[[Context], Any]] = None,
                 ignore_phase: bool = True,
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 self_config: Optional[Dict[str, Any]] = None,
                 cooldown_reset_value: Optional[int] = None,
                 group: Optional[str] = None,
                 enabled: bool = True,
                 ):
        """
        Initializes a Rule object that can have further rules as children.

        Args:
            phases (Union[Phase, Iterable]): The phase or phases in which the rule should be active.
            rules (List[Rule]): The list of child rules to be called if the rule's condition is true.
            condition (Callable[[Context]], optional): The condition that determines if the rules should be evaluated. Defaults to :py:func:`always_execute`.
            execute_all_rules (bool, optional):
                If False will only execute the first rule with a applicable condition, i.e. this MultiRule is like a node in a decision tree.
                If True all rules are evaluated, unless one raises a `DoNotEvaluateChildRules` exception.
                Defaults to :python:`False`.
            sort_rules (bool, optional): Flag indicating whether to sort the rules by priority. Defaults to :python:`True`.
            action (Callable[[Context]], optional): The action to be executed before the passed rules are evaluated. Defaults to :python:`None`.
            ignore_phase (bool, optional): Flag indicating whether to ignore the Phase of the passed child rules. Defaults to :python:`True`.
            overwrite_settings (Dict[str, Any], optional): Additional settings to overwrite the agent's settings. Defaults to :python:`None`.
            priority (RulePriority, optional): The priority of the rule. :py:attr:`RulePriority.NORMAL <classes.constants.RulePriority.NORMAL>`.
            description (str, optional): The description of the rule. Defaults to :python:`"If its own rule is true calls the passed rules."`.
            group (str | None, optional): The group name of the rule. Defaults to :python:`None`.
            enabled (bool, optional): Flag indicating whether the rule is enabled after creation. Defaults to :python:`True`.
        """
        self.ignore_phase = ignore_phase
        if rules is None:  # type: ignore
            logger.warning("Warning: No rules passed to %s: %s. You can still add rules to the rules attribute later.", self.__class__.mro()[1].__name__, self.__class__.__name__)
            rules = []
        if len(rules) == 0:
            # NOTE: This will be logged twice, once more by
            logger.warning("Rules list is empty. %s will always return NOT_APPLICABLE.", self.__class__.__name__)
        self.rules = rules
        self.execute_all_rules = execute_all_rules
        if sort_rules:
            self.rules.sort(key=lambda r: r.priority, reverse=True)
        # if an action is passed to be executed before the passed rules it is wrapped to execute both
        if action is not None:
            action = self._wrap_action(action)
        else:
            action = self.evaluate_children  # will be called elsewhere
        if condition is None and not hasattr(self, "condition"):
            condition_arg = always_execute
        else:
            condition_arg = condition
        super().__init__(phases,
                            condition=condition_arg,
                            action=action,
                            description=description,
                            overwrite_settings=overwrite_settings,
                            self_config=self_config,
                            priority=priority,
                            cooldown_reset_value=cooldown_reset_value,
                            enabled=enabled,
                            group=group)
            
    @__init__.register(_CountdownRule)  # For similar_rule = Rule(some_rule), easier cloning
    @__init__.register(type)  # For @Rule class MyRule: ...
    def __init_by_decorating_class(self, cls: "MultiRule"):   # pyright: ignore[reportUnusedFunction]
        phases = getattr(cls, "phases", getattr(cls, "phase", None))  # allow both
        cooldown_reset_value = getattr(cls, "cooldown_reset_value",
                                                        getattr(cls, "max_cooldown", None))
        assert hasattr(cls, "condition"), f"Class {cls} has no condition attribute. It must be provided."
        self.__init__(phases, cls.rules,
                      cls.condition,  # type: ignore
                      description=cls.description,
                      overwrite_settings=getattr(cls, "overwrite_settings", None),
                      self_config=getattr(cls, "self_config", None),
                      priority=getattr(cls, "priority", RulePriority.NORMAL),
                      cooldown_reset_value=cooldown_reset_value, group=getattr(cls, "group", None),
                      enabled=getattr(cls, "enabled", True),
                      sort_rules_by_priority=getattr(cls, "sort_rules_by_priority", True),
                      execute_all_rules=getattr(cls, "execute_all_rules", False),
                      prior_action=getattr(cls, "prior_action", None),
                      ignore_phase=getattr(cls, "ignore_phase", True))
    
    @__init__.register(Mapping)
    def __init_from_mapping(self, cls: "_InitParameters"):  # pyright: ignore[reportUnusedFunction]
        self.__init__(cls.get("phases", cls.get("phase")),
                      cls["rules"],
                      cls.get("condition"),
                      description=cls.get("description", self.description),
                      overwrite_settings=cls.get("overwrite_settings"),
                      self_config=cls.get("self_config"),
                      priority=cls.get("priority", RulePriority.NORMAL),
                      cooldown_reset_value=cls.get("cooldown_reset_value"),
                      group=cls.get("group"),
                      enabled=cls.get("enabled", True),
                      sort_rules_by_priority=cls.get("sort_rules_by_priority", True),
                      execute_all_rules=cls.get("execute_all_rules", False),
                      prior_action=cls.get("prior_action", None),
                      ignore_phase=cls.get("ignore_phase", True))

    def evaluate_children(self, ctx: Context) -> Union[List[Any], Any]:  # pyright: ignore[reportIncompatibleMethodOverride]
        """
        Evaluates the children rules of the current rule in the given context.

        Args:
            ctx : The context in which the child rules are evaluated.

        Returns:
            The results of evaluating the children rules.
            Returns a list of results if execute_all_rules is True,
            otherwise the result of the first rule that was applied.
        """
        results: List[Any] = []
        for rule in self.rules:
            try:
                result = rule(ctx, ignore_phase=self.ignore_phase)
            except DoNotEvaluateChildRules:
                return results
            if not self.execute_all_rules and result is not Rule.NOT_APPLICABLE:  # one rule was applied end.
                return result
            results.append(result)
        if not self.execute_all_rules:
            return Rule.NOT_APPLICABLE  # does not expect a list
        return results


class RandomRule(MultiRule, metarule=True):
    """
    A rule that selects and evaluates one or more random child rules from a set of rules.

    Args:
        phases : The phase or phases in which the rule is applicable.
        rules : The set of rules from which to select random child rules.
        repeat_if_not_applicable : If False, only one rule will be evaluated even if it is not applicable. Defaults to :python:`True`.
        condition :
            A callable that determines if the rule is applicable in a given context.
            If None and the rule does not implement a :py:attr:`condition` attribute the rule always executes.
            Defaults to :python:`None`.
        action : A callable that defines the action to be performed when the rule is applicable. Defaults to :python:`None`.
        ignore_phase : If True, the rule will be evaluated even if it is not in the specified phase. Defaults to :python:`True`.
        priority : The priority of the rule. :py:attr:`RulePriority.NORMAL <classes.constants.RulePriority.NORMAL>`.
        description : A description of the rule. Defaults to :python:`"If its own condition is true calls one or more random child rules from the passed rules."`.
        overwrite_settings : A dictionary of settings to overwrite the default settings of the rule. Defaults to :python:`None`.
        cooldown_reset_value : The value to reset the cooldown of the rule. Defaults to :python:`None`.
        group : The group to which the rule belongs. Defaults to :python:`None`.
        enabled : If False, the rule will not be evaluated. Defaults to :python:`True`.
        weights : The weights associated with each rule when selecting random child rules. Defaults to :python:`None`.

    Raises:
        ValueError: When passing **rules** as a dict with weights, the **weights** argument must be None.
    """
    
    # TODO: add a dummy attribute for one additional weight, that skips the evaluation. Should only considered once.
    
    if TYPE_CHECKING:
        class _InitParameters(MultiRule._InitParameters):  # pyright: ignore[reportPrivateUsage]
            repeat_if_not_applicable: NotRequired[bool]
            weights: NotRequired[Optional[List[float]]]
    
    @singledispatchmethod
    def __init__(self,
                 phases: Union[Phase, Iterable[Phase]],  # /, # phases must be positional; python3.8+ only
                 rules: Union[Dict[Rule, float], List[Rule]],
                 repeat_if_not_applicable: bool = True,
                 condition: Optional[Callable[[Context], Any]] = None,
                 *,
                 action: Optional[Callable[[Context], Any]] = None,
                 ignore_phase: bool = True,
                 priority: RulePriority = RulePriority.NORMAL,
                 description: str = "If its own condition is true calls one or more random child rules from the passed rules.",
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 self_config: Optional[Dict[str, Any]] = None,
                 cooldown_reset_value: Optional[int] = None,
                 group: Optional[str] = None,
                 enabled: bool = True,
                 weights: Optional[List[float]] = None
                 ):
        """
        Initializes a Rule object that can trigger one or more random child rules.
        
        Args:
            phases : The phase or phases in which the rule is applicable.
            rules : The set of rules from which to select random child rules.
            repeat_if_not_applicable : If False, only one rule will be evaluated even if it is not applicable. Defaults to :python:`True`.
            condition :
                A callable that determines if the rule is applicable in a given context.
                If None and the rule does not implement a `condition` attribute the rule always executes.
                Defaults to :python:`None`.
            action : A callable that defines the action to be performed when the rule is applicable. Defaults to :python:`None`.
            ignore_phase : If True, the rule will be evaluated even if it is not in the specified phase. Defaults to :python:`True`.
            priority : The priority of the rule. Defaults to :py:attr:`RulePriority.NORMAL <classes.constants.RulePriority.NORMAL>`.
            description : A description of the rule. Defaults to :python:`"If its own condition is true calls one or more random child rules from the passed rules."`.
            overwrite_settings : A dictionary of settings to overwrite the default settings of the rule. Defaults to :python:`None`.
            cooldown_reset_value : The value to reset the cooldown of the rule. Defaults to :python:`None`.
            group : The group to which the rule belongs. Defaults to :python:`None`.
            enabled : If False, the rule will not be evaluated. Defaults to :python:`True`.
            weights : The weights associated with each rule when selecting random child rules. Defaults to :python:`None`.
        """
        if isinstance(rules, dict):
            if weights is not None:
                raise ValueError("When passing rules as a dict with weights, the weights argument must be None")
            self.weights = list(accumulate(rules.values()))  # cumulative weights for random.choices are more efficient
            self.rules = list(rules.keys())
        else:
            self.weights = weights or list(accumulate(r.priority for r in rules))
            self.rules = rules
        self.repeat_if_not_applicable = repeat_if_not_applicable
        super().__init__(phases, rules, condition=condition, action=action, description=description, priority=priority, ignore_phase=ignore_phase, overwrite_settings=overwrite_settings, self_config=self_config, cooldown_reset_value=cooldown_reset_value, enabled=enabled, group=group)

    @__init__.register(_CountdownRule)
    @__init__.register(type)
    def __init_by_decorating_class(self, cls: "RandomRule"):  # pyright: ignore[reportUnusedFunction]
        phases = getattr(cls, "phases", getattr(cls, "phase", None))
        cooldown_reset_value = getattr(cls, "cooldown_reset_value", getattr(cls, "max_cooldown", None))
        
        assert hasattr(cls, "condition"), f"Class {cls} has no condition attribute. It must be provided."
        self.__init__(phases, cls.rules, repeat_if_not_applicable=cls.repeat_if_not_applicable,
                      condition=cls.condition,
                      description=cls.description,
                      overwrite_settings=getattr(cls, "overwrite_settings", None),
                      self_config=getattr(cls, "self_config", None),
                      priority=getattr(cls, "priority", RulePriority.NORMAL),
                      cooldown_reset_value=cooldown_reset_value, group=getattr(cls, "group", None),
                      enabled=getattr(cls, "enabled", True),
                      prior_action=getattr(cls, "prior_action", None),
                      ignore_phase=getattr(cls, "ignore_phase", True))
    
    @__init__.register(Mapping)
    def __init_from_mapping(self, cls: "_InitParameters"):  # pyright: ignore[reportUnusedFunction]
        self.__init__(cls.get("phases", cls.get("phase")),
                      cls["rules"],
                      repeat_if_not_applicable=cls.get("repeat_if_not_applicable", True),
                      condition=cls.get("condition"),
                      description=cls.get("description", self.description),
                      overwrite_settings=cls.get("overwrite_settings"),
                      self_config=cls.get("self_config"),
                      priority=cls.get("priority", RulePriority.NORMAL),
                      cooldown_reset_value=cls.get("cooldown_reset_value"),
                      group=cls.get("group"),
                      enabled=cls.get("enabled", True),
                      sort_rules_by_priority=cls.get("sort_rules_by_priority", True),
                      execute_all_rules=cls.get("execute_all_rules", False),
                      prior_action=cls.get("prior_action", None),
                      ignore_phase=cls.get("ignore_phase", True))

    def evaluate_children(self, ctx: Context, overwrite: Optional[Dict[str, Any]] = None) -> Any:
        """
        Evaluate a random child rule.
        If `self.repeat_if_not_applicable=False` and the randomly chosen rule is not applicable,
        then no further rules are evaluated
        For `self.repeat_if_not_applicable=False` possible rules are evaluated in a random fashion
        until one rule was applicable.
        """
        if len(self.rules) == 0:
            logger.warning("No rules to evaluate in %s. Returning NOT_APPLICABLE.", self.__class__.__name__)
            return RuleResult.NOT_APPLICABLE
        if self.repeat_if_not_applicable:
            rules = self.rules.copy()
            weights = self.weights.copy()
        else:
            rules = self.rules
            weights = self.weights

        result = RuleResult.NOT_APPLICABLE
        while rules:
            rule = random.choices(rules, cum_weights=weights, k=1)[0]
            try:
                result = rule(ctx, overwrite, ignore_phase=self.ignore_phase)  # NOTE: Context action/evaluation results only store result of LAST rule
            except DoNotEvaluateChildRules:
                return None
            if not self.repeat_if_not_applicable or result is not Rule.NOT_APPLICABLE:
                # break after the first rule of `self.repeat_if_not_applicable=False`
                # else break if it was applicable.
                break
            rules.remove(rule)
            weights = list(accumulate(r.priority for r in rules))
        return result


class BlockingRule(Rule, metarule=True):
    """
    This meta rule allows to define rules that are able to takeover the agent's workflow and
    apply the :py:class:`.VehicleControl` directly from withhin the rule.
    
    """

    _gameframework: ClassVar[Union["GameFramework", "CallableProxyType[GameFramework]", None]] = None
    """
    Set when a :py:class:`GameFramework` is initialized.
    Alternatively can be set when any BlockingRule is created.
    """

    ticks_passed: int
    """Count how many ticks have been performed by this rule and blocked the agent."""
    
    MAX_TICKS = 5000  # 5000 * 1/20 = 250 seconds
    """
    The amount of ticks that can be performed by this rule before it is automatically disabled.
    If the rule has looped for this amount of ticks if will then call :py:attr:`max_tick_callback`
    and raise an :py:exc:`.UnblockRuleException` afterwards.
    
    As a hack :py:attr:`max_tick_callback` can change :py:attr:`ticks_passed` to prevent the
    exception and continue the rule.
    """
    
    max_tick_callback: Optional[Callable[[Self, Context], Any]] = None
    """
    An optional callback that is executed when :py:attr:`ticks_passed` reaches :py:attr:`MAX_TICKS`.
    """

    if TYPE_CHECKING:
        class _InitParameters(Rule._InitParameters):   # pyright: ignore[reportPrivateUsage]
            gameframework: Required[Optional[GameFramework]]

    @singledispatchmethod
    def __init__(self,
                 phases: Union[Phase, Iterable[Phase]],  # iterable of Phases
                 #/, # phases must be positional; python3.8+ only
                 condition: Optional[ConditionFunctionLikeT] = None,
                 action: Optional[Union[CallableAction[Self, []],
                                        Dict[Any, CallableAction[Self, []]]]] = None,
                 false_action: Optional[CallableAction[Self, []]] = None,
                 *,
                 gameframework: Optional[GameFramework],
                 actions: Optional[Dict[Any, CallableAction[Rule, []]]] = None,
                 description: str = "What does this rule do?",
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 self_config: Optional[Dict[str, Any]] = None,
                 priority: RulePriority = RulePriority.NORMAL,
                 cooldown_reset_value: Optional[int] = None,
                 group: Optional[str] = None,
                 enabled: bool = True,
                 ):
        super().__init__(phases, condition, action, false_action,
                         actions=actions,
                         description=description, overwrite_settings=overwrite_settings,
                         self_config=self_config,
                         priority=priority,
                         cooldown_reset_value=cooldown_reset_value,
                         group=group,
                         enabled=enabled)
        if gameframework:
            BlockingRule._gameframework = gameframework
        if not GameFramework.clock or not GameFramework.display:
            # Not much we can do about it
            #logger.info("%s : GameFramework should be initialized before using this rule.", self.__class__.__name__)
            GameFramework.init_pygame()
        self.ticks_passed = 0

    @__init__.register(_CountdownRule)
    @__init__.register(type)
    def __init_by_decorating_class(self, cls: "BlockingRule"):  # pyright: ignore[reportUnusedFunction]
        """
        Initialize by passing a Rule or class object to the __init__ method.
        
        This allows the usage of the @Rule decorator and easy copying.
        """
        phases = getattr(cls, "phases", getattr(cls, "phase", None))  # allow for both
        cooldown_reset_value = getattr(cls, "cooldown_reset_value", getattr(cls, "max_cooldown", None))
        assert hasattr(cls, "condition"), f"Class {cls} has no condition attribute. It must be provided."
        self.__init__(phases,
                      cls.condition,  # type: ignore
                      action=getattr(cls, "action", None), false_action=getattr(cls, "false_action", None),
                      gameframework=getattr(cls, "gameframework", BlockingRule._gameframework),
                      actions=getattr(cls, "actions", None), description=cls.description,
                      overwrite_settings=getattr(cls, "overwrite_settings", None),
                      self_config=getattr(cls, "self_config", None),
                      priority=getattr(cls, "priority", RulePriority.NORMAL),
                      cooldown_reset_value=cooldown_reset_value,
                      group=getattr(cls, "group", None), enabled=getattr(cls, "enabled", True))
        
    @__init__.register(Mapping)
    def __init_from_mapping(self, cls: "_InitParameters"):  # pyright: ignore[reportUnusedFunction]
        super().__init__(cls.get("phases", cls.get("phase")), **cls)
    
    def _render_everything(self, ctx: Context):
        if self._gameframework:
            self._gameframework.render_everything()
        else:
            world_model = ctx.agent._world_model  # pyright: ignore[reportPrivateUsage]
            display = GameFramework.display
            world_model.tick(GameFramework.clock)  # does not tick the world!
            world_model.render(display, finalize=False)
            try:
                world_model.controller.render(display)  # type: ignore[attr-defined]  # noqa: SIM105
            except AttributeError:
                pass
            
            dm_render_conf = world_model._args.camera.hud.detection_matrix  # pyright: ignore[reportPrivateUsage]
            if dm_render_conf and ctx.agent:
                ctx.agent.render_detection_matrix(display, **dm_render_conf)  # pyright: ignore[reportPrivateUsage]
            world_model.finalize_render(display)
        pygame.display.flip()

    @overload
    def loop_agent(self, ctx: Context, control: Optional[carla.VehicleControl] = None,
                   *, execute_planner: Literal[True], execute_phases: Any) -> carla.VehicleControl:
        ...
        
    @overload
    def loop_agent(self, ctx: Context, control: Optional[carla.VehicleControl] = None,
                   *, execute_planner: Literal[False], execute_phases: Any) -> None:
        ...

    def loop_agent(self, ctx: Context, control: Optional[carla.VehicleControl] = None,
                   *, execute_planner: bool, execute_phases: Any = True) -> "carla.VehicleControl | None":
        """
        A combination of `LunaticAgent.parse_keyboard_input`, `LunaticAgent.apply_control`, `BlockingRule.update_world`,
        and `Context.get_or_calculate_control` to advance agent and world.
        
        Args:
            ctx (Context): The current context object
            control (Optional[carla.VehicleControl], optional): The control to apply; will overwrite the context's control.
                If None takes the context's control.
                Defaults to :python:`None`.
        
        See Also:
            Executes the following methods:
        
            1. :py:meth:`.LunaticAgent.parse_keyboard_input`
            2. :py:meth:`.LunaticAgent.apply_control`
            3. :py:meth:`.BlockingRule.update_world` ticks the :py:class:`carla.World` and renders everything.
            4. :py:meth:`.Context.get_or_calculate_control` to acquire the :py:class:`carla.VehicleControl` object.
        """
        ctx.agent.parse_keyboard_input(control=control)  # NOTE: if skipped the user has no option to stop the agent
        ctx.agent.apply_control(control)
            
        # NOTE: This ticks the world forward by one step
        # The ctx.control is reset to None; execute_plan
        # > Phase.UPDATE_INFORMATION | Phase.BEGIN
        self.update_world(ctx, execute_phases=execute_phases)
        if execute_planner:
            return ctx.get_or_calculate_control()
        return None

    @staticmethod
    def get_world() -> carla.World:
        """Method to access the world object"""
        return CarlaDataProvider.get_world()

    def _begin_tick(self, ctx: Context):
        self._gameframework.clock.tick()  # self.args.fps)  # type: ignore[attr-defined]
        frame = None
        if self._gameframework and self._gameframework._args.handle_ticks:  # i.e. no scenario runner doing it for us
            if CarlaDataProvider.is_sync_mode():
                frame = self.get_world().tick()
            else:
                frame = self.get_world().wait_for_tick().frame
            CarlaDataProvider.on_carla_tick()
        else:
            # CRITICAL: The framework expects a return value before it ticks the world,
            # however the blocking rules should take over the ticks; so it should still do this!
            # TODO: Should implement some return <-> pass trough mechanism; maybe implement a
            # generator-like variant of the rule.
            if CarlaDataProvider.is_sync_mode():
                frame = self.get_world().tick()
            else:
                frame = self.get_world().wait_for_tick().frame
            CarlaDataProvider.on_carla_tick()

        if CarlaDataProvider.is_sync_mode():
            # We do this only in sync mode as frames could pass between gathering this information
            # and an agent calling InformationManager.tick(), which in turn calls global_tick
            # with possibly a DIFFERENT frame wasting computation.
            if frame is None:
                frame = self.get_world().get_snapshot().frame
            InformationManager.global_tick(frame)

        # Tick world and render everything
        # control should be reset, we are at the "start of the tick again"
        ctx.set_control(None)
        self.ticks_passed += 1

    def update_world(self, ctx: Context, *, execute_phases: Union[bool, Container[Phase]] = True) -> "carla.VehicleControl | None":
        """
        Ticks the world and takes care of the rendering.
    
        Will call
            - :python:`ctx.agent.execute_phase(Phase.CUSTOM_CYCLE | Phase.BEGIN, prior_results=<this Rule instance>)`
            - :py:meth:`.LunaticAgent.update_information`, with or without executing the phases, depending on **execute_phases**.

        Args:
            ctx: The context to use
            execute_update_information:
                Whether to execute the :python:`Phase.UPDATE_INFORMATION | Phase.[BEGIN|END]` with this function.
                Can also be a container containing one of both of these phases.
                Defaults to :python:`True`.

        Raises:
            UnblockRuleException: If the ticks passed are over :py:attr:`MAX_TICKS`
            
        Attention:
            The usage with Leaderboard_ is working but experimental.
            The scenario expects the agent to return a control object in every step, however as this rule
            takes over the ticks completely an outside ScenarioManager might not work as expected.
        """
        self._begin_tick(ctx)
        ctx.agent.execute_phase(Phase.CUSTOM_CYCLE | Phase.BEGIN, prior_results=self)

        # Update the agent's information
        if execute_phases and (execute_phases is True or Phase.UPDATE_INFORMATION | Phase.BEGIN in execute_phases):
            ctx.agent.execute_phase(Phase.UPDATE_INFORMATION | Phase.BEGIN, prior_results=self)
        ctx.agent._update_information()
        if execute_phases and Phase.UPDATE_INFORMATION | Phase.END not in self.phases:
            ctx.agent.execute_phase(Phase.UPDATE_INFORMATION | Phase.END, prior_results=self)
        if self.ticks_passed > self.MAX_TICKS:
            logger.info("Rule %s has passed its max_ticks %s, calling max_tick_callback and unblocking it", self, self.MAX_TICKS)
            if self.max_tick_callback:
                self.max_tick_callback(ctx)
                if self.ticks_passed > self.MAX_TICKS:
                    raise UnblockRuleException
                # max_tick_callback can override the ticks passed
            else:
                raise UnblockRuleException
        
        self._render_everything(ctx)

    def __call__(self, ctx: Context, overwrite: Optional[Dict[str, Any]] = None, in_loop: bool = False,
                 *,  # Kwargs from Rule.__call__
                 ignore_phase: bool = False,
                 ignore_cooldown: bool = False) -> Union[Any, Literal[RuleResult.NOT_APPLICABLE]]:
        if not in_loop:
            self.ticks_passed = 0
        else:
            ignore_phase = True
            ignore_cooldown = True
        if self in ctx.agent._active_blocking_rules:
            logger.warning("Rule %s is already blocking the agent, this is a recursive call. Not executing the rule.", self)
            return Rule.NOT_APPLICABLE
        try:
            return super().__call__(ctx, overwrite, ignore_phase=ignore_phase, ignore_cooldown=ignore_cooldown)
        except UnblockRuleException as e:
            return e.result
        finally:
            ctx.agent._active_blocking_rules.discard(self)  # pyright: ignore[reportPrivateUsage]
            
    def evaluate(self, ctx: Context, overwrite: Optional[Dict[str, Any]] = None) -> Union[bool, Hashable, Literal[RuleResult.NO_RESULT]]:
        result = super().evaluate(ctx, overwrite)
        if result in self.actions:
            ctx.agent._active_blocking_rules.add(self)  # pyright: ignore[reportPrivateUsage]
        return result

# Provide necessary imports for the evaluation_function module and prevents circular imports

import classes.evaluation_function as __evaluation_function  # noqa
__evaluation_function.Rule = Rule
__evaluation_function.Context = Context
del __evaluation_function
