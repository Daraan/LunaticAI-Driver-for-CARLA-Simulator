"""
Aim of this module is to provide a less convoluted access to information,
i.e. distill the information from the data and return high level information
"""

# todo: maybe find another name for this module

from fnmatch import fnmatch
import carla
from launch_tools import CarlaDataProvider

import time

class InformationManager:
    
    _tick = 0
    
    all_actors : carla.ActorList = None
    """
    Actor list of all actors; might not be up to date
    
    Will also include sensors, traffic lights, etc.
    """
    
    vehicles : "list[carla.Vehicle]"
    walkers : "list[carla.Walker]"
        
    @staticmethod
    def tick():
        InformationManager.vehicles = [a for a in CarlaDataProvider._carla_actor_pool.values() if a.is_alive and fnmatch(a.type_id, "*vehicle*")]
        InformationManager.walkers = [a for a in CarlaDataProvider._carla_actor_pool.values() if a.is_alive and fnmatch(a.type_id, "*walker.pedestrian*")]
