# Copyright (c) # Copyright (c) 2018-2020 CVC.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

# NOTE: This file currently contains code from the three agents that were implemented in the original CARLA repo. so
# no added customization yet, also not yet all useful code.

""" This module implements an agent that roams around a track following random
waypoints and avoiding other vehicles. The agent also responds to traffic lights,
traffic signs, and has different possible configurations. """

from __future__ import annotations

from copy import deepcopy
from functools import wraps
import random
from typing import ClassVar, Dict, List, Optional, Set, Tuple, Union, TYPE_CHECKING, cast as assure_type
import weakref

from omegaconf import DictConfig

import carla

from DataGathering.run_matrix import AsyncDataMatrix, DataMatrix
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.behavior_agent import BehaviorAgent

import agents.tools
from agents.tools.misc import (TrafficLightDetectionResult, get_speed, ObstacleDetectionResult, is_within_distance,
                               compute_distance)
import agents.tools.lunatic_agent_tools
from agents.tools.lunatic_agent_tools import generate_lane_change_path

from agents import substep_managers
from agents.dynamic_planning.dynamic_local_planner import DynamicLocalPlanner, DynamicLocalPlannerWithRss, RoadOption

from classes.constants import Phase, Hazard
from classes.rule import Context, Rule
from conf.default_options.original_behavior import BasicAgentSettings
from conf.lunatic_behavior_settings import LunaticBehaviorSettings

