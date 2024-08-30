"""
Helper library to define type protocols for classes and functions in the project.

See Also:
    Useful references:
        - https://docs.python.org/3/library/typing.html
        - https://docs.python.org/3/library/stdtypes.html#types-genericalias
        - https://typing-extensions.readthedocs.io/en/latest/
"""

# pyright: strict

from __future__ import annotations

import sys
from typing import Callable, Hashable, TYPE_CHECKING, Any, Optional, Sequence, Union
from typing_extensions import (Protocol, ParamSpec, Concatenate,
                               TypeAlias, TypeVar, TypeAliasType, Literal)
import carla  # type: ignore


if TYPE_CHECKING:
    from agents.tools.config_creation import AgentConfig
    from agents.navigation.local_planner import LocalPlanner
    from agents.dynamic_planning.dynamic_local_planner import DynamicLocalPlanner  # noqa: F401
    from classes.rule import Rule, Context
    from classes.evaluation_function import ConditionFunction
    from agents.tools.config_creation import BehaviorAgentSettings, LunaticAgentSettings  # noqa: F401
    from classes.worldmodel import WorldModel
    from classes.constants import AgentState

__all__ = [
    "RuleT",
    "CallableCondition",
    "CallableAction",
    "CallableT",
    "AgentConfigT",
    "ConditionFunctionLike",
    "AnyConditionFunctionLike",
    "AnyConditionFunctionLikeT",
    "AnyCallableCondition",
    "CallableConditionT",
    "AnyCallableAction",
    "CallableActionT",
    "ConditionFunctionLikeT",
    
    # Protocols
    "HasBaseSettings",
    "HasConfig",
    "HasContext",
    "Has_WorldModel",
    "HasStates",
    "Has_Vehicle",
    "HasPlanner",
    "HasPlannerWithConfig",
    "UseableWithDynamicPlanner",
    
    "CanDetectObstacles",
    "CanDetectNearbyObstacles",
    "CanDetectNearbyTrafficLights",
]

_T = TypeVar("_T", default=Any)
_H = TypeVar("_H", bound=Hashable)   # Free
_CH = TypeVar("_CH", bound=Hashable, default=Hashable)  # Generic of ConditionFunction

_P = ParamSpec("_P", default=[])   # Free, e.g. for action function.
_CP = ParamSpec("_CP", default=[]) # Generic of ConditionFunction

RuleT = TypeVar("RuleT", bound="Rule", default="Rule")
""":py:class:`typing.TypeVar`: A type variable for a :py:class:`.Rule` type."""

_A = TypeVar("_A", bound=carla.Actor, default=carla.Actor)

# NOTE: This requires a stub file where ActorList is Generic
if TYPE_CHECKING:
    _Generic_carlaActorList = carla.ActorList[_A]
else:
    _Generic_carlaActorList = TypeAliasType("_Generic_carlaActorList", carla.ActorList, type_params=(_A,))

ActorList : TypeAlias = Union[_Generic_carlaActorList[_A], Sequence[_A]]
"""Type alias for a sequence of carla actors."""


CallableCondition : TypeAlias = Union[
                        Callable[Concatenate[RuleT, "Context", _CP], _CH],  # With Rule
                        Callable[Concatenate["Context", _CP], _CH]          # Only Context
                        ]
"""
A :term:`generic type` alias for a callable condition function to be used with a :py:class:`.ConditionFunction`.
Its first arguments must accept a :py:class:`.Rule` and a :py:class:`.Context`,
or only a :py:class:`.Context`, additional keyword arguments are allowed.
It must return a :term:`hashable` value.
"""

CallableAction : TypeAlias = Union[
                        Callable[Concatenate[RuleT, "Context", _P], _T],  # With Rule
                        Callable[Concatenate["Context", _P], _T]          # Only Context
                        ]
"""
A :term:`generic type` alias for a callable action function to be used with a :py:class:`.Rule`
or :py:meth:`.ConditionFunction.register_action`.
Its first arguments must accept a :py:class:`.Rule` and a :py:class:`.Context`,
or only a :py:class:`.Context`, additional keyword arguments are allowed.
It can return an arbitrary value.
"""


CallableT = TypeVar("CallableT", bound=Callable[..., Any])
""":py:class:`typing.TypeVar`: A type variable for a any callable."""

