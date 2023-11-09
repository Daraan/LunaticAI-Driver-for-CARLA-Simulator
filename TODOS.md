# Major TODOs

**Notes:**

Useful vscode extension: [Todo-Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)

**Research:**

* [ ] Check **original Carla/PythonAPI/examples** for useful classes and functions.
    Check if they differ and merge into one class here
* [ ] config/original_behavior.py, look for TODOs and unclear parameters -> find usage & explain

**Agent:**

* [ ] add the other important functions from behavior_agent.py to our agent (e.g. all managers). Tag which other functions (from basic_agent) can be removed or should be adjusted.

* Implement [OmegaConf](https://omegaconf.readthedocs.io/en/2.3_branch/usage.html):
* [ ] **config/original_behavior.py :** Instead of creating a simple dict (`get_options`) use an attributed dict [OmegaConf](https://omegaconf.readthedocs.io/en/2.3_branch/usage.html)
  * [ ] Group attributes into useful sections (e.g. "speed", "distances" , ...), as sub-dicts or via OmegaConf, maybe via merge or adding a dict as (sub)attribute.
* [ ] agent's `__init__`: Instead of storing variables like `self._max_speed` use [OmegaConf](https://omegaconf.readthedocs.io/en/2.3_branch/usage.html) dict (i.e. treat the parameters) -> This allows easier getting and setting of values.  
  i.e. for all use something like `self.config.max_speed` instead of `self._max_speed`. Modify all usages accordingly and remove setting of parameters in the init. Check which attributes are parameters and which are variables (like self._look_ahead_steps) and note if those variables maybe have potential to be (slightly) modified by the AI

* Other:
* [ ] For a better focus on the AI/planning part make a simple base class with setters/getters and less used functions, e.g. get_local_planner (NOTE: we can get rid of many attributes/setters/getters by using OmegaConf, see below)

* [ ] for `emergency_stop` add *reasons*, e.g. traffic light, vehicle, other obstacle, ...; call with a appropriate reason in run_step
* [ ] Write basic game loop for our setup; check out the examples/automatic_control-ours.py for inspiration and necessities

**Misc:**

* [ ] Merge **classes/carla_originals/world** (check the World classes in other **PythonAPI/examples** in the original repo) and our **classes/carla_service**
  
  * [ ] Combine World/CarlaServices with **utils/arguments_parsing** functionality and extend with useful arguments
* [ ] Camera modes to agent's vehicle
  * [ ] for pygame setting
  * [ ] during UEngine views
* (late future) write README.md file for the project
* [ ] Check important TODOs in the code and add them here
