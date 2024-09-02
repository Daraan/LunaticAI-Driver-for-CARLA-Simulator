"""
Helper Tools for :py:mod:`.config_tools`.
"""

from __future__ import annotations

import ast
import inspect
import logging
import os

# pyright: reportPrivateUsage=false, reportUnknownLambdaType=false, reportUnusedClass=false
# pyright: reportPossiblyUnboundVariable=information,reportAttributeAccessIssue=warning
# pyright: reportUnknownVariableType=information, reportUnknownMemberType=information
import sys
from dataclasses import is_dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, cast, get_type_hints

import carla
import omegaconf.errors
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, DictConfig, ListConfig, MissingMandatoryValue, OmegaConf, SCMode, open_dict
from omegaconf._utils import is_structured_config
from typing_extensions import TypeAlias, TypeAliasType, TypeVar

from classes.constants import AD_RSS_AVAILABLE, Phase, RssLogLevelStub, RssRoadBoundariesModeStub
from launch_tools import ast_parse

if TYPE_CHECKING:
    from agents.tools.config_creation import (
        AgentConfig,
        CreateRuleFromConfig,
        LunaticAgentSettings,
        RuleConfig,
        RuleCreatingParameters,
    )
    from classes.rule import Rule

#from types import MappingProxyType
#ALLOW_OBJECTS = cast(Dict[str, Literal[True]], MappingProxyType({"allow_objects" : True}))
#"""
#Alias for :python:`{"allow_objects" : True}`
# NOTE: Problem: Flag is not copied to a new dictionary, it cannot be modified; or is shared
# if this one is mutable
#"""

READTHEDOCS = os.environ.get("READTHEDOCS", False)
"""Whether the code is currently running on readthedocs."""

# ----------- Resolvers -------------

def look_ahead_time(speed: float, time_to_collision: float, plus: float=0) -> float:
    """
    Convert the current speed in km /h and a time to collision in seconds to a distance in meters
    and adds a slight buffer on top.

    Use as :python:`"${look_ahead_time: ${live_info.current_speed}, time, }"`
    """
    return speed / 3.6 * time_to_collision + plus # km / h * s = m

# need this check for readthedocs
if not READTHEDOCS and os.environ.get("_OMEGACONF_RESOLVERS_REGISTERED", "0") == "0":
    import random
    OmegaConf.register_new_resolver("sum", lambda x, y: x + y)       # type: ignore[arg-type]
    OmegaConf.register_new_resolver("subtract", lambda x, y: x - y)  # type: ignore[arg-type]
    OmegaConf.register_new_resolver("multiply", lambda x, y: x * y)  # type: ignore[arg-type]
    OmegaConf.register_new_resolver("divide", lambda x, y: x / y)    # type: ignore[arg-type]
    OmegaConf.register_new_resolver("min", lambda *els: min(els))
    OmegaConf.register_new_resolver("max", lambda *els: max(els))
    OmegaConf.register_new_resolver("randint", random.randint)
    OmegaConf.register_new_resolver("randuniform", random.uniform)
    OmegaConf.register_new_resolver("look_ahead_time", look_ahead_time)
    os.environ["_OMEGACONF_RESOLVERS_REGISTERED"] = "1"


CONFIG_SCHEMA_NAME = "launch_config_schema.yaml"
"""Name to use for the launch_config as it cannot be launch_config itself."""


config_store = ConfigStore.instance()
"""Hydra_ 's ConfigStore instance to access config schemas."""

POSTPOND_REGISTER = sys.version_info < (3, 10)
postpond_register: dict[str, type[Any]] = {}

def register_hydra_schema(obj: "type[Any]", name: Optional[str]=None):
    """
    Uses Hydra's ConfigStore to register the schema of the current class in the
    :py:obj:`ConfigStore <config_store>`.
    
    See also:
        :py:func:`config_path`
    """
    if name is None:
        name = cast(str, getattr(obj, "_config_path", obj.__name__))
    #if not POSTPOND_REGISTER:
    #    pass
    #else:
    #    postpond_register[name] = obj
    config_store.store(name, OmegaConf.structured(obj, flags={"allow_objects" : True}),
                        provider="agents.tools.config_creation", group=None, package=obj.__module__)
        
    
