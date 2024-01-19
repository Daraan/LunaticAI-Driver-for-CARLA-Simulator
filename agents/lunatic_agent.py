# Copyright (c) # Copyright (c) 2018-2020 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

# NOTE: This file currently contains code from the three agents that were implemented in the original CARLA repo. so
# no added customization yet, also not yet all useful code.

""" This module implements an agent that roams around a track following random
waypoints and avoiding other vehicles. The agent also responds to traffic lights,
traffic signs, and has different possible configurations. """

from functools import wraps
import random
from typing import List
import numpy as np
from omegaconf import DictConfig

import carla
from shapely.geometry import Polygon

from agents.navigation.global_route_planner import GlobalRoutePlanner
import agents.tools
from agents.tools.misc import (TrafficLightDetectionResult, get_speed, ObstacleDetectionResult, is_within_distance,
                               compute_distance)

from agents.navigation.behavior_agent import BehaviorAgent
from agents.tools.lunatic_agent_tools import Phases

# NEW: Style
from agents.dynamic_planning.dynamic_local_planner import DynamicLocalPlanner, RoadOption
from config.default_options.original_behavior import BasicAgentSettings
from config.lunatic_behavior_settings import LunaticBehaviorSettings

#from agents import rule_behavior
# TODO: Not a class currently, maybe move to tools.
from classes import managers

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

