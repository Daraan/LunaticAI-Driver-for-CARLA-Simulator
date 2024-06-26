# Agents

There are two different agent classes than can be used the [](#LunaticAgent) that is fully customizable,
and the simpler but less flexible [](#LunaticChallenger).

## Agent Classes

### LunaticChallenger Class

The [](#agents.leaderboard_agent.LunaticChallenger) is wrapped around the [`LunaticAgent`](#agents.lunatic_agent.LunaticAgent).
It can be more easily combined with the [ScenarioRunner](https://scenario-runner.readthedocs.io/en/latest/) and be used with the [Leaderboard 2.0](https://leaderboard.carla.org/get_started/) for which this class is especially designed.

In the simplest way an agent can be used like this:

```python

from agents.leaderboard_agent import LunaticChallenger

# ... setup carla

# Create the ego vehicle, after you have chosen a blueprint for the ego vehicle
ego_bp.set_attribute('role_name', 'hero')
ego = world.spawn_actor(ego_bp, ego_transform)

agent = LunaticChallenger()
# Further setup the scenario in between

agent.setup() # Do not forget this step!

while True:
    control = agent.run_step()
    ego.apply_control(control)
```

### LunaticAgent Class

The [`LunaticAgent`](#agents.lunatic_agent.LunaticAgent) can be initialized in multiple ways

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

Alternatively it can be initialized quicker through the game framework, providing other useful instances at the same time.

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

The agent can be configures by passing any attribute supporting Mapping structure, e.g. nested [(data)classes](https://docs.python.org/3/library/dataclasses.html), [attrs](https://www.attrs.org/en/stable/index.html), or [omegaconf's DictConfig](https://omegaconf.readthedocs.io/en/2.3_branch/) which can extend on these two.

For more info read the [ConfigFiles.md](../conf/ConfigFiles) section.