def config_path(path: Optional[str] = None):
    """
    Decorator to register the schema of the current class with Hydra's ConfigStore.
    
    Returns
        (Callable[[type[AgentConfig]], type[AgentConfig]]) Wrapper function to register the schema.
    """
    
    if not READTHEDOCS:
    
        def _register(obj : "type[_AnAgentConfig]") -> "type[_AnAgentConfig]":  # pyright: ignore[reportRedeclaration]
            if path is None:
                name = obj._config_path # type: ignore[attr-defined]
            else:
                name = path
            if name is None or name == "NOT_GIVEN":
                raise ValueError(f"Path is not given for {obj.__name__}. Use @register('path/to/config.yaml') to set the path.")
            dots = name.count(".")
            if dots > 0 and not (dots == 1 and name.endswith(".yaml")):
                raise ValueError(f"Use '/' as separator and not dots. E.g. {name.replace('.', '/')} and not '{name}'")
            obj._config_path = name
            if not is_dataclass(obj) and not TYPE_CHECKING: # type: ignore
                raise ValueError(f"Only dataclasses can be registered. {obj.__name__} is not a dataclass.")
            register_hydra_schema(obj, name)
            return obj
    else:
        # dummy, to avoid errors
        def _register(obj : "type[_AnAgentConfig]") -> "type[_AnAgentConfig]":
            return obj
        
    return _register
    
def load_config_schema(name: str) -> Any:
    return config_store.load(name).node

# ---------------------
# Helper methods
# ---------------------

def set_readonly_keys(conf : Union[DictConfig, ListConfig], keys : List[str]):
    """
    Sets nodes to readonly.

    See: https://github.com/omry/omegaconf/issues/1161
    """
    if isinstance(keys, str):
        keys = [keys]
    for key in keys:
        OmegaConf.set_readonly(conf._get_node(key), True) # pyright: ignore[reportArgumentType]

def set_readonly_interpolations(conf : Union[DictConfig, ListConfig]):
    """
    Sets all interpolations to readonly.

    See: https://github.com/omry/omegaconf/issues/1161
    """
    if conf._is_interpolation():
        OmegaConf.set_readonly(conf, True)
    elif isinstance(conf, DictConfig):
        for key in conf:
            set_readonly_interpolations(conf._get_node(key)) # pyright: ignore[reportArgumentType]
    elif isinstance(conf, ListConfig):                                # type: ignore
        for key in range(len(conf)):
            set_readonly_interpolations(conf._get_node(key)) # pyright: ignore[reportArgumentType]
    else:
        print("WARNING: Could not set readonly for", type(conf))


_NOTSET = object()
"""Sentinel value for not set default values."""

# ----- Type Annotations -----

ConfigType = TypeVar("ConfigType", DictConfig, "AgentConfig")
"""
Generic of an object that is a :py:class:`omegaconf.DictConfig`
or a subclass of :py:class:`AgentConfig`.
"""

_T = TypeVar("_T")
_M = TypeVar("_M", Dict[str, Any], DictConfig)
"""A generic type variable for a mapping type."""

_AnAgentConfig = TypeVar("_AnAgentConfig", bound="AgentConfig")
"""A generic :py:class:`AgentConfig` type variable"""

AsDictConfig = TypeAliasType("AsDictConfig", _AnAgentConfig, type_params=(_AnAgentConfig,))
"""
This annotation hints that object is a duck-typed :py:class:`omegaconf.DictConfig`
and not a subclass of :py:class:`AgentConfig`.
"""

# Problem in Sphinx is entered twice and creates large signatures

"""
Allowed types for nested config
"""

