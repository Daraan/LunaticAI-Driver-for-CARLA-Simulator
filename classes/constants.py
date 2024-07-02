from enum import Enum, Flag, IntEnum, auto
from functools import lru_cache, reduce
from typing import NewType, Union, TYPE_CHECKING

import carla

if TYPE_CHECKING:
    from agents.navigation.local_planner import RoadOption
    
NO_RESULT_TYPE = NewType("NO_RESULT_TYPE", object)
"""Type helper for objects that indicate no result."""

RULE_NO_RESULT = NO_RESULT_TYPE(object())

class StreetType(str, Enum):
    ON_HIGHWAY = "On highway"
    NON_HIGHWAY_STREET = "Non highway street"
    ON_JUNCTION = "On junction"
    ON_HIGHWAY_ENTRY = "On highway entry"
    ON_HIGHWAY_EXIT = "On highway exit"
    JUNCTION_AHEAD = "Junction ahead"
    HIGHWAY_TRAFFIC_LIGHT = "Highway traffic light"
    HIGHWAY_WITH_ENTRY_AND_EXIT = "Highway with entry/exit"
    
class StreetOccupation(IntEnum):
    NO_CAR = 0
    EGO = 1
    CAR = 2
    NO_ROAD = 3
    
    def __str__(self) -> str:
        s = super().__str__()
        return f"{s:^7}" # center the word
        

