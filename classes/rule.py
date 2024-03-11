from __future__ import annotations 
from collections.abc import Mapping
from functools import wraps
import inspect
try: # Python 3.8+
    from functools import singledispatchmethod
except ImportError:
    from functools import singledispatch, update_wrapper

    def singledispatchmethod(func):
        dispatcher = singledispatch(func)
        def wrapper(*args, **kw):
            return dispatcher.dispatch(args[1].__class__)(*args, **kw)
        wrapper.register = dispatcher.register
        update_wrapper(wrapper, func)
        return wrapper
    
from itertools import accumulate
import random
from enum import IntEnum
from typing import Any, ClassVar, List, Set, Tuple, Union, Iterable, Callable, Optional, Dict, Hashable, TYPE_CHECKING
from weakref import WeakSet

from omegaconf import DictConfig, OmegaConf

from classes.constants import Phase
from utils.evaluation_function import EvaluationFunction

if TYPE_CHECKING:
    import carla
    from agents.lunatic_agent import LunaticAgent
    from conf.agent_settings import LunaticAgentSettings


class Context:
    """
    Object to be passed as the first argument (instead of self) to rules, actions and evaluation functions.
    
    NOTE: That Context.config are the read-only settings for the given rule and actions with potential overwrites.
    """
    agent : "LunaticAgent"
    config : "LunaticAgentSettings"
    
    evaluation_results : Dict["Phase", Hashable] # ambigious wording, which result? here evaluation result
    action_results : Dict["Phase", Any] 
    
    control : Optional["carla.VehicleControl"]
    _control : Optional["carla.VehicleControl"]
    
    prior_result : Optional[Any]
    
    last_context : Optional["Context"]

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
        return self.agent.current_phase
    
    @property
    def control(self) -> Union["carla.VehicleControl", None]:
        return self._control
    
    @control.setter
    def control(self, control : "carla.VehicleControl"):
        if control is None:
            raise ValueError("Context.control must not be None. To set it to None explicitly use set_control.")
        self._control = control
        
    def set_control(self, control : Optional["carla.VehicleControl"]):
        self._control = control
    
    def end_of_phase(self):
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
def always_execute(ctx : Context):
    return True


class _CountdownRule:

    # TODO: low prio: make cooldown dependant of tickrate or add a conversion from seconds to ticks OR make time-based
    tickrate : ClassVar[int] = NotImplemented

    DEFAULT_COOLDOWN_RESET : ClassVar[int] = 0
    _cooldown : int # if 0 the rule can be executed

    # Keep track of all instances for the cooldowns
    instances : ClassVar[WeakSet["_CountdownRule"]] = WeakSet()

    def __init__(self, cooldown_reset_value : Optional[int] = None, enabled: bool = True):
        self.instances.add(self)
        self._cooldown = 0
        self.max_cooldown = cooldown_reset_value or self.DEFAULT_COOLDOWN_RESET
        self._enabled = enabled

    def is_ready(self) -> bool:
        """Group aware check if a rule is ready."""
        return self.enabled and self.cooldown == 0 # Note: uses property getters. Group aware for GroupRules
    
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
            
    @property
    def enabled(self) -> bool:
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
            if exc_type is None:
                Rule.update_all_cooldowns()


class _GroupRule(_CountdownRule):
    group : Optional[str] = None # group of rules that share a cooldown

    # first two values in the list are current and max cooldown, the third is a set of all instances
    group_instances : ClassVar[Dict[str, List[int, int, WeakSet["_GroupRule"]]]] = {}
    
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
    actions : Dict[Any, Callable[[Context], Any]]
    description : str
    overwrite_settings : Dict[str, Any]
    phases : Set["Phase"]

    group : Optional[str] = None # group of rules that share a cooldown

    # Indicate that no rule was applicable in the current phase
    # i.e.  rule(ctx) in actions was False 
    NOT_APPLICABLE : ClassVar = object()

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
                 rule : Callable[[Context], Hashable], 
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
                 ) -> None:
        if action is not None and actions is not None:
            raise ValueError("Only one of 'action' and 'actions' can be set.")
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
        if not isinstance(description, str):
            raise ValueError(f"description must be of type str, not {type(description)}")
        super().__init__(group or self.group, cooldown_reset_value, enabled) # or self.group for subclassing
        self.priority : float | int | RulePriority = priority # used by agent.add_rule

        self.phases = phases
        if action is None:
            self.actions = actions
        elif isinstance(action, dict):
            self.actions = action
            if false_action is not None or actions is not None:
                raise ValueError("When passing a dict to action, false_action and actions must be None")
        else:
            self.actions = {}
            if action is not None:
                self.actions[True] = action
            if false_action is not None:
                self.actions[False] = false_action
        
        self.rule = rule
        self.description = description
        self.overwrite_settings = overwrite_settings or {}
        
    def __init_subclass__(cls) -> None:
        """
        Automatically creates a __init__ function to allow for a simple to use class-interface to create rule classes.
        
        By setting __no_auto_init = True in the class definition, the automatic __init__ creation is disabled.
        """
        if not "__init__" in cls.__dict__ and not cls.__dict__.get("__no_auto_init", False):
            params = inspect.signature(cls.__init__).parameters # find overlapping parameters
            @wraps(cls.__init__)
            def partial_init(self, phases=None, *args, **kwargs):
                phases = getattr(cls, "phases")
                kwargs.update({k:v for k,v in cls.__dict__.items() if k in params and k != "phases"})
                super(cls, self).__init__(phases, *args, **kwargs)
            
            #cls.__init__ = partialmethod(cls.__init__, phases, **{k:v for k,v in cls.__dict__.items() if k in params and k != "phases"})
            cls.__init__ = partial_init
    
    @__init__.register(_CountdownRule)
    @__init__.register(type)
    def __init_by_decorating_class(self, cls):
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
        if not ignore_phase and ctx.agent.current_phase not in self.phases:
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
        return self.__class__.__name__ + f"(description={self.description}, phases={self.phases}, group={self.group}, priority={self.priority}, actions={self.actions}, rule={self.rule}, cooldown={self.cooldown})" 

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
