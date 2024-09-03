"""Helper module that contains all the custom exceptions used in the project"""

from typing import Any

import carla

from classes.constants import Hazard, RuleResult

__all__ = [
    "UserInterruption",
    "LunaticAgentException",
    "AgentDoneException",
    "ContinueLoopException",
    "SkipInnerLoopException",
    "EmergencyStopException",
    "UpdatedPathException",
    "NoFurtherRulesException",
    "DoNotEvaluateChildRules",
    "UnblockRuleException",
    "_RuleResultException"
]

class UserInterruption(Exception):
    """
    Terminate the loop if user input is detected.
    Allows the scenario runner and Leaderboard_ to exit gracefully, if
    handled appropriately, e.g. by directly returning.

    Thrown by :py:meth:`LunaticAgent.parse_keyboard_input <agents.lunatic_agent.LunaticAgent.parse_keyboard_input>`.
    
    Note:
        Is not a :py:class:`LunaticAgentException`.
    """

class LunaticAgentException(Exception):
    """
    Base class for all custom exceptions that influence the Workflow of the :py:class:`.LunaticAgent`.
    """

class AgentDoneException(LunaticAgentException):
    """
    Raised when there is no more waypoint in the queue to follow and no rule set a new destination.

    When the a :py:class:`GameFramework` instance is used as context manager will set :py:attr:`game_framework.continue_loop <classes.worldmodel.GameFramework.continue_loop>` to :python:`False`.
    """


class ContinueLoopException(LunaticAgentException):
    """
    Raise when :py:meth:`.LunaticAgent.run_step` action of the agent should not be continued further.

    The agent returns the current :python:`ctx.control` to the caller of :code:`run_step`.

    Note:
        Handled in :py:meth:`.LunaticAgent.run_step`, this exception should not propagate outside.
        It can be caught by :py:class:`.GameFramework` and skip the current loop and not apply any controls,
        an error will be logged.
    """


class SkipInnerLoopException(LunaticAgentException):
    """
    Can be raised in `LunaticAgent._inner_step`. A new control object must be provided.
    """

    planned_control : carla.VehicleControl

    def __init__(self, planned_control : carla.VehicleControl, *args: object) -> None:
        if not isinstance(planned_control, carla.VehicleControl):
            raise TypeError("Must provide a carla.VehicleControl instance to raise a SkipInnerLoopException")
        super().__init__(*args)
        self.planned_control = planned_control


class EmergencyStopException(LunaticAgentException):

    hazards_detected : "set[Hazard]"

    def __init__(self, hazards: "set[Hazard]", *args: object) -> None:
        super().__init__(*args)
        self.hazards_detected = hazards


class UpdatedPathException(LunaticAgentException):
    """
    Should be raised when the path has been updated and the agent should replan.

    Rules that replan on Phase.DONE | END, should throw this exception at the end.
    """

class _RuleResultException(LunaticAgentException):
    """
    Abstract class for exceptions that can be raised by rules
    **that still are able to return a result**.
    
    :meta public:
    """
    
    result : Any = RuleResult.NO_RESULT
    
    def __init__(self, result: Any = RuleResult.NO_RESULT, *args : object):
        super().__init__(*args)
        self.result = result

class NoFurtherRulesException(_RuleResultException):
    """
    Raised when no further rules should be executed in this phase.
    
    Caught by :py:meth:`.LunaticAgent.execute_phase`.
    
    The agent will continue at the phase where the :py:class:`BlockedRule` was triggered.
    """
    

class DoNotEvaluateChildRules(_RuleResultException):
    """
    Can be raised in a :py:class:`MultiRule` to prevent the evaluation of child rules.

    Can also be raised by child rules to prevent the evaluation of further child rules.
    """
    
class UnblockRuleException(_RuleResultException):
    """
    Can be raised in a :py:class:`BlockedRule` to end it.
    
    The agent will continue at the phase where the :py:class:`BlockedRule` was triggered.
    
    Note:
        Further rules that are in this phase can still be executed.
        Alternatively, consider raising a :py:class:`NoFurtherRulesException`.
    """
