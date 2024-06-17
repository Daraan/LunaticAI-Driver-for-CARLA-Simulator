# Agents

There are two different agent classes than can be used the `LunaticAgent` that is fully customizable,
and the simpler but less flexible `LunaticChallenger`.

## Agent Classes

### LunaticChallenger

The `LunaticChallenger` is wrapped around the `LunaticAgent` it can be more easily combined with the [scenario_runner](https://github.com/carla-simulator/scenario_runner) or be used with the [leaderboard-2.0](https://leaderboard.carla.org/get_started/) for which this class is especially designed.

In the simplest way an agent can be used like this:

```python

from agents.leaderboard_agent import LunaticChallenger

# Create the ego vehicle
ego_bp.set_attribute('role_name', 'hero')
ego = world.spawn_actor(ego_bp, ego_transform)

agent = LunaticChallenger()
# Further setup the scenario in between

agent.setup() # Do not forget this step!

while True:
    control = agent.run_step()
    ego.apply_control(control)
```

### LunaticAgent

XXX

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
