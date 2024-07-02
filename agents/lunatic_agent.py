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

import sys
from copy import deepcopy
from typing import Any, ClassVar, Dict, Iterable, List, NoReturn, Optional, Set, Tuple, Union, TYPE_CHECKING, cast as assure_type

from agents.rules import rule_from_config

import carla
import omegaconf
from omegaconf import DictConfig, OmegaConf

from agents.tools.hints import ObstacleDetectionResult, TrafficLightDetectionResult
from classes.exceptions import *
from data_gathering.car_detection_matrix.run_matrix import AsyncDetectionMatrix, DetectionMatrix
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.behavior_agent import BehaviorAgent

import agents.tools
from agents.tools.lunatic_agent_tools import detect_vehicles, must_clear_hazard, phase_callback
from agents.tools.misc import (is_within_distance,
                               compute_distance, lanes_have_same_direction)
import agents.tools.lunatic_agent_tools
from agents.tools.lunatic_agent_tools import generate_lane_change_path, result_to_context
from agents.tools.logging import logger

from agents import substep_managers
from agents.dynamic_planning.dynamic_local_planner import DynamicLocalPlanner, DynamicLocalPlannerWithRss, RoadOption

from classes.constants import AgentState, Phase, Hazard
from classes.rss_sensor import AD_RSS_AVAILABLE
from classes.rule import BlockingRule, Context, Rule
from agents.tools.config_creation import AgentConfig, CallFunctionFromConfig, LaunchConfig, LiveInfo, LunaticAgentSettings, CreateRuleFromConfig, RuleCreatingParameters

from classes.worldmodel import WorldModel, CarlaDataProvider
from classes.keyboard_controls import RSSKeyboardControl
from data_gathering.information_manager import InformationManager

if TYPE_CHECKING:
    from typing import Literal # for Python 3.8
    import pygame
    