# Special annotations
if READTHEDOCS and not TYPE_CHECKING:
    from typing_extensions import TypeAliasType
    # annotate MISSING instead of ???
    MISSING = TypeAliasType("MISSING", Any)
    """
    Alias for :py:obj:`omegaconf.MISSING`, is literally :python:`"???"` but has type :python:`Any`.

    If an attribute with this value is accessed from a :py:class:`DictConfig`,
    it will raise a :py:exc:`MissingMandatoryValue` error.

    :meta hide-value:
    :meta public:
    """

    # prevent unpack of nested types
    NestedConfigDict = TypeAliasType("NestedConfigDict", dict[str, "AgentConfig | DictConfig | Any |  NestedConfigDict"]) # type: ignore
    """
    Type alias for nested configurations: :python:`Dict[str, NestedConfigDict | AgentConfig | DictConfig | Any]`

    :meta hide-value:
    """
else:
    NestedConfigDict : TypeAlias = Dict[str, "AgentConfig | DictConfig | Any | NestedConfigDict"]

_NestedStrDict = Dict[str, "str | _NestedStrDict"]
"""Nested dict with str as leaves"""

if TYPE_CHECKING:
    # AgentConfig parent should include DictConfig interface; without being a DictConfig
    # BaseContainer adds the methods, however is ABC with more methods
    from omegaconf.basecontainer import BaseContainer  # noqa: F401
    # More informative types when type checking; need primitive types at runtime
    DictConfigAlias : TypeAlias = Union[DictConfig, NestedConfigDict]
    OverwriteDictTypes : TypeAlias = Dict[str, Union[Dict[str, NestedConfigDict], "AgentConfig"]]
    
    class DictConfigLike(DictConfig):
        """
        Duck-typed DictConfig still appears like a DictConfig.
        
        Note:
            At runtime this is just :py:class:`object`.
        """
        keys = DictConfig.keys
        values = DictConfig.values
else:
    # primitive type at runtime
    DictConfigAlias : TypeAlias = Dict[str, Any]
    OverwriteDictTypes : TypeAlias = Dict[str, Dict[str, Any]]
    DictConfigLike = object

# --------------- YAML Export -----------------

PATH_FIELD_NAME = "config_path"

def extract_annotations(parent : "ast.Module", docs : Dict[str, _NestedStrDict], global_annotations : Dict[str, _NestedStrDict]):
    """Extracts comments from the source code"""
    import re
    for main_body in parent.body:
        # Skip non-classes
        if not isinstance(main_body, ast.ClassDef):
            continue
        if main_body.name in ("AgentConfig", "SimpleConfig", "class_or_instance_method", "_from_config_default_rules"):
            continue
        docs[main_body.name] = {}
        for base in reversed(main_body.bases):
            # Fill in parent information
            try:
                if isinstance(base, ast.IfExp) and base.test.id == "TYPE_CHECKING": # (DictConfig if TYPE_CHECKING else object):
                    continue
                docs[main_body.name].update(docs.get(base.id, {})) # pyright: ignore[reportUnknownArgumentType]
            except Exception:
                logging.exception(f"Error in {main_body.name}")

        target : str
        for i, body in enumerate(main_body.body):
            if isinstance(body, ast.ClassDef):
                # Nested classes, extract recursive
                extract_annotations(ast.Module([body], type_ignores=[]), docs[main_body.name], global_annotations) # type: ignore[arg-type]
                continue
            elif isinstance(body, ast.AnnAssign):
                target = body.target.id
                continue
            elif isinstance(body, ast.Assign):
                target = body.targets[0].id
                continue
            elif isinstance(body, ast.Expr):
                try:
                    # NOTE: This is different for <Python3.8; this is ast.Str
                    doc: str = body.value.value # type: ignore
                except AttributeError:
                    # Try < 3.8 code
                    doc = body.value.s          # type: ignore
                assert isinstance(doc, str)
                if i == 0: # Docstring of class
                    target = "__doc__"
                # else: use last found target
            else:
                continue

            if doc.startswith(".. <take doc|") and doc.endswith(">"):
                key = doc[len(".. <take doc|"):-1]
                try:
                    docs[main_body.name][target] = docs[main_body.name][key]
                except KeyError as e:
                    try:
                        # Do global look up, docs is here _class_annotations
                        # Move fitting sub-class to key
                        docs[main_body.name][target] = global_annotations[key] # pyright: ignore[reportOptionalSubscript]
                        continue
                    except Exception:
                        pass
                    raise NameError(f"{key} needs to be defined before {target} or globally") from e
                continue
            doc = inspect.cleandoc(doc)
            if target == "__doc__":
                header = ("-" * len(main_body.name)) + "\n" # + main_body.name + "\n" + ("-" * len(main_body.name)) + "\n" + doc
                footer = "\n" + ("-" * len(main_body.name))

                if doc.startswith(".. @package"):
                    start = doc.find("\n") + 1
                    if start == 0:
                        # no linebreak found
                        doc += "\n"
                        start = doc.find("\n") + 1
                    header += main_body.name + "\n" + ("-" * len(main_body.name)) + "\n"
                    if doc[start:].lstrip():
                        doc = doc[3:start] + header + doc[start:].lstrip() + footer + "\n\n"
                    else:
                        # no content beside package
                        doc = doc[3:start] + header + "\n"
                else:
                    doc = header + doc + footer
            # remove rst
            doc = re.sub(r":py:\w+:\\?`[~.!]*(.+?)\\?`", r"`\1`", doc)
            doc = re.sub(r":(?::|\w|-)+?:`+(.+?)`+", r"`\1`", doc)
            docs[main_body.name][target] = doc
            del target # delete to get better errors
            del doc

