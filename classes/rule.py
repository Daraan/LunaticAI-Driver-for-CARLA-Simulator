from __future__ import annotations # todo: can this be removed?

from collections.abc import Mapping
from functools import partial, wraps
try: # Python 3.8+
    from functools import singledispatchmethod
except ImportError:
    from functools import singledispatch, update_wrapper

    def singledispatchmethod(func):
        """
        Works like functools.singledispatch, but for methods. Backward compatible code
        """
        dispatcher = singledispatch(func)
        def wrapper(*args, **kw):
            return dispatcher.dispatch(args[1].__class__)(*args, **kw)
        wrapper.register = dispatcher.register
        update_wrapper(wrapper, func)
        return wrapper
    
import random
import inspect
from inspect import isclass
from itertools import accumulate
from enum import IntEnum
from typing import Any, ClassVar, List, Set, Tuple, Union, Iterable, Callable, Optional, Dict, Hashable, TYPE_CHECKING
from weakref import WeakSet

from omegaconf import OmegaConf

from launch_tools import CarlaDataProvider
from classes.constants import Phase
from classes.evaluation_function import EvaluationFunction, TruthyEvaluationFunction
from agents.tools.logging import logger

if TYPE_CHECKING:
    import carla
    from agents.lunatic_agent import LunaticAgent
    from agents.tools.config_creation import LunaticAgentSettings


class Context(CarlaDataProvider):
    """
    Object to be passed as the first argument (instead of self) to rules, actions and evaluation functions.
    
    The `Context` class derives from the scenario runner's `CarlaDataProvider` to allow access to the world, map, etc.
    
    NOTE: That Context.config are the read-only settings for the given rule and actions with potential overwrites.
    """
    
    agent : "LunaticAgent"
    config : "LunaticAgentSettings"
    """A copy of the agents config. Overwritten by the rule's settings."""
    
    evaluation_results : Dict["Phase", Hashable] # ambiguous wording, which result? here evaluation result
    action_results : Dict["Phase", Any] 
    
    control : Optional["carla.VehicleControl"]
    """Current control the agent should use. Set by execute_phase(control=...). Safeguarded to be not set to None."""
    _control : Optional["carla.VehicleControl"]
    """Current control the agent should use."""
    
    prior_result : Optional[Any] # TODO: maybe rename
    """Result of the current phase."""
    
    last_context : Optional["Context"]
    """The context object of the last tick. Used to access the last phase's results."""
    
    second_pass : bool = None
    """
    Whether or not the run_step function performs a second pass.
    
    NOTE: The correct value of should not be assumed.
    The user is responsible for setting this value to True if a second pass is required.
    """

    def __init__(self, agent : "LunaticAgent", **kwargs):
        self.agent = agent
        self._control = kwargs.pop("control", None)
        self._init_arguments = kwargs
        self.evaluation_results = {}
        self.action_results = {}
        self.last_phase_evaluation_results = {}
        self.last_phase_action_results = {}
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
    
    def end_of_phase(self): # TODO: keep or remove? unused
        self.last_phase_action_results = self.action_results.copy()
        self.last_phase_evaluation_results = self.evaluation_results.copy()
        self.evaluation_results.clear()
        self.action_results.clear()


class RulePriority(IntEnum):
    """
    Priority of a rule. The higher a value, the higher the priority.
    Rules are sorted by their priority before being applied.
    """
    NULL = 0
    LOWEST = 1
    LOW = 2
    NORMAL = 4
    HIGH = 8
    HIGHEST = 16

@EvaluationFunction
def always_execute(ctx : Context): # pylint: disable=unused-argument
    return True


