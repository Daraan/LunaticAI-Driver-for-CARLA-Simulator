"""Helper module that contains all the custom exceptions used in the project"""

import carla

from classes.constants import Hazard


class LunaticAIException(Exception):
    """
    Base class for all custom exceptions in the project.
    """

class AgentDoneException(LunaticAIException):
    """
    Raised when there is no more waypoint in the queue to follow and no rule set a new destination.

    When the a GameFramework instance is used as context manager will set game_framework.continue_loop to False.
    """


class ContinueLoopException(LunaticAIException):
    """
    Raise when `run_step` action of the agent should not be continued further.

    The agent returns the current ctx.control to the caller of run_step.

    Note:
        Handled in Agent.run_step, this exception should not propagate outside.
        It can be caught by GameFramework and skip the current loop and not apply any controls, 
        an error will be logged.
    """


class SkipInnerLoopException(LunaticAIException):
    """
    Can be raised in `LunaticAgent._inner_step`. A new control object must be provided.
    """

    planned_control : carla.VehicleControl

    def __init__(self, planned_control : carla.VehicleControl, *args) -> None:
        if not isinstance(planned_control, carla.VehicleControl):
            raise TypeError("Must provide a carla.VehicleControl instance to raise a SkipInnerLoopException")
        super().__init__(*args)
        self.planned_control = planned_control


class EmergencyStopException(LunaticAIException):

    hazards_detected : "set[Hazard]"

    def __init__(self, hazards: "set[Hazard]", *args: object) -> None:
        super().__init__(*args)
        self.hazards_detected = hazards


class UserInterruption(Exception):
    """
    Terminate the loop if user input is detected.
    Allows the scenario runner and leaderboard to exit gracefully, if 
    handled appropriately, e.g. by directly returning.

    Thrown by [LunaticAgent.parse_keyboard_controls](#agents.lunatic_agent.LunaticAgent.parse_keyboard_controls).
    """


class UpdatedPathException(LunaticAIException):
    """
    Should be raised when the path has been updated and the agent should replan.

    Rules that replan on Phase.DONE | END, should throw this exception at the end.
    """


class DoNotEvaluateChildRules(LunaticAIException):
    """
    Can be raised in a MultiRule to prevent the evaluation of child rules.

    Can also be raised by child rules to prevent the evaluation of further child rules.
    """