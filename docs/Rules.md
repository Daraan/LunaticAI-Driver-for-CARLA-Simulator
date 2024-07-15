# Rules

Rules have three main components

- a condition
- an action
- a set of phases in which the condition should be evaluated.

There are three different ways to define a rule, with their own advantages and disadvantages.

## Phases

The [](#classes.constants.Phase) enumeration defines different stages and states that the agent transitions through during its [operational cycle](/index.rst#readme-workflow).
Each phase is represented as a flag allowing combinations.
Foremost is each `Phase` of the workflow combined with of of the two flags [](#Phase.BEGIN) or [](#Phase.END).

```{seealso}
To see which phases are available and how they are defined, see the [](#Phase) class in [classes/constants.py](#classes.constants.Phase).
```

![Image of phase logic](/docs/images/PhaseSystem.drawio.svg)

When a phase is executed ([](#LunaticAgent.execute_phase)), the agent will evaluate the rules associated with this phase and execute the actions of the rules that have a fulfilled condition.
Phases are therefore a necessary part for [`Rule` creation](#creation) an need to be [registered](#adding-rules-to-an-agent) with the agent.

In the default case the order of execution is `Phase.BEGIN | Phase.SOME_PHASE`, followed by the agent's function of this phase, and lastly `Phase.END | Phase.SOME_PHASE`.
However, there are some exceptions to this order like the [](#emergency-phase), phases that are handled by the user, or `Phase.END | Phase.DETECT_CARS` which is only executed when no car is detected.

```{attention}
- Currently phases are checked for a correct match. 
- Only pair wise flag combinations with [](#Phase.BEGIN) or [](#Phase.END) are used in the normal workflow.
```

```{tip}
The [](#context-object) stores the results in [](#Context.phase_results), which is a dictionary with the keys set to the various phases.
By default all values are set to [](#Context.PHASE_NOT_EXECUTED).
```

### Emergency Phase

If the agent detects an emergency, i.e. a pedestrian in front of it. The agent will execute the phase `Phase.BEGIN | Phase.EMERGENCY`. If during this phase not all elements of the set [](#LunaticAgent.detected_hazards) are cleared by rules an [](#EmergencyStopException) is raised.

In general, if an `EmergencyStopException` is raised, which can also be done by [rule actions](#XXX), the [](#LunaticAgent.emergency_manager) will calculate a response and afterwards executes `Phase.EMERGENCY | Phase.END`.

```{note}
- The check if [](#LunaticAgent.detected_hazards) is empty is done during the workflow of the agent and not tied to the execution of the `Phase.BEGIN | Phase.EMERGENCY` itself.

- Currently the `emergency_manager` applies a full stop in all situations. Handling situations differently must be done by user-implemented rules.
```

## Creation

### Functional API

With the functional API the rule object will be instantiated from the rule class.
**While `condition` and `action` are able** to access the `self` object, providing additional attributes they have to be written outside from the class.

```python
slow_down_rule = Rule(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, 
                        condition=lambda ctx: True, 
                        action=...
                        overwrite_settings= {"speed": {"intersection_speed_decrease": 10}},
                        description="Set speed to intersection speed")
```

### Class API

The class API allows to define rules and actions in the class body.
When defining a function with `self` and the required `ctx` argument you can make use of instance attributes.
In the end the class must still be instantiated to be used (TODO: do that automatically).

```python
class SlowDownAtIntersectionRule(Rule):
    """
    This will be the description
    """
    phases = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    # condition and action can be defined as functions (only the Context argument)
    # or as methods (self and Context argument)
    @ConditionFunction
    def condition(ctx: Context) -> bool:
        return True
    def action(self, ctx: Context):
        ...
    overwrite_settings = {"speed": {"intersection_speed_decrease": 10}}

slow_down_rule = SlowDownAtIntersectionRule()
```

### Decorator API

The decorator API automatically instantiates the rule class from the class body, with all the advantages of the class API.
Be aware that these rules should be tied to a **single agent** only.

```python
@Rule # This creates an instance
class slow_down_rule:
    """
    Slow down the car when turning at a junction.
    """
    phases = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    condition = always_execute
    action = set_default_intersection_speed
    overwrite_settings = {"speed": {"intersection_speed_decrease": 10}}
    description = "Set speed to intersection speed"
```

### Duplicating a Rule

Rules can be duplicated by calling the `new_rule = old_rule.clone()` method on the rule object.
Similarly, `new_rule = Rule(old_rule)` is also valid, which allows to copy attributes to a different class should this be necessary.

## condition functions & ConditionFunction

The passed `condition` can be simple functions with a signature of `(Context) -> Hashable` or `(self: Rule, Context) -> Hashable`,
if two or more arguments are detected the `self` argument for the Rule instance will be provided.

The `ConditionFunction` extends a simple function with additional utility, it can be used in the following ways:

### As decorator

```python

# Plain
@ConditionFunction
def foo(...):
    ...

# Provide a name for the function
@ConditionFunction("This function always returns True")
def foo(...):
    ...

# Keyword only arguments
@ConditionFunction(truthy=True, use_self=False)
def evaluate_this(ctx: Context, value=None) -> bool:
    # In the background this will be converted to bool(value)
    return value 
```

### Functional

The functional approach has the advantage that a function can be used in different ConditionFunctions.
This is especially useful if actions are tied to conditions through `ConditionFunction.register_action`

```python
def bar(self, ctx: Context):
    ...

eval_bar1 = ConditionFunction(bar)
eval_bar2 = ConditionFunction(bar)
```

## Registering Actions

There are multiple ways how actions can be defined to be executed when a condition is fulfilled.
In general a rule can execute multiple actions, depending on the returned value of the condition function.
By default the action is only executed if the condition returns `True` and does not be specified specially.

### Functional & Class API

#### True / False

```python
true_false_rule = Rule(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, 
                        condition=lambda ctx: choice([True, False])
                        action=true_action,
                        false_action=false_action)

class TrueFalseRule(Rule):
    phases = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    condition = lambda ctx: choice([True, False])
    def action(self, ctx: Context): # NOTE: This function NEEDS to be called "action"
        ...
    false_action = false_action # NOTE: This attribute needs to be called "false_action"
```

#### Any Return Type

To use more than two actions depending on the return value of the condition function, the `actions` dict for a condition can be used.
The definition of for the functional API also uses the `actions` parameter.

```python
class AnyReturnRule(Rule):
    phases = Phase.NONE
    condition = lambda ctx: choice([True, False, "foo"])
    actions = {
        True: true_action,
        False: false_action,
        "foo": foo_action
    }
```

### ConditionFunction.register_action

Using the `ConditionFunction.register_action` method allows to bind actions to a condition function,
when creating a `Rule` the `action(s)` parameter is then omitted.

```python
class TrueFalseRule(Rule):
    phases = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    @ConditionFunction
    def condition(ctx: Context) -> bool: # NOTE: That the function must still be called condition
        return choice([True, False, "foo"])
    
    # These two are equivalent, use only one of them
    @condition.register_action
    @condition.register_action(True)
    def true_action(self, ctx: Context):
        ...

    @condition.register_action(False)
    def false_action(self, ctx: Context):
        ...

    @condition.register_action("foo")
    def foo_action(self, ctx: Context):
        ...
```

`register_action` can also be used directly

```python

@ConditionFunction
def foo(ctx: Context):
    ...

def action(ctx: Context, value=True):
    ...

foo.register_action(action, use_self=False)
foo2 = foo.copy()
foo2.register_action(action, use_self=False, value=False)
```

## Adding Rules to an Agent

A single rule can be added by calling `agent.add_rule(rule)` or multiple rules by calling `agent.add_rules(rules)`.

For example:

```python
rules = [Rule1(), Rule2(), Rule3()]
agent.add_rules(rules)
```

## Context Object

A tick-constant [](#Context) object gives access to all information from the agent, the current tick, and rule that currently executed. The [](#LunaticAgent.ctx) object is passed as `ctx` argument to all rule conditions and actions.
It holds a *temporary* [`config`](#Context.config) which is the one used to calculate the controls of this tick, similarly the [](#Context.control) object holds the vehicle's *final* control command that should be executed in the end when [](#LunaticAgent.apply_control) is called.

The key attributes of the [](#Context) object are:

- [`ctx.agent`](#Context.agent) : Backreference to the agent.
- [`ctx.config`](#Context.config) : Merge of the agents config and a rule's `overwrite_settings`; if a rules action is executed, the `overwrite_settings` are merged into the context's config for the rest of the step. The config is backed by the [](#ContextConfig) schema.
- [`ctx.detected_hazards`](#Context.detected_hazards) : Quicker access to `agent.config.live_info`
- **[`ctx.control`](#Context.control) : Holds the vehicle's *final* control command** that should be executed in the end and **can be replaced**.
It is first set at the end of the [agent's inner step](#LunaticAgent._inner_step) Formally it is updated at the end of certain phases at the end or after the agent's inner step: [`agent.execute_phase(phase, control=new_control)`](#LunaticAgent.execute_phase).  
Check the [workflow diagram](/index.rst#readme-workflow) for the phases where this update is done.

:::{attention}

```{eval-rst}
|:exclamation:| Key points:\
```

- The [](#Context.config) is a **copy** of the agent's config **merged with the {py:attr}`overwrite_settings <.Rule.overwrite_settings>`** of the associated [Rule](#Class-API).
- During the {py:attr}`condition <Rule.condition>` evaluation these changes are temporary.
  If a rule's action is executed the {py:attr}`overwrite_settings <.Rule.overwrite_settings>` are merged into the [](#Context.config) for the rest of this tick. For permanent changes the agent's config needs to be adjusted separately.
- **The [](#Context.config) is the configuration used by the local planner to calculate the controls of this tick.**
- The `ctx.control` object is used when [`agent.apply_control()`](#LunaticAgent.apply_control) is used.
:::



## Troubleshooting

### IndexError: tuple index out of range

This error will be less ambiguous in future python versions and turns into a TypeError.
In short the function requires at least one positional argument, but none was provided, for example only trough keyword arguments.

```py
  File "/home/dsperber/miniconda3/envs/python3.10/lib/python3.10/functools.py", line 925, in _method
    method = self.dispatcher.dispatch(args[0].__class__)
IndexError: tuple index out of range
```

Likely the problem is that the condition was instantiated without a positional `phase(s)` argument, e.g. `Rule(phases=Phase.NONE)`.
To fix it use `Rule(Phase.NONE)`.

### TypeError(f'{funcname} requires at least 1 positional argument')

see IndexError above.

---

## Future Work

- Implement a Rule.reset functionality, when the rule persists over multiple independent scenarios.
