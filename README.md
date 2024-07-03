# LunaticAI Driver for CARLA-Simulator

[![Documentation Status](https://readthedocs.org/projects/lunaticai-driver-for-carla-simulator/badge/?version=latest)](https://lunaticai-driver-for-carla-simulator.readthedocs.io/?badge=latest)

The full documentation can be found online at [ReadTheDocs](https://lunaticai-driver-for-carla-simulator.readthedocs.io/).

---

This repository offers a modularized rule-based agent system for the
[CARLA simulator](https://carla.org/)[<img src="https://github.githubassets.com/favicons/favicon.svg" alt="drawing" width="14"/>](https://github.com/carla-simulator/carla)
designed to be easily extendable and configurable. Special submodules like the rule system, the configuration system and the information gathering can directly or with slight modifications be used in other projects as stand alone.

If you are familiar with the CARLA simulator, our agent builds up on the standard agents provided by the CARLA developers, but remodels and extends them in many ways. The key changes are:

- Full, dynamic and transparent Configuration, backed by [Hydra<img src="https://github.githubassets.com/favicons/favicon.svg" alt="drawing" width="14"/>](https://hydra.cc/):
  - Adjust the agent's behavior at runtime.
  - Automatically logged and repeatable experiments.
  - Hierarchically structured configuration allow for coarse and fine-grained changes to configure experiments
  - Backed by schemas that can be optionally enforced for validation and statically provide type-hints and autocompletion.
- Rule System: Customizing the agent's behavior by defining rules and actions.
- Efficient reuse of existing information

## Most important Branches

| branch | Supporting | notes |
| -- | -- | -- |
|`main` | CARLA 0.9.14+, Python 3.7+ with/without RSS build | **Trying to keep it stable** |
|`dev/main` | CARLA 0.9.14, Python 3.7+ without RSS build.<br> CARLA 0.9.15 Python 3.10 with RSS build | potentially unstable |
|`dev/daniel`| Supporting CARLA 0.9.15+, Python 3.10+ with RSS build | potentially unstable |
|`WIP/dev_daniel` | Most recent development branch | likely unstable |

Note: The [Leaderboard 2.0](https://github.com/carla-simulator/leaderboard) supporting `LunaticChallenger`, only supports CARLA 0.9.15 and Python 3.10+.

## Installation

See the [Installation Guide](docs/Install.md) for more details.

## Agent Classes

At the core is the [`LunaticAgent`(agents/lunatic_agent.py)](https://github.com/Daraan/LunaticAI-Driver-for-CARLA-Simulator/blob/main/agents/lunatic_agent.py) which offers full flexibility in terms of rules and actions and how you control it during a custom written game loop.

The [`LunaticChallenger`(agents/leaderboard_agent.py)](https://github.com/Daraan/LunaticAI-Driver-for-CARLA-Simulator/blob/main//agents/leaderboard_agent.py) is a simplified version wrapped version to be compatible with the [carla/leaderboard-2.0](https://github.com/carla-simulator/leaderboard) interface, i.e. providing only a `setup` and `run_step` method.

You can look at the workflow diagram at the end of this document to see how the agent system is structured.

## Rule and Phase System

### Rules

Rules for the agent have three core components: a phase where it can be applied, a condition and lastly an action that is executed depending on the result of the condition.  

For example, the following rule will slow down the agent when it is at a junction:

```python
class SlowDownAtIntersectionRule(Rule):
    """
    Slow down the agent when it is at a junction.
    """
    phase = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    @ConditionFunction
    def condition(self, ctx: Context) -> Hashable:
        return ctx.agent.is_at_junction
    def action(self, ctx: Context):
        ctx.agent.set_target_speed(agent.live_info.target_speed - 10)
```

For more details look into the [Rules](https://github.com/Daraan/LunaticAI-Driver-for-CARLA-Simulator/blob/main/agents/rules/Rules.md) documentation.

### Phases

The agent system is based on a phase system, which allows to define rules for specific situations.
To see which phases are available and how they are defined, see the `Phase` class in [constants.py](https://github.com/Daraan/LunaticAI-Driver-for-CARLA-Simulator/blob/main/classes/constants.py#Phase).

At the beginning (`Phase.BEGIN`) and end (`Phase.END`) of a phase associated rules are evaluated and depending on their outcome the agent will perform certain actions.

## Configuration

Behavioral aspects of the agent but also the environment and user interface are configured via YAML files.
[Hydra](https://hydra.cc/) [<img src="https://github.githubassets.com/favicons/favicon.svg" alt="drawing" width="14"/>](https://github.com/facebookresearch/hydra) is used to manage the configuration files and to provide a clean way to access and manage the configuration in a flexible way.

The configuration backend is designed to make coarse and fine-grained changes by using combination of different configs on demand or by adjusting single parameters or blocks via the command line.
The configuration files are stored in the [conf](https://github.com/Daraan/LunaticAI-Driver-for-CARLA-Simulator/blob/main/conf) directory.

For more info continue read the [Configuration](conf/ConfigFiles.md) section.

## Workflow and Component Diagram of the Agent System

!["Visualization of the agents components and its workflow"](docs/images/AgentLifecycleDiagram.drawio.svg)
