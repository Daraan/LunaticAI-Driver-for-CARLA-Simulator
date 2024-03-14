# Official Example from examples/automatic-control.py
# NOTE it might has to use synchonous_mode
import os
import sys
from typing import Any, ClassVar, Dict, List, Optional, Union, cast as assure_type, TYPE_CHECKING
import weakref

import numpy as np
from omegaconf import DictConfig
import pygame

import carla
import numpy.random as random
from classes.HUD import HUD

from classes.camera_manager import CameraManager
from classes.carla_originals.sensors import CollisionSensor, GnssSensor, IMUSensor, LaneInvasionSensor, RadarSensor

from classes.rule import Rule
from classes.rss_sensor import RssSensor, AD_RSS_AVAILABLE
from classes.rss_visualization import RssUnstructuredSceneVisualizer, RssBoundingBoxVisualizer
from classes.keyboard_controls import RSSKeyboardControl

if TYPE_CHECKING:
    from conf.agent_settings import LunaticAgentSettings
    from agents.lunatic_agent import LunaticAgent

from classes.HUD import get_actor_display_name
from launch_tools.blueprint_helpers import get_actor_blueprints
from agents.tools.logging import logger

try:
    from srunner.scenariomanager.carla_data_provider import CarlaDataProvider
except ImportError:
    logger.warning("CarlaDataProvider not available: ScenarioManager (srunner module) not found in path. Make sure it is in your PYTHONPATH or PATH variable.")
    CarlaDataProvider = None

class ContinueLoopException(Exception):
    pass

# ==============================================================================
# -- Game Framework ---------------------------------------------------------------
# ==============================================================================

class GameFramework(object):
    clock : ClassVar[pygame.time.Clock]
    display : ClassVar[pygame.Surface]
    
    def __init__(self, args, config=None):
        if args.seed:
            random.seed(args.seed)
            np.random.seed(args.seed)
        self.args = args
        self.clock, self.display = self.init_pygame(args)
        self.client, self.world, self.map, self.world_settings = self.init_carla(args)
        self.config = config
        self.agent = None
        self.world_model = None
        self.controller = None
        
        self.debug = self.world.debug
        
    @staticmethod
    def init_pygame(args):
        pygame.init()
        pygame.font.init()
        clock = pygame.time.Clock()
        display = pygame.display.set_mode(
            (args.width, args.height),
            pygame.HWSURFACE | pygame.DOUBLEBUF)
        return clock, display
    
    @staticmethod
    def init_carla(args, timeout=10.0, worker_threads:int=0, *, map_layers=carla.MapLayer.All):
        if CarlaDataProvider is not None:
            client = CarlaDataProvider.get_client()
            if client is None:
                client = carla.Client(args.host, args.port, worker_threads)
                CarlaDataProvider.set_client(client)
            elif TYPE_CHECKING:
                client = assure_type(carla.Client, client)
            # Note maybe use client.load_world_if_different(world_name, reset_settings=True, map_layers=map_layers)
            sim_world = CarlaDataProvider.get_world()
            if sim_world is None:
                sim_world = client.get_world()
                CarlaDataProvider.set_world(sim_world)
            elif TYPE_CHECKING:
                sim_world = assure_type(carla.World, sim_world)
            #CarlaDataProvider.set_traffic_manager_port(args.traffic_manager_port)
            sim_map = assure_type(carla.Map, CarlaDataProvider.get_map())
        else:
            client = carla.Client(args.host, args.port, worker_threads)
            client.set_timeout(timeout)
            sim_world = client.get_world()
            sim_map = sim_world.get_map()
        
        world_name = args.map
        if world_name and sim_map.name != "Carla/Maps/" + world_name:
            logger.info(f"Loading world: {world_name}")
            sim_world = client.load_world(world_name, map_layers=map_layers)
            sim_map = sim_world.get_map()
            if CarlaDataProvider is not None:
                CarlaDataProvider.set_world(sim_world)
                CarlaDataProvider.set_map(sim_map)
        else:
            logger.debug("skipped loading world, already loaded. map_layers ignored.") # todo: remove?
        
        # Apply world settings
        if args.sync:
            logger.debug("Using synchronous mode.")
            # apply synchronous mode if wanted
            world_settings = sim_world.get_settings()
            world_settings.synchronous_mode = True
            world_settings.fixed_delta_seconds = 1/args.fps # 0.05
            sim_world.apply_settings(world_settings)
        else:
            logger.debug("Using asynchronous mode.")
            world_settings = sim_world.get_settings()
        print("World Settings:", world_settings)
        
        return client, sim_world, sim_map, world_settings
    
    def init_traffic_manager(self) -> carla.TrafficManager:
        traffic_manager = self.client.get_trafficmanager()
        if self.args.sync:
            traffic_manager.set_synchronous_mode(True)
        traffic_manager.set_hybrid_physics_mode(True) # Note default 50m
        traffic_manager.set_hybrid_physics_radius(50.0) # TODO: make a config variable
        return traffic_manager
    
    def set_config(self, config:DictConfig):
        self.config = config
    
    def make_world_model(self, config:"LunaticAgentSettings", player:carla.Vehicle = None, map_inst:Optional[carla.Map]=None):
        self.world_model = WorldModel(self.world, config, self.args, player=player, map_inst=map_inst)
        self.world_model.game_framework = weakref.proxy(self)
        return self.world_model
    
    def make_controller(self, world_model, controller_class=RSSKeyboardControl, **kwargs):
        controller = controller_class(world_model, config=self.config, clock=self.clock, **kwargs)
        self.controller = weakref.proxy(controller)
        return controller
    
    def set_controller(self, controller):
        self.controller = controller
    
    def parse_rss_controller_events(self, final_controls:carla.VehicleControl):
        return self.controller.parse_events(final_controls)

    def init_agent_and_interface(self, ego, agent_class:"LunaticAgent", overwrites:Optional[Dict[str, Any]]=None):
        self.agent, self.world_model, self.global_planner = agent_class.create_world_and_agent(ego, self.world, self.args, map_inst=self.map, overwrites=overwrites)
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
        if self.args.sync:
            self.world_model.world.tick()
        else:
            self.world_model.world.wait_for_tick()
        return self
    
    def render_everything(self):
        """Update render and hud"""
        self.world_model.tick(self.clock) # TODO # CRITICAL maybe has to tick later
        self.world_model.render(self.display)
        self.controller.render(self.display)
        self.agent.render_road_matrix(self.display)
        
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
        if exc_type is None or issubclass(exc_type, ContinueLoopException):
            self.render_everything()
            
            pygame.display.flip()
            
            Rule.update_all_cooldowns() # Rule Cooldown Framework

