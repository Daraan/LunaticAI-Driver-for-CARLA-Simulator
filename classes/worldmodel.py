"""
Interface classes between CARLA, the agent, and the user interface.
"""

from __future__ import annotations

# pyright: reportOptionalMemberAccess=warning

from collections.abc import Mapping
import os
import sys
import weakref
from typing import (Any, ClassVar, List, NoReturn, Optional, Sequence, Union, cast as assure_type,
                    TYPE_CHECKING, TypeVar, overload)

import numpy as np
import hydra
from hydra.core.global_hydra import GlobalHydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, OmegaConf, open_dict

import carla
import pygame
import numpy.random as random
from agents.tools.config_creation import LaunchConfig, LunaticAgentSettings, RssLogLevel, RssRoadBoundariesMode
from launch_tools import class_or_instance_method
from classes.hud import HUD, get_actor_display_name

from classes.camera_manager import CameraManager
from classes.carla_originals.sensors import (CollisionSensor, LaneInvasionSensor, RadarSensor,
                                             GnssSensor, IMUSensor)

from classes import exceptions as _exceptions
from classes.exceptions import AgentDoneException, ContinueLoopException
from classes.rss_sensor import RssSensor, AD_RSS_AVAILABLE
from classes.rss_visualization import RssUnstructuredSceneVisualizer, RssBoundingBoxVisualizer
from classes.keyboard_controls import KeyboardControl, RSSKeyboardControl
from data_gathering.information_manager import InformationManager

if TYPE_CHECKING:
    from types import ModuleType
    from typing_extensions import Self
    from hydra.conf import HydraConf
    from agents.lunatic_agent import LunaticAgent
    from agents.navigation.global_route_planner import GlobalRoutePlanner
    from agents.tools.config_creation import LaunchConfig, LunaticAgentSettings, RssRoadBoundariesModeAlias
    from classes._sensor_interface import CustomSensorInterface
    from data_gathering.car_detection_matrix.run_matrix import DetectionMatrix

from launch_tools.blueprint_helpers import get_actor_blueprints
from launch_tools import CarlaDataProvider, Literal, carla_service
from agents.tools.logging import logger


_ControllerClass = TypeVar("_ControllerClass", bound=KeyboardControl)

class AccessCarlaMixin:
    """
    Mixin class that delegates the attributes :py:attr:`client`, :py:attr:`map`, and :py:attr:`world`
    to the :py:class:`.CarlaDataProvider` to keep them in sync.
    
    Note:
        This mixin only works for instances, they are not class attributes.
    """
    
    @property
    def client(self) -> carla.Client:
        return CarlaDataProvider.get_client()
    
    @client.setter
    def client(self, value: carla.Client):
        CarlaDataProvider.set_client(value)
    
    @property
    def world(self) -> carla.World:
        return CarlaDataProvider.get_world()
    
    @world.setter
    def world(self, value: carla.World):
        CarlaDataProvider.set_world(value)
    
    @property
    def map(self) -> carla.Map:
        return CarlaDataProvider.get_map()
    
    @map.setter
    def map(self, value: carla.Map):
        """
        Avoid setting the map directly. Use :py:meth:`.CarlaDataProvider.set_world` instead.
        
        Raises:
            ValueError: If the map is not the same as the one set in :py:attr:`.CarlaDataProvider.get_map`.
        
        :meta private:
        """
        if CarlaDataProvider.get_map() != value:
            raise ValueError("CarlaDataProvider.get_map() and passed map are not the same.")
        # Do nothing as map is set when using get_map or set_world
    
    @staticmethod
    def get_blueprint_library() -> carla.BlueprintLibrary:
        """
        Access to a cached version of the blueprint library
        
        Attention:
            The world must be setup before (:py:meth:`.set_world`) before this can be accessed.
        """
        if CarlaDataProvider._blueprint_library is None:
            raise ValueError("Blueprint Library not set. Call CarlaDataProvider.set_world() first.")
        return CarlaDataProvider._blueprint_library

# ==============================================================================
# -- Game Framework ---------------------------------------------------------------
# ==============================================================================