class Phase(Flag):
    """
    Order of Looped through by the agent is:

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
    <Phases.EXECUTION|BEGIN: 1025>,
    <Phases.EXECUTION|END: 1026>
    
    Todo: 
        not up to date list
    
    """
    

    # NOTE: # CRITICAL : Alias creation should be done after all the phases are created.
    # see https://github.com/python/cpython/issues/91456
    # Before python version (3.12+?) auto() DOES NOT WORK AS EXPECTED when using ALIASES

    NONE = 0

    # These can be combined with any of the other Phases
    BEGIN = auto()
    END = auto()

    UPDATE_INFORMATION = auto()

    PLAN_PATH = auto()

    DETECT_TRAFFIC_LIGHTS = auto()
    DETECT_PEDESTRIANS = auto()
    DETECT_STATIC_OBSTACLES = auto()

    DETECT_CARS = auto()
    TAKE_NORMAL_STEP = auto()

    RSS_EVALUATION = auto()
    """
    See Also:
        - [LunaticAgent.parse_keyboard_input](#LunaticAgent.parse_keyboard_input)
        - [RssKeyboardControls.parse_events](#RssKeyboardControls.parse_events)
    """
    
    APPLY_MANUAL_CONTROLS = auto()
    """Applied manually via human user interface."""

    EXECUTION = auto() # Out of loop
    """
    Executed when the control is applied to the agent.
    
    See Also:
        agent.apply_control()
    """

    # --- Special situations ---
    CAR_DETECTED = auto()

    TURNING_AT_JUNCTION = auto()
    """Indicates that the agent is turning at a junction."""

    HAZARD = auto()
    EMERGENCY = auto()
    COLLISION = auto()

    DONE = auto() # agent.done() -> True
    """Indicates that the agent is at the end of its path. agent.done() is True"""
    
    TERMINATING = auto() # When closing the loop
    """Can be called when the agent is terminating. Must be executed by the user."""
    
    CUSTOM_CYCLE = auto()
    """
    Can be used to indicate that the phase change is currently handled by the user.
    
    Note:
        agent.execute_phase checks for exact match
    
    See Also:
        Executes in BlockedRule.loop_agent()
    """
    # States which the agent can be in outside of a normal Phase0-5 loop 

    # --- Aliases & Combination Phases ---
    # NOTE: # CRITICAL : Alias creation should be done after all the phases are created.!!!

    DETECT_NON_CARS = DETECT_STATIC_OBSTACLES | DETECT_TRAFFIC_LIGHTS | DETECT_PEDESTRIANS
    DETECTION_PHASE = DETECT_NON_CARS | DETECT_CARS

    EXCEPTIONS = HAZARD | EMERGENCY | COLLISION | TURNING_AT_JUNCTION | CAR_DETECTED | DONE | TERMINATING
    
    USER_CONTROLLED = APPLY_MANUAL_CONTROLS | EXECUTION | TERMINATING | CUSTOM_CYCLE
    """Phases that might or not be went through as they must be implemented manually by the user."""

    NORMAL_LOOP = UPDATE_INFORMATION | PLAN_PATH | DETECTION_PHASE | TAKE_NORMAL_STEP
    IN_LOOP = NORMAL_LOOP | EMERGENCY | COLLISION
    """
    Phases that are executed in or before the inner step, EMERGENCY is executed,
    right after the inner step.
    
    Warning:
        Phase.COLLISION is not yet implemented in the submodule.
    See Also:
        - [LunaticAgent.run_step](#LunaticAgent.run_step)
        - [collision_manager](#agents.substep_managers.collision_manager)
    """
    
    """
    def __eq__(self, other):
        # Makes sure that we can use current_phase == Phases.UPDATE_INFORMATION
        if not isinstance(other, Phase):
            return False
        # Check None
        if self is Phase.NONE or other is Phase.NONE:
            return self is other
        return self in other or other in self
    """

    def next_phase(self):
        # Hardcoded transitions
        if self in (Phase.NONE, Phase.EXECUTION|Phase.END): # Begin loop
            return Phase.BEGIN | Phase.UPDATE_INFORMATION
        #if self in (Phase.EXECUTION|Phase.END, Phase.DONE| Phase.END) : # End loop
        #    return Phase.NONE
        if self == Phase.EXECUTION | Phase.BEGIN:
            return Phase.USER_CONTROLLED # Cannot know what the next phase is
        if Phase.BEGIN in self:
            return (self & ~Phase.BEGIN) | Phase.END
        # Note these should all be END phases
        if Phase.DONE in self:
            return Phase.BEGIN | Phase.UPDATE_INFORMATION
        if Phase.EXCEPTIONS & self:
            #return Phase.EXECUTION | Phase.BEGIN
            return Phase.RSS_EVALUATION | Phase.BEGIN
        if Phase.USER_CONTROLLED & self:
            # cannot know what the next phase is
            return Phase.USER_CONTROLLED | Phase.BEGIN # assure that is a BEGIN or END phase
        if Phase.TERMINATING in self:
            return Phase.NONE
        if Phase.END in self: # Safeguard
            return Phase.BEGIN | Phase((self & ~Phase.END).value * 2)
        raise ValueError(f"Phase {self} is not a valid phase")
        return Phase(self.value * 2)
    
    def validate_next_phase(current_phase, next_phase):
        assumed_next = current_phase.next_phase()
        NotImplemented # Currently done in agent.execute_phase

    @classmethod
    def get_user_controlled_phases(cls):
        user_phases = cls.APPLY_MANUAL_CONTROLS, cls.EXECUTION, cls.TERMINATING, cls.CUSTOM_CYCLE
        assert all(p & cls.USER_CONTROLLED for p in user_phases)
        return user_phases

    @classmethod
    def get_phases(cls):
        return cls.get_main_phases() + cls.get_exceptions() + [p for phase in cls.get_user_controlled_phases() for p in (phase | cls.BEGIN, phase | cls.END)] + [cls.TERMINATING | cls.BEGIN, cls.TERMINATING | cls.END]

    @classmethod
    @lru_cache(1)  # < Python3.8
    def get_main_phases(cls):
        main_phases = [cls.NONE, cls.UPDATE_INFORMATION | cls.BEGIN]
        p = main_phases[1].next_phase()
        while p != main_phases[1] and not (p & cls.USER_CONTROLLED):
            if p & cls.USER_CONTROLLED:
                raise ValueError("User controlled phase should not be in main phases %s" % p)
            main_phases.append(p)
            p = p.next_phase()
        return main_phases

    @classmethod
    @lru_cache(1)  # < Python3.8
    def get_exceptions(cls):
        exceptions = [cls.TURNING_AT_JUNCTION, cls.HAZARD, cls.EMERGENCY, cls.COLLISION, cls.CAR_DETECTED, cls.DONE] # TODO: Get this from EXCEPTIONS
        exception_phases = []
        for e in exceptions: # improve with itertools
            exception_phases.append(e | cls.BEGIN)
            exception_phases.append(e | cls.END)
        return exception_phases

    @classmethod
    def set_phase(cls, phase : Union[int, None], end:bool=False) -> "Phase":
        """
        Set Phase by the number of the phase, i.e. PHASE_#.
        Not to be confused wih the flag value.

        Passing None will return Phases.NONE.
        """
        if phase is None:
            return cls.NONE
        return getattr(cls, f"PHASE_{phase}") | (Phase.END if end else Phase.BEGIN)
    
    @classmethod
    def from_string(cls, string: str) -> "Phase":
        """
        Utility method that turns a string 'Phase_# | Phase.BEGIN | ...' into a Phase.
        
        NOTE:
            Only supports the operator |.
        """
        
        elements = string.split("|") # Phase.NAME
        elements = [cls[e.split(".")[-1].strip()] for e in elements]
        phase = reduce(lambda x, y: x | y, elements) # build union
        return  phase


