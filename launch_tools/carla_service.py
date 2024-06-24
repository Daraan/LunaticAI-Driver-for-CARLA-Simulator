from typing import Optional, Union
import carla

from agents.tools.logging import logger

from launch_tools import CarlaDataProvider

get_client = CarlaDataProvider.get_client
get_world = CarlaDataProvider.get_world
get_map = CarlaDataProvider.get_map

def initialize_carla(map_name="Town04", ip="127.0.0.1", port=2000, *, timeout=10.0, worker_threads=0, reload_world=False, reset_settings=True, map_layers=carla.MapLayer.All):
    client = CarlaDataProvider.get_client()
    if client is None:
        client = carla.Client(ip, port, worker_threads)
        client.set_timeout(timeout)
        CarlaDataProvider.set_client(client)
    
    world = CarlaDataProvider.get_world()
    if not world:
        world = client.get_world()
        CarlaDataProvider.set_world(world)
    
    if map_name and CarlaDataProvider.get_map().name != "Carla/Maps/" + map_name:
        world = client.load_world(map_name, reset_settings, map_layers)
        CarlaDataProvider.set_world(world)
    elif reload_world:
        world = client.reload_world(reset_settings)
        CarlaDataProvider.set_world(world)
        logger.info("Reloaded world - map_layers ignored.")
    elif not CarlaDataProvider._map: # only if no map_name is provided & world exists somehow. This should actually not happen.
        logger.error("CarlaDataProvider._map is None. This should not happen.")
        CarlaDataProvider.set_world(world)
    elif map_name is None:
        logger.info("Provided map_name is None, skipped loading world. Assuming world is already loaded.")
    else:
        logger.info("skipped loading world %s, already loaded - map_layers and reset_settings ignored.", CarlaDataProvider.get_map().name)
    # These are all set if set_world was executed, will only fail if _world was set without set_world
    assert CarlaDataProvider._grp
    assert CarlaDataProvider._spawn_points is not None # can be empty
    assert CarlaDataProvider._traffic_light_map is not None # can be empty
    
    map_ = CarlaDataProvider.get_map()
    return client, world, map_

spawn_actor = CarlaDataProvider.spawn_actor

def destroy_actors(actors: "list[carla.Actor]"):
    batch = []
    for actor in actors:
        if isinstance(actor, carla.Sensor):
            actor.stop()
        if actor is not None and actor.is_alive:
            batch.append(carla.command.DestroyActor(actor))
        if CarlaDataProvider.actor_id_exists(actor.id):
            logger.warning("Actor %s is registered in the CarlaActorPool, its to remove it with CarlaActorPool._cleanup")
            del CarlaDataProvider._carla_actor_pool[actor.id] # remove by batch and not by individual command

    if batch and CarlaDataProvider._client:
        try:
            CarlaDataProvider._client.apply_batch(batch)
        except RuntimeError as e:
            if "time-out" in str(e):
                pass
            else:
                raise e

def destroy_actors(actors: "list[carla.Actor]"):
    batch = []
    for actor in actors:
        if isinstance(actor, carla.Sensor):
            actor.stop()
        if actor is not None and actor.is_alive:
            batch.append(carla.command.DestroyActor(actor))
        if CarlaDataProvider.actor_id_exists(actor.id):
            logger.warning("Actor %s is registered in the CarlaActorPool, its to remove it with CarlaActorPool._cleanup")
            del CarlaDataProvider._carla_actor_pool[actor.id] # remove by batch and not by individual command

    if batch and CarlaDataProvider._client:
        try:
            CarlaDataProvider._client.apply_batch(batch)
        except RuntimeError as e:
            if "time-out" in str(e):
                pass
            else:
                raise e
