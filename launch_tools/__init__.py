from typing import cast, TYPE_CHECKING

try:
    import carla
except ImportError as e:
    from launch_tools.egg_import import import_carla
    carla = import_carla()

try:
    # SCENARIO_RUNNER_ROOT takes precedence
    from srunner.scenariomanager.carla_data_provider import CarlaDataProvider # type: ignore # pylint: disable=unused-import 
except ImportError:
    try:
        from scenario_runner.srunner.scenariomanager.carla_data_provider import CarlaDataProvider # pylint: disable=unused-import
        # Fix import problems if srunner is in PYTHONPATH and submodule is not used.
    except Exception as e:
        raise e from None
else:
    try:
        # Check if submodule is available
        from scenario_runner.srunner.scenariomanager.carla_data_provider import CarlaDataProvider as X
        del X
    except ImportError:
        import srunner # type: ignore
        print("Using srunner from ", srunner.__file__)
        del srunner
    else:
        print("=====================================================")
        print("WARNING: srunner is likely in PYTHONPATH, submodule `scenario_runner` is not used. CarlaDataProvider might be duplicated and not used correctly.")
        print("=====================================================")

if TYPE_CHECKING:
    from scenario_runner.srunner.scenariomanager.carla_data_provider import CarlaDataProvider # still use submodule for type-hints


from . import argument_parsing # noqa # pylint: disable=unused-import
from . import blueprint_helpers
from .general import *

# backwards compatibility
prepare_blueprints = blueprint_helpers.get_contrasting_blueprints

