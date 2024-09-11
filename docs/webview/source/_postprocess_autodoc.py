# ruff: noqa: FURB101,FURB103
import re
import glob
import os
from typing_extensions import Literal

_file_contents : dict[str, str] = {}

def _get_contents(file):
    if file in _file_contents:
        return _file_contents[file]
    with open(file, "r") as f:
        contents = f.read()
        _file_contents[file] = contents
    return contents

def _change_contents(file, contents):
    assert file in _file_contents, "File not read before"
    _file_contents[file] = contents

def _write_all_contents():
    for file, contents in _file_contents.items():
        with open(file, "w") as f:
            f.write(contents)
    
def _get_subcontent(contents:str, pattern, end="----"):
    start = contents.find(pattern)
    end = contents.find(end, start)
    if end == -1:
       end = None
    return start, end, contents[start:end]

def port_install_md():
    with open("../../Install.md", "r") as f:  # noqa: FURB101
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
        
    with open("docs/Install.md", "w") as f:  # noqa: FURB103
        f.write(contents)


def module_contents_at_top():
    files = ["classes.rst", ("agents.substep_managers.rst", True), "agents.rules.rst"]
    for file in files:
        if isinstance(file, tuple):
            file, remove_section = file
        else:
            remove_section = False
        contents = _get_contents(file)
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
        _change_contents(file, contents)

def exclude_cdp():

    exclude_cdp = "\"'cleanup', 'create_blueprint', 'find_weather_presets', 'generate_spawn_points', 'get_actor_by_id', 'get_actor_by_name', 'get_local_planner', 'get_osc_global_param_value', 'get_random_seed', 'get_traffic_manager_port', 'handle_actor_batch', 'is_runtime_init_mode', 'is_sync_mode', 'on_carla_tick', 'prepare_map', 'register_actor', 'register_actors', 'remove_actor_by_id', 'remove_actors_in_surrounding', 'request_new_actor', 'request_new_actors', 'request_new_batch_actors', 'reset_lights', 'set_client', 'set_ego_route', 'set_latest_scenario', 'set_local_planner', 'set_runtime_init_mode', 'set_traffic_manager_port', 'set_world', 'spawn_actor', 'update_light_states', 'update_osc_global_params', 'world'\"".replace("'", "") #pylint: disable=line-too-long
    
    content = _get_contents("classes.rst")
    start = content.find(".. automodule:: classes.rule\n")
    end = content.find("----", start)
    subcontent = content[start:end]
    if exclude_cdp in subcontent:
        return
    # Do not write double online
    if ":exclude-members:" not in subcontent:
        subcontent = re.sub(".. automodule:: classes.rule\n", ".. automodule:: classes.rule\n   :exclude-members: " + exclude_cdp + "\n", subcontent)
    else:
        subcontent = re.sub(r':exclude-members:"', ':exclude-members: ' + exclude_cdp + ", ", subcontent)
    
    content = content[:start] + subcontent + content[end:]

    _change_contents("classes.rst", content)
        
def patch_rule():
    content = _get_contents("classes.rst")
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
        # NOTE: Should start with ", "!
        subcontent = re.sub(r':exclude-members: "', ':special-members: __call__\n   :exclude-members: ", MultiRule, RandomRule, BlockingRule, ', subcontent, count=1)
    else:
        assert ":exclude-members:" not in subcontent, "Double execution of patch_rule"
        subcontent = re.sub(".. automodule:: classes.rule\n",
                            ':special-members: __call__\n   :exclude-members: ", MultiRule, RandomRule, BlockingRule"', subcontent)

    
    subcontent = re.sub(r":\n\n", ":" + dedent(insert), subcontent, count=1)
    
    content = content[:start] + subcontent + content[end:]

    _change_contents("classes.rst", content)
            

def show_inheritance():
    """ Insert show-inheritance directive with special members"""
    files = {"classes.rst" : {"classes.worldmodel" : "get_client, get_map, get_world"}}
    for file, updates in files.items():
        content = _get_contents(file)
        
        for module, members in updates.items():
            start = content.find(".. automodule:: "+module+"\n")
            end = content.find("----", start)
            subcontent = content[start:end]
            
            if ":inherited-members: " + members in subcontent:
                continue
            subcontent = re.sub(r":members:(\n   :inherited-members:)?", r"\n   ".join([":members:",
                                                                    ":inherited-members: " + members,
            ]), subcontent, count=1)
            content = content[:start] + subcontent + content[end:]
        
        _change_contents(file, content)
        
