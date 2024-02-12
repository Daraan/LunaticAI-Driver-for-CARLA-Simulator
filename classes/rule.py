from enum import IntEnum
from typing import Any, Set, Union, Iterable, Callable, Optional, Dict, Hashable, TYPE_CHECKING
from collections.abc import Iterable

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
    Priority of a rule. The smaller a value, the higher the priority.
    Rules are sorted by their priority before being applied.
    """
    HIGHEST = -10
    HIGH = -5
    NORMAL = 0
    LOW = 5
    LOWEST = 10

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

    def __call__(self, ctx : Context, overwrite: Optional[Dict[str, Any]] = None) -> Any:
        # Check phase
        if ctx.agent.current_phase not in self.apply_in_phases:
            return None # not applicable for this phase
        result = self.evaluate(ctx, overwrite)
        ctx.evaluation_results[ctx.agent.current_phase] = result
        if result in self.actions: # TODO: allow for multiple actions / weighted random actions
            action_result = self.actions[result](ctx, overwrite) #todo allow priority, random chance
            ctx.action_results[ctx.agent.current_phase] = action_result
            return action_result
        return None



