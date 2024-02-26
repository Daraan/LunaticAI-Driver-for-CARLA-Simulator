from __future__ import annotations 
from functools import wraps
from itertools import accumulate
import random
from enum import IntEnum
from typing import Any, ClassVar, List, Set, Tuple, Union, Iterable, Callable, Optional, Dict, Hashable, TYPE_CHECKING
from weakref import WeakSet, WeakValueDictionary
import weakref

from omegaconf import DictConfig

from utils.evaluation_function import EvaluationFunction

from classes.constants import Phase
if TYPE_CHECKING:
    import carla
    from agents.lunatic_agent import LunaticAgent

class Context:
    """
    Object to be passed as the first argument (instead of self) to rules, actions and evaluation functions.
    """
    agent : "LunaticAgent"
    config : DictConfig
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

    DEFAULT_COOLDOWN_RESET : int = 0
    _cooldown : int # if 0 the rule can be executed

    # Keep track of all instances for the cooldowns
    instances : ClassVar[WeakSet["_CountdownRule"]] = WeakSet()

    def __init__(self, cooldown_reset_value : Optional[int] = None):
        self.instances.add(self)
        self._cooldown = 0
        self.max_cooldown = cooldown_reset_value or self.DEFAULT_COOLDOWN_RESET

    def is_ready(self) -> bool:
        return self._cooldown == 0
    
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
    
    class CooldownFramework:

        def __enter__(self):
            # Enter the context
            return self

        def __exit__(_, exc_type, exc_value, traceback):
            # Exit the context
            if exc_type is None:
                Rule.update_all_cooldowns()

class _GroupRule(_CountdownRule):
    group : Optional[str] = None # group of rules that share a cooldown

    # first two values in the list are current and max cooldown, the third is a set of all instances
    group_instances : ClassVar[Dict[str, List[int, int, WeakSet["_GroupRule"]]]] = {}
    
    def __init__(self, group :Optional[str]=None, cooldown_reset_value : Optional[int] = None):
        super().__init__(cooldown_reset_value)
        self.group = group
        if group is None:
            return
        if group not in self.group_instances:
            self.group_instances[group] = [0, self.max_cooldown, WeakSet()]
        self.group_instances[group][2].add(self)

    @property
    def cooldown(self) -> int:
        if self.group:
            return _GroupRule.group_instances[self.group][0]
        return super().cooldown
    
    def is_ready(self) -> bool:
        """Group aware check if a rule is ready."""
        return self.cooldown == 0 
    
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

    def __init__(self, 
                 phases : Union["Phase", Iterable["Phase"]], # iterable of Phases
                 rule : Callable[[Context], Hashable], 
                 action: Union[Callable[[Context], Any], Dict[Any, Callable]] = None, 
                 false_action = None,
                 *, 
                 actions : Dict[Any, Callable[[Context], Any]] = None,
                 description: str = "What does this rule do?",
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 priority: RulePriority = RulePriority.NORMAL,
                 cooldown_reset_value : Optional[int] = None,
                 group : Optional[str] = None,
                 ignore_chance = NotImplemented,
                 ) -> None:
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
        super().__init__(group or self.group, cooldown_reset_value) # or self.group for subclassing
        self.priority : float | int | RulePriority = priority # used by agent.add_rule

        self.phases = phases
        if isinstance(action, dict):
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

    def evaluate(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None) -> Union[bool,Hashable]:
        settings = self.overwrite_settings.copy()
        if overwrite is not None:
            settings.update(overwrite)
        ctx.config = ctx.agent.config.copy()
        ctx.config.update(settings)
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
            
            action_result = self.actions[result](ctx) #todo allow priority, random chance
            ctx.action_results[ctx.agent.current_phase] = action_result
            self._cooldown = self.max_cooldown
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
            super().__init__(phases, rule=rule, 
                             action=prior_action, 
                             description=description, 
                             overwrite_settings=overwrite_settings,
                             priority=priority, 
                             ignore_phase=ignore_phase,
                             cooldown_reset_value=cooldown_reset_value,)
    
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
                 weights: List[float] = None):
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
        super().__init__(phases, rule=rule, prior_action=prior_action, description=description, priority=priority, ignore_phase=ignore_phase)

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
