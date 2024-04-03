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
import random
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple, Union, TYPE_CHECKING, cast as assure_type
import weakref

import carla
import omegaconf
from omegaconf import DictConfig, OmegaConf

from data_gathering.car_detection_matrix.run_matrix import AsyncDataMatrix, DataMatrix
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.behavior_agent import BehaviorAgent

import agents.tools
from agents.tools.lunatic_agent_tools import AgentDoneException, UpdatedPathException
from agents.tools.lunatic_agent_tools import ContinueLoopException
from agents.tools.misc import (TrafficLightDetectionResult, get_speed, ObstacleDetectionResult, is_within_distance,
                               compute_distance)
import agents.tools.lunatic_agent_tools
from agents.tools.lunatic_agent_tools import generate_lane_change_path, result_to_context
from agents.tools.logging import logger

from agents import substep_managers
from agents.dynamic_planning.dynamic_local_planner import DynamicLocalPlanner, DynamicLocalPlannerWithRss, RoadOption

from classes.constants import Phase, Hazard
from classes.rss_sensor import AD_RSS_AVAILABLE
from classes.rule import Context, Rule
from agents.tools.config_creation import AgentConfig, LiveInfo, LunaticAgentSettings

from classes.worldmodel import WorldModel, CarlaDataProvider
from classes.keyboard_controls import RSSKeyboardControl

