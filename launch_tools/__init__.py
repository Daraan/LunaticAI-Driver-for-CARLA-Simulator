# pylint: disable=unused-import
"""
Handles problematic import deriving from version conflicts
"""

# If carla is not installed try to find the .egg file
try:
    import carla
except ImportError as e:
    from launch_tools._egg_import import import_carla
    carla = import_carla()

# Import scenario runner from submodule or SCEANRIO_RUNNER_ROOT
from functools import partial
from typing import TYPE_CHECKING, Type, Union

if TYPE_CHECKING:
    from agents.tools.config_creation import AgentConfig

from ._import_carla_data_provider import CarlaDataProvider, GameTime
from ._version_handling import *

from . import argument_parsing
from . import blueprint_helpers
from .csv_tools import *

# backwards compatibility
prepare_blueprints = blueprint_helpers.get_contrasting_blueprints


class class_or_instance_method:
    """Decorator to transform a method into both a regular and class method"""

    def __init__(self, call):
        self.__wrapped__ = call
        self._wrapper = lambda x : x # TODO/BUG: functools.partial and functools.wraps shadow the signature and doc, this reveals it again.

    if TYPE_CHECKING:
        def __get__(self, instance : Union[None, "AgentConfig"], owner : Type["AgentConfig"]):
            if instance is None:  # called on class 
                return self._wrapper(partial(self.__wrapped__, owner))
            return self._wrapper(partial(self.__wrapped__, instance)) # called on instance
    else:
        def __get__(self, instance : Union[None, "AgentConfig"], owner : Type["AgentConfig"]):
            if instance is None:  # called on class 
                return partial(self.__wrapped__, owner)
            return partial(self.__wrapped__, instance) # called on instance

