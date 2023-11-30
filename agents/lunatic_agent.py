# Copyright (c) # Copyright (c) 2018-2020 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

# NOTE: This file currently contains code from the three agents that were implemented in the original CARLA repo. so
# no added customization yet, also not yet all useful code.

""" This module implements an agent that roams around a track following random
waypoints and avoiding other vehicles. The agent also responds to traffic lights,
traffic signs, and has different possible configurations. """

import random
import numpy as np
import carla

from shapely.geometry import Polygon
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.tools.misc import (get_speed, is_within_distance,
                               get_trafficlight_trigger_location,
                               compute_distance)

from agents.navigation.behavior_agent import BehaviorAgent

# NEW: Style
from agents.dynamic_planning.dynamic_local_planner import DynamicLocalPlanner, RoadOption
from config.default_options.original_behavior import BasicAgentSettings
from config.lunatic_behavior_settings import LunaticBehaviorSettings


# As Reference:
'''
class RoadOption(IntEnum):
    """
    RoadOption represents the possible topological configurations 
    when moving from a segment of lane to other.
    """
    VOID = -1
    LEFT = 1
    RIGHT = 2
    STRAIGHT = 3
    LANEFOLLOW = 4
    CHANGELANELEFT = 5
    CHANGELANERIGHT = 6
'''


