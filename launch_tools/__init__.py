from typing import cast, TYPE_CHECKING

try:
    import carla
except ImportError as e:
    from launch_tools.egg_import import import_carla
    carla = import_carla()


try:
    from srunner.scenariomanager.carla_data_provider import CarlaDataProvider
except ImportError:
    # Fix import problems if srunner is in PYTHONPATH and submodule is not used.
    from scenario_runner.srunner.scenariomanager.carla_data_provider import CarlaDataProvider # type: ignore
    if TYPE_CHECKING:
        from srunner.scenariomanager.carla_data_provider import CarlaDataProvider as X
        CarlaDataProvider = cast("type[X]", CarlaDataProvider)
        del X
else:
    try:
        from scenario_runner.srunner.scenariomanager.carla_data_provider import CarlaDataProvider as X # type: ignore
    except ImportError:
        pass
    else:
        print("=====================================================")
        print("WARNING: srunner is likely in PYTHONPATH, submodule `scenario_runner` is not used. CarlaDataProvider might be duplicated and not used correctly.")
        print("=====================================================")
        del X

from . import argument_parsing
from . import blueprint_helpers
from .general import *

# backwards compatibility
prepare_blueprints = blueprint_helpers.get_contrasting_blueprints