class Phases(Flag):
    <Phases.NONE: 0>,
    <Phases.UPDATE_INFORMATION|BEGIN: 5>,
    <Phases.UPDATE_INFORMATION|END: 6>,
    <Phases.PLAN_PATH|BEGIN: 9>,
    <Phases.PLAN_PATH|END: 10>,
    <Phases.DETECT_TRAFFIC_LIGHTS|BEGIN: 17>,
    <Phases.DETECT_TRAFFIC_LIGHTS|END: 18>,
    <Phases.DETECT_PEDESTRIANS|BEGIN: 33>,
    <Phases.DETECT_PEDESTRIANS|END: 34>,
    <Phases.DETECT_CARS|BEGIN: 65>,
    <Phases.DETECT_CARS|END: 66>,
    <Phases.POST_DETECTION_PHASE|BEGIN: 129>,
    <Phases.POST_DETECTION_PHASE|END: 130>,
    <Phases.MODIFY_FINAL_CONTROLS|BEGIN: 257>,
    <Phases.MODIFY_FINAL_CONTROLS|END: 258>,
    <Phases.EXECUTION|BEGIN: 1025>,
    <Phases.EXECUTION|END: 1026>

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
        self.live_info : DictConfig = self.config.live_info

        self.current_phase = Phases.NONE # current phase of the agent inside the loop

        # todo set a initial tailgaite counter here, either as instance variable or in live_info
        self.config.live_info.current_tailgate_counter : int = self.config.other.tailgate_counter

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
        self.rules = []

    def _set_collision_sensor(self):
        # see: https://carla.readthedocs.io/en/latest/ref_sensors/#collision-detector
        # and https://carla.readthedocs.io/en/latest/python_api/#carla.Sensor.listen
        blueprint = self._world.get_blueprint_library().find('sensor.other.collision')
        self._collision_sensor : carla.Sensor = self._world.spawn_actor(blueprint, carla.Transform(), attach_to=self._vehicle)
        def collision_callback(event : carla.SensorData):
            self._collision_event(event)
        self._collision_sensor.listen(collision_callback)

    def destroy_sensor(self):
        if self._collision_sensor:
            self._collision_sensor.destroy()
            self._collision_sensor = None

    # ------------------ Information functions ------------------ #

    def _update_information(self, exact_waypoint=True):
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

        self.location = ego_vehicle_loc = self._vehicle.get_location()
        if exact_waypoint:
            self._current_waypoint = self._map.get_waypoint(ego_vehicle_loc)
        else:
            self._current_waypoint = self._incoming_waypoint

        self.vehicles_nearby : List[carla.Vehicle] = self._world.get_actors().filter("*vehicle*")
        # TODO: Filter this to only contain relevant vehicles # i.e. certain radius and or lanes around us.

    def is_taking_turn(self) -> bool:
        return self._incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)

    # ------------------ Step & Loop Logic ------------------ #


    def add_rule(self, rule : Rule, position=-1):
        self.rules.insert(position, rule)
        

    def execute_phase(self, phase, *, phase_results, control:carla.VehicleControl=None):
        """
        Sets the current phase of the agent and executes all rules that are associated with it.
        """
        normal_next = self.current_phase.next
        assert phase == normal_next or phase & Phases.EXCEPTIONS, f"Phase {phase} is not the next phase of {self.current_phase} or an exception phase."
        
        self.current_phase = phase # set next phase
        for rule in self.rules: # todo: maybe dict? grouped by phase?
            #todo check here for the phase instead of in the rule
            if self.current_phase in rule.phases:
                rule(self, control=control, phase_results=phase_results)

    def run_step(self, debug=False):
        # NOTE: This is our main entry point that runs every tick.        
        self.execute_phase(Phases.UPDATE_INFORMATION | Phases.BEGIN)
        self.config.other.tailgate_counter = max(0, self.config.other.tailgate_counter - 1)
        self._update_information()
        self.execute_phase(Phases.UPDATE_INFORMATION | Phases.END)

        # Detect hazards
        # phases are executed in detect_hazard
        Phases.DETECT_TRAFFIC_LIGHTS | Phases.BEGIN # phases executed inside
        pedestrians_or_traffic_light = self.detect_hazard()
        Phases.DETECT_PEDESTRIANS | Phases.END

        # Pedestrian avoidance behaviors
        # currently doing either emergency (detect_hazard) stop or nothing 
        if pedestrians_or_traffic_light:
            print("Hazard detected", pedestrians_or_traffic_light)
            (control, end_loop) = self.react_to_hazard(controls=None, hazard_detected=pedestrians_or_traffic_light)
            # Other behaviors based on hazard detection
            # TODO: needs overhaul 
            if end_loop:
                return control
    
        # Car following behaviors
        self.execute_phase(Phases.DETECT_CARS | Phases.BEGIN)
        detection_result = self.collision_and_car_avoid_manager(self._current_waypoint)
        # TODO: add a way to let the execution overwrite
        if detection_result.obstacle_was_found:
            self.execute_phase(Phases.CAR_DETECTED | Phases.BEGIN)
            # TODO some way to circumvent returning control here
            # TODO: Needs refinement with fthe car_following_behavior
            control = self.car_following_behavior(*detection_result)
            self.execute_phase(Phases.CAR_DETECTED | Phases.END, control)
            return control
        #TODO: maybe new phase
        # NOte: avoiding tailgate here
        self.execute_phase(Phases.DETECT_CARS | Phases.END)     
        
        # Intersection behavior
        # TODO: another phase that indicates a junction is coming up
        # NOTE: is_taking_turn == self._incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)
        if self._incoming_waypoint.is_junction and self.is_taking_turn():
            self.execute_phase(Phases.TURNING_AT_JUNCTION | Phases.BEGIN)
            control = self.intersection_behavior() 
            self.execute_phase(Phases.TURNING_AT_JUNCTION | Phases.END, control)
            return control

        # Normal behavior
        self.execute_phase(Phases.TAKE_NORMAL_STEP | Phases.BEGIN)
        control = self.normal_behavior()
        self.execute_phase(Phases.TAKE_NORMAL_STEP | Phases.END, control)
        # Leave loop and apply conrols outside 
        # DISCUSS: Should we apply the controls here?
        return control

    # ------------------ Hazard Detection & Reaction ------------------ #

    def detect_hazard(self):
        hazard_detected = set()
        # Red lights and stops behavior

        self.execute_phase(Phases.DETECT_TRAFFIC_LIGHTS | Phases.BEGIN)
        if self.traffic_light_manager():
            hazard_detected.add("traffic_light")
        self.execute_phase(Phases.DETECT_TRAFFIC_LIGHTS | Phases.END)

        # Pedestrian avoidance behaviors
        self.execute_phase(Phases.DETECT_PEDESTRIANS | Phases.BEGIN)
        if self.pedestrian_avoidance_behavior(self._current_waypoint):
            hazard_detected.add("pedestrian")
        self.execute_phase(Phases.DETECT_PEDESTRIANS | Phases.END)
        
        return hazard_detected
    
    def react_to_hazard(self, controls, hazard_detected : set):
        # TODO: needs creative overhaul
        # Stop indicates if the loop shoul

        print("Hazard(s) detected: ", hazard_detected)
        
        end_loop = True
        if "pedestrian" in hazard_detected:
            pass
        if "traffic_light" in hazard_detected:
            pass
        controls = self.add_emergency_stop(controls)
        print("Emergency controls", controls)
        return controls, end_loop
    
    # ------------------ Behaviors ------------------ #

    def pedestrian_avoidance_behavior(self, ego_vehicle_wp):
        walker_state, walker, w_distance = self.pedestrian_avoid_manager(ego_vehicle_wp)
        if walker_state and (w_distance - max(walker.bounding_box.extent.y, walker.bounding_box.extent.x)
                             - max(self._vehicle.bounding_box.extent.y, self._vehicle.bounding_box.extent.x)
                             < self.config.distance.braking_distance):
            print("Detected walker", walker)
            return True
        # TODO detected but not stopping -> ADD avoidance behavior
        return False
        
    def car_following_behavior(self, vehicle_detected, vehicle, distance):
        distance = distance - max(vehicle.bounding_box.extent.y, vehicle.bounding_box.extent.x) - max(
            self._vehicle.bounding_box.extent.y, self._vehicle.bounding_box.extent.x)

        if distance < self.config.distance.braking_distance:
            controls, end_loop = self.react_to_hazard(controls=None, hazard_detected={"vehicle"})
        else:
            controls = self.car_following_manager(vehicle, distance)
        return controls



    # TODO: Speed should be adjusted by a Rule
    def intersection_behavior(self):
        return self._local_planner.run_step()

    def normal_behavior(self):
        return self._local_planner.run_step()

    # ------------------ Managers for Behaviour ------------------ #

    @wraps(managers.pedestrian_avoid_manager)
    def pedestrian_avoid_manager(self, waypoint) -> ObstacleDetectionResult:
        """
        This module is in charge of warning in case of a collision
        with any pedestrian.

            :param location: current location of the agent
            :param waypoint: current waypoint of the agent
            :return vehicle_state: True if there is a walker nearby, False if not
            :return vehicle: nearby walker
            :return distance: distance to nearby walker
        """
        return managers.pedestrian_avoid_manager(self, waypoint)
        
    @wraps(managers.car_following_manager)
    def car_following_manager(self, vehicle, distance, debug=False):
        return managers.car_following_manager(self, vehicle, distance, debug=debug)

    @wraps(managers.collision_and_car_avoid_manager)
    def collision_and_car_avoid_manager(self, waypoint) -> ObstacleDetectionResult:
        """
        This module is in charge of warning in case of a collision
        and managing possible tailgating chances.

            :param location: current location of the agent
            :param waypoint: current waypoint of the agent
            :return vehicle_state: True if there is a vehicle nearby, False if not
            :return vehicle: nearby vehicle
            :return distance: distance to nearby vehicle
        """
        return managers.collision_and_car_avoid_manager(self, waypoint)
    
    @wraps(managers.traffic_light_manager)
    def traffic_light_manager(self) -> TrafficLightDetectionResult:
        """
        This method is in charge of behaviors for red lights.
        """
        affected, traffic_light = managers.traffic_light_manager(self, self._lights_list)
        return affected
    
    def _collision_event(self, event : carla.CollisionEvent):
        # https://carla.readthedocs.io/en/latest/python_api/#carla.CollisionEvent
        # e.g. setting ignore_vehicles to False, if it was True before.
        # do an emergency stop (in certain situations)
        NotImplemented  # TODO: Brainstorm and implement
        return managers.collision_manager(self, event)

    # ----


    # TODO: see if max_distance is currently still necessary
    # TODO: move angles to config
    #@override
    @wraps(agents.tools.detect_vehicles)
    def _vehicle_obstacle_detected(self, vehicle_list=None, max_distance=None, 
                                   up_angle_th=90, 
                                   low_angle_th=0,
                                   lane_offset=0):
        """
        Method to check if there is a vehicle in front or around the agent blocking its path.

            :param vehicle_list (list of carla.Vehicle): list containing vehicle objects.
                If None, all vehicle in the scene are used
            :param max_distance: max free-space to check for obstacles.
                If None, the base threshold value is used

        The angle between the location and reference transform will also be taken into account. 
        Being 0 a location in front and 180, one behind, i.e, the vector between has to satisfy: 
        low_angle_th < angle < up_angle_th.
        """
        detected_vehicle_distance = agents.tools.detect_vehicles(self, vehicle_list, max_distance, up_angle_th, low_angle_th, lane_offset)
        return detected_vehicle_distance


    #@override
    # TODO: Port this to a rule that is used during emergencies.
    @wraps(managers.emergency_manager)
    def add_emergency_stop(self, control, reason:str=None):
        """
        Modifies the control values to perform an emergency stop.
        The steering remains unchanged to avoid going out of the lane during turns.

        :param control: (carla.VehicleControl) control to be modified
        :param enable_random_steer: (bool, optional) Flag to enable random steering
        """
        return managers.emergency_manager(self, control, reason)
    
    # ------------------ Setter Function ------------------ #

    def lane_change(self, direction, same_lane_time=0, other_lane_time=0, lane_change_time=2):
        """
        Changes the path so that the vehicle performs a lane change.
        Use 'direction' to specify either a 'left' or 'right' lane change,
        and the other 3 fine tune the maneuver
        """
        speed = self._vehicle.get_velocity().length()
        path : list = agents.tools.generate_lane_change_path(
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
    
    #@override 
    def set_target_speed(self, speed):
        """
        Changes the target speed of the agent
            :param speed (float): target speed in Km/h
        """
        if self.config.speed.follow_speed_limits:
            print("WARNING: The max speed is currently set to follow the speed limits. "
                  "Use 'follow_speed_limits' to deactivate this")
        self.config.speed.target_speed = speed # shared with planner

    def follow_speed_limits(self, value:bool=True):
        """
        If active, the agent will dynamically change the target speed according to the speed limits
            :param value: (bool) whether to activate this behavior
        """
        self.config.speed.follow_speed_limits = value

    def ignore_traffic_lights(self, active=True):
        """(De)activates the checks for traffic lights"""
        self.config.obstacles.ignore_traffic_lights = active

    def ignore_stop_signs(self, active=True):
        """(De)activates the checks for stop signs"""
        self.config.obstacles.ignore_stop_signs = active

    def ignore_vehicles(self, active=True):
        """(De)activates the checks for stop signs"""
        self.config.obstacles.ignore_vehicles = active

    # ------------------ Overwritten functions ------------------ #

    #@override
    def _tailgating(self, waypoint, vehicle_list):
        raise NotImplementedError("Tailgating has been implemented as a rule")

    #@override
    def emergency_stop(self):
        raise NotImplementedError("This function was overwritten use ´add_emergency_stop´ instead")

    #@override
    def _generate_lane_change_path(*args, **kwargs):
        raise NotImplementedError("This function was overwritten use `agents.tools.generate_lane_change_path´ instead")

    # ------------------------------------ #
    # As reference Parent Functions 
    # ------------------------------------ #
    #def get_local_planner(self):
    #def get_global_planner(self):

    #def done(self): # from base class self._local_planner.done()

   #def set_destination(self, end_location, start_location=None):
        """
        This method creates a list of waypoints between a starting and ending location,
        based on the route returned by the global router, and adds it to the local planner.
        If no starting location is passed, the vehicle local planner's target location is chosen,
        which corresponds (by default), to a location about 5 meters in front of the vehicle.

            :param end_location (carla.Location): final location of the route
            :param start_location (carla.Location): starting location of the route
        """

    #def set_global_plan(self, plan, stop_waypoint_creation=True, clean_queue=True):
        """
        Adds a specific plan to the agent.

            :param plan: list of [carla.Waypoint, RoadOption] representing the route to be followed
            :param stop_waypoint_creation: stops the automatic random creation of waypoints
            :param clean_queue: resets the current agent's plan
        """

    #def trace_route(self, start_waypoint, end_waypoint):
        """
        Calculates the shortest route between a starting and ending waypoint.

            :param start_waypoint (carla.Waypoint): initial waypoint
            :param end_waypoint (carla.Waypoint): final waypoint
        """
    

