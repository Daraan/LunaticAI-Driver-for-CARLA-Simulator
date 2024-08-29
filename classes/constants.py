# pyright: reportUnusedImport=information, reportInvalidStringEscapeSequence=false
"""
In this module defines enums and constants that are used throughout the project.

.. Comment "#: :meta hide-value:" hides the value in the documentation.
"""

import os
from enum import Enum, Flag, IntEnum, auto
from functools import lru_cache, reduce
from typing import TYPE_CHECKING, ClassVar, Dict, Union
from typing_extensions import Self, TypeAlias

import carla

    
AD_RSS_AVAILABLE : bool
"""
Indicator if the :py:mod:`carla.ad` module is available, i.e. if the current carla version was build
with RSS support. As a rule of thumb: On Windows this will be always false.
If this is false some objects will be missing in the :py:mod:`carla` module, for example 
the :py:class:`carla.RssSensor`, likewise are some utilities of this project involving RSS not be
available.

See Also:
    - https://carla.readthedocs.io/en/latest/adv_rss/
    - https://github.com/intel/ad-rss-lib

:meta hide-value:
"""
try:
    from carla import ad      # pyright: ignore # noqa
    AD_RSS_AVAILABLE = True
except ImportError:
    AD_RSS_AVAILABLE = False  # pyright: ignore[reportConstantRedefinition]
    
    
READTHEDOCS = os.environ.get("READTHEDOCS", False)
"""
Whether the code is currently used to build the docs:

Values:
    - False: Normal Runtime
    - 'local' : Local build
    - other: ReadTheDocs build

:meta hide-value:
:meta private:
"""

class AgentState(Flag):
    """
    High-level states that the agent currently can be in.
    
    Used with :py:attr:`.LunaticAgent.current_states` 
    and :py:attr:`.InformationManager.state_counter`.
    """
    
    DRIVING = auto()   #: :meta hide-value:
    STOPPED = auto()   #: :meta hide-value:
    _parked = auto()   # hidden it to avoid confusion, used further down for PARKED
    
    BLOCKED_BY_VEHICLE = auto()    #: :meta hide-value:
    BLOCKED_RED_LIGHT = auto()     #: :meta hide-value:
    BLOCKED_BY_STATIC = auto()
    """
    Static obstacle. 
    
    Attention:
        Not updated by the information manager 
        but in the :py:attr:`Phase.DETECT_STATIC_OBSTACLES` phase.
    
    :meta hide-value:
    """
    
    BLOCKED_OTHER = auto()          #: :meta hide-value:
    
    REVERSE = auto()                #: :meta hide-value:
    
    OVERTAKING = auto()             #: :meta hide-value:
    
    AGAINST_LANE_DIRECTION = auto() #: :meta hide-value:
    
    PARKED = _parked | STOPPED # we want this to be a combination of the two
    """Includes :py:attr:`STOPPED`"""
    
    BLOCKED = BLOCKED_OTHER | BLOCKED_BY_VEHICLE | BLOCKED_RED_LIGHT | BLOCKED_BY_STATIC
    """
    Combination of :python:`BLOCKED_OTHER | BLOCKED_BY_VEHICLE | BLOCKED_RED_LIGHT | BLOCKED_BY_STATIC`
    
    :meta hide-value:
    """
    
    # Maybe more states like CAR_IN_FRONT <- data matrix


class RulePriority(IntEnum):
    """
    Priority of a :py:class:`Rule <classes.rule.Rule>`.
    The higher a value, the higher the priority.
    Rules are sorted by their priority before being applied.
    """
    NULL = 0
    LOWEST = 1
    LOW = 2
    NORMAL = 4
    HIGH = 8
    HIGHEST = 16

