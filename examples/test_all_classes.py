import __allow_imports_from_root
from agents.lunatic_agent import LunaticAgent
from config.lunatic_behavior_settings import LunaticBehaviorSettings


behavior = LunaticBehaviorSettings()
options = behavior.get_options()
print(behavior.get_options(yaml=True))

print(options.speed.target_speed, options.speed.current_speed, options.live_info.speed_limit)

assert behavior.speed.current_speed is behavior.live_info.speed
