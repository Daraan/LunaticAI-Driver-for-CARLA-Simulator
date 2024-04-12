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
    else:
        logger.info("skipped loading world %s, already loaded - map_layers and reset_settings ignored.", CarlaDataProvider.get_map().name)
    # These are all set if set_world was executed, will only fail if _world was set without set_world
    assert CarlaDataProvider._grp
    assert CarlaDataProvider._spawn_points is not None # can be empty
    assert CarlaDataProvider._traffic_light_map is not None # can be empty
    
    map_ = CarlaDataProvider.get_map()
    return client, world, map_


def spawn_actor(bp: carla.ActorBlueprint, spawn_point: Union[carla.Waypoint, carla.Transform], must_spawn=False, track_physics=True, attach_to: Optional[carla.Actor]=None, attachment_type=carla.AttachmentType.Rigid):
    # type: (carla.ActorBlueprint, carla.Waypoint | carla.Transform, bool, bool, carla.Actor | None, carla.AttachmentType) -> carla.Actor | None
    """
    The method will create, return and spawn an actor into the world. 
    The actor will need an available blueprint to be created.
    It can also be attached to a parent with a certain attachment type. 

    Args:
        bp (carla.ActorBlueprint): The blueprint of the actor to spawn.
        spawn_point (Union[carla.Waypoint, carla.Transform]): The spawn point of the actor.
        must_spawn (bool, optional): 
            If True, the actor will be spawned or an exception will be raised.
            If False, the function returns None if the actor could not be spawned.
            Defaults to False.
        track_physics (bool, optional): 
            If True, `get_location`, `get_transform` and `get_velocity` 
            can be used for this actor. 
            Defaults to True.
        attach_to (Optional[carla.Actor], optional): 
            The parent object that the spawned actor will follow around. 
            Defaults to None.
        attachment_type (carla.AttachmentType, optional): 
            Determines how fixed and rigorous should be the changes in position 
            according to its parent object.
            Defaults to carla.AttachmentType.Rigid.

    Returns:
        carla.Actor | None: The spawned actor if successful, None otherwise.
        
    Raises:
        RuntimeError: if `must_spawn` is True and the actor could not be spawned.
    """
    if isinstance(spawn_point, carla.Waypoint):
        spawn_point = spawn_point.transform
    world = CarlaDataProvider.get_world()
    if must_spawn:
        actor = world.spawn_actor(bp, spawn_point, attach_to, attachment_type)
    else:
        actor = world.try_spawn_actor(bp, spawn_point, attach_to, attachment_type)
        if actor is None:
            return None
    CarlaDataProvider._carla_actor_pool[actor.id] = actor
    if track_physics:
        CarlaDataProvider.register_actor(actor, spawn_point)
    return actor
