import carla
from requests import get

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
    if not CarlaDataProvider.get_world():
        world = client.get_world()
        CarlaDataProvider.set_world(world)
    else:
        world = CarlaDataProvider.get_world()
        assert world # for type hint
    if map_name and CarlaDataProvider.get_map().name != "Carla/Maps/" + map_name:
        world = client.load_world(map_name, reset_settings, map_layers)
        CarlaDataProvider.set_world(world)
    elif reload_world:
        world = client.reload_world(reset_settings)
        CarlaDataProvider.set_world(world)
        logger.info("Reloaded world - map_layers ignored.")
    else:
        logger.info("skipped loading world, already loaded - map_layers and reset_settings ignored.")
    return client, world, CarlaDataProvider.get_map()


def spawn_actor(bp: carla.ActorBlueprint, spawn_point: carla.Waypoint, must_spawn=True, attach_to: carla.Actor=None, attachment_type: carla.AttachmentType=carla.AttachmentType.Rigid):
    world = CarlaDataProvider.get_world()
    assert world
    if must_spawn:
        actor = world.spawn_actor(bp, spawn_point.transform, attach_to, attachment_type)
    else:
        actor = world.try_spawn_actor(bp, spawn_point.transform, attach_to, attachment_type)
        if actor is None:
            return None
    CarlaDataProvider.register_actor(actor, spawn_point.transform)
    return actor