class_annotations : Optional[Dict[str, _NestedStrDict]] = None
"""Nested documentation strings for classes; used for YAML comments."""

def get_commented_yaml(cls_or_self : Union[type[AgentConfig], AgentConfig], string:str, container: "DictConfig | NestedConfigDict",
                        *, include_private:bool=False) -> str:
    if inspect.isclass(cls_or_self):
        cls = cls_or_self
    else:
        cls = cls_or_self.__class__
    cls_file = inspect.getfile(cls)
    # Get documentations and store globally
    global class_annotations
    if class_annotations is None:
        with open(cls_file, "r") as f: # NOTE: This file only!
            tree = ast_parse(f.read())
            class_annotations = {}
            extract_annotations(tree, docs=class_annotations, global_annotations=class_annotations)
    
    from ruamel.yaml import YAML
    from ruamel.yaml.comments import CommentedMap
    yaml2 = YAML(typ='rt')
    #container = OmegaConf.to_container(options, resolve=False, enum_to_str=True, structured_config_mode=SCMode.DICT)
    data : CommentedMap = yaml2.load(string)
    
    cls_doc = class_annotations[cls.__name__]

    # First line
    data.yaml_set_start_comment(cls_doc.get("__doc__", cls.__name__))
    
    nested_data : list[CommentedMap] = []
    # add comments to all other attributes
    def add_comments(container : "DictConfig | NestedConfigDict",
                     data: CommentedMap,
                     lookup: Union[AgentConfig, _NestedStrDict],
                     indent: int=0):
        """
        Recursively adds comments to the YAML output.
        
        Args:
            container: The current dict to be commented
            lookup: The lookup dictionary for docstrings
        """
        nested_data.append(data)
        if isinstance(container, DictConfig):
            containeritems = container.items_ex(resolve=False)
        else:
            containeritems = container.items()
        for key, value in containeritems:
            if TYPE_CHECKING:
                assert isinstance(key, str)
            if isinstance(value, dict) and isinstance(cls_doc.get(key, None), dict):
                # Add nested comments
                add_comments(value, data[key], cls_doc[key], indent=indent+2) # type: ignore[arg-type]
                comment_txt = "\n" + cls_doc[key].get("__doc__", "")                     # type: ignore
                assert isinstance(comment_txt, str)
                # no @package in subfields
                if comment_txt.startswith("\n@package "): # already striped here
                    comment_txt = "\n".join(comment_txt.split("\n")[2:]).strip()
            else:
                comment_txt = lookup.get(key, None)
            if comment_txt is None:
                continue
            if isinstance(comment_txt, dict):
                # Add comments for nested dataclasses
                try:
                    add_comments(comment_txt, data[key], comment_txt, indent=indent+2)
                except KeyError:
                    # double nested will throw a KeyError here as key not in data; will only be the
                    # variable name of the nested dataclass; seems to be okay.
                    # NOTE: logging level might only be on WARNING here!
                    logging.debug(f"KeyError for {key} in {cls.__name__} when adding comments. "
                                  "This should be okay, report if descriptions are missing.")
                continue
            if (":meta exclude:" in comment_txt) or not include_private and ":meta private:" in comment_txt:
                data.pop(key)
                continue  # Skip private fields; TODO does not skip "_named" fields, is that a problem?
            comment_txt = comment_txt.replace("\n\n","\n \n")
            if comment_txt.count("\n") > 0:
                comment_txt = "\n"+comment_txt
            data.yaml_set_comment_before_after_key(key, comment_txt, indent=indent)
    #top_container = container  # for debugging
    add_comments(container, data, cls_doc)  # pyright: ignore[reportArgumentType]
    # data.yaml_add_eol_comment(comment_txt, key = key)

    import re
    has_null_entry = re.findall(r"^\s*\w+: null$", string, re.MULTILINE)

    import io
    stream = io.StringIO()
    yaml2.dump(data, stream)
    stream.seek(0)
    string = stream.read()
    # Fixes:
    if "rss" in data:
        start = string.find("use_stay_on_road_feature: ")
        end = string.find("\n", start)
        # quote On/Off; to not be interpreted as boolean
        string = string[:start+len("use_stay_on_road_feature: ")] + "'" + string[start+len("use_stay_on_road_feature: "):end] + "'" + string[end:]
        # entry: null has been replaced by entry: null
    if has_null_entry:
        entry: str
        for entry in has_null_entry:
            parts = entry.partition(":")
            if parts[2] != " null":
                logging.error(f"Error in {cls.__name__} for {entry}. Entry is not ' null'. This should not happen")
                continue
            entry = parts[0]+":"
            string = re.sub(fr"^{entry}$", entry + " null", string, flags=re.MULTILINE)
    return string


