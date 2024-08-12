# pyright: reportPrivateUsage=false

from __future__ import annotations

import random
from typing import TYPE_CHECKING, List, Optional, TypeVar, Union
from typing_extensions import TypeAliasType, TypeAlias

import carla
from carla import TrafficLightState
from agents.tools.logging import logger
from agents.tools.hints import TrafficLightDetectionResult
from agents.tools.misc import (is_within_distance,
                               get_trafficlight_trigger_location)

from classes.constants import AgentState
from data_gathering.information_manager import InformationManager
from launch_tools import CarlaDataProvider

if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent

_A = TypeVar("_A", bound=carla.Actor)
_ActorList : TypeAlias = Union[carla.ActorList, List[_A]]


def _is_red_light(traffic_light : "carla.TrafficLight") -> bool:
    return traffic_light.state == TrafficLightState.Red

def _is_red_or_yellow(traffic_light : "carla.TrafficLight") -> bool:
    return traffic_light.state in (TrafficLightState.Red, TrafficLightState.Yellow)

def affected_by_traffic_light(self : "LunaticAgent", 
                              lights_list : Optional[_ActorList[carla.TrafficLight]]=None, 
                              max_distance : Optional[float]=None) -> TrafficLightDetectionResult:
        """
        Method to check if there is a red light affecting the vehicle.

            :param lights_list (list of carla.TrafficLight): list containing TrafficLight objects.
                If None, all traffic lights in the scene are used
            :param max_distance (float): max distance for traffic lights to be considered relevant.
                If None, the base threshold value is used
        """
        if self.config.obstacles.ignore_traffic_lights:
            return TrafficLightDetectionResult(False, None)

        detect_yellow_tlighs = self.config.obstacles.detect_yellow_tlighs

        # Currently affected by a traffic light
        if self._last_traffic_light:
            if self._last_traffic_light.state != TrafficLightState.Red and (not detect_yellow_tlighs or self._last_traffic_light.state != TrafficLightState.Yellow):
                self._last_traffic_light = None
            else: # Still Red
                return TrafficLightDetectionResult(True, self._last_traffic_light)
        
        if lights_list is None:
            if self._world_model._args.debug:
                logger.warning("No traffic lights list provided, using all traffic lights in the scene. This should not happen."
                               "You possibly want to pass agent.traffic_lights_nearby or agent._lights_list instead.")
            lights_list = CarlaDataProvider.get_all_actors().filter("*traffic_light*")
        if len(lights_list) == 0:
            return TrafficLightDetectionResult(False, None)

        if not max_distance: # NOTE: dynamic selection is done in traffic_light_manager
            max_distance = self.config.obstacles.base_tlight_threshold

        ego_vehicle_location = self.config.live_info.current_location
        ego_vehicle_waypoint = self._current_waypoint

        filtered_lights = filter(_is_red_or_yellow if detect_yellow_tlighs else _is_red_light, lights_list) # type: ignore
        
        for traffic_light in filtered_lights:
            trigger_wp = InformationManager.get_trafficlight_trigger_waypoint(traffic_light)

            if trigger_wp.road_id != ego_vehicle_waypoint.road_id:
                continue
            
            if trigger_wp.transform.location.distance(ego_vehicle_location) > max_distance:
                continue

            ve_dir = ego_vehicle_waypoint.transform.get_forward_vector()
            wp_dir = trigger_wp.transform.get_forward_vector()
            dot_ve_wp = ve_dir.x * wp_dir.x + ve_dir.y * wp_dir.y + ve_dir.z * wp_dir.z

            if dot_ve_wp < 0:
                continue

            if is_within_distance(trigger_wp.transform, self._vehicle.get_transform(), max_distance, [0, 90]):
                self._last_traffic_light = traffic_light
                return TrafficLightDetectionResult(True, traffic_light)

        return TrafficLightDetectionResult(False, None)


def detect_traffic_light(self : "LunaticAgent", traffic_lights : Optional[List["carla.TrafficLight"]] = None) -> TrafficLightDetectionResult:
    """
    This method is in charge of behaviors for red lights.
    """
    
    # Introduce a random chance to ignore the traffic light
    if random.random() < self.config.obstacles.ignore_lights_percentage:
        return TrafficLightDetectionResult(False, None)
    
    traffic_lights = traffic_lights or self.traffic_lights_nearby

    # Behavior setting:
    max_tlight_distance = self.config.obstacles.base_tlight_threshold
    if self.config.obstacles.dynamic_threshold:
        # Basic agent setting:
        #logger.info("Increased threshold for traffic light detection from {} to {}".format(max_tlight_distance, 
        #                                                                                  max_tlight_distance + self.config.obstacles.detection_speed_ratio * self.config.live_info.current_speed))
        max_tlight_distance += self.config.obstacles.detection_speed_ratio * self.config.live_info.current_speed
        
    # TODO: Time to pass the traffic light; i.e. can we pass it without stopping? -> How risky are we?

    # TODO check if lights should be copied.
    # lights = self.lights_list.copy() #could remove certain lights, or the current one for some ticks
    affected_traffic_light : TrafficLightDetectionResult = affected_by_traffic_light(self, traffic_lights, 
                                    max_distance=max_tlight_distance)
    
    if (affected_traffic_light.traffic_light_was_found 
        and affected_traffic_light.traffic_light.state == TrafficLightState.Red):  # type: ignore[attr]
        self.current_states[AgentState.BLOCKED_RED_LIGHT] += 1
    else:
        self.current_states[AgentState.BLOCKED_RED_LIGHT] = 0

    # TODO: Implement other behaviors if needed, like taking a wrong turn or additional actions

    return affected_traffic_light