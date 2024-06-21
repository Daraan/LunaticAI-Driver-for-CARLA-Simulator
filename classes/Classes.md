# Classes

## GameFramework

The [`GameFramework`](#GameFramework) is a helper-class class for a quicker setup, it can manage the game loop of the agent and take care of:

- Initialization of:
  - carla
  - pygame
  - traffic manager
  - agent, [WorldModel](#WorldModel), [Carlas's GlobalRoutePlanner](https://github.com/carla-simulator/carla/blob/master/PythonAPI/carla/agents/navigation/global_route_planner.py), [KeyboardControler](#TODO)
- Cooldowns of rules
- Load the [LaunchConfig](../conf/ConfigFiles.md) via [Hydra's compose API](https://hydra.cc/docs/advanced/compose_api/)
- Interface to the [CarlaDataProvider](https://github.com/carla-simulator/scenario_runner/blob/master/srunner/scenariomanager/carla_data_provider.py) from the [scenario_runner](https://github.com/carla-simulator/scenario_runner) package.
- Handling of special [`Exceptions`](#Exceptions) during the agent's `run_step` loop
- Ticking of the world HUD rendering [`render_everything`](#classes.worldmodel.GameFramework.render_everything).  Note: This function is the recommended way to render everything.

## WorldModel

The [`WorldModel`](#WorldModel) is a helper-class similar to the `World` classes used in the [`examples in Carla`](https://github.com/carla-simulator/carla/tree/dev/PythonAPI/examples).
It is a extension of the [`carla.World`](https://carla.readthedocs.io/en/latest/python_api/#carla.World) class and provides the following functionalities:

- HUD management
  - Camera setup and management
  - Some sensors for the pygame user interface, displayed on the HUD
  - Toggling of [`carla.MapLayers`](https://carla.readthedocs.io/en/latest/python_api/#carla.MapLayer)
- [`RSS`](https://carla.readthedocs.io/en/latest/adv_rss/) features
- Weather change
- Spawning of the ego actor (optional)
  - Or wait until an external script provides it. Command line argument `external_actor="<actor name, default 'hero'>"`.
- Ticking (`sync=True`) or waiting for the tick (`sync=False`) of the [`carla.World`](https://carla.readthedocs.io/en/latest/python_api/#carla.World)
- Some cleanup tasks when the script ends
- HUD rendering. Note that [`GameFramework.render_everything`](#classes.worldmodel.GameFramework.render_everything) extends this function and is the prefered way to render.

## HUD and Camera Manager

The [`HUD`](#classes.HUD.HUD) is a modification of the HUD used in the [manual_control RSS example of Carla](https://github.com/carla-simulator/carla/blob/master/PythonAPI/examples/rss/manual_control_rss.py).

It closely combines with the [`CameraManager`](#classes.camera_manager.CameraManager) to provide the visual human interface for the pygame window.

## Rule

See the [`Rule documentation`](../agents/rules/Rules.md) for details.

## RSSSensor and Visualization

 See the [`RSS documentation`](https://carla.readthedocs.io/en/latest/adv_rss/) from Carla.

## KeyboardControls

See [`RSSKeyboardControl` API](#classes.keyboard_controls.RSSKeyboardControl) for a more details.

## Constants and Enums

See the [`constants`](#classes.constants) API description.

## carla_originals

This package contains (mostly) unmodified classes extracted from [`the examples provided by Carla`](https://github.com/carla-simulator/carla/tree/dev/PythonAPI/examples)

## Driver, Vehicle, VehicleSpawner

These are classes that are deprecated or will be merged or are up to major changes.

## Rule Interpreter

This class allows for an alternative way to execute rules through different interfaces (python, yaml, xml, etc). It is not yet further integrated and documented.

## Exceptions

- `AgentDoneException`  
  Raised when there is no more waypoint in the queue to follow and no rule set a new destination.

- `ContinueLoopException`  
    Raise when the `agent.run_step` of the agent should not be continued further.
    The agent then returns the current ctx.control to the caller of run_step.
- `UserInterruption`  
    Terminate the `run_step` loop if user input is detected, for example `KeyboardInterrupt` or a pygame hotkey like <kbd>Esc</kbd>.
    This allows the scenario runner and leaderboard to exit gracefully.
- `UpdatedPathException`  
  Should be raised when the path has been updated and the agent should replan.  
  `Phase.DONE | END`
