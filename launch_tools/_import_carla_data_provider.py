# pylint: disable=unused-import
"""
Import the CarlaDataProvider from the scenario_runner submodule
"""

from typing import TYPE_CHECKING

__all__ = ['CarlaDataProvider', 'GameTime']

try:
    # SCENARIO_RUNNER_ROOT takes precedence
    from srunner.scenariomanager.carla_data_provider import CarlaDataProvider # pyright: ignore[reportMissingImports]
    from srunner.scenariomanager.timer import GameTime                        # pyright: ignore[reportMissingImports]
except ImportError:
    try:
        from scenario_runner import srunner
        from scenario_runner.srunner.scenariomanager.carla_data_provider import CarlaDataProvider
        print("Using srunner from ", srunner.__file__)
        # Allows submodules to detect the "srunner" package
        import sys
        sys.path.append(srunner.__path__[0].rsplit("/", 1)[0])
        from scenario_runner.srunner.scenariomanager.timer import GameTime
        # Fix import problems if srunner is in PYTHONPATH and submodule is not used.
        del srunner
    except Exception as e:  # noqa: BLE001
        raise e from None
else:
    try:
        # Check if submodule is available
        from scenario_runner.srunner.scenariomanager.carla_data_provider import CarlaDataProvider as X  # noqa: N814
        del X
    except ImportError:
        import srunner  # pyright: ignore[reportMissingImports]
        print("Using srunner from ", srunner.__file__)
        del srunner
    else:
        import os
        if "READTHEDOCS" not in os.environ: # this module is mocked
            print("=====================================================")
            print("WARNING: srunner is likely in PYTHONPATH, submodule `scenario_runner` is not used. "
                  "CarlaDataProvider might be duplicated and not used correctly.")
            print("=====================================================")

if TYPE_CHECKING:
    # still use submodule for type-hints
    from scenario_runner.srunner.scenariomanager.carla_data_provider import CarlaDataProvider
    from scenario_runner.srunner.scenariomanager.timer import GameTime