class LunaticAgent(BehaviorAgent):
    """
    BasicAgent implements an agent that navigates the scene.
    This agent respects traffic lights and other vehicles, but ignores stop signs.
    It has several functions available to specify the route that the agent must follow,
    as well as to change its parameters in case a different driving mode is desired.
    """

    # todo: rename in the future

    def __init__(self, vehicle, behavior : LunaticBehaviorSettings, map_inst=None, grp_inst=None, overwrite_options: dict = {}):
        """
        Initialization the agent parameters, the local and the global planner.

            :param vehicle: actor to apply to agent logic onto
            :param target_speed: speed (in Km/h) at which the vehicle will move
            :param opt_dict: dictionary in case some of its parameters want to be changed.
                This also applies to parameters related to the LocalPlanner.
            :param map_inst: carla.Map instance to avoid the expensive call of getting it.
            :param grp_inst: GlobalRoutePlanner instance to avoid the expensive call of getting it.

        """
        # TODO s: Always expect a behavior.opt_dict
        # low prio todo: update description.

        # OURS: Fusing behavior

        # Settings ---------------------------------------------------------------
        print("Behavior of Agent", behavior)
        if isinstance(behavior, BasicAgentSettings):
            self._behavior = behavior
        else:
            raise ValueError("Behavior must be a " + str(BasicAgentSettings))

        opt_dict = self._behavior.get_options()  # base options from templates
        opt_dict.update(overwrite_options)  # update by custom options

        self.config = opt_dict # NOTE: This is the attribute we should use to access all information. 
        self.live_info = self.config.live_info

        # todo set a initial tailgaite counter here, either as instance variable or in live_info
        self.config.live_info.current_tailgate_counter = self.config.other.tailgate_counter

        # Original Setup ---------------------------------------------------------
        self._vehicle = vehicle
        self._world = self._vehicle.get_world()
        
        if map_inst:
            if isinstance(map_inst, carla.Map):
                self._map = map_inst
            else:
                print("Warning: Ignoring the given map as it is not a 'carla.Map'")
                self._map = self._world.get_map()
        else:
            self._map = self._world.get_map()
        self._last_traffic_light = None  # Current red traffic light

        # TODO: No more hardcoded defaults / set them from opt_dict which must have all parameters; check which are parameters and which are set by other functions (e.g. _look_ahead_steps)

        # Parameters from BehaviorAgent ------------------------------------------
        # todo: check redefinitions
        self._look_ahead_steps = 0  # updated in _update_information used for local_planner.get_incoming_waypoint_and_direction

        # Vehicle information
        self.live_info.speed = 0
        self.live_info.speed_limit = 0
        self.live_info.direction = None
        self._incoming_direction = None
        self._incoming_waypoint = None
        #config.speed.min_speed = 5
        self.config.speed.min_speed
        #config.unknown.sampling_resolution = 4.5  # NOTE also set in behaviors

        # Change parameters according to the dictionary
        # opt_dict['target_speed'] = target_speed
        # TODO instead of storing variables updating the dict could change the agent dynamically.
        #        con: Not intuitive.
        #        Better: A update_options(dict) function
        # TODO: instead of checking now throw failures if an option is not present in opt_dict (ours contains all parameters)

        # Initialize the planners
        self._local_planner = DynamicLocalPlanner(self._vehicle, opt_dict=opt_dict, map_inst=self._map, world=self._world if self._world else "MISSING")
        if grp_inst:
            if isinstance(grp_inst, GlobalRoutePlanner):
                self._global_planner = grp_inst
            else:
                print("Warning: Ignoring the given map as it is not a 'carla.Map'")
                self._global_planner = GlobalRoutePlanner(self._map, self.config.unknown.sampling_resolution)
        else:
            self._global_planner = GlobalRoutePlanner(self._map, self.config.unknown.sampling_resolution)

        # Get the static elements of the scene
        self._lights_list = self._world.get_actors().filter("*traffic_light*")
        self._lights_map = {}  # Dictionary mapping a traffic light to a wp corresponding to its trigger volume location

        # From ConstantVelocityAgent ----------------------------------------------
        self._collision_sensor = None
        self._set_collision_sensor()

    def _set_collision_sensor(self):
        blueprint = self._world.get_blueprint_library().find('sensor.other.collision')
        self._collision_sensor = self._world.spawn_actor(blueprint, carla.Transform(), attach_to=self._vehicle)
        self._collision_sensor.listen(lambda event: self._collision_event())

    def destroy_sensor(self):
        if self._collision_sensor:
            self._collision_sensor.destroy()
            self._collision_sensor = None

    def _collision_event(self):
        # TODO: Brainstorm and implement
        # e.g. setting ignore_vehicles to False, if it was True before.
        # do an emergency stop (in certain situations)
        NotImplemented
    
    def temporary_settings(self, temp_settings: dict) -> dict:
        """
        Returns a new dictionary with the agent's settings overwritten by the given temporary settings.
        NOTE: This does not change the agent's settings only returns a new dictionary to be used.
        """
        # TODO: Maybe make a temp_settings attribute, problem what if multiple temporary settings are needed that live longer.
        return { **self.config, **temp_settings} 

    def set_target_speed(self, speed):
        """
        Changes the target speed of the agent
            :param speed (float): target speed in Km/h
        """
        if self.config.speed.follow_speed_limits:
            print("WARNING: The max speed is currently set to follow the speed limits. "
                  "Use 'follow_speed_limits' to deactivate this")
        self.config.speed.target_speed = speed # shared with planner

    def follow_speed_limits(self, value=True):
        """
        If active, the agent will dynamically change the target speed according to the speed limits
            :param value: (bool) whether to activate this behavior
        """
        self._local_planner.follow_speed_limits(value)

    #def get_local_planner(self):
    #def get_global_planner(self):

    def set_destination(self, end_location, start_location=None):
        """
        This method creates a list of waypoints between a starting and ending location,
        based on the route returned by the global router, and adds it to the local planner.
        If no starting location is passed, the vehicle local planner's target location is chosen,
        which corresponds (by default), to a location about 5 meters in front of the vehicle.

            :param end_location (carla.Location): final location of the route
            :param start_location (carla.Location): starting location of the route
        """
        if not start_location:
            start_location = self._local_planner.target_waypoint.transform.location
            clean_queue = True
        else:
            start_location = self._vehicle.get_location()
            clean_queue = False

        start_waypoint = self._map.get_waypoint(start_location)
        end_waypoint = self._map.get_waypoint(end_location)

        route_trace = self.trace_route(start_waypoint, end_waypoint)
        self._local_planner.set_global_plan(route_trace, clean_queue=clean_queue)

    def set_global_plan(self, plan, stop_waypoint_creation=True, clean_queue=True):
        """
        Adds a specific plan to the agent.

            :param plan: list of [carla.Waypoint, RoadOption] representing the route to be followed
            :param stop_waypoint_creation: stops the automatic random creation of waypoints
            :param clean_queue: resets the current agent's plan
        """
        self._local_planner.set_global_plan(
            plan,
            stop_waypoint_creation=stop_waypoint_creation,
            clean_queue=clean_queue
        )

    def trace_route(self, start_waypoint, end_waypoint):
        """
        Calculates the shortest route between a starting and ending waypoint.

            :param start_waypoint (carla.Waypoint): initial waypoint
            :param end_waypoint (carla.Waypoint): final waypoint
        """
        start_location = start_waypoint.transform.location
        end_location = end_waypoint.transform.location
        return self._global_planner.trace_route(start_location, end_location)

    def _update_information(self):
        """
        This method updates the information regarding the ego
        vehicle based on the surrounding world.
        """
        self.live_info.current_speed = get_speed(self._vehicle)
        self.live_info.current_speed_limit = self._vehicle.get_speed_limit()
        # planner has access to config
        #self._local_planner.set_speed(self.live_info.speed_limit)            # <-- Adjusts Planner
        
        self.live_info.direction : RoadOption = self._local_planner.target_road_option
        if self.live_info.direction is None:
            self.live_info.direction = RoadOption.LANEFOLLOW

        self._look_ahead_steps = int((self.live_info.speed_limit) / 10)

        self._incoming_waypoint, self._incoming_direction = self._local_planner.get_incoming_waypoint_and_direction(
            steps=self._look_ahead_steps)
        if self._incoming_direction is None:
            self._incoming_direction = RoadOption.LANEFOLLOW

    def run_step(self, debug=False):
        # NOTE: This is our main entry point that runs every tick.
        self._update_information()
        # Detect hazards
        hazard_detected = self.detect_hazard()
        # React based on detected hazards and behaviors
        control = self.react_to_hazard(hazard_detected, debug)
        return control

    def detect_hazard(self):
        vehicle_list = self._world.get_actors().filter("*vehicle*")

        vehicle_speed = get_speed(self._vehicle) / 3.6

        # Check for possible vehicle obstacles
        max_vehicle_distance = self.config.obstacles.base_vehicle_threshold + self.config.obstacles.detection_speed_ratio * vehicle_speed
        affected_by_vehicle, _, _ = self._vehicle_obstacle_detected(vehicle_list, max_vehicle_distance)
        if affected_by_vehicle:
            hazard_detected = True

        # Check if the vehicle is affected by a red traffic light
        max_tlight_distance = self.config.obstacles.base_tlight_threshold + self.config.obstacles.detection_speed_ratio * vehicle_speed
        affected_by_tlight, _ = self._affected_by_traffic_light(self._lights_list, max_tlight_distance)
        if affected_by_tlight:
            hazard_detected = True

        # Combine hazard detection results
        return affected_by_vehicle or affected_by_tlight

    def react_to_hazard(self, hazard_detected, debug):
        control = None

        if hazard_detected:
            control = self.add_emergency_stop(self._local_planner.run_step())

        # Other behaviors based on hazard detection
        else:
            self.config.other.tailgate_counter = max(0, self.config.other.tailgate_counter - 1)
            ego_vehicle_loc = self._vehicle.get_location()
            ego_vehicle_wp = self._map.get_waypoint(ego_vehicle_loc)

            # Red lights and stops behavior
            if self.traffic_light_manager():
                return self.emergency_stop()

            # Pedestrian avoidance behaviors
            walker_state, walker, w_distance = self.pedestrian_avoid_manager(ego_vehicle_wp)
            # TODO: Here we should insert rules:
            if walker_state and (w_distance - max(walker.bounding_box.extent.y, walker.bounding_box.extent.x)
                                 - max(self._vehicle.bounding_box.extent.y, self._vehicle.bounding_box.extent.x)
                                 < self.config.distance.braking_distance):
                return self.emergency_stop()

            # Car following behaviors
            vehicle_state, vehicle, distance = self.collision_and_car_avoid_manager(ego_vehicle_wp)
            if vehicle_state:
                distance = distance - max(vehicle.bounding_box.extent.y, vehicle.bounding_box.extent.x) - max(
                    self._vehicle.bounding_box.extent.y, self._vehicle.bounding_box.extent.x)

                if distance < self.config.distance.braking_distance:
                    return self.emergency_stop()
                else:
                    control = self.car_following_manager(vehicle, distance)

            # Intersection behavior
            elif self._incoming_waypoint.is_junction and (
                    self._incoming_direction in [RoadOption.LEFT, RoadOption.RIGHT]):
                target_speed = min([
                    self.config.speed.max_speed,
                    self.config.live_info.current_speed_limit - 5])
                self._local_planner.set_speed(target_speed)
                control = self._local_planner.run_step(debug=debug)

            # Normal behavior
            else:
                target_speed = min([
                    self.config.speed.max_speed,
                    self.config.live_info.current_speed_limit - self.config.speed.speed_lim_dist])
                self._local_planner.set_speed(target_speed)
                control = self._local_planner.run_step(debug=debug)

        return control

    # NEW
    def get_current_waypoint(self):
        ego_vehicle_loc = self._vehicle.get_location()
        ego_vehicle_wp = self._map.get_waypoint(ego_vehicle_loc)
        return ego_vehicle_wp


    # TODO: The manager functions could be moved into a separate class or file
    # ; cleans up space here and might be more logical
    def pedestrian_avoid_manager(self, waypoint):
        """
        This module is in charge of warning in case of a collision
        with any pedestrian.

            :param location: current location of the agent
            :param waypoint: current waypoint of the agent
            :return vehicle_state: True if there is a walker nearby, False if not
            :return vehicle: nearby walker
            :return distance: distance to nearby walker
        """

        walker_list = self._world.get_actors().filter("*walker.pedestrian*")

        def dist(w):
            return w.get_location().distance(waypoint.transform.location)

        walker_list = [w for w in walker_list if dist(w) < 10]

        if self.config.live_info.direction == RoadOption.CHANGELANELEFT:
            walker_state, walker, distance = self._vehicle_obstacle_detected(walker_list, max(
                self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=90, lane_offset=-1)
        elif self.config.live_info.direction == RoadOption.CHANGELANERIGHT:
            walker_state, walker, distance = self._vehicle_obstacle_detected(walker_list, max(
                self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=90, lane_offset=1)
        else:
            walker_state, walker, distance = self._vehicle_obstacle_detected(walker_list, max(
                self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 3), up_angle_th=60)

        return walker_state, walker, distance

    def car_following_manager(self, vehicle, distance, debug=False):
        """
        Module in charge of car-following behaviors when there's
        someone in front of us.

            :param vehicle: car to follow
            :param distance: distance from vehicle
            :param debug: boolean for debugging
            :return control: carla.VehicleControl
        """

        vehicle_speed = get_speed(vehicle)
        delta_v = max(1, (self.config.live_info.current_speed - vehicle_speed) / 3.6)
        ttc = (distance / delta_v if delta_v != 0  # TimeTillCollision
               else distance / np.nextafter(0., 1.)  # do not divide by 0,
               )

        # Under safety time distance, slow down.
        if self.config.speed.safety_time > ttc > 0.0:
            target_speed = min([
                max(0.0, vehicle_speed - self.config.speed.speed_decrease),
                self.config.speed.max_speed,
                self.config.live_info.current_speed_limit - self.config.speed.speed_lim_dist])
            self._local_planner.set_speed(target_speed)
            control = self._local_planner.run_step(debug=debug)

        # Actual safety distance area, try to follow the speed of the vehicle in front.
        elif 2 * self.config.speed.safety_time > ttc >= self.config.speed.safety_time:
            target_speed = min([
                max(self._min_speed, vehicle_speed),
                self.config.speed.max_speed,
                self.config.live_info.current_speed_limit - self.config.speed.speed_lim_dist])
            self._local_planner.set_speed(target_speed)
            control = self._local_planner.run_step(debug=debug)

        # Normal behavior.
        else:
            target_speed = min([
                self.config.speed.max_speed,
                self.config.live_info.current_speed_limit - self.config.speed.speed_lim_dist])
            self._local_planner.set_speed(target_speed)
            control = self._local_planner.run_step(debug=debug)

        return control

    def collision_and_car_avoid_manager(self, waypoint):
        """
        This module is in charge of warning in case of a collision
        and managing possible tailgating chances.

            :param location: current location of the agent
            :param waypoint: current waypoint of the agent
            :return vehicle_state: True if there is a vehicle nearby, False if not
            :return vehicle: nearby vehicle
            :return distance: distance to nearby vehicle
        """

        vehicle_list = self._world.get_actors().filter("*vehicle*")

        def dist(v): # is it more efficient to use an extra function here, why not utils.dist_to_waypoint(v, waypoint)?
            return v.get_location().distance(waypoint.transform.location)

        vehicle_list = [v for v in vehicle_list if dist(v) < 45 and v.id != self._vehicle.id]

        # Triple (<is there an obstacle> , )
        if self.config.live_info.direction == RoadOption.CHANGELANELEFT:
            vehicle_state, vehicle, distance = self._vehicle_obstacle_detected(
                vehicle_list, max(
                    self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=-1)
        elif self.config.live_info.direction == RoadOption.CHANGELANERIGHT:
            vehicle_state, vehicle, distance = self._vehicle_obstacle_detected(
                vehicle_list, max(
                    self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=1)
        else:
            vehicle_state, vehicle, distance = self._vehicle_obstacle_detected(
                vehicle_list, max(
                    self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 3), up_angle_th=30)

            # Check for tailgating
            if not vehicle_state and self.config.live_info.direction == RoadOption.LANEFOLLOW \
                    and not waypoint.is_junction and self.config.live_info.current_speed > 10 \
                    and self.config.other.tailgate_counter == 0:
                self._tailgating(waypoint, vehicle_list)

        return vehicle_state, vehicle, distance


    #def done(self): # from base class self._local_planner.done()

    def ignore_traffic_lights(self, active=True):
        """(De)activates the checks for traffic lights"""
        self.config.obstacles.ignore_traffic_lights = active

    def ignore_stop_signs(self, active=True):
        """(De)activates the checks for stop signs"""
        self.config.obstacles.ignore_stop_signs = active

    def ignore_vehicles(self, active=True):
        """(De)activates the checks for stop signs"""
        self.config.obstacles.ignore_vehicles = active

    def lane_change(self, direction, same_lane_time=0, other_lane_time=0, lane_change_time=2):
        """
        Changes the path so that the vehicle performs a lane change.
        Use 'direction' to specify either a 'left' or 'right' lane change,
        and the other 3 fine tune the maneuver
        """
        speed = self._vehicle.get_velocity().length()
        path : list = self._generate_lane_change_path(
            self._map.get_waypoint(self._vehicle.get_location()), # get current waypoint
            direction,
            same_lane_time * speed, # get direction in meters t*V
            other_lane_time * speed,
            lane_change_time * speed,
            check=False,        # TODO: Explanation of this parameter? Make use of it and & how? Could mean that it is checked if there is a left lane
            lane_changes=1,     # changes only one lane
            step_distance= self.config.unknown.sampling_resolution
        )
        if not path:
            print("WARNING: Ignoring the lane change as no path was found")

        self.set_global_plan(path)

    @staticmethod
    def _generate_lane_change_path(waypoint, direction='left', distance_same_lane=10,
                                   distance_other_lane=25, lane_change_distance=25,
                                   check=True, lane_changes=1, step_distance=2):
        """
        This method generates a path that results in a lane change.
        Use the different distances to fine-tune the maneuver.
        If the lane change is impossible, the returned path will be empty.
        """
        distance_same_lane = max(distance_same_lane, 0.1)
        distance_other_lane = max(distance_other_lane, 0.1)
        lane_change_distance = max(lane_change_distance, 0.1)

        plan = [(waypoint, RoadOption.LANEFOLLOW)]
        option = RoadOption.LANEFOLLOW

        # Same lane
        distance = 0
        while distance < distance_same_lane:
            next_wps = plan[-1][0].next(step_distance)  # follow a path of waypoints
            if not next_wps:
                return []
            next_wp = next_wps[0]
            distance += next_wp.transform.location.distance(plan[-1][0].transform.location)
            plan.append((next_wp, RoadOption.LANEFOLLOW))  # next waypoint to the path

        if direction == 'left':
            option = RoadOption.CHANGELANELEFT
        elif direction == 'right':
            option = RoadOption.CHANGELANERIGHT
        else:
            # ERROR, input value for change must be 'left' or 'right'
            return []

        lane_changes_done = 0
        lane_change_distance = lane_change_distance / lane_changes

        # Lane change
        while lane_changes_done < lane_changes:

            # Move forward
            next_wps = plan[-1][0].next(lane_change_distance)
            if not next_wps:
                return []
            next_wp = next_wps[0]

            # Get the side lane
            if direction == 'left':
                if check and str(next_wp.lane_change) not in ['Left', 'Both']:
                    return []
                side_wp = next_wp.get_left_lane()  # get waypoint on other lane
            else:
                if check and str(next_wp.lane_change) not in ['Right', 'Both']:
                    return []
                side_wp = next_wp.get_right_lane()

            if not side_wp or side_wp.lane_type != carla.LaneType.Driving:
                return []

            # Update the plan
            plan.append((side_wp, option))
            lane_changes_done += 1

        # Other lane
        # NOTE: Might force it to follow the other lane for some time
        distance = 0
        while distance < distance_other_lane:
            next_wps = plan[-1][0].next(step_distance)
            if not next_wps:
                return []
            next_wp = next_wps[0]
            distance += next_wp.transform.location.distance(plan[-1][0].transform.location)
            plan.append((next_wp, RoadOption.LANEFOLLOW))

        return plan

    def traffic_light_manager(self):
        """
        This method is in charge of behaviors for red lights.
        """
        # Introduce a random chance to ignore the traffic light
        
        # Todo: check if drawing randomly each step is more efficient than the calculation below
        if random.random() < self.config.obstacles.ignore_lights_percentage:
            return False
    	
        # TODO check if lights should be copied.
        # lights = self.lights_list.copy() #could remove certain lights, or the current one for some ticks
        affected, traffic_light = self._affected_by_traffic_light(self._lights_list, 
						max_distance=self.config.obstacles.base_tlight_threshold)

        # TODO: Implement other behaviors if needed, like taking a wrong turn or additional actions

        return affected

    def _affected_by_traffic_light(self, lights_list=None, max_distance=None):
        """
        Method to check if there is a red light affecting the vehicle.

            :param lights_list (list of carla.TrafficLight): list containing TrafficLight objects.
                If None, all traffic lights in the scene are used
            :param max_distance (float): max distance for traffic lights to be considered relevant.
                If None, the base threshold value is used
        """
        if self.config.obstacles.ignore_traffic_lights:
            return (False, None)

        if not lights_list:
            lights_list = self._world.get_actors().filter("*traffic_light*")

        if not max_distance:
            max_distance = self.config.obstacles.base_tlight_threshold

        if self._last_traffic_light:
            if self._last_traffic_light.state != carla.TrafficLightState.Red:
                self._last_traffic_light = None
            else:
                return True, self._last_traffic_light

        ego_vehicle_location = self._vehicle.get_location()
        ego_vehicle_waypoint = self._map.get_waypoint(ego_vehicle_location)

        for traffic_light in lights_list:
            if traffic_light.id in self._lights_map:
                trigger_wp = self._lights_map[traffic_light.id]
            else:
                trigger_location = get_trafficlight_trigger_location(traffic_light)
                trigger_wp = self._map.get_waypoint(trigger_location)
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

            if traffic_light.state != carla.TrafficLightState.Red:
                continue

            if is_within_distance(trigger_wp.transform, self._vehicle.get_transform(), max_distance, [0, 90]):
                self._last_traffic_light = traffic_light
                return True, traffic_light

        return False, None

    # TODO: see if max_distance is currently still necessary
    # TODO: move angles to config
    #@override
    def _vehicle_obstacle_detected(self, vehicle_list=None, max_distance=None, up_angle_th=90, low_angle_th=0,
                                   lane_offset=0):
        """
        Method to check if there is a vehicle in front of the agent blocking its path.

            :param vehicle_list (list of carla.Vehicle): list containing vehicle objects.
                If None, all vehicle in the scene are used
            :param max_distance: max free-space to check for obstacles.
                If None, the base threshold value is used
        """
        def get_route_polygon():
            # Note nested functions can access variables from the outer scope
            route_bb = []
            extent_y = self._vehicle.bounding_box.extent.y
            r_ext = extent_y + self.config.controls.offset
            l_ext = -extent_y + self.config.controls.offset
            r_vec = ego_transform.get_right_vector()
            p1 = ego_location + carla.Location(r_ext * r_vec.x, r_ext * r_vec.y)
            p2 = ego_location + carla.Location(l_ext * r_vec.x, l_ext * r_vec.y)
            route_bb.extend([[p1.x, p1.y, p1.z], [p2.x, p2.y, p2.z]])

            for wp, _ in self._local_planner.get_plan():
                if ego_location.distance(wp.transform.location) > max_distance:
                    break

                r_vec = wp.transform.get_right_vector()
                p1 = wp.transform.location + carla.Location(r_ext * r_vec.x, r_ext * r_vec.y)
                p2 = wp.transform.location + carla.Location(l_ext * r_vec.x, l_ext * r_vec.y)
                route_bb.extend([[p1.x, p1.y, p1.z], [p2.x, p2.y, p2.z]])

            # Two points don't create a polygon, nothing to check
            if len(route_bb) < 3:
                return None

            return Polygon(route_bb)

        if self.config.obstacles.ignore_vehicles:
            return (False, None, -1)

        if not vehicle_list:
            vehicle_list = self._world.get_actors().filter("*vehicle*")

        if not max_distance:
            max_distance = self.config.obstacles.base_vehicle_threshold

        ego_transform = self._vehicle.get_transform()
        ego_location = ego_transform.location
        ego_wpt = self._map.get_waypoint(ego_location)

        # Get the right offset
        if ego_wpt.lane_id < 0 and lane_offset != 0:
            lane_offset *= -1

        # Get the transform of the front of the ego
        ego_front_transform = ego_transform
        ego_front_transform.location += carla.Location(
            self._vehicle.bounding_box.extent.x * ego_transform.get_forward_vector())

        opposite_invasion = abs(self.config.controls.offset) + self._vehicle.bounding_box.extent.y > ego_wpt.lane_width / 2
        use_bbs = self.config.unknown.use_bbs_detection or opposite_invasion or ego_wpt.is_junction

        # Get the route bounding box
        route_polygon = get_route_polygon()

        for target_vehicle in vehicle_list:
            if target_vehicle.id == self._vehicle.id:
                continue

            target_transform = target_vehicle.get_transform()
            if target_transform.location.distance(ego_location) > max_distance:
                continue

            target_wpt = self._map.get_waypoint(target_transform.location, lane_type=carla.LaneType.Any)

            # General approach for junctions and vehicles invading other lanes due to the offset
            if (use_bbs or target_wpt.is_junction) and route_polygon:

                target_bb = target_vehicle.bounding_box
                target_vertices = target_bb.get_world_vertices(target_vehicle.get_transform())
                target_list = [[v.x, v.y, v.z] for v in target_vertices]
                target_polygon = Polygon(target_list)

                if route_polygon.intersects(target_polygon):
                    return (True, target_vehicle, compute_distance(target_vehicle.get_location(), ego_location))

            # Simplified approach, using only the plan waypoints (similar to TM)
            else:

                if target_wpt.road_id != ego_wpt.road_id or target_wpt.lane_id != ego_wpt.lane_id + lane_offset:
                    next_wpt = self._local_planner.get_incoming_waypoint_and_direction(steps=3)[0]
                    if not next_wpt:
                        continue
                    if target_wpt.road_id != next_wpt.road_id or target_wpt.lane_id != next_wpt.lane_id + lane_offset:
                        continue

                target_forward_vector = target_transform.get_forward_vector()
                target_extent = target_vehicle.bounding_box.extent.x
                target_rear_transform = target_transform
                target_rear_transform.location -= carla.Location(
                    x=target_extent * target_forward_vector.x,
                    y=target_extent * target_forward_vector.y,
                )

                if is_within_distance(target_rear_transform, ego_front_transform, max_distance,
                                      [low_angle_th, up_angle_th]):
                    return True, target_vehicle, compute_distance(target_transform.location, ego_transform.location)

        return False, None, -1

    #@override
    def emergency_stop(self):
        raise NotImplementedError("This function was overwritten use ´add_emergency_stop´ instead")

    #@override
    # TODO: Port this to a rule that is used during emergencies.
    def add_emergency_stop(self, control, reason:str=None):
        """
        Modifies the control values to perform an emergency stop.
        The steering remains unchanged to avoid going out of the lane during turns.

        :param control: (carla.VehicleControl) control to be modified
        :param enable_random_steer: (bool, optional) Flag to enable random steering
        """

        # TODO, future: Use rules here.
        if self.config.emergency.ignore_percentage > 0.0 and self.config.emergency.ignore_percentage / 100 > random.random():
            return control
        
        control.throttle = 0.0
        # negate the chosen default setting
        if self.config.emergency.hand_brake_modify_chance > 0.0 and self.config.emergency.hand_brake_modify_chance / 100 > random.random():
            control.hand_brake = not self.config.emergency.use_hand_brake
        else:
            control.hand_brake = self.config.emergency.use_hand_brake

        # Enable random steering if flagged
        if self.config.emergency.do_random_steering:
            control.steer = random.uniform(*self.config.emergency.random_steering_range)  # Randomly adjust steering

        return control
    
    # ported from behavior_agent, maybe we can make a # updated behaviorAgent class
    #@override
    def _tailgating(self, waypoint, vehicle_list):
        """
        This method is in charge of tailgating behaviors.

            :param location: current location of the agent
            :param waypoint: current waypoint of the agent
            :param vehicle_list: list of all the nearby vehicles
        """

        left_turn = waypoint.left_lane_marking.lane_change
        right_turn = waypoint.right_lane_marking.lane_change

        left_wpt = waypoint.get_left_lane()
        right_wpt = waypoint.get_right_lane()

        behind_vehicle_state, behind_vehicle, _ = self._vehicle_obstacle_detected(vehicle_list, max(
            self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=180, low_angle_th=160)
        if behind_vehicle_state and self._speed < get_speed(behind_vehicle):
            if (right_turn == carla.LaneChange.Right or right_turn ==
                carla.LaneChange.Both) and waypoint.lane_id * right_wpt.lane_id > 0 and right_wpt.lane_type == carla.LaneType.Driving:
                new_vehicle_state, _, _ = self._vehicle_obstacle_detected(vehicle_list, max(
                    self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=1)
                if not new_vehicle_state:
                    print("Tailgating, moving to the right!")
                    end_waypoint = self._local_planner.target_waypoint
                    self.config.other.tailgate_counter = 200
                    self.set_destination(end_waypoint.transform.location,
                                         right_wpt.transform.location)
            elif left_turn == carla.LaneChange.Left and waypoint.lane_id * left_wpt.lane_id > 0 and left_wpt.lane_type == carla.LaneType.Driving:
                new_vehicle_state, _, _ = self._vehicle_obstacle_detected(vehicle_list, max(
                    self.config.distance.min_proximity_threshold, self.config.live_info.current_speed_limit / 2), up_angle_th=180, lane_offset=-1)
                if not new_vehicle_state:
                    print("Tailgating, moving to the left!")
                    end_waypoint = self._local_planner.target_waypoint
                    self.config.other.tailgate_counter = 200
                    self.set_destination(end_waypoint.transform.location,
                                         left_wpt.transform.location)

