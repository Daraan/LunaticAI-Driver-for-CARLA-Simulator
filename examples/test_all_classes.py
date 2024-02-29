from pprint import pprint
import __allow_imports_from_root
import carla
from agents.lunatic_agent import LunaticAgent
from classes.constants import Phase

from classes.rule import Rule, EvaluationFunction, Context, always_execute
from conf.agent_settings import LunaticAgentSettings, LunaticAgentSpeedSettings

arule = Rule(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, 
                                      rule=always_execute, 
                                      action=lambda ctx: print("Hello World"), 
                                      overwrite_settings= {"speed": {"intersection_speed_decrease": 10}},
                                      description="Set speed to intersection speed")

print(arule)


behavior = LunaticAgentSettings()
options : LunaticAgentSettings
options : LunaticAgentSettings = behavior.get_options()
y = behavior.speed.to_yaml()
print(y)

behavior.export_options("../conf/lunatic_behavior_settings.yaml", resolve=False)
loaded = LunaticAgentSettings.from_yaml("../conf/lunatic_behavior_settings.yaml")

assert loaded == behavior

options.live_info.current_speed = 10
options.live_info.current_speed_limit = 35

from omegaconf import OmegaConf
print(OmegaConf.to_yaml(options, resolve=False))

print(options.speed.current_speed, options.live_info.current_speed)


assert options.speed.current_speed is options.live_info.current_speed
