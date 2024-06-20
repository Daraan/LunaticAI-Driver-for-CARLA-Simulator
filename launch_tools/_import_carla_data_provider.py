"""
Import the CarlaDataProvider from the scenario_runner submodule
"""

from typing import TYPE_CHECKING

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