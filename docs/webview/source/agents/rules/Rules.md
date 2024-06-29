# Rules

Rules have three main components

- a condition
- an action
- a set of phases in which the condition should be evaluated.

There are three different ways to define a rule, with their own advantages and disadvantages.

## Phases

To see which phases are available and how they are defined, see the `Phase` class in [classes/constants.py](#classes.constants.Phase).

At the beginning (`Phase.BEGIN`) and end (`Phase.END`) of a phase associated rules are evaluated and depending on their outcome the agent will perform certain actions.

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

## condition & ConditionFunction

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

## Registering actions

There are multiple ways how actions can be defined to be executed when the condition is fullfilled.
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

To use more than two actions depending on the return value of the condition function, the `actions` dict for a rule can be used.
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

Using the `ConditionFunction.register_action` method allows to bind actions to a condition function.

Warning:
    When passing a condition with registered actions the rule omits the `action(s)` parameter.

Todo:
    Could merge both dicts, but in which order?

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

def action(ctx: Context):
    ...

foo.register_action(action, True)
```

## Adding Rules to an Agent

A single rule can be added by calling `agent.add_rule(rule)` or multiple rules by calling `agent.add_rules(rules)`.

For example:

```python
rules = [Rule1(), Rule2(), Rule3()]
agent.add_rules(rules)
```

## Troubleshooting

### IndexError: tuple index out of range

This error will be less ambiguous in future python versions and turns into a TypeError.
In short the function requires at least one positional argument, but none was provided, for example only trough keyword arguments.

```py
  File "/home/dsperber/miniconda3/envs/python3.10/lib/python3.10/functools.py", line 925, in _method
    method = self.dispatcher.dispatch(args[0].__class__)
IndexError: tuple index out of range
```

Likely the problem is that a `Rule` was instantiated without a positional `phase(s)` argument, e.g. `Rule(phases=Phase.NONE)`.
To fix it use `Rule(Phase.NONE)`.

### TypeError(f'{funcname} requires at least 1 positional argument')

see IndexError above.

---

## TODOs

- Implement a Rule.reset functionality, when the rule persists over multiple independent scenarios.
