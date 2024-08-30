"""These are rules for testing and debugging"""

from typing import TYPE_CHECKING, Optional
from typing_extensions import Self
from agents.rules.behaviour_templates import *  # noqa
from classes.constants import Phase
from classes.rule import Context, Rule


from typing_extensions import Callable, assert_type

x = ConfigBasedRSSUpdates()
assert x.description == ConfigBasedRSSUpdates.__doc__
if x.description != "Always accept RSS updates if :any:`rss.always_accept_update <LunaticAgentSettings.rss>` is set to True in the config.":
    print("Warning: Description not set correctly")

test = AlwaysAcceptRSSUpdates()

# Check static type hints
class_like = ConditionFunction(truthy=True) # this is actually a partial[type[ConditionFunction]]
assert issubclass(class_like.func, ConditionFunction)  # type: ignore
inst = ConditionFunction(int) # type: ignore # just test
assert isinstance(inst, ConditionFunction)


def _check_type(instance, cls):
    assert isinstance(instance, cls)
    return instance

def context_method(self, ctx : "Context") -> bool:
    assert isinstance(self, Rule)
    assert isinstance(ctx, Context)
    return True

def context_function(ctx : "Context") -> bool:
    assert isinstance(ctx, Context)
    return True

@ConditionFunction
def eval_context_method(self: Rule, ctx : "Context") -> int:
    assert isinstance(self, Rule)
    assert isinstance(ctx, Context)
    return 2

@ConditionFunction
def eval_context_function(ctx : "Context") -> int:
    assert isinstance(ctx, Context)
    return 1

def ctx_action(ctx : Context):
    _check_type(ctx, Context)
    
def ctx_self_action(self, ctx : Context):
    _check_type(self, Rule)
    _check_type(ctx, Context)

def ctx_action_kwargs(ctx : Context, arg1):
    assert arg1 == "arg1", f"Expected arg1 but got {arg1}"
    _check_type(ctx, Context)
    
def ctx_self_action_kwargs(self, ctx : Context, arg1):
    _check_type(self, Rule)
    assert arg1 == "arg1", f"Expected arg1 but got {arg1}"
    _check_type(ctx, Context)

@Rule
class SimpleRule1:
    phase = Phase.UPDATE_INFORMATION | Phase.BEGIN
    condition = context_function
    action = lambda ctx: _check_type(ctx, Context)  # noqa: E731
    description = "Simple Rule 1"


class SimpleRule(Rule):
    phases = Phase.UPDATE_INFORMATION | Phase.BEGIN # type: ignore[assignment]
    condition = context_method
    action = lambda self, ctx: ctx_self_action(self, ctx)  # noqa: E731

class ReverseWhenCollide(Rule):
    phases = {Phase.COLLISION | Phase.END}    # type: ignore[assignment]
    condition = context_method
    
    @staticmethod
    def action(ctx : Context):
        _check_type(ctx, Context)
        ctx.control.reverse = True   # type: ignore[arg-type]

@Rule
class SimpleRule1B:
    phases = Phase.UPDATE_INFORMATION | Phase.BEGIN
    condition = eval_context_function.copy() # TODO: can I copy this via a __set__
    condition.register_action(ctx_self_action_kwargs, arg1="arg1")
    
class SimpleRule2B(Rule):
    phase = Phase.UPDATE_INFORMATION | Phase.BEGIN
    condition = eval_context_function.copy() # TODO: can I copy this via a __set__
    condition.register_action(ctx_action_kwargs, use_self=False, arg1="arg1")

class SimpleRuleB(Rule):
    phases = Phase.UPDATE_INFORMATION | Phase.BEGIN # type: ignore[assignment]
    condition = eval_context_method.copy()
    condition.register_action(ctx_action)


class DebugRuleWithEval(Rule):
    phases = Phase.UPDATE_INFORMATION | Phase.BEGIN  # type: ignore[assignment]
    
    @ConditionFunction("AlwaysTrue")
    def condition(self, ctx : "Context") -> int:
        assert isinstance(ctx, Context)
        assert isinstance(self, DebugRuleWithEval)
        return 1
    
    if TYPE_CHECKING:
        assert_type(condition, ConditionFunction[[], int])
    
    @condition.register_action(True, arg1="arg1")
    def true_action(self, ctx: "Context", arg1:str) -> None:
        assert arg1 == "arg1", f"Expected arg1 but got {arg1}"
        assert isinstance(ctx, Context)
        assert isinstance(self, DebugRuleWithEval)
        return None
    
    if TYPE_CHECKING:
        assert_type(true_action, Callable[[Self, Context], None])
    
