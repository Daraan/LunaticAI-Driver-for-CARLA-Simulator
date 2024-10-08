"""
This module creates type-hint schemas for the Hydra and OmegaConf backend.

Note:
    The `conf/agent/default_settings.yaml` file is automatically created
    when this file runs.
"""

# pyright: reportAttributeAccessIssue=warning
# pyright: reportCallIssue=warning
# pyright: reportInvalidStringEscapeSequence=false
# pyright: reportPrivateUsage=false
# pyright: reportSelfClsParameterName=false
# pyright: reportAbstractUsage=false
from __future__ import annotations as _

import inspect
import logging
import os
import sys
from copy import deepcopy
from dataclasses import dataclass, field, is_dataclass
from functools import partial
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional, Tuple, Type, Union, cast, get_type_hints

import carla
from hydra.conf import HydraConf

# ---- Typing ----
# SI and II are for type-hinting interpolation strings
# II : Equivalent to ${interpolation}
# SI [StringInterpolation] : Use this for String interpolation, for example "http://${host}:${port}"
from omegaconf import II, SI, DictConfig, ListConfig, OmegaConf
from omegaconf.errors import InterpolationKeyError
from typing_extensions import Annotated, Literal, Never, Self, TypeAlias, overload

# Type Annotations and Helpers
from agents.tools._config_tools import (  # Type Alias & special objects
    MT,
    _NOTSET,
    _T,
    AsDictConfig,
    ConfigType,
    DictConfigAlias,
    DictConfigLike,
    NestedConfigDict,
    OverwriteDictTypes,
    # OmegaConf tools
    config_path,
    config_store,
    # Export tools
    export_options,
    set_readonly_interpolations,
    set_readonly_keys,
    to_yaml,
)
from agents.tools._config_tools import (
    MISSING as _MISSING,
)
from agents.tools.hints import CameraBlueprint
from agents.tools.logs import logger
from classes.constants import (
    AD_RSS_AVAILABLE,
    READTHEDOCS,
    Phase,
    RoadOption,
    # Correct runtime versions, Stub or carla.RssLogLevel
    RssLogLevel,
    # Union Types for both cases
    RssLogLevelAlias,
    RssRoadBoundariesMode,
    RssRoadBoundariesModeAlias,
    RulePriority,
)
from classes.rss_visualization import RssDebugVisualizationMode
from launch_tools import class_or_instance_method

if TYPE_CHECKING:
    from agents.leaderboard_agent import LunaticChallenger
    from classes.rule import Rule
    from classes.worldmodel import GameFramework

__all__ = [
    "AgentConfig",
    "AsDictConfig",
    "AutopilotBehavior",
    "BasicAgentSettings",
    "BehaviorAgentSettings",
    "CallFunctionFromConfig",
    "CameraConfig",
    "ContextSettings",
    "CreateRuleFromConfig",
    "LaunchConfig",
    "LunaticAgentSettings",
    "RssLogLevel",
    "RssRoadBoundariesMode",
    "RuleConfig",
    "config_store",
]

if sys.version_info < (3, 9):
    # fix for typing.get_type_hints when OmegaConf.structured is used with nested dataclasses
    __original_config_path = config_path
    def config_path(path: Optional[str] = None):
        decorator = __original_config_path(path)

        def wrapper(cls: type):
            globals()[cls.__name__] = cls  # add to globals
            return decorator(cls)
        return wrapper


# ---------- Globals --------------

_WARN_LIVE_INFO = True
"""Warn about a possibly malformed live_info in the config."""

_file_path = __file__
"""
__file__ alias of this module. used for YAML comments.
Modify this variable if a config from a different file should be parsed.

.. deprecated::
    Will take the file of the object automatically
"""

if READTHEDOCS and not TYPE_CHECKING:
    # Import and usage with sphinx imported-members does not work
    from typing_extensions import TypeAliasType

    # annotate MISSING instead of ???
    MISSING: Any = _MISSING  # type: ignore
    """
    Alias for :py:obj:`omegaconf.MISSING`, is literally :python:`"???"` but has type :python:`Any`.

    If an attribute with this value is accessed from a :py:class:`DictConfig`,
    it will raise a :py:exc:`MissingMandatoryValue` error.
    
    :meta hide-value:
    """

    # prevent unpack of nested types
    NestedConfigDict = TypeAliasType(
        "NestedConfigDict", dict[str, "AgentConfig | DictConfig | Any |  NestedConfigDict"]
    )
    """
    Alias for nested configurations: :python:`Dict[str, NestedConfigDict | AgentConfig | DictConfig | Any]`

    :meta hide-value:
    """
    __all__.insert(0, "MISSING")  # type: ignore
    __all__.insert(1, "NestedConfigDict")  # type: ignore
else:
    from omegaconf import MISSING  # type: ignore


# ---------------------
# Base Classes
# ---------------------


