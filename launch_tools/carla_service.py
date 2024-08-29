# pylint: disable=protected-access, no-member
"""
Provides tools to interact with carla: access the client, world, map,
spawn actors, destroy actors, and initialize carla.

.. deprecated:: In favor of using GameFramework
"""

from typing import Iterable, Union
import carla

from agents.tools.logging import logger

from classes._sensor_interface import CustomSensorInterface
from launch_tools import CarlaDataProvider

get_client = CarlaDataProvider.get_client
get_world = CarlaDataProvider.get_world
get_map = CarlaDataProvider.get_map

def initialize_carla(map_name="Town04", ip="127.0.0.1", port:int=2000, *,
                     timeout:float=10.0, worker_threads=0,
                     reload_world: bool=False, reset_settings: bool=True,
                     map_layers: carla.MapLayer=carla.MapLayer.All,
                     sync: Union[bool, None]=True,
                     fps: int=20):
    client = CarlaDataProvider.get_client()
    if client is None:
        client = carla.Client(ip, port, worker_threads)
        client.set_timeout(timeout)
        CarlaDataProvider.set_client(client)
    
    world = CarlaDataProvider.get_world()
    if not world:
        world = client.get_world()
    _map = world.get_map() # CarlaDataProvider map not yet set ->  set_world
    
    if map_name and _map.name != "Carla/Maps/" + map_name:
        world: carla.World = client.load_world(map_name, reset_settings, map_layers)
    elif reload_world:
        world = client.reload_world(reset_settings)
        logger.info("Reloaded world - map_layers ignored.")
    elif map_name is None:
        logger.info("Provided map_name is None, skipped loading world. Assuming world is already loaded.")
    else:
        logger.info("skipped loading world %s, already loaded - map_layers and reset_settings ignored.", _map.name)
    
    world_settings = world.get_settings()
    # Apply world settings
    if sync is not None:
        if sync:
            logger.debug("Using synchronous mode.")
            # apply synchronous mode if wanted
            world_settings.synchronous_mode = True
            world_settings.fixed_delta_seconds = 1/fps # 0.05
            world.apply_settings(world_settings)
        else:
            logger.debug("Using asynchronous mode.")
            world_settings.synchronous_mode = False
        world.apply_settings(world_settings)
    print("World Settings:", world_settings)
    # Note: This loads multiple information. It should be called after applying the world settings.
    CarlaDataProvider.set_world(world)
    
    map_ = CarlaDataProvider.get_map()
    return client, world, map_

spawn_actor = CarlaDataProvider.spawn_actor

def destroy_actors(actors: "Iterable[carla.Actor | CustomSensorInterface]"):
    """
    Destroys the given actors and customs sensors implemented in this package.
    
    Removes destroyed actors from the :py:class:`.CarlaDataProvider` actor pool.
    """
    batch: "list[carla.command.DestroyActor]" = []
    for actor in actors:
        if isinstance(actor, (carla.Sensor, CustomSensorInterface)):
            actor.stop()
        if isinstance(actor, carla.Actor):
            if actor.is_alive:
                batch.append(carla.command.DestroyActor(actor))
        else:
            actor.destroy()

    if batch and CarlaDataProvider._client:
        try:
            CarlaDataProvider._client.apply_batch(batch)
        except RuntimeError as e:
            if "time-out" in str(e):
                pass
            else:
                raise e
        else:
            for command in batch:
                if CarlaDataProvider.actor_id_exists(command.actor_id):
                    del CarlaDataProvider._carla_actor_pool[command.actor_id] # remove by batch and not by individual command
    elif not CarlaDataProvider._client:
        print("WARNING: No client available to destroy actors.")
