try:
    import carla
except ImportError as e:
    from launch_tools.egg_import import import_carla
    carla = import_carla()

from . import argument_parsing
from . import blueprint_helpers
from .general import *

# backwards compatibility
prepare_blueprints = blueprint_helpers.get_contrasting_blueprints