def remove_inheritance():
    """ Insert no-inherited-members directive to all modules"""
    files = ['agents.rules.obstacles.rst',
                        'agents.rules.rst']
    
    for file in files:
        content = _get_contents(file)
        if ":no-inherited-members:" in content:
            continue # for double execution on read the docs.
        content = re.sub(r":show-inheritance:", r"\n   ".join([":show-inheritance:",
                                                                    #":no-index:"
                                                                        ":no-inherited-members:"]),
                                                            content)
        _change_contents(file, content)
            
    fine_files: dict[str, list[str]] = {"classes.rst" : ["classes.constants", "classes.exceptions"],
                                        "agents.tools.rst" : ["agents.tools.config_creation", "agents.tools.hints"],
                                  }
    
    for file, submodules in fine_files.items():
        content = _get_contents(file)
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
        _change_contents(file, content)

def _patch_agent(content:str):
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
    """Add members to LunaticChallenger"""
    content = _get_contents("agents.rst")
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
        
        shown = "'set_global_plan', 'destroy', 'run_step', 'sensors', 'setup', '__init__', 'BASE_SETTINGS'".replace("'", "")  # noqa
        excluded = "get_entry_point"
        subcontent = re.sub(r":members:", r"\n   ".join([":members:",#+shown,
                                                        #":no-index:"
                                                            ":exclude-members: " + excluded,
                                                            ":special-members: __call__",]),
                                                string=subcontent,
                                                count=1)
    
        content = content[:start] + subcontent + content[end:]
    _change_contents("agents.rst", content)
        
def add_imported_members():
    modules: dict[str, "list[str] | str | Literal['all'] | tuple[str, list[str]]"] = {"classes" : ["CustomSensorInterface"],
                                                             "classes.carla_originals" : "all",
                                                             "agents.tools" : ("config_creation", ["MISSING, NestedConfigDict"]), # BUG somehow does not work
                                                             }
    for file, members in modules.items():
        if isinstance(members, str) and members != "all":
            members = [members]
        content = _get_contents(file+".rst")
        if isinstance(members, tuple):
            module = file + "." + members[0]
            members = members[1]
        else:
            module = file
        start = content.find(".. automodule:: "+module+"\n")
        end = content.find("----", start)
        if end == -1:
            subcontent = content[start:]
            pattern = "\n$"
            extra = "\n"
        else:
            subcontent = content[start:end]
            pattern = "\n\n"
            extra = "\n"
        if members != "all":
            members = list(filter(lambda member: member not in subcontent, members))
            if not members:
                continue
            subcontent = re.sub(pattern, extra+"   :imported-members: " + ", ".join(members) +extra+"\n", subcontent, count=1)
        elif ":imported-members:" in subcontent:
            continue
        else:
            subcontent = re.sub(pattern, extra+"   :imported-members:" + extra +"\n", subcontent, count=1)
        content = content[:start] + subcontent + content[end:]
        _change_contents(file+".rst", content)
        
def remove_submodules():
    packages = ["classes.carla_originals.rst"]
    for package in packages:
        content = _get_contents(package)
        start = content.find("Submodules\n----------")
        if start == -1:
            continue
        end = content.find("Module contents\n", start)
        newcontent = content[:start] + content[end:]
        newcontent = newcontent.strip() + "\n\n"
        _change_contents(package, newcontent)
            
#def make_canonical():
#    pass

def remove_init():
    module : "dict[str, list[str | tuple[str, str | None]]]" = {
                              "classes" : [("classes.evaluation_function", "__add__, __and__, __or__, __invert__" ),
                                           ("classes.type_protocols", None),
                                           ],
                              "classes.carla_originals" : [("classes.carla_originals", None)],
                              "agents.tools" : [("agents.tools.hints", "__bool__")],
              }
    for file, members in module.items():
        content = _get_contents(file+".rst")
        for member in members:
            if not isinstance(member, str) and member is not None:
                member, include_only = member
                directive : str = ":special-members:"
            if include_only is None:
                directive = ":no-special-members:"
                include_only = "<blank>"
            elif include_only == "all":
                directive = ":special-members:"
                include_only = "<blank>"
            else:
                assert directive  # this is then from last iteration
            start = content.find(".. automodule:: "+member+"\n")
            end = content.find("----", start)
            subcontent = content[start:end]
            if include_only in subcontent:
                continue
            
            subcontent = re.sub(r":members:", r"\n   ".join([":members:",
                                                            directive + (" " + include_only if include_only != "<blank>" else ""),
                                                            ]),
                                                    string=subcontent,
                                                    count=1)
            content = content[:start] + subcontent + content[end:]
            _change_contents(file+".rst", content)


