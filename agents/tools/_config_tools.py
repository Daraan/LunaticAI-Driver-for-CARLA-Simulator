"""
Helper Tools for :py:mod:`.config_tools`.
"""
# pyright: reportPrivateUsage=false, reportUnknownLambdaType=false, reportUnusedClass=false
# pyright: reportPossiblyUnboundVariable=information,reportAttributeAccessIssue=warning
# pyright: reportUnknownVariableType=information, reportUnknownMemberType=information

import ast
import os
import carla
import inspect
import logging

from dataclasses import is_dataclass
from enum import IntEnum

import omegaconf.errors
from omegaconf import MISSING, DictConfig, ListConfig, MissingMandatoryValue, OmegaConf, SCMode
from omegaconf._utils import is_structured_config
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional, Union, cast, get_type_hints
from typing_extensions import TypeAlias, TypeVar, Self, TypeAliasType

from classes.constants import AD_RSS_AVAILABLE

if TYPE_CHECKING:
    from agents.tools.config_creation import AgentConfig

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

from hydra.core.config_store import ConfigStore
config_store = ConfigStore.instance()
"""Hydra_ 's ConfigStore instance to access config schemas."""

def register_hydra_schema(obj: type[Any], name: Optional[str]=None):
    """
    Uses Hydra's ConfigStore to register the schema of the current class in the
    :py:obj:`ConfigStore <config_store>`.
    
    See also:
        :py:func:`config_path`
    """
    if name is None:
        name = cast(str, getattr(obj, "_config_path", obj.__name__))
    config_store.store(name, OmegaConf.structured(obj, flags={"allow_objects" : True}), 
                       provider="agents.tools.config_creation", group=None, package=None)

def config_path(path: Optional[str] = None):
    """
    Decorator to register the schema of the current class with Hydra's ConfigStore.
    
    Returns 
        (Callable[[type[AgentConfig]], type[AgentConfig]]) Wrapper function to register the schema.
    """
    
    if not READTHEDOCS:
    
        def _register(obj : "type[_AC]") -> "type[_AC]":  # pyright: ignore[reportRedeclaration]
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
        def _register(obj : "type[_AC]") -> "type[_AC]":
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

# ----- Type Annotations -----

ConfigType = TypeVar("ConfigType", DictConfig, "AgentConfig")
"""
Generic of an object that is a :py:class:`omegaconf.DictConfig` 
or a subclass of :py:class:`AgentConfig`.
"""

_T = TypeVar("_T")
_M = TypeVar("_M", Dict[str, Any], DictConfig)
"""A generic type variable for a mapping type."""

_AC = TypeVar("_AC", bound="AgentConfig")
"""A agent config type variable"""
    

ConfigDict = TypeAliasType("ConfigDict", _AC, type_params=(_AC,))
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
    from omegaconf.basecontainer import BaseContainer
    # More informative types when type checking; need primitive types at runtime
    DictConfigAlias : TypeAlias = Union[DictConfig, NestedConfigDict]
    OverwriteDictTypes : TypeAlias = Dict[str, Union[Dict[str, NestedConfigDict], "AgentConfig"]]
    
    class _DictConfigLike(BaseContainer):
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
    _DictConfigLike = object


# Boost.Python.enum cannot be used as annotations for omegaconf, replacing them by real enums,
# Functional API is easier to create but cannot be used as type hints
if AD_RSS_AVAILABLE:
    RssRoadBoundariesModeAliasX = IntEnum("RssRoadBoundariesModeAlias",  # pyright: ignore[reportRedeclaration]
                                         {str(name):value for value, name in carla.RssRoadBoundariesMode.values.items()}, module=__name__) 
    RssLogLevelAliasX = IntEnum("RssLogLevelAlias",      # pyright: ignore[reportRedeclaration]
                               {str(name):value for value, name in carla.RssLogLevel.values.items()}, module=__name__)
    """Enum for RSS Road Boundaries Mode"""

    for value, name in carla.RssRoadBoundariesMode.values.items():
        assert RssRoadBoundariesModeAliasX[str(name)] == value   # pyright: ignore[reportIndexIssue]
        
    for value, name in carla.RssLogLevel.values.items():
        assert RssLogLevelAliasX[str(name)] == value             # pyright: ignore[reportIndexIssue]
else:
    # primitive type at runtime without RSS
    RssLogLevelAliasX = Union[int, str]
    RssRoadBoundariesModeAliasX = Union[int, str, bool]
    


class __CarlaIntEnum(IntEnum):
    """
    CARLA's Enums have a `values` entry that is not part of the python enum.Enum class.
    This abstract class adds this method.
    """
        
    values : ClassVar[Dict[int, Self]]
    names  : ClassVar[Dict[str, Self]]
    
    def __init_subclass__(cls):
        cls.values : dict[int, cls]
        cls.names  : dict[str, cls]
    
class RssLogLevelStub(__CarlaIntEnum):
    """Enum declaration used in carla.RssSensor to set the log level."""
    trace = 0
    debug = 1
    info = 2
    warn = 3
    err = 4
    critical = 5
    off = 6
    
class RssRoadBoundariesModeStub(__CarlaIntEnum):
    """
    Enum declaration used in carla.RssSensor to enable or disable the stay on road feature. 
    In summary, this feature considers the road boundaries as virtual objects.
    The minimum safety distance check is applied to these virtual walls, 
    in order to make sure the vehicle does not drive off the road. 
    """
    Off = 0
    On = 1

if AD_RSS_AVAILABLE:
    for value, name in carla.RssRoadBoundariesMode.values.items():
        assert RssRoadBoundariesModeStub[str(name)] == value
        
    for value, name in carla.RssLogLevel.values.items():
        assert RssLogLevelStub[str(name)] == value
    
if TYPE_CHECKING:
    RssLogLevelAlias: TypeAlias = Union[carla.RssLogLevel, RssLogLevelStub]
    RssRoadBoundariesModeAlias: TypeAlias = Union[carla.RssRoadBoundariesMode, RssRoadBoundariesModeStub]
# Correct at Runtime, correct time needed for OmegaConf
elif AD_RSS_AVAILABLE:
    RssLogLevelAlias = carla.RssLogLevel
    RssRoadBoundariesModeAlias = carla.RssRoadBoundariesMode
else:
    RssLogLevelAlias = RssLogLevelStub
    RssRoadBoundariesModeAlias = RssRoadBoundariesModeStub

# Non type variant
if AD_RSS_AVAILABLE:
    RssLogLevel = carla.RssLogLevel
    RssRoadBoundariesMode = carla.RssRoadBoundariesMode
else:
    RssLogLevel = RssLogLevelStub
    RssRoadBoundariesMode = RssRoadBoundariesModeStub



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
                    except:
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
            
# --------------- Other Tools -----------------

def set_container_type(base: "type[AgentConfig]", container : Union[NestedConfigDict, "AgentConfig"]):
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
            if OmegaConf.get_type(value) == dict: # but is not
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
                

        
def _flatten_dict(source : NestedConfigDict, target : NestedConfigDict, resolve : bool=False):
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
