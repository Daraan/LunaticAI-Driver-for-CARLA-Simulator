from __future__ import annotations # todo: can this be removed?

from collections.abc import Mapping
from dataclasses import is_dataclass
from functools import partial, wraps

from carla.libcarla import VehicleControl
import omegaconf

from launch_tools import CarlaDataProvider
import pygame

from classes.exceptions import DoNotEvaluateChildRules, LunaticAgentException, SkipInnerLoopException, UnblockRuleException
from classes.worldmodel import GameFramework

try: # Python 3.8+
    from functools import singledispatchmethod
except ImportError:
    from launch_tools import singledispatchmethod
    
import random
import inspect
from inspect import isclass
from itertools import accumulate
from typing import Any, ClassVar, FrozenSet, List, Set, Tuple, Union, Iterable, Callable, Optional, Dict, Hashable, TYPE_CHECKING
from weakref import WeakSet, proxy

from omegaconf import DictConfig, OmegaConf

from classes.constants import RULE_NO_RESULT, Hazard, Phase, NO_RESULT_TYPE as _NO_RESULT_TYPE, RulePriority
from classes.evaluation_function import ConditionFunction, TruthyConditionFunction
from agents.tools.logging import logger

from data_gathering.information_manager import InformationManager
if TYPE_CHECKING:
    import carla
    from agents.lunatic_agent import LunaticAgent
    from agents.tools.config_creation import LunaticAgentSettings, LiveInfo, RuleConfig, ContextSettings
    from typing import override
    
    # Note: gameframework.py adds GameFramework to this module's variables
    # at this position it would be a circular import

