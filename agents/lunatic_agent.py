# pyright: strict

"""
This module implements an agent that roams around a track following random
waypoints and avoiding other vehicles. The agent also responds to traffic lights,
traffic signs, and has different possible configurations.
"""

from __future__ import annotations

import sys
from copy import deepcopy
from typing import (Any, ClassVar, Dict, Iterable, List, NoReturn, Optional, Sequence, Set, Union, 
                    TYPE_CHECKING, cast as assure_type)
from typing_extensions import Self, Literal, Unpack
from agents.rules import rule_from_config

import carla  # pyright: ignore[reportMissingTypeStubs]
import omegaconf
from omegaconf import DictConfig, OmegaConf

from classes.exceptions import *
from classes.constants import (AgentState, HazardSeverity, Phase, Hazard, RoadOption, 
                               AD_RSS_AVAILABLE, READTHEDOCS)
from classes.worldmodel import WorldModel, CarlaDataProvider
from classes.rule import BlockingRule, Context, Rule

import agents.tools
import agents.tools.lunatic_agent_tools

from agents.tools.config_creation import RssRoadBoundariesModeAlias
from agents.tools.hints import ObstacleDetectionResult, TrafficLightDetectionResult
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.behavior_agent import BehaviorAgent

from agents.tools.logging import logger
from agents.tools.lunatic_agent_tools import (detect_vehicles, must_clear_hazard, replace_with,
                                              result_to_context,
                                              phase_callback, generate_lane_change_path) # type: ignore[unused-import]
from agents.tools.misc import lanes_have_same_direction

from agents import substep_managers
from agents.dynamic_planning.dynamic_local_planner import DynamicLocalPlannerWithRss

from agents.tools.config_creation import (AgentConfig, LaunchConfig, LiveInfo, LunaticAgentSettings, 
                                          RuleCreatingParameters)

from data_gathering.information_manager import InformationManager
from data_gathering.car_detection_matrix.run_matrix import AsyncDetectionMatrix, DetectionMatrix

if TYPE_CHECKING:
    import pygame

