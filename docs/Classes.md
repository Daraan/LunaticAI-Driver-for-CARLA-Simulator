# Classes Overview

```{eval-rst}
.. Note this is a MyST Markdown file to be used with Sphinx and will not render completely on GitHub. Build the documentation or refer to the online documentation at Read The Docs.
```

## GameFramework

The {py:class}`.GameFramework` is a helper-class class for a quicker setup, it can manage the game loop of the agent and take care of:

- Initialization of:
  - carla
  - pygame
  - traffic manager
  - agent, {py:class}`.WorldModel`, [CARLAS's GlobalRoutePlanner](gh:https://github.com/carla-simulator/carla/blob/master/PythonAPI/carla/agents/navigation/global_route_planner.py), {py:class}`.KeyboardController <RSSKeyboardControl>`
- Cooldowns of rules
- Load the [LaunchConfig](conf/ConfigFiles.md) via [Hydra's compose API](https://hydra.cc/docs/advanced/compose_api/){.external-icon}
- Interface to the [CarlaDataProvider](gh:https://github.com/carla-simulator/scenario_runner/blob/master/srunner/scenariomanager/carla_data_provider.py) from the [scenario_runner](gh:https://github.com/carla-simulator/scenario_runner) package.
- Handling of special [exceptions](#exceptions-overview) during the agent's `run_step` loop
- Ticking of the world HUD rendering {py:meth}`.GameFramework.render_everything`. Note: This function is the recommended way to render everything.

## WorldModel

The {py:class}`.WorldModel` is a helper-class similar to the `World` classes used in the [examples from CARLA](https://github.com/carla-simulator/carla/tree/dev/PythonAPI/examples){.external-icon}.
It is a extension of the [{external:class}`carla.World`]{.external-icon} class and provides the following functionalities:

- HUD management
  - Camera setup and management
  - Some sensors for the pygame user interface, displayed on the HUD
  - Toggling of [{external:class}`carla.MapLayer`]{.external-icon}
- [RSS](https://carla.readthedocs.io/en/latest/adv_rss/){.external-icon} features
- Weather change
- Spawning of the ego actor (optional)
  - Or wait until an external script provides it. Command line argument `external_actor="<actor name, default 'hero'>"`.
- Ticking (`sync=True`) or waiting for the tick (`sync=False`) of the [{external:class}`carla.World`]{.external-icon}
- Some cleanup tasks when the script ends
- HUD rendering. Note that {py:meth}`.GameFramework.render_everything` extends this function and is the preferred way to render.

## HUD and Camera Manager

The {py:class}`.HUD` {py:class}`.HUD` is a modification of the HUD used in the [manual_control RSS example of Carla](https://github.com/carla-simulator/carla/blob/master/PythonAPI/examples/rss/manual_control_rss.py){.external-icon}.

It closely combines with the [](#classes.camera_manager.CameraManager) to provide the visual human interface for the pygame window.

## Rules

See the [Rule documentation](../docs/Rules) for details.

## RssSensor and Visualization

 See the [RSS documentation](https://carla.readthedocs.io/en/latest/adv_rss/){.external-icon} from CARLA.

## KeyboardControls

See [`RSSKeyboardControl` API](#classes.keyboard_controls.RSSKeyboardControl) for a more details.

## Constants and Enums

See contents of the {py:mod}`classes.constants` module.

## carla_originals

This package contains (mostly) unmodified classes extracted from [examples provided by CARLA](https://github.com/carla-simulator/carla/tree/dev/PythonAPI/examples){.external-icon}

## Driver, Vehicle, VehicleSpawner

These are classes that are deprecated or will be merged or are up to major changes.

## Rule Interpreter

This class allows for an alternative way to execute rules through different interfaces (python, yaml, xml, etc). It is not yet further integrated and documented.

## Exceptions Overview

- {py:class}`.AgentDoneException`
  Raised when there is no more waypoint in the queue to follow and no rule set a new destination.

- {py:class}`.ContinueLoopException`
    Raise when the `agent.run_step` of the agent should not be continued further.
    The agent then returns the current `ctx.control` to the caller of `run_step`.
- {py:class}`.UserInterruption`
    Terminate the `run_step` loop if user input is detected, for example `KeyboardInterrupt` or a pygame hotkey like <kbd>Esc</kbd>.
    This allows the scenario runner and leaderboard to exit gracefully.
- {py:class}`.UpdatedPathException`
  Should be raised when the path has been updated and the agent should replan.  
  `Phase.DONE | END`

  For more details see the {py:mod}`classes.exceptions` API documentation.