# ==============================================================================
# -- World ---------------------------------------------------------------
# ==============================================================================

class WorldModel(object):
    """ Class representing the surrounding environment """

    controller : Optional[RSSKeyboardControl] = None# Set when controller is created. Uses weakref.proxy
    game_framework : Optional[GameFramework] = None # Set when world created via GameFramework. Uses weakref.proxy

    def get_blueprint_library(self):
        return self.world.get_blueprint_library()

    def __init__(self, carla_world : carla.World, config : "LunaticAgentSettings", args, agent:"LunaticAgent" = None, player : carla.Vehicle = None, map_inst:Optional[carla.Map]=None):
        """Constructor method"""
        self.world = carla_world
        self.world_settings = self.world.get_settings()
        # TEMP:
        if agent:
            agent._world_model = self
        
        if map_inst:
            if isinstance(map_inst, carla.Map):
                self._map = map_inst
            else:
                print("Warning: Ignoring the given map as it is not a 'carla.Map'")
            self._map = None
        if not map_inst or not self._map:
            try:
                if agent:
                    self.map = agent._map
                else:
                    self.map = self.world.get_map()
            except RuntimeError as error:
                print('RuntimeError: {}'.format(error))
                print('  The server could not send the OpenDRIVE (.xodr) file:')
                print('  Make sure it exists, has the same name of your town, and is correct.')
                sys.exit(1)
        
        self._config = config
        self._args = args
        self.hud = HUD(args.width, args.height, carla_world)
        self.sync : bool = args.sync
        self.dim = (args.width, args.height)
        self.external_actor : bool = args.externalActor
        self.actor_role_name : Optional[str] = args.rolename

        # TODO: Remove?
        self.recording = False
        self.recording_frame_num = 0
        self.recording_dir_num = 0
        
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
        
        self._actor_filter = args.filter
        self._actor_generation = args.generation
        self._gamma = args.gamma
        self.recording_enabled = False
        self.recording_start = 0
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
        
        self._actor_filter = args.filter
        if not self._actor_filter.startswith("vehicle."):
            print('Error: RSS only supports vehicles as ego.')
            sys.exit(1)
        if AD_RSS_AVAILABLE:
            self._restrictor = carla.RssRestrictor()
        else:
            self._restrictor = None

        self.restart(args) # # interactive without args
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

    def restart(self, args):
        """Restart the world"""
        # Keep same camera config if the camera manager exists.
        # TODO: unsure if correct
        cam_index = self.camera_manager.index if self.camera_manager is not None else 0
        cam_pos_id = self.camera_manager.transform_index if self.camera_manager is not None else 0
        if self.external_actor:
            # Check whether there is already an actor with defined role name
            actor_list = self.world.get_actors() # In sync mode the actor list could be empty
            if len(actor_list) == 0:
                self.tick_server_world() 
                actor_list = self.world.get_actors()
            self.player = self._find_external_actor(self.world, self.actor_role_name, actor_list)
            
            # TODO: Make this more nicer, see maybe scenario runner how to wait for spawn. Only do tick if in sync mode. Async wait.
            if self.player is None:
                self.tick_server_world() 
                self.player = assure_type(carla.Vehicle, self._find_external_actor(self.world, self.actor_role_name))
            if self.player is None:
                print("Error: No actor found with role name: " + self.actor_role_name)
                sys.exit(1)
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
        
        self.camera_manager = CameraManager(self.player, self.hud, self._gamma)
        self.camera_manager.transform_index = cam_pos_id
        self.camera_manager.set_sensor(cam_index, notify=False)
        
        actor_type = get_actor_display_name(self.player)
        self.hud.notification(actor_type)
        
        self.rss_unstructured_scene_visualizer = RssUnstructuredSceneVisualizer(self.player, self.world, self.dim)
        self.rss_bounding_box_visualizer = RssBoundingBoxVisualizer(self.dim, self.world, self.camera_manager.sensor)
        if AD_RSS_AVAILABLE:
            self.rss_sensor = RssSensor(self.player, self.world,
                                    self.rss_unstructured_scene_visualizer, self.rss_bounding_box_visualizer, self.hud.rss_state_visualizer)
            self.rss_set_road_boundaries_mode(self._config.rss.use_stay_on_road_feature)
        else: 
            self.rss_sensor = None
        self.tick_server_world()

    def tick_server_world(self):
        if self.sync:
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
            dir_name = "_out%04d" % self.recording_dir_num
            while os.path.exists(dir_name):
                self.recording_dir_num += 1
                dir_name = "_out%04d" % self.recording_dir_num
            self.recording_frame_num = 0
            os.mkdir(dir_name)
        else:
            self.hud.notification('Recording finished (folder: _out%04d)' % self.recording_dir_num)
        
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

    def render(self, display):
        """Render world"""
        self.camera_manager.render(display)
        self.rss_bounding_box_visualizer.render(display, self.camera_manager.current_frame)
        self.rss_unstructured_scene_visualizer.render(display)
        self.hud.render(display)

        if self.recording:
            pygame.image.save(display, "_out%04d/%08d.bmp" % (self.recording_dir_num, self.recording_frame_num))
            self.recording_frame_num += 1

    def destroy_sensors(self):
        """Destroy sensors"""
        self.camera_manager.sensor.destroy()
        self.camera_manager.sensor = None
        self.camera_manager.index = None

    def destroy(self, destroy_ego=False):
        """Destroys all actors"""
        # stop from ticking
        if self.world_tick_id:
            self.world.remove_on_tick(self.world_tick_id)
        if self.rss_sensor:
            self.rss_sensor.destroy()
        if self.rss_unstructured_scene_visualizer:
            self.rss_unstructured_scene_visualizer.destroy()
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
            vehicle_control = self._restrictor.restrict_vehicle_control(
                            vehicle_control, rss_proper_response, self.rss_sensor.ego_dynamics_on_route, self._vehicle_physics)
            self.hud.restricted_vehicle_control = vehicle_control
            self.hud.allowed_steering_ranges = self.rss_sensor.get_steering_ranges()     
            return vehicle_control
        return None


def find_weather_presets():
    """Method to find weather presets"""
    import re
    rgx = re.compile('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)')

    def name(x): return ' '.join(m.group(0) for m in rgx.finditer(x))

    presets = [x for x in dir(carla.WeatherParameters) if re.match('[A-Z].+', x)]
    return [(getattr(carla.WeatherParameters, x), name(x)) for x in presets]
