# pyright: reportPrivateUsage=false

from __future__ import annotations

import random
from typing import Optional, TYPE_CHECKING, cast

import carla
from carla import TrafficLightState

from agents.tools.hints import TrafficLightDetectionResult
from agents.tools.logs import logger
from agents.tools.misc import is_within_distance
from classes.constants import AgentState
from classes.information_manager import InformationManager
from launch_tools import CarlaDataProvider

if TYPE_CHECKING:
    from classes.type_protocols import ActorList, CanDetectNearbyTrafficLights


def _is_red_light(traffic_light : "carla.TrafficLight") -> bool:
    """Filter function to check if a traffic light is red."""
    return traffic_light.state == TrafficLightState.Red

def _is_red_or_yellow(traffic_light : "carla.TrafficLight") -> bool:
    """Filter function to check if a traffic light is red or yellow."""
    return traffic_light.state in (TrafficLightState.Red, TrafficLightState.Yellow)

def affected_by_traffic_light(self : "CanDetectNearbyTrafficLights",
                              lights_list : Optional[ActorList[carla.TrafficLight]] = None,
                              max_distance : Optional[float] = None) -> TrafficLightDetectionResult:
    """
    Method to check if there is a red light affecting the vehicle.

    Parameters:
        lights_list: list containing traffic light objects.
            If None, all traffic lights in the scene are used.
        max_distance: max distance for a traffic lights to be considered relevant.
            If None, the base threshold value is used.
    """
    if self.config.obstacles.ignore_traffic_lights:
        return TrafficLightDetectionResult(False, None)

    detect_yellow_tlighs = self.config.obstacles.detect_yellow_tlights

    # Currently affected by a traffic light
    if self._last_traffic_light:
        if self._last_traffic_light.state != TrafficLightState.Red and (not detect_yellow_tlighs or self._last_traffic_light.state != TrafficLightState.Yellow):
            self._last_traffic_light = None
        else:  # Still Red
            return TrafficLightDetectionResult(True, self._last_traffic_light)
    
    if lights_list is None:
        if self._world_model._args.debug:
            logger.warning("No traffic lights list provided, using all traffic lights in the scene. This should not happen."
                            "You possibly want to pass agent.traffic_lights_nearby or agent._lights_list instead.")
        lights_list = cast("carla.ActorList[carla.TrafficLight]",
                           CarlaDataProvider.get_all_actors().filter("*traffic_light*"))
    if len(lights_list) == 0:
        return TrafficLightDetectionResult(False, None)

    if not max_distance:  # NOTE: dynamic selection is done in traffic_light_manager
        max_distance = self.config.obstacles.base_tlight_threshold

    ego_vehicle_location = self.config.live_info.current_location
    ego_vehicle_waypoint = self._current_waypoint

    filtered_lights = filter(_is_red_or_yellow if detect_yellow_tlighs else _is_red_light, lights_list)  # type: ignore
    
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

def detect_traffic_light(self: CanDetectNearbyTrafficLights,
                         traffic_lights : Optional[ActorList[carla.TrafficLight]] = None) -> TrafficLightDetectionResult:
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
