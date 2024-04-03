"""
Aim of this module is to provide a less convoluted access to information,
i.e. distill the information from the data and return high level information
"""

# todo: maybe find another name for this module

from fnmatch import fnmatch
from typing import ClassVar
import carla
from launch_tools import CarlaDataProvider



class InformationManager:
    
    _tick = 0
    
    vehicles : ClassVar["list[carla.Vehicle]"]
    walkers : ClassVar["list[carla.Walker]"]
    
    relevant_traffic_light : carla.TrafficLight = None
    relevant_traffic_light_distance : float = None
    _relevant_traffic_light_location : carla.Location = None
    
    def __init__(self, actor: carla.Actor):
        self._actor = actor
        self.relevant_traffic_light = CarlaDataProvider.get_next_traffic_light(actor)
        self._relevant_traffic_light_location = self.relevant_traffic_light.get_location()
        self.relevant_traffic_light_distance = self._relevant_traffic_light_location.distance(CarlaDataProvider.get_location(actor))
           
    @staticmethod
    def global_tick():
        InformationManager.vehicles = [a for a in CarlaDataProvider._carla_actor_pool.values() if a.is_alive and fnmatch(a.type_id, "*vehicle*")]
        InformationManager.walkers = [a for a in CarlaDataProvider._carla_actor_pool.values() if a.is_alive and fnmatch(a.type_id, "*walker.pedestrian*")]
            
    def tick(self):
        # Next relevant traffic light
        # NOTE: Does not check for planned path but current route along waypoints, might not be exact.
        if not self.relevant_traffic_light or self._relevant_traffic_light_location.distance(CarlaDataProvider.get_location(self._actor)) > self.relevant_traffic_light_distance:
            # Update if the distance increased, and we might target another one
            self.relevant_traffic_light = CarlaDataProvider.get_next_traffic_light(self._actor)
            self._relevant_traffic_light_location = self.relevant_traffic_light.get_location()
            self.relevant_traffic_light_distance = self._relevant_traffic_light_location.distance(CarlaDataProvider.get_location(self._actor))