class AgentConfig(DictConfigLike if TYPE_CHECKING else object):
    """
    Base interface for the agent settings.
    
    Handling the initialization from a nested dataclass and merges in the changes
    from the overwrites options.
    """
    
    _config_path: ClassVar[Optional[str]] = "NOT_GIVEN"
    """
    The key, relative to the LaunchConfig, where the config is stored.

    Create subclasses like:
    
    .. code-block:: python
    
        @config_path("agent/speed")
        @dataclass
        class AgentSpeedSettings(AgentConfig):
        
    Attention:
        - Use "/" as separator and not dots.
        - This is used for the Hydra schema registration and repeated paths will overwrite each other.
        - This value is inherited (if != :code:`NOT_GIVEN`), and the value of the parent is taken
          as default. Do not type-hint this value it must be a ClassVar to not conflict with dataclasses.
        
    :meta private:
    """
    
    overwrites: "Optional[NestedConfigDict]" = None
    """Overwrites of nested dictionaries for used for the initialization of the config."""
    
    @classmethod
    def get_defaults(cls) -> "Self":
        """Returns the global default options."""
        return cls()  # type: ignore[call-arg]
    
    @class_or_instance_method
    def export_options(
        cls_or_self: Union[Type[Self], Self],
        path: Union[str, "os.PathLike[str]"],
        *,
        resolve: bool = False,
        with_comments: bool = False,
        detailed_rules: bool = False,
        include_private: bool = False,
    ) -> None:
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
        export_options(
            cls_or_self,
            path,
            resolve=resolve,
            with_comments=with_comments,
            detailed_rules=detailed_rules,
            include_private=include_private,
        )

    @class_or_instance_method
    def to_yaml(
        cls_or_self: Union[Type[Self], Self],
        resolve: bool = False,
        yaml_commented: bool = True,
        detailed_rules: bool = False,
        *,
        include_private: bool = False,
    ) -> str:
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
        return to_yaml(
            cls_or_self,
            resolve=resolve,
            yaml_commented=yaml_commented,
            detailed_rules=detailed_rules,
            include_private=include_private,
        )

    @classmethod
    def from_yaml(cls, path: str, *, merge: bool = True) -> Self:
        """
        Loads the options from a yaml file.
        
        Args:
            path: The path to the yaml file.
            merge: Merges the loaded yaml into the base class settings. Otherwise returns
                   the settings as they are in the file.
                   Defaults to True.
        
        Returns:
            AgentConfig: An instance of this class
        """
        loaded = OmegaConf.load(path)
        if not merge:
            return cast(cls, loaded)
        options = OmegaConf.merge(OmegaConf.structured(cls, flags={"allow_objects": True}), loaded)
        return cast(cls, options)
    
    @classmethod
    def load_schema(cls, path: Optional[str] = None) -> AsDictConfig[Self]:
        """
        Classes decorated with :py:func:`@config_path <.config_path>` can be loaded with this method.
        
        This is equivalent to:
            create(as_dictconfig=True, dict_config_no_parent=False)
        
        See Also:
            Hydra_ ConfigStore
            
        :meta private:
        """
        path = path or cls._config_path
        if path is None:
            raise ValueError("No path to the schema provided and the class has not been created with `@config_path`.")
        return cast(cls, config_store.load(path).node)
    
    @classmethod
    def create(
        cls,
        settings: "Union[os.PathLike[str], str, DictConfig, NestedConfigDict | AgentConfig, None]" = None,
        overwrites: "Optional[NestedConfigDict]" = None,
        *,
        assure_copy: bool = True,
        as_dictconfig: Optional[bool] = True,
        dict_config_no_parent: bool = True,
    ) -> "Self | AsDictConfig[Self]":
        r"""
        Creates the agent settings based on the provided arguments.
        
        Note:
            By default this returns a DictConfig version of this class.

        Parameters:
            settings : The argument specifying the agent settings. It can be a path to a YAML file, a dictionary, a
                   :external-icon-parse:`:py:mod:\`@dataclass <dataclasses>\`` decorated class or a :external-icon-parse:`:py:class:\`omegaconf.DictConfig\``.
            overwrites : Optional mapping containing additional settings to overwrite the default agent settings.
            as_dictconfig :

                - If True, the agent settings are returned as a :py:class:`DictConfig`.
                - If False, the agent settings are returned as an instance of this class.
                - If None, the return type is determined by the type of the args and other arguments
                  i.e. if args is a :py:class:`DictConfig` and assure_copy is False, the
                  original input is checked and returned.

        Returns:
            :py:class:`AgentConfig` (duck-typed); actually :external-icon-parse:`:py:class:\`omegaconf.DictConfig\``): The created agent settings.

        Raises:
            Exception: If the overwrites cannot be merged into the agent settings.
        """

        behavior: cls
        if settings is None:
            if not as_dictconfig:
                behavior = cls(overwrites=settings) if cls.uses_overwrite_interface() else cls(**settings)
            else:
                behavior = cls.load_schema()
        if isinstance(settings, (str, os.PathLike)):
            # load yaml file
            logger.info("Using agent settings from file `%s`", settings)
            behavior = cls.from_yaml(settings)  # DictConfig  # type: ignore[attr-type]
        elif isinstance(settings, dict):
            logger.debug(
                "Using agent settings from dict with LunaticAgentSettings. Note settings are NOT a dict config. Interpolations not available."
            )
            behavior = cls(overwrites=settings) if cls.uses_overwrite_interface() else cls(**settings)  # type: ignore[attr-type]
        elif is_dataclass(settings) or isinstance(settings, DictConfig):
            logger.debug("Using agent settings as is, as it is a dataclass or DictConfig.")
            # clean_settings = {k : v for k, v in settings.items() if not OmegaConf.is_missing(v)}
            if assure_copy:
                behavior = cls(overwrites=settings) if cls.uses_overwrite_interface() else cls(**settings)
            elif inspect.isclass(settings):
                behavior = settings()
            else:
                # instantiate class to check keys but use original type
                cls(overwrites=settings) if cls.uses_overwrite_interface() else cls(
                    **settings
                )  # convert to class to check keys
                behavior = settings  # stays duck-typed DictConfig # type: ignore
        else:
            if as_dictconfig is None:
                logger.warning(
                    "Type `%s` of launch argument type `agent_settings` not supported, trying to use it anyway. Expected are (str, dataclass, DictConfig)",
                    type(settings),
                )
            if inspect.isclass(settings):
                behavior = settings()  # be sure to have an instance
            if assure_copy:
                behavior = cls(overwrites=settings) if cls.uses_overwrite_interface() else cls(**settings)
            else:
                # instantiate to class to check keys but use original type
                cls(overwrites=settings) if cls.uses_overwrite_interface() else cls(**settings)
                behavior = settings  # has Unknown type but keys are present # type: ignore
        
        if overwrites:
            if isinstance(behavior, DictConfig):
                behavior = cls.cast(
                    OmegaConf.merge(behavior, OmegaConf.structured(overwrites, flags={"allow_objects": True}))
                )
            else:
                try:
                    behavior.merge_with(overwrites)
                except Exception:
                    logger.error(
                        "Overwrites could not be merged into the agent settings with `base_config.update(overwrites)`. Passing config_mode=True might help."
                    )
                    raise
        if as_dictconfig and not isinstance(behavior, DictConfig):
            try:
                behavior = OmegaConf.structured(behavior, flags={"allow_objects": True})
            except Exception as e:
                print(e)
                # breakpoint()
                raise
        elif as_dictconfig is False and isinstance(behavior, DictConfig):
            return cls(overwrites=settings) if cls.uses_overwrite_interface() else cls(**settings)  # pyright: ignore[reportCallIssue]
        elif as_dictconfig is None:
            logger.debug(
                "A clear return type of %s.create_from_args has not set as config_mode is None. Returning as %s",
                cls.__name__,
                type(behavior),
            )

        if isinstance(behavior, DictConfig):
            behavior._set_flag("allow_objects", True)
            if dict_config_no_parent:
                # Dict config interpolations always use the full path, interpolations might go from the root of the config.
                # If there is launch_config.agent, with launch config as root, the interpolations will not work.
                behavior.__dict__["_parent"] = None  # Remove parent from the config, i.e. make it a top-level config.
        
        return cast(cls, behavior)
    
    @overload
    @classmethod
    def check_config(
        cls, config: MT, strictness: "Literal[0, False]", as_dict_config: "Literal[False]"
    ) -> MT: ...

    @overload
    @classmethod
    def check_config(
        cls, config: ConfigType, strictness: "Literal[0, False]", as_dict_config: "Literal[True]"
    ) -> ConfigType: ...

    @overload
    @classmethod
    def check_config(cls, config: ConfigType, strictness: int, as_dict_config: "Literal[True]") -> Self: ...
    
    @classmethod
    def check_config(
        cls, config: "ConfigType | MT | NestedConfigDict", strictness: int = 1, as_dict_config: bool = True
    ) -> "Self | ConfigType | MT":
        """
        - :python:`strictness == 1` type-cast the config to this class, assuring all keys are present.
          However the type and correctness of the field-contents are not checked.
        - :python:`strictness > 1` the config will be a :external_py_class:`DictConfig` object.
          **as_dict_config** is ignored.
        - :python:`strictness == 2`: Will assure that the *initial* types are correct.
        - :python:`strictness >= 2` will return the config as a structured config, forcing the
          defined types during runtime as well.
          
        Attention:
            Type-forcing for more complex types does not work, e.g. types from the :py:mod:`carla` module,
            this especially includes carla's enum objects.
            For what is supported see https://omegaconf.readthedocs.io/en/2.3_branch/structured_config.html.
            
        Parameters:
            config: The configuration to check against this class
            
        Args:
            strictness: See above. Defaults to 1.
            as_dict_config: Whether to return a duck-typed :external_py_class:`DictConfig`
                            instead of an instance of this class.
                            Defaults to :python:`True`.
            
        Returns:
            A version of this class or a duck-typed :external_py_class:`DictConfig`.
        """
        if "experiments" in config and not hasattr(cls, "experiments"):  # For LaunchConfig
            print(
                "\nWARNING: There is key 'experiments' in the config. Did you forget a '# @package _global_' in the first line? Keys in experiments: %s",
                config["experiments"].keys(),
            )
        if strictness <= 0:
            if as_dict_config and not isinstance(config, DictConfig):
                new_config0: MT = OmegaConf.structured(config, flags={"allow_objects": True})
                return new_config0
            return cast(MT, config)
        if strictness == 1:
            new_config = cls(**config)
            if as_dict_config and not isinstance(config, DictConfig):
                return cls.cast(OmegaConf.structured(new_config, flags={"allow_objects": True}))
            return new_config
        # TODO: # Note: This does not assure missing keys:
        new_config = cls.create(config, as_dictconfig=True, assure_copy=False)
        if strictness == 2:
            if as_dict_config and not isinstance(new_config, DictConfig):
                return cast(cls, OmegaConf.structured(new_config, flags={"allow_objects": True}))
            return new_config
        new_config: cls = OmegaConf.structured(new_config, flags={"allow_objects": True})  # include flag, yes no?
        return new_config
    
    if READTHEDOCS and not TYPE_CHECKING:
        # simplify signature for online
        check_config.__wrapped__.__annotations__ = check_config.__annotations__ = {"config": "NestedConfigDict", 'strictness': 'int', 'as_dict_config': 'bool', "return": "Self"}  # pylint: disable=protected-access, line-too-long
        
    @class_or_instance_method
    def to_dict_config(
        cls_or_self: Union[Type[Self], Self],
        *,
        lock_interpolations: bool = True,
        lock_fields: Optional[List[str]] = None,
    ) -> DictConfig:
        r"""
        Returns a :external-icon-parse:`:py:class:\`omegaconf.DictConfig\`` from the current options.
        
        Interpolations can be locked to prevent them from being overwritten.
        E.g. :code:`speed.current_speed` cannot diverge from :code:`live_info.current_speed`.
        
        Parameters:
            lock_interpolations: Whether to set interpolations to readonly. Defaults to :python:`True`.
            lock_fields: A list of fields to set to readonly. Defaults to :python:`None`.
            
        Returns:
            :py:class:`AgentConfig` (duck-typed); actually :external-icon-parse:`:py:class:\`omegaconf.DictConfig\``) : The options as a :py:class:`DictConfig`.
        """
        options = cls_or_self
        conf = OmegaConf.structured(options, flags={"allow_objects": True})
        # This pre
        if lock_interpolations:
            set_readonly_interpolations(conf)
        if lock_fields:
            set_readonly_keys(conf, lock_fields)
        return conf
    
    def copy(self) -> "Self":
        """Returns a deep copy of this object."""
        return deepcopy(self)

    @class_or_instance_method
    def get(cls_or_self: Union[Type[Self], Self], key: str, default: _T = _NOTSET) -> "Any | _T":
        """
        Analog of :py:func:`.getattr`.
        
        Raises:
            AttributeError: If the **key** is not found and no **default** is provided.
        """
        if default is _NOTSET:
            return getattr(cls_or_self, key)
        return getattr(cls_or_self, key, default)
    
    def update(self, options: "Union[NestedConfigDict, DictConfig, AgentConfig]", clean: bool = True) -> None:
        """
        Updates the options with a new dictionary. Will call :py:meth:`update` recursively
        for nested :py:class:`AgentConfig` objects.
        
        Parameters:
            options: The new options to update with.
            clean: Whether to call :py:meth:`_clean_options` after updating. Defaults to True.
        """
        try:
            if is_dataclass(options):  # instance of AgentConfig
                key_values = options.__dataclass_fields__.items()
            elif isinstance(options, DictConfig):
                key_values = options.items_ex(resolve=False)  # Calling this with missing keys will raise an error
            else:
                key_values = options.items()  # type: ignore
            
            for k, v in key_values:
                if isinstance(getattr(self, k), AgentConfig):  # pyright: ignore[reportArgumentType], k is str
                    getattr(self, k).update(v)                 # pyright: ignore[reportArgumentType]
                else:
                    setattr(self, k, v)                        # pyright: ignore[reportArgumentType]
            if clean:
                self._clean_options()
        except Exception as e:
            print("\n ERROR updating", self.__class__.__name__, "with >", options, "< Error:", e, "\n")
            raise
        
    @classmethod
    def uses_overwrite_interface(cls) -> bool:
        """
        Whether or not the class is created by a single parameter "overwrites"
        or via keyword arguments for each field.
        """
        return "overwrites" in inspect.signature(cls.__init__).parameters
    
    @classmethod
    def cast(cls, value: Any):
        """Type-hinting method to cast a value to this class."""
        return cast(cls, value)
    
    def _clean_options(self):
        """
        Postprocessing of possibly wrong values
        
        :meta public:
        """
        return

    def __post_init__(self):
        """
        Assures that if a dict is passed the values overwrite the defaults.
        
        # NOTE: Will be used for dataclass derived children
        """
        self._clean_options()
        if self.overwrites is None:
            return
        assert is_dataclass(self)
        #if isinstance(self.overwrites, DictConfig):
        #    self.overwrites = OmegaConf.to_container(self.overwrites, throw_on_missing=False) # convert to dict
        # Merge the overwrite dict into the correct ones.
        
        # Handle the overwrites
        try:
            value: Union[NestedConfigDict, AgentConfig, DictConfig, str, bool, float, int, list[Any], ListConfig, None, Literal["None"]]  # noqa: PYI051 # literal and str
            annotations = get_type_hints(self.__class__)
            for key in self.overwrites.keys():
                if key in annotations:  # This is "overwrites" -> to "self"
                    # retrieve safe value
                    if isinstance(self.overwrites, DictConfig):
                        if OmegaConf.is_missing(self.overwrites, key):
                            logging.debug("%s is MISSING, keeping as it is", key)
                            setattr(self, key, MISSING)
                            continue
                        if OmegaConf.is_interpolation(self.overwrites, key):
                            # Take interpolation as is
                            logging.debug("%s is an interpolation, keeping as it is", key)
                            value = self.overwrites._get_node(key)._value()  # pyright: ignore[reportOptionalMemberAccess]
                            setattr(self, key, value)
                            continue
                    value = self.overwrites[key]
                    
                    # Special cases
                    if key == "current_rule":
                        if value != ContextSettings.current_rule:
                            logging.warning(
                                "Overwriting `current_rule` with %s. Expecting interpolation '%s'",
                                value,
                                ContextSettings.current_rule,
                            )
                    elif key == "overwrites":
                        if value:
                            logging.error(
                                "A non-empty overwrites key should not be set in the overwrites dict. Ignoring it"
                            )
                    elif key == "rules":
                        setattr(self, key, value)  # value is a list
                    elif key == "live_info":
                        if TYPE_CHECKING:
                            assert isinstance(value, LiveInfo)
                        live_info_dict: LiveInfo = self.live_info  # type: ignore[attr-defined]
                        for live_info_key in value.keys():
                            if _WARN_LIVE_INFO and not OmegaConf.is_missing(value, live_info_key):
                                logging.warning("WARNING: live_info should only consist of missing values. "
                                                "Setting %s to %s", live_info_key, value[live_info_key])
                                setattr(live_info_dict, live_info_key, value[live_info_key])  # type: ignore[attr]
                    # Delegate False to a subfield
                    elif self.__dataclass_fields__[key].metadata.get("can_be_false", False) and value in (False, None, "None", True):
                        # redirect to .enabled subkey.
                        if value in (False, None, "None"):
                            # Rss or Datamatrix settings
                            getattr(self, key).update({"enabled": False})
                        elif value is True:
                            getattr(self, key).update({"enabled": True})
                    # NOTE: Do not use Union keys with AgentConfig, else this will throw an error
                    elif issubclass(annotations[key], AgentConfig):
                        getattr(self, key).update(value)  # AgentConfig.update
                    else:
                        logging.debug(
                            "%s : %s is not a Config or annotated as AgentConfig", key, value
                        )  # this does normally not happen
                        setattr(self, key, value)
                else:
                    logging.error(
                        "ERROR: Key '%s' not found in %s default options. Consider updating or creating a new class to avoid this message.",
                        key, self.__class__.__name__
                    )
        except InterpolationKeyError:
            logging.exception("Interpolation error")
            print("Interpolation error in", self.__class__.__name__)
            # breakpoint()
            raise
        except Exception as e:
            logging.exception("Error")
            print("\n\nError updating", self.__class__.__name__, "key:", key, "value:", value, "Error:", e)  # type: ignore
            #breakpoint()
            raise


