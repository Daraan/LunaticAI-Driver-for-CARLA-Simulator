# pyright: strict
# pylint: disable=unused-import
# pyright: reportUnusedImport=information
# pyright: reportMissingTypeStubs=none
"""
Handles problematic import deriving from version conflicts
"""

import sys

# If carla is not installed try to find the .egg file
try:
    import carla
except ImportError as e:
    from launch_tools._egg_import import import_carla
    carla = import_carla()

# Import scenario runner from submodule or SCENARIO_RUNNER_ROOT
from typing import TYPE_CHECKING, Callable, Optional
from typing_extensions import TypeVar, ParamSpec

from ._import_carla_data_provider import CarlaDataProvider, GameTime # type: ignore[import]
from ._version_handling import *

from . import argument_parsing # type: ignore[import]
from . import blueprint_helpers
from .csv_tools import *

# backwards compatibility
prepare_blueprints = blueprint_helpers.get_contrasting_blueprints


_T = TypeVar("_T")
_R_co = TypeVar("_R_co", covariant=True)
_Parameters = ParamSpec("_Parameters")
"""
instance_signature : Concatenate[_T, _P]
class signature : Concatenate[type[_T], _P]
"""

# pylint: disable=too-few-public-methods, invalid-name
class class_or_instance_method(classmethod[_T, _Parameters, _R_co] 
                               if sys.version_info >= (3, 11) or TYPE_CHECKING else 
                               classmethod):
    """
    Decorator to transform a method into both a regular and class method
    
    The first argument of the decorated function should be decorated with:
    :python:`type[Self] | Self` or :python:`Union[Type[Self], Self]`
    """

    def __get__(
        self, instance : Optional[_T], type_: "type[_T] | None" = None
    ) -> Callable[_Parameters, _R_co]:
        if instance is None:
            return super().__get__ (instance, type_)      # type: ignore # type_ is not None
        return self.__func__.__get__(instance, type_)

