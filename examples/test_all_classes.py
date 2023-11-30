import __allow_imports_from_root
from agents.lunatic_agent import LunaticAgent
from config.lunatic_behavior_settings import LunaticBehaviorSettings


behavior = LunaticBehaviorSettings()
options = behavior.get_options()
print(behavior.get_options(yaml=True))

print(options.speed.target_speed, options.speed.current_speed, options.live_info.current_speed_limit)
behavior.export_options("config/lunatic_behavior_settings.yaml")


assert behavior.speed.current_speed is behavior.live_info.current_speed