# ---------------------

# ---------------------
# Live Info
# ---------------------


@config_path("agent/live_info")
@dataclass
class LiveInfo(AgentConfig):
    """
    .. @package agent.live_info
    
    Keeps track of information that changes during the simulation.
    """
    
    velocity_vector: carla.Vector3D = MISSING
    """
    3D Vector of the current velocity of the vehicle.
    """
    
    current_speed: float = MISSING
    """
    Velocity of the vehicle in km/h.
    
    Note:
        The `z` component is ignored.
    """
    
    current_transform: carla.Transform = MISSING
    current_location: carla.Location = MISSING
    
    current_speed_limit: float = MISSING
    
    executed_direction: RoadOption = MISSING
    """
    Direction that was executed in the last step by the local planner
    
    planner.target_road_option is the option last executed by the planner (constant)
    incoming direction is the next *planned* direction subject to change (variable)
    """
    
    incoming_direction: RoadOption = MISSING
    """
    RoadOption that will used for the current step
    """
    
    incoming_waypoint: Optional[carla.Waypoint] = MISSING
    """
    Waypoint that is planned to be targeted in this step.
    """
    
    is_taking_turn: bool = MISSING
    """
    incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)
    """
    
    is_changing_lane: bool = MISSING
    """
    incoming_direction in (RoadOption.CHANGELANELEFT, RoadOption.CHANGELANERIGHT)
    """
    
    next_traffic_light: Union[carla.TrafficLight, None] = MISSING
    """
    Traffic light that is closest to the next intersection.
    
    Is `None` if the agent is at an intersection.
    
    + NOTE: This might not be in the path or infront of the vehicle.
    """
    
    next_traffic_light_distance: Union[float, None] = MISSING
    """
    Distance to the assumed next traffic light.
    """
    
    last_applied_controls: carla.VehicleControl = MISSING
    """
    :py:class:`carla.VehicleControl` that was applied in the last step.
    """
    
    # NOTE: Not ported to OmegaConf
    @property
    def speed(self):
        return self.current_speed

    @property
    def speed_limit(self):
        return self.current_speed_limit
    
    # NOTE: not wr
    #current_speed : float = II(".speed") # alias for convenience
    #current_speed_limit : float = II(".speed_limit")

# ---------------------
# Speed
# ---------------------


@dataclass
class BasicAgentSpeedSettings(AgentConfig):
    current_speed: float = II("live_info.current_speed")
    """This is a reference to live_info.current_speed, which is updated by the agent"""
    
    current_speed_limit: float = II("live_info.current_speed_limit")
    """This is a reference to live_info.current_speed_limit, which is updated by the agent"""
    
    target_speed: float = 20
    """desired cruise speed in Km/h; overwritten by SpeedLimit if follow_speed_limit is True"""
    
    follow_speed_limits: bool = False
    """If the agent should follow the speed limit. *NOTE:* SpeedLimit overwrites target_speed if True (local_planner.py)"""


@dataclass
class BehaviorAgentSpeedSettings(BasicAgentSpeedSettings):
    """
    The three situations they adjust their speed; # SEE: `behavior_agent.car_following_manager`
    
    Case A car in front and getting closer : slow down; slower than car in front
          Take minium from, speed decrease, speed limit adjustment and target_speed
          `target_speed` = min( other_vehicle_speed - self._behavior.speed_decrease, # <-- slow down BELOW the other car
                              self._behavior.max_speed # use target_speed instead
                              self._speed_limit - self._behavior.speed_lim_dist])
    Case B car in front but safe distance : match speed
          `target_speed` = min([
                    max(self._min_speed, other_vehicle_speed),  # <- match speed
                    self._behavior.max_speed,
                    self._speed_limit - self._behavior.speed_lim_dist])
    Case C front is clear
          `target_speed` = min([
                    self._behavior.max_speed,
                    self._speed_limit - self._behavior.speed_lim_dist])
    """
    # DEPRECATED:  deprecated max_speed use target_speed instead   # NOTE: Behavior agents are more flexible in their speed.
    max_speed: float = 50
    """The maximum speed in km/h your vehicle will be able to reach.
    From normal behavior. This supersedes the target_speed when following the BehaviorAgent logic."""
    
    # CASE A
    speed_decrease: float = 10
    """other_vehicle_speed"""
    
    safety_time: float = 3
    """Time in s before a collision at the same speed -> apply speed_decrease"""

    # CASE B
    min_speed: float = 5
    """Implement als variable, currently hard_coded"""

    # All Cases
    speed_lim_dist: float = 3
    """
    Difference to speed limit.
    NOTE: For negative values the car drives above speed limit
    """

    intersection_speed_decrease: float = 5.0
    """Reduction of the targeted_speed when approaching an intersection"""


@dataclass
class AutopilotSpeedSettings(AgentConfig):
    vehicle_percentage_speed_difference: float = 30  # in percent
    """
    Sets the difference the vehicle's intended speed and its current speed limit.
    Speed limits can be exceeded by setting the percentage to a negative value.
    Default is 30.
    
    Exceeding a speed limit can be done using negative percentages.
    """


@config_path("agent/speed")
@dataclass
class LunaticAgentSpeedSettings(AutopilotSpeedSettings, BehaviorAgentSpeedSettings):
    vehicle_percentage_speed_difference: float = MISSING  # 30
    """
    TODO: Port from traffic manager.
    
    Sets the difference the vehicle's intended speed and its current speed limit.
    Speed limits can be exceeded by setting the perc to a negative value.
    Default is 30.
    Exceeding a speed limit can be done using negative percentages.
    """
    
    intersection_target_speed: float = SI(
        "${min:${.max_speed}, ${sub:${.current_speed_limit}, ${.intersection_speed_decrease}}}"
    )
    """Formula or value to calculate the target speed when approaching an intersection"""


