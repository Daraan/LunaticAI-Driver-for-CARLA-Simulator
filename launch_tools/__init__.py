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
from ._import_carla_data_provider import CarlaDataProvider, GameTime
from ._version_handling import *

from . import argument_parsing
from . import blueprint_helpers
from .csv_tools import *

# backwards compatibility
prepare_blueprints = blueprint_helpers.get_contrasting_blueprints

