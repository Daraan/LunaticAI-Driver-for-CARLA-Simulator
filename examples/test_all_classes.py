import __allow_imports_from_root
import carla
from agents.lunatic_agent import LunaticAgent
from classes.constants import Phase

from classes.rule import Rule, EvaluationFunction, Context, always_execute
from conf.agent_settings import LunaticAgentSettings

arule = Rule(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, 
                                      rule=always_execute, 
                                      action=lambda ctx: print("Hello World"), 
                                      overwrite_settings= {"speed": {"intersection_speed_decrease": 10}},
                                      description="Set speed to intersection speed")

print(arule)


behavior = LunaticAgentSettings()
options : LunaticAgentSettings
options : LunaticAgentSettings = behavior.get_options()
print(behavior.speed.to_yaml())

print(options.speed.target_speed, options.live_info)
behavior.speed.export_options("conf/lunatic_behavior_settings.yaml", resolve=False)

options.live_info.current_speed = 10
options.live_info.current_speed_limit = 35

from omegaconf import OmegaConf
print(OmegaConf.to_yaml(options, resolve=False))

print(behavior.speed.current_speed, behavior.live_info.current_speed)

print(OmegaConf.to_yaml(options, resolve=True))

assert behavior.speed.current_speed is behavior.live_info.current_speed
