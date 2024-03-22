# Official Example from examples/automatic-control.py
# NOTE it might has to use synchonous_mode
from collections.abc import Mapping
import os
import sys
from typing import Any, ClassVar, Dict, List, Optional, Union, cast as assure_type, TYPE_CHECKING
import weakref

import numpy as np
from omegaconf import DictConfig, OmegaConf
import pygame

import carla
import numpy.random as random
from agents.tools.lunatic_agent_tools import AgentDoneException, ContinueLoopException
from classes.HUD import HUD

from classes.camera_manager import CameraManager
from classes.carla_originals.sensors import CollisionSensor, GnssSensor, IMUSensor, LaneInvasionSensor, RadarSensor

from classes.rule import Rule
from classes.rss_sensor import RssSensor, AD_RSS_AVAILABLE
from classes.rss_visualization import RssUnstructuredSceneVisualizer, RssBoundingBoxVisualizer
from classes.keyboard_controls import RSSKeyboardControl

if TYPE_CHECKING:
    from agents.tools.config_creation import LunaticAgentSettings, LaunchConfig
    from agents.lunatic_agent import LunaticAgent

from classes.HUD import get_actor_display_name
from launch_tools.blueprint_helpers import get_actor_blueprints
from agents.tools.logging import logger

try:
    from scenario_runner.srunner.scenariomanager.carla_data_provider import CarlaDataProvider # type: ignore
    logger.info("Using CarlaDataProvider from srunner module.")
except ImportError:
    try:
        from srunner.scenariomanager.carla_data_provider import CarlaDataProvider
    except ImportError:
        logger.warning("CarlaDataProvider not available: ScenarioManager (srunner module) not found in path. Make sure it is in your PYTHONPATH or PATH variable.")
        CarlaDataProvider = None

class AccessCarlaDataProviderMixin:
    """Mixin class that delegates to CarlaDataProvider if available to keep in Sync."""
    
    if CarlaDataProvider is not None:
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
            if CarlaDataProvider.get_map() != value:
                raise ValueError("CarlaDataProvider.get_map() and passed map are not the same.")
            # Do nothing as map is set when using get_map or set_world
    else:
        __client: carla.Client = None # type: ignore
        __map: carla.Map = None  # type: ignore
        __world: carla.World = None # type: ignore
        
        @property
        def client(self) -> carla.Client:
            return AccessCarlaDataProviderMixin.__client
        
        @client.setter
        def client(self, value: carla.Client):
            AccessCarlaDataProviderMixin.__client = value
            
        @property
        def world(self) -> carla.World:
            return AccessCarlaDataProviderMixin.__world
        
        @world.setter
        def world(self, value: carla.World):
            AccessCarlaDataProviderMixin.__world = value
            
        @property
        def map(self) -> carla.Map:
            return AccessCarlaDataProviderMixin.__map
        
        @map.setter
        def map(self, value: carla.Map):
            AccessCarlaDataProviderMixin.__map = value

# ==============================================================================
# -- Game Framework ---------------------------------------------------------------
# ==============================================================================