AgentConfigT = TypeVar("AgentConfigT", bound="AgentConfig", default="AgentConfig",
                         infer_variance=True)
""":py:class:`typing.TypeVar`: A type variable for a :py:class:`.AgentConfig` type."""

ConditionFunctionLike = TypeAliasType("ConditionFunctionLike",
                                      Union[CallableCondition[RuleT, _CP, _CH],
                                            "ConditionFunction[_CP, _CH]"],
                                      type_params=(RuleT, _CP, _CH))
"""
Callable that can be used for :py:attr:`.Rule.condition`.
A callable that uses a :py:class:`Context` object as a single argument,
or alternatively a :py:class:`Rule` and a :py:class:`Context` object (in this order).

The function must return a :term:`Hashable` value.
"""

ConditionFunctionLikeT = ... # Version limitation, fixing done below
""":py:class:`.TypeVar` version of :py:obj:`ConditionFunctionLike`"""


AnyConditionFunctionLike = TypeAliasType("AnyConditionFunctionLike",
    Union[CallableCondition[RuleT, _CP, _CH],
          "ConditionFunction[_CP, _CH]"], type_params=(RuleT, _CP, _CH))
"""
A :term:`generic type` alias for a callable condition function to be used with a :py:class:`.Rule`.
Its first arguments must accept a :py:class:`.Rule` and a :py:class:`.Context`,
or only a :py:class:`.Context`, additional keyword arguments are allowed.
It must return a :term:`hashable` value.
"""

AnyConditionFunctionLikeT = TypeVar("AnyConditionFunctionLikeT", bound=AnyConditionFunctionLike)

# Python 3.11+
if TYPE_CHECKING or sys.version_info >= (3, 11):
    AnyCallableCondition: TypeAlias = CallableCondition[RuleT, ..., Hashable]
    """Non generic variant of :py:obj:`CallableCondition`, can use used as :py:class:`typing.TypeAlias`."""

    AnyCallableAction : TypeAlias = CallableAction[RuleT, ..., Any]
    """Non generic variant of :py:obj:`CallableAction`, can use used as :py:class:`typing.TypeAlias`."""
    
    ConditionFunctionLikeT = TypeVar("ConditionFunctionLikeT", bound=ConditionFunctionLike["Rule", ..., Hashable])
    """:py:class:`.TypeVar` version of :py:obj:`ConditionFunctionLike`"""

# handle version conflicts with ParamSpec, Concatenate and Ellipsis
# NOTE: Near-Future typing_extension upgrades should make this easier.
elif sys.version_info[:2] <= (3, 10):
    __ellipsis_dummy = ParamSpec("__ellipsis_dummy")
    # Create valid concatenate types
    __ConcatRC = Concatenate["Rule", "Context", __ellipsis_dummy]
    __ConcatC = Concatenate["Context", __ellipsis_dummy]
    
    AnyCallableAction = CallableAction["Rule", __ellipsis_dummy, Any]
    AnyCallableCondition = CallableCondition["Rule",  __ellipsis_dummy, Hashable]
    
    __ConditionFunctionLikeBound = ConditionFunctionLike["Rule", __ellipsis_dummy, Hashable]
    
    # Remove dummy parameter
    __ConcatRC.__args__ = __ConcatRC.__args__[:-1] + (...,)
    __ConcatC.__args__ = __ConcatC.__args__[:-1] + (...,)
    __ConditionFunctionLikeBound.__args__ = tuple(a if a is not __ellipsis_dummy
                                                  else ...
                                                  for a in __ConditionFunctionLikeBound.__args__)
    AnyCallableCondition.__args__[0].__args__ = (__ConcatRC, Hashable)
    AnyCallableCondition.__args__[1].__args__ = (__ConcatC, Hashable)
    AnyCallableAction.__args__[0].__args__ = (__ConcatRC, Any)
    AnyCallableAction.__args__[1].__args__ = (__ConcatC, Any)
    AnyCallableCondition.__parameters__ = AnyCallableCondition.__args__[0].__parameters__ = \
        AnyCallableCondition.__args__[1].__parameters__ = AnyCallableAction.__parameters__ = \
        AnyCallableAction.__args__[0].__parameters__ = AnyCallableAction.__args__[1].__parameters__= \
        __ConditionFunctionLikeBound.__parameters__ = ()
    
    ConditionFunctionLikeT = TypeVar("ConditionFunctionLikeT", bound=__ConditionFunctionLikeBound)
