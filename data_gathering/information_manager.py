"""
Aim of this module is to provide a less convoluted access to information,
i.e. distill the information from the data and return high level information
"""

# todo: maybe find another name for this module

from fnmatch import fnmatch
from functools import wraps
from typing import Any, ClassVar, TYPE_CHECKING, NamedTuple, Union
import carla

if TYPE_CHECKING:
    from agents.lunatic_agent import LunaticAgent

from launch_tools import CarlaDataProvider

from agents.tools import logger


from classes.constants import AgentState

DRIVING_SPEED_THRESHOLD = 0.05 # m/s >= check
STOPPED_SPEED_THRESHOLD = 0.05 # m/s < check

class InformationManager:
    
    _tick = 0
    
    # Instance Variables
    relevant_traffic_light : Union[float, carla.TrafficLight] = None
    relevant_traffic_light_distance : Union[float, None] = None
    _relevant_traffic_light_location : carla.Location = None
    
    state_counter: "dict[AgentState, int]"
    _vehicle_speed : float # m/s
    
    gathered_information : "dict[str, Any]"
    
    # Class & Global Variables
    vehicles : ClassVar["list[carla.Vehicle]"]
    walkers : ClassVar["list[carla.Walker]"]
    
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
        
        self.state_counter = {s: 0 for s in AgentState}
        self._states_checked = {s: False for s in AgentState}
        if update_information:
            self.tick()
    
    # AgentState detection
    
    def _check_state(state):
        def wrapper(func):
            @wraps(func)
            def inner(self: "InformationManager", *args, **kwargs):
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
    def detect_driving_state(self):
        return self._vehicle_speed >= DRIVING_SPEED_THRESHOLD
    
    @_check_state(AgentState.STOPPED)
    def detect_stopped_state(self):
        return self._vehicle_speed < STOPPED_SPEED_THRESHOLD
    
    @_check_state(AgentState.REVERSE)
    def detect_reverse_state(self):
        """
        Determines if in the last tick the VehicleControl.reverse flag was set.
        """
        # TODO: can this be detected differently e.g. through the vehicle
        return self.live_info.last_applied_controls.reverse
    
    @_check_state(AgentState.AGAINST_LANE_DIRECTION)
    def detect_driving_against_lane_direction(self):
        self._agent._current_waypoint

    # Not implemented checks
    
    @_check_state(AgentState.OVERTAKING)
    def detect_overtaking_state(self):
        NotImplemented # Can probably not be done easily, and must be done from outside
    
    def check_states(self):
        # Updates are handles trough the decorators
        self.detect_driving_state()
        self.detect_stopped_state()
        self.detect_reverse_state()

    # --- Traffic Light ---
    
    def _get_next_traffic_light(self):
        self.relevant_traffic_light = CarlaDataProvider.get_next_traffic_light(self._vehicle)
        if self.relevant_traffic_light:
            self._relevant_traffic_light_location = self.relevant_traffic_light.get_location()
            self.relevant_traffic_light_distance = self._relevant_traffic_light_location.distance(CarlaDataProvider.get_location(self._vehicle))
        else:
            # Is at an intersection
            self._relevant_traffic_light_location = None
            self.relevant_traffic_light_distance = None
            logger.debug("No traffic light found - at intersection?")
        # TODO: Assure that the traffic light is not behind the actor, but in front of it.
        # TODO: Do not use the CDP but use the planned route instead.
    
    
    def detect_next_traffic_light(self):
        """
        Next relevant traffic light
        NOTE: Does not check for planned path but current route along waypoints, might not be exact.
        """
        if self.relevant_traffic_light_distance:
            tlight_distance = self._relevant_traffic_light_location.distance(self.live_info.current_location)
        else:
            tlight_distance = None
        
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
        self.live_info.current_location = CarlaDataProvider.get_location(self._vehicle)

        # Only exact waypoint. TODO: update in agent
        current_waypoint : carla.Waypoint = CarlaDataProvider.get_map().get_waypoint(self.live_info.current_location)
        
        # Traffic Light
        # NOTE: Must be AFTER the location update
        self.detect_next_traffic_light()
        self.live_info.next_traffic_light = self.relevant_traffic_light
        self.live_info.next_traffic_light_distance = self.relevant_traffic_light_distance
        
        return self.Information(
            current_waypoint= current_waypoint,
            current_speed= self.live_info.current_speed,
            relevant_traffic_light=self.relevant_traffic_light, 
            relevant_traffic_light_distance=self.relevant_traffic_light_distance,
            vehicles= self.vehicles,
            walkers = self.walkers
        )

    class Information(NamedTuple):
        current_waypoint: carla.Waypoint
        current_speed: float
        relevant_traffic_light: carla.TrafficLight
        relevant_traffic_light_distance: float
        vehicles: "list[carla.Vehicle]"
        walkers: "list[carla.Walker]"

    # ---- Global Information ----

    @staticmethod
    def global_tick(frame=None):
        # Assure to call this only once
        if frame is None:
            frame = CarlaDataProvider.get_world().get_snapshot().frame
        else:
            # DEBUG; TEMP
            snap_frame = CarlaDataProvider.get_world().get_snapshot().frame
            assert frame == snap_frame, f"Frame {frame} does not match snapshot frame {snap_frame}"
        if frame == InformationManager.frame:
            return
        InformationManager.frame = frame
        
        # Todo compare speed with global ActorList filter
        InformationManager.vehicles = [a for a in CarlaDataProvider._carla_actor_pool.values() if a.is_alive and fnmatch(a.type_id, "*vehicle*")]
        InformationManager.walkers = [a for a in CarlaDataProvider._carla_actor_pool.values() if a.is_alive and fnmatch(a.type_id, "*walker.pedestrian*")]
        
    @staticmethod
    def get_vehicles():
        return InformationManager.vehicles
    
    @staticmethod
    def get_walkers():
        return InformationManager.walkers
            