class _CountdownRule:

    # TODO: low prio: make cooldown dependant of tickrate or add a conversion from seconds to ticks OR make time-based
    tickrate : ClassVar[int] = NotImplemented

    DEFAULT_COOLDOWN_RESET : ClassVar[int] = 0
    """Value the cooldown is reset to when `reset_cooldown` is called without a value."""
       
    start_cooldown : ClassVar[int] = 0
    """Initial Cooldown when initialized. if >0 the rule will not be ready for the first start_cooldown ticks."""

    instances : ClassVar[WeakSet["_CountdownRule"]] = WeakSet()
    """Keep track of all instances for the cooldowns"""
    
    _cooldown : int
    """If 0 the rule is ready to be executed."""
    
    blocked : bool = False # NOTE: not a property
    """Indicates if the rule is blocked for this tick only. Reset to False after the tick."""

    def __init__(self, cooldown_reset_value : Optional[int] = None, enabled: bool = True):
        self.instances.add(self)
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
        return self._cooldown
    
    @cooldown.setter
    def cooldown(self, value):
        self._cooldown = value
    
    def update_cooldown(self):
        if self._cooldown > 0:
            self._cooldown -= 1
    
    @classmethod
    def update_all_cooldowns(cls):
        for instance in cls.instances:
            instance.update_cooldown()
            
    @classmethod
    def unblock_all_rules(cls):
        for instance in cls.instances:
            instance.blocked = False
            
    @property
    def enabled(self) -> bool:
        """If False the rule will not be evaluated. Contrary to `blocked` it will not be reset after the tick."""
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
    
    def set_active(self, value: bool):
        self._enabled = value
    
    class CooldownFramework:
        """Context manager to reduce all cooldowns from a with statement."""

        def __enter__(self):
            return self

        def __exit__(_, exc_type, exc_value, traceback):
            Rule.update_all_cooldowns()
            Rule.unblock_all_rules()
                

class _GroupRule(_CountdownRule):
    group : Optional[str] = None # group of rules that share a cooldown
    """
    Group name of rules that should share their cooldown.
    
    None for a rule to not share its cooldown.
    """

    # first two values in the list are current and max cooldown, the third is a set of all instances
    group_instances : ClassVar[Dict[str, List[int, int, WeakSet["_GroupRule"]]]] = {}
    """
    Dictionary of all group instances. Key is the group name. 
    
    Value is a list of the current cooldown, the max cooldown for reset and a WeakSet of all instances.
    """
    
    def __init__(self, group :Optional[str]=None, cooldown_reset_value : Optional[int] = None, enabled: bool = True):
        super().__init__(cooldown_reset_value, enabled)
        self.group = group
        if group is None:
            return
        if group not in self.group_instances:
            self.group_instances[group] = [0, self.max_cooldown, WeakSet()]
        self.group_instances[group][2].add(self) # add to weak set

    @property
    def cooldown(self) -> int:
        if self.group:
            return _GroupRule.group_instances[self.group][0]
        return super().cooldown
    
    @property
    def has_group(self) -> bool:
        return self.group is not None
    
    @cooldown.setter
    def cooldown(self, value):
        if self.group:
            _GroupRule.group_instances[self.group][0] = value
            return
        super().cooldown = value
    
    def set_cooldown_of_my_group(self, value: Optional[int]=None):
        if value is None:
            self.group_instances[self.group][0] = self.group_instances[self.group][1] # set to max
        else:
            self.group_instances[self.group][0] = value

    def reset_cooldown(self, value:Optional[int]=None):
        if self.group:
            self.set_cooldown_of_my_group(value)
        else:
            super().reset_cooldown()

    @classmethod
    def set_cool_down_of_group(cls, group : str, value: int):
        if group in cls.group_instances:
            cls.group_instances[group][0] = value
        else:
            raise ValueError(f"Group {group} does not exist.")

    __filter_not_ready_instances = lambda instance: instance.group is None and instance._cooldown > 0
    """Filter function to get all instances that are not ready. see `update_all_cooldowns`."""

    @classmethod
    def update_all_cooldowns(cls):
        # Update Groups
        for instance_data in cls.group_instances.values():
            if instance_data[0] > 0:
                instance_data[0] -= 1
        for instance in filter(cls.__filter_not_ready_instances, cls.instances):
            instance._cooldown -= 1


