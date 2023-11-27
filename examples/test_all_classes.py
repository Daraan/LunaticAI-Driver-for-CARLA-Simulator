import __allow_imports_from_root
from agents.lunatic_agent import LunaticAgent
from config.lunatic_behavior_settings import LunaticBehaviorSettings


behavior = LunaticBehaviorSettings()
behavior.get_options()
print(behavior.get_options(yaml=True))