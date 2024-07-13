import re

def exclude_cdp():

    exclude_cdp = "\"'cleanup', 'create_blueprint', 'find_weather_presets', 'generate_spawn_points', 'get_actor_by_id', 'get_actor_by_name', 'get_local_planner', 'get_osc_global_param_value', 'get_random_seed', 'get_traffic_manager_port', 'handle_actor_batch', 'is_runtime_init_mode', 'is_sync_mode', 'on_carla_tick', 'prepare_map', 'register_actor', 'register_actors', 'remove_actor_by_id', 'remove_actors_in_surrounding', 'request_new_actor', 'request_new_actors', 'request_new_batch_actors', 'reset_lights', 'set_client', 'set_ego_route', 'set_latest_scenario', 'set_local_planner', 'set_runtime_init_mode', 'set_traffic_manager_port', 'set_world', 'spawn_actor', 'update_light_states', 'update_osc_global_params', 'world'\"".replace("'", "") #pylint: disable=line-too-long
    
    with open("classes.rst", "r+") as f:
        content = f.read()
        start = content.find(".. automodule:: classes.rule\n")
        end = content.find("----", start)
        subcontent = content[start:end]
        if exclude_cdp in subcontent:
            return
        # Do not write double online
        if not ":exclude-members:" in subcontent:
            subcontent = re.sub(".. automodule:: classes.rule\n", ".. automodule:: classes.rule\n   :exclude-members: " + exclude_cdp + "\n", subcontent)
        else:
            subcontent = re.sub(r':exclude-members:"', ':exclude-members: ' + exclude_cdp + ", ", subcontent)
        
        content = content[:start] + subcontent + content[end:]

        f.seek(0)
        f.write(content)
        
def patch_rule():
    with open("classes.rst", "r+") as f:
        content = f.read()
        start = content.find(".. automodule:: classes.rule\n")
        end = content.find("----", start)
        
        subcontent = content[start:end]
        
        exclude = "CooldownFramework, NOT_APPLICABLE, NO_RESULT, clone, set_cooldown_of_group, unblock_all_rules, update_all_cooldowns"
        
        insert =f"""
        
        .. autoclass:: BlockingRule
           :members:
           :exclude-members: {exclude}
           :undoc-members:
           :show-inheritance:
           :special-members: __call__
        
        .. autoclass:: MultiRule
           :members:
           :exclude-members: {exclude}
           :undoc-members:
           :show-inheritance:
           :special-members: __call__
           
        .. autoclass:: RandomRule
           :members:
           :exclude-members: {exclude}
           :undoc-members:
           :show-inheritance:
           :special-members: __call__
        
        """
        
        from textwrap import dedent
        if ".. autoclass:: BlockingRule" in subcontent and f":exclude-members: {exclude}" in subcontent: # already applied
            return
        
        if ":exclude-members: \"" in subcontent:
            subcontent = re.sub(r':exclude-members: "', ':special-members: __call__\n   :exclude-members: ", MultiRule, RandomRule, BlockingRule, ', subcontent, count=1)
        else:
            assert ":exclude-members:" not in subcontent, "Double execution of patch_rule"
            subcontent = re.sub(".. automodule:: classes.rule\n", 
                                ':special-members: __call__\n   :exclude-members: ", MultiRule, RandomRule, BlockingRule"', subcontent)

        
        subcontent = re.sub(r":\n\n", ":" + dedent(insert), subcontent, count=1)
        
        content = content[:start] + subcontent + content[end:]

        f.seek(0)
        f.write(content)
            
        
def remove_inheritance():
    files = ['agents.rules.obstacles.rst',
                        'agents.rules.rst']
    
    for file in files:
        with open(file, "r") as f:
            content = f.read()
            if ":no-inherited-members:" in content:
                continue # for double execution on read the docs.
            content = re.sub(r":show-inheritance:", r"\n   ".join([":show-inheritance:",
                                                                        #":no-index:"
                                                                         ":no-inherited-members:"]),
                                                                content)
        # Shortening the content clear it
        with open(file, "w") as f:
            f.write(content)
            
    fine_files: dict[str, list[str]] = {"classes.rst" : ["classes.constants", "classes.exceptions"],
                                        "agents.tools.rst" : ["agents.tools.config_creation", "agents.tools.hints"],
                                  }
    
    for file, submodules in fine_files.items():
        with open(file, "r+") as f:
            content = f.read()
            for submodule in submodules:
                start = content.find(".. automodule:: "+submodule+"\n")
                end = content.find("----", start)
                subcontent = content[start:end]
                if ":no-inherited-members:" in subcontent:
                    continue
                subcontent = re.sub(r":show-inheritance:", r"\n   ".join([":show-inheritance:",
                                                                        #":no-index:"
                                                                         ":no-inherited-members:"]),
                                                                string=subcontent,
                                                                count=1)
                content = content[:start] + subcontent + content[end:]
            f.seek(0)
            f.write(content)