def to_yaml(cls_or_self : Union[type[AgentConfig], AgentConfig], resolve:bool=False, yaml_commented:bool=True,
            detailed_rules:bool=False, *, include_private:bool = False) -> str:
    """
    Convert the options to a YAML string representation.

    Args:
        resolve : Whether to resolve interpolations. Defaults to False.
        yaml_commented : Whether to include comments in the YAML output. Defaults to True.
        detailed_rules : Whether to include detailed rules in the YAML output. Defaults to False.
        include_private : Whether to include fields that are marked as private. Defaults to False.

    Returns:
        str: The YAML string representation of the options.
    """
    
    """
    # Draft a dumper
    from omegaconf._utils import get_omega_conf_dumper
    Dumper = get_omega_conf_dumper()
    org_func = Dumper.str_representor
    def str_representor(dumper, data: str):
        result = org_func(dumper, data)
        return result
    
    Dumper.add_representor(str, str_representor)
    string = yaml.dump(  # type: ignore
        container,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=kwargs.get("sort_keys", False),
        Dumper=Dumper,
    )
    """
    import yaml
    from omegaconf._utils import get_omega_conf_dumper
    cfg : DictConfig = OmegaConf.structured(cls_or_self, flags={"allow_objects": True})

    if ((inspect.isclass(cls_or_self) and cls_or_self.__name__ == "LunaticAgentSettings")
        or (isinstance(cls_or_self, object) and cls_or_self.__class__.__name__ == "LunaticAgentSettings")):
        with open_dict(cfg):
            del cfg["self"]
            del cfg["current_rule"]
    if "rules" in cfg:
        # Validate and remove missing keys for the yaml export
        if TYPE_CHECKING:
            assert isinstance(cfg, LunaticAgentSettings)
        rules :  List[RuleCreatingParameters] = cfg.rules
        masked_rules : list[DictConfig] = []
        for rule_cfg in rules:
            if "phases" in rule_cfg.keys():
                if TYPE_CHECKING:
                    assert isinstance(rule_cfg, CreateRuleFromConfig)
                # > CreateRuleFromConfig
                if detailed_rules:
                    # Circular import can only call this after agents.rules
                    try:
                        from agents.rules import rule_from_config
                    except ImportError:
                        print("Could not import agents.rules.rule_from_config. Set detailed_rules=False to avoid this error. Call this function somewhere else.")
                        raise
                    rule: Rule = rule_from_config(rule_cfg)
                    self_config: RuleConfig = rule.self_config
                    if OmegaConf.is_missing(rule_cfg, "phases"):
                        rule_cfg.phases = next(iter(self_config.instance.phases)) # only support one atm
                    with open_dict(self_config):
                        del self_config["instance"]
                    if OmegaConf.is_missing(rule_cfg, "self_config"):
                        rule_cfg.self_config = OmegaConf.to_container(self_config, enum_to_str=True) # type: ignore
                    else:
                        try:
                            rule_cfg.self_config.update(self_config)
                        except Exception:
                            with open_dict(rule_cfg):
                                rule_cfg.self_config = OmegaConf.to_container(OmegaConf.merge(self_config, rule_cfg.self_config), enum_to_str=True) # type: ignore
                
                if "phases" in rule_cfg and not isinstance(rule_cfg.phases, str):
                    assert isinstance(rule_cfg.phases, Phase), "Currently only supports a Phase as string or Phase object."
                    rule_cfg.phases = str(rule_cfg.phases)
                
                if detailed_rules:
                    assert not OmegaConf.is_missing(rule_cfg, "phases")
                
            # NOTE: For some reason "_args_" in rule does NOT WORK
            elif "_args_" in rule_cfg.keys() and OmegaConf.is_missing(rule_cfg, key="_args_"):
                # check > CallFunctionFromConfig
                raise ValueError(f"{rule_cfg} has no phase or (positional) `_args_` key. Did you forget to add a phase?"
                                    "If the _target_ is a function, still prove an empty `_args_ = []` key.")
            missing_keys = {k for k in rule_cfg.keys() if OmegaConf.is_missing(rule_cfg, k)}
            clean_rule = OmegaConf.masked_copy(rule_cfg, set(rule_cfg.keys()) - missing_keys)  # pyright: ignore[reportArgumentType]
            masked_rules.append(clean_rule)
        cfg.rules = masked_rules # type: ignore[attr-defined]
        
    container: Dict[str, Any] = OmegaConf.to_container(cfg, resolve=resolve, enum_to_str=True) # pyright: ignore[reportAssignmentType]
    if AD_RSS_AVAILABLE:
        def replace_carla_enum(content: _T) -> _T:
            # retrieve name from the stubs
            if isinstance(content, carla.RssLogLevel):
                return RssLogLevelStub(content).name
            if isinstance(content, carla.RssRoadBoundariesMode):
                return RssRoadBoundariesModeStub(content).name
            return content
        
        def recursive_replace(content: _T) -> _T:
            if isinstance(content, dict):
                return {k: recursive_replace(v) for k, v in content.items()} # type: ignore
            if isinstance(content, list):
                return [recursive_replace(v) for v in content]               # type: ignore
            return replace_carla_enum(content)
        container = recursive_replace(container)
    string = yaml.dump(
        container,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        Dumper=get_omega_conf_dumper(),
    )
    if not yaml_commented:
        return string
    # Extend
    return get_commented_yaml(cls_or_self, string, container)  # type: ignore[arg-type]

