import __allow_imports_from_root
import carla
from agents.lunatic_agent import LunaticAgent
from agents.tools.lunatic_agent_tools import Phase
from config.lunatic_behavior_settings import LunaticBehaviorSettings
from classes.rule import Rule, EvaluationFunction, Context, always_execute

arule = Rule(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, 
                                      rule=always_execute, 
                                      action=lambda ctx: print("Hello World"), 
                                      overwrite_settings= {"speed": {"intersection_speed_decrease": 10}},
                                      description="Set speed to intersection speed")

print(arule)
arule(carla.Vehicle())


behavior = LunaticBehaviorSettings()
options = behavior.get_options()
print(behavior.get_options(yaml=True))

print(options.speed.target_speed, options.speed.current_speed, options.live_info.current_speed_limit)
behavior.export_options("config/lunatic_behavior_settings.yaml")

options.live_info.current_speed = 10
options.live_info.current_speed_limit = 35

from omegaconf import OmegaConf
print(OmegaConf.to_yaml(options, resolve=False))

print(behavior.speed.current_speed, behavior.live_info.current_speed)

print(OmegaConf.to_yaml(options, resolve=True))

assert behavior.speed.current_speed is behavior.live_info.current_speed