class Hazard(Flag):
    # Type
    TRAFFIC_LIGHT = auto()
    PEDESTRIAN = auto()
    CAR = auto()
    STATIC_OBSTACLE = auto()
    """
    Note:
        These refer to actors and not the environment barriers.
    """
    
    OTHER = auto()

    JUNCTION = auto() # maybe

    # Severity
    WARNING = auto() # Level 1
    CRITICAL_ONLY = auto()
    EMERGENCY_ONLY = auto()

    COLLISION = auto()

    # Aliases
    CRITICAL = WARNING | CRITICAL_ONLY # Level 2
    EMERGENCY = CRITICAL | EMERGENCY_ONLY # Level 3

    OBSTACLE = PEDESTRIAN | CAR


class RulePriority(IntEnum):
    """
    Priority of a `Rule`. The higher a value, the higher the priority.
    Rules are sorted by their priority before being applied.
    """
    NULL = 0
    LOWEST = 1
    LOW = 2
    NORMAL = 4
    HIGH = 8
    HIGHEST = 16

class __ItemAccess(type):
    def __getitem__(cls, key) -> carla.Color:
        return getattr(cls, key)
    
    def __call__(cls, option: "RoadOption") -> carla.Color:
        return getattr(cls, option.name)

class RoadOptionColor(metaclass=__ItemAccess):
    VOID = carla.Color(0, 128, 0)  # Green
    LEFT = carla.Color(128, 128, 0) # Yellow
    RIGHT = carla.Color(0, 128, 128) # Cyan
    STRAIGHT = carla.Color(64, 64, 64) # Gray
    LANEFOLLOW = carla.Color(0, 128, 0)  # Green
    CHANGELANELEFT = carla.Color(128, 32, 0)  # Orange
    CHANGELANERIGHT = carla.Color(0, 32, 128) # Dark Cyan
    
    
class AgentState(Flag):
    DRIVING = auto()
    STOPPED = auto()
    _parked = auto() # hide it to avoid confusion, used further down for PARKED
    
    BLOCKED_BY_VEHICLE = auto()
    BLOCKED_RED_LIGHT = auto()
    BLOCKED_OTHER = auto()
    
    REVERSE = auto()
    
    OVERTAKING = auto()
    
    AGAINST_LANE_DIRECTION = auto()
    
    PARKED = _parked | STOPPED # we want this to be a combination of the two
    BLOCKED = BLOCKED_OTHER | BLOCKED_BY_VEHICLE | BLOCKED_RED_LIGHT
    
    # Maybe more states like CAR_IN_FRONT <- data matrix
        