class GameFramework(AccessCarlaMixin, CarlaDataProvider):
    clock : ClassVar[pygame.time.Clock] = None
    display : ClassVar[pygame.Surface] = None
    controller: weakref.ProxyType[RSSKeyboardControl] | RSSKeyboardControl
    
    traffic_manager : Optional[carla.TrafficManager] = None
    
    @property
    def launch_config(self) -> LaunchConfig:
        """:py:class:`.LaunchConfig` object that was used for the initialization (**args**)"""
        return self._args
    
    @property
    def agent_config(self) -> LunaticAgentSettings:
        """
        The configuration of the attached :py:attr:`agent`, if it exists otherwise the
        **agent** attribute of the stored :py:attr:`launch_config`.
        """
        return self.agent.config if self.agent else self._args.agent
    
    # ----- Init Functions -----
    
    @classmethod
    def quickstart(cls, launch_config: Optional[LaunchConfig]=None, *, logging: bool=False) -> "Self":
        """
        Initializes Hydra_ in a limited way, i.e. does not allow for command line overrides.
        
        Sets up the :py:class:`carla.Client` and related instances as well as pygame.
        
        Note:
            It is recommended that you use a :python:`@hydra.main` decorated main function instead
            to make full use of the Hydra_ framework.
        
        Parameters:
            launch_config: The configuration to use. If :code:`None`, will use the default
                           configuration from :code:`./conf/launch_config.yaml`.
            logging: If True, change the how logging is done by applying the logger settings from
                     :code:`./conf/config_extensions/job_logging.yaml`.
                     Default is :code:`False`.
                     
        Returns:
            The initialized :py:class:`GameFramework` instance.
                     
        See Also:
            This function uses:
                - :py:meth:`.initialize_hydra`
                - :py:meth:`.init_carla`
                - :py:meth:`.init_pygame`
        """
        if not launch_config:
            launch_config = cls.initialize_hydra(logging=logging)
        if not logging and AD_RSS_AVAILABLE:
            launch_config.agent.rss.log_level = RssLogLevel.off
        cls.init_carla(launch_config)
        cls.init_pygame(launch_config)
        return cls(launch_config)

    # Hydra Tools
    # TODO: this could be some launch_tools MixinClass
    @staticmethod
    def initialize_hydra(config_dir: str="./conf",
                         config_name: str="launch_config",
                         version_base=None, *,
                         job_name="LunaticAgentJob",
                         logging=True,
                         structured=True) -> "LaunchConfig":
        """
        Use this function only if no hydra.main is available.
        
        Usage:
        
        .. code-block:: python
        
            args = GameFramework.initialize_hydra(config_dir=<abs_path_of_conf>, config_name="launch_config")
            game_framework = GameFramework(args)
            
        Args:
            config_dir: The directory where the hydra configuration is stored.
            config_name: The name of the configuration file.
            version_base: The version base of hydra for the configuration. Default is None.
            job_name: The name of the job.
            logging: If True, will set up logging.
            structured: If True will create the config based on :py:class:`.LaunchConfig`,
                        otherwise it will be based on a :python:`dict`. This is useful for runtime
                        type-checks and conversions.
                        If the configs :py:attr:`.LaunchConfig.strict_config` value is < 2, this
                        parameter is ignored. Disable if you experience problems.
                        Default is :python:`True`.
            
        See Also:
            Hydra functions:
                - :py:func:`hydra.initialize_config_dir`
                - :py:func:`hydra.compose`
        """
        config_dir = os.path.abspath(config_dir)
        hydra_initialized = GameFramework.hydra_initialized()
        if not hydra_initialized:
            # Not save-guarding this against multiple calls, expose the hydra error
            # todo: low-prio check if config dir and the other parameters are the same.
            hydra.initialize_config_dir(version_base=version_base,
                                            config_dir=config_dir,
                                            job_name=job_name)
            
        dict_config = hydra.compose(config_name=config_name,
                                                return_hydra_config=not hydra_initialized,
                                                overrides=None)
        if structured and dict_config.get("strict_config", 3) >= 2:
            # Uses the correct dataclass schemas as values.
            from agents.tools.config_creation import LaunchConfig, config_store
            if config_name == "launch_config":
                if LaunchConfig._config_path:
                    # Load defined schema from the config Store
                    cn = config_store.load(LaunchConfig._config_path)
                    schema: Optional[DictConfig] = cn.node # type: ignore[assignment]
                    with open_dict(schema):
                        schema.merge_with(dict_config)
                    config = assure_type(LaunchConfig, schema)
                else:
                    schema = None
            else:
                schema = None
            if schema is None:
                logger.debug("No schema found for structured init file %s. Falling back to LaunchConfig", config_name)
                launch_config = LaunchConfig(**dict_config) # type: ignore
                config : LaunchConfig = OmegaConf.structured(launch_config,
                                                            flags={'allow_objects' : True})
        else:
            config = assure_type("LaunchConfig", dict_config)
        
        if not hydra_initialized:
            hydra_conf: HydraConfig = GameFramework.get_hydra_config(raw=True)
            if OmegaConf.is_missing(config.hydra.runtime, "output_dir"):
                config.hydra.runtime.output_dir = config.hydra.run.dir
            hydra_conf.set_config(config)       # type: ignore
            os.makedirs(config.hydra.runtime.output_dir, exist_ok=True)
            from hydra.core.utils import configure_log
            if logging:
                 # Assure that our logger works
                configure_log(config.hydra.job_logging, logger.name) # type: ignore
            with open_dict(config):
                del config["hydra"]
        config.agent._set_flag("allow_objects", True)
        config.agent.__dict__["_parent"] = None # Remove parent from the config, i.e. make it a top-level config.
        return config
        
    # TODO: Maybe unify these settings; make overrides available in the config.
    @staticmethod
    def load_hydra_config(config_name: str="conf/launch_config") -> "LaunchConfig":
        if GameFramework.hydra_initialized():
            return assure_type(LaunchConfig, hydra.compose(config_name=config_name))
        else:
            config_dir, config_name = os.path.split(config_name)
            import inspect
            frame = inspect.stack()[-1]
            module = inspect.getmodule(frame[0])
            name = module.__file__ if module and module.__file__ else "unknown"
            return GameFramework.initialize_hydra(config_dir, config_name, job_name=name)
            
    
    def __init__(self, args: "LaunchConfig",
                 config: Optional[DictConfig]=None,
                 timeout:float=10.0,
                 worker_threads:int =0,
                 *, map_layers=carla.MapLayer.All):
        """
        Parameters:
            args: Configuration for the GameFramework.
            config: Optional config for the agent (unused in this project)
            timeout: Timeout for the :py:class:`carla.Client`.
            worker_threads: See :py:class:`carla.Client`.
            map_layers: See :py:meth:`carla.Client.load_world`
        """
        if args.seed:
            random.seed(args.seed)
            np.random.seed(args.seed)
        self._args = args
        self.world_settings: carla.WorldSettings = self.init_carla(args, timeout, worker_threads, map_layers=map_layers)
        
        # These are class variables
        clock, display = self.init_pygame(args) # pylint: disable=unused-variable
        
        self.config = config
        self.agent = None
        self.world_model = None
        self.controller = None
        
        self.debug = self.world.debug
        self.continue_loop = True
        self.traffic_manager : Optional[carla.TrafficManager] = self.init_traffic_manager()
        
        # Import here to avoid circular imports
        from classes.rule import BlockingRule, Rule
        self.cooldown_framework = Rule.CooldownFramework() # used in context manager. # NOTE: Currently can be constant
        
        BlockingRule._gameframework = weakref.proxy(self)
        
    @class_or_instance_method
    def init_pygame(cls_or_self: "Self | type[Self]", launch_config: Optional[LaunchConfig]=None,
                    recreate: bool=False) -> tuple[pygame.time.Clock, pygame.Surface]:
        """
        Parameters:
            launch_config: Will use the :py:attr:`width<.LaunchConfig.width>` and
                :py:attr:`height<.LaunchConfig.height> attributes of this object if set the
                :py:mod:`pygame` windows size. Otherwise will use :python:`(1280, 720)`.
                Defaults to :code:`None`.
                
            recreate: If :python:`True`, will reinitialize pygame a second time if this function is
                called.
                
        .. experimental; returns None, None if launch_config.pygame is False.
        """
        if recreate or GameFramework.clock is None or GameFramework.display is None:
            if launch_config is None:
                launch_config = getattr(cls_or_self, "_args", None) # get from inst.
            if getattr(launch_config, "pygame", True):
                pygame.init()
                pygame.font.init()
            GameFramework.clock = pygame.time.Clock()
            if getattr(launch_config, "pygame", True) and "READTHEDOCS" not in os.environ:
                GameFramework.display = pygame.display.set_mode(
                    size=(launch_config.width, launch_config.height)
                         if launch_config else (1280, 720),
                    flags=pygame.HWSURFACE | pygame.DOUBLEBUF)
        return GameFramework.clock, GameFramework.display
    
    @staticmethod
    def init_carla(args: Optional[LaunchConfig]=None,
                   timeout: float =10.0,
                   worker_threads: int=0, *,
                   map_layers: carla.MapLayer=carla.MapLayer.All) -> carla.WorldSettings:
        """
        Initializes the :py:class:`carla.Client` and the connects it to the simulator.
        
        See Also:
            - :py:class:`carla.Client`
            - :py:meth:`carla.Client.load_world`
        """
        # Note: This sets up the CarlaDataProvider
        if args is None:
            carla_service.initialize_carla(timeout=timeout,
                                           worker_threads=worker_threads,
                                           map_layers=map_layers)
        else:
            carla_service.initialize_carla(args.map,
                                           args.host, args.port,
                                           timeout=timeout,
                                           worker_threads=worker_threads,
                                           map_layers=map_layers,
                                           sync=args.sync,
                                           fps=args.fps)
        return CarlaDataProvider.get_world().get_settings()
    
    def init_traffic_manager(self, port: Optional[int]=None) -> carla.TrafficManager:
        """
        Returns an instance of the :py:class:`carla.TrafficManager`
        related to the specified port. If it does not exist, this will be created.
        
        See Also:
            :py:meth:`carla.Client.get_trafficmanager`
            
        Parameters:
            port: The port to use. If :code:`None`, will use the port from
                :py:meth:`.CarlaDataProvider.get_traffic_manager_port`, which defaults to :code:`8000`.
        """
        if port is None:
            port = CarlaDataProvider.get_traffic_manager_port()
        traffic_manager = self.client.get_trafficmanager(port)
        if self._args.handle_ticks:
            if self._args.sync:
                traffic_manager.set_synchronous_mode(True)
            traffic_manager.set_hybrid_physics_mode(True) # Note default 50m
            traffic_manager.set_hybrid_physics_radius(50.0) # TODO: make a LaunchConfig config variable
        self.traffic_manager = traffic_manager
        return traffic_manager
    
    def init_agent_and_interface(self,
            ego: Optional[carla.Vehicle],
            agent_class: "type[LunaticAgent]",
            config: Optional[LunaticAgentSettings]=None,
            overwrites: Optional[dict[str, Any]]=None
        ) -> "tuple[LunaticAgent, WorldModel, GlobalRoutePlanner, RSSKeyboardControl]":
        """
        Quick setup for the agent and the world model.
        
        Among others this executes:
            - :py:meth:`.LunaticAgent.create_world_and_agent`
            - :py:meth:`.GameFramework.make_controller`
            - :py:meth:`.WorldModel.tick_server_world`
        
        .. code-block:: python
        
            from agents.lunatic_agent import LunaticAgent, LunaticAgentSettings
            
            ego = world.spawn_actor(world.get_blueprint_library().find("vehicle.audi.tt"))
            agent, world_model, global_planner, controller = (
                game_framework.init_agent_and_interface(ego, LunaticAgent)
            )
            
        Arguments:
            ego: The ego vehicle. Can be :code:`None` if the agent is set to use an
                 external actor (:py:attr:`.LaunchConfig.externalActor`).
            agent_class: The agent class to instantiate.
            config: The configuration of the agent. If :code:`None` the
                    :py:attr:`.agent_class.BASE_SETTINGS <.LunaticAgent.BASE_SETTINGS>` are used.
            overwrites: Additional overwrites to the configuration.
        """
        if ego is None and not self._args.externalActor:
            raise ValueError("`ego` must be passed if ``externalActor` is not set.")
        self.agent, self.world_model, self.global_planner \
            = agent_class.create_world_and_agent(self._args,
                                               vehicle=ego,
                                               sim_world=self.world,
                                               agent_config=config,
                                               overwrites=overwrites)
        self.config = self.agent.config
        controller = self.make_controller(self.world_model, RSSKeyboardControl, start_in_autopilot=False) # Note: stores weakref to controller
        self.world_model.game_framework = weakref.proxy(self)
        self.world_model.tick_server_world()
        self.agent.verify_settings(strictness=-1) # NOTE: Here live info is already available and will throw some errors
        return self.agent, self.world_model, self.global_planner, controller
    
    def make_world_model(self, config: "LunaticAgentSettings",
                         player: Optional[carla.Vehicle]=None) -> "WorldModel":
        """
        Creates a :py:class:`WorldModel` with a backreference to the GameFramework.
        """
        self.world_model = WorldModel(config, self._args, player=player)
        self.world_model.game_framework = weakref.proxy(self)
        return self.world_model
    
    def make_controller(self,
                        world_model: "WorldModel",
                        controller_class: "type[_ControllerClass]"=RSSKeyboardControl,
                        **kwargs):
        """
        Creates a keyboard controller and attaches it to the world model.
        
        Args:
            world_model: The world model to attach the controller to.
            controller_class: The controller class to instantiate. Defaults to :py:class:`.RSSKeyboardControl`.
            **kwargs: Additional arguments to pass to the controller.
        """
        controller = controller_class(world_model,
                                        config=self.config,
                                        clock=self.clock,
                                        **kwargs)
        self.controller = weakref.proxy(controller)
        return controller # NOTE: does not return the proxy object.
    
    @staticmethod
    def hydra_initialized() -> bool:
        """
        Checks wether Hydra_ is initialized. This is normally only done
        when the :py:func:`@hydra.main` decorator is used.
        """
        return GlobalHydra.instance().is_initialized()

    @overload
    @staticmethod
    def get_hydra_config(raw: Literal[False]=False) -> "HydraConf":
        ...
    @overload
    @staticmethod
    def get_hydra_config(raw: Literal[True]) -> HydraConfig:
        ...

    @staticmethod
    def get_hydra_config(raw: bool=False) -> "HydraConfig | HydraConf":
        """
        Retrieves the Hydra_ configuration object.
        
        Parameters:
            raw: If :python:`True`, returns the :py:class:`hydra.conf.HydraConf` dataclass, otherwise the
                :py:class:`hydra.core.hydra_config.HydraConfig` singleton. Default is :code:`False`.
                
        Raises:
            ValueError: If the HydraConfig was not set up yet and :python:`raw=True`.
        """
        if raw:
            return HydraConfig.instance()
        return HydraConfig.get()
    

    
    # ----- Setters -----
    
    def set_controller(self, controller: KeyboardControl) -> None:
        """
        Set the :py:class:`KeyboardControl`
        
        :meta private:
        """
        self.controller = controller # type: ignore ; maybe use proxy
    
    def set_config(self, config:DictConfig) -> None:
        """
        Change the :py:attr:`config`.
        
        :meta private:
        """
        self.config = config
    
    # ----- UI Functions -----
    
    def parse_rss_controller_events(self, final_controls:carla.VehicleControl):
        return self.controller.parse_events(final_controls)
    
    def render_everything(self):
        """
        Update render and hud
        
        Note:
            This is the preferred method to update the world and render the camera.
        """
        self.world_model.tick(self.clock)  # NOTE: Ticks WorldMODEL not CARLA WORLD!  # pyright: ignore[reportOptionalMemberAccess]
        self.world_model.render(self.display, finalize=False)  # pyright: ignore[reportOptionalMemberAccess]
        self.controller.render(self.display)
        dm_render_conf: "DetectionMatrix.RenderOptions" \
            = OmegaConf.select(self._args, "camera.hud.data_matrix", default=None)
        if dm_render_conf and self.agent:
            self.agent._render_detection_matrix(self.display, **dm_render_conf)
        self.world_model.finalize_render(self.display)  # pyright: ignore[reportOptionalMemberAccess]
        
    @staticmethod
    def skip_rest_of_loop(message="GameFramework.end_loop") -> NoReturn:
        """
        Terminates the current iteration and exits the GameFramework by raising a :py:exc:`.ContinueLoopException`.
        
        Note:
            It is the users responsibility to manage the agent & local planner
            before calling this function, i.e. that the agent has a :py:class:`carla.VehicleControl` set.
        
        Raises:
            ContinueLoopException: With the given **message**.
        """
        # TODO: add option that still allows for rss.
        raise ContinueLoopException(message)
    
    # -------- Tools --------
    
    spawn_actor = staticmethod(carla_service.spawn_actor)
    
    destroy_actors = staticmethod(carla_service.destroy_actors)
    
    # -------- Context Manager --------

    def __call__(self, agent: "LunaticAgent"):
        """
        Use as context manager to handle the game loop.
        Pass an agent if None is set yet.
        """
        self.agent = agent
        self.world_model = agent._world_model
        try:
            if self.world_model.controller: # weakref.proxy
                self.controller = self.world_model.controller
        except ReferenceError:
            self.controller = None                            # type: ignore[assignment]
        if not self.controller:
            logger.debug("Creating new controller.")
            self.controller = self.make_controller(self.world_model, start_in_autopilot=self._args.autopilot) # hard reference # type: ignore
            self.world_model.controller = self.controller  # hard instead of weak reference
        self.agent._validate_phases = False
        return self

    def __enter__(self):
        if self.agent is None:
            raise ValueError("Agent not initialized.")
        if self.world_model is None:
            raise ValueError("World Model not initialized.")
        if self.controller is None:
            raise ValueError("Controller not initialized.")
        
        self.clock.tick() # self.args.fps)
        frame = None
        if self._args.handle_ticks: # i.e. no scenario runner doing it for us
            if CarlaDataProvider.is_sync_mode():
                frame = self.world_model.world.tick()
            else:
                frame = self.world_model.world.wait_for_tick().frame
            CarlaDataProvider.on_carla_tick()

        if CarlaDataProvider.is_sync_mode():
            # We do this only in sync mode as frames could pass between gathering this information
            # and an agent calling InformationManager.tick(), which in turn calls global_tick
            # with possibly a DIFFERENT frame wasting computation.
            if frame is None:
                frame = self.get_world().get_snapshot().frame
            InformationManager.global_tick(frame)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cooldown_framework.__exit__(exc_type, exc_val, exc_tb)
        if exc_val:
            if isinstance(exc_val, AgentDoneException):
                self.continue_loop = False
            elif isinstance(exc_val, ContinueLoopException):
                logger.error("ContinueLoopException(%s) should be thrown during `agent.run_step` but caught by GameFramework this should not happen. Skipping this step; no controls are applied!", exc_val)
            else:
                return # skip render and likely terminate.
        self.render_everything()
        pygame.display.flip()

    @class_or_instance_method
    def cleanup(cls_or_self: "type[Self] | Self",
                *,
                disable_sync: bool=True,
                quit_pygame: bool=True):
        """
        Cleans up resources and actors.
        
        Args:
            disable_sync: If True, will disable synchronous mode. This will
                prevent the freezing of the Unreal Editor.
                Default is True.
            quit_pygame: If True, will call :py:func:`pygame.quit`. Default is True.
        
        Note:
            - When called from an instance with an attached agent,
              the :python:`agent.destroy()` method is called.
            - Otherwise will call :py:obj:`CarlaDataProvider.cleanup() <.CarlaDataProvider>`.
        """
        try:
            # Should only work for instance version, but maybe future Singleton support
            try:
                if cls_or_self.agent:            # pyright: ignore[reportAttributeAccessIssue]
                    cls_or_self.agent.destroy()  # pyright: ignore[reportAttributeAccessIssue]
            finally:
                if cls_or_self.world_model:            # pyright: ignore[reportAttributeAccessIssue]
                    cls_or_self.world_model.destroy()  # pyright: ignore[reportAttributeAccessIssue]
            if disable_sync and cls_or_self.traffic_manager:
                try:
                    cls_or_self.traffic_manager.set_synchronous_mode(False)
                except Exception:
                    pass
        finally:
            if disable_sync:
                # Prevent freezing of the editor
                if CarlaDataProvider.get_world() is not None:
                    # Disable Synchronous Mode
                    world_settings = carla.WorldSettings(synchronous_mode=False,
                                                        fixed_delta_seconds=0.0)
                    cls_or_self._world.apply_settings(world_settings)
            CarlaDataProvider.cleanup()
            if quit_pygame:
                pygame.quit()
    
    # Include access to our exceptions here
    exceptions : "ModuleType" = _exceptions
    """
    shortcut to :py:mod:`.exceptions` module containing custom exceptions.
    
    :meta hide-value:
    """