if TYPE_CHECKING:
    from classes.worldmodel import WorldModel

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

    # using a ClassVar which allows to define preset rules for a child class
    # NOTE: Use deepcopy to avoid shared state between instances
    rules : ClassVar[Dict[Phase, List[Rule]]] = {k : [] for k in Phase.get_phases()}
    _world_model : WorldModel = None
    _ctx : weakref.ReferenceType["Context"] = None
    
    # todo: rename in the future

    def __init__(self, vehicle : carla.Vehicle, world : carla.World, behavior : LunaticBehaviorSettings, map_inst : carla.Map=None, grp_inst:GlobalRoutePlanner=None, overwrite_options: dict = {}):
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
        self._vehicle : carla.Vehicle = vehicle
        self._world : carla.World = world
        if map_inst:
            if isinstance(map_inst, carla.Map):
                self._map = map_inst
            else:
                print("Warning: Ignoring the given map as it is not a 'carla.Map'")
                self._map = self._world.get_map()
        else:
            self._map = self._world.get_map()

        opt_dict = self._behavior.get_options()  # base options from templates
        opt_dict.update(overwrite_options)  # update by custom options

        self.config = opt_dict # NOTE: This is the attribute we should use to access all information.
        
        self.current_phase : Phase = Phase.NONE # current phase of the agent inside the loop

        self.live_info : DictConfig = self.config.live_info

        # Vehicle information
        self.live_info.speed = 0
        self.live_info.speed_limit = 0
        self.live_info.direction = None
        #config.speed.min_speed = 5
        self.config.speed.min_speed
        #config.unknown.sampling_resolution = 4.5  # NOTE also set in behaviors

        # Original Setup ---------------------------------------------------------
        
        self._last_traffic_light = None  # Current red traffic light

        # TODO: No more hardcoded defaults / set them from opt_dict which must have all parameters; check which are parameters and which are set by other functions (e.g. _look_ahead_steps)

        # Parameters from BehaviorAgent ------------------------------------------
        # todo: check redefinitions

        self._incoming_waypoint : carla.Waypoint = None
        self._look_ahead_steps = 0  # updated in _update_information used for local_planner.get_incoming_waypoint_and_direction
        self._previous_direction : Optional[RoadOption] = None
        self._incoming_direction : RoadOption = None

        # Initialize the planners
        self._local_planner = DynamicLocalPlannerWithRss(self._vehicle, opt_dict=opt_dict, map_inst=self._map, world=self._world if self._world else "MISSING")
        if grp_inst:
            if isinstance(grp_inst, GlobalRoutePlanner):
                self._global_planner = grp_inst
            else:
                print("Warning: Ignoring the given map as it is not a 'carla.Map'")
                self._global_planner = GlobalRoutePlanner(self._map, self.config.unknown.sampling_resolution)
        else:
            self._global_planner = GlobalRoutePlanner(self._map, self.config.unknown.sampling_resolution)

        # Get the static elements of the scene
        # TODO: This could be done globally and not for each instance :/
        self._lights_list : List[carla.TrafficLight] = self._world.get_actors().filter("*traffic_light*")
        self._lights_map : Dict[int, carla.Waypoint] = {}  # Dictionary mapping a traffic light to a wp corresponding to its trigger volume location

        # From ConstantVelocityAgent ----------------------------------------------
        self._collision_sensor : carla.Sensor = None
        self._set_collision_sensor()

        #Rule Framework
        self.rules = deepcopy(self.__class__.rules) # Copies the ClassVar to the instance
        
        # Data Matrix
        world_settings = self._world_model.world_settings if self._world_model is not None else self._world.get_settings() # TODO: change when creation order can be reversed.
        if world_settings.synchronous_mode:
            self._road_matrix_updater = DataMatrix(self._vehicle, world, map_inst)
        else:
            self._road_matrix_updater = AsyncDataMatrix(self._vehicle, world, map_inst)
            
    @property
    def road_matrix(self):
        return self._road_matrix_updater.getMatrix()

    def _set_collision_sensor(self):
        # see: https://carla.readthedocs.io/en/latest/ref_sensors/#collision-detector
        # and https://carla.readthedocs.io/en/latest/python_api/#carla.Sensor.listen
        blueprint = self._world.get_blueprint_library().find('sensor.other.collision')
        self._collision_sensor : carla.Sensor = assure_type(carla.Sensor, 
                                                     self._world.spawn_actor(blueprint, carla.Transform(), attach_to=self._vehicle))
        def collision_callback(event : carla.SensorData):
            self._collision_event(event)
        self._collision_sensor.listen(self._collision_event)

    def destroy_sensor(self):
        if self._collision_sensor:
            self._collision_sensor.destroy()
            self._collision_sensor = None
            
    @property
    def ctx(self) -> Union[Context, None]:
        return self._ctx() # might be None
    
    def make_context(self, last_context : Union[Context, None], **kwargs):
        if last_context is not None:
            del last_context.last_context
        ctx = Context(agent=self, last_context=last_context, **kwargs)
        self._ctx = weakref.ref(ctx)
        return ctx

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
        
        self.live_info.direction : RoadOption = self._local_planner.target_road_option # type: ignore
        if self.live_info.direction is None:
            self.live_info.direction = RoadOption.LANEFOLLOW

        self._look_ahead_steps = int((self.live_info.speed_limit) / 10)

        self._previous_direction = self._incoming_direction
        self._incoming_waypoint, self._incoming_direction = self._local_planner.get_incoming_waypoint_and_direction(
            steps=self._look_ahead_steps)
        if self._incoming_direction is None:
            self._incoming_direction = RoadOption.LANEFOLLOW

        self.location = ego_vehicle_loc = self._vehicle.get_location()
        if exact_waypoint:
            self._current_waypoint : carla.Waypoint = self._map.get_waypoint(ego_vehicle_loc)
        else:
            self._current_waypoint : carla.Waypoint = self._incoming_waypoint

        # TODO: Filter this to only contain relevant vehicles # i.e. certain radius and or lanes around us. Avoid this slow call.
        self.vehicles_nearby : List[carla.Vehicle] = self._world.get_actors().filter("*vehicle*")
        self.walkers_nearby : List[carla.Walker] = self._world.get_actors().filter("*walker.pedestrian*")
        
        # RSS
        # todo uncomment if agent is created after world model
        #self.rss_set_road_boundaries_mode() # in case this was adjusted during runtime. # TODO: maybe implement this update differently. As here it is called unnecessarily often.
        
        # Data Matrix
        self._road_matrix_updater.update() # NOTE: Does nothing if in async mode. self.road_matrix is updated in the background.
        

    def is_taking_turn(self) -> bool:
        return self._incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)

    # ------------------ Step & Loop Logic ------------------ #


    def add_rule(self, rule : Rule, position=-1):
        for p in rule.phases:
            self.rules[p].append(rule)
            self.rules[p].sort(key=lambda r: r.priority, reverse=True)
            
    def add_rules(self, rules : List[Rule]):
        """Add a list of rules and sort the agents rules by priority."""
        for rule in rules:
            for phase in rule.phases:
                self.rules[phase].append(rule)
        for phase in Phase.get_phases():
            self.rules[phase].sort(key=lambda r: r.priority, reverse=True)
        
    def execute_phase(self, phase : Phase, *, prior_results, control:carla.VehicleControl=None) -> Context:
        """
        Sets the current phase of the agent and executes all rules that are associated with it.
        """
        normal_next = self.current_phase.next_phase() # sanity checking if everything is correct
        assert phase == normal_next or phase & Phase.EXCEPTIONS, f"Phase {phase} is not the next phase of {self.current_phase} or an exception phase. Expected {normal_next}"
        
        self.current_phase = phase # set next phase
        
        if control is not None:
            self.ctx.set_control(control)
        self.ctx.prior_result = prior_results
        rules_to_check = self.rules[phase]
        for rule in rules_to_check: # todo: maybe dict? grouped by phase?
            #todo check here for the phase instead of in the rule
            assert self.current_phase in rule.phases, f"Current phase {self.current_phase} not in Rule {rule.phases}" # TODO remove:
            rule(self.ctx)
        return self.ctx
    
    @staticmethod
    def result_to_context(key):
        """
        Decorator to insert the result into the context object
        """
        def decorator(func):
            @wraps(func)
            def wrapper(self : LunaticAgent, *args, **kwargs):
                result = func(self, *args, **kwargs)
                setattr(self.ctx, key, result)
                return result
            return wrapper
            
        return decorator

    @result_to_context("control")
    def run_step(self, debug=False):
        """
        This is our main entry point that runs every tick.  
        """
        self.debug = debug
        # ----------------------------
        # Phase 0 - Update Information
        # ----------------------------
        self.execute_phase(Phase.UPDATE_INFORMATION | Phase.BEGIN, prior_results=None)
        self._update_information()
        self.execute_phase(Phase.UPDATE_INFORMATION | Phase.END, prior_results=None)

        # ----------------------------
        # Phase 1 - Plan Path
        # ----------------------------

        # TODO: What TODO if the last phase was COLLISION, EMERGENCY
        # Some information to PLAN_PATH should reflect this

        # TODO: add option to diverge from existing path here, or plan a new path
        # NOTE: Currently done in the local planner and behavior functions
        self.execute_phase(Phase.PLAN_PATH | Phase.BEGIN, prior_results=None)
        self.execute_phase(Phase.PLAN_PATH | Phase.END, prior_results=None)

        # ----------------------------
        # Phase 2 - Detection of Pedestrians and Traffic Lights
        # ----------------------------

        # Detect hazards
        # phases are executed in detect_hazard
        Phase.DETECT_TRAFFIC_LIGHTS | Phase.BEGIN # phases executed inside
        pedestrians_or_traffic_light = self.detect_hazard()
        Phase.DETECT_PEDESTRIANS | Phase.END

        # Pedestrian avoidance behaviors
        # currently doing either emergency (detect_hazard) stop or nothing 
        if pedestrians_or_traffic_light:

            # ----------------------------
            # Phase Hazard Detected (traffic light or pedestrian)
            # TODO: needs overhaul 
            # ----------------------------

            print("Hazard detected", pedestrians_or_traffic_light)
            (control, end_loop) = self.react_to_hazard(control=None, hazard_detected=pedestrians_or_traffic_light)
            # Other behaviors based on hazard detection
            if end_loop: # Likely emergency stop
                # TODO: overhaul -> this might not be the best place to do this
                #TODO HIGH: This is doubled in react_to_hazard!
                self.execute_phase(Phase.EMERGENCY | Phase.END, prior_results=pedestrians_or_traffic_light, control=control)
                return control
    
        # ----------------------------
        # Phase 3 - Detection of Cars
        # ----------------------------
            
        self.execute_phase(Phase.DETECT_CARS | Phase.BEGIN, prior_results=None) # TODO: Maybe add some prio result
        detection_result :ObstacleDetectionResult = substep_managers.collision_detection_manager(self, self._current_waypoint)
        # TODO: add a way to let the execution overwrite
        if detection_result.obstacle_was_found:

            # ----------------------------
            # Phase 2.A - React to cars in front
            # TODO: turn this into a rule.
            #    remove CAR_DETECTED -> pass detection_result to rules
            # TODO some way to circumvent returning control here, like above.
            # TODO: Needs refinement with the car_following_behavior
            # ----------------------------

            self.execute_phase(Phase.CAR_DETECTED | Phase.BEGIN, prior_results=detection_result)
            control = self.car_following_behavior(*detection_result) # NOTE: can currently go into EMEGENCY phase
            self.execute_phase(Phase.CAR_DETECTED | Phase.END, control=control, prior_results=detection_result)
            return control
        
        #TODO: maybe new phase instead of END or remove CAR_DETECTED and handle as rules (maybe better)
        self.execute_phase(Phase.DETECT_CARS | Phase.END, prior_results=None) # NOTE: avoiding tailgate here
        
        # Intersection behavior
        # NOTE: is_taking_turn == self._incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)
        if self._incoming_waypoint.is_junction and self.is_taking_turn():

            # ----------------------------
            # Phase Turning at Junction
            # ----------------------------

            self.execute_phase(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, prior_results=None)
            control = self._local_planner.run_step(debug=debug)
            self.execute_phase(Phase.TURNING_AT_JUNCTION | Phase.END, control=control, prior_results=None)
            return control

        # ----------------------------
        # Phase 4 - Plan Path normally
        # ----------------------------
        
        # Normal behavior
        self.execute_phase(Phase.TAKE_NORMAL_STEP | Phase.BEGIN, prior_results=None)
        control = self._local_planner.run_step(debug=debug)
        self.execute_phase(Phase.TAKE_NORMAL_STEP | Phase.END, prior_results=None, control=control)

        # Leave loop and apply controls outside 
        # DISCUSS: Should we apply the controls here?
        return control

    # ------------------ Hazard Detection & Reaction ------------------ #

    def detect_hazard(self) -> Set[str]:
        hazard_detected = set()
        # Red lights and stops behavior

        self.execute_phase(Phase.DETECT_TRAFFIC_LIGHTS | Phase.BEGIN, prior_results=None)
        tlight_detection_result = self.traffic_light_manager()
        if tlight_detection_result.traffic_light_was_found:
            hazard_detected.add(Hazard.TRAFFIC_LIGHT)             #TODO: Currently cannot give fine grained priority results
        self.execute_phase(Phase.DETECT_TRAFFIC_LIGHTS | Phase.END, prior_results=tlight_detection_result)

        # Pedestrian avoidance behaviors
        self.execute_phase(Phase.DETECT_PEDESTRIANS | Phase.BEGIN, prior_results=None)
        hazard, detection_result = self.pedestrian_avoidance_behavior(self._current_waypoint)
        if detection_result.obstacle_was_found:
            if hazard:   #TODO: Currently cannot give very fine grained priority results, i.e. slow down or stop
                hazard_detected.add(Hazard.PEDESTRIAN | Hazard.EMERGENCY)
            else:
                hazard_detected.add(Hazard.PEDESTRIAN | Hazard.WARNING)
        self.execute_phase(Phase.DETECT_PEDESTRIANS | Phase.END, prior_results=(hazard, detection_result))
        
        return hazard_detected
    
    def react_to_hazard(self, control, hazard_detected : set):
        # TODO: # CRITICAL: needs creative overhaul
        # Stop indicates if the loop shoul

        print("Hazard(s) detected: ", hazard_detected)
        end_loop = True
        
        if "pedestrian" in hazard_detected:
            pass # Maybe let rules handle this and remove
        if "traffic_light" in hazard_detected:
            pass

        # TODO: PRIORITY: let execute_phase handle end_loop
        self.execute_phase(Phase.EMERGENCY | Phase.BEGIN, prior_results=hazard_detected)
        control = self.add_emergency_stop(control)
        # TODO: Let a rule decide if the loop should end
        self.execute_phase(Phase.EMERGENCY | Phase.END, control=control, prior_results=hazard_detected)
        # self.ctx.end_loop = True # TODO: ³ IDEA: work in
        print("Emergency controls", control)
        return control, end_loop
    
    # ------------------ Behaviors ------------------ #
    # TODO: Section needs overhaul -> turn into rules

    def pedestrian_avoidance_behavior(self, ego_vehicle_wp : carla.Waypoint) -> Tuple[bool, ObstacleDetectionResult]:
        # TODO: # CRITICAL: This for some reasons also detects vehicles as pedestrians
        # note ego_vehicle_wp is the current waypoint self._current_waypoint
        detection_result = substep_managers.pedestrian_detection_manager(self, ego_vehicle_wp)
        if (detection_result.obstacle_was_found
            and (detection_result.distance - max(detection_result.obstacle.bounding_box.extent.y, 
                                                 detection_result.obstacle.bounding_box.extent.x)
                                           - max(self._vehicle.bounding_box.extent.y, 
                                                 self._vehicle.bounding_box.extent.x)
            < self.config.distance.braking_distance)):
            print("Detected walker", detection_result.obstacle)
            return True, detection_result
        # TODO detected but not stopping -> ADD avoidance behavior
        return False, detection_result
        
    def car_following_behavior(self, vehicle_detected:bool, vehicle:carla.Actor, distance:float) -> carla.VehicleControl:
        exact_distance = distance - max(vehicle.bounding_box.extent.y, vehicle.bounding_box.extent.x) - max(
            self._vehicle.bounding_box.extent.y, self._vehicle.bounding_box.extent.x)

        if exact_distance < self.config.distance.braking_distance:
            controls, end_loop = self.react_to_hazard(control=None, hazard_detected={Hazard.CAR})
        else:
            controls = self.car_following_manager(vehicle, exact_distance)
        return controls

    # ------------------ Managers for Behaviour ------------------ #

    
    def traffic_light_manager(self) -> TrafficLightDetectionResult:
        """
        This method is in charge of behaviors for red lights.
        """
        return substep_managers.traffic_light_manager(self, self._lights_list)
    
    def car_following_manager(self, vehicle, distance, debug=False) -> carla.VehicleControl:
        return substep_managers.car_following_manager(self, vehicle, distance, debug=debug)
    
    def _collision_event(self, event : carla.CollisionEvent):
        # https://carla.readthedocs.io/en/latest/python_api/#carla.CollisionEvent
        # e.g. setting ignore_vehicles to False, if it was True before.
        # do an emergency stop (in certain situations)
        NotImplemented  # TODO: Brainstorm and implement
        return substep_managers.collision_manager(self, event)

    # ----

    # TODO: see if max_distance is currently still necessary
    # TODO: move angles to config
    #@override
    def _vehicle_obstacle_detected(self, vehicle_list=None, max_distance=None, 
                                   up_angle_th=90, 
                                   low_angle_th=0,
                                   lane_offset=0) -> ObstacleDetectionResult:
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
        return agents.tools.lunatic_agent_tools.detect_vehicles(self, vehicle_list, max_distance, up_angle_th, low_angle_th, lane_offset)

    #@override
    # TODO: Port this to a rule that is used during emergencies.
    def add_emergency_stop(self, control, reason:str=None) -> carla.VehicleControl:
        """
        Modifies the control values to perform an emergency stop.
        The steering remains unchanged to avoid going out of the lane during turns.

        :param control: (carla.VehicleControl) control to be modified
        :param enable_random_steer: (bool, optional) Flag to enable random steering
        """
        return substep_managers.emergency_manager(self, control, reason)
    
    # ------------------ Setter Function ------------------ #

    def lane_change(self, direction, same_lane_time=0, other_lane_time=0, lane_change_time=2):
        """
        Changes the path so that the vehicle performs a lane change.
        Use 'direction' to specify either a 'left' or 'right' lane change,
        and the other 3 fine tune the maneuver
        """
        speed = self._vehicle.get_velocity().length()
        path : list = generate_lane_change_path(
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
    def set_target_speed(self, speed : float):
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
        
    def rss_set_road_boundaries_mode(self, road_boundaries_mode: Optional[Union[bool, carla.RssRoadBoundariesMode]]=None):
        if road_boundaries_mode is None:
            road_boundaries_mode : bool = self.config.rss.use_stay_on_road_feature
        self._world_model.rss_set_road_boundaries_mode(road_boundaries_mode)

    # ------------------ Overwritten functions ------------------ #

    # NOTE: the original pedestrian_avoid_manager is still usable
    def pedestrian_avoid_manager(self, waypoint):
        raise NotImplementedError("This function was replaced by ", substep_managers.pedestrian_detection_manager)

    #@override
    def collision_and_car_avoid_manager(self, waypoint):
        raise NotImplementedError("This function was split into collision_detection_manager and car_following_manager")
    
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
    

