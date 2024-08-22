"""
Aim of this module is to provide a less convoluted access to information,
i.e. distill the information from the data and return high level information
"""

from __future__ import annotations

# todo: maybe find another name for this module

from fnmatch import fnmatch
from functools import wraps
from typing import (Any, ClassVar, TYPE_CHECKING, 
                    NamedTuple, Optional, Union, Dict, List, Callable, TypeVar)
from typing_extensions import Literal, Self, ParamSpec, Concatenate
from cachetools import cached
import carla

from launch_tools import CarlaDataProvider
from agents.tools.logging import logger
from classes.constants import AgentState

if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent

_T = TypeVar("_T")
_P = ParamSpec("_P")

DRIVING_SPEED_THRESHOLD = 0.05 # m/s >= check
STOPPED_SPEED_THRESHOLD = 0.05 # m/s < check

class InformationManager:
    """
    Tracks global information, e.g. all actors, traffic lights, etc. as well as
    agent specific information, e.g. current speed, current location, and nearby actors in
    relation to the agent.
    
    Tip:
        global information is attributed by :py:obj:`ClassVar` and :py:obj:`staticmethod` and is
        shared across all instances, this information is constant for the current tick.
    """
    
    _tick : ClassVar[int] = 0
    """Current tick to not double class :py:meth:`global_tick`"""
    
    # Instance Variables
    relevant_traffic_light : Union[carla.TrafficLight, None] = None
    """Result of :py:meth:`.CarlaDataProvider.get_next_traffic_light`"""
    
    relevant_traffic_light_distance : float = float('inf')
    """
    Distance to the :py:attr:`relevant_traffic_light`
    Is float('inf') if :py:attr:`relevant_traffic_light` is None.
    """
    
    _relevant_traffic_light_location : carla.Location = None
    
    state_counter: Dict[AgentState, int]
    """
    Tracks different :py:class:`AgentState` and the amount of ticks the agent is in this state.
    """
    
    _vehicle_speed : float # m/s
    
    gathered_information : "InformationManager.Information"
    """:py:class:`.InformationManager.Information` gathered during :py:meth:`tick`"""
    
    # Class & Global Variables
    vehicles : ClassVar["list[carla.Vehicle]"]
    """List of all tracked vehicles"""
    
    walkers : ClassVar["list[carla.Walker]"]
    """List of all tracked pedestrians"""
    
    static_obstacles : ClassVar["list[carla.Actor]"]
    """List of all tracked static obstacles"""
    
    obstacles : ClassVar["list[carla.Actor]"]
    """Union of :py:attr:`vehicles`, py:attr:`walkers` and py:attr:`static_obstacles`"""
    
    lights_map : ClassVar["Dict[int, carla.Waypoint]"] = {}
    """Map of traffic lights to their trigger waypoints"""
    
    frame: ClassVar["int | None"] = None
    """
    Last frame the InformationManager was updated.
    
    The current frame of the world should be passed to the global_tick method.
    """
    
    # ---- Agent Specific Information ----
    
    def __init__(self, agent: "LunaticAgent", update_information: bool = True):
        self._agent = agent
        self.live_info = agent.live_info
        
        self._vehicle = agent._vehicle # maybe use a property
        
        # Share the dict
        if getattr(agent, "current_states", None) is not None:
            self.state_counter = agent.current_states
        else:
            self.state_counter = agent.current_states = dict.fromkeys(AgentState, 0)
        self._states_checked = {s: False for s in AgentState}
        if update_information:
            self.tick()
    
    # AgentState detection
    
    #@staticmethod # not possible in python3.7
    def _check_state(state: AgentState): # pyright: ignore[reportSelfClsParameterName, reportGeneralTypeIssues]
        """
        Updates the state counter and the state checked dict when the function is called.
        """
        def wrapper(func : Callable[Concatenate[Self,_P], _T]) ->  Callable[Concatenate[Self,_P], _T]:# -> _Wrapped[Callable[Concatenate[Self, _P], Any], bool | Non...:
            @wraps(func)
            def inner(self: Self, *args: _P.args, **kwargs: _P.kwargs):
                result = func(self, *args, **kwargs)
                if result is not None:
                    if result:
                        self.state_counter[state] += 1
                    else:
                        self.state_counter[state] = 0
                    self._states_checked[state] = True
                return result
            return inner
        return wrapper
    
    @_check_state(AgentState.DRIVING)
    def detect_driving_state(self) -> bool:
        """
        Increased the :py:attr:`AgentState.DRIVING` counter if the vehicle is driving.
        
        :meta private:
        """
        return self._vehicle_speed >= DRIVING_SPEED_THRESHOLD
    
    @_check_state(AgentState.STOPPED)
    def detect_stopped_state(self) -> bool:
        """
        Increased the :py:attr:`AgentState.STOPPED` counter if the vehicle is stopped.
        
        :meta private:
        """
        return self._vehicle_speed < STOPPED_SPEED_THRESHOLD
    
    @_check_state(AgentState.REVERSE)
    def detect_reverse_state(self) -> bool:
        """
        Determines if in the last tick the VehicleControl.reverse flag was set.
        
        Increases the :py:attr:`AgentState.REVERSE` counter if the vehicle is driving in reverse.
        
        :meta private:
        """
        # TODO: can this be detected differently e.g. through the vehicle
        return self.live_info.last_applied_controls.reverse
    
    # Not implemented checks
    
    @_check_state(AgentState.AGAINST_LANE_DIRECTION)
    def detect_driving_against_lane_direction(self):
        """
        :meta private:
        """
        self._agent._current_waypoint.lane_id # positive or negative
        # TODO: How detect if the heading is against this direction?
        # Need to also account for reverse state.
        NotImplemented
    
    @_check_state(AgentState.OVERTAKING)
    def detect_overtaking_state(self):
        """
        :meta private:
        """
        NotImplemented # Can probably not be done easily, and must be done from outside
    
    def check_states(self):
        """
        Updates all states. Called in :py:meth:`tick`.
        
        :meta private:
        """
        # Updates are handles trough the decorators
        self.detect_driving_state()
        self.detect_stopped_state()
        self.detect_reverse_state()

    # --- Traffic Light ---
    
    def _get_next_traffic_light(self) -> Optional[carla.TrafficLight]:
        # TODO: Do not use the CDP but use the planned route instead.
        self.relevant_traffic_light = CarlaDataProvider.get_next_traffic_light(self._vehicle)
        if self.relevant_traffic_light:
            self._relevant_traffic_light_location = self.relevant_traffic_light.get_location()
            self.relevant_traffic_light_distance = self._relevant_traffic_light_location.distance(
                CarlaDataProvider.get_location(self._vehicle))  # pyright: ignore[reportArgumentType]
        else:
            # Is at an intersection; always check for tlight or distance
            self._relevant_traffic_light_location = None  # type: ignore[assignment]
            self.relevant_traffic_light_distance = float('inf')
        return self.relevant_traffic_light
    
    def detect_next_traffic_light(self):
        """
        Set the :py:attr:`relevant_traffic_light` and :py:attr:`relevant_traffic_light_distance` if not set.
        
        Note: 
            Does not check for planned path but current route along waypoints, might not be exact.
            
            **This function is automatically called in :py:meth:`tick`**
        """
        if self.relevant_traffic_light_distance < float('inf'):
            tlight_distance = self._relevant_traffic_light_location.distance(self.live_info.current_location)
        else:
            tlight_distance = float('inf')
        
        # Search for a traffic light if none is given or if the distance to the current one increased
        # 1% tolerance to prevent permanent updates when far away from a traffic light
        if not self.relevant_traffic_light or tlight_distance > self.relevant_traffic_light_distance * 1.01: 
            # Update if the distance increased, and we might need to target another one; # TODO: This might be circumvented by passing and intersection
            if self.relevant_traffic_light and tlight_distance > self.relevant_traffic_light_distance * 1.01:
                logger.debug("Traffic light distance increased %s, did slow update.", self.relevant_traffic_light_distance)
            self._get_next_traffic_light()
        elif self.relevant_traffic_light:
            self.relevant_traffic_light_distance = tlight_distance
    
    # ---- Tick ----
        
    def tick(self):
        """
        Tick the information manager and update the information for the corresponding agent.
        """
        snapshot = CarlaDataProvider.get_world().get_snapshot()
        self.global_tick(snapshot.frame)
        
        # --- Vehicle Information ---
        self.live_info.last_applied_controls = self._vehicle.get_control()
        
        # - Speed -
        # NOTE: get_velocity does not take the z axis into account.
        self.live_info.current_speed_limit = self._vehicle.get_speed_limit()
        
        self.live_info.velocity_vector = self._vehicle.get_velocity()
        
        self._vehicle_speed = CarlaDataProvider.get_velocity(self._vehicle) # used for AgentState Checks
        self.live_info.current_speed = self._vehicle_speed * 3.6 # km/h
        
        # - Location -
        # NOTE: That transform.location and location are similar but not identical.
        self.live_info.current_transform = CarlaDataProvider.get_transform(self._vehicle)
        self.live_info.current_location = _current_loc = CarlaDataProvider.get_location(self._vehicle) # NOTE: is None if past run not cleaned # noqa: E501
        # Only exact waypoint. TODO: update in agent
        # Comment should be visible in traceback. 
        current_waypoint : carla.Waypoint = CarlaDataProvider.get_map().get_waypoint(_current_loc) # NOTE: Might throw error if past run was not cleaned; or the world did not tick yet. # noqa: E501 # pyright: ignore[reportCallIssue]
        
        # Traffic Light
        # NOTE: Must be AFTER the location update
        self.detect_next_traffic_light()
        self.live_info.next_traffic_light = self.relevant_traffic_light
        self.live_info.next_traffic_light_distance = self.relevant_traffic_light_distance
        
        # Nearby actors
        self.distances: Dict[carla.Actor, float] = {}
        
        @cached(cache=self.distances)
        def dist(v : carla.Actor): 
            if not v.is_alive:
                logger.warning("Actor is not alive - this should not happen.")
                return _v_filter_dist # filter out
            return v.get_location().distance(_current_loc)  # pyright: ignore[reportArgumentType]
        
        # Filter nearby
        # Vehicles
        _v_filter_dist = self._agent.config.obstacles.nearby_vehicles_max_distance
        self.vehicles_nearby : List[carla.Vehicle] = []
        for v in self.vehicles:
            if v.id != self._vehicle.id and dist(v) < _v_filter_dist:
                self.vehicles_nearby.append(v)
        self.vehicles_nearby = sorted(self.vehicles_nearby, key=dist)
        
        # Static obstacles
        self.static_obstacles_nearby = []
        for o in self.static_obstacles:
            if dist(o) < _v_filter_dist:
                self.static_obstacles_nearby.append(o)
        self.static_obstacles_nearby = sorted(self.static_obstacles_nearby, key=dist)
        
        # Walkers
        _v_filter_dist = self._agent.config.obstacles.nearby_walkers_max_distance # in case of a different distance for walkers.
        self.walkers_nearby = []
        for w in self.walkers:
            if dist(w) < _v_filter_dist:
                self.walkers_nearby.append(w)
        
        self.walkers_nearby = sorted(self.walkers_nearby, key=dist)
        # All actors to be tracked
        self.obstacles_nearby = self.walkers_nearby + self.static_obstacles_nearby + self.vehicles_nearby
        self.obstacles_nearby = sorted(self.obstacles_nearby, key=dist)
        
        # Nearby Traffic lights
        # By default this checks for 5 seconds range + 10 m
        self.traffic_lights_nearby = [tl for tl, trans in InformationManager.get_traffic_lights().items() if dist(tl) < self._agent.config.obstacles.nearby_tlights_max_distance]
        self.traffic_lights_nearby = sorted(self.traffic_lights_nearby, key=dist)
        
        self.check_states()
        
        # ----- Return Summary -----
        
        # TODO: Extend distances with carla lights
        self.gathered_information = InformationManager.Information(
            current_waypoint= current_waypoint,
            current_speed= self.live_info.current_speed,
            current_states= self.state_counter,
            
            relevant_traffic_light=self.relevant_traffic_light, 
            relevant_traffic_light_distance=self.relevant_traffic_light_distance,
            
            vehicles= self.vehicles,
            walkers = self.walkers,
            static_obstacles = self.static_obstacles,
            obstacles = self.obstacles,
            
            walkers_nearby= self.walkers_nearby,
            vehicles_nearby= self.vehicles_nearby,
            static_obstacles_nearby= self.static_obstacles_nearby,
            obstacles_nearby= self.obstacles_nearby,
            traffic_lights_nearby= self.traffic_lights_nearby,
            
            distances = self.distances,
        )
        return self.gathered_information

    # Helper subclass

    class Information(NamedTuple):
        """Data gathered by the InformationManager which is passed to the agent."""
        
        current_waypoint: carla.Waypoint
        current_speed: float
        current_states : Dict[AgentState, int]
        
        relevant_traffic_light: Optional[carla.TrafficLight]
        relevant_traffic_light_distance: float
        
        vehicles: List[carla.Vehicle]
        walkers: List[carla.Walker]
        static_obstacles: List[carla.Actor]
        """Filtered obstacles by InformationManager.OBSTACLE_FILTER"""
        obstacles : List[carla.Actor]
        """Union of vehicles, walkers and static_obstacles"""
        
        walkers_nearby: List[carla.Walker]
        vehicles_nearby: List[carla.Vehicle]
        static_obstacles_nearby: List[carla.Actor]
        obstacles_nearby: List[carla.Actor]
        
        traffic_lights_nearby : List[carla.TrafficLight]
        
        distances: Dict[carla.Actor, float]
        """Distances to all actors in :py:attr:`obstacles`"""

    # ---- Global Information ----
    
    OBSTACLE_FILTER : str  = "static.prop.[cistmw]*"
    """
    fnmatch for obstacles that the agent will consider in its path.
    https://carla.readthedocs.io/en/latest/bp_library/#static 
    """
    
    @staticmethod
    def get_traffic_lights() -> Dict[carla.TrafficLight, carla.Transform]:
        return CarlaDataProvider._traffic_light_map
    
    @staticmethod
    def get_trafficlight_trigger_waypoint(traffic_light : "carla.TrafficLight") -> carla.Waypoint:
        """
        Get the location where the traffic light is triggered.
        """
        if traffic_light.id in InformationManager.lights_map:
            return InformationManager.lights_map[traffic_light.id]
        trigger_location = CarlaDataProvider.get_trafficlight_trigger_location(traffic_light)
        trigger_wp = CarlaDataProvider.get_map().get_waypoint(trigger_location)
        InformationManager.lights_map[traffic_light.id] = trigger_wp
        return trigger_wp

    @staticmethod
    def global_tick(frame: Optional[int]=None) -> None:
        """
        Update global information that is constant for the current tick and not agent specific.
        
        Updates:
            - :py:attr:`vehicles`
            - :py:attr:`walkers`
            - :py:attr:`static_obstacles`
            - :py:attr:`obstacles`
            - :py:attr:`frame`
        
        Parameters:
            frame: The id of the current frame. If None retrieves the id from the current 
                :py:class:`carla.WorldSnapshot`. Multiple calls with the same frame are ignored.
                (default: None)
        """
        # Assure to call this only once
        if frame is None:
            frame = CarlaDataProvider.get_world().get_snapshot().frame
        else:
            # DEBUG; TEMP
            snap_frame = CarlaDataProvider.get_world().get_snapshot().frame
            if frame != snap_frame:
                logger.warning(f"Frame {frame} does not match snapshot frame {snap_frame}")
        if frame == InformationManager.frame:
            return
        InformationManager.frame = frame

        # Filter vehicles
        InformationManager.vehicles = []
        InformationManager.walkers = []
        InformationManager.static_obstacles = []
        InformationManager._other_actors: List[carla.Actor] = []
        # For traffic lights use: InformationManager.get_traffic_lights(), which is map-constant
        
        # Use copy and check for None because of updates could be done by threads in parallel
        for actor_id in CarlaDataProvider._carla_actor_pool.copy():
            try:
                actor = CarlaDataProvider._carla_actor_pool[actor_id] # might be deleted in parallel
                if actor is None or not actor.is_alive:
                    logger.debug("Detected dead actor in the pool. %s", (actor.id, actor.type_id, actor.attributes))
                    del CarlaDataProvider._carla_actor_pool[actor_id]
                    continue
            except KeyError:
                # actor was deleted in parallel
                print("KeyError", actor_id)
                continue
            if fnmatch(actor.type_id, "vehicle*"):
                InformationManager.vehicles.append(actor)  # pyright: ignore[reportArgumentType]]
            elif fnmatch(actor.type_id, "walker.pedestrian*"):
                InformationManager.walkers.append(actor)  # pyright: ignore[reportArgumentType]
            # TODO: we could assume that these actors are mostly constant and only created in slow intervals
            elif fnmatch(actor.type_id, InformationManager.OBSTACLE_FILTER):
                InformationManager.static_obstacles.append(actor)
            else:
                InformationManager._other_actors.append(actor)

        InformationManager.obstacles = InformationManager.walkers + InformationManager.static_obstacles + InformationManager.vehicles
        
    @staticmethod
    def get_vehicles() -> List[carla.Vehicle]:
        return InformationManager.vehicles
    
    @staticmethod
    def get_walkers() -> List[carla.Walker]:
        return InformationManager.walkers

    @staticmethod
    def cleanup() -> None:
        """Resets the global information."""
        InformationManager.vehicles.clear()
        InformationManager.walkers.clear()
        InformationManager.static_obstacles.clear()
        InformationManager.obstacles.clear()
        InformationManager._other_actors.clear()
        InformationManager.frame = None
        InformationManager._tick = 0