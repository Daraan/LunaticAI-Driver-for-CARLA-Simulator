from pprint import pprint
import __allow_imports_from_root
import carla
from agents.lunatic_agent import LunaticAgent
from classes.constants import Phase

from classes.rule import Rule, ConditionFunction, Context, always_execute
from agents.tools.config_creation import LunaticAgentSettings, LunaticAgentSpeedSettings

arule = Rule(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, 
                                      condition=always_execute, 
                                      action=lambda ctx: print("Hello World"), 
                                      overwrite_settings= {"speed": {"intersection_speed_decrease": 10}},
                                      description="Set speed to intersection speed")

print(arule)

print(ConditionFunction("Testing this"))

named_wrapper = ConditionFunction("Testing this")


class AnotherRule(Rule):
    phases = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    
    @ConditionFunction("Always execute this condition")
    def condition(ctx):
        return True
    
    def action(ctx):
        print("Hello World")
    overwrite_settings = {"speed": {"intersection_speed_decrease": 10}}
    description = "Set speed to intersection speed"
    
@Rule
class AnotherRule2:
    """
    Note that @Rule creates an instance of class AnotherRule2(Rule)
    """
    phases = Phase.TURNING_AT_JUNCTION | Phase.BEGIN
    
    @ConditionFunction("Always execute this condition")
    def condition(ctx):
        return True
    
    def action(ctx):
        print("Hello World")
    overwrite_settings = {"speed": {"intersection_speed_decrease": 10}}
    description = "Rule class via the at"
    
    def myfuc(self):
        print("Hello World")
 
AnotherRule2.myfuc()
 

drule = Rule({"phase": Phase.TURNING_AT_JUNCTION | Phase.BEGIN,
      "condition": always_execute,
      "action": lambda ctx: print("Hello World"),
      "overwrite_settings": {"speed": {"intersection_speed_decrease": 10}},
      "description": "Rule created from dictionary"})

print(drule)

# Clone rule

crule = arule.clone()
crule2 = Rule(arule)

print("------\n\n", crule2,"\n", arule, "\n", crule)

behavior = LunaticAgentSettings()
options : LunaticAgentSettings
options : LunaticAgentSettings = behavior.make_config()
y = behavior.speed.to_yaml()
print(y)


import os
if "examples" in os.getcwd():
    root = "../"
else:
    root = "./"
    
behavior.export_options(root+"conf/lunatic_behavior_settings.yaml", resolve=False)
loaded = LunaticAgentSettings.from_yaml(root+"conf/lunatic_behavior_settings.yaml")

assert loaded == behavior

options.live_info.current_speed = 10
options.live_info.current_speed_limit = 35

from omegaconf import OmegaConf
print(OmegaConf.to_yaml(options, resolve=False))

print(options.speed.current_speed, options.live_info.current_speed)


assert options.speed.current_speed is options.live_info.current_speed