# ---------------------
# Distance
# ---------------------


@dataclass
class BasicAgentDistanceSettings(AgentConfig):
    pass


@dataclass
class BehaviorAgentDistanceSettings(BasicAgentDistanceSettings):
    """
    Collision Avoidance
    -------------------

    Distance in which for vehicles are checked.
    
    Usage: max_distance = max(min_proximity_threshold, self._speed_limit / (2 if <LANE CHANGE> else 3 ) )
    """
    
    emergency_braking_distance: float = 5
    """Emergency Stop Distance Trigger"""
    

@dataclass
class AutopilotDistanceSettings(AgentConfig):
    distance_to_leading_vehicle: float = 5.0
    """
    Sets the minimum distance in meters that a vehicle has to keep with the others.
    The distance is in meters and will affect the minimum moving distance. It is computed from front to back of the vehicle objects.
    """


@config_path("agent/distance")
@dataclass
class LunaticAgentDistanceSettings(AutopilotDistanceSettings, BehaviorAgentDistanceSettings):
    distance_to_leading_vehicle: float = MISSING  # 5.0
    """
    PORT from TrafficManager # TODO:
    
    Sets the minimum distance in meters that a vehicle has to keep with the others.
    The distance is in meters and will affect the minimum moving distance. It is computed from front to back of the vehicle objects.
    """


# ---------------------
# Lane Change
# ---------------------


@dataclass
class BasicAgentLaneChangeSettings(AgentConfig):
    """
    Timings in seconds to finetune the lane change behavior.
    
    NOTE: see: `BasicAgent.lane_change` and `BasicAgent._generate_lane_change_path`
    """

    same_lane_time: float = 0.0
    other_lane_time: float = 0.0
    lane_change_time: float = 2.0


@dataclass
class BehaviorAgentLaneChangeSettings(BasicAgentLaneChangeSettings):
    pass


@dataclass
class AutopilotLaneChangeSettings(AgentConfig):
    auto_lane_change: bool = True
    """Turns on or off lane changing behavior for a vehicle."""
    
    random_left_lanechange_percentage: float = 0.1
    """
    Adjust probability that in each timestep the actor will perform a left/right lane change,
    dependent on lane change availability.
    """
    
    random_right_lanechange_percentage: float = 0.1
    """
    Adjust probability that in each timestep the actor will perform a left/right lane change,
    dependent on lane change availability.
    """

    keep_right_rule_percentage: float = 0.7
    """
    During the localization stage, this method sets a percent chance that vehicle will follow the keep right rule,
    and stay in the right lane.
    """


@config_path("agent/lane_change")
@dataclass
class LunaticAgentLaneChangeSettings(BehaviorAgentLaneChangeSettings):
    """
    Lane Change

    Adjust probability that in each timestep the actor will perform a left/right lane change,
    dependent on lane change availability.
    """
    
    # Moved to -> RandomLaneChangeRule
    #random_lane_change_interval : int = 200
    #"""Cooldown value for a lane change in the 'lane_change' group."""


# ---------------------
# Obstacles
# ---------------------


@dataclass
class BasicAgentObstacleDetectionAngles(AgentConfig):
    """
    Detection Angles for the BasicAgent used in the `BasicAgent._vehicle_obstacle_detected` method.
    
    The angle between the location and reference object.
    Being 0 a location in front and 180, one behind, i.e, the vector between has to satisfy:
    low_angle_th < angle < up_angle_th.
    """
    
    walkers_lane_change: Tuple[float, float] = (0.0, 90.0)
    """Detection angle of walkers when staying in the same lane"""
    
    walkers_same_lane: Tuple[float, float] = (0.0, 60.0)
    """Detection angle of walkers when changing lanes"""
    
    cars_lane_change: Tuple[float, float] = (0.0, 180.0)
    """Detection angle of cars when staying in the same lane"""
    
    cars_same_lane: Tuple[float, float] = (0.0, 30.0)
    """Detection angle of cars when changing lanes"""


@dataclass
class BasicAgentObstacleSettings(AgentConfig):
    """
    --------------------------
    Agent Level
    see :py:meth:`_affected_by_traffic_light` and :py:meth:`_affected_by_vehicle`
    in :py:mod:`basic_agent.py <agents.navigation.basic_agent>`
    --------------------------
    Agents is aware of the vehicles and traffic lights within its distance parameters
    optionally can always ignore them.
    """
    
    ignore_vehicles: bool = False
    """Whether the agent should ignore vehicles"""
    
    ignore_traffic_lights: bool = False
    """Whether the agent should ignore traffic lights"""
    
    ignore_stop_signs: bool = MISSING
    """
    Whether the agent should ignore stop signs
    
    Attention:
        No usage implemented yet.
    
    Idea:
        Nearby landmarks from waypoints need to be retrieved
        and checked for stop signs.
    """
    
    use_bbs_detection: bool = True
    """
    True: Whether to use a general approach to detect vehicles invading other lanes due to the offset.

    False: Simplified approach, using only the plan waypoints (similar to TM)
    
    See `BasicAgent._vehicle_obstacle_detected`
    """
    
    detect_yellow_tlights: bool = True
    """
    If the the agent will treat a yellow light like a red light. If False will not detect them.
    
    Rules must decide how to handle yellow lights.
    """
    
    base_tlight_threshold: float = 2.0
    """
    Base distance to traffic lights to check if they affect the vehicle
        
    Usage: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
    Usage: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed
    """
    
    base_vehicle_threshold: float = 4.0
    """
    Base distance to vehicles to check if they affect the vehicle
            
    Usage:
        Only vehicles with distance < `nearby_vehicles_max_distance` are checked for
        ```python
        max_vehicle_distance = base_vehicle_threshold
        if dynamic_threshold:
            max_vehicle_distance += detection_speed_ratio * vehicle_speed
        ```
        
        A vehicle is considered if distance < max_vehicle_distance < nearby_vehicles_max_distance
    """

    detection_speed_ratio: float = 0.1
    """
    Increases detection range based on speed
    
    Usage: max_vehicle_distance = base_vehicle_threshold + detection_speed_ratio * vehicle_speed
    Usage: max_tlight_distance  = base_tlight_threshold  + detection_speed_ratio * vehicle_speed
    """
    
    dynamic_threshold: bool = True
    """
    Whether to add a dynamic threshold based on the vehicle speed to the base threshold.
    
    Usage: base_threshold + detection_speed_ratio * vehicle_speed
    
    + NOTE: Currently only applied to traffic lights
    
    + NOTE: Part of the agent overhaul
    """
    
    detection_angles: BasicAgentObstacleDetectionAngles = field(default_factory=BasicAgentObstacleDetectionAngles)
    """Defines detection angles used when checking for obstacles."""


@dataclass
class BehaviorAgentObstacleSettings(BasicAgentObstacleSettings):
    nearby_vehicles_max_distance: float = 45
    """
    For performance filters out vehicles that are further away than this distance in meters
    
    Info:
        These vehicles are stored in `vehicles_nearby`.
    """
    
    nearby_walkers_max_distance: float = 10
    """
    For performance filters out pedestrians that are further away than this distance in meters
    
    Info:
        These pedestrians are stored in `walkers_nearby`.
    """
    
    min_proximity_threshold: float = 10
    """
    When making lane changes determines the minimum distance to check for vehicles.
    
    max_distance_check = max(obstacles.min_proximity_threshold,
                             live_info.current_speed_limit / speed_detection_downscale)
                             
    Hint:
        Lower values mean that further away vehicles are maybe not considered,
        an agent might ignore fast vehicles coming from behind in the other lane,
        or ignores slower vehicles in front of it in the other lane.
    """
    
    # Python 3.7 compatibility allows no nesting here
    @config_path("agent/obstacles/speed_detection_downscale")
    @dataclass
    class SpeedLimitDetectionDownscale(AgentConfig):
        """see `speed_detection_downscale`"""
        
        same_lane: float = 3.0
        other_lane: float = 2.0
        overtaking: float = 2.5
        """
        Used by SimpleOvertakeRule, look further ahead for overtaking
        """
        
        tailgating: float = 2
        """
        Used by AvoidTailgatorRule, look further behind for tailgators
        """

    speed_detection_downscale: SpeedLimitDetectionDownscale = field(default_factory=SpeedLimitDetectionDownscale)
    """
    When making lane changes determines the maximum distance to check for vehicles.
    
    max_distance_check = max(obstacles.min_proximity_threshold,
                             live_info.current_speed_limit / speed_detection_downscale.[same|other]_lane)
                             
    Hint:
        Higher values mean that further away vehicles are not considered,
        an agent might ignore fast vehicles coming from behind in the other lane,
        or ignores slower vehicles in front of it in the other lane.
    """
    

@dataclass
class AutopilotObstacleSettings(AgentConfig):
    ignore_lights_percentage: float = 0.0
    """
    Percentage of time to ignore traffic lights
    """
    
    ignore_signs_percentage: float = 0.0
    """
    Percentage of time to ignore stop signs
    """
    
    ignore_walkers_percentage: float = 0.0
    """
    Percentage of time to ignore pedestrians
    """
    