def export_options(cls_or_self: Union[type[AgentConfig], AgentConfig],
                    path: Union[str, "os.PathLike[str]"],
                    *,
                    resolve: bool = False,
                    with_comments: bool = False,
                    detailed_rules: bool = False,
                    include_private: bool = False) -> None:
    """
    Exports the options to a YAML file. With the :py:meth:`to_yaml` method.

    Args:
        path : The path for the exported YAML file.
        resolve : Whether to resolve the options before exporting. Defaults to False.
        with_comments : Whether to include comments in the exported YAML file. Defaults to False.
        detailed_rules : Whether to include detailed rules in the exported YAML file. Defaults to False.
        include_private : Whether to include private fields in the exported YAML file. Defaults to False.

    Returns:
        None
    """
    if inspect.isclass(cls_or_self):
        options = cls_or_self()  # type: ignore[call-arg]
    else:
        options = cls_or_self
    if with_comments:
        string = cls_or_self.to_yaml(resolve=resolve, yaml_commented=True, detailed_rules=detailed_rules,
                                    include_private=include_private)
        os.makedirs(os.path.split(path)[0], exist_ok=True)
        with open(path, "w") as f:
            f.write(string)
        return
    if not isinstance(options, DictConfig):
        # TODO: look how we can do this directly from dataclass
        options = OmegaConf.create(options, flags={"allow_objects": True})  # type: ignore
    OmegaConf.save(options, path, resolve=resolve)  # NOTE: This might raise if options is structured, for export structured this is actually not necessary. # type: ignore[argument-type]

            