class GameFramework(AccessCarlaDataProviderMixin):
    clock : ClassVar[pygame.time.Clock]
    display : ClassVar[pygame.Surface]
    controller: "weakref.proxy[RSSKeyboardControl]" # TODO: is proxy a good idea, must be set bound outside
    
    def __init__(self, args: "LaunchConfig", config=None, timeout=10.0, worker_threads:int=0, *, map_layers=carla.MapLayer.All):
        if args.seed:
            random.seed(args.seed)
            np.random.seed(args.seed)
        self._args = args
        self.clock, self.display = self.init_pygame(args)
        self.world_settings = self.init_carla(args, timeout, worker_threads, map_layers=map_layers)
        self.config = config
        self.agent = None
        self.world_model = None
        self.controller = None
        
        self.debug = self.world.debug
        self.continue_loop = True
        
        self.cooldown_framework = Rule.CooldownFramework() # used in context manager. # NOTE: Currently can be constant
        
    @staticmethod
    def init_pygame(args):
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()
        display = pygame.display.set_mode(
            (args.width, args.height),
            pygame.HWSURFACE | pygame.DOUBLEBUF)
        return clock, display
    
    def init_carla(self, args, timeout=10.0, worker_threads:int=0, *, map_layers=carla.MapLayer.All):
        if self.client is None: # TODO: Note this maybe prevents usage of two different ports
            self.client = carla.Client(args.host, args.port, worker_threads)
            self.client.set_timeout(timeout)
        else:
            assert isinstance(self.client, carla.Client)
        
        if self.world is None:
            self.world = self.client.get_world()
        else:
            assert isinstance(self.world, carla.World)
            
        if self.map is None:
            self.map = self.world.get_map()
        else:
            assert isinstance(self.map, carla.Map)
        
        world_name = args.map
        if world_name and self.map.name != "Carla/Maps/" + world_name:
            logger.info(f"Loading world: {world_name}")
            self.world = self.client.load_world(world_name, map_layers=map_layers)
            if not self.map: # Note: CarlaDataProvider.set_world handles this.
                self.map = self.world.get_map()
        else:
            logger.debug("skipped loading world, already loaded. map_layers ignored.") # todo: remove?
        
        # Apply world settings
        if args.sync is not None: # Else let this be handled by someone else
            if args.sync:
                logger.debug("Using synchronous mode.")
                # apply synchronous mode if wanted
                world_settings = self.world.get_settings()
                world_settings.synchronous_mode = True
                world_settings.fixed_delta_seconds = 1/args.fps # 0.05
                self.world.apply_settings(world_settings)
            else:
                logger.debug("Using asynchronous mode.")
                world_settings = self.world.get_settings()
        else:
            world_settings = self.world.get_settings()
            print("World Settings:", world_settings)
        
        return world_settings
    
    def init_traffic_manager(self) -> carla.TrafficManager:
        traffic_manager = self.client.get_trafficmanager()
        if self._args.sync:
            traffic_manager.set_synchronous_mode(True)
        traffic_manager.set_hybrid_physics_mode(True) # Note default 50m
        traffic_manager.set_hybrid_physics_radius(50.0) # TODO: make a config variable
        return traffic_manager
    
    def set_config(self, config:DictConfig):
        self.config = config
    
    def make_world_model(self, config:"LunaticAgentSettings", player:carla.Vehicle = None, map_inst:Optional[carla.Map]=None):
        self.world_model = WorldModel(config, self._args, player=player)
        self.world_model.game_framework = weakref.proxy(self)
        return self.world_model
    
    def make_controller(self, world_model, controller_class=RSSKeyboardControl, **kwargs):
        controller = controller_class(world_model, config=self.config, clock=self.clock, **kwargs)
        self.controller: controller_class = weakref.proxy(controller) # note type not correct. TODO: proxy a good idea?
        return controller # NOTE: does not return the proxy object.
    
    def set_controller(self, controller):
        self.controller = controller
    
    def parse_rss_controller_events(self, final_controls:carla.VehicleControl):
        return self.controller.parse_events(final_controls)

    def init_agent_and_interface(self, ego, agent_class:"LunaticAgent", config:"LunaticAgentSettings"=None, overwrites:Optional[Dict[str, Any]]=None):
        self.agent, self.world_model, self.global_planner = agent_class.create_world_and_agent(ego, self.world, self._args, map_inst=self.map, config=config, overwrites=overwrites)
        self.config = self.agent.config
        controller = self.make_controller(self.world_model, RSSKeyboardControl, start_in_autopilot=False) # Note: stores weakref to controller
        self.world_model.game_framework = weakref.proxy(self)
        return self.agent, self.world_model, self.global_planner, controller

    def __enter__(self):
        if self.agent is None:
            raise ValueError("Agent not initialized.")
        if self.world_model is None:
            raise ValueError("World Model not initialized.")
        if self.controller is None:
            raise ValueError("Controller not initialized.")
        
        self.clock.tick() # self.args.fps)
        if self._args.handle_ticks:
            if self._args.sync is not None:
                if self._args.sync:
                    self.world_model.world.tick()
                else:
                    self.world_model.world.wait_for_tick()
        return self
    
    def render_everything(self):
        """Update render and hud"""
        self.world_model.tick(self.clock) # TODO # CRITICAL maybe has to tick later
        self.world_model.render(self.display, finalize=False)
        self.controller.render(self.display)
        options = OmegaConf.select(self._args, "camera.hud.data_matrix", default=None)
        if options and self.agent:
            self.agent.render_road_matrix(self.display, options)
        self.world_model.finalize_render(self.display)
        
    @staticmethod
    def skip_rest_of_loop(message="GameFrameWork.end_loop"):
        """
        Terminates the current iteration and exits the GameFramework.
        
        NOTE: It is the users responsibility to manage the agent & local planner
        before calling this function.
        
        Raises: ContinueLoopException
        """
        # TODO: add option that still allows for rss.
        raise ContinueLoopException(message)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cooldown_framework.__exit__(exc_type, exc_val, exc_tb)
        self.render_everything()
        pygame.display.flip()
        
        if isinstance(exc_val, AgentDoneException):
            self.continue_loop = False
        #elif exc_type is None or issubclass(exc_type, ContinueLoopException):
        #    pass

