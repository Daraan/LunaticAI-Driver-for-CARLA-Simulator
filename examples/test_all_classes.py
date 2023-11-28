import __allow_imports_from_root
from agents.lunatic_agent import LunaticAgent
from config.lunatic_behavior_settings import LunaticBehaviorSettings


behavior = LunaticBehaviorSettings()
options = behavior.get_options()
print(behavior.get_options(yaml=True))

print(options.speed.target_speed, options.speed.speed, options.speed.speed_limit)


assert behavior.speed.target_speed is behavior.target_speed