# --------------- Other Tools -----------------

def set_container_type(base: "type[AgentConfig]", container : Union[NestedConfigDict, "AgentConfig"]) -> None:
    """
    Sets the object_type for sub configs if the config has been initialized with
    a :py:class:`omegaconf.DictConfig` and not the respective AgentConfig subclass.

    Args:
        base : The base / duck type the container should have.
        container : The passed value.
    """
    try:
        annotations = get_type_hints(base)
    except TypeError:
        logging.debug("Error getting type hints for", base.__name__, "with container", type(container))
        return
    keys: "list[str]" = container.__dataclass_fields__.keys() if is_dataclass(container) else container.keys() # type: ignore
    for key in keys:
        if key == "overwrites" or key not in annotations:
            continue
        if (isinstance(container, (DictConfig, ListConfig))
            and (OmegaConf.is_interpolation(container, key)
                    or key not in container)):
            continue
        try:
            value = getattr(container, key, MISSING)
        except MissingMandatoryValue:
            continue
        if value == MISSING:
            continue
        typ = annotations[key]
        if is_structured_config(typ): # is structured dataclass or attrs
            if OmegaConf.get_type(value) is dict: # but is not
                if isinstance(value, DictConfig):
                    #value._metadata.object_type = typ
                    if hasattr(typ, "create"):
                        setattr(container, key, typ.create(value, as_dictconfig=True))
                    else:
                        setattr(container, key, OmegaConf.structured(typ(**value), flags={"allow_objects" : True}))
                # Below might rise type-errors if the schema is not correct
                elif hasattr(typ, "uses_overwrite_interface") and typ.uses_overwrite_interface():  # type: ignore[attr-defined]
                    setattr(container, key, typ(overwrites=value)) # type: ignore[arg-type]
                else:
                    setattr(container, key, typ(**value))
            if isinstance(value, (DictConfig, dict)) or is_dataclass(value):
                set_container_type(typ, value) # type: ignore[arg-type]
                

        
def _flatten_dict(source : NestedConfigDict, target : NestedConfigDict, resolve : bool=False) -> None:
    if isinstance(source, DictConfig):
        items = source.items_ex(resolve=resolve)
    else:
        items = source.items() # normal case after to_container
    for k, v in items:
        if isinstance(v, dict):
            _flatten_dict(v, target)
        else:
            if k in target:
                print(f"Warning: Key '{k}'={target[k]} already exists in target. Overwriting with {v}.")
            target[k] = v  # type: ignore[arg-type]
            
def flatten_config(config : "type[AgentConfig] | AgentConfig", *, resolve: bool = True) -> Dict[str, Any]:
    """
    Returns the data as a flat hierarchy.
    
    Note:
        Interpolations are replaced by default.
        For example :py:attr:`target_speed` and :py:attr:`max_speed` are two *different* references.
        Also with **resolve=False** the interpolation will be just a string value, as the return
        type is a normal dictionary.
    """
    try:
        resolved = cast(NestedConfigDict, OmegaConf.to_container(OmegaConf.structured(config, flags={"allow_objects" : True}),
                                                        resolve=resolve,
                                                        throw_on_missing=False,
                                                        structured_config_mode=SCMode.DICT))
    except omegaconf.errors.InterpolationToMissingValueError:
        print("Resolving has failed because a missing value has been accessed. "
                "Fill all missing values before calling this function or use `resolve=False`.")
        # NOTE: alternatively call again with resolve=False
        raise
    options: Dict[str, Any] = {}
    _flatten_dict(resolved, options, resolve=resolve)
    return options