@config_path("agent/obstacles/detection_angles")
@dataclass
class LunaticAgentObstacleDetectionAngles(BasicAgentObstacleDetectionAngles):
    """
    Detection Angles for the BasicAgent used in the `BasicAgent._vehicle_obstacle_detected` method.
    
    The angle between the location and reference object.
    Being 0 a location in front and 180, one behind, i.e, the vector between has to satisfy:
    low_angle_th < angle < up_angle_th.
    
    Note:
        These settings are NotImplemented
    """
    
    # --------------------------
    # Note: Unused and deprecated
    # --------------------------
    
    when_turning: Tuple[float, float] = MISSING
    """Idea: When the agent is turning it might needs a wider angle to detect vehicles"""
    

@config_path("agent/obstacles")
@dataclass
class LunaticAgentObstacleSettings(AutopilotObstacleSettings, BehaviorAgentObstacleSettings):
    dynamic_threshold: bool = True
    """
    Whether to add a dynamic threshold based on the vehicle speed to the base threshold.
    
    Usage: base_threshold + detection_speed_ratio * vehicle_speed
    
    #NOTE: Currently only applied to traffic lights
    """
    
    detection_angles: LunaticAgentObstacleDetectionAngles = field(default_factory=LunaticAgentObstacleDetectionAngles)  # pyright: ignore[ reportIncompatibleVariableOverride]
    
    nearby_statics_max_distance: float = 150
    """For performance filters out statics that are further away than this distance in meters"""
    
    base_static_threshold: float = 2.0
    """
    Base distance to vehicles to check if they affect the vehicle
            
    Usage:
        static_detection_speed_ratio = base_static_threshold + static_detection_speed_ratio * vehicle_speed
    """
    
    static_detection_speed_ratio: float = 0.5
    """
    Usage:
        static_detection_speed_ratio = base_static_threshold + static_detection_speed_ratio * vehicle_speed
    """
    
    nearby_tlights_max_distance: float = II("look_ahead_time:${live_info.current_speed_limit}, 5.0, 10.0")
    """
    For performance filters out traffic lights that are further away than this distance in meters.
    
    By default checks converts the current speed to a distance of 5 seconds and adds 10 meters.
    """


# ---------------------
# ControllerSettings
# ---------------------

@dataclass
class BasicAgentControllerSettings(AgentConfig):
    """Limitations of the controls used one the PIDController Level"""
    
    max_brake: float = 0.5
    """
    Vehicle control how strong the brake is used,
    
    NOTE: Also used in emergency stop
    """
    max_throttle: float = 0.75
    """maximum throttle applied to the vehicle"""
    max_steering: float = 0.8
    """maximum steering applied to the vehicle"""
    
    # Aliases used:
    @property
    def max_throt(self):
        return self.max_throttle

    @property
    def max_steer(self):
        return self.max_steering


@dataclass
class BehaviorAgentControllerSettings(BasicAgentControllerSettings):
    pass


@dataclass
class AutopilotControllerSettings(AgentConfig):
    vehicle_lane_offset: float = 0
    """
    Sets a lane offset displacement from the center line. Positive values imply a right offset while negative ones mean a left one.
    Default is 0. Numbers high enough to cause the vehicle to drive through other lanes might break the controller.
    """
    

@config_path("agent/controls")
@dataclass
class LunaticAgentControllerSettings(AutopilotControllerSettings,
                                     BehaviorAgentControllerSettings):
    pass

# ---------------------
# PlannerSettings
# ---------------------


@dataclass
class PIDControllerDict(AgentConfig):
    """
    PID controller using the following semantics:
        K_P -- Proportional term
        K_D -- Differential term
        K_I -- Integral term
        dt -- time differential in seconds
    """
            
    K_P: float = MISSING
    K_D: float = MISSING
    K_I: float = 0.05
    dt: float = 1.0 / 20.0
    """time differential in seconds"""