class Phase(Flag):
    """
    A rough order of the looped through states of the agent is:

    .. code-block:: python
    
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

    Note:
        The above cycle list is not up to date.
    
        A complete list of all the main phases can be obtained by calling
            - :py:func:`Phase.get_main_phases`
            - :py:func:`Phase.get_phases`
    """
    
    # NOTE: # CRITICAL : Alias creation should be done >after< all the phases are created.
    # see https://github.com/python/cpython/issues/91456
    # Before python version (3.12+?) auto() DOES NOT WORK AS EXPECTED when using ALIASES

    NONE = 0                       
    
    # These can be combined with any of the other Phases
    BEGIN = auto()
    """
    Indicates the beginning of a phase. Should always
    be combined with another phase.
    
    :meta hide-value:
    """
    
    END = auto()
    """
    Indicates the end of a phase. Should always
    be combined with another phase.
    
    :meta hide-value:
    """

    UPDATE_INFORMATION = auto()
    """
    Indicates the execution of the agents 
    :py:meth:`~.LunaticAgent.update_information` method
    
    This is the first Phase of the agent and executed every
    step.
    
    :meta hide-value:
    """

    PLAN_PATH = auto()
    """
    Indicates that the planning of a new path has started.
    
    Attention:
        If the the path is replanned a :py:exc:`UpdatedPathException` 
        should be raised.
        
    :meta hide-value:
    """

    DETECT_TRAFFIC_LIGHTS = auto()
    """
    Executed during the agents :py:meth:`~.LunaticAgent.detect_hazard`
    method. Can add :py:attr:`.Hazard.TRAFFIC_LIGHT_RED` or
    :py:attr:`.Hazard.TRAFFIC_LIGHT_YELLOW` to the agents 
    `.LunaticAgent.detected_hazards`:py:attr:.
    
    :meta hide-value:
    """
    
    DETECT_PEDESTRIANS = auto()
    """
    Executed during the agents :py:meth:`~.LunaticAgent.detect_hazard`
    method. Can add :py:attr:`.Hazard.PEDESTRIAN` to the agents
    `.LunaticAgent.detected_hazards`:py:attr:.
    
    :meta hide-value:
    """
    
    DETECT_STATIC_OBSTACLES = auto()
    """
    | Checks for static obstacles in the agents path with
    | :py:attr:`.detect_obstacles_in_path` (:py:attr:`.LunaticAgent.static_obstacles_nearby`)
    
    :meta hide-value:
    """
    # TODO: exchange LunaticAgent -> InformationManager when documented

    DETECT_CARS = auto()
    """
    | Checks for vehicles in the agents path with
    | :py:attr:`.detect_obstacles_in_path` (:py:attr:`.LunaticAgent.vehicles_nearby`)
    
    Note:
        If a car was detected executes :python:`Phase.CAR_DETECTED | BEGIN`,
        :python:`Phase.DETECT_CARS | BEGIN` is **only** executed if no car was detected.
    
    :meta hide-value:
    """
    
    TAKE_NORMAL_STEP = auto()
    """
    During this phase the :external-icon-parse:`:py:class:\`carla.VehicleControl\``
    is calculated by the local planner.
    
    :meta hide-value:
    """

    RSS_EVALUATION = auto()
    """
    
    See Also:
        - :py:meth:`agents.lunatic_agent.LunaticAgent.parse_keyboard_input`
        - :py:meth:`classes.keyboard_controls.RssKeyboardControls.parse_events`
    
    :meta hide-value:
    """
    
    APPLY_MANUAL_CONTROLS = auto()
    """Applied manually via human user interface.
    
    :meta hide-value:
    """

    EXECUTION = auto()
    """
    Executed when the control is applied to the agent.
    
    See Also:
        :py:meth:`LunaticAgent.apply_control() <agents.lunatic_agent.LunaticAgent.parse_keyboard_input>`
        
    :meta hide-value:
    """

    # --- Special situations ---
    CAR_DETECTED = auto()
    """
    The :python:`Phase.CAR_DETECTED | BEGIN` is executed when a car is detected
    and follows the :python:`Phase.DETECT_CARS | BEGIN` phase. If no car is detected
    the :python:`Phase.DETECT_CARS | END` phase is executed.
    
    :meta hide-value:
    """

    TURNING_AT_JUNCTION = auto()
    """
    Indicates that the agent is turning at a junction.
    
    Warning:
        This Phase might become obsolete.
    
    :meta hide-value:
    """

    HAZARD = auto()
    """
    Not implemented. Refer to EMERGENCY | BEGIN
    
    :meta hide-value:
    """
    
    EMERGENCY = auto()
    """
    Special Phase
    
    See Also:
        - `Emergency Phases`__

    __ docs/Rules.html#emergency-phase
    """
    
    COLLISION = auto()
    """
    Special phase that is executed out-of-order when a
    :external-icon-parse:`:py:class:\`carla.Sensor\`` detects a collision. 
    
    See Also:
        - :external-icon-parse:`:py:class:\`carla.CollisionEvent\``
        - https://carla.readthedocs.io/en/latest/ref_sensors/#collision-detector
    
    :meta hide-value:
    """

    DONE = auto()
    """
    Indicates that the agent is at the end of its path and
    :py:meth:`agent.done() <.LunaticAgent.done>` is :python:`True`.
    
    :meta hide-value:
    """
    
    TERMINATING = auto()
    """
    Can be called when the agent is terminating. Must be executed by the user.
    
    :meta hide-value:
    """
    
    CUSTOM_CYCLE = auto()
    """
    **experimental**
    
    Can be used to indicate that the phase change is currently handled by the user.
    
    Warning:
        :any:`LunaticAgent.execute_phase` checks for exact match, 
        i.e. a phase :python:`UPDATE_INFORMATION | BEGIN | END`
        will not be executed in the normal loop.
    
    See Also:
        Executed in :py:meth:`BlockingRule.loop_agent <classes.rule.BlockingRule.loop_agent>`
        
    :meta hide-value:
    """
    # States which the agent can be in outside of a normal Phase0-5 loop 

    # --- Aliases & Combination Phases ---
    # NOTE: # CRITICAL : Alias creation should be done after all the phases are created.!!!

    DETECT_NON_CARS = DETECT_STATIC_OBSTACLES | DETECT_TRAFFIC_LIGHTS | DETECT_PEDESTRIANS
    """
    Combination of :python:`DETECT_STATIC_OBSTACLES | DETECT_TRAFFIC_LIGHTS | DETECT_PEDESTRIANS`
    
    :meta hide-value:
    """
    
    DETECTION_PHASE = DETECT_NON_CARS | DETECT_CARS
    """
    Combination of :python:`DETECT_STATIC_OBSTACLES | DETECT_TRAFFIC_LIGHTS | DETECT_PEDESTRIANS | DETECT_CARS`
    
    :meta hide-value:
    """
    

    EXCEPTIONS = HAZARD | EMERGENCY | COLLISION | TURNING_AT_JUNCTION \
                     | CAR_DETECTED | DONE | TERMINATING
    """
    Combination of :python:`HAZARD | EMERGENCY | COLLISION | TURNING_AT_JUNCTION | CAR_DETECTED | DONE | TERMINATING`
    
    :meta hide-value:
    """
    
    
    USER_CONTROLLED = APPLY_MANUAL_CONTROLS | EXECUTION | TERMINATING | CUSTOM_CYCLE
    """
    Phases that might or not be went through as they must be implemented manually by the user.
    
    Combination of :python:`APPLY_MANUAL_CONTROLS | EXECUTION | TERMINATING | CUSTOM_CYCLE`
    
    :meta hide-value:
    """

    NORMAL_LOOP = UPDATE_INFORMATION | PLAN_PATH | DETECTION_PHASE | TAKE_NORMAL_STEP
    """
    Combination of :python:`UPDATE_INFORMATION | PLAN_PATH | DETECTION_PHASE | TAKE_NORMAL_STEP`
    
    :meta hide-value:
    """
    
    
    IN_LOOP = NORMAL_LOOP | EMERGENCY | COLLISION
    """
    Phases that are executed in or before the inner step, EMERGENCY is executed,
    right after the inner step.
    
    Combination of :python:`NORMAL_LOOP | EMERGENCY | COLLISION`
    
    See Also:
        - :py:meth:`LunaticAgent.run_step <agents.lunatic_agent.LunaticAgent.run_step>`
        - :py:mod:`agents.substep_managers.collision_manager`
    
    :meta hide-value:     
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
        """
        Note:
            This function is more for >>debugging<< and testing purposes,
            because of different control flows in the agent, the next phase
            might not be accurate.
            
        :meta private:
        """
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
    

    def validate_next_phase(current_phase, next_phase : "Phase") -> None: # type: ignore
        """
        :meta private:
        """
        
        assumed_next = current_phase.next_phase()  # type: ignore # noqa
        NotImplemented # Currently done in agent.execute_phase # type: ignore

    @classmethod
    def get_user_controlled_phases(cls):
        """
        :meta private:
        """
        user_phases = cls.APPLY_MANUAL_CONTROLS, cls.EXECUTION, cls.TERMINATING, cls.CUSTOM_CYCLE
        assert all(p & cls.USER_CONTROLLED for p in user_phases)
        return user_phases

    @classmethod
    def get_phases(cls):
        """Get all BEGIN and END phases combination."""
        return cls.get_main_phases() + cls.get_exceptions() + [p for phase in cls.get_user_controlled_phases() for p in (phase | cls.BEGIN, phase | cls.END)] + [cls.TERMINATING | cls.BEGIN, cls.TERMINATING | cls.END]

    @classmethod
    @lru_cache(1)  # < Python3.8
    def get_main_phases(cls):
        """
        Phases which are not exceptions or user controlled.
        
        :meta private:
        """
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
    def get_exceptions(cls) -> "list[Phase]":
        """
        Returns the :py:attr:`BEGIN` and :py:attr:`END` combinations of the exceptions that
        do not follow the normal loop.
        
        :meta private:
        """
         # TODO: Get this from EXCEPTIONS
        exceptions = [cls.TURNING_AT_JUNCTION, cls.HAZARD, cls.EMERGENCY, cls.COLLISION, cls.CAR_DETECTED, cls.DONE]
        exception_phases : "list[Phase]" = []
        for e in exceptions: # improve with itertools
            exception_phases.append(e | cls.BEGIN)
            exception_phases.append(e | cls.END)
        return exception_phases
    
    @classmethod
    def from_string(cls, string: str) -> "Phase":
        """
        Utility method that turns a string like :code:`Phase.NAME | BEGIN | ...` into a Phase.
        
        NOTE:
            Only supports the operator :code:`|`. :code:`NAME` must be a valid Phase name.
        """
        elements = string.split("|") # Phase.NAME
        elements = [cls[e.split(".")[-1].strip()] for e in elements]
        phase = reduce(lambda x, y: x | y, elements) # build union
        return  phase


class Hazard(Flag):
    """
    Values currently stored in the agent's :py:attr:`~.LunaticAgent.detected_hazards`.
    attribute.
    """
    
    # Type
    TRAFFIC_LIGHT_RED = auto()      #: :meta hide-value:
    TRAFFIC_LIGHT_YELLOW = auto()   #: :meta hide-value:
    
    PEDESTRIAN = auto()             #: :meta hide-value:
    CAR = auto()                    #: :meta hide-value:
    STATIC_OBSTACLE = auto()
    """
    Note:
        These refer to actors and not the environment barriers.
        
    :meta hide-value:
    """
    
    OTHER = auto()    #: :meta hide-value:

    JUNCTION = auto() #: :meta hide-value:
    
    OBSTACLE = PEDESTRIAN | CAR | STATIC_OBSTACLE
    """
    Combination of :python:`PEDESTRIAN | CAR | STATIC_OBSTACLE`
    
    :meta hide-value:
    """
    
    TRAFFIC_LIGHT = TRAFFIC_LIGHT_RED | TRAFFIC_LIGHT_YELLOW
    """
    Combination of :python:`TRAFFIC_LIGHT_RED | TRAFFIC_LIGHT_YELLOW`
    
    :meta hide-value:
    """
    

class HazardSeverity(Flag):
    """
    High level descriptions to further weight :py:class:`Hazard`.
    The :py:class:`HazardSeverity` flags are stored in :py:attr:`~.LunaticAgent.detected_hazards_info`.
    """
    
    UNKNOWN = -1 
    
    NONE = 0
    """
    Initial values for :py:attr:`.LunaticAgent.detected_hazards_info`
    """

    # Severity
    WARNING = auto()            # Level 1
    CRITICAL_ONLY = auto()      #: :meta private:
    EMERGENCY_ONLY = auto()     #: :meta private:

    COLLISION = auto()
    """
    Special case for collision.
    
    :meta hide-value:
    """

    # Aliases - Always register at the end!
    CRITICAL = WARNING | CRITICAL_ONLY # Level 2
    """
    Includes :py:attr:`WARNING`
    """
    
    EMERGENCY = CRITICAL | EMERGENCY_ONLY # Level 3
    """
    Includes :py:attr:`WARNING` and :py:attr:`CRITICAL`
    """

# ----------------- RoadOptions -----------------

if TYPE_CHECKING:
    # For type-checkers these classes should be the same.
    # Prevent circular imports
    from agents.navigation.local_planner import RoadOption
else:
    class RoadOption(IntEnum):
        """
        RoadOption represents the possible topological configurations when moving from a segment of lane to other.

        See Also:
            :py:class:`RoadOptionColor` for the color representation of the road options.
        """

        VOID = -1
        """
        Indicated by green
        """

        LEFT = 1
        """
        Indicated by yellow
        
        :meta hide-value:
        """

        RIGHT = 2
        """
        Indicated by cyan
        
        :meta hide-value:
        """

        STRAIGHT = 3
        """
        Indicated by gray
        
        :meta hide-value:
        """

        LANEFOLLOW = 4
        """
        Indicated by green
        
        :meta hide-value:
        """

        CHANGELANELEFT = 5
        """
        Indicated by orange
        
        :meta hide-value:
        """

        CHANGELANERIGHT = 6
        """
        Indicated by dark cyan
        
        :meta hide-value:
        """


class __ItemAccessMeta(type):  # noqa
    """Class that allows item access on the class."""
    def __getitem__(cls, key : str) -> carla.Color:
        return getattr(cls, key)
    
    def __call__(cls, option: "RoadOption") -> carla.Color:
        return getattr(cls, option.name)

class RoadOptionColor(metaclass=__ItemAccessMeta):
    """
    Points to a :py:class:`carla.Color` object that represents the color of the road option.
    
    Supports :python:`__getitem__(name)` and :python:`__call__(RoadOption)` for easy access.
    """
    
    VOID = carla.Color(0, 128, 0) # Green
    """
    Green
    
    :meta hide-value:
    """
    
    LEFT = carla.Color(128, 128, 0) # Yellow
    """
    Yellow
    
    :meta hide-value:
    """
    
    RIGHT = carla.Color(0, 128, 128) # Cyan
    """
    Cyan
    
    :meta hide-value:
    """
    
    STRAIGHT = carla.Color(64, 64, 64) # Gray
    """
    Gray
    
    :meta hide-value:
    """
    
    LANEFOLLOW = carla.Color(0, 128, 0)  # Green
    """
    Green
    
    :meta hide-value:
    """
    
    CHANGELANELEFT = carla.Color(128, 32, 0)  # Orange
    """
    Orange
    
    :meta hide-value:
    """
    
    CHANGELANERIGHT = carla.Color(0, 32, 128) # Dark Cyan
    """
    Dark Cyan
    
    :meta hide-value:
    """


# ----------------- RSS -----------------
# depending on availability of the carla.ad module

# Stub classes that are alike
class _CarlaIntEnum(IntEnum):
    """
    CARLA's Enums have a `values` entry that is not part of the python enum.Enum class.
    This abstract class adds this method.
    """

    values : ClassVar[Dict[int, Self]]
    names  : ClassVar[Dict[str, Self]]

    def __init_subclass__(cls):
        cls.values : dict[int, cls]
        cls.names  : dict[str, cls]


class RssLogLevelStub(_CarlaIntEnum):
    """Enum declaration used in carla.RssSensor to set the log level."""
    trace = 0
    debug = 1
    info = 2
    warn = 3
    err = 4
    critical = 5
    off = 6


class RssRoadBoundariesModeStub(_CarlaIntEnum):
    """
    Enum declaration used in carla.RssSensor to enable or disable the stay on road feature. 
    In summary, this feature considers the road boundaries as virtual objects.
    The minimum safety distance check is applied to these virtual walls, 
    in order to make sure the vehicle does not drive off the road. 
    """
    Off = 0
    On = 1

# assert that the stubs are correct
if AD_RSS_AVAILABLE:
    for value, name in carla.RssRoadBoundariesMode.values.items():
        assert RssRoadBoundariesModeStub[str(name)] == value
        
    for value, name in carla.RssLogLevel.values.items():
        assert RssLogLevelStub[str(name)] == value
    
if TYPE_CHECKING:
    RssLogLevelAlias: TypeAlias = Union[carla.RssLogLevel, RssLogLevelStub]
    RssRoadBoundariesModeAlias: TypeAlias = Union[carla.RssRoadBoundariesMode, RssRoadBoundariesModeStub]
# Correct at Runtime, correct time needed for OmegaConf
elif AD_RSS_AVAILABLE:  # noqa
    RssLogLevelAlias = carla.RssLogLevel
    RssRoadBoundariesModeAlias = carla.RssRoadBoundariesMode
else:
    RssLogLevelAlias = RssLogLevelStub
    RssRoadBoundariesModeAlias = RssRoadBoundariesModeStub

# Non type variant
if AD_RSS_AVAILABLE:
    RssLogLevel = carla.RssLogLevel
    RssRoadBoundariesMode = carla.RssRoadBoundariesMode
else:
    RssLogLevel = RssLogLevelStub
    RssRoadBoundariesMode = RssRoadBoundariesModeStub

#  ----------------- RuleResult -----------------
    
class RuleResult(Enum):
    """Special :python:`objects` that indicate special return values a :py:class:`.Rule`"""
    
    NO_RESULT = object()
    """
    Indicates the the rule returned no result, e.g. because an exception was raised.
    
    :meta hide-value:
    """
    
    NOT_APPLICABLE = object()
    """
    Object that indicates that no action was executed, e.g. because the rule is on cooldown or blocked.
    
    :meta hide-value:
    """
 
# ----------------- DetectionMatrix -----------------

class StreetType(str, Enum):
    """Used by the :py:class:`.DetectionMatrix` to interpret the street type."""
    
    ON_HIGHWAY = "On highway"
    NON_HIGHWAY_STREET = "Non highway street"
    ON_JUNCTION = "On junction"
    ON_HIGHWAY_ENTRY = "On highway entry"
    ON_HIGHWAY_EXIT = "On highway exit"
    JUNCTION_AHEAD = "Junction ahead"
    HIGHWAY_TRAFFIC_LIGHT = "Highway traffic light"
    HIGHWAY_WITH_ENTRY_AND_EXIT = "Highway with entry/exit"
    
class StreetOccupation(IntEnum):
    """
    Enum to interpret the results of the :py:class:`DetectionMatrix`
    """
    NO_CAR = 0
    EGO = 1
    CAR = 2
    NO_ROAD = 3
    
    def __str__(self) -> str:
        s = super().__str__()
        return f"{s:^7}" # center the word
    

