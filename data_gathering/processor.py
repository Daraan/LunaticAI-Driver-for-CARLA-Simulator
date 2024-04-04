"""
Aim of this module is to provide a less convoluted access to information,
i.e. distill the information from the data and return high level information
"""

# todo: maybe find another name for this module

from fnmatch import fnmatch
from typing import ClassVar
import carla
from launch_tools import CarlaDataProvider

from agents.tools import logger


class InformationManager:
    
    _tick = 0
    
    vehicles : ClassVar["list[carla.Vehicle]"]
    walkers : ClassVar["list[carla.Walker]"]
    
    relevant_traffic_light : carla.TrafficLight = None
    relevant_traffic_light_distance : float = None
    _relevant_traffic_light_location : carla.Location = None
    
    def __init__(self, actor: carla.Actor):
        self._actor = actor
        self._get_next_traffic_light()
            
    def _get_next_traffic_light(self):
        self.relevant_traffic_light = CarlaDataProvider.get_next_traffic_light(self._actor)
        if self.relevant_traffic_light:
            self._relevant_traffic_light_location = self.relevant_traffic_light.get_location()
            self.relevant_traffic_light_distance = self._relevant_traffic_light_location.distance(CarlaDataProvider.get_location(self._actor))
        else:
            # Is at an intersection
            self._relevant_traffic_light_location = None
            self.relevant_traffic_light_distance = None
            logger.debug("No traffic light found - at intersection?")
        # TODO: Assure that the traffic light is not behind the actor, but in front of it.
        # TODO: Do not use the CDP but use the planned route instead.
           
    @staticmethod
    def global_tick():
        InformationManager.vehicles = [a for a in CarlaDataProvider._carla_actor_pool.values() if a.is_alive and fnmatch(a.type_id, "*vehicle*")]
        InformationManager.walkers = [a for a in CarlaDataProvider._carla_actor_pool.values() if a.is_alive and fnmatch(a.type_id, "*walker.pedestrian*")]
            
    def tick(self):
        # Next relevant traffic light
        # NOTE: Does not check for planned path but current route along waypoints, might not be exact.
        if not self.relevant_traffic_light or self._relevant_traffic_light_location.distance(CarlaDataProvider.get_location(self._actor)) > self.relevant_traffic_light_distance * 1.01: # 1% tolerance to prevent permanent updates when far away from a traffic light
            # Update if the distance increased, and we might need to target another one; # TODO: This might be circumvented by passing and intersection
            if self.relevant_traffic_light and self._relevant_traffic_light_location.distance(CarlaDataProvider.get_location(self._actor)) > self.relevant_traffic_light_distance * 1.01:
                logger.debug("Traffic light distance increased %s, updating.", self.relevant_traffic_light_distance)
            self._get_next_traffic_light()