class Context(CarlaDataProvider):
    """
    Object to be passed as the first argument (instead of self) to rules, actions and evaluation functions.
    
    The `Context` class derives from the scenario runner's [`CarlaDataProvider`](https://github.com/carla-simulator/scenario_runner/blob/master/srunner/scenariomanager/carla_data_provider.py) to allow access to the world, map, etc.
    
    Note: 
        That Context.config are read-only settings for the given condition and actions with potential overwrites.
    """
    
    agent : "LunaticAgent"
    """Gives access to the agent."""
    
    config : "ContextSettings"
    """A copy of the agents config. Overwritten by the condition's settings."""
    
    evaluation_results : Dict["Phase", Hashable] # ambiguous wording, which result? here evaluation result
    action_results : Dict["Phase", Any] 
    
    control : Optional["carla.VehicleControl"]
    """Current control the agent should use. Set by execute_phase(update_controls=...). Safeguarded to be not set to None."""
    _control : Optional["carla.VehicleControl"]
    """Current control the agent should use."""
    
    prior_result : Optional[Any] # TODO: maybe rename
    """Result of the current phase."""
    
    last_context : Optional["Context"]
    """The context object of the last tick. Used to access the last phase's results."""
    
    second_pass : bool = None
    """
    Whether or not the run_step function performs a second pass, i.e.
    after the route has been replanned.
    
    Warning: 
        The correctness should *not* be assumed. 
        The user is responsible for setting this value to True if a second pass is required.
    """
    
    _detected_hazards : Set[Hazard]
    """
    Detected hazards in the current phase.
    
    If not empty at the end of the inner step an EmergencyStopException is raised.
    """
    
    detected_hazards_info : Dict[Hazard, Any]
    """Information about the detected hazards."""

    def __init__(self, agent : "LunaticAgent", **kwargs):
        self.agent = agent
        self._control = kwargs.pop("control", None)
        self._init_arguments = kwargs
        self.evaluation_results = {}
        self.action_results = {}
        self.last_phase_evaluation_results = {}
        self.last_phase_action_results = {}
        self.detected_hazards = set()
        self.detected_hazards_info = {h: None for h in Hazard}
        self.__dict__.update(kwargs)

    @property
    def current_phase(self) -> "Phase":
        """Current phase the agent is in"""
        return self.agent.current_phase
    
    @property
    def control(self) -> Union["carla.VehicleControl", None]:
        """
        Control the agent currently should use. 
        
        Setting it to None directly is discouraged. 
        Use `set_control` to set it to None.
        """
        return self._control
    
    @control.setter
    def control(self, control : "carla.VehicleControl"):
        if control is None:
            raise ValueError("Context.control must not be None. To set it to None explicitly use set_control.")
        self._control = control
        
    def set_control(self, control : Optional["carla.VehicleControl"]):
        """Set the control, allows to set it to None."""
        self._control = control
        
    def get_or_calculate_control(self) -> "carla.VehicleControl":
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
            - [LunaticAgent.calculate_control](#LunaticAgent.calculate_control)
        """
        if self.control:
            return self.control
        self.control = self.agent._calculate_control()
        return self.control
        
    @property
    def detected_hazards(self) -> Set[Hazard]:
        """
        Detected hazards in the current phase.
        
        If not empty at the end of the inner step an EmergencyStopException is raised.
        """
        return self._detected_hazards
    
    @detected_hazards.setter
    def detected_hazards(self, hazards : Set[Hazard]):
        if not isinstance(hazards, set):
            raise TypeError("detected_hazards must be a set of Hazards.")
        self._detected_hazards = hazards
    
    def end_of_phase(self): # TODO: keep or remove? unused
        self.last_phase_action_results = self.action_results.copy()
        self.last_phase_evaluation_results = self.evaluation_results.copy()
        self.evaluation_results.clear()
        self.action_results.clear()

    # Convenience function when using detect_vehicles
    from agents.tools.lunatic_agent_tools import max_detection_distance

    @property
    def live_info(self) -> "LiveInfo":
        return self.config.live_info
    
    @property
    def active_blocking_rules(self) -> List["BlockingRule"]:
        return self.agent._active_blocking_rules
    
   
@ConditionFunction
def always_execute(ctx : Context): # pylint: disable=unused-argument
    """This is an `ConditionFunction` that always returns True. It can be used to always execute an action."""
    return True


class _CountdownRule:

    # TODO: low prio: make cooldown dependant of tickrate or add a conversion from seconds to ticks OR make time-based
    tickrate : ClassVar[int] = NotImplemented

    DEFAULT_COOLDOWN_RESET : ClassVar[int] = 0
    """Value the cooldown is reset to when `reset_cooldown` is called without a value."""
    
    start_cooldown : ClassVar[int] = 0
    """Initial Cooldown when initialized. if >0 the rule will not be ready for the first start_cooldown ticks."""

    _instances : ClassVar[WeakSet["_CountdownRule"]] = WeakSet()
    """Keep track of all instances for the cooldowns"""
    
    _cooldown : int
    """If 0 the rule is ready to be executed."""
    
    blocked : bool = False # NOTE: not a property
    """Indicates if the rule is blocked for this tick only. Is reset to False after the tick."""

    def __init__(self, cooldown_reset_value: Optional[int] = None, enabled: bool = True):
        self._instances.add(self)
        self._cooldown = self.start_cooldown
        self.max_cooldown = cooldown_reset_value or self.DEFAULT_COOLDOWN_RESET
        self._enabled = enabled

    def is_ready(self) -> bool:
        """Group aware check if a rule is ready."""
        return self.cooldown == 0 and self.enabled and not self.blocked # Note: uses property getters. Group aware for GroupRules
    
    def reset_cooldown(self, value:Optional[int]=None):
        if value is None:
            self._cooldown = self.max_cooldown
        elif value >= 0:
            self._cooldown = int(value)
        else:
            raise ValueError("Cooldown value must be a None or a non-negative integer.")

    @property
    def cooldown(self) -> int:
        """
        Cooldown of the rule in ticks until it can be executed again after its action was executed.
        If 0 the rule is ready to be executed.
        """
        return self._cooldown
    
    @cooldown.setter
    def cooldown(self, value):
        self._cooldown = value
    
    def update_cooldown(self):
        """Update the cooldown of *this* rule."""
        if self._cooldown > 0:
            self._cooldown -= 1
    
    @classmethod
    def update_all_cooldowns(cls):
        """Updates the cooldown of *all* rules."""
        for instance in cls._instances:
            instance.update_cooldown()
            
    @classmethod
    def unblock_all_rules(cls):
        """Unblocks all rules"""
        for instance in cls._instances:
            instance.blocked = False
            
    @property
    def enabled(self) -> bool:
        """If False the rule will not be evaluated. Contrary to `blocked` it will not be reset after the tick."""
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
    
    def set_active(self, value: bool):
        """Enables or disables the rule. Contrary to `blocked` it will not be reset after the tick."""
        self._enabled = value
    
    class CooldownFramework:
        """Context manager that can reduce all cooldowns at the end of a `with` statement."""

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.tick()
        
        @staticmethod
        def tick():
            Rule.update_all_cooldowns()
            Rule.unblock_all_rules()
                

class _GroupRule(_CountdownRule):
    group : Optional[str] = None # group of rules that share a cooldown
    """
    Group name of rules that should share their cooldown.
    
    None for a rule to not share its cooldown.
    """

    # first two values in the list are current and max cooldown, the third is a set of all instances
    _group_instances : ClassVar[Dict[str, List[int, int, WeakSet["_GroupRule"]]]] = {}
    """
    Dictionary of all group instances. Key is the group name. 
    
    Value is a list of the current cooldown, the max cooldown for reset and a WeakSet of all instances.
    """
    
    def __init__(self, group :Optional[str]=None, cooldown_reset_value: Optional[int] = None, enabled: bool = True):
        super().__init__(cooldown_reset_value, enabled)
        self.group = group
        if group is None:
            return
        if group not in self._group_instances:
            self._group_instances[group] = [0, self.max_cooldown, WeakSet()]
        self._group_instances[group][2].add(self) # add to weak set

    @property
    def cooldown(self) -> int:
        """
        Cooldown of the rule in ticks until it can be executed again after its action was executed.
        If 0 the rule is ready to be executed.
        """
        if self.group:
            return _GroupRule._group_instances[self.group][0]
        return super().cooldown
    
    @property
    def has_group(self) -> bool:
        return self.group is not None
    
    @cooldown.setter
    def cooldown(self, value):
        if self.group:
            _GroupRule._group_instances[self.group][0] = value
            return
        super().cooldown = value
    
    def set_my_group_cooldown(self, value: Optional[int]=None):
        """Update the cooldown of the group this rule belong to"""
        if value is None:
            self._group_instances[self.group][0] = self._group_instances[self.group][1] # set to max
        else:
            self._group_instances[self.group][0] = value

    def reset_cooldown(self, value:Optional[int]=None):
        """Reset or set the cooldown"""
        if self.group:
            self.set_my_group_cooldown(value)
        else:
            super().reset_cooldown()

    @classmethod
    def set_cooldown_of_group(cls, group: str, value: int):
        """Updates the cooldown of the specified group."""
        if group in cls._group_instances:
            cls._group_instances[group][0] = value
        else:
            raise ValueError(f"Group {group} does not exist.")

    __filter_not_ready_instances = lambda instance: instance.group is None and instance._cooldown > 0
    """Filter function to get all instances that are not ready. see `update_all_cooldowns`."""

    @classmethod
    def update_all_cooldowns(cls):
        """Globally updates the cooldown of *all* rules."""
        # Update Groups
        for instance_data in cls._group_instances.values():
            if instance_data[0] > 0:
                instance_data[0] -= 1
        for instance in filter(cls.__filter_not_ready_instances, cls._instances):
            instance._cooldown -= 1


class Rule(_GroupRule):
    _auto_init_: ClassVar[bool] = True
    """
    If set to False the automatic __init__ creation is disabled when subclassing.
    This automatic __init__ will fix parameters like `phases` and `rule` to the class.
    
    Declaring an `__init__` method in the class has the same effect as setting `_auto_init_` to False.
    
    Note:
        Using `class NewRuleType(metaclass=Rule)` equivalent to `_auto_init_=False`, but is not inherited.
    """
    
    # Indicate that no rule was applicable in the current phase
    # i.e.  rule(ctx) in actions was False 
    NOT_APPLICABLE : ClassVar[object] = object()
    """Object that indicates that no action was executed."""
    
    NO_RESULT = RULE_NO_RESULT
    """Indicates that the action raised an exception."""
    
    _PROPERTY_MEMBERS : ClassVar[Set[str]] = {"cooldown", "has_group", "enabled"}
    """
    A subclass can only overwrite these attributes with properties. This prevents a user accidentally overwriting the property,
    e.g. `cooldown = 20` with a method or variable.
    
    TODO:
        Consider making enabled a variable and not a property.
    """
    
    description : str
    """Description of what this rule should do"""
    
    phases : FrozenSet["Phase"]
    """
    The phase or phases in which the rule should be evaluated.
    For instantiation the phases attribute can be any `Iterable[Phase]`.
    """
    
    phase : "Phase"
    """For the Class API the phase attribute be set to a single Phase object."""
    
    condition : ConditionFunction
    """
    The condition that determines if the rule's actions should be executed.
    
    Simple variant:
        return True if the action should be executed, False otherwise.
        if `false_action` is defined, False will execute `false_action`.
        
    Advanced variant:
        return a Hashable value that is used as key in the `actions` dict.
    """
    
    actions : Dict[Any, Callable[[Context], Any]]
    """Dictionary that maps rule results to the action that should be executed."""
    
    action : Optional[Callable[[Context], Any]]
    """Action that should be executed if the rule is True. If `actions` is set, this is ignored."""
    
    #group : Optional[str]
    #"""Group name for rules that should share their cooldown."""
    
    overwrite_settings : Dict[str, Any]
    """
    Settings that should overwrite the agent's settings for this rule.
    
    Note:
        The overwrite settings are dict objects, DictConfigs are converted to dict.
    """
    
    self_config : "RuleConfig"
    """
    A custom sub-config for the rule that is not included in the agents settings.
    Automatically gets a `instance` key added with the rule instance.
    
    Can be accessed via `ctx.config.current_rule` or `self.config.self`.
    
    Note:
        Internally `self.config` and `ctx.config` is the same object, which makes
        interpolations to the agent's settings possible.
        
    Warning:
        The `self_config` object is *not* constant it is recreated each time the
        rule is evaluated to have the current context available.
    """
    
    priority: RulePriority = RulePriority.NORMAL
    """Rules are executed in order of their priority, from high to low."""
    
    # Initialization functions
    
    _ctx : Optional[Context] = None
    """No hard attachment, to not keep the context objects alive, use with care. Check where it is set in a rule."""

    def clone(self):
        """
        Create a new instance of the rule with the same settings.
        
        Note: 
            - The current cooldown is not taken into account.
            - The current enabled state is taken into account.
        """
        return self.__class__(self) # Make use over overloaded __init__

    @singledispatchmethod
    def __init__(self, 
                 phases : Union["Phase", Iterable["Phase"]], # iterable of Phases
                 #/, # phases must be positional; python3.8+ only
                 condition : Optional[Union[ConditionFunction, Callable[[Context], Hashable]]]=None, 
                 action: Optional[Union[Callable[[Context], Any], Dict[Any, Callable]]] = None,
                 false_action: Optional[Callable[[Context], Any]] = None,
                 *, 
                 actions : Optional[Dict[Any, Callable[[Context], Any]]] = None,
                 description: str = "What does this rule do?",
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 self_config: Optional[Dict[str, Any]] = None,
                 priority: RulePriority = RulePriority.NORMAL,
                 cooldown_reset_value : Optional[int] = None,
                 group : Optional[str] = None,
                 enabled: bool = True,
                 ignore_chance = NotImplemented,
                 ):
        """
        Initializes a Rule object.

        Parameters:
        - phases: The phase(s) when the rule should be evaluated.
            An iterable of Phase objects or a single Phase object.
        - condition: A function that takes a Context object as input and returns a Hashable value. 
            If not provided, the class must implement a `condition` function.
        - action: A function or a dictionary of functions that take a Context object as input. 
            If `action` behaves like `actions`.
            Only one of `action` and `actions` can be set.
        - false_action: A function that takes a Context object as input and returns any value. 
            It is used when `action` is a single function and represents the action to be taken when the condition is False.
        - actions: A dictionary of `action` functions
            It should map the return values of `condition` to the corresponding action function. 
            If `action` is None, `actions` must be provided.
        - description: A string that describes what this rule does.
        - overwrite_settings: A dictionary of settings that will overwrite the 
            agent's setting for this Rule.
        - priority: The priority of the rule. It can be a float, an integer, or a RulePriority enum value.
        - cooldown_reset_value: An optional integer value that represents the cooldown reset value for the rule.
            If not provided falls back to the class attribute DEFAULT_COOLDOWN_RESET.
        - group: An optional string that specifies the group to which this rule belongs.
        - enabled: A boolean value indicating whether the rule is enabled or not.
        - ignore_chance: Not implemented.

        Raises:
        - ValueError: If `phases` is empty or None, or if `phases` contains an object that is not of type Phase.
        - TypeError: If `condition` is None and the class does not implement a `condition` function, or if both `action` and `actions` are None and the class does not have an `actions` attribute or an `action` function.
        - TypeError: if actions is not a Mapping object.
        - ValueError: If both `action` and `actions` are provided.
        - ValueError: If `action` is a Mapping and either `false_action` or `actions` is not None.
        - ValueError: If an action function is not callable.
        - ValueError: If `description` is not a string.
        """
        
        # Check phases
        if not phases:
            raise ValueError("phases must not be empty or None")
        if not isinstance(phases, frozenset):
            if isinstance(phases, Iterable):
                phases = frozenset(phases)
            else:
                phases = frozenset([phases]) # single element
        for p in phases:
            if not isinstance(p, Phase):
                raise ValueError(f"phase must be of type Phases, not {type(p)}")
        self.phases = phases
        
        # Check Rule
        if condition is None and not hasattr(self, "condition"):
            raise TypeError("%s.__init__() missing 1 required positional argument: 'condition'. Alternatively the class must implement a `condition` function." % self.__class__.__name__)
        
        if condition is not None and not hasattr(self, "condition"):
            self.condition = condition
        elif condition is not None and hasattr(self, "condition"):
            # Warn if cls.condition and passes condition are different
            self_func = getattr(self.condition, "__func__", getattr(self.condition, "func", self.condition))
            if self_func != condition: # Compare method with function
                logger.warning(f"Warning 'condition' argument passed but class {self.__class__.__name__} already implements a different function 'self.condition'. Overwriting {self.condition} with passed condition {getattr(condition, '__name__', str(condition))}. This might lead to undesired results.")
            
            # NOTE: IMPORTANT: self.condition = condition overwrites methods with functions
            # To keep methods as methods the condition parameter is removed with 
            # `do_not_overwrite.append("condition")` used during __init_subclass__
            # Could move this check also to here, however, it will then not be checked during class creation
            self.condition = condition
        
        # Check Actions
        if action is not None and actions is not None:
            try:
                if len(actions) == 1 and action is actions[True]:
                    logger.info("`action` and `actions` have been both been used when initializing %s. Did you use `condition.register_action`? Then you can omit the action parameter / attribute.", self)
                    action = None
                else:
                    raise ValueError("Only one of 'action' and 'actions' can be set.")
            except Exception as e:
                raise ValueError("Either only one of 'action' and 'actions' can be set, or actions[True] must be the same as action - other actions are currently not supported.") from e
        if action is None and actions is None and not hasattr(self, "actions"):
            # NOTE: the k in params check below is essential for this to work correctly.
            raise TypeError("%s.__init__() arguments `action` and `actions` are both None. Provide at least one argument alternatively the class must have an `actions` attribute or an `action` function." % self.__class__.__name__)

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
            self.actions = {}
            if action is not None:
                self.actions[True] = action
            if false_action is not None:
                self.actions[False] = false_action
        # actions can be the dict of the class, we do not want the same dict instance
        self.actions = dict(self.actions)
        
        # Assure that method(self, ctx) like functions are accessible like them
        for key, func in self.actions.items():
            if not callable(func):
                raise ValueError(f"Action for key {key} must be callable, not {type(func)}")
            if len(inspect.signature(func).parameters) >= 2:
                # NOTE: could use types.MethodType
                self.actions[key] = partial(func, self) # bind to self
        
        # Check Description
        if not isinstance(description, str):
            raise ValueError(f"description must be of type str, not {type(description)}")
        self.description = description
        super().__init__(group or self.group, cooldown_reset_value, enabled) # or self.group for subclassing
        self.priority : float | int | RulePriority = priority # used by agent.add_rule
        
        self.overwrite_settings = overwrite_settings or {}
        if not isinstance(self.overwrite_settings, dict):
            self.overwrite_settings = dict(self.overwrite_settings)
        if self_config and "self" in self.overwrite_settings and self.overwrite_settings["self"] != self_config:
            logger.debug("Warning: self_config and self.overwrite_settings['self'] must be the same object.")
        
        default_self_config = getattr(self, "self_config", getattr(self, "SelfConfig", {}))
        if isclass(default_self_config):
            if not is_dataclass(default_self_config):
                logger.warning(f"Class {self.__class__.__name__} has a self_config class that is not a dataclass. This might lead to undesired results, i.e. missing keys in the config.")
            default_self_config = default_self_config()
        if not isinstance(default_self_config, DictConfig):
            default_self_config = OmegaConf.create(default_self_config, flags={"allow_objects": True})
        if self_config:
            self.self_config = OmegaConf.merge(default_self_config, self_config)
        else:
            self.self_config = default_self_config
        assert self.self_config._get_flag("allow_objects"), "self_config must allow objects to be used as values."
        
        self.overwrite_settings["self"] = self.self_config
        self.overwrite_settings["self"]["instance"] = self
    
    def __new__(cls, phases=None, *args, **kwargs):
        """
        The @Rule decorator allows to instantiate a Rule class directly for easier out-of-the-box usage.
        Further check for metaclass initialization, else this is a normal instance creation.
        """
        # @Rule
        # class NewRuleInstance:
        if isclass(phases):
            if issubclass(phases, _CountdownRule):
                raise ValueError("When using @Rule the class may not be a subclass of Rule. Do not inherit from rule or subclass from Rule instead with the decorator."
                                 "Do not do:\n\t@Rule\n\tclass MyRule(>>Rule<<): ...\n" )
            decorated_class = phases

            # Create the new class, # NOTE: goes to __init_subclass__
            new_rule_class = type(decorated_class.__name__, (cls,), decorated_class.__dict__.copy(), init_by_decorator=True) # > calls init_subclass; copy() for correct type!
            return super().__new__(new_rule_class)
        # class NewRuleType(metaclass=Rule)
        if isinstance(phases, str):
            try:
                clsname = phases
                bases, clsdict = args[:2]
                new_rule_class = type(clsname, (cls,), clsdict, metaclass=True) # > calls init_subclass; copy() for correct type!
                return new_rule_class #
            except Exception:
                print("ERROR: If you want to initialize a rule be sure that you pass a Phase object as the first argument."
                      "A string assumes that you've used class NewSubclass(metaclass=Rule)")
                raise
        # Normal instance
        return super().__new__(cls)
    
    # Called on subclass creation. Can be used for class API
    def __init_subclass__(cls, init_by_decorator=False, metaclass=False):
        """
        Automatically creates a __init__ function to allow for a simple to use class-interface to create rule classes.
        
        By setting __auto_init_ = True in the class definition, the automatic __init__ creation is disabled.
        """
        if hasattr(cls, "phases") and hasattr(cls, "phase") and cls.phases and cls.phase:
            raise ValueError(f"Both 'phases' and 'phase' are set in class {cls.__name__}. Use only one. %s, %s" % (cls.phases, cls.phase))
        
        for attr in cls._PROPERTY_MEMBERS:
            if hasattr(cls, attr) and not hasattr(getattr(cls, attr), "__get__"):
                raise ValueError(f"Class {cls.__name__} has overwritten property {attr} with {getattr(cls, attr)}. You may only overwrite the following attributes with properties: {cls._PROPERTY_MEMBERS}."
                                 "Did you mean `start_cooldown` or `cooldown_reset_value` instead of `cooldown`?")
        if not cls._auto_init_ or metaclass: # TODO: Check for multirule, should _auto_init_ be set to False?
            return
        
        if "__init__" in cls.__dict__:
            custom_init = cls.__dict__["__init__"]
        else:
            custom_init = False
            
        do_not_overwrite = ["phases"]
        if hasattr(cls, "condition"):
            # Check if the condition should be treated as a method or function
            if isinstance(cls.condition, ConditionFunction):
                rule_func = cls.condition.evaluation_function
            else:
                rule_func = cls.condition
            
            # Decide method(self, ctx) vs. function(ctx)
            if hasattr(cls.condition, "use_self") and cls.condition.use_self is not None:
                condition_as_method = cls.condition.use_self # User decides
            else:
                params = len(inspect.signature(rule_func).parameters)
                if params >= 2:
                    if params > 2:
                        logger.warning(f"Rule {cls.condition.__name__} has more than 2 parameters. Treating it as a method(self, ctx, **kwargs) with self argument! To avoid this message or use it as a function use ConditionFunction(use_self=True|False) explicitly.")
                    condition_as_method = True
                else:
                    condition_as_method = False
            if condition_as_method:
                logger.debug("Implementing %s as method(self, ctx) - If you need it as a function(ctx, *args) decorate use @ConditionFunction(use_self=False).", cls.condition.__name__)
                do_not_overwrite.append("condition")
            else:
                # If the signature has only one parameter its clear it has to be a function; else its user decision.
                logger.info("Implementing %s as function(ctx) without a self argument - If you need it as a method(self, ctx, *args) decorate use @ConditionFunction(use_self=True).", cls.condition.__name__)
            
            # Actions provided by condition.actions, e.g. ConditionFunction.register_action
            if hasattr(cls.condition, "actions") and cls.condition.actions:
                if hasattr(cls, "actions") and cls.actions:
                    raise ValueError(f"Class {cls.__name__} already has an 'actions' attribute. It will be overwritten by the 'actions' attribute of the condition. This is the case if ConditionFunction.register_action has been used.")
                cls.actions = cls.condition.actions
                
        if not hasattr(cls, "description"):
            cls.description = cls.__doc__
            if not cls.description:
                cls.description = "No description provided."
        
        # Create a __init__ function that sets some of the parameters.
        params = inspect.signature(cls.__init__).parameters # find overlapping parameters
        
        # TODO: to be lazy Rule arguments need to be added to params so that "k in params" works
        
        @wraps(cls.__init__)
        def partial_init(self: Rule, phases=None, *args, **kwargs):
            # Need phases as first argument
            cls_phases = getattr(cls, "phases", None) # allow for both wordings
            cls_phase = getattr(cls, "phase", None)
            if init_by_decorator:
                # Using @Rule phases as first argument is the class
                phases = cls_phases or cls_phase
            else:
                if phases is None: # NOTE: Could be Phase.NONE
                    phases = cls_phases or cls_phase
            if phases is None:
                raise ValueError(f"`phases` or `phase` must be provided for class {cls.__name__}")
            # Removing condition to not overwrite it
            kwargs.update({k:v for k,v in cls.__dict__.items() if k in params and k not in do_not_overwrite})
            try:
                if custom_init:
                    custom_init(self, phases, *args, **kwargs)
                else:
                    super(cls, self).__init__(phases, *args, **kwargs) # note: could be single dispatch function
            except IndexError: # functools <= python3.10
                logger.error("\nError in __init__ of %s. Possible reason: Check if the __init__ method has the correct signature. `phases` must be a positional argument.\n", cls.__name__)
                raise
            except TypeError as e:
                # e.g. forgot a action, or rules attribute (MultiRule)
                if "missing" in str(e):
                    logger.error("Class %s has likely missing attributes that cannot be passed to init. Check if all required attributes are set in the class definition.", cls.__name__)
                raise e
        cls.__init__ = partial_init
    
    @__init__.register(_CountdownRule)
    @__init__.register(type)
    def __init_by_decorating_class(self, cls: "Rule"): # pylint: disable=unused-variable
        """
        Initialize by passing a Rule or class object to the __init__ method.
        
        This allows the usage of the @Rule decorator and easy copying.
        """
        phases = getattr(cls, "phases", getattr(cls, "phase", None)) # allow for spelling mistake
        cooldown_reset_value = getattr(cls, "cooldown_reset_value", getattr(cls, "max_cooldown", None))
        
        # TODO: Automate this via inspect.signature
        
        self.__init__(phases, cls.condition, getattr(cls, "action", None), getattr(cls, "false_action", None), actions=getattr(cls, "actions", None), description=cls.description, overwrite_settings=getattr(cls, "overwrite_settings", None), self_config=getattr(cls, "self_config", None), priority=getattr(cls, "priority", RulePriority.NORMAL), cooldown_reset_value=cooldown_reset_value, group=getattr(cls, "group", None), enabled=getattr(cls, "enabled", True))
        
    @__init__.register
    def __init_from_mapping(self, cls:Mapping): # pylint: disable=unused-variable
        # NOTE: This is weakly tested and not much supported.
        self.__init__(cls.get("phases", cls.get("phase")), cls["condition"], cls.get("action"), cls.get("false_action"), actions=cls.get("actions"), description=cls["description"], overwrite_settings=cls.get("overwrite_settings"), self_config=cls.get("self_config"),  priority=cls.get("priority", RulePriority.NORMAL), cooldown_reset_value=cls.get("cooldown_reset_value"), group=cls.get("group"), enabled=cls.get("enabled", True))        


    # -----------------------
    
    @classmethod
    def get_init_signature(cls):
        """
        Get the signature of the __init__ function.
        
        Returns:
            The signature of the __init__ function.
        """
        return inspect.signature(cls.__init__).parameters.keys()

    def execute_phase(self, *args, **kwargs):
        """
        Helper function to execute a phase from within a rule.
        
        Use with care to avoid loops or recursions.
        """
        try:
            self._ctx.agent.execute_phase(*args, **kwargs)
        except AttributeError:
            logger.exception("Error in Rule.execute_phase. Weakproxy might have been deleted")
            

    # -----------------------
    # Evaluation functions
    # -----------------------

    def evaluate(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None) -> Union[bool,Hashable, _NO_RESULT_TYPE]:
        self._ctx = proxy(ctx)
        settings = self.overwrite_settings.copy()
        if overwrite:
            settings.update(overwrite)
        if settings:
            ctx.config = OmegaConf.merge(ctx.agent.config, settings) # NOTE: if you got an error check if you used `"setting.subsetting" : value` instead of `settings : { subsetting: value}`. NO DOT NOTATION FOR KEYS!
        else:
            # If settings is empty the more expensive merge is not necessary.
            ctx.config = ctx.agent.config.copy()
            
        # NOTE: # TODO: this creates a hardlink, which means that the memory is not freed when ctx.config is updated!
        # Solution: can make self_config a weakproxy and store a parentless copy in self.overwrite_settings["self"]
        self.self_config = self.overwrite_settings["self"] = ctx.config["self"]
        #assert self.self_config is self.overwrite_settings["self"]; this works if overwrite_settings is a dict
        
        OmegaConf.set_readonly(ctx.config, True) # only the original agent.config can be modified. Make clear that these have no permanent effect.
        # The Rule's settings should be dynamic.
        OmegaConf.set_readonly(self.self_config, False)
        
        result = self.condition(ctx)
        return result
    
    def evaluate_children(self, ctx : Context):
        raise NotImplementedError("This method should be implemented in a subclass")

    def __call__(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None, *, ignore_phase=False, ignore_cooldown=False) -> Any:
        # Check phase
        assert ignore_phase or ctx.agent.current_phase in self.phases
        
        if not self.is_ready() and not ignore_cooldown:
            return self.NOT_APPLICABLE
        if not ignore_phase and ctx.agent.current_phase not in self.phases: #NOTE: This is currently never False as checked in execute_phase and the agents dictionary.
            return self.NOT_APPLICABLE # not applicable for this phase

        exception = None
        result = Rule.NO_RESULT
        try:
            result = self.evaluate(ctx, overwrite)
        except BaseException as e:
            exception = e
        except LunaticAgentException as e:
            exception = e
        else:
            ctx.evaluation_results[ctx.agent.current_phase] = result
            if result in self.actions:
                self.reset_cooldown()
                action_result = self.actions[result](ctx) #todo allow priority, random chance
                ctx.action_results[ctx.agent.current_phase] = action_result
                return action_result
            return self.NOT_APPLICABLE # No action was executed
        finally:
            self._ctx = None
            if exception:
                self.reset_cooldown() # 
                raise exception
    # 
    
    def __str__(self) -> str:
        try:
            if isinstance(self.condition, partial):
                return self.__class__.__name__ + f"(description='{self.description}', phases={self.phases}, group={self.group}, priority={self.priority}, actions={self.actions}, condition={self.condition.func}, cooldown={self.cooldown})"
            return self.__class__.__name__ + f"(description='{self.description}', phases={self.phases}, group={self.group}, priority={self.priority}, actions={self.actions}, condition={self.condition.__name__}, cooldown={self.cooldown})" 
        except AttributeError as e:
            logger.warning(str(e))
            return self.__class__.__name__ + "(Error in condition.__str__: Rule has not been initialized correctly. Missing attributes: " + str(e) + ")"

    def __repr__(self) -> str:
        return str(self)
    

    

class MultiRule(metaclass=Rule):

    rules : List[Rule]
    """The list of child rules to be called if this rule's condition is true."""
    
    def _wrap_action(self, action: Callable[[Context], Any]):
        """
        Wrap the passed action.
        First the action is executed afterwards the child rules are evaluated.
        
        Note:
            There is no extra condition that is checked between the two actions.
        """
        @wraps(action)
        def wrapper(ctx : Context, *args, **kwargs) -> Any:
            try:
                result = action(ctx, *args, **kwargs)
            except DoNotEvaluateChildRules as e:
                return e, None
            else:
                results = self.evaluate_children(ctx) # execute given rules as well
            return result, results
        return wrapper

    @singledispatchmethod
    def __init__(self, 
                 phases: Union["Phase", Iterable], 
                 #/, # phases must be positional; python3.8+ only
                 rules: List[Rule], 
                 condition : Optional[Callable[[Context], Any]] = None,
                 *,
                 description: str = "If its own condition is true calls the passed rules.",
                 priority: RulePriority = RulePriority.NORMAL, 
                 sort_rules : bool = True,
                 execute_all_rules = False,
                 action : Optional[Callable[[Context], Any]] = None,
                 ignore_phase : bool = True,
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 self_config: Optional[Dict[str, Any]] = None,
                 cooldown_reset_value : Optional[int] = None,
                 group : Optional[str] = None,
                 enabled: bool = True,
                 ):
            """
            Initializes a Rule object that can have further rules as children.

            Args:
                phases (Union[Phase, Iterable]): The phase or phases in which the rule should be active.
                rules (List[Rule]): The list of child rules to be called if the rule's condition is true.
                condition (Callable[[Context]], optional): The condition that determines if the rules should be evaluated. Defaults to always_execute.
                execute_all_rules (bool, optional): 
                    If False will only execute the first rule with a applicable condition, i.e. this MultiRule is like a node in a decision tree.
                    If True all rules are evaluated, unless one raises a `DoNotEvaluateChildRules` exception.
                    Defaults to False.
                sort_rules (bool, optional): Flag indicating whether to sort the rules by priority. Defaults to True.
                action (Callable[[Context]], optional): The action to be executed before the passed rules are evaluated. Defaults to None.
                ignore_phase (bool, optional): Flag indicating whether to ignore the Phase of the passed child rules. Defaults to True.
                overwrite_settings (Dict[str, Any], optional): Additional settings to overwrite the agent's settings. Defaults to None.
                priority (RulePriority, optional): The priority of the rule. Defaults to RulePriority.NORMAL.
                description (str, optional): The description of the rule. Defaults to "If its own rule is true calls the passed rules.".
                group (str | None, optional): The group name of the rule. Defaults to None.
                enabled (bool, optional): Flag indicating whether the rule is enabled after creation. Defaults to True.
            """
            self.ignore_phase = ignore_phase
            if rules is None:
                logger.warning("Warning: No rules passed to %s: %s. You can still add rules to the rules attribute later.", self.__class__.mro()[1].__name__, self.__class__.__name__) 
                rules = []
            self.rules = rules
            self.execute_all_rules = execute_all_rules
            if sort_rules:
                self.rules.sort(key=lambda r: r.priority.value, reverse=True)
            # if an action is passed to be executed before the passed rules it is wrapped to execute both
            if action is not None:
                action = self._wrap_action(action)
            else:
                action = self.evaluate_children
            if condition is None and not hasattr(self, "condition"):
                condition = always_execute
            super().__init__(phases, 
                             condition=condition, 
                             action=action, 
                             description=description, 
                             overwrite_settings=overwrite_settings,
                             self_config=self_config,
                             priority=priority, 
                             cooldown_reset_value=cooldown_reset_value,
                             enabled=enabled,
                             group=group)
            
    @__init__.register(_CountdownRule) # For similar_rule = Rule(some_rule), easier cloning
    @__init__.register(type) # For @Rule class MyRule: ...
    def __init_by_decorating_class(self, cls: "MultiRule"):
        phases = getattr(cls, "phases", getattr(cls, "phase", None)) # allow for spelling mistake
        cooldown_reset_value = getattr(cls, "cooldown_reset_value", getattr(cls, "max_cooldown", None)) 
        
        self.__init__(phases, cls.rules, cls.condition, description=cls.description, overwrite_settings=getattr(cls, "overwrite_settings", None), self_config=getattr(cls, "self_config", None), priority=getattr(cls, "priority", RulePriority.NORMAL), cooldown_reset_value=cooldown_reset_value, group=getattr(cls, "group", None), enabled=getattr(cls, "enabled", True), sort_rules_by_priority=getattr(cls, "sort_rules_by_priority", True), execute_all_rules=getattr(cls, "execute_all_rules", False), prior_action=getattr(cls, "prior_action", None), ignore_phase=getattr(cls, "ignore_phase", True))
    
    @__init__.register(Mapping)
    def __init_from_mapping(self, cls:Mapping):
        self.__init__(cls.get("phases", cls.get("phase")), cls["rules"], cls.get("condition"), description=cls["description"], overwrite_settings=cls.get("overwrite_settings"), self_config=cls.get("self_config"), priority=cls.get("priority", RulePriority.NORMAL), cooldown_reset_value=cls.get("cooldown_reset_value"), group=cls.get("group"), enabled=cls.get("enabled", True), sort_rules_by_priority=cls.get("sort_rules_by_priority", True), execute_all_rules=cls.get("execute_all_rules", False), prior_action=cls.get("prior_action", None), ignore_phase=cls.get("ignore_phase", True))

    
    def evaluate_children(self, ctx : Context) -> Union[List[Any], Any]:
        """
        Evaluates the children rules of the current rule in the given context.

        Args:
            ctx (Context): The context in which the child rules are evaluated.

        Returns:
            Union[List[Any], Any]: The results of evaluating the children rules.
                Returns a list of results if execute_all_rules is True, otherwise the result of the first rule that was applied.
        """
        results = []
        for rule in self.rules:
            try:
                result = rule(ctx, ignore_phase=self.ignore_phase)
            except DoNotEvaluateChildRules:
                return results
            if not self.execute_all_rules and result is not Rule.NOT_APPLICABLE: # one rule was applied end.
                return result
            results.append(result)
        return results

class RandomRule(metaclass=MultiRule):
    """
    A rule that selects and evaluates one or more random child rules from a set of rules.

    Args:
        phases (Union["Phase", Iterable]): The phase or phases in which the rule is applicable.
        rules (Union[Dict[Rule, float], List[Rule]]): The set of rules from which to select random child rules.
        repeat_if_not_applicable (bool, optional): If False, only one rule will be evaluated even if it is not applicable. Defaults to True.
        condition (Optional[Callable[[Context], Any]], optional): 
            A callable that determines if the rule is applicable in a given context.
            If None and the rule does not implement a `condition` attribute the rule always executes.
            Defaults to None.
        action (Optional[Callable[[Context], Any]], optional): A callable that defines the action to be performed when the rule is applicable. Defaults to None.
        ignore_phase (bool, optional): If True, the rule will be evaluated even if it is not in the specified phase. Defaults to True.
        priority (RulePriority, optional): The priority of the rule. Defaults to RulePriority.NORMAL.
        description (str, optional): A description of the rule. Defaults to "If its own condition is true calls one or more random child rules from the passed rules.".
        overwrite_settings (Optional[Dict[str, Any]], optional): A dictionary of settings to overwrite the default settings of the rule. Defaults to None.
        cooldown_reset_value (Optional[int], optional): The value to reset the cooldown of the rule. Defaults to None.
        group (Optional[str], optional): The group to which the rule belongs. Defaults to None.
        enabled (bool, optional): If False, the rule will not be evaluated. Defaults to True.
        weights (Optional[List[float]], optional): The weights associated with each rule when selecting random child rules. Defaults to None.

    Raises:
        ValueError: When passing rules as a dict with weights, the weights argument must be None.

    Methods:
        evaluate_children(ctx: Context, overwrite: Optional[Dict[str, Any]]) -> Any:
            Evaluate a random child rule. If `self.repeat_if_not_applicable=False` and the randomly chosen rule is not applicable,
            then no further rules are evaluated. For `self.repeat_if_not_applicable=False`, possible rules are evaluated in a random fashion
            until one rule is applicable.

    """
    
    # TODO: add a dummy attribute for one additional weight, that skips the evaluation. Should only considered once.
    
    @singledispatchmethod
    def __init__(self, 
                 phases : Union["Phase", Iterable], #/, # phases must be positional; python3.8+ only
                 rules : Union[Dict[Rule, float], List[Rule]], 
                 repeat_if_not_applicable : bool = True,
                 condition : Optional[Callable[[Context], Any]] = None, 
                 *,
                 action : Optional[Callable[[Context], Any]] = None,
                 ignore_phase = True,
                 priority: RulePriority = RulePriority.NORMAL, 
                 description: str = "If its own condition is true calls one or more random child rules from the passed rules.", 
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 self_config: Optional[Dict[str, Any]] = None,
                 cooldown_reset_value : Optional[int] = None,
                 group : Optional[str] = None,
                 enabled: bool = True,
                 weights: Optional[List[float]] = None
                 ):
        """
        Initializes a Rule object that can trigger one or more random child rules.
        
        Args:
            phases (Union["Phase", Iterable]): The phase or phases in which the rule is applicable.
            rules (Union[Dict[Rule, float], List[Rule]]): The set of rules from which to select random child rules.
            repeat_if_not_applicable (bool, optional): If False, only one rule will be evaluated even if it is not applicable. Defaults to True.
            condition (Optional[Callable[[Context], Any]], optional): 
                A callable that determines if the rule is applicable in a given context.
                If None and the rule does not implement a `condition` attribute the rule always executes.
                Defaults to None.
            action (Optional[Callable[[Context], Any]], optional): A callable that defines the action to be performed when the rule is applicable. Defaults to None.
            ignore_phase (bool, optional): If True, the rule will be evaluated even if it is not in the specified phase. Defaults to True.
            priority (RulePriority, optional): The priority of the rule. Defaults to RulePriority.NORMAL.
            description (str, optional): A description of the rule. Defaults to "If its own condition is true calls one or more random child rules from the passed rules.".
            overwrite_settings (Optional[Dict[str, Any]], optional): A dictionary of settings to overwrite the default settings of the rule. Defaults to None.
            cooldown_reset_value (Optional[int], optional): The value to reset the cooldown of the rule. Defaults to None.
            group (Optional[str], optional): The group to which the rule belongs. Defaults to None.
            enabled (bool, optional): If False, the rule will not be evaluated. Defaults to True.
            weights (Optional[List[float]], optional): The weights associated with each rule when selecting random child rules. Defaults to None.
        """
        if isinstance(rules, dict):
            if weights is not None:
                raise ValueError("When passing rules as a dict with weights, the weights argument must be None")
            self.weights = list(accumulate(rules.values())) # cumulative weights for random.choices are more efficient
            self.rules = list(rules.keys())
        else:
            self.weights = weights or list(accumulate(r.priority.value for r in rules))
            self.rules = rules
        self.repeat_if_not_applicable = repeat_if_not_applicable
        super().__init__(phases, rules, condition=condition, action=action, description=description, priority=priority, ignore_phase=ignore_phase, overwrite_settings=overwrite_settings, self_config=self_config, cooldown_reset_value=cooldown_reset_value, enabled=enabled, group=group)

    @__init__.register(_CountdownRule)
    @__init__.register(type)
    def __init_by_decorating_class(self, cls: "RandomRule"):
        phases = getattr(cls, "phases", getattr(cls, "phase", None))
        cooldown_reset_value = getattr(cls, "cooldown_reset_value", getattr(cls, "max_cooldown", None)) 
        
        self.__init__(phases, cls.rules, repeat_if_not_applicable=cls.repeat_if_not_applicable, condition=cls.condition, description=cls.description, overwrite_settings=getattr(cls, "overwrite_settings", None), self_config=getattr(cls, "self_config", None), priority=getattr(cls, "priority", RulePriority.NORMAL), cooldown_reset_value=cooldown_reset_value, group=getattr(cls, "group", None), enabled=getattr(cls, "enabled", True), prior_action=getattr(cls, "prior_action", None), ignore_phase=getattr(cls, "ignore_phase", True))
    
    @__init__.register(Mapping)
    def __init_from_mapping(self, cls:Mapping):
        self.__init__(cls.get("phases"), cls["rules"], repeat_if_not_applicable=cls.get("repeat_if_not_applicable", True), condition=cls.get("condition"), description=cls["description"], overwrite_settings=cls.get("overwrite_settings"), self_conifg=cls.get("self_config"), priority=cls.get("priority", RulePriority.NORMAL), cooldown_reset_value=cls.get("cooldown_reset_value"), group=cls.get("group"), enabled=cls.get("enabled", True), sort_rules_by_priority=cls.get("sort_rules_by_priority", True), execute_all_rules=cls.get("execute_all_rules", False), prior_action=cls.get("prior_action", None), ignore_phase=cls.get("ignore_phase", True))

    def evaluate_children(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None) -> Any:
        """
        Evaluate a random child rule.
        If `self.repeat_if_not_applicable=False` and the randomly chosen rule is not applicable,
        then no further rules are evaluated
        For `self.repeat_if_not_applicable=False` possible rules are evaluated in a random fashion
        until one rule was applicable.
        """
        if self.repeat_if_not_applicable:
            rules = self.rules.copy()
            weights = self.weights.copy()
        else:
            rules = self.rules
            weights = self.weights

        while rules:
            rule = random.choices(rules, cum_weights=weights, k=1)[0]
            try:
                result = rule(ctx, overwrite, ignore_phase=self.ignore_phase) #NOTE: Context action/evaluation results only store result of LAST rule
            except DoNotEvaluateChildRules:
                return None
            if not self.repeat_if_not_applicable or result is not Rule.NOT_APPLICABLE:
                # break after the first rule of `self.repeat_if_not_applicable=False`
                # else break if it was applicable.
                break
            rules.remove(rule)
            weights = list(accumulate(r.priority.value for r in rules))
        return result





class BlockingRule(metaclass=Rule):

    _gameframework: ClassVar[Union["GameFramework", "proxy[GameFramework]", None]] = None

    ticks_passed : int
    """Count how many ticks have been performed by this rule and blocked the agent."""
    
    MAX_TICKS = 5000 # 5000 * 1/20 = 250 seconds
    
    max_tick_callback : Optional[Callable[[BlockingRule, Context], Any]] = None

    @singledispatchmethod
    def __init__(self, 
                 phases : Union["Phase", Iterable["Phase"]], # iterable of Phases
                 #/, # phases must be positional; python3.8+ only
                 condition : Optional[Union[ConditionFunction, Callable[[Context], Hashable]]]=None, 
                 action: Optional[Union[Callable[[Context], Any], Dict[Any, Callable]]] = None,
                 false_action: Optional[Callable[[Context], Any]] = None,
                 *, 
                 gameframework: Optional["GameFramework"],
                 actions : Optional[Dict[Any, Callable[[Context], Any]]] = None,
                 description: str = "What does this rule do?",
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 self_config: Optional[Dict[str, Any]] = None,
                 priority: RulePriority = RulePriority.NORMAL,
                 cooldown_reset_value : Optional[int] = None,
                 group : Optional[str] = None,
                 enabled: bool = True,
                 ignore_chance = NotImplemented,
                 ):
        super().__init__(phases, condition, action, false_action, actions=actions, description=description, overwrite_settings=overwrite_settings, self_config=self_config, priority=priority, cooldown_reset_value=cooldown_reset_value, group=group, enabled=enabled, ignore_chance=ignore_chance)
        if gameframework:
            BlockingRule._gameframework = gameframework
        if not GameFramework.clock or not GameFramework.display:
            # Not much we can do about it
            #logger.info("%s : GameFramework should be initialized before using this rule.", self.__class__.__name__)
            GameFramework.init_pygame()
        self.ticks_passed = 0

    @__init__.register(_CountdownRule)
    @__init__.register(type)
    def __init_by_decorating_class(self, cls: "BlockingRule"): # pylint: disable=unused-variable
        """
        Initialize by passing a Rule or class object to the __init__ method.
        
        This allows the usage of the @Rule decorator and easy copying.
        """
        phases = getattr(cls, "phases", getattr(cls, "phase", None)) # allow for spelling mistake
        cooldown_reset_value = getattr(cls, "cooldown_reset_value", getattr(cls, "max_cooldown", None)) 
        self.__init__(phases, cls.condition, action=getattr(cls, "action", None), false_action=getattr(cls, "false_action", None), gameframework=getattr(cls, "gameframework", BlockingRule._gameframework), actions=getattr(cls, "actions", None), description=cls.description, overwrite_settings=getattr(cls, "overwrite_settings", None), self_config=getattr(cls, "self_config", None), priority=getattr(cls, "priority", RulePriority.NORMAL), cooldown_reset_value=cooldown_reset_value, group=getattr(cls, "group", None), enabled=getattr(cls, "enabled", True))
    
    def _render_everything(self, ctx: Context):
        if self._gameframework:
            self._gameframework.render_everything()
        else:
            world_model = ctx.agent._world_model
            display = GameFramework.display
            world_model.tick(GameFramework.clock)
            world_model.render(display, finalize=False)
            world_model.controller.render(display)
            dm_render_conf = OmegaConf.select(world_model._args, "camera.hud.data_matrix", default=None)

            if dm_render_conf and ctx.agent:
                ctx.agent.render_detection_matrix(display, dm_render_conf)
            world_model.finalize_render(display)
        pygame.display.flip()

    if TYPE_CHECKING:
        @override
        def loop_agent(self, ctx: Context, *, execute_planner: True, execute_phases:Any) -> VehicleControl: ...
            
        @override
        def loop_agent(self, ctx: Context, *, execute_planner: False, execute_phases:Any) -> None: ...

    def loop_agent(self, ctx: Context, control: Optional[carla.VehicleControl]=None, *, execute_planner: bool, execute_phases=True) -> VehicleControl | None:
        """
        A combination of `LunaticAgent.parse_keyboard_input`, `LunaticAgent.apply_control`, `BlockingRule.update_world`,
        and `Context.get_or_calculate_control` to advance agent and world.
        
        Args:
            ctx (Context): The current context object
            control (Optional[carla.VehicleControl], optional): The control to apply; will overwrite the context's control.
                If None takes the context's control.
                Defaults to None.
        
        See Also:
            - [](#LunaticAgent.parse_keyboard_input)
            - [](#LunaticAgent.apply_control)
            - [](#BlockingRule.update_world)
            - [](#Context.get_or_calculate_control)
        """
        ctx.agent.parse_keyboard_input(control=control) # NOTE: if skipped the user has no option to stop the agent
        ctx.agent.apply_control(control)
            
        # NOTE: This ticks the world forward by one step
        # The ctx.control is reset to None; execute_plan
        # > Phase.UPDATE_INFORMATION | Phase.BEGIN
        self.update_world(ctx, execute_planner=True, execute_phases=execute_phases)
        if execute_planner:
            control = ctx.get_or_calculate_control()
            return control
        return None

    @staticmethod
    def get_world():
        return CarlaDataProvider.get_world()

    def _begin_tick(self, ctx: Context):
        self._gameframework.clock.tick() # self.args.fps)
        frame = None
        if self._gameframework._args.handle_ticks: # i.e. no scenario runner doing it for us
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

    def update_world(self, ctx: Context, *, execute_phases=True) -> VehicleControl | None:
        """
        When true, the agent will execute the 
            execute_phase(Phase.CUSTOM_CYCLE | Phase.BEGIN, prior_results=<this Rule instance>)

            Phase.UPDATE_INFORMATION | Phase.[BEGIN|END] while blocked. 
            Default is True.

        Args:
            ctx (Context): The context to use
            execute_update_information (bool, optional): Whether to execute the Phase.UPDATE_INFORMATION | Phase.[BEGIN|END] while blocked. Defaults to True.
            run_step (bool, optional): 
                Whether to run the next step of the local planner.
            
                Note:
                    If you want to update the behavior of the agent after Phase.UPDATE_INFORMATION | Phase.END
                    inside the rule's action you should should use `execute_planner=False`.
                    If you need a ready control object for the next step to work with, use `execute_planner=True`
                    or call `ctx.get_or_calculate_control()` inside the rule's action afterwards.

        Raises:
            UnblockRuleException: If the ticks passed are over MAX_TICKS
        """
        self._begin_tick(ctx)
        ctx.agent.execute_phase(Phase.CUSTOM_CYCLE | Phase.BEGIN, prior_results=self)

        # Update the agent's information
        if execute_phases:
            ctx.agent.execute_phase(Phase.UPDATE_INFORMATION | Phase.BEGIN, prior_results=self)
        ctx.agent._update_information()
        if execute_phases and Phase.UPDATE_INFORMATION | Phase.END not in self.phases:
            ctx.agent.execute_phase(Phase.UPDATE_INFORMATION | Phase.END, prior_results=self)
        if self.ticks_passed > self.MAX_TICKS:
            if self.max_tick_callback:
                self.max_tick_callback(ctx)
            raise UnblockRuleException()
        
        self._render_everything(ctx)

    def __call__(self, ctx: Context, overwrite=None, *args, in_loop=False, **kwargs):
        if not in_loop:
            self.ticks_passed = 0
        else:
            kwargs.setdefault("ignore_phase", True)
            kwargs.setdefault("ignore_cooldown", True)
        if self in ctx.agent._active_blocking_rules:
            logger.warning("Rule %s is already blocking the agent, this is a recursive call. Not executing the rule.", self)
            return Rule.NOT_APPLICABLE
        try:
            return super().__call__(ctx, overwrite, *args, **kwargs)
        except UnblockRuleException as e:
            return e.result
        finally:
            ctx.agent._active_blocking_rules.discard(self)
            
    def evaluate(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None) -> Union[bool,Hashable, "Rule.NO_RESULT"]:
        result = super().evaluate(ctx, overwrite)
        if result in self.actions:
            ctx.agent._active_blocking_rules.add(self)
        return result

# Provide necessary imports for the evaluation_function module and prevents circular imports

import classes.evaluation_function as __evaluation_function
__evaluation_function.Rule = Rule
__evaluation_function.Context = Context
del __evaluation_function

import classes.constants as __constants
__constants.Rule = Rule
__constants.Context = Context
del __constants