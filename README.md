# LunaticAI Driver for CARLA-Simulator

<link rel="shortcut icon" type="image/png" href="https://github.githubassets.com/favicons/favicon.svg">

This repository offers a modularized rule-based agent system for the 
[CARLA simulator](https://carla.org/)[<img src="https://github.githubassets.com/favicons/favicon.svg" alt="drawing" width="14"/>](https://github.com/carla-simulator/carla)
designed to be easily extendable and configurable.
If you are familiar with the CARLA simulator, our agent builds up on the standard agents provided by the CARLA team but remodels and extends them in many ways.


## Work in Progress

### Most important Branches

| | | |
| -- | -- | -- |
|`main` | Supporting CARLA 0.9.14+, Python 3.7+ with/without RSS build | **Trying to keep it stable**|
|`dev/main` | Supporting CARLA 0.9.14+, Python 3.7+ with RSS build | potentially unstable |
|`dev/daniel`| Supporting CARLA 0.9.15+, Python 3.10+ with RSS build | potentially unstable |
|`WIP/dev_daniel` | Most recent development branch | likely unstable |

## Installation

XXX

## Agent Classes

At the core is the [`LunaticAgent`(./agents/lunatic_agent.py)](./agents/lunatic_agent.py) which offers full flexibility in terms of rules and actions and how you control it during a custom written game loop.

The [`LunaticChallenger`(./agents/leaderboard_agent.py)](./agents/leaderboard_agent.py) is a simplified version wrapped around the `LunaticAgent` to be compatible with the [carla/leaderboard-2.0](https://github.com/carla-simulator/leaderboard) interface, i.e. providing only a `setup` and `run_step` method.

## Rule and Phase System

### Rules

Rules for the agent can be designed in a class-based way. For example the following rule will slow down the agent when it is at a junction:

```python
class SlowDownAtIntersectionRule(Rule):
    """
    Slow down the agent when it is at a junction.
    """
    phase = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    @EvaluationFunction
    def rule(self, ctx: Context) -> Hashable:
        return ctx.agent.is_at_junction
    def action(self, ctx: Context):
        ctx.agent.set_target_speed(agent.live_info.target_speed - 10)
```

For more details look into the [Rules](./agents/rules/Rules.md) documentation.

### Phases

The agent system is based on a phase system, which allows to define rules for specific situations.
To see which phases are available and how they are defined, see the `Phase` class in [constants.py](./classes/constants.py#Phase).

At the beginning (`Phase.BEGIN`) and end (`Phase.END`) of a phase associated rules are evaluated and depending on their outcome the agent will perform certain actions.

## Configuration

Behavioral aspects of the agent but also the environment and user interface are configured via YAML files.
[Hydra](https://hydra.cc/) [<img src="https://github.githubassets.com/favicons/favicon.svg" alt="drawing" width="14"/>](https://github.com/facebookresearch/hydra) is used to manage the configuration files and to provide a clean way to access and manage the configuration in a flexible way.

The configuration backend is designed to make coarse and fine-grained changes by using combination of different configs on demand or by adjusting single parameters or blocks via the command line.
The configuration files are stored in the [conf](./conf) directory.

For more info see XXX

## Workflow and Component Diagram of the Agent System

!["Visualization of the agents components and its workflow"](./docs/AgentLifecycleDiagram.drawio.svg)
