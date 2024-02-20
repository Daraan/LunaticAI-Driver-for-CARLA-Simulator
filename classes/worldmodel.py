# Official Example from examples/automatic-control.py
# NOTE it might has to use synchonous_mode
import os
import sys
from typing import List, Optional, Union, cast as assure_type

import pygame

import carla
import numpy.random as random
from classes.HUD import HUD

from classes.camera_manager import CameraManager
from classes.carla_originals.sensors import CollisionSensor, GnssSensor, IMUSensor, LaneInvasionSensor, RadarSensor

from classes.carla_originals.rss_sensor import RssSensor
from classes.carla_originals.rss_visualization import RssUnstructuredSceneVisualizer, RssBoundingBoxVisualizer

from utils import get_actor_display_name
from utils.blueprint_helpers import get_actor_blueprints
from utils.blueprint_helpers import find_weather_presets


# ==============================================================================
# -- World ---------------------------------------------------------------
# ==============================================================================

class WorldModel(object):
    """ Class representing the surrounding environment """

    def get_blueprint_library(self):
        return self.world.get_blueprint_library()

    def __init__(self, carla_world : carla.World, hud :"HUD", args, player:carla.Vehicle=None):
        """Constructor method"""
        self._args = args
        self.world = carla_world
        self.sync : bool = args.sync
        # TODO: must be added to arguments or removed
        self.actor_role_name : Optional[str] = args.rolename
        self.dim = (args.width, args.height)
        try:
            self.map = self.world.get_map()
        except RuntimeError as error:
            print('RuntimeError: {}'.format(error))
            print('  The server could not send the OpenDRIVE (.xodr) file:')
            print('  Make sure it exists, has the same name of your town, and is correct.')
            sys.exit(1)
        self.external_actor = args.externalActor

        self.hud = hud # or HUD(args.width, args.height, carla_world)
        # TODO: Remove?
        self.recording = False
        self.recording_frame_num = 0
        self.recording_dir_num = 0
        
        self.player = player
        assert self.player is not None or self.external_actor # Note: Former optional
        self._lights = carla.VehicleLightState.NONE

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
        self.actors.append(self.player)
        
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
        self.rss_sensor = None
        self.rss_unstructured_scene_visualizer = None
        self.rss_bounding_box_visualizer = None
        self._actor_filter = args.filter
        if not self._actor_filter.startswith("vehicle."):
            print('Error: RSS only supports vehicles as ego.')
            sys.exit(1)
        self._restrictor = carla.RssRestrictor()

        self.restart(args) # # interactive without args
        self._vehicle_physics = self.player.get_physics_control()
        self.world_tick_id = self.world.on_tick(self.hud.on_world_tick)

    def rss_set_road_boundaries_mode(self, road_boundaries_mode: Union[bool, carla.RssRoadBoundariesMode]):
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

    def restart(self, args):
        """Restart the world"""
        if self.external_actor:
            # Check whether there is already an actor with defined role name
            for actor in self.world.get_actors():
                if actor.attributes.get('role_name') == self.actor_role_name:
                    self.player = assure_type(carla.Vehicle, actor)
        else:            
            # From interactive:
            #self.player_max_speed = 1.589
            #self.player_max_speed_fast = 3.713
        
            # Keep same camera config if the camera manager exists.
            cam_index = self.camera_manager.index if self.camera_manager is not None else 0
            cam_pos_id = self.camera_manager.transform_index if self.camera_manager is not None else 0

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
            assert isinstance(self.player, carla.Vehicle)


        if self.external_actor:
            ego_sensors = []
            for actor in self.world.get_actors():
                if actor.parent == self.player:
                    ego_sensors.append(actor)

            for ego_sensor in ego_sensors:
                if ego_sensor is not None:
                    ego_sensor.destroy()

        # Set up the sensors.
        self.collision_sensor = CollisionSensor(self.player, self.hud)
        self.lane_invasion_sensor = LaneInvasionSensor(self.player, self.hud)
        self.gnss_sensor = GnssSensor(self.player)
        self.imu_sensor = IMUSensor(self.player)
        self.camera_manager = CameraManager(self.player, self.hud, self._gamma)
        self.camera_manager.transform_index = cam_pos_id
        self.camera_manager.set_sensor(cam_index, notify=False)
        actor_type = get_actor_display_name(self.player)
        self.hud.notification(actor_type)
        
        self.rss_unstructured_scene_visualizer = RssUnstructuredSceneVisualizer(self.player, self.world, self.dim)
        self.rss_bounding_box_visualizer = RssBoundingBoxVisualizer(self.dim, self.world, self.camera_manager.sensor)
        self.rss_sensor = RssSensor(self.player, self.world,
                                    self.rss_unstructured_scene_visualizer, self.rss_bounding_box_visualizer, self.hud.rss_state_visualizer)
        if self.sync:
            self.world.tick()
        else:
            self.world.wait_for_tick()

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

    def modify_vehicle_physics(self, actor):
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

    def destroy(self):
        """Destroys all actors"""
        # stop from ticking
        if self.world_tick_id:
            self.world.remove_on_tick(self.world_tick_id)
        if self.radar_sensor is not None:
            self.toggle_radar()
        if self.rss_sensor:
            self.rss_sensor.destroy()
        if self.rss_unstructured_scene_visualizer:
            self.rss_unstructured_scene_visualizer.destroy()
        actors : List[carla.Actor] = [
            self.camera_manager.sensor,
            self.collision_sensor.sensor,
            self.lane_invasion_sensor.sensor,
            self.gnss_sensor.sensor,
            self.imu_sensor.sensor,
            # self.player
        ]
        actors.extend(self.actors)
        for actor in actors:
            if actor is not None:
                try:
                    actor.stop()
                except AttributeError:
                    pass
                actor.destroy()
        # TODO: Call destroy_sensors?
        
        
    # TODO: These semantically do not fit in here 
    def update_lights(self, vehicle_control : carla.VehicleControl):
        current_lights = self._lights
        if vehicle_control.brake:
            current_lights |= carla.VehicleLightState.Brake
        else:  # Remove the Brake flag
            current_lights &= carla.VehicleLightState.All ^ carla.VehicleLightState.Brake
        if vehicle_control.reverse:
            current_lights |= carla.VehicleLightState.Reverse
        else:  # Remove the Reverse flag
            current_lights &= carla.VehicleLightState.All ^ carla.VehicleLightState.Reverse
        if current_lights != self._lights:  # Change the light state only if necessary
            self._lights = current_lights
            self.player.set_light_state(carla.VehicleLightState(self._lights))

    def rss_check_control(self, vehicle_control : carla.VehicleControl) -> Union[carla.VehicleControl, None]:
        self.hud.original_vehicle_control = vehicle_control
        self.hud.restricted_vehicle_control = vehicle_control
        
        if self.rss_sensor and self.rss_sensor.ego_dynamics_on_route and not self.rss_sensor.ego_dynamics_on_route.ego_center_within_route:
            print("Not on route!" +  str(self.rss_sensor.ego_dynamics_on_route))
        # Is there a proper response?
        rss_proper_response = self.rss_sensor.proper_response if self.rss_sensor and self.rss_sensor.response_valid else None
        if rss_proper_response:
            # adjust the controls
            vehicle_control = self._restrictor.restrict_vehicle_control(
                            vehicle_control, rss_proper_response, self.rss_sensor.ego_dynamics_on_route, self._vehicle_physics)
            assert vehicle_control is not self.hud.original_vehicle_control # todo remove, but assure they are different
            self.hud.restricted_vehicle_control = vehicle_control
            self.hud.allowed_steering_ranges = self.rss_sensor.get_steering_ranges()     
            return vehicle_control
        return None