def insert_github_ref():
    contents = _get_contents("AgentGameLoop.rst")
    start, _, _ = _get_subcontent(contents, "===\n", end=".. automodule::")
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
    _change_contents("AgentGameLoop.rst", contents)
        
def patch_config_creation():
    # Remove init
    contents = _get_contents("agents.tools.rst")
    start, end, subcontent = _get_subcontent(contents, ".. automodule:: agents.tools.config_creation\n")
    if "no-special-members" in subcontent:
        return
    subcontent = re.sub(r":members:", r"\n   ".join([":members:",
                                                    ":no-special-members:"]),
                                            string=subcontent,
                                            count=1)
    contents = contents[:start] + subcontent + contents[end:]
    _change_contents("agents.tools.rst", contents)
        
def remove_empty_modules():
    from textwrap import dedent
    no_modules = ["agents", "agents.tools", "agents.rules.obstacles"]
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
        contents = _get_contents(file+".rst")
        match = rgx.search(contents)
        # should match
        if not match:
            continue
        repl = match.group(1) if "===" in match.group(1) else ""
        contents = rgx.sub(repl, contents)
        _change_contents(file+".rst", contents)
        
def insert_file_references():
    rst_files = filter(lambda file: file not in ("index.rst", "readme_link.rst"),
                       glob.glob("[!_]*.rst"))  # NOTE: if prefixed with ./ need to be stripped  # noqa: PTH207
    re_packages = re.compile(r"(^[a-zA-Z._]+) package\n=+")
    
    re_modules = re.compile(r"(([a-zA-Z0-9\\_.]+) module\n)")
    
    for file in rst_files:
        
        content = _get_contents(file)
        packages: "list[str]" = re_packages.findall(content)
        for package in packages:
            # allow file anchors to here
            py_package = package.replace(".", "/")
            if py_package[-1] != "/":
                py_package += "/"
            inject = fr".. _{py_package}:\n\n{package} package\n\1"
            if inject in content:
                continue
            content = re.sub(rf"{package} package\n(=+)", inject, content, count=1)
            
        modules: "list[tuple[str, str]]" = re_modules.findall(content)
        for match in modules:
            full_match, module = match
            # allow file anchors to here
            py_module = module.replace(".", "/").replace("\\", "")  # + ".py"; _ underscores are escaped
            inject = f"\n.. _{py_module}:\n\n{full_match}"
            if inject in content:
                continue
            content = content.replace(full_match, inject)
            
        _change_contents(file, content)
        #content = content.replace(match, f":file:`{match}`")
        #re.sub(r"(\w+) package\n==")
        
    
    

def _no_value_constants():
    return
    try:
        import classes.constants, inspect, enum  # noqa
        all_classes = [getattr(classes.constants, key) for key, cls in vars(classes.constants).items() if not key.startswith("_") and inspect.isclass(cls)]
        flags = [cls for cls in all_classes if issubclass(cls, (enum.Flag, enum.IntFlag, enum.Enum)) and cls.__module__ == classes.constants.__name__]  # noqa
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



def patch_all():
    """Executes all public functions of this module"""
    if os.getcwd().endswith("docs/webview/source"):  # noqa: PTH109
        pass
    else:
        return
    from typing import Callable
    this_module= globals().get("__name__", "docs.webview.source._postprocess_autodoc")
    all_funcs : dict[str, "Callable"] = dict(filter(lambda v: not v[0].startswith("_")
                                  and callable(v[1])
                                  and v[1].__module__ == this_module
                                  and v[0] not in ("execute_all", "patch_all", _write_all_contents.__name__)
                                  ,
                        globals().items()))
    for foo in all_funcs.values():
        if foo == insert_file_references:
            continue
        foo()
    insert_file_references() # do that one later
    _write_all_contents()
