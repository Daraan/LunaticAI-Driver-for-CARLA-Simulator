import re

def _get_contents(file):
    with open(file, "r") as f:
        return f.read()
    
def _get_subcontent(contents:str, pattern, end="----"):
    start = contents.find(pattern)
    end = contents.find(end, start)
    if end == -1:
       end = None
    return start, end, contents[start:end]

def port_install_md():
    with open("../../Install.md", "r") as f:
        contents = f.read()
        find = re.search(r"^>\s*\[!(\w+)\](?:\s*>\s*([^\n]*))*", contents, flags=re.MULTILINE)
        while find:
            s = slice(*find.span())
            subcontent = contents[s]
            note = find[1].lower()
            subcontent = re.sub(r">\s*(\[!(\w+)\]\s*)?", "", subcontent, flags=re.MULTILINE)
            contents = contents[:s.start] + "```{" + note + "}\n"+ subcontent + "\n```" +contents[s.stop:]
            find = re.search(r"^>\s*\[!(\w+)\](?:\s*>\s*([^\n]*))*", contents, flags=re.MULTILINE)
        
        # [`LunaticChallenger`](/agents/leaderboard_agent.py#LunaticChallenger) -> :py:class:`LunaticChallenger`
        contents = re.sub(r"\[`Lunatic(\w+)`\]\(\S+\)", r"{py:class}`.Lunatic\1`", contents)
        contents = contents.replace("[AgentGameLoop.py](/AgentGameLoop.py)", "{py:mod}`AgentGameLoop.py <AgentGameLoop>`")
        
    with open("docs/Install.md", "w") as f:
        f.write(contents)


def module_contents_at_top():
    files = ["classes.rst", ("agents.substep_managers.rst", True), "agents.rules.rst"]
    for file in files:
        if isinstance(file, tuple):
            file, remove_section = file
        else:
            remove_section = False
        with open(file, "r+") as f:
            contents = f.read()
            start = contents.find("Module contents\n")
            if start == -1:
                continue # should be already at top
            end = contents.find("Submodules\n", start)
            if end != -1: # already at top
                return
            end = None
            subcontent = contents[start:end] + "\n"

            start2 = contents.find("Submodules\n")
            contents = contents[:start2] + subcontent + contents[start2:start]
            if remove_section:
                contents = contents.replace("\nModule contents\n---------------\n", "")
            f.seek(0)
            f.write(contents)

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
    if ":special-members:" in subcontent:
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
                extra = "\n"
            members = list(filter(lambda member: member not in subcontent, members))
            if not members:
                continue
            subcontent = re.sub(pattern, extra+"   :imported-members: " + ", ".join(members) +extra+"\n", subcontent, count=1)
            content = content[:start] + subcontent + content[end:]
            f.seek(0)
            f.write(content)
            
#def make_canonical():
#    pass

def remove_init():
    module = {"classes" : ["classes.evaluation_function"]}
    for file, members in module.items():
        with open(file+".rst", "r+") as f:
            content = f.read()
            for member in members:
                start = content.find(".. automodule:: "+member+"\n")
                end = content.find("----", start)
                subcontent = content[start:end]
                if "__add__, __and__, __or__, __invert__" in subcontent:
                    continue
                subcontent = re.sub(r":members:", r"\n   ".join([":members:",
                                                                ":special-members: __add__, __and__, __or__, __invert__",
                                                                ]),
                                                        string=subcontent,
                                                        count=1)
                content = content[:start] + subcontent + content[end:]
            f.seek(0)
            f.write(content)


def insert_github_ref():
    with open("AgentGameLoop.rst", "r+") as f:
        contents = f.read()
        start, end, subcontent = _get_subcontent(contents, "===\n", end=".. automodule::")
        from textwrap import dedent
        inject = dedent("""
        .. include:: _include.md
            :parser: myst_parser.sphinx_
            :start-after: ## $$ AgentGameLoopHeader
            :end-before: ## $$
        """)
        if inject in contents:
            return
        
        contents = contents[:start+4] + inject + contents[start+4:]
        f.seek(0)
        f.write(contents)
        
def patch_config_creation():
    # Remove init
    with open("agents.tools.rst", "r+") as f:
        contents = f.read()
        start, end, subcontent = _get_subcontent(contents, ".. automodule:: agents.tools.config_creation\n")
        if "no-special-members" in subcontent:
            return
        subcontent = re.sub(r":members:", r"\n   ".join([":members:",
                                                        ":no-special-members:"]),
                                                string=subcontent,
                                                count=1)
        contents = contents[:start] + subcontent + contents[end:]
        f.seek(0)
        f.write(contents)
        
def remove_empty_modules():
    from textwrap import dedent
    no_modules = ["agents", "agents.tools", "data_gathering", "data_gathering.car_detection_matrix", "agents.rules.obstacles"]
    rgx = re.compile(dedent(
        r"""
        (Module contents
        ---------------
        |===\n)
        .. automodule:: [a-zA-Z0-9_.]+
        \s*:members:
        \s*:undoc-members:
        \s*:show-inheritance:(
        \s*:no-inherited-members:)?
        """[1:-1]))
    for file in no_modules:
        with open(file+".rst", "r+") as f:
            contents = f.read()
            match = rgx.search(contents)
            # should match
            if not match:
                continue
            repl = match.group(1) if "===" in match.group(1) else ""
            contents = rgx.sub(repl, contents)
            f.seek(0)
            f.write(contents)
            f.truncate()

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