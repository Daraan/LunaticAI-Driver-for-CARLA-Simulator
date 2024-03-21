from enum import Enum, Flag, IntEnum, auto
from functools import lru_cache
from typing import Union

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

    DETECT_CARS = auto()
    TAKE_NORMAL_STEP = auto()

    RSS_EVALUATION = auto()
    
    """Applied manually via human user interface."""
    APPLY_MANUAL_CONTROLS = auto()

    EXECUTION = auto() # Out of loop

    # --- Special situations ---
    CAR_DETECTED = auto()

    TURNING_AT_JUNCTION = auto()

    HAZARD = auto()
    EMERGENCY = auto()
    COLLISION = auto()

    DONE = auto() # agent.done() -> True
    TERMINATING = auto() # When closing the loop
    # States which the agent can be in outside of a normal Phase0-5 loop 

    # --- Aliases & Combination Phases ---
    # NOTE: # CRITICAL : Alias creation should be done after all the phases are created.!!!


    DETECT_NON_CARS = DETECT_TRAFFIC_LIGHTS | DETECT_PEDESTRIANS
    DETECTION_PHASE = DETECT_NON_CARS | DETECT_CARS

    PHASE_0 = UPDATE_INFORMATION
    PHASE_1 = PLAN_PATH # alias
    PHASE_2 = DETECT_NON_CARS  # alias
    PHASE_3 = DETECT_CARS # alias
    PHASE_4 = TAKE_NORMAL_STEP # alias
    PHASE_5 = EXECUTION # out of loop

    EXCEPTIONS = HAZARD | EMERGENCY | COLLISION | TURNING_AT_JUNCTION | CAR_DETECTED | DONE | TERMINATING
    
    USER_CONTROLLED = APPLY_MANUAL_CONTROLS | EXECUTION | TERMINATING
    """Phases that might or not be went through as they must be implemented manually by the user."""

    NORMAL_LOOP = UPDATE_INFORMATION | PLAN_PATH | DETECTION_PHASE | TAKE_NORMAL_STEP
    IN_LOOP = NORMAL_LOOP | EMERGENCY | COLLISION


    """
    def __eq__(self, other):
        # Makes sure that we can use current_phase == Phases.UPDATE_INFORMATION
        if isinstance(other, Phases):
            if self is Phases.NONE or other is Phases.NONE:
                return self is other
            return self in other or other in self
        return False
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

    @classmethod
    def get_user_controlled_phases(cls):
        return cls.APPLY_MANUAL_CONTROLS, cls.EXECUTION, cls.TERMINATING

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


class Hazard(Flag):
    # Type
    TRAFFIC_LIGHT = auto()
    PEDESTRIAN = auto()
    CAR = auto()
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