class Rule(_GroupRule):
    rule : EvaluationFunction
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
    
    description : str
    """Description of what this rule should do"""
    
    overwrite_settings : Dict[str, Any]
    """Settings that should overwrite the agent's settings for this rule."""
    
    phases : Set["Phase"]
    """The phase or phases in which the rule should be evaluated."""

    # Indicate that no rule was applicable in the current phase
    # i.e.  rule(ctx) in actions was False 
    NOT_APPLICABLE : ClassVar = object()
    """Object that indicates that no action was executed."""
    
    priority: RulePriority = RulePriority.NORMAL

    def clone(self):
        """
        Create a new instance of the rule with the same settings.
        
        Note: 
            * The current cooldown is not taken into account.
            * The current enabled state is taken into account.
        """
        return self.__class__(self) # Make use over overloaded __init__

    @singledispatchmethod
    def __init__(self, 
                 phases : Union["Phase", Iterable["Phase"]], # iterable of Phases
                 rule : Optional[Callable[[Context], Hashable]]=None, 
                 action: Optional[Union[Callable[[Context], Any], Dict[Any, Callable]]] = None,
                 false_action: Optional[Callable[[Context], Any]] = None,
                 *, 
                 actions : Optional[Dict[Any, Callable[[Context], Any]]] = None,
                 description: str = "What does this rule do?",
                 overwrite_settings: Optional[Dict[str, Any]] = None,
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
        - rule: A function that takes a Context object as input and returns a Hashable value. 
            If not provided, the class must implement a `rule` function.
        - action: A function or a dictionary of functions that take a Context object as input. 
            If `action` behaves like `actions`.
            Only one of `action` and `actions` can be set.
        - false_action: A function that takes a Context object as input and returns any value. 
            It is used when `action` is a single function and represents the action to be taken when the condition is False.
        - actions: A dictionary of `action` functions
            It should map the return values of `rule` to the corresponding action function. 
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
        - TypeError: If `rule` is None and the class does not implement a `rule` function, or if both `action` and `actions` are None and the class does not have an `actions` attribute or an `action` function.
        - TypeError: if actions is not a Mapping object.
        - ValueError: If both `action` and `actions` are provided.
        - ValueError: If `action` is a Mapping and either `false_action` or `actions` is not None.
        - ValueError: If an action function is not callable.
        - ValueError: If `description` is not a string.

        """
        # Check phases
        if not phases:
            raise ValueError("phases must not be empty or None")
        if not isinstance(phases, set):
            if isinstance(phases, Iterable):
                phases = set(phases)
            else:
                phases = {phases}
        for p in phases:
            if not isinstance(p, Phase):
                raise ValueError(f"phase must be of type Phases, not {type(p)}")
        self.phases = phases
        
        # Check Rule
        if rule is None and not hasattr(self, "rule"):
            raise TypeError("%s.__init__() missing 1 required positional argument: 'rule'. Alternatively the class must implement a `rule` function." % self.__class__.__name__)
        #if rule is not None and not isinstance(rule, EvaluationFunction) \
        #    and (isinstance(rule, partial) and not isinstance(rule.func, EvaluationFunction)):
        #    raise TypeError(f"rule must be of type EvaluationFunction or a partial of a , not {type(rule)}")
        if rule is not None and not hasattr(self, "rule"):
            self.rule = rule
        elif rule is not None and hasattr(self, "rule"):
            logger.debug(f"Warning 'rule' argument passed but class {self.__class__.__name__} already implements 'self.rule'. Overwriting 'self.rule' with passed rule.")
            self.rule = rule
        
        # Check Actions
        if action is not None and actions is not None:
            try:
                if len(actions) == 1 and action is actions[True]:
                    logger.info("`action` and `actions` have been both been used when initializing %s. Did you use `rule.register_action`? Then you can omit the action parameter / attribute.", self)
                    action = None
                else:
                    raise ValueError("Only one of 'action' and 'actions' can be set.")
            except Exception as e:
                raise ValueError("Either only one of 'action' and 'actions' can be set, or actions[True] must be the same as action - other actions are currently not supported.") from e
        if action is None and actions is None and not hasattr(self, "actions"):
            raise TypeError("%s.__init__() `action` and `actions` are both None. Provide at least one argument alternatively the class must have an `actions` attribute or an `action` function." % self.__class__.__name__)

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
        
        
        # Assure that method(self, ctx) like functions are accessible like them
        for key, func in self.actions.items():
            if not callable(func):
                raise ValueError(f"Action for key {key} must be callable, not {type(func)}")
            if len(inspect.signature(func).parameters) >= 2:
                self.actions[key] = partial(func, self) # bind to self
        
        # Check Description
        if not isinstance(description, str):
            raise ValueError(f"description must be of type str, not {type(description)}")
        self.description = description
        super().__init__(group or self.group, cooldown_reset_value, enabled) # or self.group for subclassing
        self.priority : float | int | RulePriority = priority # used by agent.add_rule
        
        self.overwrite_settings = overwrite_settings or {}
    
    def __new__(cls, phases=None, *args, **kwargs):
        """
        The @Rule decorator allows to instantiate a Rule class directly for easier out-of-the-box usage.
        """
        if isclass(phases):
            if issubclass(phases, _CountdownRule):
                raise ValueError("When using @Rule the class must not be a subclass of Rule. Consider subclassing Rule instead.")
            decorated_class = phases

            # Create the new class
            new_rule_class = type(decorated_class.__name__, (cls,), decorated_class.__dict__.copy()) # > calls init_subclass; copy() for correct type!
            return super().__new__(new_rule_class)
        return super().__new__(cls)
    
    def __init_subclass__(cls):
        """
        Automatically creates a __init__ function to allow for a simple to use class-interface to create rule classes.
        
        By setting __no_auto_init = True in the class definition, the automatic __init__ creation is disabled.
        """
        if not "__init__" in cls.__dict__ and not cls.__dict__.get("__no_auto_init", False):
            do_not_overwrite = ["phases"]
            if hasattr(cls, "rule"):
                
                # Check if the rule should be treated as a method or function
                if isinstance(cls.rule, EvaluationFunction):
                    rule_func = cls.rule.evaluation_function
                else:
                    rule_func = cls.rule
                if len(inspect.signature(rule_func).parameters) >= 2:
                    # If it has two arguments it will not be overwritten -> method(self, ctx)
                    # Else with one argument function(ctx), self.rule = rule will overwrite it
                    do_not_overwrite.append("rule")
                
                #if not isinstance(cls.rule, EvaluationFunction):# and (isinstance(cls.rule, partial) and not isinstance(cls.rule.func, EvaluationFunction)):
                #    raise TypeError(f"{cls.__name__}.rule must be of type EvaluationFunction. Decorate it with @EvaluationFunction.")
                if hasattr(cls.rule, "actions") and cls.rule.actions:
                    if hasattr(cls, "actions") and cls.actions:
                        raise ValueError(f"Class {cls.__name__} already has an 'actions' attribute. It will be overwritten by the 'actions' attribute of the rule.")
                    cls.actions = cls.rule.actions
            
            # Create a __init__ function that sets some of the parameters.
            params = inspect.signature(cls.__init__).parameters # find overlapping parameters
            
            @wraps(cls.__init__)
            def partial_init(self, phases=None, *args, **kwargs):
                # Need phases as first argument
                phases = getattr(cls, "phases", None) # allow for both wordings
                phase = getattr(cls, "phase", None)
                if phases and phase:
                    raise ValueError(f"Both 'phases' and 'phase' are set in class {cls.__name__}. Use only one.")
                phases = phases or phase
                if phases is None:
                    raise ValueError(f"`phases` or `phase` must be provided for class {cls.__name__}")
                # Removing rule to not overwrite it
                kwargs.update({k:v for k,v in cls.__dict__.items() if k in params and k not in do_not_overwrite})
                super(cls, self).__init__(phases, *args, **kwargs)
            
            cls.__init__ = partial_init
    
    @__init__.register(_CountdownRule)
    @__init__.register(type)
    def __init_by_decorating_class(self, cls):
        """
        Initialize by passing a Rule or class object to the __init__ method.
        
        This allows the usage of the @Rule decorator and easy copying.
        """
        phases = getattr(cls, "phases", getattr(cls, "phase", None)) # allow for spelling mistake
        cooldown_reset_value = getattr(cls, "cooldown_reset_value", getattr(cls, "max_cooldown", None)) 
        self.__init__(phases, cls.rule, getattr(cls, "action", None), getattr(cls, "false_action", None), actions=getattr(cls, "actions", None), description=cls.description, overwrite_settings=getattr(cls, "overwrite_settings", None), priority=getattr(cls, "priority", RulePriority.NORMAL), cooldown_reset_value=cooldown_reset_value, group=getattr(cls, "group", None), enabled=getattr(cls, "enabled", True))
        
    @__init__.register
    def __init_from_mapping(self, cls:Mapping):
        self.__init__(cls.get("phases", cls.get("phase")), cls["rule"], cls.get("action"), cls.get("false_action"), actions=cls.get("actions"), description=cls["description"], overwrite_settings=cls.get("overwrite_settings"), priority=cls.get("priority", RulePriority.NORMAL), cooldown_reset_value=cls.get("cooldown_reset_value"), group=cls.get("group"), enabled=cls.get("enabled", True))        

    def evaluate(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None) -> Union[bool,Hashable]:
        settings = self.overwrite_settings.copy()   
        if overwrite:
            settings = self.overwrite_settings.copy()
            settings.update(overwrite)
        ctx.config = OmegaConf.merge(ctx.agent.config, settings)
        OmegaConf.set_readonly(ctx.config, True) # only the original agent.config can be modified. Make clear that these have no permanent effect.
        #ctx.config.update(settings)
        result = self.rule(ctx)
        return result
    
    def evaluate_children(self, ctx : Context):
        raise NotImplementedError("This method should be implemented in a subclass")

    def __call__(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None, *, ignore_phase=False, ignore_cooldown=False) -> Any:
        # Check phase
        assert ctx.agent.current_phase in self.phases
            
        if not self.is_ready() and not ignore_cooldown:
            return self.NOT_APPLICABLE
        if not ignore_phase and ctx.agent.current_phase not in self.phases: #NOTE: This is currently never False as checked in execute_phase and the agents dictionary.
            return self.NOT_APPLICABLE # not applicable for this phase
        result = self.evaluate(ctx, overwrite)

        ctx.evaluation_results[ctx.agent.current_phase] = result
        if result in self.actions:
            self._cooldown = self.max_cooldown
            action_result = self.actions[result](ctx) #todo allow priority, random chance
            ctx.action_results[ctx.agent.current_phase] = action_result
            return action_result
        return self.NOT_APPLICABLE # No action was executed
    
    def __str__(self) -> str:
        try:
            if isinstance(self.rule, partial):
                return self.__class__.__name__ + f"(description='{self.description}', phases={self.phases}, group={self.group}, priority={self.priority}, actions={self.actions}, rule={self.rule.func}, cooldown={self.cooldown})"
            return self.__class__.__name__ + f"(description='{self.description}', phases={self.phases}, group={self.group}, priority={self.priority}, actions={self.actions}, rule={self.rule.__name__}, cooldown={self.cooldown})" 
        except AttributeError as e:
            logger.warning(str(e))
            return self.__class__.__name__ + ("Error in rule.__str__: Rule has not been initialized correctly. Missing attributes: " + str(e))

    def __repr__(self) -> str:
        return str(self)

class MultiRule(Rule):

    def _wrap_action(self, action: Callable[[Context], Any]):
        """
        Wrap the past function to that afterwards the children rules are executed.
        """
        @wraps(action)
        def wrapper(ctx : Context, *args, **kwargs) -> Any:
            result = action(ctx, *args, **kwargs)
            results = self.evaluate_children(ctx) # execute given rules as well
            return result, results
        return wrapper

    @singledispatchmethod
    def __init__(self, 
                 phases: Union["Phase", Iterable], 
                 rules: List[Rule], 
                 rule : Callable[[Context], Any] = always_execute,
                 *,
                 description: str = "If its own rule is true calls the passed rules.",
                 priority: RulePriority = RulePriority.NORMAL, 
                 sort_rules_by_priority : bool = True,
                 execute_all_rules = False,
                 prior_action : Optional[Callable[[Context], Any]] = None,
                 ignore_phase : bool = True,
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 cooldown_reset_value : Optional[int] = None,
                 group : Optional[str] = None,
                 enabled: bool = True,
                 ):
            """
            Initializes a Rule object.

            # TODO update docstring
            Args:
                phases (Union[Phase, Iterable]): The phase or phases in which the rule should be active.
                rules (List[Rule]): The list of rules to be called if the rule's condition is true.
                rule (Callable[[Context]], optional): The condition that determines if the rules should be evaluated. Defaults to always_execute.
                execute_all_rules (bool, optional): Flag indicating whether to execute all rules or stop after a rule as been applied. Defaults to False.
                sort_rules_by_priority (bool, optional): Flag indicating whether to sort the rules by priority. Defaults to True.
                prior_action (Callable[[Context]], optional): The action to be executed before the passed rules are evaluated. Defaults to None.
                ignore_phase (bool, optional): Flag indicating whether to ignore the Phase of the passed rules. Defaults to True.
                overwrite_settings (Dict[str, Any], optional): Additional settings to overwrite the rule's settings. Defaults to None.
                priority (RulePriority, optional): The priority of the rule. Defaults to RulePriority.NORMAL.
                description (str, optional): The description of the rule. Defaults to "If its own rule is true calls the passed rules.".
            """
            self.ignore_phase = ignore_phase
            self.rules = rules
            self.execute_all_rules = execute_all_rules
            if sort_rules_by_priority:
                self.rules.sort(key=lambda r: r.priority.value, reverse=True)
            # if an action is passed to be executed before the passed rules it is wrapped to execute both
            if prior_action is not None:
                prior_action = self._wrap_action(prior_action)
            else:
                prior_action = self.evaluate_children
            super().__init__(phases, 
                             rule=rule, 
                             action=prior_action, 
                             description=description, 
                             overwrite_settings=overwrite_settings,
                             priority=priority, 
                             cooldown_reset_value=cooldown_reset_value,
                             enabled=enabled)
            
    @__init__.register(_CountdownRule) # For Rule(some_rule), easier cloning
    @__init__.register(type) # For @Rule class MyRule: ...
    def __init_by_decorating_class(self, cls):
        phases = getattr(cls, "phases", getattr(cls, "phase", None)) # allow for spelling mistake
        cooldown_reset_value = getattr(cls, "cooldown_reset_value", getattr(cls, "max_cooldown", None)) 
        
        self.__init__(phases, cls.rules, cls.rule, description=cls.description, overwrite_settings=getattr(cls, "overwrite_settings", None), priority=getattr(cls, "priority", RulePriority.NORMAL), cooldown_reset_value=cooldown_reset_value, group=getattr(cls, "group", None), enabled=getattr(cls, "enabled", True), sort_rules_by_priority=getattr(cls, "sort_rules_by_priority", True), execute_all_rules=getattr(cls, "execute_all_rules", False), prior_action=getattr(cls, "prior_action", None), ignore_phase=getattr(cls, "ignore_phase", True))
    
    @__init__.register(Mapping)
    def __init_from_mapping(self, cls:Mapping):
        self.__init__(cls.get("phases", cls.get("phase")), cls["rules"], cls.get("rule"), description=cls["description"], overwrite_settings=cls.get("overwrite_settings"), priority=cls.get("priority", RulePriority.NORMAL), cooldown_reset_value=cls.get("cooldown_reset_value"), group=cls.get("group"), enabled=cls.get("enabled", True), sort_rules_by_priority=cls.get("sort_rules_by_priority", True), execute_all_rules=cls.get("execute_all_rules", False), prior_action=cls.get("prior_action", None), ignore_phase=cls.get("ignore_phase", True))

    
    def evaluate_children(self, ctx : Context) -> Union[List[Any], Any]:
        """
        Evaluates the children rules of the current rule in the given context.

        Args:
            ctx (Context): The context in which the rules are evaluated.

        Returns:
            Union[List[Any], Any]: The results of evaluating the children rules.
                Returns a list of results if execute_all_rules is True, otherwise the result of the first rule that was applied.
        """
        results = []
        for rule in self.rules:
            result = rule(ctx, ignore_phase=self.ignore_phase)
            if not self.execute_all_rules and result is not Rule.NOT_APPLICABLE: # one rule was applied end.
                return result
            results.append(result)
        return results

class RandomRule(MultiRule):

    @singledispatchmethod
    def __init__(self, 
                 phases : Union["Phase", Iterable], 
                 rules : Union[Dict[Rule, float], List[Rule]], 
                 repeat_if_not_applicable : bool = True,
                 rule = always_execute, 
                 *,
                 prior_action : Optional[Callable[[Context], Any]] = None,
                 ignore_phase = True,
                 priority: RulePriority = RulePriority.NORMAL, 
                 description: str = "If its own rule is true calls one or more random rule from the passed rules.", 
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 cooldown_reset_value : Optional[int] = None,
                 group : Optional[str] = None,
                 enabled: bool = True,
                 weights: List[float] = None
                 ):
        #if amount < 1:
        #    raise ValueError("Amount must be at least 1")
        #self.amount = amount 
        if isinstance(rules, dict):
            if weights is not None:
                raise ValueError("When passing rules a dict with weights, the weights argument must be None")
            self.weights = list(accumulate(rules.values())) # cumulative weights for random.choices are more efficient
            self.rules = list(rules.keys())
        else:
            self.weights = weights or list(accumulate(r.priority.value for r in rules))
            self.rules = rules
        self.repeat_if_not_applicable = repeat_if_not_applicable
        super().__init__(phases, rule=rule, prior_action=prior_action, description=description, priority=priority, ignore_phase=ignore_phase, overwrite_settings=overwrite_settings, cooldown_reset_value=cooldown_reset_value, enabled=enabled, group=group)

    @__init__.register(_CountdownRule)
    @__init__.register(type)
    def __init_by_decorating_class(self, cls):
        phases = getattr(cls, "phases", getattr(cls, "phase", None))
        cooldown_reset_value = getattr(cls, "cooldown_reset_value", getattr(cls, "max_cooldown", None)) 
        
        self.__init__(phases, cls.rules, repeat_if_not_applicable=cls.repeat_if_not_applicable, rule=cls.rule, description=cls.description, overwrite_settings=getattr(cls, "overwrite_settings", None), priority=getattr(cls, "priority", RulePriority.NORMAL), cooldown_reset_value=cooldown_reset_value, group=getattr(cls, "group", None), enabled=getattr(cls, "enabled", True), prior_action=getattr(cls, "prior_action", None), ignore_phase=getattr(cls, "ignore_phase", True))
    
    @__init__.register(Mapping)
    def __init_from_mapping(self, cls:Mapping):
        self.__init__(cls.get("phases"), cls["rules"], repeat_if_not_applicable=cls.get("repeat_if_not_applicable", True), rule=cls.get("rule"), description=cls["description"], overwrite_settings=cls.get("overwrite_settings"), priority=cls.get("priority", RulePriority.NORMAL), cooldown_reset_value=cls.get("cooldown_reset_value"), group=cls.get("group"), enabled=cls.get("enabled", True), sort_rules_by_priority=cls.get("sort_rules_by_priority", True), execute_all_rules=cls.get("execute_all_rules", False), prior_action=cls.get("prior_action", None), ignore_phase=cls.get("ignore_phase", True))


    def evaluate_children(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None) -> Any:
        if self.repeat_if_not_applicable:
            rules = self.rules.copy()
            weights = self.weights.copy()
        else:
            rules = self.rules
            weights = self.weights

        while rules:
            rule = random.choices(rules, cum_weights=weights, k=1)[0]
            result = rule(ctx, overwrite, ignore_phase=self.ignore_phase) #NOTE: Context action/evaluation results only store result of LAST rule
            if not self.repeat_if_not_applicable or result is not Rule.NOT_APPLICABLE:
                break
            rules.remove(rule)
            weights = list(accumulate(r.priority.value for r in rules))
        return result

# Provide necessary imports for the evaluation_function module but prevents circular imports

import classes.evaluation_function as __evaluation_function
__evaluation_function.Rule = Rule
__evaluation_function.Context = Context