else:
    # Works for older typing_extensions versions, e.g. 4.10.0 and Python3.10
    AnyCallableCondition = CallableCondition["Rule", Concatenate[...], Hashable]
    AnyCallableAction = CallableAction["Rule", Concatenate[...], Any]
    
CallableConditionT = TypeVar("CallableConditionT", bound=AnyCallableCondition)
""":py:class:`typing.TypeVar` variant of :py:obj:`AnyCallableCondition`."""

CallableActionT = TypeVar("CallableActionT", bound=AnyCallableAction)
""":py:class:`typing.TypeVar` variant of :py:obj:`AnyCallableAction`."""


# ------------- Protocols -------------

class HasBaseSettings(Protocol[AgentConfigT]):
    BASE_SETTINGS: type[AgentConfigT]
    
class HasConfig(Protocol[AgentConfigT]):
    @property # Note: Must be read-only, can be normal attribute when implemented
    def config(self) -> AgentConfigT:
        """
        read-only attribute of a :py:class:`.AgentConfig` object; can also be a normal attribute.
        """
        ...

_LocalPlannerT = TypeVar("_LocalPlannerT",
                         bound="LocalPlanner",
                         default="LocalPlanner",
                         covariant=True)
""":py:class:`typing.TypeVar`: A type variable for a :py:class:`.LocalPlanner` type."""

class HasPlanner(Protocol[_LocalPlannerT]):
    """
    Uses a Local planner to calculate controls
    """
    
    @property
    def _local_planner(self) -> _LocalPlannerT:
        """
        read-only attribute for a :py:class:`.LocalPlanner` object; can also be a normal attribute.
        
        :meta public:
        """
        ...
    
    def _calculate_control(self, debug: bool=False, *args, **kwargs) -> carla.VehicleControl:  # pyright: ignore
        """
        :meta public:
        """
        ...

class HasPlannerWithConfig(HasPlanner["DynamicLocalPlanner"], HasConfig[AgentConfigT], Protocol):
    """
    Uses a :py:class:`.DynamicLocalPlanner` that works with a :py:class:`.AgentConfig`
    """
    ...
    
class HasContext(Protocol):
    ctx: "Context"

class Has_WorldModel(Protocol):
    _world_model: "WorldModel"
    """
    :meta public:
    """
    
class HasStates(Protocol):
    current_states: dict["AgentState", int]
    
class Has_Vehicle(Protocol):
    _vehicle: carla.Vehicle
    """
    :meta public:
    """
    
class UseableWithDynamicPlanner(HasPlannerWithConfig, Has_Vehicle, HasContext, Protocol):
    """Can be used with :py:class:`.DynamicLocalPlanner`."""
    ...

class CanDetectObstacles(Has_Vehicle, HasPlanner,
                         HasConfig["BehaviorAgentSettings | LunaticAgentSettings"],
                         Protocol):
    """Can be used with :py:func:`lunatic_agent_tools.detect_obstacles`."""
    ...
    
class CanDetectNearbyObstacles(CanDetectObstacles, Protocol):
    """Can be used with :py:func:`lunatic_agent_tools.detect_obstacles_in_path`."""
    
    all_obstacles_nearby : list[carla.Actor]
    """Actors that are considered to be near the actor."""

    def max_detection_distance(self, lane: Literal["same_lane", "other_lane"]) -> float:
        """
        Convenience function to be used with :py:func:`lunatic_agent_tools.detect_vehicles`
        and :any:`LunaticAgent.detect_obstacles_in_path`.

        The max distance to consider an obstacle in the same lane or in another lane, obstacles
        further away will be ignored.

        Parameters:
            self : An object that implements the `config` and `live_info` attributes
            lane : The lane to consider.
        """
        ...

class CanDetectNearbyTrafficLights(CanDetectObstacles, HasStates, Has_WorldModel, Protocol):
    """Can be used with :py:func:`lunatic_agent_tools.detect_obstacles_in_path`."""
    
    traffic_lights_nearby : list[carla.TrafficLight]
    """Actors that are considered to be near the actor."""
    
    _last_traffic_light : Optional[carla.TrafficLight]
    
    _current_waypoint : carla.Waypoint