class LunaticAgent(BehaviorAgent):
    """
    BasicAgent implements an agent that navigates the scene.
    This agent respects traffic lights and other vehicles, but ignores stop signs.
    It has several functions available to specify the route that the agent must follow,
    as well as to change its parameters in case a different driving mode is desired.
    """

    BASE_SETTINGS: "type[LunaticAgentSettings]" = LunaticAgentSettings
    """
    Base AgentConfig class for this agent. This is used to create the default settings for the agent
    if none are provided.
    """
    
    DEFAULT_RULES: ClassVar[Dict[Phase, List[Rule]]] = {k : [] for k in Phase.get_phases()}
    """
    Default rules of this agent class when initialized.
    
    :meta hide-value:
    """
    
    rules: Dict[Phase, List[Rule]]
    """
    The rules of the this agent.
    When initialized the rules are deep copied from :py:attr:`DEFAULT_RULES`.
    """
    
    ctx : "Context"
    """The context object of the current step"""
    
    # Information from the InformationManager
    walkers_nearby: List[carla.Walker]
    vehicles_nearby: List[carla.Vehicle]
    static_obstacles_nearby: List[carla.Actor]
    """Static obstacles detected by the :py:class:`.InformationManager`"""
    
    obstacles_nearby: List[carla.Actor]
    """
    Combination of :py:attr:`vehicles_nearby`, :py:attr:`walkers_nearby` 
    and :py:attr:`static_obstacles_nearby`.
    """
    
    traffic_lights_nearby : List[carla.TrafficLight]
    traffic_signs_nearby : List[carla.TrafficSign] = NotImplemented
    """
    Not yet implemented
    
    :meta private:
    """
    
    current_states: Dict[AgentState, int]
    """The current states of the agent. The count of the steps being each state is stored as value."""
    
    #  
    
    _world_model : WorldModel
    """Reference to the attached :py:class:`WorldModel`."""
    
    _validate_phases = False
    """A flag to sanity check if the agent passes trough the phases in the correct order"""
    
    _active_blocking_rules: Set[BlockingRule] = set()
    """Blocking rules that are currently active and have taken over the agents loop."""
    
    # ------------------ Initialization ------------------ #
    
    from agents.tools.lunatic_agent_tools import create_agent_config as _create_agent_config
    
    @classmethod
    def create_world_and_agent(cls, args: LaunchConfig, *, 
                               vehicle : Optional[carla.Vehicle]=None, 
                               sim_world : carla.World,
                               settings_archetype: "Optional[type[AgentConfig]]"=None, 
                               agent_config: Optional["LunaticAgentSettings"]=None, 
                               overwrites: Optional[Dict[str, Any]]={}
                               ) -> tuple[Self, WorldModel, GlobalRoutePlanner]:
        """
        Setup function to create the agent from the :py:class:`LaunchConfig` settings.
        
        Note:
            - :py:meth:`.GameFramework.init_agent_and_interface` is the preferred way to create to
              instantiate the agent, only use this method if you try not do create a 
              :py:class:`GameFramework` object.
        """
        if overwrites is None:
            overwrites = {}

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
                behavior = settings_archetype(overwrites) # type: ignore
                agent_config = cls.BASE_SETTINGS.cast(behavior.to_dict_config())
            else:
                logger.debug("Using %s._base_settings %s to create config.", cls.__name__, cls.BASE_SETTINGS)
                agent_config = cls.BASE_SETTINGS.cast(cls.BASE_SETTINGS.to_dict_config())
            assert agent_config is not None
        else:
            logger.debug("A config was passed, using it as is.")
        
        world_model = WorldModel(agent_config, args=args, carla_world=sim_world, player=vehicle) # TEST: without args
        agent_config.planner.dt = world_model.world_settings.fixed_delta_seconds or 1/world_model._args.fps  # pyright: ignore[reportPrivateUsage]
        
        agent = cls(agent_config, world_model)
        return agent, world_model, agent.get_global_planner()

    def __init__(self, 
                 settings: Union[str, LunaticAgentSettings], 
                 world_model: Optional[WorldModel]=None, 
                 *, 
                 vehicle: Optional[carla.Vehicle]=None, 
                 overwrite_options: dict[str, Any] = {}, 
                 debug: bool=True):
        """
        Initialize the LunaticAgent.

        Args:
            settings : 
                The settings of the agent to construct the :py:attr:`LunaticAgent.config`. 
                It can be either a string pointing to a yaml file or a LunaticAgentSettings.
            world_model : The world model to use. If None, a new WorldModel will be created.
            vehicle : The vehicle controlled by the agent. Can be None then the :code:`world_model.player` will be used.
            overwrite_options : Additional options to overwrite the default agent configuration.
            debug : Whether to enable debug mode.
        """
        self._debug = debug
        """Enables additional debug output."""
        if world_model is None and len(sys.argv) > 1:
            logger.error("BUG: Beware when not passing a WorldModel, the WorldModel currently ignores command line overrides, "
                         "i.e. will only use the config file.\n> Use `%s.create_world_and_agent` and provide the LaunchConfig instead.", self.__class__.__name__)

        # -------------------- Settings ------------------------
        # Depending on the input type, the settings are created differently.
        
        self.config = self._create_agent_config(settings, world_model, overwrite_options)
          
        # -------------------------------
        
        logger.info("\n\nAgent config is %s", OmegaConf.to_yaml(self.config))
        
        # World Model
        if world_model is None:
            world_model = WorldModel(self.config, player=vehicle)
            self.config.planner.dt = world_model.world_settings.fixed_delta_seconds or 1/world_model._args.fps # pyright: ignore[reportPrivateUsage]
        
        self._world_model : WorldModel = world_model
        self._world : carla.World = world_model.world
        
        # Register Vehicle
        assert world_model.player is not None
        self.set_vehicle(world_model.player)
        
        self.current_phase : Phase = Phase.NONE
        """current phase of the agent inside the loop"""
        
        self.ctx = None                         # type: ignore

        self._last_traffic_light : Optional[carla.TrafficLight] = None
        """Current red traffic light"""

        # TODO: No more hardcoded defaults / set them from opt_dict which must have all parameters; check which are parameters and which are set by other functions (e.g. _look_ahead_steps)

        # Parameters from BehaviorAgent ------------------------------------------
        # todo: check redefinitions

        self._look_ahead_steps : int = 0
        """
        updated in _update_information used for local_planner.get_incoming_waypoint_and_direction
        """

        # Initialize the planners
        self._global_planner = CarlaDataProvider.get_global_route_planner() # NOTE: THIS does not use self.config.planner.sampling_resolution
        if not self._global_planner:
            logger.error("Global Route Planner not set - This should not happen, if the CarlaDataProvider has been initialized.")
            self._global_planner = GlobalRoutePlanner(CarlaDataProvider.get_map(), self.config.planner.sampling_resolution)
            CarlaDataProvider._grp = self._global_planner  # pyright: ignore[reportPrivateUsage]

        # Get the static elements of the scene
        self._traffic_light_map: Dict[carla.TrafficLight, carla.Transform] = CarlaDataProvider._traffic_light_map  # pyright: ignore[reportPrivateUsage]
        self._lights_list = CarlaDataProvider._traffic_light_map.keys()  # pyright: ignore[reportPrivateUsage]
        self._lights_map: Dict[int, carla.Waypoint] = {}
        """Dictionary mapping a traffic light to a wp corresponding to its trigger volume location"""

        # Vehicle Lights
        self._vehicle_lights = carla.VehicleLightState.NONE

        # Collision Sensor # NOTE: another in the WorldModel for the HUD
        self._set_collision_sensor()

        # Rule Framework
        # 1. add all rules from the class, if any - else this is a dict with empty lists
        self.rules = deepcopy(self.__class__.DEFAULT_RULES) # Copies the ClassVar to the instance
        
        # 2. add rules from the config
        self.add_config_rules()
        
        # Information Manager
        self.information_manager = InformationManager(self)
        self.current_states = self.information_manager.state_counter # share the dict
        
        
    # --------------------- Collision Callback ------------------------
        
    def _set_collision_sensor(self):
        # see: https://carla.readthedocs.io/en/latest/ref_sensors/#collision-detector
        # and https://carla.readthedocs.io/en/latest/python_api/#carla.Sensor.listen
        blueprint = CarlaDataProvider._blueprint_library.find('sensor.other.collision') # pyright: ignore[reportPrivateUsage]
        self._collision_sensor : carla.Sensor = assure_type(carla.Sensor, CarlaDataProvider.get_world().spawn_actor(
                                                            blueprint, carla.Transform(), attach_to=self._vehicle))

        self._collision_sensor.listen(self._collision_event)
        
    from agents.substep_managers import collision_manager as _collision_manager
    
    def _collision_event(self, event: carla.CollisionEvent):
        """
        Callback function for the collision sensor.
        
        By default uses :py:func:`agents.substep_managers.collision_manager`.
        
        Executes Phases:
            - :py:class:`Phase.COLLISION | Phase.BEGIN<.Phase>`
            - :py:class:`Phase.COLLISION | Phase.END<.Phase>`
        """
        # https://carla.readthedocs.io/en/latest/python_api/#carla.CollisionEvent
        # e.g. setting ignore_vehicles to False, if it was True before.
        # do an emergency stop (in certain situations)
        self.execute_phase(Phase.COLLISION | Phase.BEGIN, prior_results=event)
        result = self._collision_manager(event)
        self.execute_phase(Phase.COLLISION | Phase.END, prior_results=result)
        
    # --------------------- Adding rules ------------------------

    def add_rule(self, rule : Rule, position:Union[int, None]=None):
        """
        Add a rule to the agent. The rule will be inserted at the given position.
        
        Args:
            rule : The rule to add
            position : 
                The position to insert the rule at. 
                If :python:`None` the rule list will be sorted by priority.
                Defaults to :python:`None`.
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

    
    def add_rules(self, rules : "Rule | Iterable[Rule]"):
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
        if isinstance(config, (AgentConfig, DictConfig)) and "rules" in config.keys():
            try:
                rule_list = config.rules
            except omegaconf.MissingMandatoryValue:
                logger.debug("`rules` key was missing, skipping rule addition.")
                return
        else:
            rule_list : List[RuleCreatingParameters] = config  # type: ignore[assignment]
        logger.debug("Adding rules from config:\n%s", OmegaConf.to_yaml(rule_list))
        for rule in rule_list:
            self.add_rules(rule_from_config(rule))  # each call could produce one or more rules
            
            self.add_rules(rule_from_config(rule)) # each call could produce one or more rules

    #  --------------------- Properties ------------------------
    
    @property
    def live_info(self) -> LiveInfo:
        return self.config.live_info

    @property
    def detection_matrix(self):
        """
        Returns :any:`DetectionMatrix.getMatrix` if the matrix is set.
        """
        if self._detection_matrix:
            return self._detection_matrix.getMatrix()
        
    # ------------------ Hazard ------------------ #
    
    @property
    def detected_hazards(self) -> Set[Hazard]:
        return self.ctx.detected_hazards
    
    @property
    def detected_hazards_info(self) -> Dict[Hazard, Any]:
        """
        Information about the detected hazards, e.g. severity.
        """
        return self.ctx.detected_hazards_info
    
    @detected_hazards.setter
    def detected_hazards(self, hazards : Set[Hazard]):
        if not isinstance(hazards, set):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("detected_hazards must be a set of Hazards.")
        self.ctx._detected_hazards = hazards  # noqa # pyright: ignore[reportPrivateUsage]
        
    # These have the same signature and can be used interchangeably
    discard_hazard = Context.discard_hazard
    add_hazard = Context.add_hazard
    has_hazard = Context.has_hazard
    
    #
    @property
    def current_traffic_light(self) -> "carla.TrafficLight | None":
        """Alias to :py:attr:`self._last_traffic_light <_last_traffic_light>`."""
        return self._last_traffic_light
    
    @current_traffic_light.setter
    def current_traffic_light(self, traffic_light : carla.TrafficLight):
        self._last_traffic_light = traffic_light
    
    @property
    def phase_results(self) -> Dict[Phase, Any]:
        """
        Retrieves :py:attr:`agent.ctx.phase_results <classes.rule.Context.phase_results>`
        
        Stores the results of the phases the agent has been in. 
        By default the keys are set to :any:`Context.PHASE_NOT_EXECUTED`.
        """
        return self.ctx.phase_results
    
    @property
    def active_blocking_rules(self) -> Set[BlockingRule]:
        """
        Blocking rules that are currently active and have taken over the agents loop.
        """
        return self._active_blocking_rules
    
    @property
    def _map(self) -> carla.Map:
        """Get the current map of the world.""" # Needed *only* for set_destination
        return CarlaDataProvider.get_map()
    
    # ------------------ 
            
    #@property
    #def ctx(self) -> Union[Context, None]:
    #    print("Getting Context", self._ctx())
    #    return self._ctx() # might be None

    # ------------------ Information functions ------------------ #

    def update_information(self, second_pass: bool=False):
        """
        Updates the information regarding the ego vehicle based on the surrounding world.
        
        Parameters:
            second_pass : *Internal usage* set to :python:`True` if this function is called a second
                time in the same tick, e.g. after a route update.
                
        See Also:
            - :py:attr:`information_manager`
            
        Executes the phases:
            - :py:class:`Phase.UPDATE_INFORMATION | Phase.BEGIN<.Phase>`
            - :py:class:`Phase.UPDATE_INFORMATION | Phase.END<.Phase>`
        """
        self.execute_phase(Phase.UPDATE_INFORMATION | Phase.BEGIN, prior_results=None)
        self._update_information(second_pass=second_pass)
        self.execute_phase(Phase.UPDATE_INFORMATION | Phase.END, prior_results=None)
    
    def _update_information(self, *, second_pass: bool=False):
        """
        This method updates the information regarding the ego
        vehicle based on the surrounding world.
        
        second_pass = True will skip some calculations, 
        especially useful if a second call to _update_information is necessary in the same tick.
        
        Assumes: second_pass == True => agent.done() == False
        
        Note:
            Does not execute any Phase.
        """
        # --------------------------------------------------------------------------
        # Information that is CONSTANT DURING THIS TICK and INDEPENDENT OF THE ROUTE
        # --------------------------------------------------------------------------
        if not second_pass:
            if self._debug:
                if not self._lights_list and len(CarlaDataProvider._traffic_light_map.keys()):  # pyright: ignore[reportPrivateUsage]
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
            
            self.traffic_lights_nearby = information.traffic_lights_nearby
            
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
            
            #  ----- Follow speed limits -------
            # NOTE: This is once again set in the local planner, but only on the Context config!
            if self.config.speed.follow_speed_limits:
                self.config.speed.target_speed = self.config.live_info.current_speed_limit
            
            # NOTE: This is the direction used by the planner in the *last* step.
            self.live_info.executed_direction = self._local_planner.target_road_option
        
        assert self.live_info.executed_direction == self._local_planner.target_road_option, "Executed direction should not change."
        
        # -------------------------------------------------------------------
        # Information that NEEDS TO BE UPDATED AFTER a plan / ROUTE CHANGE.
        # -------------------------------------------------------------------
        if not self.done():
            # NOTE: This should be called after 
            self.live_info.incoming_waypoint, self.live_info.incoming_direction = self._local_planner.get_incoming_waypoint_and_direction(  # pyright: ignore[reportAttributeAccessIssue]
                steps=self._look_ahead_steps)
        else:
            assert second_pass == False, "In the second pass the agent should have replanned and agent.done() should be False"
            # Assumes second_pass is False
            # Queue is empty
            self.live_info.incoming_waypoint = None
            self.live_info.incoming_direction = RoadOption.VOID
        
        # Information that requires updated waypoint and route information:
        self.live_info.is_taking_turn = self.is_taking_turn()
        self.live_info.is_changing_lane = self.is_changing_lane()
            
        #logger.debug(f"Incoming Direction: {str(self.live_info.incoming_direction):<20} - Second Pass: {second_pass}")

        # RSS
        # todo uncomment if agent is created after world model
        #self.rss_set_road_boundaries_mode() # in case this was adjusted during runtime. # TODO: maybe implement this update differently. As here it is called unnecessarily often.
        
        if self._debug:
            OmegaConf.to_container(self.live_info, resolve=True, throw_on_missing=True)
    
    def is_taking_turn(self) -> bool:
        """Checks if the agent is taking a turn in a few steps"""
        return self.live_info.incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)
    
    def is_changing_lane(self) -> bool:
        """Checks if the agent is changing lanes in a few steps"""
        return self.live_info.incoming_direction in (RoadOption.CHANGELANELEFT, RoadOption.CHANGELANERIGHT)
    
            
    # ------------------ Step & Loop Logic ------------------ #
    
    def execute_phase(self, phase : Phase, *, prior_results: Any, update_controls:Optional[carla.VehicleControl]=None) -> Context:
        """
        Sets the current phase of the agent and executes all rules that are associated with it.
        
        Parameters:
            phase : The phase to execute.
            prior_results : The results of the previous phase, e.g. :py:attr:`detected_hazards`.
            update_controls : Optionally controls that should be used from now onward.
        """
        normal_next = self.current_phase.next_phase() # sanity checking if everything is correct
        if self._validate_phases:
            assert (normal_next == Phase.USER_CONTROLLED 
                    or phase == normal_next 
                    or phase & Phase.EXCEPTIONS 
                    or phase & Phase.USER_CONTROLLED),\
                    f"Phase {phase} is not the next phase of {self.current_phase} or an exception phase. Expected {normal_next}"
        
        self.current_phase = phase # set next phase
        
        if update_controls is not None:
            self.set_control(update_controls)
        self.ctx.prior_result = prior_results
        self.ctx.phase_results[phase] = prior_results
        
        rules_to_check = self.rules.get(phase, ()) # use get if a custom phase is added, without a rule
        try:
            for rule in rules_to_check: # todo: maybe dict? grouped by phase?
                assert self.current_phase in rule.phases, f"Current phase {self.current_phase} not in Rule {rule.phases}" # TODO remove:
                rule(self.ctx)
                # NOTE: Blocking rules can change the and above assertion will fail.
                if phase != self.current_phase:
                    logger.warning("Phase was changed by rule %s to %s. "
                        "Resting self.current_phase to %s. "
                        "To prevent his raise an exception in the rule or adjust the phase.",
                        rule, self.current_phase, phase)
                    self.current_phase = phase
                    
        except NoFurtherRulesException:
            pass
        except omegaconf.ReadonlyConfigError:
            print("WARNING: A action likely tried to change `ctx.config` which is non-permanent. Use `ctx.agent.config.` instead.")
            raise
        return self.ctx
    
    def _plan_path_phase(self, *, second_pass:bool, debug:bool=False):
        try:
            self.execute_phase(Phase.PLAN_PATH | Phase.BEGIN, prior_results=None)
            # User defined action
            # TODO: when going around corners / junctions and the distance between waypoints is too big,
            # We should replan and and make a more fine grained plan, to stay on the road.
            self.execute_phase(Phase.PLAN_PATH | Phase.END, prior_results=None)
        except UpdatedPathException as e:
            if second_pass:
                logger.warning("UpdatedPathException was raised in the second pass. This should not happen: %s. Restrict your rule on ctx.second_pass.", e)
            return self.run_step(debug, second_pass=True)
        return None
        
    def _make_context(self, last_context : Union[Context, None], **kwargs: Any) -> Context:
        """Creates a new context object for the agent at the start of a step."""
        if last_context is not None:
            del last_context.last_context
        ctx = Context(agent=self, last_context=last_context, **kwargs)
        self.ctx = ctx
        return ctx
    
    def __call__(self, debug: bool=False) -> carla.VehicleControl:
        """Calculates the next vehicle control object."""
        return self.run_step(debug, second_pass=False) # debug should be positional!
                
    # Python 3.8+ add / for positional only arguments
    def run_step(self, debug: bool=False, second_pass: bool=False) -> carla.VehicleControl:
        """
        Calculates the next vehicle control object.
        
        Arguments:
            debug : Whether to enable debug mode.
                This prints some more information and debugdrawings.
            second_pass : **Internal usage** set to :python:`True`
                if this function is called a second time, e.g. after a route update.
        
        Warning:
            To be compatible with the :py:class:`.LunaticChallenger`, **always pass** :code:`debug` **as a positional argument**,
            or use the :py:meth:`__call__` method.
        """
        
        if not second_pass:
            ctx = self._make_context(last_context=self.ctx)
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
                return self.run_step(debug, second_pass=True) # NOTE! For child classes like the leaderboard agent this calls the higher level run_step.
            
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
                planned_control = self.get_control() # type: carla.VehicleControl # type: ignore[assignment]
            
            # Other Exceptions
            
            except SkipInnerLoopException as skip:
                self.set_control(skip.planned_control)
                self.current_phase = Phase.USER_CONTROLLED
                planned_control = skip.planned_control
            except UserInterruption:
                raise
            except UpdatedPathException as e:
                if second_pass > 5:
                    logger.warning("UpdatedPathException was raised more than %s times. "
                                   "Warning: This might be an infinite loop.", second_pass)
                elif second_pass > 50:
                    raise RecursionError("UpdatedPathException was raised more than 50 times. "
                                         "Assuming an infinite loop and terminating")
                else:
                    logger.warning("UpdatedPathException was raised in the inner step, this should be done in Phase.PLAN_PATH ", e)
                return self.run_step(second_pass=int(second_pass)+1) # type: ignore
            except LunaticAgentException as e:
                if self.ctx.control is None:
                    raise ValueError("A VehicleControl object must be set on the agent when %s is "
                                     "raised during `._inner_step`" % type(e).__name__) from e
                planned_control = self.get_control() # type: ignore[assignment]
            # assert ctx.control
            
            # ----------------------------
            # No known Phase multiple exit points
            # ----------------------------
            
            # ----------------------------
            # Phase RSS - Check RSS
            # ----------------------------
            
            ctx = self.execute_phase(Phase.RSS_EVALUATION | Phase.BEGIN, 
                                     prior_results=None, 
                                     update_controls=planned_control)
            if AD_RSS_AVAILABLE and self.config.rss and self.config.rss.enabled:
                rss_updated_controls = self._world_model.rss_check_control(ctx.control) # type: ignore[arg-type]
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
        
        planned_control = self.ctx.control # type: carla.VehicleControl # type: ignore[assignment]
        planned_control.manual_gear_shift = False
        return self.get_control()          # type: ignore[return-value]

    @must_clear_hazard
    @result_to_context("control")
    def _inner_step(self, debug:bool=False) -> carla.VehicleControl:
        """
        This is is the internal function to provide the next control object for
        the agent; it should run every tick.
        
        Raises:
            EmergencyStopException: If :py:attr:`detected_hazards` is not empty when the 
                function returns.
            
        :meta public:
        """
        self.debug = debug

        # ----------------------------
        # Phase 2 - Detection of Pedestrians and Traffic Lights
        # ----------------------------

        # Detect hazards
        # phases are executed in detect_hazard
        # > Phase.DETECT_TRAFFIC_LIGHTS | Phase.BEGIN # phases executed inside
        pedestrians_and_tlight_hazard = self.detect_hazard()
        # > Phase.DETECT_PEDESTRIANS | Phase.END

        # Pedestrian avoidance behaviors
        # currently doing either emergency (detect_hazard) stop or nothing 
        if self.detected_hazards:

            # ----------------------------
            # Phase Hazard Detected (traffic light or pedestrian)
            # If no Rule with Phase.EMERGENCY | BEGIN clears pedestrians_or_traffic_light
            # An EmergencyStopException is raised
            # ----------------------------
            self.react_to_hazard(pedestrians_and_tlight_hazard) # Optional[NoReturn]
    
        # -----------------------------
        # Phase Detect Static Obstacles
        # -----------------------------
        
        self.execute_phase(Phase.DETECT_STATIC_OBSTACLES | Phase.BEGIN, prior_results=None)
        static_obstacle_detection_result = self.detect_obstacles_in_path(self.static_obstacles_nearby)
        if static_obstacle_detection_result.obstacle_was_found:
            self.current_states[AgentState.BLOCKED_BY_STATIC] += 1 
            # Must plan around it
            self.add_hazard(Hazard.STATIC_OBSTACLE)
        else:
            self.current_states[AgentState.BLOCKED_BY_STATIC] = 0
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
            control = self.car_following_behavior(*vehicle_detection_result)  # type: ignore[arg-type]
            # NOTE: might throw EmergencyStopException
            self.execute_phase(Phase.CAR_DETECTED | Phase.END, update_controls=control, prior_results=vehicle_detection_result)
            return self.get_control()  # type: ignore[return-value]
        
        #TODO: maybe new phase instead of END or remove CAR_DETECTED and handle as rules (maybe better)
        self.execute_phase(Phase.DETECT_CARS | Phase.END, prior_results=None) # NOTE: avoiding tailgate here
        
        # Intersection behavior
        # NOTE: is_taking_turn <- incoming_direction in (RoadOption.LEFT, RoadOption.RIGHT)
        if self.live_info.incoming_waypoint.is_junction and self.is_taking_turn():  # pyright: ignore[reportOptionalMemberAccess]

            # ----------------------------
            # Phase Turning at Junction
            # ----------------------------

            self.execute_phase(Phase.TURNING_AT_JUNCTION | Phase.BEGIN, prior_results=None)
            control = self._calculate_control(debug=debug)
            self.execute_phase(Phase.TURNING_AT_JUNCTION | Phase.END, update_controls=control, prior_results=None)
            return self.get_control() # type: ignore[return-value]

        # ----------------------------
        # Phase 4 - Plan Path normally
        # ----------------------------
        
        # Normal behavior
        self.execute_phase(Phase.TAKE_NORMAL_STEP | Phase.BEGIN, prior_results=None)
        control = self._calculate_control(debug=debug)
        self.execute_phase(Phase.TAKE_NORMAL_STEP | Phase.END, prior_results=None, update_controls=control)

        # Leave loop and apply controls outside 
        return self.get_control() # type: ignore[return-value]
    
    def _calculate_control(self, debug: bool=False):
        """
        Plan the next step of the agent. This will execute the local planner
        to retrieve the next control fitting the current path and settings.
        
        Note:
            This is the innermost function of the agents run_step function.
            It should be called each step to acquire a desired control object.
            Use this function inside rules if a control object is desired.
            
            **[Context.get_or_calculate_control](#Context.get_or_calculate_control) 
            is a safer alternative to this function**
        
        Warning:
            If you do not use this function in a [`BlockingRule`](#BlockingRule)
            you should raise a `SkipInnerLoopException` or `ContinueLoopException` 
            else the planned path will skip a waypoint.
            
        Warning:
            This function only calculates and returns the control object directly. 
            **It does not set the :py:attr:`agent/ctx.control <control>` attribute which is the one
            the agent uses in [`apply_control`](#apply_control) to apply the final controls.**
        """
        if self.ctx.control is not None:
            logger.error("Control was set before calling _calculate_control. This might lead to unexpected behavior.")
        
        return self._local_planner.run_step(debug)

    def parse_keyboard_input(self, allow_user_updates:bool =True, 
                             *, control: Optional[carla.VehicleControl]=None) -> None:
        """
        Parse the current user input and allow manual updates of the controls.
        
        Args:
            allow_user_updates: If :python:`True`, the user can update the controls manually.
                Otherwise only the normal hotkeys do work.
        
        Executes Phases:
            - :py:class:`Phase.APPLY_MANUAL_CONTROLS | Phase.BEGIN <classes.constants.Phase>`
            - :py:class:`Phase.APPLY_MANUAL_CONTROLS | Phase.END <classes.constants.Phase>`
        """
        planned_control = control or self.get_control()
        self.execute_phase(Phase.APPLY_MANUAL_CONTROLS | Phase.BEGIN, prior_results=planned_control)
        
        # Controls can be updated inplace by the user.        
        if self._world_model.controller.parse_events(planned_control if allow_user_updates else carla.VehicleControl()): # pyright: ignore[reportOptionalMemberAccess]
            print("Exiting by user input.")
            raise UserInterruption("Exiting by user input.")
       
        self.execute_phase(Phase.APPLY_MANUAL_CONTROLS | Phase.END, prior_results=None)
    
    def apply_control(self, control: Optional[carla.VehicleControl]=None):
        """
        Applies the control to the agent's actor.
        Will execute the :py:class:`Phase.EXECUTION | Phase.BEGIN <classes.constants.Phase>` 
        and :py:class:`Phase.EXECUTION | Phase.END <classes.constants.Phase>` phases.
        
        Note:
            The final control object that is applied to the agent's actor
            is stored in the :py:attr:`ctx.control <ctx>` attribute.
        
        Raises ValueError:
            If the control object is not set, i.e. :py:meth:`get_control` returns :python:`None`.
        """
        if control is None:
            control = self.get_control()
            if control is None:
                raise ValueError("The agent has not yet performed a step this tick "
                                 "and has no control object was passed.")
        if self.current_phase != Phase.EXECUTION | Phase.BEGIN:
            self.execute_phase(Phase.EXECUTION | Phase.BEGIN, prior_results=control, update_controls=control)
        else:
            logger.debug("Agent is already in execution phase.")
        # Set automatic control-related vehicle lights
        final_control : carla.VehicleControl = self.get_control()  # type: ignore[assignment]
        self._update_lights(final_control)
        self._vehicle.apply_control(final_control)
        self.execute_phase(Phase.EXECUTION | Phase.END, prior_results=final_control)
    
    # ------------------ Hazard Detection & Reaction ------------------ #

    from agents.substep_managers import detect_traffic_light # -> TrafficLightDetectionResult
    traffic_light_manager = detect_traffic_light 
    """Alias of :py:meth:`detect_traffic_light`"""
    
    def detect_hazard(self) -> Set[Hazard]:
        """
        Checks for red traffic lights and pedestrians in the agents path.
        
        If :py:attr:`.LunaticAgentSettings.obstacles.detect_yellow_tlights` is set to :python:`True`,
        then yellow traffic lights will also be regarded as a hazard that can trigger an 
        :py:exc:`EmergencyStopException` in :py:meth:`react_to_hazard` that is executed after this
        function.
        """
        # Red lights and stops behavior

        self.execute_phase(Phase.DETECT_TRAFFIC_LIGHTS | Phase.BEGIN, prior_results=None)
        tlight_detection_result: TrafficLightDetectionResult = self.detect_traffic_light()
        if tlight_detection_result.traffic_light_was_found:
            if tlight_detection_result.traffic_light.state == carla.TrafficLightState.Red:  # pyright: ignore[reportOptionalMemberAccess]
                self.add_hazard(Hazard.TRAFFIC_LIGHT_RED)
            else: # NOTE: self.config.obstacles.detect_yellow_tlights must be True
                self.add_hazard(Hazard.TRAFFIC_LIGHT_YELLOW, HazardSeverity.WARNING)
            
            #assert self.live_info.next_traffic_light.id == tlight_detection_result.traffic_light.id, "Next assumed traffic light should be the same as the detected one." # TEMP
            
            # NOTE next tlight is the next bounding box and might not be the next "correct" one
            # self.live_info.next_traffic_light.id != tlight_detection_result.traffic_light.id:
            
        self.execute_phase(Phase.DETECT_TRAFFIC_LIGHTS | Phase.END, prior_results=tlight_detection_result)

        # Pedestrian avoidance behaviors
        self.execute_phase(Phase.DETECT_PEDESTRIANS | Phase.BEGIN, prior_results=None)
        is_dangerous, detection_result = self.pedestrian_avoidance_behavior()
        if detection_result.obstacle_was_found:
            if is_dangerous:
                self.add_hazard(Hazard.PEDESTRIAN, hazard_level=HazardSeverity.EMERGENCY)
            else:
                self.add_hazard(Hazard.PEDESTRIAN, hazard_level=HazardSeverity.WARNING)
                # NOTE: its a flag, could pack all in one bin
                # Pro: easier to check
                # Con: when to remove other states like warning
                # Make it a dict with the state as key and the detection result as value!
        self.execute_phase(Phase.DETECT_PEDESTRIANS | Phase.END, prior_results=(is_dangerous, detection_result))
        
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
            raise EmergencyStopException(self.detected_hazards)
        logger.info("Hazards have been cleared.")
        
    # ------------------ Behaviors ------------------ #
    # TODO: Section needs overhaul -> turn into rules

    def pedestrian_avoidance_behavior(self) -> tuple[bool, ObstacleDetectionResult]:
        """
        Detects pedestrians in the agents path.
        
        Returns:
            A tuple containing a boolean indicating if the detected pedestrian is dangerous
            and the detection result.
        """
        # note ego_vehicle_wp is the current waypoint self._current_waypoint
        detection_result = self.detect_obstacles_in_path(self.walkers_nearby)
        if (detection_result.obstacle_was_found
            and (detection_result.distance - max(detection_result.obstacle.bounding_box.extent.y,  # pyright: ignore[reportOptionalMemberAccess]
                                                 detection_result.obstacle.bounding_box.extent.x)  # pyright: ignore[reportOptionalMemberAccess]
                                           - max(self._vehicle.bounding_box.extent.y, 
                                                 self._vehicle.bounding_box.extent.x)
            < self.config.distance.emergency_braking_distance)):
            #print("Detected walker", detection_result.obstacle)
            # NOTE: should slow down here
            return True, detection_result
        # NOTE detected but not stopping -> ADD avoidance behavior
        elif detection_result.obstacle_was_found:
            logger.debug("Detected a pedestrian but determined no intervention necessary (too far away).")
        return False, detection_result
        
    def car_following_behavior(self, 
                               vehicle_detected: bool, 
                               vehicle: carla.Actor, 
                               distance: float) -> carla.VehicleControl:
        """
        Parameters:
            Must match :py:class:`.ObstacleDetectionResult`
        
        Assumes:
            - That an obstacle was detected:
                :py:attr:`vehicle_detected<.ObstacleDetectionResult.obstacle_was_found> is True and
                :py:attr:`vehicle<.ObstacleDetectionResult.obstacle>` is the detected vehicle.
        """
        exact_distance = distance - max(vehicle.bounding_box.extent.y, vehicle.bounding_box.extent.x) - max(
            self._vehicle.bounding_box.extent.y, self._vehicle.bounding_box.extent.x)

        if exact_distance < self.config.distance.emergency_braking_distance:
            # Note: If the passed set is not cleared by a Phase.EMERGENCY | Phase.BEGIN rule, 
            # an EmergencyStopException is raised.
            self.add_hazard(Hazard.CAR)
            self.react_to_hazard(hazard_detected={Hazard.CAR}) # Optional[NoReturn]
        controls = self.car_following_manager(vehicle, exact_distance)
        return controls

    # ------------------ External Helpers ------------------ #

    # Moved outside of the class for organization
    from agents.tools.lunatic_agent_tools import detect_obstacles_in_path
    from agents.substep_managers import car_following_manager # -> carla.VehicleControl
    from agents.substep_managers import emergency_manager
    
    # Subfunction of traffic_light_manager. In traffic_light_manager the parameters are chosen automatically
    # which is why traffic_light_manager should be used instead.
    # Kept for backwards compatibility and possible future use.
    from agents.substep_managers.traffic_light import affected_by_traffic_light

    # ----

    #@override
    def add_emergency_stop(self, control: carla.VehicleControl, reasons:"Optional[set[str]]"=None) -> carla.VehicleControl:
        """
        Modifies the control values to perform an emergency stop.
        The steering remains unchanged to avoid going out of the lane during turns.

        :param control: (carla.VehicleControl) control to be modified
        :param enable_random_steer: (bool, optional) Flag to enable random steering
        """
        return self.emergency_manager(reasons=reasons, control=control) # type: ignore[arg-type]
    
    def lane_change(self, 
                    direction: Literal['left', 'right'], 
                    same_lane_time: float=0, 
                    other_lane_time: float=0, 
                    lane_change_time: float=2,
                    *,
                    check: bool=False):
        """
        Changes the path so that the vehicle performs a lane change.
        Use 'direction' to specify either a 'left' or 'right' lane change,
        and the time parameters to fine tune the maneuver.
        
        Steps for the lane change:
            1. **same_lane_time** seconds in the same lane.
            2. **lane_change_time** seconds to reach the other lane.
            3. **other_lane_time** seconds to stay in the other lane.
        
        Parameters:
            waypoint: The starting waypoint.
            direction: The direction of the lane change, either 'left' or 'right'.
                Defaults to 'left'.
            same_lane_time: The time to follow the same lane before the lane change.
            other_lane_time: The time to follow the other lane after the lane change.
            lane_change_time: The time to reach the center of the last lane.
                A low value will make a fast lane change, while a high value will make slow lane change.
            check: If :python:`True`, the function will check if the lane change is possible, i.e.
                if there is a lane of :py:class:`carla.LaneType.Driving <carla.LaneType>` in 
                the desired direction. Otherwise it can change to other lane types as well.
                Defaults to :code:`False`.
                
        See Also:
            - :py:func:`agents.tools.lunatic_agent_tools.generate_lane_change_path`
            - :py:meth:`set_global_plan`
        """
        speed = self.live_info.current_speed / 3.6 # m/s
        # This is a staticfunction from BasicAgent function
        path: list[tuple[carla.Waypoint, RoadOption]] = self._generate_lane_change_path(
            self._current_waypoint, # NOTE: Assuming exact_waypoint
            direction,
            same_lane_time * speed, # get direction in meters t*V
            other_lane_time * speed,
            lane_change_time * speed,
            check=check,
            lane_changes=1,     # changes only one lane
            step_distance= self.config.planner.sampling_resolution
        )
        if not path:
            logger.info("Ignoring the lane change as no path was found")

        # Change path to take now
        super(LunaticAgent, self).set_global_plan(path)
        # TODO: # CRITICAL: Keep old global plan if it is some end goal -> Restore it.
        
    # TODO: Use generate_lane_change_path to finetune 
    def make_lane_change(self, 
                         order: Sequence[Literal["left", "right"]]=["left", "right"], 
                         up_angle_th: int=180, 
                         low_angle_th: int=0) -> "None | Literal[True]":
        """
        Move to the left/right lane if possible

        Args:
            order : The order in
                which the agent should try to change lanes. If a single string is given, the agent
                will try to change to that lane.
            up_angle_th : The angle threshold for the upper limit of obstacle detection in the other lane.
                Default is 180 degrees, meaning that the agent will detect obstacles ahead.
            low_angle_th : The angle threshold for the lower limit of obstacle detection in the other lane.
                Default is 0 degrees, meaning that the agent will detect obstacles behind.
            
        Assumes:
            - :python:`(self.config.live_info.incoming_direction == RoadOption.LANEFOLLOW \
                and not waypoint.is_junction and self.config.live_info.current_speed > 10)`
            - :python:`check_behind.obstacle_was_found and self.config.live_info.current_speed < get_speed(check_behind.obstacle)`
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
                raise ValueError("Direction must be 'left' or 'right', was %s" % direction)
            if (can_change # other_wpt is not None
                and lanes_have_same_direction(waypoint, other_wpt)  # type: ignore[arg-type]
                and other_wpt.lane_type == carla.LaneType.Driving):  # type: ignore[attr-defined]
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
                    self.set_destination(end_location=other_wpt.transform.location,  # type: ignore[arg-type]
                                         start_location=end_waypoint.transform.location, clean_queue=True)
                    return True
        
    # ------------------ Other Function ------------------ #
    
    def _update_lights(self, vehicle_control : carla.VehicleControl):
        """Updates the light of the vehicle in the simulation."""
        current_lights: carla.VehicleLightState = self._vehicle_lights
        if vehicle_control.brake:
            current_lights |= carla.VehicleLightState.Brake
        else:  # Remove the Brake flag
            current_lights &= carla.VehicleLightState.All ^ carla.VehicleLightState.Brake
        if vehicle_control.reverse:
            current_lights |= carla.VehicleLightState.Reverse
        else:  # Remove the Reverse flag
            current_lights &= carla.VehicleLightState.All ^ carla.VehicleLightState.Reverse
        if current_lights != self._vehicle_lights:  # Change the light state only if necessary
            self._vehicle_lights = current_lights
            self._vehicle.set_light_state(carla.VehicleLightState(self._vehicle_lights))

    def _render_detection_matrix(self, display:"pygame.Surface", **options: Unpack["DetectionMatrix.RenderOptions"]):
        """
        Attention:
            **options** must 
        """
        if self._detection_matrix:
            # options should align with CameraConfig.DetectionMatrixHudConfig
            self._detection_matrix.render(display, **options)
            
            
    def verify_settings(self, config: Optional[LunaticAgentSettings] =None, *, 
                        verify_dataclass: Union["type[AgentConfig]", bool] =True, 
                        strictness: Literal[-1, 0, 1, 2, 3, 4]=0):
        """
        Verifies the settings of the LunaticAgent.
        Foremost this checks if the :py:obj:`.planner.dt` value has been set
        to the speed of the world ticks in synchronous mode.
        Secondly if :python:`verify_dataclass=True` or a different AgentConfig class is provided, 
        it will check for correct type usage.

        Args:
            config: The configuration to verify. 
                If not provided, the agent's default configuration will be used. 
                Defaults to :code:`None`.
            verify_dataclass: 
                Determines the dataclass to use for verification. 
                If :python:`True`, the :py:attr:`.BASE_SETTINGS` dataclass will be used.
                See :py:meth:`AgentConfig.check_config` for more details.
                Defaults to True.
            strictness: 
                The strictness level for :py:meth:`AgentConfig.check_config`. 
                Defaults to :python:`3`.

        Raises:
            TypeError: If **verify_dataclass** is not a valid AgentConfig subclass or True.
            MissingMandatoryValue: If :python:`config.planner.dt` is not present 
                or not a :python:`float`
        """
        config = config or self.config
        
        if self._world_model.world_settings.synchronous_mode:
            # Assure that dt is set
            if isinstance(config, DictConfig):
                OmegaConf.select(config,
                    "planner.dt",
                    throw_on_missing=True
                )
            elif not isinstance(config.planner.dt, float):
                from omegaconf import MissingMandatoryValue
                raise MissingMandatoryValue("`config.planner.dt` needs to be set to a value. "
                                            "Cannot be:", type(config.planner.dt), config.planner.dt)
        
        if strictness < 0:
            return
        
        # NOTE: Below is experimental and might fail as the config at this point has already been setup
    
        from agents.tools import config_creation  # noqa
        _old = config_creation._WARN_LIVE_INFO    # pyright: ignore[reportPrivateUsage]
        config_creation._WARN_LIVE_INFO = False   # pyright: ignore[reportPrivateUsage]

        if verify_dataclass:
            if verify_dataclass is True:
                dataclass = self.BASE_SETTINGS
            elif issubclass(verify_dataclass, AgentConfig):  # pyright: ignore[reportUnnecessaryIsInstance]
                dataclass = verify_dataclass
            else:
                raise TypeError("`verify_dataclass` must be a `AgentConfig` or `True` to select the BASE_SETTINGS ")
            dataclass.check_config(config, dataclass.get("strict_config", strictness), as_dict_config=True)

        config_creation._WARN_LIVE_INFO = _old   # pyright: ignore[reportPrivateUsage]

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
    
    def _init_detection_matrix(self):
        if self.config.detection_matrix and self.config.detection_matrix.enabled:
            if self.config.detection_matrix.sync and self._world_model.world_settings.synchronous_mode:
                self._detection_matrix = DetectionMatrix(self._vehicle, self._world_model.world)
            else:
                self._detection_matrix = AsyncDetectionMatrix(self._vehicle, self._world_model.world)
            self._detection_matrix.start()
        else:
            self._detection_matrix = None
        self._road_matrix_counter = 0
        
    if READTHEDOCS or TYPE_CHECKING:
        # From the parent class, but without type-hints
        def set_destination(self,
                            end_location: carla.Location, 
                            start_location: Optional[carla.Location]=None, 
                            clean_queue:bool=True) -> None:
            ...
    
    def set_vehicle(self, vehicle:carla.Actor) -> None:
        """
        Set the vehicle for the agent (experimental if applied a second time)
        
        :meta private:
        """
        self._vehicle = assure_type(carla.Vehicle, vehicle)
        # do not register same id twice
        if all(actor.id != vehicle.id for actor in CarlaDataProvider._actor_velocity_map):  # pyright: ignore[reportPrivateUsage]
            try:
                CarlaDataProvider.register_actor(vehicle, vehicle.get_transform())  # pyright: ignore[reportUnknownMemberType]
            except KeyError:
                pass
        else:
            # Exchange the key for a faster lookup
            for key in CarlaDataProvider._actor_velocity_map:  # pyright: ignore[reportPrivateUsage]
                if key.id == vehicle.id:
                    break
            else:
                # This does not happen because of the first if condition
                raise ValueError("The vehicle was not registered in the actor map.")
            CarlaDataProvider._actor_velocity_map[vehicle] = CarlaDataProvider._actor_velocity_map.pop(key)    # pyright: ignore[reportPrivateUsage]
            CarlaDataProvider._actor_transform_map[vehicle] = CarlaDataProvider._actor_transform_map.pop(key)  # pyright: ignore[reportPrivateUsage]
            CarlaDataProvider._actor_location_map[vehicle] = CarlaDataProvider._actor_location_map.pop(key)    # pyright: ignore[reportPrivateUsage]
            
        self._init_detection_matrix()
        self._local_planner = DynamicLocalPlannerWithRss(self, 
                                                         map_inst=CarlaDataProvider.get_map(), 
                                                         world=CarlaDataProvider.get_world(), 
                                                         rss_sensor=self._world_model.rss_sensor)
    
    #@override 
    def set_target_speed(self, speed : float) -> None:
        """
        Changes the target speed of the agent
            :param speed (float): target speed in Km/h
        """
        if self.config.speed.follow_speed_limits:
            print("WARNING: The max speed is currently set to follow the speed limits. "
                  "Use 'follow_speed_limits' to deactivate this")
        self.config.speed.target_speed = speed # shared with planner

    def follow_speed_limits(self, value:bool=True) -> None:
        """
        If active, the agent will dynamically change the target speed according to the speed limits
        
        Arguments:
            value: Whether to activate this behavior
        """
        self.config.speed.follow_speed_limits = value

    def ignore_traffic_lights(self, active: bool=True) -> None:
        """(De)activates the checks for traffic lights"""
        self.config.obstacles.ignore_traffic_lights = active

    def ignore_stop_signs(self, active: bool=True) -> None:
        """(De)activates the checks for stop signs"""
        self.config.obstacles.ignore_stop_signs = active

    def ignore_vehicles(self, active: bool=True) -> None:
        """(De)activates the checks for stop signs"""
        self.config.obstacles.ignore_vehicles = active
        
    def rss_set_road_boundaries_mode(self, 
                                     road_boundaries_mode: Optional[
                                         Union[bool, RssRoadBoundariesModeAlias]]=None) -> None:
        if road_boundaries_mode is None:
            road_boundaries_mode = self.config.rss.use_stay_on_road_feature
        self._world_model.rss_set_road_boundaries_mode(road_boundaries_mode)

    
    # ------------------ Overwritten & Outsourced functions ------------------ #
    
    from agents.tools.lunatic_agent_tools import max_detection_distance

    # Compatibility with BehaviorAgent interface
    @replace_with(agents.tools.lunatic_agent_tools.detect_vehicles)
    def _vehicle_obstacle_detected(_):
        """
        **Unused**, kept for compatibility with BehaviorAgent interface.
        Substituted by :py:func:`agents.tools.lunatic_agent_tools.detect_vehicles`.
        """
 
    # Staticmethod that we outsource
    @staticmethod
    @replace_with(agents.tools.lunatic_agent_tools.generate_lane_change_path)
    def _generate_lane_change_path(_):
        """Substituted by :py:func:`agents.tools.lunatic_agent_tools.generate_lane_change_path`"""

    # NOTE: the original pedestrian_avoid_manager is still usable
    def pedestrian_avoid_manager(self, waypoint) -> NoReturn:  # noqa # type: ignore
        """
        This function was replaced by ", substep_managers.pedestrian_detection_manager
        
        :meta private:
        """
        raise NotImplementedError("This function was replaced by ", substep_managers.pedestrian_detection_manager)

    #@override
    def collision_and_car_avoid_manager(self, waypoint) -> NoReturn:  # noqa # type: ignore
        """
        This function was split into detect_obstacles_in_path and car_following_manager
        
        :meta private:
        """
        raise NotImplementedError("This function was split into detect_obstacles_in_path and car_following_manager")
    
    #@override
    def _tailgating(self, waypoint, vehicle_list) -> NoReturn:  # noqa # type: ignore
        raise NotImplementedError("Tailgating has been implemented as a rule")

    #@override
    def emergency_stop(self) -> NoReturn:
        """
        :meta private:
        """
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
    
    # ---------------- Cleanup ------------------- #

    def _destroy_sensor(self):
        if self._detection_matrix:
            self._detection_matrix.stop()
            self._detection_matrix = None
        if self._collision_sensor:
            self._collision_sensor.destroy()
            self._collision_sensor = None  # type: ignore[assignment]
            
    def destroy(self):
        """Resets attributes and destroys helpers like the :py:class:`.DetectionMatrix`."""
        self._destroy_sensor()
        self._world_model = None    # type: ignore[assignment]
        self._world = None          # type: ignore[assignment]
        if self.ctx:
            self.ctx.agent = None   # type: ignore[assignment]
        self.ctx = None             # type: ignore[assignment]
        try:
            self.all_vehicles.clear()
            self.vehicles_nearby.clear()
            self.all_walkers.clear()
            self.walkers_nearby.clear()
        except AttributeError:
            pass
        
    def __del__(self):
        try:
            self.destroy()
        except Exception:
            pass
