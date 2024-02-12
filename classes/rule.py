import random
from enum import IntEnum
from typing import Any, List, Set, Tuple, Union, Iterable, Callable, Optional, Dict, Hashable, TYPE_CHECKING

from omegaconf import DictConfig

from agents.tools.lunatic_agent_tools import Phase
from utils.evaluation_function import EvaluationFunction

if TYPE_CHECKING:
    import carla
    from agents.lunatic_agent import LunaticAgent

class Context:
    agent : "LunaticAgent"
    config : DictConfig
    evaluation_results : Dict[Phase, Hashable] # ambigious wording, which result? here evaluation result
    action_results : Dict[Phase, Any] 
    control : carla.VehicleControl

    def __init__(self, agent : "LunaticAgent", **kwargs):
        self.agent = agent
        self.control = None
        self._init_arguments = kwargs
        self.evaluation_results = {}
        self.action_results = {}
        self.last_phase_evaluation_results = {}
        self.last_phase_action_results = {}
        self.__dict__.update(kwargs)

    @property
    def current_phase(self) -> Phase:
        return self.agent.current_phase
    
    def set_control(self, control : carla.VehicleControl):
        self.control = control
    
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

class Rule:
    rule : EvaluationFunction
    actions : Dict[Any, Callable[[Context], Any]]
    description : str
    overwrite_settings : Dict[str, Any]
    apply_in_phases : Set[Phase]

    def __init__(self, 
                 phases : Union[Phase, Iterable], # iterable of Phases
                 rule : Callable[[Context], Hashable], 
                 action: Union[Callable, Dict[Any, Callable]] = None, 
                 false_action = None,
                 *, 
                 priority: RulePriority = RulePriority.NORMAL,
                 actions : Dict[Any, Callable[[Context], Any]] = None,
                 description: str = "What does this rule do?",
                 overwrite_settings: Optional[Dict[str, Any]] = None,
                 ignore_chance=0.2,
                 ) -> None:
        if not isinstance(phases, set):
            if isinstance(phases, Iterable):
                phases = set(phases)
            else:
                phases = {phases}
        for p in phases:
            if not isinstance(p, Phase):
                raise ValueError(f"phase must be of type Phases, not {type(p)}")
        self.priority : float | int | RulePriority = priority
        
        self.apply_in_phases = phases # TODO: CRITICAL: 
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

    def evaluate(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None) -> bool | Hashable:
        settings = self.overwrite_settings.copy()
        if overwrite is not None:
            settings.update(overwrite)
        ctx.config = ctx.agent.config.copy()
        ctx.config.update(settings)
        result = self.rule(ctx, settings)
        return result

    def __call__(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None, *, ignore_phase=False) -> Any:
        # Check phase
        if not ignore_phase or ctx.agent.current_phase not in self.apply_in_phases:
            return None # not applicable for this phase
        result = self.evaluate(ctx, overwrite)
        ctx.evaluation_results[ctx.agent.current_phase] = result
        if result in self.actions: # TODO: allow for multiple actions / weighted random actions
            action_result = self.actions[result](ctx, overwrite) #todo allow priority, random chance
            ctx.action_results[ctx.agent.current_phase] = action_result
            return action_result
        return None

class MultiRule(Rule):
    def __init__(self, 
                 phases: Union[Phase, Iterable], 
                 rules: List[Rule], 
                 rule=always_execute,
                 *,
                 ignore_phase=True,
                 priority: RulePriority = RulePriority.NORMAL, 
                 description: str = "If its own rule is true calls the passed rules."):
        """
        Initializes a Rule object.
        NOTE: Rules are evaluated in the order they are passed. Their priorities are not considered.

        Args:
            phases (Union[Phase, Iterable]): The phase or phases in which the rule should be active.
            rules (List[Rule]): The list of rules to be called if the rule's condition is true.
            rule: The condition that determines if the rule should be executed. Defaults to always_execute.
            ignore_phase (bool): Flag indicating whether to ignore the phase when evaluating the rule. Defaults to True.
            priority (RulePriority): The priority of the rule. Defaults to RulePriority.NORMAL.
            description (str): The description of the rule. Defaults to "If its own rule is true calls the passed rules.".
        """
        self.ignore_phase = ignore_phase
        self.rules = rules
        super().__init__(phases, rule=rule, action=self._action, description=description, priority=priority, ignore_phase=ignore_phase)
    
    def _action(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None) -> Any:
        results = []
        for rule in self.rules:
            result = rule(ctx, overwrite, ignore_phase=self.ignore_phase)
            result[rule] = result
        return results

class RandomRule(MultiRule):

    def _action(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None) -> Any:
        selection = random.choices(self.rules, cum_weights=self.weights, k=self.amount)
        results : List[Tuple[Rule, Any]] = []
        for rule in selection:
            result = rule(ctx, overwrite, ignore_phase=self.ignore_phase) #NOTE: Context action/evaluation results only store result of LAST rule
            results.append((rule, result))
        return results

    def __init__(self, 
                 phases : Union[Phase, Iterable], 
                 rules : Union[Dict[Rule, int | float], List[Rule]], 
                 amount : int = 1,
                 rule = always_execute, *, 
                 ignore_phase=True,
                 priority: RulePriority = RulePriority.NORMAL, 
                 description: str = "If its own rule is true calls one or more random rule from the passed rules.", 
                 weights: List[float] = None):
        if amount < 1:
            raise ValueError("Amount must be at least 1")
        if isinstance(rules, dict):
            if weights is not None:
                raise ValueError("When passing rules a dict with weights, the weights argument must be None")
            from itertools import accumulate
            self.weights = list(accumulate(rules.values())) # cumulative weights for random.choices are more efficient
            self.rules = list(rules.keys())
        else:
            self.weights = weights or list(accumulate(r.priority.value for r in rules))
            self.rules = rules
        self.amount = amount 
        super().__init__(phases, rule=rule, action=self._action, description=description, priority=priority, ignore_phase=ignore_phase, priority=priority)

            



