"""
Aim of this module is to provide a less convoluted access to information,
i.e. distill the information from the data and return high level information
"""

# todo: maybe find another name for this module

import carla
from launch_tools import CarlaDataProvider

class InformationManager:
    
    _tick = 0
    
    all_actors : carla.ActorList = None
    """Actor list of all actors; might not be up to date"""
    
    vehicles : carla.Vehicle
    walkers : carla.Walker
    
    @staticmethod
    def _sync_actor_pool():
        InformationManager.all_actors = CarlaDataProvider.get_all_actors()
        for actor in InformationManager.all_actors:
            if actor.id not in CarlaDataProvider._carla_actor_pool: # TODO: maybe use setdefault or set anyway. # TEST speed
                CarlaDataProvider._carla_actor_pool[actor.id] = actor
            # Assuming that the pool is cleaned up by the environment
        if len(CarlaDataProvider._carla_actor_pool) > len(InformationManager.all_actors):
            print("ERROR: Pool is bigger, not cleaned properly")
        InformationManager.vehicles = InformationManager.all_actors.filter("*vehicle*")
        InformationManager.walkers = InformationManager.all_actors.filter("*walker.pedestrian*")
    
    @staticmethod
    def manage_actor_pool():
        # CarlaDataProvider._carla_actor_pool # Might be updated by Spawning and Removing actors outside the area.
        if len(CarlaDataProvider._carla_actor_pool) != len(InformationManager.all_actors):
            print("Pool and all actors have not the same length")
            InformationManager._sync_actor_pool()
        
    @staticmethod
    def tick():
        if not InformationManager.all_actors or InformationManager._tick % 10 == 0:
            InformationManager._sync_actor_pool()
        InformationManager.manage_actor_pool()
        InformationManager._tick += 1 # Use a clock to make this depend on server/fps and not only on the client