class DebugRuleWithEval2(Rule):
    phases = Phase.UPDATE_INFORMATION | Phase.BEGIN  # type: ignore[assignment]
    
    @ConditionFunction
    def condition(self, ctx : "Context") -> int:
        assert isinstance(ctx, Context)
        assert isinstance(self, DebugRuleWithEval)
        return 1
    
    if TYPE_CHECKING:
        assert_type(condition, ConditionFunction[[], int])
    
    deco = condition.register_action(True, arg1="arg1")
    @deco
    def true_action(self, ctx: "Context", arg1:str) -> float:
        assert arg1 == "arg1", f"Expected arg1 but got {arg1}"
        assert isinstance(ctx, Context)
        assert isinstance(self, DebugRuleWithEval)
        return 1.0
        
if TYPE_CHECKING:
    from typing import cast
    c = cast(Context, None)
    res_eval_context_func = eval_context_function(c)
    res_eval_context_method = eval_context_method(c)
    assert_type(res_eval_context_func, int)
    assert_type(res_eval_context_method, int)
    
    rule = DebugRuleWithEval2()
    result = rule.condition(c)
    assert_type(result, int)
    result2 = rule(c)
    a_result = rule.true_action(c)
    assert_type(a_result, float)
    rule.true_action(c)
    o_rule = cast(Rule, rule)
    assert_type(DebugRuleWithEval2.true_action(rule, c), float)

    
class Another(Rule):
    phase = Phase.UPDATE_INFORMATION | Phase.BEGIN
    
    condition = always_execute
    
    actions = {True: lambda self, ctx: (_check_type(self, Rule), _check_type(ctx, Context)),
            False: lambda ctx: _check_type(ctx, Context)}
    

a = Another()

class CustomInitRule(Rule):
    def __init__(self, phases:Optional[Phase]=None):
        # NOTE: The
        super().__init__(phases or Phase.UPDATE_INFORMATION | Phase.BEGIN, condition=always_execute, action=lambda ctx: _check_type(ctx, Context))
        self._custom = True
    
    phase = Phase.UPDATE_INFORMATION | Phase.BEGIN
    
    _cooldown = 0
    condition = lambda ctx: [][1] # This should not be executed, overwritten in the custom Init # noqa: E731
    
    actions = {True: lambda self, ctx: (_check_type(self, Rule), _check_type(ctx, Context)),
            False: lambda ctx: _check_type(ctx, Context)}
    
class RuleAttributes(Another):
    DEFAULT_COOLDOWN_RESET = 10
    start_cooldown = 20
    cooldown_reset_value = 50
    
test_init = RuleAttributes()

new_rule = DebugRuleWithEval()
#new_rule.action
simple_rule = SimpleRule()
simple_ruleB = SimpleRuleB(Phase.UPDATE_INFORMATION | Phase.BEGIN)
simple_rule2B = SimpleRule2B(Phase.UPDATE_INFORMATION | Phase.BEGIN)
another_rule = Another()

def _test_custom_init_Rule():
    """Suppress warning message when creating this invalid case"""
    from contextlib import redirect_stderr
    import io, sys, re  # noqa
    alt_out = io.StringIO()
    # suppress expected message
    
    with redirect_stderr(alt_out):
        custom_rule = CustomInitRule()
    
    alt_out.seek(0)
    content = alt_out.read()
    if f"Warning 'condition' argument passed but class {CustomInitRule.__name__}" not in content:
        print("ERROR: Expected warning message not found")
    else:
        content = re.sub(fr"Warning 'condition' argument passed but class {CustomInitRule.__name__}.+?"
                            "This might lead to undesired results.\n", "", content)
    if content:
        print(content, file=sys.stderr)
    assert custom_rule._custom
    return custom_rule

custom_rule = _test_custom_init_Rule()

# Check Doc -> Descritpion

class CheckDescription(Rule):
    """This is my description"""
    phase = Phase.BEGIN
    
assert CheckDescription.description == """This is my description"""
cd_rule = CheckDescription(Phase.END, # type: ignore[reportCallIssue]
                            action=lambda ctx: _check_type(ctx, Context),
                            condition=lambda self, ctx: (_check_type(self, Rule)))
#print(cd_rule.phases)
phase = list(cd_rule.phases).pop() # does not work with frozenset
cd_rule.phases = set() # type: ignore
#print(cd_rule.phases, cd_rule.phase)
assert phase == Phase.END, f"Expected {Phase.END} but got {phase}"
assert not cd_rule.phases
assert cd_rule.description == """This is my description"""


debug_rules: list[Rule] = [test, simple_rule, simple_ruleB, simple_rule2B, another_rule, custom_rule, new_rule, cd_rule]