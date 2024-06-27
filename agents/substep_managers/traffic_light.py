import random
from typing import TYPE_CHECKING, List

import carla
from carla import TrafficLightState
from agents.tools import logger
from agents.tools.hints import TrafficLightDetectionResult
from agents.tools.misc import (is_within_distance,
                               get_trafficlight_trigger_location)

from launch_tools import CarlaDataProvider

if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent
    
def _is_red_light(traffic_light : "carla.TrafficLight") -> bool:
    return traffic_light.state == TrafficLightState.Red

def affected_by_traffic_light(self : "LunaticAgent", 
                              lights_list : List["carla.TrafficLight"]=None, 
                              max_distance : float=None) -> TrafficLightDetectionResult:
        """
        Method to check if there is a red light affecting the vehicle.

            :param lights_list (list of carla.TrafficLight): list containing TrafficLight objects.
                If None, all traffic lights in the scene are used
            :param max_distance (float): max distance for traffic lights to be considered relevant.
                If None, the base threshold value is used
        """
        if self.config.obstacles.ignore_traffic_lights:
            return TrafficLightDetectionResult(False, None)

        if not lights_list:
            if self._world_model._args.debug:
                logger.warning("No traffic lights list provided, using all traffic lights in the scene. This should not happen.")
            lights_list = self._world.get_actors().filter("*traffic_light*")

        if not max_distance:
            max_distance = self.config.obstacles.base_tlight_threshold

        # Currently affected by a traffic light
        if self._last_traffic_light:
            if self._last_traffic_light.state != TrafficLightState.Red:
                self._last_traffic_light = None
            else: # Still Red
                return TrafficLightDetectionResult(True, self._last_traffic_light)

        ego_vehicle_location = self.config.live_info.current_location
        ego_vehicle_waypoint = self._current_waypoint

        for traffic_light in filter(_is_red_light, lights_list):
            if traffic_light.id in self._lights_map:
                trigger_wp = self._lights_map[traffic_light.id]
            else:
                trigger_location = get_trafficlight_trigger_location(traffic_light)
                trigger_wp = CarlaDataProvider.get_map().get_waypoint(trigger_location)
                self._lights_map[traffic_light.id] = trigger_wp

            if trigger_wp.transform.location.distance(ego_vehicle_location) > max_distance:
                continue

            if trigger_wp.road_id != ego_vehicle_waypoint.road_id:
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


def traffic_light_manager(self : "LunaticAgent", traffic_lights : List["carla.TrafficLight"]) -> TrafficLightDetectionResult:
        """
        This method is in charge of behaviors for red lights.
        """
        
        # Introduce a random chance to ignore the traffic light
        if random.random() < self.config.obstacles.ignore_lights_percentage:
            return TrafficLightDetectionResult(False, None)

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

        # TODO: Implement other behaviors if needed, like taking a wrong turn or additional actions

        return affected_traffic_light