@dataclass
class BasicAgentPlannerSettings(AgentConfig):
    """
    PID controller using the following semantics:
            K_P -- Proportional term
            K_D -- Differential term
            K_I -- Integral term
            dt -- time differential in seconds
    offset: If different than zero, the vehicle will drive displaced from the center line.
    Positive values imply a right offset while negative ones mean a left one.
    Numbers high enough to cause the vehicle to drive through other lanes might break the controller.
    
    Notes:
    `sampling_resolution` is used by the global planner to build a graph of road segments, also to get a path of waypoints from A to B

    `sampling_radius` is similar but only used only by the local_planner to compute the next waypoints forward. The distance of those is the sampling_radius.
    
    """
    
    dt: float = 1.0 / 20.0
    """time differential in seconds"""

    # NOTE: two variables because originally used with two different names in different places
    #lateral_control_dict : PIDControllerDict = field(default_factory=partial(PIDControllerDict, **{'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2}))
    lateral_control_dict: PIDControllerDict = field(default_factory=lambda: PIDControllerDict(**{'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2}))
    """values of the lateral PID controller"""

    # NOTE: two variables because originally used with two different names in different places
    longitudinal_control_dict: PIDControllerDict = field(default_factory=lambda: PIDControllerDict(**{'K_P': 1.0, 'K_I': 0.05, 'K_D': 0}))
    """values of the longitudinal PID controller"""
    
    offset: float = 0.0
    """
    If different than zero, the vehicle will drive displaced from the center line.
    
    Positive values imply a right offset while negative ones mean a left one. Numbers high enough
    to cause the vehicle to drive through other lanes might break the controller.
    """
    
    sampling_radius: float = 2.0
    """
    Distance between waypoints when planning a path in `local_planner._compute_next_waypoints`
    
    Used with Waypoint.next(sampling_radius)
    """
    
    sampling_resolution: float = 2.0
    """
    Distance between waypoints in `BasicAgent._generate_lane_change_path`
    Furthermore in the GlobalRoutePlanner to build the topology and for path planning.
    
    Used with the Waypoint.next(sampling_radius) and distance between waypoints.
    """
    
    min_distance_next_waypoint: float = 3.0
    """
    Removes waypoints from the queue that are too close to the vehicle.
    
    Usage: min_distance = min_distance_next_waypoint + next_waypoint_distance_ratio * vehicle_speed
    """
    
    next_waypoint_distance_ratio: float = 0.5
    """Increases the minimum distance to the next waypoint based on the vehicles speed."""
    
    # Alias
    @property
    def step_distance(self):
        return self.sampling_resolution


@dataclass
class BehaviorAgentPlannerSettings(BasicAgentPlannerSettings):
    sampling_resolution: float = 4.5
    """
    Distance between waypoints in `BasicAgent._generate_lane_change_path`
    and GlobalRoutePlanner to build the topology and path planning.
    
    Used with the Waypoint.next(sampling_radius)
    """
    

@config_path("agent/planner")
@dataclass
class LunaticAgentPlannerSettings(BehaviorAgentPlannerSettings):
    dt: float = MISSING  # 1.0 / 20.0 # Note: Set this from main script and do not assume it.
    """
    time differential in seconds
    
    NOTE: Should set from main script.
    """
    
    # NOTE: two variables because originally used with two different names in different places
    lateral_control_dict: PIDControllerDict = field(default_factory=partial(PIDControllerDict, **{'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2, 'dt': II("${..dt}")}))
    """values of the lateral PID controller"""

    # NOTE: two variables because originally used with two different names in different places
    longitudinal_control_dict: PIDControllerDict = field(default_factory=partial(PIDControllerDict, **{'K_P': 1.0, 'K_I': 0.05, 'K_D': 0, 'dt': II("${..dt}")}))
    """values of the longitudinal PID controller"""
    
    offset: float = II("controls.vehicle_lane_offset")
    """
    If different than zero, the vehicle will drive displaced from the center line.
    
    Positive values imply a right offset while negative ones mean a left one. Numbers high enough
    to cause the vehicle to drive through other lanes might break the controller.
    """


# ---------------------
# Emergency
# ---------------------
    
@dataclass
class BasicAgentEmergencySettings(AgentConfig):
    throttle: float = 0.0
    max_emergency_brake: float = II("controls.max_brake")
    hand_brake: bool = False
    
    
@dataclass
class BehaviorAgentEmergencySettings(BasicAgentEmergencySettings):
    pass


@config_path("agent/emergency")
@dataclass
class LunaticAgentEmergencySettings(BehaviorAgentEmergencySettings):
    ignore_percentage: float = 0.0
    """Percentage of time to ignore an emergency situation and proceed as normal"""
    
    hand_brake_modify_chance: float = 0.0
    """Chance to choose the opposite of hand_break"""
    
    do_random_steering: bool = False  # TODO: Should be evasive steering
    """Whether to do random steering"""
    
    random_steering_range: Tuple[float, float] = (-0.25, 0.25)
    """Range of random steering that is applied"""

# ---------------------
# RSS
# ---------------------


@config_path("agent/rss")
@dataclass
class RssSettings(AgentConfig):
    
    enabled: bool = True
    """
    Use the RSS sensor.
    
    NOTE: Initializing with False and changing it to True is not supported.
    If RSS is not available (no ad-rss library) this will be set to False.
    """
    
    if AD_RSS_AVAILABLE:
        use_stay_on_road_feature: carla.RssRoadBoundariesMode = carla.RssRoadBoundariesMode.On     # pyright: ignore[reportRedeclaration]
        """Use the RssRoadBoundariesMode. NOTE: A call to :py:meth:`.rss_set_road_boundaries_mode` is necessary"""
        
        log_level: carla.RssLogLevel = carla.RssLogLevel.err                                       # pyright: ignore[reportRedeclaration]
        """Set the initial log level of the RSSSensor"""
    else:
        enabled = False
        
        use_stay_on_road_feature: RssRoadBoundariesModeAlias = RssRoadBoundariesMode.On      # pyright: ignore[reportRedeclaration]
        """Use the RssRoadBoundariesMode. NOTE: A call to :py:meth:`.rss_set_road_boundaries_mode` is necessary"""
        
        log_level: RssLogLevelAlias = RssLogLevel.err                                        # pyright: ignore[reportRedeclaration]
        """Set the initial log level of the RSSSensor"""
        
    debug_visualization_mode: RssDebugVisualizationMode = RssDebugVisualizationMode.RouteOnly
    """Sets the visualization mode that should be rendered on the screen."""
    
    always_accept_update: bool = False
    """Setting for the default rule to always accept RSS updates if they are valid"""
    
    rss_max_speed: float = MISSING  # NotImplemented
    """For fast vehicles RSS currently is unreliable, disables rss updates when the vehicle is faster than this."""
    
    # ------
    
    def _clean_options(self) -> None:
        if AD_RSS_AVAILABLE:
            if not isinstance(self.log_level, RssLogLevelAlias):         # pyright: ignore[reportUnnecessaryIsInstance]
                if isinstance(self.log_level, str):
                    self.log_level = getattr(carla.RssLogLevel, self.log_level)
                else:
                    self.log_level = carla.RssLogLevel.values[self.log_level]
            if not isinstance(self.use_stay_on_road_feature, RssRoadBoundariesModeAlias):   # pyright: ignore[reportUnnecessaryIsInstance]
                if isinstance(self.use_stay_on_road_feature, str):
                    self.use_stay_on_road_feature = getattr(carla.RssRoadBoundariesMode, self.use_stay_on_road_feature)
                else:
                    self.use_stay_on_road_feature = carla.RssRoadBoundariesMode.values[bool(self.use_stay_on_road_feature)]
        else:
            if not isinstance(self.use_stay_on_road_feature, RssRoadBoundariesModeAlias):   # pyright: ignore[reportUnnecessaryIsInstance]
                if isinstance(self.use_stay_on_road_feature, str):
                    self.use_stay_on_road_feature = RssRoadBoundariesMode[self.use_stay_on_road_feature]
                else:
                    self.use_stay_on_road_feature = RssRoadBoundariesMode(bool(self.use_stay_on_road_feature))
            # other not accessed
            if not isinstance(self.log_level, RssLogLevelAlias):  # pyright: ignore[reportUnnecessaryIsInstance]
                if isinstance(self.log_level, str):
                    self.log_level = RssLogLevel[self.log_level]
                else:
                    self.log_level = RssLogLevel(self.log_level)


@config_path("agent/detection_matrix")
@dataclass
class DetectionMatrixSettings(AgentConfig):
    enabled: bool = True
    """Activate or deactivate the detection matrix"""
    
    sync: bool = True
    """
    When the world uses synchronous mode and sync is true, the detection matrix will be updated every sync_interval ticks.
    A low value will have a negative impact on the fps.
    If the world uses asynchronous mode or sync is False the detection matrix will be updated by a different thread.
    This increases the fps but updates will be less frequent.
    """
    
    sync_interval: int = 5
    """
    The interval in frames after which the detection matrix should be updated. Sync must be true.
    """
    
    hud: Never = MISSING
    """
    TODO: Do not have this in Agent config; instead use an interpolation
        hud : ${camera.hud.detection_matrix}
        However, non-trivial cannot interpolate to LaunchConfig.
     #drawing_options -> see camera.yaml; need a singleton LaunchConfig and resolve to it.
    
    ---
        
    Keyword arguments for `DetectionMatrix.render`.

    Warning:
        Not implemented yet. Use `camera.hud.detection_matrix` instead.
        
    :meta exclude:
    """

# ---------------------
# Rules
# ---------------------


@dataclass
class RuleConfig(DictConfigLike if TYPE_CHECKING else object):
    """Subconfig for rules; can have arbitrary keys"""
        
    instance: object = MISSING             # pyright: ignore[reportRedeclaration, reportAssignmentType]
    """The instance of the rule, can be accessed by :python:`ctx.current_rule.instance`"""
    
    if TYPE_CHECKING:  # Cannot import Rule but need a type for OmegaConf
        instance: Rule = MISSING
        """The instance of the rule, can be accessed by :python:`ctx.current_rule.instance`"""


@dataclass
class CallFunctionFromConfig(DictConfigLike if TYPE_CHECKING else object):
    _target_: str
    """
    The name of the function to call for generating one or more rules
    hydra.utils.instantiate function.
    
    Note:
        The function must be imported in agents.rules.__init__ or
        `_target_` must be a dotted path to the function (see hydra docs).
    
    See Also:
        https://hydra.cc/docs/advanced/instantiate_objects/overview/
    
    """
    
    _args_: List[Any] = field(default_factory=list)
    """Positional arguments to pass to the Rule or Function"""
    
    random_lane_change: bool = False
    """For :py:func:`.create_default_rules`; Should the :py:class:`.RandomLaneChangeRule` be added"""


@dataclass
class CreateRuleFromConfig(DictConfigLike if TYPE_CHECKING else object):
    r"""
    Keywords to instantiate Rule classes
    
    :external-icon-parse:`:py:attr:\`omegaconf.MISSING\`` (alias for :python:`'???'`) attributes will not be passed to a :py:class:`.Rule`'s :py:meth:`~.classes.rule.Rule.__init__` method.
    """
    
    _target_: str
    """
    The name of the rule class to instantiate to be used with the
    hydra.utils.instantiate function.
    
    - overwrite_settings: These will be used to overwrite the settings of the agent.
    - self_config: This is a private storage for this rule instance to be used with
        its own condition and action functions.
    
    Note:
        The class must be imported in agents.rules.__init__ or
        `_target_` must be a dotted path to the class (see hydra docs).
    
    See Also:
        https://hydra.cc/docs/advanced/instantiate_objects/overview/
        :py:class:`.Rule` for more information on the parameters.
    
    """
    
    _args_: Optional[List[Any]] = MISSING
    """Positional arguments to pass to the Rule or Function"""
    
    phases: Optional[Union[str, Phase]] = MISSING
    #/, # phases must be positional; python3.8+ only
    condition: Optional[str] = MISSING
    action: Optional[str] = MISSING
    false_action: Optional[str] = MISSING
    actions: Optional[Dict[Any, str]] = MISSING
    description: str = MISSING
    overwrite_settings: Optional[Dict[str, Any]] = MISSING
    """These will be used to overwrite the settings of the agent."""
    
    self_config: DictConfigAlias = MISSING
    """
    This is a private storage for this rule instance to be used with
    its own condition and action functions.
    
    Interpolation to agent, or rather, context keys is possible.
    
    Note:
        - Also has an **instance** key which is the instance of the rule.
        - You can access config rule also with :python:`ctx.current_rule`
    """
    if READTHEDOCS and not TYPE_CHECKING:
        self_config: NestedConfigDict = MISSING  # lets not introduce a new variable
    
    priority: RulePriority = MISSING
    cooldown_reset_value: Optional[int] = MISSING
    group: Optional[str] = MISSING
    enabled: bool = MISSING
    
    if READTHEDOCS or TYPE_CHECKING:
        rules: "List[CreateRuleFromConfig]" = MISSING
    else:
        rules: list = MISSING  # List[CreateRuleFromConfig] # Cannot use this forward ref with omegaconf
    
    execute_all_rules: bool = MISSING
    
    weights: Optional[Dict[str, float]] = MISSING
    repeat_if_not_applicable: bool = MISSING
    ignore_phase: bool = MISSING
    
    MAX_TICKS: Optional[int] = MISSING
    max_tick_callback: Optional[str] = MISSING
    
    gameframework: None = MISSING  # pyright: ignore[reportRedeclaration]
    """Needed explicitly for :py:class:`BlockingRules` once. Depending on setup can be omitted"""
    
    if READTHEDOCS or TYPE_CHECKING:
        gameframework: Optional[GameFramework] = MISSING
    
    def __post_init__(self):
        if isinstance(self.phases, str):
            if self.phases == MISSING:
                return
            phase_strings = self.phases.strip().split(",")
            assert len(phase_strings) == 1, "Only one phase is allowed currently"
            phases = [Phase.from_string(phase_string) for phase_string in phase_strings]
            self.phases = phases[0]
        for key in self.__class__.__annotations__:
            if getattr(self, key) == MISSING:
                delattr(self, key)


RuleCreatingParameters: TypeAlias = Union[CreateRuleFromConfig, CallFunctionFromConfig, DictConfig]
"""
Alias of types that are valid for :py:func:`hydra.instantiate`
to create :py:class:`Rule | list[Rule] <Rule>`.
"""


def _from_config_default_rules():
    """
    Factory function to create a list of rule creating parameters.
    
    Rules can be added by using
    - CreateRuleFromConfig(_target_="RuleName", **kwargs)
    - CallFunctionFromConfig(_target_="function_name", _args_=[*positional_arguments])
    
    Note:
        FunctionArguments does not support keyword arguments
        
    See Also:
        - https://hydra.cc/docs/advanced/instantiate_objects/overview/
    """
    rules = [
        # Rules cann be added from
        CallFunctionFromConfig("create_default_rules", random_lane_change=False),
        CreateRuleFromConfig("DriveSlowTowardsTrafficLight", gameframework=None,
                              # NOTE: Dot notation is NOT SUPPORTED you need to nest dictionaries
                                overwrite_settings={"speed": {"follow_speed_limits": True}},
                                description="Drive slow towards while trying not to cross the line (experimental)."
                             ),
        CreateRuleFromConfig("PassYellowTrafficLightRule",
                             self_config={
                                 "try_to_pass": True,
                                 "passing_speed": II("max:${mul:${live_info.current_speed_limit},1.33},${speed.target_speed}")
                             },
                             description="Speed up to pass a yellow traffic light."
                             ),
        
        #CreateRuleFromConfig("RandomLaneChangeRule",
        #        # NOTE: Dot notation is NOT SUPPORTED you need to nest dictionaries
        #        overwrite_settings={"lane_change" : {"same_lane_time" : 0}},
        #        )
    ]
    return rules

# ---------------------
# Final Settings
# ---------------------


@dataclass
class AutopilotBehavior(AgentConfig):
    """
    These are settings from the autopilot :py:class:`carla.TrafficManager`
    which are not exposed or not used by the original carla agents.
    
    In this class they are collected in a flat structure.
    
    Note:
        That default values do not exist for most settings;
        and should be to something reasonable.
    
    :meta private:
    """

    auto_lane_change: bool = True
    """Turns on or off lane changing behavior for a vehicle."""
    
    vehicle_lane_offset: float = 0
    """
    Sets a lane offset displacement from the center line.
    
    Positive values imply a right offset while negative ones mean a left one.
    Default is 0.
    
    NOTE: Numbers high enough to cause the vehicle to drive through other lanes might break the controller.
    """

    random_left_lanechange_percentage: float = 0.1
    """
    Adjust probability that in each timestep the actor will perform a left/right lane change,
    dependent on lane change availability.
    """
    random_right_lanechange_percentage: float = 0.1
    """
    Adjust probability that in each timestep the actor will perform a left/right lane change,
    dependent on lane change availability.
    """

    keep_right_rule_percentage: float = 0.7
    """
    During the localization stage, this method sets a percent chance that vehicle will follow the keep right rule,
    and stay in the right lane.
    """

    distance_to_leading_vehicle: float = 5.0
    """
    Sets the minimum distance in meters that a vehicle has to keep with the others.
    The distance is in meters and will affect the minimum moving distance. It is computed from front to back of the vehicle objects.
    """

    vehicle_percentage_speed_difference: float = 30  # in percent
    """
    Sets the difference the vehicle's intended speed and its current speed limit.
    Speed limits can be exceeded by setting the percentage to a negative value.
    Exceeding a speed limit can be done using negative percentages.
    
    Default is 30.
    
    Note:
        Unit is in percent.
    """
    
    ignore_lights_percentage: float = 0.0
    ignore_signs_percentage: float = 0.0
    ignore_walkers_percentage: float = 0.0

    update_vehicle_lights: bool = False
    """Sets if the Traffic Manager is responsible of updating the vehicle lights, or not."""


@dataclass
class BasicAgentSettings(AgentConfig):
    """
    Settings used by the :py:class:`BasicAgent` provided with CARLA.
    """
    overwrites: Optional[OverwriteDictTypes] = field(default_factory=dict, repr=False)
    live_info: LiveInfo = field(default_factory=LiveInfo, init=False)
    speed: BasicAgentSpeedSettings = field(default_factory=BasicAgentSpeedSettings, init=False)
    distance: BasicAgentDistanceSettings = field(default_factory=BasicAgentDistanceSettings, init=False)
    lane_change: BasicAgentLaneChangeSettings = field(default_factory=BasicAgentLaneChangeSettings, init=False)
    obstacles: BasicAgentObstacleSettings = field(default_factory=BasicAgentObstacleSettings, init=False)
    controls: BasicAgentControllerSettings = field(default_factory=BasicAgentControllerSettings, init=False)
    planner: BasicAgentPlannerSettings = field(default_factory=BasicAgentPlannerSettings, init=False)
    emergency: BasicAgentEmergencySettings = field(default_factory=BasicAgentEmergencySettings, init=False)
        
    
@dataclass
class BehaviorAgentSettings(AgentConfig):
    """
    Settings used by the :py:class:`BehaviorAgent` provided with CARLA.
    """
    overwrites: Optional[OverwriteDictTypes] = field(default_factory=dict, repr=False)
    live_info: LiveInfo = field(default_factory=LiveInfo, init=False)
    speed: BehaviorAgentSpeedSettings = field(default_factory=BehaviorAgentSpeedSettings, init=False)
    distance: BehaviorAgentDistanceSettings = field(default_factory=BehaviorAgentDistanceSettings, init=False)
    lane_change: BehaviorAgentLaneChangeSettings = field(default_factory=BehaviorAgentLaneChangeSettings, init=False)
    obstacles: BehaviorAgentObstacleSettings = field(default_factory=BehaviorAgentObstacleSettings, init=False)
    controls: BehaviorAgentControllerSettings = field(default_factory=BehaviorAgentControllerSettings, init=False)
    planner: BehaviorAgentPlannerSettings = field(default_factory=BehaviorAgentPlannerSettings, init=False)
    emergency: BehaviorAgentEmergencySettings = field(default_factory=BehaviorAgentEmergencySettings, init=False)
    avoid_tailgators: bool = True


@config_path("agent")
@dataclass
class LunaticAgentSettings(AgentConfig):
    """
    .. @package agent
    
    Config schema definition for the :py:class:`.LunaticAgent` class
    """
    
    overwrites: Optional[OverwriteDictTypes] = field(default_factory=dict, repr=False)
    """Nested dictionaries used for the manual initialization of the config."""
    
    live_info: LiveInfo = field(default_factory=LiveInfo, init=False)
    """.. <take doc|LiveInfo>"""
    speed: LunaticAgentSpeedSettings = field(default_factory=LunaticAgentSpeedSettings, init=False)
    """.. <take doc|LunaticAgentSpeedSettings>"""
    distance: LunaticAgentDistanceSettings = field(default_factory=LunaticAgentDistanceSettings, init=False)
    """.. <take doc|LunaticAgentDistanceSettings>"""
    lane_change: LunaticAgentLaneChangeSettings = field(default_factory=LunaticAgentLaneChangeSettings, init=False)
    """.. <take doc|LunaticAgentLaneChangeSettings>"""
    obstacles: LunaticAgentObstacleSettings = field(default_factory=LunaticAgentObstacleSettings, init=False)
    """.. <take doc|LunaticAgentObstacleSettings>"""
    controls: LunaticAgentControllerSettings = field(default_factory=LunaticAgentControllerSettings, init=False)
    """.. <take doc|LunaticAgentControllerSettings>"""
    planner: LunaticAgentPlannerSettings = field(default_factory=LunaticAgentPlannerSettings, init=False)
    """.. <take doc|LunaticAgentPlannerSettings>"""
    emergency: LunaticAgentEmergencySettings = field(default_factory=LunaticAgentEmergencySettings, init=False)
    """.. <take doc|LunaticAgentEmergencySettings>"""
    
    # Can be set to False/None to disable
    rss: RssSettings = field(default_factory=RssSettings, init=False, metadata={"can_be_false": True})
    """.. <take doc|RssSettings>"""
    detection_matrix: DetectionMatrixSettings = field(default_factory=DetectionMatrixSettings, init=False, metadata={"can_be_false": True})
    """.. <take doc|DetectionMatrixSettings>"""
    
    # TODO: This attribute can be removed after the rules have been initialized for performance
    rules: list = field(default_factory=_from_config_default_rules)   # pyright: ignore[reportRedeclaration,reportMissingTypeArgument,reportArgumentType]
    """
    A list of Rule parameters that allow the instantiation of Rules,
    with the Hydra instantiate feature.
    
    See Also:
        - :py:class:`CreateRuleFromConfig`
        - :py:class:`CallFunctionFromConfig`
        - :py:func:`_from_config_default_rules` : Creates the default rules in the YAML file
    """
    
    if READTHEDOCS or TYPE_CHECKING:
        # variant needs to be first.
        rules: "list[RuleCreatingParameters]" = field(default_factory=_from_config_default_rules)  # pyright: ignore[reportArgumentType]
        
    # ---- Special Attributes for Context and Rule overwrites ----
    # These attributes are not usable by the agent
    
    current_rule: Never = field(default=II("self"), init=False)
    """
    Special settings of the current rule. Only available from Context within rules ctx.config.current_rule
    
    :meta private:
    """
    
    self: Never = field(default=MISSING, init=False)
    """
    Special settings of the current rule. Only available from Context within rules ctx.config.current_rule
    
    :meta private:
    """


@dataclass
class ContextSettings(LunaticAgentSettings):
    """
    Config class for the :py:class:`.Context` object.
    
    Extends the :py:class:`LunaticAgentSettings` by the **current_rule** attribute
    to accesses the :py:attr:`.Rule.self_config` attribute from the context.
    """
    
    current_rule: RuleConfig = field(default=II("self"), init=False)  # pyright: ignore[reportIncompatibleVariableOverride]
    """
    Special settings of the current rule. Only available from :py:class:`.Context` within rules :code:`ctx.config.current_rule`
    
    Note:
        Internally :py:attr:`.Context.config.current_rule` and :py:attr:`.Rule.self_config`
        are the same object.
        
    See Also:
        - :py:attr:`.RuleConfig.self_config`
    """
    
    self: RuleConfig = field(default=MISSING, init=False)                      # pyright: ignore[reportIncompatibleVariableOverride]
    """
    Describes the :py:attr:`.Rule.self_config` attribute of the current rule,
    which is the same as the :py:attr:`.Context.config.current_rule` attribute.
    Rules should use the **self** key to access these settings.
    
    :meta private:
    """

# ---------------------
# Launch Settings
# ---------------------


@config_path("camera")
@dataclass
class CameraConfig(AgentConfig):
    """
    .. @package camera
    """
    
    # Use from launch_config
    width: int = II("width")
    """With pygame window. Takes the value from the :py:class:`LaunchConfig`."""
    height: int = II("height")
    """Height of pygame window. Takes the value from the :py:class:`LaunchConfig`."""
    gamma: float = II("gamma")
    """Gamma correction of the camera. Takes the value from the :py:class:`LaunchConfig`."""
    
    spectator: bool = True
    """If True will update the Unreal Engine's spectator camera"""
    
    # NotImplemented
    
    # In structured mode named tuples and carla Types are problematic
    camera_blueprints: list = field(default_factory=lambda: [  # pyright: ignore[reportRedeclaration]
        CameraBlueprint("sensor.camera.rgb", carla.ColorConverter.Raw, "RGB camera")
        ])
    """
    Cameras and sensors attached to the ego vehicle
    that can be viewed by the user in the pygame window.
    
    Used with the :py:attr:`.CameraManager.sensors`.
    
    Attention:
        Usage not yet implemented.
    """

    if TYPE_CHECKING:
        camera_blueprints: List["CameraBlueprint"] = field(default_factory=lambda: [
            CameraBlueprint("sensor.camera.rgb", carla.ColorConverter.Raw, "RGB camera"),
            ])
    
    @config_path("camera/recorder")
    @dataclass
    class RecorderSettings(AgentConfig):
        """
        Recorder settings for the camera.
        """
        
        enabled: bool = MISSING
        """
        Whether the recorder is enabled
        
        Set at WorldModel level
        
        :meta private:
        """
        
        output_path: str = '${hydra:runtime.output_dir}/recorder/session%03d/%08d.bmp'
        """
        Folder to record the camera
        
        Needs two numeric conversion placeholders.
        
        Note:
            When using the ${hydra:runtime.output_dir} resolver
            @hydra.main needs to be used or hydra must be initialized.
        """
        
        frame_interval: int = 4
        """Interval to record the camera"""
        
    recorder: RecorderSettings = field(default_factory=RecorderSettings)
    """.. <take doc|RecorderSettings>"""
    
    @config_path("camera/hud")
    @dataclass
    class HUDConfig(AgentConfig):
        """
        HUD settings for the pygame window.
        """
        
        # Block not implemented
        enabled: bool = True
        """Whether the HUD is enabled. Not Implemented"""
        
        font_size: int = 20
        """Font size of the HUD. Not Implemented"""
        
        font_color: Tuple[int, int, int] = (255, 255, 255)
        """Font color of the HUD. Not Implemented"""
        
        font: str = "arial"
        """Font of the HUD. Not Implemented"""
        # ----------------------------
    
        @config_path("camera/hud/detection_matrix")
        @dataclass
        class DetectionMatrixHUDConfig(AgentConfig):
            """
            DetectionMatrix settings for the HUD
            
            Attention:
                Keys must match keywords of :py:meth:`.DetectionMatrix.render`
            """
            
            draw: bool = True
            """Whether to draw the detection matrix"""
            
            draw_values: bool = True
            """Whether to draw the numerical values as text"""
            
            vertical: bool = True
            """Orient vertical (lanes are left to right) instead of horizontal."""
            
            imshow_settings: Dict[str, Any] = field(default_factory=lambda: {'cmap': 'jet'})
            """Settings for the pyplot.imshow function"""
            
            text_settings: Dict[str, Any] = field(default_factory=lambda: {'color': 'orange'})
            """Settings for the text of pyplot.text when drawing the numerical values"""

        detection_matrix: DetectionMatrixHUDConfig = field(default_factory=DetectionMatrixHUDConfig)
        """.. <take doc|DetectionMatrixHUDConfig>"""
        
    hud: HUDConfig = field(default_factory=HUDConfig)
    """.. <take doc|HUDConfig>"""


@config_path("launch_config_default.yaml")  # NOTE: this may not be named launch_config
@dataclass
class LaunchConfig(AgentConfig):
        
    strict_config: Union[bool, int] = 3
    """
    If enabled will assert that the loaded config is a subset of the `LaunchConfig` class.
    
    If set to >= 2, will assert that during runtime the types are correct.
    """
    
    verbose: bool = True
    """unused kept for compatibility with carla examples."""
    
    debug: bool = True
    """If true will print out some more information and draws waypoints"""
    
    interactive: bool = False
    """
    If True will create an interactive session with command line input
    - NOTE: Needs custom code in the main file (Not implemented)
    """
    
    seed: Optional[int] = 1

    # carla_service:
    map: str = "Town04_Opt"
    host: str = "127.0.0.1"
    port: int = 2000
    
    timeout: float = 10.0
    """
    Timeout for the :py:class:`carla.Client` connection.
    """
    
    fps: int = 20
    """
    Used to fix :py:attr:`carla.WorldSettings.fixed_delta_seconds`
    
    Experimental also used to cap fps in the simulation.
    """
    
    sync: Union[bool, None] = True
    """
    If True, the simulation will be set to run in synchronous mode.
    For False, the simulation will be set to run in asynchronous mode.
    If None the world settings for synchronous mode will not be adjusted,
    assuming this is handled by the user / external system.
    """
    
    handle_ticks: bool = True
    """
    Decide if the GameFramework & WoldModel are allowed to call carla.World.tick()
    or if `False` the ticks should be handled by an outside system.
    """

    loop: bool = True
    """
    If True the agent will look for a new waypoint after the initial route is done.
    
    Note:
        Needs custom implementation in the main file by the user.
    """

    # camera:
    width: int = 1280
    """width of pygame window"""
    height: int = 720
    """height of pygame window"""
    gamma: float = 2.2
    """
    Gamma correction of the camera.
    Depending on the weather and map this might need to be adjusted.
    """

    # Actor
    externalActor: bool = True
    """
    If False will spawn a vehicle for the agent to control, using the `filter` and `generation` settings.
    Otherwise will not spawn a vehicle but will wait until an actor with the name defined in `rolename` (default: "hero") is found.
    
    This vehicle needs to be spawned by another process, e.g. through the scenario runner.
    """
    
    rolename: str = "hero"
    """Actor name to wait for if `externalActor` is True."""
    
    filter: str = "vehicle.*"
    """Filter for the ego blueprint. Kept for compatibility with carla examples."""
    
    generation: Union[int, str] = 2  # pyright: ignore[reportRedeclaration]
    """Generation for the ego blueprint. Kept for compatibility with carla examples."""
    
    if READTHEDOCS or TYPE_CHECKING:
        generation: Literal[1, 2, 'all']
    
    autopilot: bool = False
    r"""
    Whether or not to use the CARLAS's :external-icon-parse:`:py:class:\`carla.TrafficManager\`` to autopilot the agent
    
    Note:
        This disables the usage of the LunaticAgent, however needs to be
        enabled in the main script by the user to work.
    """
    
    restart_clean_sensors: Optional[bool] = None
    """
    If None will remove all sensors from an externalActor if :py:meth:`.WorldModel.restart` is
    called outside from the initialization, i.e. :py:meth:`~.WorldModel.restart` it is called a second time.
    Else will always/never remove the sensors when using :py:meth:`.WorldModel.restart`.
    """
    
    agent: LunaticAgentSettings = MISSING
    """The settings of the agent"""
    
    camera: CameraConfig = field(default_factory=CameraConfig)
    """.. <take doc|CameraConfig>"""
    
    pygame: bool = True
    """
    Deactivates the pygame window and interface.
    
    Attention:
        Experimental
    
    :meta private:
    """
    
    # ---
    
    hydra: Annotated[HydraConf, "Key not guaranteed to be present or complete."] = field(
        default=MISSING, compare=False, hash=False
    )
    """
    Hydra_ config dict.
    
    Attention:
        This field is not guaranteed to be present or the complete :py:class:`HydraConf` schema.
    
    :meta exclude: # not included in yaml.comments
    """
    
    if not TYPE_CHECKING:
        # should not be HydraConf at runtime, as it is not complete
        hydra: HydraConf = field(default=MISSING, compare=False, hash=False)
    
    if READTHEDOCS or TYPE_CHECKING:
        leaderboard: Annotated[DictConfig, "Only present for the", LunaticChallenger] = field(init=False, kw_only=True)

# ---------------------


def export_schemas(detailed_rules: bool = False):
    """
    Exports the schemas as YAML files to the `conf/` folder with comment annotations.
    
    Parameters:
        detailed_rules: If True, the :py:attr:`LunaticAgentSettings.rules` entry will also include comments and
            further information. Default is :code:`False`.
    
    Note:
        This function is executed automatically when the module is imported.<br>
        **detailed_rules** may only be :python:`True` *after* the rules submodule has been initialized,
        i.e. cannot be called in this file.
    """
    
    #  Using OmegaConf.set_struct, it is possible to prevent the creation of fields that do not exist:
    LunaticAgentSettings.export_options(
        "conf/agent/default_settings.yaml", with_comments=True, detailed_rules=detailed_rules
    )
    
    # Export the launch config
    lc = LaunchConfig()
    lc.camera.camera_blueprints = ["NotImplemented"]  # TODO: Currently not converted to yaml layout
    lc.export_options("conf/launch_config_default.yaml", with_comments=True, detailed_rules=detailed_rules)
    lc.camera.export_options(
        "conf/config_extensions/camera_default.yaml", with_comments=True, detailed_rules=detailed_rules
    )
    # LiveInfo
    LiveInfo.export_options("conf/agent/live_info.yaml", with_comments=True, detailed_rules=detailed_rules)


# Always want the schemas to be up to date
# Cannot extract rules because of circular imports; a second call is done in rules/__init__.py
if not READTHEDOCS:
    try:
        export_schemas(detailed_rules=False)
    except Exception:
        logging.exception("Error exporting schemas")
