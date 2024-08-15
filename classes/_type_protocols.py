from __future__ import annotations

from typing import ClassVar, TypeVar, TYPE_CHECKING, Mapping, Any
from typing_extensions import Protocol

import carla

if TYPE_CHECKING:
    from agents.tools.config_creation import AgentConfig, BasicAgentSettings
    from agents.navigation.local_planner import LocalPlanner
    from agents.dynamic_planning.dynamic_local_planner import DynamicLocalPlanner

AgentConfigT = TypeVar("AgentConfigT", bound="AgentConfig")

class HasBaseSettings(Protocol[AgentConfigT]):
    BASE_SETTINGS: type[AgentConfigT]
    
class HasConfig(Protocol[AgentConfigT]):
    config: AgentConfigT

class HasPlanner(Protocol):
    _local_planner: "LocalPlanner"
    
    def _calculate_control(self, debug: bool=False, *args, **kwargs) -> carla.VehicleControl:
        ...

class HasPlannerWithConfig(HasPlanner, HasConfig[AgentConfigT]):
    _local_planner: "DynamicLocalPlanner"