# ==============================================================================
# -- World ---------------------------------------------------------------
# ==============================================================================

class WorldModel(AccessCarlaDataProviderMixin):
    """ Class representing the surrounding environment """

    controller : Optional[RSSKeyboardControl] = None# Set when controller is created. Uses weakref.proxy
    game_framework : Optional[GameFramework] = None # Set when world created via GameFramework. Uses weakref.proxy

    def get_blueprint_library(self):
        return self.world.get_blueprint_library()

    def __init__(self, config : "LunaticAgentSettings", args:"Union[LaunchConfig, Mapping, os.PathLike]"="./conf/launch_config.yaml", agent:"LunaticAgent" = None, *, carla_world: Optional[carla.World]=None, player: Optional[carla.Vehicle] = None, map_inst:Optional[carla.Map]=None):
        """Constructor method"""
        # Set World
        if self.world is None:
            if carla_world is None:
                raise ValueError("CarlaDataProvider not available and `carla_world` not passed.")
            self.world = carla_world
        elif carla_world is not None and self.world != carla_world:
            raise ValueError("CarlaDataProvider.get_world() and passed `carla_world` are not the same.")
        self.world_settings = self.world.get_settings()
        
        # TEMP:
        if agent:
            agent._world_model = self
        
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
                self.map = self.world.get_map()
            except RuntimeError as error:
                print('RuntimeError: {}'.format(error))
                print('  The server could not send the OpenDRIVE (.xodr) file:')
                print('  Make sure it exists, has the same name of your town, and is correct.')
                sys.exit(1)
        
        self._config = config
        if not isinstance(args, Mapping):
            # Args is expeced to be a string here
            # NOTE: THis does NOT INCLUDE CLI OVERWRITES
            args = OmegaConf.load(args)
            args.externalActor = not (player is not None or agent is not None) # TEMP: Remove to force clean config.
        self._args : LaunchConfig = args
        self.hud = HUD(args.width, args.height, self.world)
        self.sync : bool = args.sync
        self.dim = (args.width, args.height)
        self.external_actor : bool = args.externalActor
        self.actor_role_name : Optional[str] = args.rolename
        self._actor_filter = args.filter
        self._actor_generation = args.generation
        self._gamma = args.camera.gamma

        # TODO: Unify with CameraManager
        self.recording = False
        self.recording_frame_num = 0
        self.recording_dir_num = 0
        
        # From manual controls
        self.recording_enabled = False
        self.recording_start = 0
        
        if self.external_actor and (player is not None or agent is not None):
            raise ValueError("External actor cannot be used with player or agent.")
        if player is None and agent is not None:
            self.player = agent._vehicle
        elif player is not None and agent is not None:
            if player != agent._vehicle:
                raise ValueError("Passed `player` and `agent._vehicle` are not the same.")
            self.player = player
        else:
            self.player = player

        assert self.player is not None or self.external_actor # Note: Former optional. PLayer set in restart

        self.collision_sensor = None
        self.lane_invasion_sensor = None
        self.gnss_sensor = None
        self.imu_sensor = None   # from interactive
        self.radar_sensor = None # from interactive
        self.camera_manager = None
        
        self._weather_presets = find_weather_presets()
        self._weather_index = 0
        self.weather = None
        

        self.actors = []
        
        # From interactive:
        self.constant_velocity_enabled = False
        self.show_vehicle_telemetry = False
        self.doors_are_open = False
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
        self.rss_sensor = None # set in restart
        self.rss_unstructured_scene_visualizer = None
        self.rss_bounding_box_visualizer = None
        
        if config.rss.enabled and not self._actor_filter.startswith("vehicle."):
            print('Error: RSS only supports vehicles as ego.')
            sys.exit(1)
        if config.rss.enabled and AD_RSS_AVAILABLE:
            self._restrictor = carla.RssRestrictor()
        else:
            self._restrictor = None

        logger.debug("Calling WorldModel.restart()")
        self.restart()
        self._vehicle_physics = self.player.get_physics_control()
        self.world_tick_id = self.world.on_tick(self.hud.on_world_tick)

    def rss_set_road_boundaries_mode(self, road_boundaries_mode: Optional[Union[bool, "carla.RssRoadBoundariesMode"]]=None):
        # Called from KeyboardControl
        if road_boundaries_mode is None:
            road_boundaries_mode = self._config.rss.use_stay_on_road_feature
        else:
            if AD_RSS_AVAILABLE:
                self._config.rss.use_stay_on_road_feature = carla.RssRoadBoundariesMode.On if road_boundaries_mode else carla.RssRoadBoundariesMode.Off
            else:
                self._config.rss.use_stay_on_road_feature = bool(road_boundaries_mode)
        if self.rss_sensor:
            self.rss_sensor.sensor.road_boundaries_mode = carla.RssRoadBoundariesMode.On if road_boundaries_mode else carla.RssRoadBoundariesMode.Off
        else:
            print("Warning: RSS Road Boundaries Mode not set. RSS sensor not found.")

    def toggle_pause(self):
        settings = self.world.get_settings()
        self.pause_simulation(not settings.synchronous_mode)

    def pause_simulation(self, pause):
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
    def _find_external_actor(world:carla.World, role_name:str, actor_list: Optional[carla.ActorList]=None) -> Union[None, carla.Actor]:
        for actor in actor_list or world.get_actors():
            if actor.attributes.get('role_name') == role_name:
                return actor
        return None

    def _wait_for_external_actor(self, timeout=20, sleep=3) -> carla.Actor:
        import time
        self.tick_server_world() # Tick the world?
        start = time.time()
        t = start
        while t < start + timeout:
            player = self._find_external_actor(self.world, self.actor_role_name)
            if player is not None:
                return player
            logger.info("...External actor not found. Waiting to find external actor named `%s`", self.actor_role_name)
            time.sleep(sleep) # Note if on same thread, nothing will happen. Put function into thread?
            self.tick_server_world() # Tick the world?
            t = time.time()
        logger.error("External actor `%s` not found. Exiting...", self.actor_role_name)
        print("External actor `%s` not found. Exiting..." % self.actor_role_name)
        sys.exit(1)

    def restart(self):
        """Restart the world"""
        # Keep same camera config if the camera manager exists.
        # TODO: unsure if correct
        cam_index = self.camera_manager.index if self.camera_manager is not None else 0
        cam_pos_id = self.camera_manager.transform_index if self.camera_manager is not None else 0
        if self.external_actor:
            # Check whether there is already an actor with defined role name
            actor_list = self.world.get_actors() # In sync mode the actor list could be empty
            self.player = self._find_external_actor(self.world, self.actor_role_name, actor_list)
            if self.player is None:
                self.player = assure_type(carla.Vehicle, 
                                self._wait_for_external_actor(timeout=20))
            # TODO: Make this more nicer, see maybe scenario runner how to wait for spawn. Only do tick if in sync mode. Async wait.
            elif TYPE_CHECKING:
                self.player = assure_type(carla.Vehicle, self.player)
        else:
            # Get a random blueprint.
            blueprint : carla.ActorBlueprint = random.choice(get_actor_blueprints(self.world, self._actor_filter, self._actor_generation))
            blueprint.set_attribute('role_name', self.actor_role_name)
            if blueprint.has_attribute('color'):
                color = random.choice(blueprint.get_attribute('color').recommended_values)
                blueprint.set_attribute('color', color)
            # From Interactive:
            if blueprint.has_attribute('terramechanics'): # For Tire mechanics/Physics? # Todo is that needed?
                blueprint.set_attribute('terramechanics', 'true')
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
                if self.camera_manager is not None: # TODO: Validate, remove line
                    self.destroy()
                    self.player = assure_type(carla.Vehicle, self.world.try_spawn_actor(blueprint, spawn_point))
                self.modify_vehicle_physics(self.player)
            while self.player is None:
                if not self.map.get_spawn_points():
                    print('There are no spawn points available in your map/town.')
                    print('Please add some Vehicle Spawn Point to your UE4 scene.')
                    sys.exit(1)
                spawn_points = self.map.get_spawn_points()
                spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
                self.player = assure_type(carla.Vehicle, self.world.try_spawn_actor(blueprint, spawn_point))
                # From Interactive:
                # See: https://carla.readthedocs.io/en/latest/tuto_G_control_vehicle_physics/            
                self.show_vehicle_telemetry = False
                self.modify_vehicle_physics(self.player)

        if self.external_actor:
            ego_sensors : List[carla.Actor] = []
            for actor in self.world.get_actors():
                if actor.parent == self.player:
                    ego_sensors.append(actor)

            for ego_sensor in ego_sensors: # TODO: Why we do this
                if ego_sensor is not None:
                    ego_sensor.destroy()

        # Set up the sensors.
        self.collision_sensor = CollisionSensor(self.player, self.hud)
        self.lane_invasion_sensor = LaneInvasionSensor(self.player, self.hud)
        self.gnss_sensor = None # GnssSensor(self.player) # TODO: make it optional
        self.imu_sensor = None # IMUSensor(self.player)
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
        self.hud.notification(actor_type)
        
        self.rss_unstructured_scene_visualizer = RssUnstructuredSceneVisualizer(self.player, self.world, self.dim, gamma_correction=self._gamma) # TODO: use args instead of gamma
        self.rss_bounding_box_visualizer = RssBoundingBoxVisualizer(self.dim, self.world, self.camera_manager.sensor)
        if self._config.rss.enabled and AD_RSS_AVAILABLE:
            self.rss_sensor = RssSensor(self.player, self.world,
                                    self.rss_unstructured_scene_visualizer, self.rss_bounding_box_visualizer, self.hud.rss_state_visualizer,
                                    visualizer_mode=self._config.rss.debug_visualization_mode)
            self.rss_set_road_boundaries_mode(self._config.rss.use_stay_on_road_feature)
        else: 
            self.rss_sensor = None
        self.tick_server_world()

    def tick_server_world(self):
        if self._args.handle_ticks:
            if self.sync: #TODO: What if ticks are handled externally?
                return self.world.tick()
            return self.world.wait_for_tick()

    #def tick(self, clock):
    #    self.hud.tick(self.player, clock) # RSS example. TODO: Check which has to be used!

    def tick(self, clock):
        """Method for every tick"""
        self.hud.tick(self, clock)

    def next_weather(self, reverse=False):
        """Get next weather setting"""
        self._weather_index += -1 if reverse else 1
        self._weather_index %= len(self._weather_presets)
        preset = self._weather_presets[self._weather_index]
        self.hud.notification('Weather: %s' % preset[1])
        self.player.get_world().set_weather(preset[0])
        self.weather = preset[1]

    def next_map_layer(self, reverse=False):
        self.current_map_layer += -1 if reverse else 1
        self.current_map_layer %= len(self.map_layer_names)
        selected = self.map_layer_names[self.current_map_layer]
        self.hud.notification('LayerMap selected: %s' % selected)

    def load_map_layer(self, unload=False):
        selected = self.map_layer_names[self.current_map_layer]
        if unload:
            self.hud.notification('Unloading map layer: %s' % selected)
            self.world.unload_map_layer(selected)
        else:
            self.hud.notification('Loading map layer: %s' % selected)
            self.world.load_map_layer(selected)

    def toggle_recording(self):
        if not self.recording:
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
            self.hud.notification('Started recording (folder: %s)' % dir_name_formatted)
        else:
            dir_name_formatted = os.path.split(self.recording_file_format)[0] % self.recording_dir_num
            self.hud.notification('Recording finished (folder: %s)' % dir_name_formatted)
        
        self.recording = not self.recording
    
    def toggle_radar(self):
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

    def finalize_render(self, display):
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

    def render(self, display, finalize=True):
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

        

    def destroy_sensors(self): # TODO only camera_manager, should be renamed.
        """Destroy sensors"""
        self.camera_manager.sensor.destroy()
        self.camera_manager.sensor = None
        self.camera_manager.index = None

    def destroy(self, destroy_ego=False):
        """Destroys all actors"""
        # stop from ticking
        if self.world_tick_id and self.world:
            self.world.remove_on_tick(self.world_tick_id)
        if self.rss_sensor:
            self.rss_sensor.destroy()
            self.rss_sensor = None
        if self.rss_unstructured_scene_visualizer:
            self.rss_unstructured_scene_visualizer.destroy()
            self.rss_unstructured_scene_visualizer = None
        if self.radar_sensor is not None:
            self.toggle_radar()
        if self.camera_manager is not None:
            self.destroy_sensors()
        if destroy_ego and not self.player in self.actors: # do not destroy external actors.
            print("Destroying player")
            self.actors.append(self.player)
        elif not destroy_ego and self.player in self.actors:
            logger.warning("destroy_ego=False, but player is in actors list. Destroying the actor from within WorldModel.destroy.")
        print("to destroy", list(map(str, self.actors)))
        while self.actors:
            actor = self.actors.pop(0)
            if actor is not None:
                print("destroying actor: " + str(actor), end=" destroyed=")
                try:
                    if hasattr(actor, 'stop'):
                        actor.stop()
                except AttributeError:
                    pass
                try:
                    x = actor.destroy()
                    print(x)
                except RuntimeError:
                    print("Warning: Could not destroy actor: " + str(actor))
                    #raise

        
    def rss_check_control(self, vehicle_control : carla.VehicleControl) -> Union[carla.VehicleControl, None]:
        self.hud.original_vehicle_control = vehicle_control
        self.hud.restricted_vehicle_control = vehicle_control
        if not AD_RSS_AVAILABLE:
            return None
        
        if self.rss_sensor and self.rss_sensor.ego_dynamics_on_route and not self.rss_sensor.ego_dynamics_on_route.ego_center_within_route:
            print("Not on route! " +  str(self.rss_sensor.ego_dynamics_on_route))
        # Is there a proper response?
        rss_proper_response = self.rss_sensor.proper_response if self.rss_sensor and self.rss_sensor.response_valid else None
        if rss_proper_response:
            # adjust the controls
            proposed_vehicle_control = self._restrictor.restrict_vehicle_control(
                            vehicle_control, rss_proper_response, self.rss_sensor.ego_dynamics_on_route, self._vehicle_physics)
            self.hud.restricted_vehicle_control = proposed_vehicle_control
            self.hud.allowed_steering_ranges = self.rss_sensor.get_steering_ranges()     
            return proposed_vehicle_control
        return None


def find_weather_presets():
    """Method to find weather presets"""
    import re
    rgx = re.compile('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)')

    def name(x): return ' '.join(m.group(0) for m in rgx.finditer(x))

    presets = [x for x in dir(carla.WeatherParameters) if re.match('[A-Z].+', x)]
    return [(getattr(carla.WeatherParameters, x), name(x)) for x in presets]