# ==============================================================================
# -- World ---------------------------------------------------------------
# ==============================================================================

class WorldModel(AccessCarlaMixin, CarlaDataProvider):
    """
    Class representing the surrounding environment.
    
    This class is the interface between the agent, the :external_py_class:`carla.World`, the
    :py:class:`.HUD`, and the :py:class:`.KeyboardControl`.
    It handles ticking of the simulator and rendering of the pygame interface.
    
    If :py:attr:`.LaunchConfig.externalActor` is set, it will look for an actor with the role name
    :py:attr:`.LaunchConfig.rolename`, if such an actor does not yet exist it will wait for its
    creation until the calling script continues.
    """

    controller : Optional[Union[RSSKeyboardControl, weakref.ProxyType[RSSKeyboardControl]]] = None
    """
    Set when controller is created. Uses weakref.proxy as backreference.
    This is not a :py:mod:`weakref` object, when
    `with gameframework(agent) <GameFramework.__call__>`:py:meth: is used.
    """
    
    game_framework : Optional["weakref.CallableProxyType[GameFramework]"] = None
    """
    Set when world created via GameFramework. Uses weakref.proxy as backreference
    
    Attention:
        Currently not used and not initialized.
    
    :meta private:
    """

    player : carla.Vehicle
    """
    The linked actor. If :py:attr:`.external_actor` is set this will be the first actor found
    with that role name.
    """

    def __init__(self, config: "LunaticAgentSettings",
                 args: Union[LaunchConfig, Mapping[str, Any], "os.PathLike[str]", str] ="./conf/launch_config.yaml",
                 agent: Optional[LunaticAgent] = None,
                 *,
                 carla_world: Optional[carla.World] =None,
                 player: Optional[carla.Vehicle] =None,
                 map_inst: Optional[carla.Map] =None):
        """Constructor method"""
        # Set World
        if self.get_world() is None:
            if carla_world is None:
                raise ValueError("CarlaDataProvider not available and `carla_world` not passed.")
            self.world = carla_world
        elif carla_world is not None and self.world != carla_world:
            raise ValueError("CarlaDataProvider.get_world() and passed `carla_world` are not the same.")
        
        self.world_settings = self.world.get_settings()
        """Object containing some data about the simulation such as synchrony between client and server or rendering mode."""
        
        if agent:
            agent._world_model = self # backreference, if needed; the LunaticAgent sets this as well.
        
        if self.map is not None: # if this is set accesses CarlaDataProvider
            if map_inst and self.map != map_inst:
                raise ValueError("CarlaDataProvider.get_map() and passed map_inst are not the same.")
        elif map_inst:
            if isinstance(map_inst, carla.Map):
                self.map = map_inst
            else:
                logger.warning("Warning: Ignoring the given map as it is not a 'carla.Map'")
        if self.map is None:
            try:
                self.set_world(self.world) # CDP function
            except RuntimeError as error:
                print(f'RuntimeError: {error}')
                print('  The server could not send the OpenDRIVE (.xodr) file:')
                print('  Make sure it exists, has the same name of your town, and is correct.')
                sys.exit(1)
        
        self._config = config
        from agents.tools.config_creation import LaunchConfig         # circular import
        if not isinstance(args, (Mapping, DictConfig, LaunchConfig)): # TODO: should rather check for string like
            # Args is expected to be a string here
            # NOTE: This does NOT INCLUDE CLI OVERWRITES
            # When passed as path with directory
            config_dir, config_name = os.path.split(args)
            try:
                args = GameFramework.initialize_hydra(config_dir, config_name)
            except ValueError:
                # Hydra already initialized
                args = GameFramework.load_hydra_config(config_name)
            except Exception as e:
                print("Problem with", type(args), args)
                raise e
            args.externalActor = not (player is not None or agent is not None) # TEMP: Remove to force clean config.
        self._args : LaunchConfig = assure_type(LaunchConfig, args)
        
        self.hud: HUD = HUD(self._args.width, self._args.height, self.world)
        """The :py:class:`HUD` that is managed."""
        
        self.sync : Optional[bool] = self._args.sync
        """Set from :py:attr:`.LaunchConfig.sync`"""
        
        self.dim = (self._args.width, self._args.height)
        
        self.external_actor : bool = self._args.externalActor
        """Set from :py:attr:`.LaunchConfig.externalActor`"""
        
        self.actor_role_name : Optional[str] = self._args.rolename
        """Set from :py:attr:`.LaunchConfig.rolename`"""
        
        self._actor_filter = self._args.filter
        self._actor_generation: Literal[1, 2, "all"] = self._args.generation
        self._gamma = self._args.camera.gamma

        # TODO: Unify with CameraManager
        self.recording = False
        self._has_recorded = False
        self._recording_dirs = []
        self.recording_frame_num = 0
        self.recording_dir_num = 0
        
        # From manual controls; used client.start_recorder()
        #
        self.recording_enabled : bool = False
        """
        Indicator if :py:attr:`carla.Client` recording feature is on or off.
        
        Experimental & Untested!
        CTRL + R     : toggle recording of simulation (replacing any previous)
        CTRL + P     : start replaying last recorded simulation
        
        :meta private:
        """
        
        self.recording_start = 0
        """
        CTRL + +     : increments the start time of the replay by 1 second (+SHIFT = 10 seconds)
        CTRL + -     : decrements the start time of the replay by 1 second (+SHIFT = 10 seconds)
        
        :meta private:
        """
        
        if self.external_actor and (player is not None or agent is not None):
            raise ValueError("External actor cannot be used with player or agent.")
        if player is None and agent is not None:
            self.player = agent._vehicle
        elif player is not None and agent is not None:
            if player != agent._vehicle:
                raise ValueError("Passed `player` and `agent._vehicle` are not the same.")
            self.player = player
        else:
            # If player is None here, will set in in restart()
            self.player = player  # pyright: ignore[reportAttributeAccessIssue]

        assert self.player is not None or self.external_actor # Note: Former optional. Player set in restart

        self.collision_sensor : CollisionSensor = None   # type: ignore # set in restart
        self.lane_invasion_sensor : LaneInvasionSensor = None # type: ignore # set in restart
        self.gnss_sensor : Optional[GnssSensor] = None
        self.imu_sensor : Optional[IMUSensor] = None     # from interactive
        self.radar_sensor : Optional[RadarSensor] = None # from interactive
        self.camera_manager : CameraManager = None       # type: ignore # set in restart
        """
        Manages cameras for the user interface and :py:class:`.HUD`.
        """
        
        self._weather_presets = CarlaDataProvider.find_weather_presets()
        self._weather_index = 0
        self.weather: str = None
        """
        Name of currently used weather preset.
        See also: :py:class:`CarlaDataProvider.find_weather_presets()<CarlaDataProvider>`
        """
        
        self.actors: List[Union[carla.Actor, CustomSensorInterface]] = []
        """Actors attached to this instance for the user interface and :py:class:`.HUD`."""
        
        # From interactive:
        self.constant_velocity_enabled = NotImplemented  #: :meta private:
        self.show_vehicle_telemetry = False  #: :meta private: # enabled via KeyboardController
        self.doors_are_open: bool = False
        """
        Note:
            Only set over the KeyboardController, does not query the actor or simulation
            
        :meta private:
        """
        
        self.current_map_layer = 0
        self.map_layer_names = [
            carla.MapLayer.NONE,
            carla.MapLayer.Buildings,
            carla.MapLayer.Decals,
            carla.MapLayer.Foliage,
            carla.MapLayer.Ground,
            carla.MapLayer.ParkedVehicles,
            carla.MapLayer.Particles,
            carla.MapLayer.Props,
            carla.MapLayer.StreetLights,
            carla.MapLayer.Walls,
            carla.MapLayer.All
        ]
        # RSS
        # set in restart
        self.rss_sensor: Optional[RssSensor] = None
        self.rss_unstructured_scene_visualizer: RssUnstructuredSceneVisualizer = None # type: ignore[assignment]
        self.rss_bounding_box_visualizer: RssBoundingBoxVisualizer = None  # type: ignore[assignment]
        
        if config.rss:
            if config.rss.enabled and not self._actor_filter.startswith("vehicle."):
                print('Error: RSS only supports vehicles as ego. Disable RSS or use a vehicle filter for the actor.')
                sys.exit(1)
            if AD_RSS_AVAILABLE and config.rss.enabled:
                self._restrictor = carla.RssRestrictor()
            else:
                self._restrictor = None
        else:
            self._restrictor = None

            logger.info("Calling WorldModel.restart()")
        self._first_start = True
        """Indicate that restart was called for the first time."""
        self.restart()
        assert self.player is not None
        self._vehicle_physics = self.player.get_physics_control()
        self.world_tick_id = self.world.on_tick(self.hud.on_world_tick)
        
        if CarlaDataProvider._traffic_light_map is None:
            logger.error("Traffic light map not set at this point") # should not have happened
            CarlaDataProvider.set_world(self._world)
        elif not CarlaDataProvider._traffic_light_map:
            logger.error("Traffic light map is empty") # should not have happened
            CarlaDataProvider.prepare_map()

    def rss_set_road_boundaries_mode(self,
                                     road_boundaries_mode: Optional[Union['RssRoadBoundariesModeAlias',
                                                                          carla.RssRoadBoundariesMode,
                                                                          bool]]=None) -> None:
        """
        Choose wether or not to use the RSS road boundaries feature.
        
        Toggles: :py:attr:`.RssSettings.use_stay_on_road_feature`
        
        Parameters:
            road_boundaries_mode: If :python:`None`, uses the value from the config.
                If :python:`True`, sets to :py:attr:`carla.RssRoadBoundariesMode.On`.
                If :python:`False`, sets to :py:attr:`carla.RssRoadBoundariesMode.Off`.
                
        See Also:
            - :py:class:`carla.RssSensor`
        """
        # Called from KeyboardControl
        if road_boundaries_mode is None:
            road_boundaries_mode = self._config.rss.use_stay_on_road_feature
        else:
            # Depending on AD_RSS_AVAILABLE this uses carla.RssRoadBoundariesMode or the alias
            if road_boundaries_mode:
                self._config.rss.use_stay_on_road_feature = RssRoadBoundariesMode.On
            else:
                self._config.rss.use_stay_on_road_feature = RssRoadBoundariesMode.Off
        if self.rss_sensor:
            self.rss_sensor.sensor.road_boundaries_mode = (carla.RssRoadBoundariesMode.On
                                                           if road_boundaries_mode
                                                           else carla.RssRoadBoundariesMode.Off)
        else:
            print("Warning: RSS Road Boundaries Mode not set. RSS sensor not found.")

    def toggle_pause(self):
        """
        Toggle pause_simulation from the KeyboardControls.
        
        :meta private:
        """
        settings = self.world.get_settings()
        self.pause_simulation(not settings.synchronous_mode)

    def pause_simulation(self, pause: bool):
        """
        Pauses the simulation by setting the world to synchronous mode.
        
        Attention:
            Only works reliable in **asynchronous mode** (:py:attr:`sync=False <.LaunchConfig.sync>`)
            and might lead to unexpected behavior in synchronous mode.
        """
        if self._args.sync:
            logger.warning("Pause simulation only works in asynchronous mode.")
        
        settings = self.world.get_settings()
        if pause and not settings.synchronous_mode:
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = 0.05
            self.world.apply_settings(settings)
        elif not pause and settings.synchronous_mode:
            settings.synchronous_mode = False
            settings.fixed_delta_seconds = None
            self.world.apply_settings(settings)

    @staticmethod
    def _find_external_actor(world: carla.World,
                             role_name: str,
                             actor_list: Optional[carla.ActorList]=None) -> Optional[carla.Actor]:
        """
        Looks to find an actor with a matching **role_name**.
        """
        player = None
        for actor in actor_list or world.get_actors():
            if actor.attributes.get('role_name') == role_name:
                if player is not None:
                    logger.error("Multiple actors with role_name `%s` found. id: %s. "
                                 "Returning the first one found.", role_name, actor.id)
                else:
                    player = actor
        return player

    def _wait_for_external_actor(self, timeout=20, sleep=3) -> carla.Actor:
        """
        Does not resume the script until an external actor with the role name is found.
        
        Raises:
            AssertionError: If :py:attr:`actor_role_name` is not set.
            SystemExit: If the actor is not found within the time period.
        """
        assert self.actor_role_name
        import time
        self.tick_server_world() # Tick the world?
        start = time.time()
        t = start
        while t < start + timeout:
            player = self._find_external_actor(self.world, self.actor_role_name)
            if player is not None:
                return player
            logger.info("...External actor not found. Waiting to find external actor named `%s`",
                        self.actor_role_name)
            time.sleep(sleep) # Note if on same thread, nothing will happen. Put function into thread?
            self.tick_server_world() # Tick the world?
            t = time.time()
        logger.error(f"External actor `{self.actor_role_name}` not found. Exiting...")
        print(f"External actor `{self.actor_role_name}` not found. Exiting...")
        sys.exit(1)

    def restart(self):
        """
        Restart the world and sets up the :py:class:`.HUD` sensors.
        If :py:attr:`player` is not set or :py:attr:`external_actor` is set,
        looks for an actor with the role name, or spawns a new actor.
        
        Note:
            Called during :py:meth:`__init__`.
        """
        # Keep same camera config if the camera manager exists.
        cam_index = assure_type(int, self.camera_manager.index
                                          if self.camera_manager is not None
                                          else 0)
        cam_pos_id = (self.camera_manager.transform_index
                      if self.camera_manager is not None
                      else 0)
        if self.external_actor:
            # Check whether there is already an actor with defined role name
            if not self.actor_role_name:
                raise ValueError("When using external actor, rolename must be set.")
            actor_list = self.world.get_actors() # In sync mode the actor list could be empty
            external_actor = self._find_external_actor(self.world, self.actor_role_name, actor_list)
            if self.player is None:
                if external_actor:
                    self.player = assure_type(carla.Vehicle, external_actor)
                else:
                    self.player = assure_type(carla.Vehicle,
                                    self._wait_for_external_actor(timeout=20))
            elif external_actor and self.player.id != external_actor.id: # NOTE: even with same id different instances and hashes.
                logger.warning("External actor found with role_name `%s` but different id. "
                               "Keeping the current actor (%s) and ignoring the external actor (%s)",
                               self.actor_role_name, self.player.id, external_actor.id)
            if TYPE_CHECKING:
                self.player = assure_type(carla.Vehicle, self.player)
            
        else:
            # Get a random blueprint.
            if self.player is None or self.camera_manager is not None:
                # First pass without a player or second pass -> new player
                blueprint: carla.ActorBlueprint = assure_type(carla.ActorBlueprint,
                    random.choice(get_actor_blueprints(self._actor_filter, self._actor_generation)))  # type: ignore[arg-type]
                blueprint.set_attribute('role_name', self.actor_role_name) # type: ignore
                if blueprint.has_attribute('color'):
                    color = random.choice(blueprint.get_attribute('color').recommended_values)
                    blueprint.set_attribute('color', color)
                # From Interactive:
                if blueprint.has_attribute('terramechanics'): # For Tire mechanics/Physics? # Todo is that needed?
                    blueprint.set_attribute('terramechanics', 'false')
                if blueprint.has_attribute('driver_id'):
                    driver_id = random.choice(blueprint.get_attribute('driver_id').recommended_values)
                    blueprint.set_attribute('driver_id', driver_id)
                if blueprint.has_attribute('is_invincible'):
                    blueprint.set_attribute('is_invincible', 'true')
            
            # TODO: Make this a config option to choose automatically.
            # set the max speed
            #if blueprint.has_attribute('speed'):
            #    self.player_max_speed = float(blueprint.get_attribute('speed').recommended_values[1])
            #    self.player_max_speed_fast = float(blueprint.get_attribute('speed').recommended_values[2])

            # Spawn the player.
            if self.player is not None:
                spawn_point = self.player.get_transform()
                spawn_point.location.z += 2.0
                spawn_point.rotation.roll = 0.0
                spawn_point.rotation.pitch = 0.0
                if self.camera_manager is not None: # None at first start; not None if player was already set before
                    self.destroy()
                    self.player = assure_type(carla.Vehicle, self.world.try_spawn_actor(blueprint, spawn_point))
                self.modify_vehicle_physics(self.player)
            while self.player is None:
                if not self.map.get_spawn_points():
                    print('There are no spawn points available in your map/town.')
                    print('Please add some Vehicle Spawn Point to your UE4 scene.')
                    sys.exit(1)
                spawn_points  = self.map.get_spawn_points()
                spawn_point : carla.Transform = random.choice(spawn_points) if spawn_points else carla.Transform() # type: ignore
                self.player = assure_type(carla.Vehicle,
                                          self.world.try_spawn_actor(blueprint, spawn_point))
                # From Interactive:
                # See: https://carla.readthedocs.io/en/latest/tuto_G_control_vehicle_physics/
                self.show_vehicle_telemetry = False
                self.modify_vehicle_physics(self.player)

        # Clean external actors restarting a second time
        if self.external_actor and self._args.restart_clean_sensors is not False \
           and not self._first_start or self._args.restart_clean_sensors is True:
            ego_sensors : List[carla.Actor] = []
            for actor in self.world.get_actors():
                if actor.parent == self.player:
                    ego_sensors.append(actor)

            # Remove all old sensors
            for ego_sensor in ego_sensors:
                if ego_sensor is not None:
                    ego_sensor.destroy()

        # Set up the sensors.
        self.collision_sensor = CollisionSensor(self.player, self.hud)
        self.lane_invasion_sensor = LaneInvasionSensor(self.player, self.hud)
        self.gnss_sensor = None # GnssSensor(self.player) # TODO: make it optional
        self.imu_sensor = None  # IMUSensor(self.player)
        self.actors.extend([
            self.collision_sensor,
            self.lane_invasion_sensor,
        ])
        if self.gnss_sensor:
            self.actors.append(self.gnss_sensor)
        if self.imu_sensor:
            self.actors.append(self.imu_sensor)
        
        self.camera_manager = CameraManager(self.player, self.hud, self._args)
        self.camera_manager.transform_index = cam_pos_id
        self.camera_manager.set_sensor(cam_index, notify=False)
        
        actor_type = get_actor_display_name(self.player)
        self.hud.notification(text=actor_type)
        
        self.rss_unstructured_scene_visualizer = RssUnstructuredSceneVisualizer(self.player,
                                                                                self.world,
                                                                                self.dim,
                                                                                gamma_correction=self._gamma) # TODO: use args instead of gamma
        self.rss_bounding_box_visualizer = RssBoundingBoxVisualizer(self.dim,
                                                                    self.world,
                                                                    self.camera_manager.sensor)
        if AD_RSS_AVAILABLE and self._config.rss and self._config.rss.enabled:
            log_level = self._config.rss.log_level
            if not isinstance(log_level, carla.RssLogLevel):
                try:
                    if isinstance(log_level, str):
                        log_level = carla.RssLogLevel.names[log_level]
                    else:
                        log_level = carla.RssLogLevel(log_level)
                except Exception as e:
                    raise KeyError("Could not convert '{log_level}' to RssLogLevel must be in {valid}".format(
                                    log_level=log_level, valid=list(carla.RssLogLevel.names.keys()))
                    ) from e
                logger.info("Carla Log level was not a RssLogLevel")
            self.rss_sensor = RssSensor(self.player,
                                    self.rss_unstructured_scene_visualizer,
                                    self.rss_bounding_box_visualizer,
                                    self.hud.rss_state_visualizer,
                                    visualizer_mode=self._config.rss.debug_visualization_mode,
                                    log_level=log_level)
            self.rss_set_road_boundaries_mode(self._config.rss.use_stay_on_road_feature)
        else:
            self.rss_sensor = None
        self._first_start = False
        self.tick_server_world()

    def tick_server_world(self) -> "int | carla.WorldSnapshot | None":
        """
        When :py:attr:`.LaunchConfig.handle_ticks` is :python:`True`
        uses :external_py_meth:`carla.World.tick` or :external_py_meth:`carla.World.wait_for_tick`
        depending on :py:attr:`.LaunchConfig.sync`.
        """
        if self._args.handle_ticks:
            if self.sync:
                return self.world.tick()
            return self.world.wait_for_tick()

    #def tick(self, clock):
    #    self.hud.tick(self.player, clock) # RSS example. TODO: Check which has to be used!

    def tick(self, clock: "pygame.time.Clock"):
        """Method for every tick"""
        self.hud.tick(self, clock, InformationManager.obstacles)

    def next_weather(self, reverse: bool =False) -> None:
        """Get next weather setting"""
        self._weather_index += -1 if reverse else 1
        self._weather_index %= len(self._weather_presets)
        preset = self._weather_presets[self._weather_index]
        self.hud.notification(f'Weather: {preset[1]}')
        self.player.get_world().set_weather(preset[0])
        self.weather = preset[1]

    def next_map_layer(self, reverse: bool =False) -> None:
        self.current_map_layer += -1 if reverse else 1
        self.current_map_layer %= len(self.map_layer_names)
        selected = self.map_layer_names[self.current_map_layer]
        self.hud.notification(f'LayerMap selected: {selected}')

    def load_map_layer(self, unload: bool=False):
        selected = self.map_layer_names[self.current_map_layer]
        if unload:
            self.hud.notification(f'Unloading map layer: {selected}')
            self.world.unload_map_layer(selected)
        else:
            self.hud.notification(f'Loading map layer: {selected}')
            self.world.load_map_layer(selected)

    def toggle_recording(self):
        """
        Start recording images from the camera output.
        
        Saved in
        :py:attr:`LaunchConfig.camera.recorder.output_path <.CameraConfig.RecorderSettings.output_path>`
        with the current frame number.
        """
        if not self.recording:
            self._has_recorded = True
            dir_name, filename = os.path.split(self._args.camera.recorder.output_path)
            try:
                dir_name_formatted = dir_name % self.recording_dir_num
            except TypeError:
                dir_name += "%04d"
                dir_name_formatted = dir_name % self.recording_dir_num
            while os.path.exists(dir_name_formatted):
                self.recording_dir_num += 1
                dir_name_formatted = dir_name % self.recording_dir_num
            self.recording_file_format = os.path.join(dir_name, filename) # keep unformatted.
            self.recording_frame_num = 0
            os.makedirs(dir_name_formatted)
            self.hud.notification(f'Started recording (folder: {dir_name_formatted})')
            self._recording_dirs.append(dir_name_formatted)
        else:
            dir_name_formatted = os.path.split(self.recording_file_format)[0] % self.recording_dir_num
            self.hud.notification(f'Recording finished (folder: {dir_name_formatted})')
        
        self.recording = not self.recording
    
    def toggle_radar(self):
        """Adds or destroys a radar sensor for the user interface"""
        if self.radar_sensor is None:
            self.radar_sensor = RadarSensor(self.player)
        elif self.radar_sensor.sensor is not None:
            self.radar_sensor.sensor.destroy()
            self.radar_sensor = None

    def modify_vehicle_physics(self, actor : carla.Vehicle):
        # If actor is not a vehicle, we cannot use the physics control
        try:
            physics_control = actor.get_physics_control()
            physics_control.use_sweep_wheel_collision = True
            actor.apply_physics_control(physics_control)
        except Exception:
            pass

    def finalize_render(self, display : pygame.Surface):
        """
        Draws the HUD and saves the image if recording is enabled.
        
        Assumes render(..., finalize=False) was called before,
        use this function if you want to render something in between.
        """
        self.hud.render(display)
        if self.recording:
            try:
                pygame.image.save(display, self.recording_file_format % (self.recording_dir_num, self.recording_frame_num))
            except Exception as e:
                logger.error("Could not save image format: `%s` % (self.recording_dir_num, self.recording_frame_num): %s", self.recording_file_format, e)
            self.recording_frame_num += 1

    def render(self, display : pygame.Surface, finalize:bool=True):
        """
        Render world
        
        Recording should be done at the end of the render method,
        however camera_manager.render is called first to render the camera.
        
        Call with finalize=False to only render the camera.
        
        Afterwards applying other render features call `finalize_render`
        to draw the HUD and save the image if recording is enabled.
        """
        self.camera_manager.render(display)
        self.rss_bounding_box_visualizer.render(display, self.camera_manager.current_frame)
        self.rss_unstructured_scene_visualizer.render(display)
        if finalize:
            self.finalize_render(display)

    def destroy_sensors(self):
        """Destroy sensors"""
        if self.rss_sensor:
            self.rss_sensor.destroy()
            self.rss_sensor = None
        if self.rss_unstructured_scene_visualizer:
            self.rss_unstructured_scene_visualizer.destroy()
            self.rss_unstructured_scene_visualizer = None  # type: ignore[assignment]
        if self.camera_manager is not None:
            self.camera_manager.destroy()
            self.camera_manager = None  # type: ignore[assignment]
        if self.radar_sensor is not None:
            self.toggle_radar()  # destroys it if not None

    def destroy(self, destroy_ego: bool=False):
        """
        Destroys all actors
        
        Parameters:
            destroy_ego: If True, will destroy the :py:attr:`player` as well. Else assume that it
                is destroyed by someone else.
        """
        # stop from ticking
        if self.world_tick_id and self.world:
            self.world.remove_on_tick(self.world_tick_id)
        self.destroy_sensors()
        if destroy_ego and self.player not in self.actors: # do not destroy external actors.
            logger.debug("Adding player to destruction list.")
            self.actors.append(self.player)
        elif not destroy_ego and self.player in self.actors:
            logger.warning("destroy_ego=False, but player is in actors list. "
                           "Destroying the actor from within WorldModel.destroy.")
        
        #logger.info("to destroy %s", list(map(str, self.actors)))
        # Batch destroy in one simulation step
        real_actors: Sequence[carla.Actor] = [actor for actor in self.actors
                                              if isinstance(actor, carla.Actor)]
        GameFramework.destroy_actors(real_actors)
        
        # e.g. CustomSensorInterface
        other_actors = [actor for actor in self.actors
                        if not isinstance(actor, carla.Actor)]
        while other_actors:
            actor = other_actors.pop(0)
            if actor is not None:
                print("destroying actor: " + str(actor), end=" destroyed=")
                try:
                    actor.stop()
                except AttributeError as e:
                    logger.debug("Error with actor {}: {}", actor, e)
                try:
                    x = actor.destroy() # Non carla instances
                    print(x)
                except RuntimeError:
                    logger.warning("Could not destroy actor: " + str(actor))
        self.actors.clear()
        if self._args.handle_ticks and self.get_world():
            self.get_world().tick()
            
        if self._has_recorded:
            runtime_dir = GameFramework.get_hydra_config().runtime.output_dir
            for dir_name_formatted in self._recording_dirs:
                dirname = os.path.split(dir_name_formatted)[1]
                os.system(f'ffmpeg -an -sn -i "{dir_name_formatted}/%08d.bmp" -framerate 1 -vcodec mpeg4 -r 60 "{os.path.join(runtime_dir, dirname)}.avi"')  # noqa: E501
                print(f"Recording saved in {os.path.join(runtime_dir, dirname)}.avi")
            
        
    def rss_check_control(self, vehicle_control : carla.VehicleControl) -> Union[carla.VehicleControl, None]:
        """
        Checks the vehicle control against the RSS restrictions and possibly proposes an alternative.
        """
        self.hud.original_vehicle_control = vehicle_control
        self.hud.restricted_vehicle_control = vehicle_control
        if not AD_RSS_AVAILABLE or not self.rss_sensor:
            return None
        
        if (self.rss_sensor.log_level <= carla.RssLogLevel.warn
            and self.rss_sensor.ego_dynamics_on_route
            and not self.rss_sensor.ego_dynamics_on_route.ego_center_within_route):
            logger.warning("RSS: Not on route! " +  str(self.rss_sensor.ego_dynamics_on_route)[:97] + "...")
        # Is there a proper response?
        rss_proper_response = self.rss_sensor.proper_response if self.rss_sensor and self.rss_sensor.response_valid else None
        if rss_proper_response:
            # adjust the controls
            proposed_vehicle_control = self._restrictor.restrict_vehicle_control(  # pyright: ignore[reportOptionalMemberAccess]
                            vehicle_control,
                            rss_proper_response,
                            self.rss_sensor.ego_dynamics_on_route,
                            self._vehicle_physics)
            self.hud.restricted_vehicle_control = proposed_vehicle_control
            self.hud.allowed_steering_ranges = self.rss_sensor.get_steering_ranges()
            return proposed_vehicle_control
        return None