class LunaticAgent(BehaviorAgent):
    """
    BasicAgent implements an agent that navigates the scene.
    This agent respects traffic lights and other vehicles, but ignores stop signs.
    It has several functions available to specify the route that the agent must follow,
    as well as to change its parameters in case a different driving mode is desired.
    """

    # using a ClassVar which allows to define preset rules for a child class
    # NOTE: Use deepcopy to avoid shared state between instances
    BASE_SETTINGS: "ClassVar[type[AgentConfig]]" = LunaticAgentSettings
    """
    Base AgentConfig class for this agent. This is used to create the default settings for the agent
    if none are provided.
    """
    
    rules: ClassVar[Dict[Phase, List[Rule]]] = {k : [] for k in Phase.get_phases()}
    """
    The rules of the this agent class. When initialized the rules of the class are copied.
    """
    
    ctx : "Context"
    """The context object of the current step"""
    
    # Information from the InformationManager
    walkers_nearby: List[carla.Walker]
    vehicles_nearby: List[carla.Vehicle]
    static_obstacles_nearby: List[carla.Actor]
    obstacles_nearby: List[carla.Actor]
    
    current_states: Dict[AgentState, int]
    """The current states of the agent. The count of the steps being each state is stored as value."""
    
    _world_model : WorldModel = None # TODO: maybe as weakref
    
    _validate_phases = False
    """A flag to sanity check if the agent passes trough the phases in the correct order"""
    
    _active_blocking_rules: Set[BlockingRule] = set()
    """Blocking rules that are currently active and have taken over the agents loop."""
    
    @classmethod
    def create_world_and_agent(cls, args: LaunchConfig, *, vehicle : carla.Vehicle, sim_world : carla.World,
                               settings_archetype: "Optional[type[AgentConfig]]"=None, agent_config: Optional["LunaticAgentSettings"]=None, 
                               overwrites: Dict[str, Any]={}):
        
        if agent_config is None:
            if hasattr(args, "agent"):
                if settings_archetype is not None:
                    logger.warning("settings_archetype was passed but using args.agent. Ignoring settings_archetype.")
                agent_config = args.agent
            elif settings_archetype is not None and isinstance(settings_archetype, object):
                logger.warning("settings_archetype is an instance. To pass an instance use agent_config instead.")
                agent_config = settings_archetype
            elif settings_archetype is not None:
                logger.debug("Creating config from settings_archetype")
                behavior = settings_archetype(overwrites)
                agent_config = behavior.make_config()
            else:
                logger.debug("Using %s._base_settings %s to create config.", cls.__name__, cls.BASE_SETTINGS)
                agent_config = cls.BASE_SETTINGS.make_config()
        else:
            logger.debug("A config was passed, using it as is.")
        
        world_model = WorldModel(agent_config, args=args, carla_world=sim_world, player=vehicle) # TEST: without args
        agent_config.planner.dt = world_model.world_settings.fixed_delta_seconds or 1/world_model._args.fps
        
        agent = cls(agent_config, world_model)
        return agent, world_model, agent.get_global_planner()

    def __init__(self, behavior: Union[str, LunaticAgentSettings], world_model: Optional[WorldModel]=None, *, vehicle: carla.Vehicle=None, overwrite_options: dict = {}, debug=True):
        """
        Initialization the agent parameters, the local and the global planner.

            :param vehicle: actor to apply to agent logic onto
            :param target_speed: speed (in Km/h) at which the vehicle will move
            :param opt_dict: dictionary in case some of its parameters want to be changed.
                This also applies to parameters related to the LocalPlanner.
            :param map_inst: carla.Map instance to avoid the expensive call of getting it.

            :debug: boolean to activate the debug mode. In the debug mode more settings will be validated.
        """
        self._debug = debug

        # Settings ---------------------------------------------------------------
        # This check should be save now. The WorldModel
        if world_model is None and len(sys.argv) > 1:
            logger.error("BUG: Beware when not passing a WorldModel, the WorldModel currently ignores command line overrides, "
                         "i.e. will only use the config file.\n> Use `%s.create_world_and_agent` and provide the LaunchConfig instead.", self.__class__.__name__)
        
        # TODO: Move this to an outside function
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
        if isinstance(behavior, DictConfig):
            behavior._set_flag("allow_objects", True)
            behavior.__dict__["_parent"] = None # Remove parent from the config, i.e. make it a top-level config.  
            
        self._behavior = behavior
        self.config = opt_dict # NOTE: This is the attribute we should use to access all information.
        
        logger.info("\n\nAgent config is %s", OmegaConf.to_yaml(self.config))
        
        # World Model
        if world_model is None:
            world_model = WorldModel(self.config, player=vehicle)
            self.config.planner.dt = world_model.world_settings.fixed_delta_seconds or 1/world_model._args.fps
        
        self._world_model : WorldModel = world_model
        self._world : carla.World = world_model.world
        
        # Register Vehicle
        self._vehicle : carla.Vehicle = world_model.player
        try:
            CarlaDataProvider.register_actor(self._vehicle) # assure that the vehicle is registered
        except KeyError as e:
            logger.info("Ignoring error of already registered actor: %s", e)
        
        self.current_phase : Phase = Phase.NONE # current phase of the agent inside the loop
        self.ctx = None

        self._live_info : LiveInfo = self.config.live_info # Accessible via property
        
        self._last_traffic_light : carla.TrafficLight = None  # Current red traffic light

        # TODO: No more hardcoded defaults / set them from opt_dict which must have all parameters; check which are parameters and which are set by other functions (e.g. _look_ahead_steps)

        # Parameters from BehaviorAgent ------------------------------------------
        # todo: check redefinitions

        self._look_ahead_steps = 0  # updated in _update_information used for local_planner.get_incoming_waypoint_and_direction

        # Initialize the planners
        self._local_planner = DynamicLocalPlannerWithRss(self._vehicle, opt_dict=opt_dict, map_inst=world_model.map, world=self._world if self._world else "MISSING", rss_sensor=world_model.rss_sensor)
        self._global_planner = CarlaDataProvider.get_global_route_planner() # NOTE: THIS does not use self.config.planner.sampling_resolution
        assert self._global_planner, "Global Route Planner not set - This should not happen, if the CarlaDataProvider has been initialized."
        if not self._global_planner:
            # This should not happen, as the global planner is set in the CarlaDataProvider at set_world
            self._global_planner = GlobalRoutePlanner(CarlaDataProvider.get_map(), self.config.planner.sampling_resolution)
            CarlaDataProvider._grp = self._global_planner 

        # Get the static elements of the scene
        self._traffic_light_map: Dict[carla.TrafficLight, carla.Transform] = CarlaDataProvider._traffic_light_map
        self._lights_list = CarlaDataProvider._traffic_light_map.keys()
        self._lights_map: Dict[int, carla.Waypoint] = {}  # Dictionary mapping a traffic light to a wp corresponding to its trigger volume location

        # Vehicle Lights
        self._lights = carla.VehicleLightState.NONE

        # Collision Sensor # TODO: duplicated in WorldModel, maybe can be shared.
        self._collision_sensor: carla.Sensor = None
        self._set_collision_sensor()

        #Rule Framework
        self.rules = deepcopy(self.__class__.rules) # Copies the ClassVar to the instance
        
        # Data Matrix
        if self.config.detection_matrix and self.config.detection_matrix.enabled:
            if self.config.detection_matrix.sync and self._world_model.world_settings.synchronous_mode:
                self._detection_matrix = DetectionMatrix(self._vehicle, self._world_model.world)
            else:
                self._detection_matrix = AsyncDetectionMatrix(self._vehicle, self._world_model.world)
            self._detection_matrix.start()  # TODO maybe find a nicer way
        else:
            self._detection_matrix = None
        self._road_matrix_counter = 0 # TODO: Todo make this nicer and maybe get ticks from world.
        
        # Information Manager
        self.information_manager = InformationManager(self)
        self.current_states = dict.fromkeys(AgentState, 0)
        
        self.add_config_rules()

    
    @property
    def live_info(self) -> LiveInfo:
        return self._live_info

    @property
    def detection_matrix(self):
        if self._detection_matrix:
            return self._detection_matrix.getMatrix()
        
    @property
    def detected_hazards(self) -> Set[Hazard]:
        return self.ctx.detected_hazards
    
    @detected_hazards.setter
    def detected_hazards(self, hazards : Set[Hazard]):
        if not isinstance(hazards, set):
            raise TypeError("detected_hazards must be a set of Hazards.")
        self.ctx._detected_hazards = hazards
        
        
    @property
    def active_blocking_rules(self) -> Set[BlockingRule]:
        """
        Blocking rules that are currently active and have taken over the agents loop.
        """
        return self._active_blocking_rules
    
    def add_hazard(self, hazard: Hazard):
        if not isinstance(hazard, Hazard): # Maybe could check for list / iterable here.
            logger.error("Adding a non Hazard to the detected_hazards set. Type %s", type(hazard))
        self.detected_hazards.add(hazard)
    
    @property
    def _map(self) -> carla.Map:
        """Get the current map of the world.""" # Needed *only* for set_destination
        return CarlaDataProvider.get_map()
    
    def render_detection_matrix(self, display:"pygame.Surface", options:Dict[str, Any]={}):
        if self._detection_matrix:
            self._detection_matrix.render(display, **options)

    def _set_collision_sensor(self):
        # see: https://carla.readthedocs.io/en/latest/ref_sensors/#collision-detector
        # and https://carla.readthedocs.io/en/latest/python_api/#carla.Sensor.listen
        blueprint = CarlaDataProvider._blueprint_library.find('sensor.other.collision')
        self._collision_sensor : carla.Sensor = assure_type(carla.Sensor, CarlaDataProvider.get_world().spawn_actor(
                                                            blueprint, carla.Transform(), attach_to=self._vehicle))
        def collision_callback(event : carla.SensorData):
            self._collision_event(event)
        self._collision_sensor.listen(self._collision_event)

    def destroy_sensor(self):
        if self._detection_matrix:
            self._detection_matrix.stop()
            self._detection_matrix = None
        if self._collision_sensor:
            self._collision_sensor.destroy()
            self._collision_sensor = None
            
    def destroy(self):
        self.destroy_sensor()
        self._world_model = None
        self._world = None
        if self.ctx:
            self.ctx.agent = None
        self.ctx = None
        try:
            self.all_vehicles.clear()
            self.vehicles_nearby.clear()
            self.all_walkers.clear()
            self.walkers_nearby.clear()
        except AttributeError:
            pass
            
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

    def update_information(self, second_pass=False):
        """
        Updates the information regarding the ego vehicle based on the surrounding world.
        """
        self.execute_phase(Phase.UPDATE_INFORMATION | Phase.BEGIN, prior_results=None)
        self._update_information(second_pass=second_pass)
        self.execute_phase(Phase.UPDATE_INFORMATION | Phase.END, prior_results=None)

    
    def _update_information(self, *, second_pass=False):
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
            if self._debug:
                if not self._lights_list and len(CarlaDataProvider._traffic_light_map.keys()):
                    logger.error("Traffic light list is empty, but map is not.")

            # ----------------------------
            # First Pass for expensive and tick-constant information
            
            # --- InformationManager ---
            information: InformationManager.Information = self.information_manager.tick() # NOTE: # Warning: Currently not route-dependant, might need to be changed later
            self.tick_information = information
            
            self._current_waypoint = information.current_waypoint
            self.current_states = information.current_states
            
            # Maybe access over subattribute, or properties
            # NOTE: If other scripts, e.g. the scenario_runner, are used in parallel or sync=False
            #       the stored actors might could have been destroyed later on.
            
            # Global Information
            self.all_vehicles = information.vehicles
            self.all_walkers = information.walkers
            self.all_static_obstacles = information.static_obstacles
            # Combination of the three lists
            self.all_obstacles = information.obstacles
        
            # Filtered by config.obstacles.nearby_vehicles_max_distance and nearby_vehicles_max_distance
            self.vehicles_nearby = information.vehicles_nearby
            self.walkers_nearby = information.walkers_nearby
            self.static_obstacles_nearby = information.static_obstacles_nearby
            
            # Combination of the three lists
            self.all_obstacles_nearby = information.obstacles_nearby
            
            # Find vehicles and walkers nearby; could be moved to the information manager
            
            # ----------------------------
            
            # Data Matrix
            # update not every frame to save performance
            if self._detection_matrix and self._detection_matrix.sync:
                self._road_matrix_counter += 1
                if (self._road_matrix_counter % self.config.detection_matrix.sync_interval) == 0:
                    #logger.debug("Updating Road Matrix")
                    # TODO: Still prevent async mode from using too much resources and slowing fps down too much.
                    self._detection_matrix.update() # NOTE: Does nothing if in async mode. self.road_matrix is updated by another thread.
                else:
                    pass
            
            # used for self._local_planner.get_incoming_waypoint_and_direction
            self._look_ahead_steps = int((self.live_info.current_speed_limit) / 10) # TODO: Maybe make this an interpolation and make more use of it
            
            # NOTE: This is the direction used by the planner in the *last* step.
            self.live_info.executed_direction = assure_type(RoadOption, self._local_planner.target_road_option)
        
        assert self.live_info.executed_direction == self._local_planner.target_road_option, "Executed direction should not change."
        
        # -------------------------------------------------------------------
        # Information that NEEDS TO BE UPDATED AFTER a plan / ROUTE CHANGE.
        # -------------------------------------------------------------------
        if not self.done():
            # NOTE: This should be called after 
            self.live_info.incoming_waypoint, self.live_info.incoming_direction = self._local_planner.get_incoming_waypoint_and_direction(
                steps=self._look_ahead_steps)
        else:
            assert second_pass == False, "In the second pass the agent should have replanned and agent.done() should be False"
            # Assumes second_pass is False
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
        
        if self._debug:
            OmegaConf.to_container(self.live_info, resolve=True, throw_on_missing=True)
    
    # TODO: Use executed direction not the one that is looked ahead
    def is_taking_turn(self) -> bool:
        return self.live_info.incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)
    
    def is_changing_lane(self) -> bool:
        return self.live_info.incoming_direction in (RoadOption.CHANGELANELEFT, RoadOption.CHANGELANERIGHT)

    # ------------------ Step & Loop Logic ------------------ #

    def add_rule(self, rule : Rule, position:Union[int, None]=None):
        """
        Add a rule to the agent. The rule will be inserted at the given position.
        
        Args:
            rule (Rule): The rule to add
            position (Union[int, None], optional): 
                The position to insert the rule at. 
                If None the rule list will be sorted by priority.
                Defaults to None.
        """
        for p in rule.phases:
            if p not in self.rules:
                logger.warning("Phase %s from Rule %s is not a default phase. Adding a new phase.", p, rule)
                self.rules[p] = []
            if position is None:
                self.rules[p].append(rule)
                self.rules[p].sort(key=lambda r: r.priority, reverse=True)
            else:
                self.rules[p].insert(position, rule)
    
    def add_rules(self, rules : List[Rule]):
        """Add a list of rules and sort the agents rules by priority."""
        if isinstance(rules, Rule):
            rules = [rules]
        for rule in rules:
            for phase in rule.phases:
                self.rules[phase].append(rule)
        for phase in self.rules.keys():
            self.rules[phase].sort(key=lambda r: r.priority, reverse=True)
            
    def add_config_rules(self, config: Optional[Union[LunaticAgentSettings, List[RuleCreatingParameters]]]=None):
        """
        Adds rules 
        """
        if config is None:
            config = self.config
        rule_list : List[RuleCreatingParameters]
        if "rules" in config:
            rule_list = config.rules
        else:
            rule_list = config
        logger.debug("Adding rules from config:\n%s", OmegaConf.to_yaml(rule_list))
        for rule in rule_list:
            self.add_rules(rule_from_config(rule))
    
    def execute_phase(self, phase : Phase, *, prior_results, update_controls:carla.VehicleControl=None) -> Context:
        """
        Sets the current phase of the agent and executes all rules that are associated with it.
        """
        normal_next = self.current_phase.next_phase() # sanity checking if everything is correct
        if self._validate_phases:
            assert normal_next == Phase.USER_CONTROLLED or phase == normal_next or phase & Phase.EXCEPTIONS or phase & Phase.USER_CONTROLLED, f"Phase {phase} is not the next phase of {self.current_phase} or an exception phase. Expected {normal_next}"
        
        self.current_phase = phase # set next phase
        
        if update_controls is not None:
            self.ctx.set_control(update_controls)
        self.ctx.prior_result = prior_results
        rules_to_check = self.rules.get(phase, ()) # use get if a custom phase is added, without a rule
        try:
            for rule in rules_to_check: # todo: maybe dict? grouped by phase?
                #todo check here for the phase instead of in the rule
                assert self.current_phase in rule.phases, f"Current phase {self.current_phase} not in Rule {rule.phases}" # TODO remove:
                rule(self.ctx)
        except NoFurtherRulesException:
            pass
        except omegaconf.ReadonlyConfigError:
            print("WARNING: A action likely tried to change `ctx.config` which is non-permanent. Use `ctx.agent.config.` instead.")
            raise
        return self.ctx
    
    def _plan_path_phase(self, *, second_pass, debug=False):
        try:
            self.execute_phase(Phase.PLAN_PATH | Phase.BEGIN, prior_results=None)
            # User defined action
            # TODO: when going around corners / junctions and the distance between waypoints is too big,
            # We should replan and and make a more fine grained plan, to stay on the road.
            self.execute_phase(Phase.PLAN_PATH | Phase.END, prior_results=None)
        except UpdatedPathException as e:
            if second_pass:
                logger.warning("UpdatedPathException was raised in the second pass. This should not happen: %s. Restrict your rule on ctx.second_pass.", e)
            return self.run_step(debug, second_pass=True) # TODO: # CRITICAL: For child classes like the leaderboard agent this calls the higher level run_step.
            
    def verify_settings(self, config: LunaticAgentSettings = None, *, verify_dataclass: Union["type[AgentConfig]", bool] = True, strictness=0):
        """
        Verifies the settings of the LunaticAgent.
        Foremost this checks if the planner.dt value has been set to the speed of the world ticks in synchronous mode.
        Secondly if `verify_dataclass=True` or a different AgentConfig class is provided, it will check for 
        correct type usage.

        Args:
            config (LunaticAgentSettings, optional): The configuration to verify. 
                If not provided, the agent's default configuration will be used. 
                Defaults to None.
            verify_dataclass (Union["type[AgentConfig]", bool], optional): 
                Determines the dataclass to use for verification. 
                If True, the BASE_SETTINGS dataclass will be used.
                See [`AgentConfig.check_config`](#AgentConfig.check_config) for more details.
                Defaults to True.
            strictness (int, optional): 
                The strictness level for  [`AgentConfig.check_config`](#AgentConfig.check_config). 
                Defaults to 3.

        Raises:
            TypeError: If `verify_dataclass` is not a valid AgentConfig subclass or True.
            MissingMandatoryValue: If `config.planner.dt` is not present or not a float

        """
        if self._world_model.world_settings.synchronous_mode:
            # Assure that dt is set
            if isinstance(config, DictConfig):
                OmegaConf.select(config,
                    "planner.dt",
                    throw_on_missing=True
                )
            elif not isinstance(config.planner.dt, float):
                from omegaconf import MissingMandatoryValue
                raise MissingMandatoryValue("`config.planner.dt` needs to be set to a value. Cannot be:", type(config.planner.dt), config.planner.dt)
        
        if strictness < 0:
            return
        
        # NOTE: Below is experimental and might fail as the config at this point has already beeen setup
        
        config = config or self.config
        
        from agents.tools import config_creation
        _old = config_creation.WARN_LIVE_INFO
        config_creation.WARN_LIVE_INFO = False

        if verify_dataclass:
            if verify_dataclass == True:
                dataclass = self.BASE_SETTINGS
            elif issubclass(verify_dataclass, AgentConfig):
                dataclass = verify_dataclass
            else:
                raise TypeError("`verify_dataclass` must be a `AgentConfig` or `True` to select the BASE_SETTINGS ")
            dataclass.check_config(config, dataclass.get("strict_config", strictness), as_dict_config=True)

        config_creation.WARN_LIVE_INFO = _old
                

    def run_step(self, debug=False, second_pass=False) -> carla.VehicleControl:
        """
        The agent.run_step is the main method in which the agent calculates the next vehicle control object.
        
        Warning:
            To be compatible with the leaderboard agent, always pass debug as a positional argument, e.g.
            when you are using a `BlockingRule` that loops
        """
        
        if not second_pass:
            ctx = self.make_context(last_context=self.ctx)
        else:
            ctx = self.ctx
        ctx.second_pass = second_pass
        try:
            # ----------------------------
            # Phase 0 - Update Information
            # ----------------------------
            # > Phase.UPDATE_INFORMATION | Phase.BEGIN
            self.update_information(second_pass=second_pass)
            # > Phase.UPDATE_INFORMATION | Phase.END
            
            # ----------------------------
            # Phase 1 - Plan Path
            # ----------------------------

            # TODO: What TODO if the last phase was COLLISION, EMERGENCY
            # Some information to PLAN_PATH should reflect this

            # TODO: add option to diverge from existing path here, or plan a new path
            # NOTE: Currently done in the local planner and behavior functions
            self._plan_path_phase(second_pass=second_pass, debug=debug)
            
            if self.done():
                # NOTE: Might be in NONE phase here.
                self.execute_phase(Phase.DONE| Phase.BEGIN, prior_results=None)
                if self.done():
                    # No Rule set a net destination
                    print("The target has been reached, stopping the simulation")
                    self.execute_phase(Phase.TERMINATING | Phase.BEGIN, prior_results=None)
                    raise AgentDoneException
                self.execute_phase(Phase.DONE | Phase.END, prior_results=None)
                return self.run_step(second_pass=True) # TODO: # CRITICAL: For child classes like the leaderboard agent this calls the higher level run_step.
            
            # ----------------------------
            # Phase NONE - Before Running step
            # ----------------------------
            try:
                planned_control = self._inner_step(debug=debug)  # debug=True draws waypoints
                if self.detected_hazards:
                    raise EmergencyStopException(self.detected_hazards)
    
            except EmergencyStopException as emergency:
                
                # ----------------------------
                # Phase Emergency
                # no Rule with Phase.EMERGENCY | BEGIN cleared the provided hazards in ctx.prior_results
                # ----------------------------
                
                emergency_controls = self.emergency_manager(reasons=emergency.hazards_detected)
                
                # TODO: somehow backup the control defined before.
                self.execute_phase(Phase.EMERGENCY | Phase.END, update_controls=emergency_controls, prior_results=emergency.hazards_detected)
                planned_control = self.get_control()
            
            # Other Exceptions
            
            except SkipInnerLoopException as skip:
                self.set_control(skip.planned_control)
                self.current_phase = Phase.USER_CONTROLLED
                planned_control = skip.planned_control
            except UserInterruption:
                raise
            except UpdatedPathException as e:
                if second_pass > 5:
                    logger.warning("UpdatedPathException was raised more than %s times. Warning: This might be an infinite loop.", second_pass)
                elif second_pass > 50:
                    raise RecursionError("UpdatedPathException was raised more than 50 times. Assuming an infinite loop and terminating")
                else:
                    logger.warning("UpdatedPathException was raised in the inner step, this should be done in Phase.PLAN_PATH ", e)
                return self.run_step(second_pass=int(second_pass)+1) 
            except LunaticAgentException as e:
                if self.ctx.control is None:
                    raise ValueError("A VehicleControl object must be set on the agent when %s is raised during `._inner_step`" % type(e).__name__) from e
            
            # ----------------------------
            # No known Phase multiple exit points
            # ----------------------------
            
            # ----------------------------
            # Phase RSS - Check RSS
            # ----------------------------
            
            ctx = self.execute_phase(Phase.RSS_EVALUATION | Phase.BEGIN, prior_results=None, update_controls=planned_control)
            if AD_RSS_AVAILABLE and self.config.rss and self.config.rss.enabled:
                rss_updated_controls = self._world_model.rss_check_control(ctx.control)
            else:
                rss_updated_controls = None
            # NOTE: rss_updated_controls could be None. 
            ctx = self.execute_phase(Phase.RSS_EVALUATION | Phase.END, prior_results=rss_updated_controls)
            
            #if ctx.control is not planned_control:
            #    logger.debug("RSS updated control accepted.")
            
        except ContinueLoopException as e:
            logger.debug("ContinueLoopException skipping rest of loop.")
            if self.ctx.control is None:
                raise ValueError("A VehicleControl object must be set on the agent when %s is raised during `._inner_step`" % type(e).__name__) from e
        
        planned_control = self.ctx.control
        planned_control.manual_gear_shift = False
        return self.get_control()

    @must_clear_hazard
    @result_to_context("control")
    def _inner_step(self, debug=False) -> carla.VehicleControl:
        """
        This is our main entry point that runs every tick.
        
        Raises:
            EmergencyStopException: If self.detected_hazards is not empty when the 
            function returns.
        """
        self.debug = debug

        # ----------------------------
        # Phase 2 - Detection of Pedestrians and Traffic Lights
        # ----------------------------

        # Detect hazards
        # phases are executed in detect_hazard
        # > Phase.DETECT_TRAFFIC_LIGHTS | Phase.BEGIN # phases executed inside
        pedestrians_or_traffic_light = self.detect_hazard()
        # > Phase.DETECT_PEDESTRIANS | Phase.END

        # Pedestrian avoidance behaviors
        # currently doing either emergency (detect_hazard) stop or nothing 
        if self.detected_hazards:

            # ----------------------------
            # Phase Hazard Detected (traffic light or pedestrian)
            # If no Rule with Phase.EMERGENCY | BEGIN clears pedestrians_or_traffic_light
            # An EmergencyStopException is raised
            # ----------------------------

            self.react_to_hazard(pedestrians_or_traffic_light) # Optional[NoReturn]
    
        # -----------------------------
        # Phase Detect Static Obstacles
        # -----------------------------
        
        self.execute_phase(Phase.DETECT_STATIC_OBSTACLES | Phase.BEGIN, prior_results=None)
        static_obstacle_detection_result = self.detect_obstacles_in_path(self.static_obstacles_nearby)
        if static_obstacle_detection_result.obstacle_was_found:
            # Must plan around it
            self.add_hazard(Hazard.STATIC_OBSTACLE)
        # TODO: add a basic rule for circumventing static obstacles
        self.execute_phase(Phase.DETECT_STATIC_OBSTACLES | Phase.END, prior_results=static_obstacle_detection_result)
        # Not throwing an error here yet
        
        # ----------------------------
        # Phase 3 - Detection of Cars
        # ----------------------------
            
        self.execute_phase(Phase.DETECT_CARS | Phase.BEGIN, prior_results=None) # TODO: Maybe add some prio result
        vehicle_detection_result = self.detect_obstacles_in_path(self.vehicles_nearby)
        
        # TODO: add a way to let the execution overwrite
        if vehicle_detection_result.obstacle_was_found:

            # ----------------------------
            # Phase 2.A - React to cars in front
            # TODO: turn this into a rule.
            #    remove CAR_DETECTED -> pass detection_result to rules
            # TODO some way to circumvent returning control here, like above.
            # TODO: Needs refinement with the car_following_behavior
            # ----------------------------

            self.execute_phase(Phase.CAR_DETECTED | Phase.BEGIN, prior_results=vehicle_detection_result)
            control = self.car_following_behavior(*vehicle_detection_result) # Optional[NoReturn]
            self.execute_phase(Phase.CAR_DETECTED | Phase.END, update_controls=control, prior_results=vehicle_detection_result)
            return self.get_control()
        
        #TODO: maybe new phase instead of END or remove CAR_DETECTED and handle as rules (maybe better)
        self.execute_phase(Phase.DETECT_CARS | Phase.END, prior_results=None) # NOTE: avoiding tailgate here
        
        
        # Intersection behavior
        # NOTE: is_taking_turn <- incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)
        if self.live_info.incoming_waypoint.is_junction and self.is_taking_turn():

            # ----------------------------
            # Phase Turning at Junction
            # ----------------------------

            self.execute_phase(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, prior_results=None)
            control = self._calculate_control(debug=debug)
            self.execute_phase(Phase.TURNING_AT_JUNCTION | Phase.END, update_controls=control, prior_results=None)
            return self.get_control()

        # ----------------------------
        # Phase 4 - Plan Path normally
        # ----------------------------
        
        # Normal behavior
        self.execute_phase(Phase.TAKE_NORMAL_STEP | Phase.BEGIN, prior_results=None)
        control = self._calculate_control(debug=debug)
        self.execute_phase(Phase.TAKE_NORMAL_STEP | Phase.END, prior_results=None, update_controls=control)

        # Leave loop and apply controls outside 
        return self.get_control()
    
    def _calculate_control(self, debug=False):
        """
        Plan the next step of the agent. This will execute the local planner
        to retrieve the next control fitting the current path and settings.
        
        Note:
            This is the innermost function of the agents run_step function.
            It should be called each step to acquire a desired control object.
            Use this function inside rules if a control object is desired.
            
            **[Context.get_or_calculate_control](#Context.get_or_calculate_control) is a safer alternative to this function**
        
        Warning:
            If you do not use this function in a [`BlockingRule`](#BlockingRule)
            you should raise a `SkipInnerLoopException` or `ContinueLoopException` 
            else the planned path will skip a waypoint.
            
        Warning:
            This function only calculates and returns the control object directly. 
            **It does not set the agent/ctx.control attribute which is the one
            the agent uses in [`apply_control`](#apply_control) to apply the final controls.**
            
        See Also:

        """
        if self.ctx.control is not None:
            logger.error("Control was set before calling _calculate_control. This might lead to unexpected behavior.")
        
        return self._local_planner.run_step(debug)

    def parse_keyboard_input(self, allow_user_updates=True, *, control=None):
        """
        Parse the current user input and allow manual updates of the controls.
        
        Args:
            allow_user_updates: If True, the user can update the controls manually.
                Otherwise only the normal hotkeys do work.
        """
        planned_control = control or self.get_control()
        self.execute_phase(Phase.APPLY_MANUAL_CONTROLS | Phase.BEGIN, prior_results=planned_control)
        
        # Controls can be updated inplace by the user.        
        if self._world_model.controller.parse_events(planned_control if allow_user_updates else carla.VehicleControl()):
            print("Exiting by user input.")
            raise UserInterruption("Exiting by user input.")
       
        self.execute_phase(Phase.APPLY_MANUAL_CONTROLS | Phase.END, prior_results=None)
    
    @phase_callback(on_exit=Phase.EXECUTION | Phase.END)
    def apply_control(self, control: Optional[carla.VehicleControl]=None):
        """
        Applies the control to the agent's actor.
        Will execute the `Phase.EXECUTION | Phase.BEGIN` and `Phase.EXECUTION | Phase.END` phases.
        
        Note:
            The final control object that is applied to the agent's actor
            is stored in the `ctx.control` attribute.
        """
        if control is None:
            control = self.get_control()
        if self.current_phase != Phase.EXECUTION | Phase.BEGIN:
            self.execute_phase(Phase.EXECUTION | Phase.BEGIN, prior_results=control)
        else:
            logger.debug("Agent is already in execution phase.")
        # Set automatic control-related vehicle lights
        self.update_lights(control)
        self._vehicle.apply_control(control)
    
    # ------------------ Hazard Detection & Reaction ------------------ #

    def detect_hazard(self) -> Set[Hazard]:
        # Red lights and stops behavior

        self.execute_phase(Phase.DETECT_TRAFFIC_LIGHTS | Phase.BEGIN, prior_results=None)
        tlight_detection_result = self.traffic_light_manager()
        if tlight_detection_result.traffic_light_was_found:
            assert tlight_detection_result.traffic_light.id
            self.add_hazard(Hazard.TRAFFIC_LIGHT)             #TODO: Currently cannot give fine grained priority results
            #assert self.live_info.next_traffic_light.id == tlight_detection_result.traffic_light.id, "Next assumed traffic light should be the same as the detected one." # TEMP
            
            # NOTE next tlight is the next bounding box and might not be the next "correct" one
            # self.live_info.next_traffic_light.id != tlight_detection_result.traffic_light.id:
            
        self.execute_phase(Phase.DETECT_TRAFFIC_LIGHTS | Phase.END, prior_results=tlight_detection_result)

        # Pedestrian avoidance behaviors
        self.execute_phase(Phase.DETECT_PEDESTRIANS | Phase.BEGIN, prior_results=None)
        hazard, detection_result = self.pedestrian_avoidance_behavior(self._current_waypoint)
        if detection_result.obstacle_was_found:
            if hazard:   #TODO: Currently cannot give very fine grained priority results, i.e. slow down or stop
                self.add_hazard(Hazard.PEDESTRIAN | Hazard.EMERGENCY)
            else:
                self.add_hazard(Hazard.PEDESTRIAN | Hazard.WARNING)
                # NOTE: its a flag, could pack all in one bin
                # Pro: easier to check
                # Con: when to remove other states like warning
                # Make it a dict with the state as key and the detection result as value!
        self.execute_phase(Phase.DETECT_PEDESTRIANS | Phase.END, prior_results=(hazard, detection_result))
        
        return self.detected_hazards
    
    def react_to_hazard(self, hazard_detected : Union[Hazard, Iterable[Hazard], None]) -> Optional[NoReturn]:
        """
        Called when a hazard was detected-
        
        Will store the detected hazards in the Context: `ctx.prior_result`
        If no rule clears this variable, the agent will throw a EmergencyStopException
        
        Raises:
            EmergencyStopException: If a hazard was detected and no rule cleared it.
        """

        # update state? prevent flodding of log information
        #logger.info("Hazard(s) detected: %s", self.detected_hazards)
        if hazard_detected:
            if not isinstance(hazard_detected, Hazard):
                self.detected_hazards.update(hazard_detected)
            else:
                self.detected_hazards.add(hazard_detected)
        
        if self.detected_hazards:
            self.execute_phase(Phase.EMERGENCY | Phase.BEGIN, prior_results=hazard_detected)
        else:
            logger.info("react_to_hazard was called without any detected hazards.")
        if self.detected_hazards:
            raise EmergencyStopException(hazard_detected)
        logger.info("Hazards have been cleared.")
        
    
    # ------------------ Behaviors ------------------ #
    # TODO: Section needs overhaul -> turn into rules

    def pedestrian_avoidance_behavior(self, ego_vehicle_wp : carla.Waypoint) -> Tuple[bool, ObstacleDetectionResult]:
        # TODO: # CRITICAL: This for some reasons also detects vehicles as pedestrians
        # note ego_vehicle_wp is the current waypoint self._current_waypoint
        detection_result = self.detect_obstacles_in_path(self.walkers_nearby)
        if (detection_result.obstacle_was_found
            and (detection_result.distance - max(detection_result.obstacle.bounding_box.extent.y, 
                                                 detection_result.obstacle.bounding_box.extent.x)
                                           - max(self._vehicle.bounding_box.extent.y, 
                                                 self._vehicle.bounding_box.extent.x)
            < self.config.distance.emergency_braking_distance)):
            print("Detected walker", detection_result.obstacle)
            # TODO: should slow down here
            return True, detection_result
        # TODO detected but not stopping -> ADD avoidance behavior
        elif detection_result.obstacle_was_found:
            logger.debug("Detected a pedestrian but determined no intervention necessary (too far away).")
        return False, detection_result
        
    def car_following_behavior(self, vehicle_detected:bool, vehicle:carla.Actor, distance:float) -> carla.VehicleControl:
        exact_distance = distance - max(vehicle.bounding_box.extent.y, vehicle.bounding_box.extent.x) - max(
            self._vehicle.bounding_box.extent.y, self._vehicle.bounding_box.extent.x)

        if exact_distance < self.config.distance.emergency_braking_distance:
            # Note: If the passed set is not cleared by a Phase.EMERGENCY | Phase.BEGIN rule, 
            # an EmergencyStopException is raised.
            self.add_hazard(Hazard.CAR)
            self.react_to_hazard(hazard_detected={Hazard.CAR}) # Optional[NoReturn]
        controls = self.car_following_manager(vehicle, exact_distance)
        return controls

    # ------------------ Managers ------------------ #

    # Moved outside of the class for organization
    from agents.tools.lunatic_agent_tools import detect_obstacles_in_path
    from agents.substep_managers import traffic_light_manager # -> TrafficLightDetectionResult
    from agents.substep_managers import car_following_manager # -> carla.VehicleControl
    from agents.substep_managers import emergency_manager
    
    # Subfunction of traffic_light_manager. In traffic_light_manager the parameters are chosen automatically.
    from agents.substep_managers.traffic_light import affected_by_traffic_light

    # ----

    #@override
    def add_emergency_stop(self, control, reasons:"set[str]"=None) -> carla.VehicleControl:
        """
        Modifies the control values to perform an emergency stop.
        The steering remains unchanged to avoid going out of the lane during turns.

        :param control: (carla.VehicleControl) control to be modified
        :param enable_random_steer: (bool, optional) Flag to enable random steering
        """
        return self.emergency_manager(control, reasons)
    
    
    def lane_change(self, direction: "Literal['left'] | Literal['right']", same_lane_time=0, other_lane_time=0, lane_change_time=2):
        """
        Changes the path so that the vehicle performs a lane change.
        Use 'direction' to specify either a 'left' or 'right' lane change,
        and the other 3 fine tune the maneuver
        """
        speed = self.live_info.current_speed / 3.6 # m/s
        # This is a staticfunction from BasicAgent function
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
            logger.info("Ignoring the lane change as no path was found")

        super(LunaticAgent, self).set_global_plan(path)
        # TODO: # CRITICAL: Keep old global plan if it is some end goal -> Restore it.
        
    # TODO: Use generate_lane_change_path to finetune 
    def make_lane_change(self, order=["left", "right"], up_angle_th=180, low_angle_th=0):
        """
        Move to the left/right lane if possible

        Args:
            order (Sequence[Literal["left", "right"]] | Literal["left", "right"]): The order in
                which the agent should try to change lanes. If a single string is given, the agent
                will try to change to that lane.
            up_angle_th (int): The angle threshold for the upper limit of obstacle detection in the other lane.
                Default is 180 degrees, meaning that the agent will detect obstacles ahead.
            low_angle_th (int): The angle threshold for the lower limit of obstacle detection in the other lane.
                Default is 0 degrees, meaning that the agent will detect obstacles behind.
            
        Assumes:
            (self.config.live_info.incoming_direction == RoadOption.LANEFOLLOW \
                and not waypoint.is_junction and self.config.live_info.current_speed > 10)
            check_behind.obstacle_was_found and self.config.live_info.current_speed < get_speed(check_behind.obstacle)
        """
        vehicle_list = self.vehicles_nearby
        waypoint = self._current_waypoint # todo use a getter

        # There is a faster car behind us
        if isinstance(order, str):
            order = [order]
        
        for direction in order:
            if direction == "right":
                right_turn = waypoint.right_lane_marking.lane_change
                can_change = (right_turn == carla.LaneChange.Right or right_turn == carla.LaneChange.Both)
                other_wpt = waypoint.get_right_lane()
                lane_offset = 1
            elif direction == "left":
                left_turn = waypoint.left_lane_marking.lane_change
                can_change = (left_turn == carla.LaneChange.Left or left_turn == carla.LaneChange.Both)
                other_wpt = waypoint.get_left_lane()
                lane_offset = -1
            else:
                ValueError("Direction must be 'left' or 'right', was %s" % direction)
            if can_change and lanes_have_same_direction(waypoint, other_wpt) and other_wpt.lane_type == carla.LaneType.Driving:
                # Detect if right lane is free
                detection_result = detect_vehicles(self, vehicle_list, 
                                                self.max_detection_distance("other_lane"), 
                                                    up_angle_th=up_angle_th,
                                                    low_angle_th=low_angle_th,
                                                    lane_offset=lane_offset)
                if not detection_result.obstacle_was_found:
                    logger.debug("Change Lane, moving to the %s! Reason: %s", direction, "Overtaking" if tuple(order) == ("left", "right") else "Tailgating")

                    end_waypoint = self._local_planner.target_waypoint
                    # TODO: How to set waypoint order? Or better use generate_lane_change_path!
                    self.set_destination(end_location=other_wpt.transform.location, 
                                         start_location=end_waypoint.transform.location, clean_queue=True)
                    return True

    # ------------------ Callbacks ------------------ #
    
    def _collision_event(self, event : carla.CollisionEvent):
        # https://carla.readthedocs.io/en/latest/python_api/#carla.CollisionEvent
        # e.g. setting ignore_vehicles to False, if it was True before.
        # do an emergency stop (in certain situations)
        NotImplemented  # TODO: Brainstorm and implement
        return substep_managers.collision_manager(self, event)
        
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
    
    def get_control(self):
        """
        Returns the currently planned control of the agent.
        
        If retrieved before the local planner has been run, it will return None.
        """
        return self.ctx.control

    # ------------------ Setter Function ------------------ #
    
    def set_control(self, control : carla.VehicleControl):
        """
        Set new controls for the agent. Must be called before apply_control.
        
        Raises:
            ValueError: If the control is None.
        """
        self.ctx.control = control
    
    def set_vehicle(self, vehicle:carla.Vehicle):
        self._vehicle = vehicle
        # Data Matrix
        if self.config.detection_matrix.enabled:
            if self._world_model.world_settings.synchronous_mode:
                self._detection_matrix = DetectionMatrix(self._vehicle, self._world_model.world, self._world_model.map)
            else:
                self._detection_matrix = AsyncDetectionMatrix(self._vehicle, self._world_model.world, self._world_model.map)
        else:
            self._detection_matrix = None
        self._local_planner = DynamicLocalPlannerWithRss(self._vehicle, opt_dict=self.config, map_inst=CarlaDataProvider.get_map(), world=self._world_model.world, rss_sensor=self._world_model.rss_sensor)
    
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

    from agents.tools.lunatic_agent_tools import max_detection_distance
    

    # ------------------ Overwritten functions ------------------ #

    # Compatibility with BehaviorAgent interface
    _vehicle_obstacle_detected = agents.tools.lunatic_agent_tools.detect_vehicles
    """
    Single Lane Detection
    
    Note:
        Unused, kept for compatibility with BehaviorAgent interface
    """

    
    # Staticmethod that we outsource
    _generate_lane_change_path = staticmethod(agents.tools.lunatic_agent_tools.generate_lane_change_path)


    # NOTE: the original pedestrian_avoid_manager is still usable
    def pedestrian_avoid_manager(self, waypoint) -> NoReturn:
        raise NotImplementedError("This function was replaced by ", substep_managers.pedestrian_detection_manager)

    #@override
    def collision_and_car_avoid_manager(self, waypoint) -> NoReturn:
        a = self.pedestrian_avoid_manager()
        raise NotImplementedError("This function was split into detect_obstacles_in_path and car_following_manager")
    
    #@override
    def _tailgating(self, waypoint, vehicle_list) -> NoReturn:
        raise NotImplementedError("Tailgating has been implemented as a rule")

    #@override
    def emergency_stop(self) -> NoReturn:
        raise NotImplementedError("This function was overwritten use ´add_emergency_stop´ instead")

    # ------------------------------------ #
    # As reference Parent Functions 
    # ------------------------------------ #
    #def get_local_planner(self):
    #def get_global_planner(self):

    #def done(self): # from base class self._local_planner.done()
        
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
    

