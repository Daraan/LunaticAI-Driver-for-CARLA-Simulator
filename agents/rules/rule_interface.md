# Rules

Rules have three main components

- a condition
- an action
- a set of phases in which the condition should be evaluated.

There are three different ways to define a rule, with their own advantages and disadvantages.

## Creation

### Functional API

With the functional API the rule object will be instantiated from the rule class.
**While `rule` and `action` are able** to access the `self` object, providing additional attributes they have to be written outside from the class.

```python
slow_down_rule = Rule(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, 
                        rule=lambda ctx: True, 
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
    # rule and action can be defined as functions (only the Context argument)
    # or as methods (self and Context argument)
    @EvaluationFunction
    def rule(ctx: Context) -> bool:
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
    rule = always_execute
    action = set_default_intersection_speed
    overwrite_settings = {"speed": {"intersection_speed_decrease": 10}}
    description = "Set speed to intersection speed"
```

### Duplicating a rule

Rules can be duplicated by calling the `new_rule = old_rule.clone()` method on the rule object.
Similarly, `new_rule = Rule(old_rule)` is also valid, which allows to copy attributes to a different class should this be necessary.

## rule functions & EvaluationFunction

The passed `rule` can be simple functions with a signature of `(Context) -> Hashable` or `(self: Rule, Context) -> Hashable`,
if two or more arguments are detected the `self` argument for the Rule instance will be provided.

The `EvaluationFunction` extends a simple function with additional utility, it can be used in the following ways:

### As decorator

```python

# Plain
@EvaluationFunction
def foo(...):
    ...

# Provide a name for the function
@EvaluationFunction("This function always returns True")
def foo(...):
    ...

# Keyword only arguments
@EvaluationFunction(truthy=True, use_self=False)
def evaluate_this(ctx: Context, value=None) -> bool:
    # In the background this will be converted to bool(value)
    return value 
```

### Functional

The functional approach has the advantage that a function can be used in different EvaluationFunctions.
This is especially useful if actions are tied to conditions through `EvaluationFunction.register_action`

```python
def bar(self, ctx: Context):
    ...

eval_bar1 = EvaluationFunction(bar)
eval_bar2 = EvaluationFunction(bar)
```

## Registering actions

There are multiple ways how actions can be defined to be executed when a rule is triggered.
In general a rule can execute multiple actions, depending on the returned value of the condition function.
By default the action is only executed if the condition returns `True` and does not be specified specially.

### Functional & Class API

#### True / False

```python
true_false_rule = Rule(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, 
                        rule=lambda ctx: choice([True, False])
                        action=true_action,
                        false_action=false_action)

class TrueFalseRule(Rule):
    phases = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    rule = lambda ctx: choice([True, False])
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
    rule = lambda ctx: choice([True, False, "foo"])
    actions = {
        True: true_action,
        False: false_action,
        "foo": foo_action
    }
```

### EvaluationFunction.register_action

Using the `EvaluationFunction.register_action` method allows to bind actions to a condition function,
when creating a rule the `action(s)` parameter is omitted.

```python
class TrueFalseRule(Rule):
    phases = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    @EvaluationFunction
    def rule(ctx: Context) -> bool: # NOTE: That the function must still be called rule
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

@EvaluationFunction
def foo(ctx: Context):
    ...

def action(ctx: Context):
    ...

foo.register_action(action, True)
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

Likely the problem is that a rule was instantiated without a positional `phase(s)` argument, e.g. `Rule(phases=Phase.NONE)`.
To fix it use `Rule(Phase.NONE)`.

### TypeError(f'{funcname} requires at least 1 positional argument')

see IndexError above.

---

## TODOs

- Implement a Rule.reset functionality, when the rule persists over multiple independent scenarios.
