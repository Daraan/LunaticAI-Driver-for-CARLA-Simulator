# Agents

```{eval-rst}
.. Note this is a MyST Markdown file to be used with Sphinx and will not render completely on GitHub. Build the documentation or refer to the online documentation at Read The Docs.
```

There are two different agent classes than can be used the {py:class}`agents.lunatic_agent.LunaticAgent` that is fully customizable,
and the simpler but less flexible {py:class}`agents.leaderboard_agent.LunaticChallenger`.

## Agent Classes

### LunaticChallenger Class

The {py:class}`.LunaticChallenger` is wrapped around the {py:class}`.LunaticAgent`.
It can be more easily combined with the [ScenarioRunner](https://scenario-runner.readthedocs.io/en/latest/) and be used with the [Leaderboard 2.0](https://leaderboard.carla.org/get_started/) for which this class is especially designed.

In the simplest way an agent can be used like in the snipplet below. However we recommend that you follow the documentation from the [installation](/docs/Install) section and [Leaderboard 2.0](https://leaderboard.carla.org/get_started/), afterwards you can test this agent by executing the `run_leaderboard_agent.sh` file.

```python
# examples/minimal_leaderboard.py
from agents.leaderboard_agent import LunaticChallenger
from classes.worldmodel import GameFramework

# Sets up Carla and Pygame, and Hydra in a minimal way
game_framework = GameFramework.quickstart()
ego = GameFramework.request_new_actor("car", rolename="hero", random_location=True)

# Create a lunatic agent
agent = LunaticChallenger("localhost", carla_port=2000)
agent.setup(game_framework.launch_config) # Do not forget this step!
try:
    while game_framework.continue_loop:
        with game_framework(agent):
            agent() # The LunaticChallenger should be called
            agent.apply_control()
except:
    game_framework.cleanup()
    raise
```

:::{attention}

```{eval-rst}
|:warning:|
```

 The `LunaticChallenger` is easier to setup, however its usage and customization are, limited as it complies with the `AutonomousAgent` interface from [`leaderboard-2.0`](https://leaderboard.carla.org/get_started/). So far, it only supports a limited amount of features mentioned in the [Configuration](conf/ConfigFiles.md#command-line) section. For example, changing settings over the command line is not supported as the configuration is loaded in `agent.setup` rather than a `@hydra.main` wrapped entry point.
:::

### LunaticAgent Class

The [](#agents.lunatic_agent.LunaticAgent) can be initialized in multiple ways and supports all features from the [Configuration](conf/ConfigFiles.md#configuration) section:

```python
from agents.lunatic_agent import LunaticAgent
from classes.worldmodel import GameFramework,

# ... setup carla

ego_bp.set_attribute('role_name', 'hero') # again choose a blueprint

ego = game_framework.spawn_actor(ego_bp, start, must_spawn=True)
# This creates the agent as well as other instances, from a custom configuration
behavior = LunaticAgentSettings(config.agent)
agent = LunaticAgent(behavior, vehicle=ego)

# The game framework allows to handle the loop and manages the cooldowns of all rules
game_framework = GameFramework(config)
# Certain internal events allow to stop the loop that is managed by the game_framework
while game_framework.continue_loop:
    with game_framework:
        agent.run_step()
```

The agent can be initialized quicker and directly with the {py:class}`.GameFramework`, which also provides other useful instances at the same time.

```python
agent, world_model, global_planner, keyboard_controller = game_framework.init_agent_and_interface(ego, agent_class=LunaticAgent, config=behavior)
```

## Adding Rules

Once an agent is created, it can be further customized by adding rules. Rules are the building blocks of the agent, they are the components that define the behavior of the agent. The rules can be added and removed or disabled at any time.

```python
# Adding mutliple rules
from agent.rules import create_default_rules
agent.add_rules(create_default_rules())

# Add a new rule
agent.add_rule(MyRule()) # Be sure that you instantiate your rules.
```

## Configuring the Agent

The agent can be configured by passing it any attribute-supporting {term}`Mapping` structure, for example nested [(data)classes](https://docs.python.org/3/library/dataclasses.html), [attrs](https://www.attrs.org/en/stable/index.html), or [omegaconf's DictConfig](https://omegaconf.readthedocs.io/) which extends the aforementioned.

:::{seealso}
For more info read the [config files documentation](/conf/ConfigFiles.md).
:::

## Workflow

The agent lifecycle involves several stages from initialization to continuous operation. The following diagram illustrates the lifecycle and interactions within the Lunatic AI Driver, providing its operational workflow in detail.

[![AgentLifecycleDiagram.drawio](/docs/images/AgentLifecycleDiagram.drawio.svg)](/docs/images/AgentLifecycleDiagram.drawio.svg)
(click image for fullscreen)