if TYPE_CHECKING:
    from typing import Literal # for Python 3.8
    import pygame

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
    _base_settings : "ClassVar[type[AgentConfig]]" = LunaticAgentSettings
    
    rules : ClassVar[Dict[Phase, List[Rule]]] = {k : [] for k in Phase.get_phases()}
    """
    The rules of the this agent class. When initialized the rules of the class are copied.
    """
    
    _world_model : WorldModel = None # TODO: maybe as weakref
    ctx : "Context"
    
    # todo: rename in the future
    
    @classmethod
    def create_world_and_agent(cls, vehicle : carla.Vehicle, sim_world : carla.World, args, settings_archtype: "Optional[type[AgentConfig]]"=None, config:LunaticAgentSettings=None, overwrites: Dict[str, Any]={}, map_inst : carla.Map=None, grp_inst:GlobalRoutePlanner=None):
        
        if config is None:
            if settings_archtype is not None and not isinstance(settings_archtype, type):
                logger.debug("Assuming correct config.")
                config = settings_archtype
            elif settings_archtype is not None:
                logger.debug("Creating config from settings_archtype")
                behavior = settings_archtype(overwrites)
                config = behavior.make_config()
            else:
                logger.debug("Using %s._base_settings %s to create config.", cls.__name__, cls._base_settings)
                config = cls._base_settings.make_config()
        else:
            logger.debug("A config was passed, using it as is.")
        
        #world_model = WorldModel(config, args, carla_world=sim_world, player=vehicle, map_inst=map_inst)
        world_model = WorldModel(config, args=args, carla_world=sim_world, player=vehicle, map_inst=map_inst) # TEST: without args
        config.planner.dt = world_model.world_settings.fixed_delta_seconds or 1/world_model._args.fps
        
        agent = cls(config, world_model, grp_inst=grp_inst)
        return agent, world_model, agent.get_global_planner()

    def __init__(self, behavior: Union[str, LunaticAgentSettings], world_model: Optional[WorldModel]=None, *, vehicle: carla.Vehicle=None, map_inst : carla.Map=None, grp_inst:GlobalRoutePlanner=None, overwrite_options: dict = {}):
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
        if world_model is None and vehicle is None:
            raise ValueError("Must pass vehicle when not providing the world.")
        
        opt_dict : LunaticAgentSettings
        if behavior is None and world_model and world_model._config is not None:
            logger.debug("Using world model config")
            opt_dict = world_model._config
        elif behavior is None:
            raise ValueError("Must pass a valid config as behavior or a world model with a set config.")
        elif isinstance(behavior, str): # Assuming Path
            logger.debug("Creating config from yaml file")
            opt_dict : LunaticAgentSettings = LunaticAgentSettings.from_yaml(behavior)
        elif isinstance(behavior, AgentConfig):
            logger.info("Config is a dataclass / AgentConfig")
            opt_dict  = assure_type(behavior.__class__, behavior.make_config())  # base options from templates
            opt_dict.update(overwrite_options) # Note uses DictConfig.update
        elif isinstance(behavior, DictConfig):
            logger.info("Config is a DictConfig")
            opt_dict : LunaticAgentSettings = behavior
            for k, v in overwrite_options.items():
                OmegaConf.update(opt_dict, k, v)
        elif not overwrite_options:
            logger.warning("Warning: Settings are not a supported Config class")
            opt_dict = behavior  # assume the user passed something appropriate
        else:
            logger.warning("Warning: Settings are not a supported Config class. Trying to apply overwrite options.")
            behavior.update(overwrite_options) 
            opt_dict = behavior  # assume the user passed something appropriate
        self._behavior = behavior
        self.config = opt_dict # NOTE: This is the attribute we should use to access all information.
        
        logger.info("\n\nAgent config is %s", OmegaConf.to_yaml(self.config))
        
        if world_model is None:
            world_model = WorldModel(self.config, player=vehicle, map_inst=map_inst)
            self.config.planner.dt = world_model.world_settings.fixed_delta_seconds or 1/world_model._args.fps
        
        self._vehicle : carla.Vehicle = world_model.player
        try:
            CarlaDataProvider.register_actor(self._vehicle) # assure that the vehicle is registered
        except KeyError as e:
            logger.info("Ignoring error of already registered actor: %s", e)
        self._world_model : WorldModel = world_model
        self._world : carla.World = world_model.world
        if map_inst:
            if world_model.map and map_inst != world_model.map:
                raise ValueError("Passed Map instance does not match the map instance of the world model.") # TEMP: Turn into warning
            if isinstance(map_inst, carla.Map):
                self._map = map_inst
            else:
                print("Warning: Ignoring the given map as it is not a 'carla.Map'")
                self._map = self._world.get_map()
                world_model.map = self._map
        elif world_model.map is None:
            self._map = self._world.get_map()
            world_model.map = self._map
        else:
            self._map = world_model.map
        
        self.current_phase : Phase = Phase.NONE # current phase of the agent inside the loop
        self.ctx = None

        self.live_info : LiveInfo = self.config.live_info

        #config.speed.min_speed = 5
        self.config.speed.min_speed
        #config.planner.sampling_resolution = 4.5  # NOTE also set in behaviors

        # Original Setup ---------------------------------------------------------
        
        self._last_traffic_light : carla.TrafficLight = None  # Current red traffic light

        # TODO: No more hardcoded defaults / set them from opt_dict which must have all parameters; check which are parameters and which are set by other functions (e.g. _look_ahead_steps)

        # Parameters from BehaviorAgent ------------------------------------------
        # todo: check redefinitions

        self._look_ahead_steps = 0  # updated in _update_information used for local_planner.get_incoming_waypoint_and_direction

        # Initialize the planners
        self._local_planner = DynamicLocalPlannerWithRss(self._vehicle, opt_dict=opt_dict, map_inst=world_model.map, world=self._world if self._world else "MISSING", rss_sensor=world_model.rss_sensor)
        if grp_inst:
            self._global_planner = grp_inst
        else:
            self._global_planner = GlobalRoutePlanner(world_model.map, self.config.planner.sampling_resolution)

        # Get the static elements of the scene
        # TODO: This could be done globally and not for each instance :/
        self._lights_list : List[carla.TrafficLight] = self._world.get_actors().filter("*traffic_light*")
        self._lights_map : Dict[int, carla.Waypoint] = {}  # Dictionary mapping a traffic light to a wp corresponding to its trigger volume location

        # Vehicle Lights
        self._lights = carla.VehicleLightState.NONE

        # Collision Sensor # TODO: duplicated in WorldModel, maybe can be shared.
        self._collision_sensor : carla.Sensor = None
        self._set_collision_sensor()

        #Rule Framework
        self.rules = deepcopy(self.__class__.rules) # Copies the ClassVar to the instance
        
        # Data Matrix
        if self.config.data_matrix.enabled:
            if self.config.data_matrix.sync and self._world_model.world_settings.synchronous_mode:
                self._road_matrix_updater = DataMatrix(self._vehicle, self._world_model.world, self._world_model.map)
            else:
                self._road_matrix_updater = AsyncDataMatrix(self._vehicle, self._world_model.world, self._world_model.map)
            self._road_matrix_updater.start()  # TODO maybe find a nicer way
        else:
            self._road_matrix_updater = None
        self._road_matrix_counter = 0 # TODO: Todo make this nicer and maybe get ticks from world.
        
        # Vehicle information
        #self.live_info.current_speed = 0
        #self.live_info.current_speed_limit = self._vehicle.get_speed_limit()
        #self.live_info.velocity_vector = self._vehicle.get_velocity()
        #self.live_info.executed_direction = RoadOption.VOID
        #self.live_info.incoming_direction = self._local_planner.target_road_option
        
    def set_vehicle(self, vehicle:carla.Vehicle):
        self._vehicle = vehicle
        # Data Matrix
        if self.config.data_matrix.enabled:
            if self._world_model.world_settings.synchronous_mode:
                self._road_matrix_updater = DataMatrix(self._vehicle, self._world_model.world, self._world_model.map)
            else:
                self._road_matrix_updater = AsyncDataMatrix(self._vehicle, self._world_model.world, self._world_model.map)
        else:
            self._road_matrix_updater = None
        self._local_planner = DynamicLocalPlannerWithRss(self._vehicle, opt_dict=self.config, map_inst=self._world_model.map, world=self._world_model.world, rss_sensor=self._world_model.rss_sensor)

    @property
    def road_matrix(self):
        if self._road_matrix_updater:
            return self._road_matrix_updater.getMatrix()
    
    def render_road_matrix(self, display:"pygame.Surface", options:Dict[str, Any]={}):
        if self._road_matrix_updater:
            self._road_matrix_updater.render(display, **options)

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
        if self._road_matrix_updater:
            self._road_matrix_updater.stop()
        if self._collision_sensor:
            self._collision_sensor.destroy()
            self._collision_sensor = None
            
    #@property
    #def ctx(self) -> Union[Context, None]:
    #    print("Getting Context", self._ctx())
    #    return self._ctx() # might be None
    
    def make_context(self, last_context : Union[Context, None], **kwargs):
        if last_context is not None:
            del last_context.last_context
        ctx = Context(agent=self, last_context=last_context, **kwargs)
        #self._ctx = weakref.ref(ctx)
        self.ctx = ctx
        return ctx

    # ------------------ Information functions ------------------ #

    def _update_information(self, exact_waypoint=True, second_pass=False):
        """
        This method updates the information regarding the ego
        vehicle based on the surrounding world.
        
        second_pass = True will skip some calculations, 
        especially useful if a second call to _update_information is necessary in the same tick.
        
        Assumes: second_pass == True => agent.done() == False
        """
        # --------------------------------------------------------------------------
        # Information that is CONSTANT DURING THIS TICK and INDEPENDENT OF THE ROUTE
        # --------------------------------------------------------------------------
        if not second_pass:
            # For heavy and tick-constant information
            self.live_info.current_speed_limit = self._vehicle.get_speed_limit()
            self.live_info.velocity_vector = self._vehicle.get_velocity()
            if self.live_info.use_srunner_data_provider:
                # Own properties
                # NOTE: That transform.location and location are similar but not identical!
                # NOTE: get_velocity does not take the z axis into account.
                self.live_info.current_speed = CarlaDataProvider.get_velocity(self._vehicle) * 3.6
                self.live_info.current_transform = CarlaDataProvider.get_transform(self._vehicle)
                self.live_info.current_location = CarlaDataProvider.get_location(self._vehicle)
            else:
                # Own properties
                self.live_info.current_speed = get_speed(self._vehicle)
                self.live_info.current_transform = self._vehicle.get_transform()
                self.live_info.current_location = self.live_info.current_transform.location
                
                # TODO: Filter this to only contain relevant vehicles # i.e. certain radius and or lanes around us. Avoid this slow call.
                # TODO: Use CarlaDataProvider
                _actors = self._world.get_actors()
                self.vehicles_nearby : List[carla.Vehicle] = _actors.filter("*vehicle*")
                self.walkers_nearby : List[carla.Walker] = _actors.filter("*walker.pedestrian*")
            
            # Data Matrix
            if self._road_matrix_updater and self._road_matrix_updater.sync:
                self._road_matrix_counter += 1
                if (self._road_matrix_counter % self.config.data_matrix.sync_interval) == 0:
                    logger.debug("Updating Road Matrix")
                    # TODO: Still prevent async mode from using too much resources and slowing fps down too much.
                    self._road_matrix_updater.update() # NOTE: Does nothing if in async mode. self.road_matrix is updated by another thread.
                else:
                    logger.debug("Not updating Road Matrix")
            
            self._look_ahead_steps = int((self.live_info.current_speed_limit) / 10) # TODO: Maybe make this an interpolation
            self.live_info.executed_direction = assure_type(RoadOption, self._local_planner.target_road_option) # NOTE: This is the direction used by the planner in the *last* step.
        
        assert self.live_info.executed_direction == self._local_planner.target_road_option, "Executed direction should not change."
        
        # -------------------------------------------------------------------
        # Information that NEEDS TO BE UPDATED AFTER a plan / ROUTE CHANGE.
        # -------------------------------------------------------------------
        if not self.done():
            # NOTE: This should be called after 
            self.live_info.incoming_waypoint, self.live_info.incoming_direction = self._local_planner.get_incoming_waypoint_and_direction(
                steps=self._look_ahead_steps)
            if exact_waypoint and not second_pass:
                self._current_waypoint : carla.Waypoint = self._map.get_waypoint(self.live_info.current_location)
            elif not exact_waypoint:
                self._current_waypoint : carla.Waypoint = self.live_info.incoming_waypoint
            # note: else: exact waypoint from first pass
        else:
            assert second_pass == False, "In the second pass the agent should have replanned and agent.done() should be False"
            # Assumes second_pass is False
            if exact_waypoint:
                self._current_waypoint : carla.Waypoint = self._map.get_waypoint(self.live_info.current_location)
            else:
                self._current_waypoint : carla.Waypoint = self.live_info.incoming_waypoint # NOTE: this is from the last tick, as not retrieved from planner unlike above
            # Queue is empty
            self.live_info.incoming_waypoint = None
            self.live_info.incoming_direction  = RoadOption.VOID
        
        # Information that requires updated waypoint and route information:
        self.live_info.is_taking_turn = self.is_taking_turn()
        self.live_info.is_changing_lane = self.is_changing_lane()
            
        #logger.debug(f"Incoming Direction: {str(self.live_info.incoming_direction):<20} - Second Pass: {second_pass}")

        # RSS
        # todo uncomment if agent is created after world model
        #self.rss_set_road_boundaries_mode() # in case this was adjusted during runtime. # TODO: maybe implement this update differently. As here it is called unnecessarily often.
    
    def is_taking_turn(self) -> bool:
        return self.live_info.incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)
    
    def is_changing_lane(self) -> bool:
        return self.live_info.incoming_direction in (RoadOption.CHANGELANELEFT, RoadOption.CHANGELANERIGHT)

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
        assert normal_next == Phase.USER_CONTROLLED or phase == normal_next or phase & Phase.EXCEPTIONS or phase & Phase.USER_CONTROLLED, f"Phase {phase} is not the next phase of {self.current_phase} or an exception phase. Expected {normal_next}"
        
        self.current_phase = phase # set next phase
        
        if control is not None:
            self.ctx.set_control(control)
        self.ctx.prior_result = prior_results
        rules_to_check = self.rules[phase]
        try:
            for rule in rules_to_check: # todo: maybe dict? grouped by phase?
                #todo check here for the phase instead of in the rule
                assert self.current_phase in rule.phases, f"Current phase {self.current_phase} not in Rule {rule.phases}" # TODO remove:
                rule(self.ctx)
        except omegaconf.ReadonlyConfigError:
            print("WARNING: A action likely tried to change `ctx.config` which is non-permanent. Use `ctx.agent.config.` instead.")
            raise
        return self.ctx

    def verify_settings(self, config : LunaticAgentSettings=None):
        if self._world_model.world_settings.synchronous_mode:
            # Assure that dt is set
            OmegaConf.select(config or self.config,
                "planner.dt",
                throw_on_missing=True
            )

    def run_step(self, debug=False, second_pass=False):
        if not second_pass:
            ctx = self.make_context(last_context=self.ctx)
        else:
            ctx = self.ctx
        ctx.second_pass = second_pass
        try:
            # ----------------------------
            # Phase 0 - Update Information
            # ----------------------------
            self.execute_phase(Phase.UPDATE_INFORMATION | Phase.BEGIN, prior_results=None)
            self._update_information(second_pass=second_pass)
            self.execute_phase(Phase.UPDATE_INFORMATION | Phase.END, prior_results=None)

            # ----------------------------
            # Phase 1 - Plan Path
            # ----------------------------

            # TODO: What TODO if the last phase was COLLISION, EMERGENCY
            # Some information to PLAN_PATH should reflect this

            # TODO: add option to diverge from existing path here, or plan a new path
            # NOTE: Currently done in the local planner and behavior functions
            try:
                self.execute_phase(Phase.PLAN_PATH | Phase.BEGIN, prior_results=None)
                # User defined action
                # TODO: when going around corners / junctions and the distance between waypoints is too big,
                # We should replan and and make a more fine grained plan, to stay on the road.
                self.execute_phase(Phase.PLAN_PATH | Phase.END, prior_results=None)
            except UpdatedPathException as e:
                if second_pass:
                    raise ValueError("UpdatedPathException was raised in the second pass. This should not happen.") from e
                return self.run_step(debug=debug, second_pass=True) # TODO: # CRITICAL: For child classes like the leaderboard agent this calls the higher level run_step.
            
            if self.done():
                # NOTE: Might be in NONE phase here.
                self.execute_phase(Phase.DONE| Phase.BEGIN, prior_results=None)
                if self.done():
                    # No Rule set a net destination
                    print("The target has been reached, stopping the simulation")
                    self.execute_phase(Phase.TERMINATING | Phase.BEGIN, prior_results=None)
                    raise AgentDoneException
                self.execute_phase(Phase.DONE | Phase.END, prior_results=None)
                return self.run_step(debug=debug, second_pass=True) # TODO: # CRITICAL: For child classes like the leaderboard agent this calls the higher level run_step.
            
            # ----------------------------
            # Phase NONE - Before Running step
            # ----------------------------
            planned_control = self._inner_step(debug=debug)  # debug=True draws waypoints
            # ----------------------------
            # No known Phase multiple exit points
            # ----------------------------
            
            # ----------------------------
            # Phase RSS - Check RSS
            # ----------------------------
            planned_control.manual_gear_shift = False # TODO: turn into a rule
            
            ctx = self.execute_phase(Phase.RSS_EVALUATION | Phase.BEGIN, prior_results=None, control=planned_control)
            if AD_RSS_AVAILABLE and self.config.rss.enabled:
                rss_updated_controls = self._world_model.rss_check_control(ctx.control)
            else:
                rss_updated_controls = None
            ctx = self.execute_phase(Phase.RSS_EVALUATION | Phase.END, prior_results=rss_updated_controls) # NOTE: rss_updated_controls could be None
            
            if ctx.control is not planned_control:
                logger.debug("RSS updated control accepted.")
            # ----------------------------
            # Phase Manual User Controls
            # TODO: Create a flag that allows this or not
            # ----------------------------
                
        except ContinueLoopException:
            logger.info("Continuing Loop")
        return ctx.control

    @result_to_context("control")
    def _inner_step(self, debug=False):
        """
        This is our main entry point that runs every tick.  
        """
        self.debug = debug

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
        # NOTE: is_taking_turn <- incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)
        if self.live_info.incoming_waypoint.is_junction and self.is_taking_turn():

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
    
    def apply_control(self, control: Optional[carla.VehicleControl]=None):
        # Set automatic control-related vehicle lights
        if control is None:
            control = self.ctx.control
        self.update_lights(control)
        self._vehicle.apply_control(control)

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
        control = self.add_emergency_stop(control, reasons=hazard_detected)
        # TODO: Let a rule decide if the loop should end
        self.execute_phase(Phase.EMERGENCY | Phase.END, control=control, prior_results=hazard_detected)
        # self.ctx.end_loop = True # TODO: ³ IDEA: work in
        #print("Emergency controls", control)
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
            < self.config.distance.emergency_braking_distance)):
            print("Detected walker", detection_result.obstacle)
            return True, detection_result
        # TODO detected but not stopping -> ADD avoidance behavior
        return False, detection_result
        
    def car_following_behavior(self, vehicle_detected:bool, vehicle:carla.Actor, distance:float) -> carla.VehicleControl:
        exact_distance = distance - max(vehicle.bounding_box.extent.y, vehicle.bounding_box.extent.x) - max(
            self._vehicle.bounding_box.extent.y, self._vehicle.bounding_box.extent.x)

        if exact_distance < self.config.distance.emergency_braking_distance:
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
    def add_emergency_stop(self, control, reasons:"set[str]"=None) -> carla.VehicleControl:
        """
        Modifies the control values to perform an emergency stop.
        The steering remains unchanged to avoid going out of the lane during turns.

        :param control: (carla.VehicleControl) control to be modified
        :param enable_random_steer: (bool, optional) Flag to enable random steering
        """
        return substep_managers.emergency_manager(self, control, reasons)
    
    def lane_change(self, direction: "Literal['left'] | Literal['right']", same_lane_time=0, other_lane_time=0, lane_change_time=2):
        """
        Changes the path so that the vehicle performs a lane change.
        Use 'direction' to specify either a 'left' or 'right' lane change,
        and the other 3 fine tune the maneuver
        """
        speed = self._vehicle.get_velocity().length()
        path : list = generate_lane_change_path(
            self._current_waypoint, # NOTE: Assuming exact_waypoint
            direction,
            same_lane_time * speed, # get direction in meters t*V
            other_lane_time * speed,
            lane_change_time * speed,
            check=False,        # TODO: Explanation of this parameter? Make use of it and & how? Could mean that it is checked if there is a left lane
            lane_changes=1,     # changes only one lane
            step_distance= self.config.planner.sampling_resolution
        )
        if not path:
            print("WARNING: Ignoring the lane change as no path was found")

        super(LunaticAgent, self).set_global_plan(path)
        # TODO: # CRITICAL: Keep old global plan if it is some end goal.
        
    # ------------------ Other Function ------------------ #
    
    def update_lights(self, vehicle_control : carla.VehicleControl):
        current_lights = self._lights
        if vehicle_control.brake:
            current_lights |= carla.VehicleLightState.Brake
        else:  # Remove the Brake flag
            current_lights &= carla.VehicleLightState.All ^ carla.VehicleLightState.Brake
        if vehicle_control.reverse:
            current_lights |= carla.VehicleLightState.Reverse
        else:  # Remove the Reverse flag
            current_lights &= carla.VehicleLightState.All ^ carla.VehicleLightState.Reverse
        if current_lights != self._lights:  # Change the light state only if necessary
            self._lights = current_lights
            self._vehicle.set_light_state(carla.VehicleLightState(self._lights))

    # ------------------ Getter Function ------------------ #
    
    def get_control(self) -> Union[None, carla.VehicleControl]:
        """
        Returns the currently planned control of the agent.
        
        If retrieved before the local planner has been run, it will return None.
        """
        return self.ctx.control

    # ------------------ Setter Function ------------------ #
    
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
    