def _patch_agent(content):
    start = content.find(".. automodule:: agents.lunatic_agent\n")
    end = content.find("----", start)
    subcontent = content[start:end]
    if ":special_memebers:" in subcontent:
        return content
    subcontent = re.sub(r":members:", r"\n   ".join([":members:",
                                                                        ":special-members: __call__",
                                                                         ]),
                                                                string=subcontent,
                                                                count=1)
    return content[:start] + subcontent + content[end:]
    

def patch_challenger():
    with open("agents.rst", "r+") as f:
        content = f.read()
        content = _patch_agent(content)
        start = content.find(".. automodule:: agents.leaderboard_agent\n")
        end = content.find("----", start)
        subcontent = content[start:end]
        if ":no-inherited-members:" not in subcontent:
            subcontent = re.sub(r":show-inheritance:", r"\n   ".join([":show-inheritance:",
                                                                            #":no-index:"
                                                                            ":no-inherited-members:",
                                                                            ":inherited-members: AutonomousAgent",
                                                                            ]),
                                                                    string=subcontent,
                                                                    count=1)
            
            shown = "'set_global_plan', 'destroy', 'run_step', 'sensors', 'setup', '__init__', 'BASE_SETTINGS'".replace("'", "")
            excluded = "get_entry_point"
            subcontent = re.sub(r":members:", r"\n   ".join([":members:",#+shown,
                                                            #":no-index:"
                                                                ":exclude-members: " + excluded,
                                                                ":special-members: __call__",]),
                                                    string=subcontent,
                                                    count=1)
        
            content = content[:start] + subcontent + content[end:]
        f.seek(0)
        f.write(content)
        
def add_imported_members():
    module = {"classes" : ["CustomSensorInterface"]}
    for file, members in module.items():
        with open(file+".rst", "r+") as f:
            content = f.read()
            start = content.find(".. automodule:: "+file+"\n")
            end = content.find("----", start)
            if end == -1:
                subcontent = content[start:]
                pattern = "\n$"
                extra = "\n"
            else:
                subcontent = content[start:end]
                pattern = "\n\n"
                extra = "\n\n"
            subcontent = re.sub(pattern, extra+"   :imported-members: " + ", ".join(members) +extra, subcontent, count=1)
            content = content[:start] + subcontent + content[end:]
            f.seek(0)
            f.write(content)
            
#def make_canonical():
#    pass
    

def _no_value_constants():
    return
    try:
        import classes.constants, inspect, enum
        all_classes = [getattr(classes.constants, key) for key, cls in vars(classes.constants).items() if not key.startswith("_") and inspect.isclass(cls)]
        flags = [cls for cls in all_classes if issubclass(cls, (enum.Flag, enum.IntFlag, enum.Enum)) and cls.__module__ == classes.constants.__name__]
    except AttributeError as e:
        # likely incompatible python version
        print(e)
        return
    
    with open("classes.rst", "r+") as f:
        content = f.read()
        start = content.find(".. automodule:: classes.constants\n")
        end = content.find("----", start)
        subcontent = content[start:end]
        
        if "no-value" in subcontent:
            return
        
        subcontent = re.sub(r":members:", r"\n   ".join([":members:",
                                                        ":no-value:"]),
                                                string=subcontent,
                                                count=1)
        
        '''
        if "exclude-members" in subcontent:
            return
        exclude = [cls.__name__ for cls in flags] 
        subcontent = re.sub(r":members:", r"\n   ".join([":members:",
                                                        ":exclude-members: " + ", ".join(exclude)]),
                                                string=subcontent,
                                                count=1)
        
        template = """
        .. autoclass:: {}
            :members:
            :undoc-members:
            :show-inheritance:
            :no-value:
        """
        
        autoclasses = [template.format(cls.__name__) for cls in flags]
        
        from textwrap import dedent
        subcontent = subcontent.replace(":\n\n", ":\n\n" + dedent("\n".join(autoclasses)) + "\n\n")
        '''
        content = content[:start] + subcontent + content[end:]
        f.seek(0)
        f.write(content)