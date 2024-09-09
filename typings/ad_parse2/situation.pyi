import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

AtBack: LongitudinalRelativePosition
AtLeft: LateralRelativePosition
AtRight: LateralRelativePosition
InFront: LongitudinalRelativePosition
IntersectionEgoHasPriority: SituationType
IntersectionObjectHasPriority: SituationType
IntersectionSamePriority: SituationType
NotRelevant: SituationType
OppositeDirection: SituationType
Overlap: LongitudinalRelativePosition
OverlapBack: LongitudinalRelativePosition
OverlapFront: LongitudinalRelativePosition
OverlapLeft: LateralRelativePosition
OverlapRight: LateralRelativePosition
SameDirection: SituationType
Unstructured: SituationType

class LateralRelativePosition(Boost.Python.enum):
    AtLeft: ClassVar[LateralRelativePosition] = ...
    AtRight: ClassVar[LateralRelativePosition] = ...
    Overlap: ClassVar[LateralRelativePosition] = ...
    OverlapLeft: ClassVar[LateralRelativePosition] = ...
    OverlapRight: ClassVar[LateralRelativePosition] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class LongitudinalRelativePosition(Boost.Python.enum):
    AtBack: ClassVar[LongitudinalRelativePosition] = ...
    InFront: ClassVar[LongitudinalRelativePosition] = ...
    Overlap: ClassVar[LongitudinalRelativePosition] = ...
    OverlapBack: ClassVar[LongitudinalRelativePosition] = ...
    OverlapFront: ClassVar[LongitudinalRelativePosition] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class RelativePosition(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    lateralDistance: Incomplete
    lateralPosition: Incomplete
    longitudinalDistance: Incomplete
    longitudinalPosition: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (RelativePosition)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::situation::RelativePosition)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (RelativePosition)arg1, (RelativePosition)other) -> RelativePosition :

            C++ signature :
                ad::rss::situation::RelativePosition {lvalue} assign(ad::rss::situation::RelativePosition {lvalue},ad::rss::situation::RelativePosition)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (RelativePosition)arg1, (RelativePosition)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::situation::RelativePosition {lvalue},ad::rss::situation::RelativePosition)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (RelativePosition)arg1, (RelativePosition)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::situation::RelativePosition {lvalue},ad::rss::situation::RelativePosition)"""
    @classmethod
    def __reduce__(cls): ...

class Situation(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    egoVehicleState: Incomplete
    objectId: Incomplete
    otherVehicleState: Incomplete
    relativePosition: Incomplete
    situationId: Incomplete
    situationType: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Situation)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::situation::Situation)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Situation)arg1, (Situation)other) -> Situation :

            C++ signature :
                ad::rss::situation::Situation {lvalue} assign(ad::rss::situation::Situation {lvalue},ad::rss::situation::Situation)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Situation)arg1, (Situation)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::situation::Situation {lvalue},ad::rss::situation::Situation)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Situation)arg1, (Situation)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::situation::Situation {lvalue},ad::rss::situation::Situation)"""
    @classmethod
    def __reduce__(cls): ...

class SituationSnapshot(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    defaultEgoVehicleRssDynamics: Incomplete
    situations: Incomplete
    timeIndex: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (SituationSnapshot)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::situation::SituationSnapshot)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (SituationSnapshot)arg1, (SituationSnapshot)other) -> SituationSnapshot :

            C++ signature :
                ad::rss::situation::SituationSnapshot {lvalue} assign(ad::rss::situation::SituationSnapshot {lvalue},ad::rss::situation::SituationSnapshot)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (SituationSnapshot)arg1, (SituationSnapshot)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::situation::SituationSnapshot {lvalue},ad::rss::situation::SituationSnapshot)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (SituationSnapshot)arg1, (SituationSnapshot)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::situation::SituationSnapshot {lvalue},ad::rss::situation::SituationSnapshot)"""
    @classmethod
    def __reduce__(cls): ...

class SituationType(Boost.Python.enum):
    IntersectionEgoHasPriority: ClassVar[SituationType] = ...
    IntersectionObjectHasPriority: ClassVar[SituationType] = ...
    IntersectionSamePriority: ClassVar[SituationType] = ...
    NotRelevant: ClassVar[SituationType] = ...
    OppositeDirection: ClassVar[SituationType] = ...
    SameDirection: ClassVar[SituationType] = ...
    Unstructured: ClassVar[SituationType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class SituationVector(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def append(cls, *args, **kwargs):
        """
        append( (SituationVector)arg1, (Situation)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},ad::rss::situation::Situation)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (SituationVector)arg1, (Situation)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},ad::rss::situation::Situation)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (SituationVector)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (SituationVector)arg1, (Situation)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},ad::rss::situation::Situation)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (SituationVector)arg1, (int)arg2, (Situation)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},long,ad::rss::situation::Situation)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (SituationVector)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (SituationVector)arg1, (Situation)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},ad::rss::situation::Situation)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (SituationVector)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},long)

        __delitem__( (SituationVector)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (SituationVector)arg1, (int)arg2) -> Situation :

            C++ signature :
                ad::rss::situation::Situation {lvalue} __getitem__(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},long)

        __getitem__( (SituationVector)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (SituationVector)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (SituationVector)arg1, (int)arg2, (Situation)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},long,ad::rss::situation::Situation)

        __setitem__( (SituationVector)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class VehicleState(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    distanceToEnterIntersection: Incomplete
    distanceToLeaveIntersection: Incomplete
    dynamics: Incomplete
    hasPriority: Incomplete
    isInCorrectLane: Incomplete
    objectState: Incomplete
    objectType: Incomplete
    velocity: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (VehicleState)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::situation::VehicleState)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (VehicleState)arg1, (VehicleState)other) -> VehicleState :

            C++ signature :
                ad::rss::situation::VehicleState {lvalue} assign(ad::rss::situation::VehicleState {lvalue},ad::rss::situation::VehicleState)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (VehicleState)arg1, (VehicleState)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::situation::VehicleState {lvalue},ad::rss::situation::VehicleState)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (VehicleState)arg1, (VehicleState)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::situation::VehicleState {lvalue},ad::rss::situation::VehicleState)"""
    @classmethod
    def __reduce__(cls): ...

class VelocityRange(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    speedLat: Incomplete
    speedLon: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (VelocityRange)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::situation::VelocityRange)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (VelocityRange)arg1, (VelocityRange)other) -> VelocityRange :

            C++ signature :
                ad::rss::situation::VelocityRange {lvalue} assign(ad::rss::situation::VelocityRange {lvalue},ad::rss::situation::VelocityRange)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (VelocityRange)arg1, (VelocityRange)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::situation::VelocityRange {lvalue},ad::rss::situation::VelocityRange)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (VelocityRange)arg1, (VelocityRange)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::situation::VelocityRange {lvalue},ad::rss::situation::VelocityRange)"""
    @classmethod
    def __reduce__(cls): ...

def calculateAcceleratedLimitedMovement(*args, **kwargs):
    """
    calculateAcceleratedLimitedMovement( (Speed)currentSpeed, (Speed)maxSpeedOnAcceleration, (Acceleration)acceleration, (Duration)duration, (Speed)resultingSpeed, (Distance)distanceOffset) -> bool :

        C++ signature :
            bool calculateAcceleratedLimitedMovement(ad::physics::Speed,ad::physics::Speed,ad::physics::Acceleration,ad::physics::Duration,ad::physics::Speed {lvalue},ad::physics::Distance {lvalue})"""
def calculateDistanceOffsetInAcceleratedMovement(*args, **kwargs):
    """
    calculateDistanceOffsetInAcceleratedMovement( (Speed)speed, (Acceleration)acceleration, (Duration)duration, (Distance)distanceOffset) -> bool :

        C++ signature :
            bool calculateDistanceOffsetInAcceleratedMovement(ad::physics::Speed,ad::physics::Acceleration,ad::physics::Duration,ad::physics::Distance {lvalue})"""
def calculateLateralDistanceOffsetAfterStatedBrakingPattern(*args, **kwargs):
    """
    calculateLateralDistanceOffsetAfterStatedBrakingPattern( (Speed)currentLateralSpeed, (Duration)responseTime, (Acceleration)acceleration, (Acceleration)deceleration, (Distance)distanceOffset) -> bool :

        C++ signature :
            bool calculateLateralDistanceOffsetAfterStatedBrakingPattern(ad::physics::Speed,ad::physics::Duration,ad::physics::Acceleration,ad::physics::Acceleration,ad::physics::Distance {lvalue})"""
def calculateLongitudinalDistanceOffsetAfterStatedBrakingPattern(*args, **kwargs):
    """
    calculateLongitudinalDistanceOffsetAfterStatedBrakingPattern( (Speed)currentLongitudinalSpeed, (Speed)maxSpeedOnAcceleration, (Duration)responseTime, (Acceleration)acceleration, (Acceleration)deceleration, (Distance)distanceOffset) -> bool :

        C++ signature :
            bool calculateLongitudinalDistanceOffsetAfterStatedBrakingPattern(ad::physics::Speed,ad::physics::Speed,ad::physics::Duration,ad::physics::Acceleration,ad::physics::Acceleration,ad::physics::Distance {lvalue})"""
def calculateSafeLateralDistance(*args, **kwargs):
    """
    calculateSafeLateralDistance( (VehicleState)leftVehicle, (VehicleState)rightVehicle, (Distance)safeDistance) -> bool :

        C++ signature :
            bool calculateSafeLateralDistance(ad::rss::situation::VehicleState,ad::rss::situation::VehicleState,ad::physics::Distance {lvalue})"""
def calculateSafeLongitudinalDistanceOppositeDirection(*args, **kwargs):
    """
    calculateSafeLongitudinalDistanceOppositeDirection( (VehicleState)correctVehicle, (VehicleState)oppositeVehicle, (Distance)safeDistance) -> bool :

        C++ signature :
            bool calculateSafeLongitudinalDistanceOppositeDirection(ad::rss::situation::VehicleState,ad::rss::situation::VehicleState,ad::physics::Distance {lvalue})"""
def calculateSafeLongitudinalDistanceSameDirection(*args, **kwargs):
    """
    calculateSafeLongitudinalDistanceSameDirection( (VehicleState)leadingVehicle, (VehicleState)followingVehicle, (Distance)safeDistance) -> bool :

        C++ signature :
            bool calculateSafeLongitudinalDistanceSameDirection(ad::rss::situation::VehicleState,ad::rss::situation::VehicleState,ad::physics::Distance {lvalue})"""
def calculateSpeedAndDistanceOffset(*args, **kwargs):
    """
    calculateSpeedAndDistanceOffset( (Duration)duration, (Speed)currentSpeed, (Duration)responseTime, (Speed)maxSpeedOnAcceleration, (Acceleration)aUntilReponseTime, (Acceleration)aAfterResponseTime, (Speed)resultingSpeed, (Distance)distanceOffset) -> bool :

        C++ signature :
            bool calculateSpeedAndDistanceOffset(ad::physics::Duration,ad::physics::Speed,ad::physics::Duration,ad::physics::Speed,ad::physics::Acceleration,ad::physics::Acceleration,ad::physics::Speed {lvalue},ad::physics::Distance {lvalue})"""
def calculateSpeedInAcceleratedMovement(*args, **kwargs):
    """
    calculateSpeedInAcceleratedMovement( (Speed)speed, (Acceleration)acceleration, (Duration)duration, (Speed)resultingSpeed) -> bool :

        C++ signature :
            bool calculateSpeedInAcceleratedMovement(ad::physics::Speed,ad::physics::Acceleration,ad::physics::Duration,ad::physics::Speed {lvalue})"""
def calculateStoppingDistance(*args, **kwargs):
    """
    calculateStoppingDistance( (Speed)currentSpeed, (Acceleration)deceleration, (Distance)stoppingDistance) -> bool :

        C++ signature :
            bool calculateStoppingDistance(ad::physics::Speed,ad::physics::Acceleration,ad::physics::Distance {lvalue})"""
def calculateTimeToCoverDistance(*args, **kwargs):
    """
    calculateTimeToCoverDistance( (Speed)currentSpeed, (Speed)maxSpeedOnAcceleration, (Duration)responseTime, (Acceleration)aUntilResponseTime, (Acceleration)aAfterResponseTime, (Distance)distanceToCover, (Duration)requiredTime) -> bool :

        C++ signature :
            bool calculateTimeToCoverDistance(ad::physics::Speed,ad::physics::Speed,ad::physics::Duration,ad::physics::Acceleration,ad::physics::Acceleration,ad::physics::Distance,ad::physics::Duration {lvalue})"""
def calculateTimeToStop(*args, **kwargs):
    """
    calculateTimeToStop( (Speed)currentSpeed, (Duration)responseTime, (Speed)maxSpeedOnAcceleration, (Acceleration)aUntilResponseTime, (Acceleration)aAfterResponseTime, (Duration)stopDuration) -> bool :

        C++ signature :
            bool calculateTimeToStop(ad::physics::Speed,ad::physics::Duration,ad::physics::Speed,ad::physics::Acceleration,ad::physics::Acceleration,ad::physics::Duration {lvalue})"""
def checkSafeLateralDistance(*args, **kwargs):
    """
    checkSafeLateralDistance( (VehicleState)leftVehicle, (VehicleState)rightVehicle, (Distance)vehicleDistance, (Distance)safeDistance, (bool)isDistanceSafe) -> bool :

        C++ signature :
            bool checkSafeLateralDistance(ad::rss::situation::VehicleState,ad::rss::situation::VehicleState,ad::physics::Distance,ad::physics::Distance {lvalue},bool {lvalue})"""
def checkSafeLongitudinalDistanceOppositeDirection(*args, **kwargs):
    """
    checkSafeLongitudinalDistanceOppositeDirection( (VehicleState)correctVehicle, (VehicleState)oppositeVehicle, (Distance)vehicleDistance, (Distance)safeDistance, (bool)isDistanceSafe) -> bool :

        C++ signature :
            bool checkSafeLongitudinalDistanceOppositeDirection(ad::rss::situation::VehicleState,ad::rss::situation::VehicleState,ad::physics::Distance,ad::physics::Distance {lvalue},bool {lvalue})"""
def checkSafeLongitudinalDistanceSameDirection(*args, **kwargs):
    """
    checkSafeLongitudinalDistanceSameDirection( (VehicleState)leadingVehicle, (VehicleState)followingVehicle, (Distance)vehicleDistance, (Distance)safeDistance, (bool)isDistanceSafe) -> bool :

        C++ signature :
            bool checkSafeLongitudinalDistanceSameDirection(ad::rss::situation::VehicleState,ad::rss::situation::VehicleState,ad::physics::Distance,ad::physics::Distance {lvalue},bool {lvalue})"""
def checkStopInFrontIntersection(*args, **kwargs):
    """
    checkStopInFrontIntersection( (VehicleState)vehicle, (Distance)safeDistance, (bool)isDistanceSafe) -> bool :

        C++ signature :
            bool checkStopInFrontIntersection(ad::rss::situation::VehicleState,ad::physics::Distance {lvalue},bool {lvalue})"""
def fromString(*args, **kwargs):
    """
    fromString( (str)str) -> LateralRelativePosition :

        C++ signature :
            ad::rss::situation::LateralRelativePosition fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> LongitudinalRelativePosition :

        C++ signature :
            ad::rss::situation::LongitudinalRelativePosition fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> SituationType :

        C++ signature :
            ad::rss::situation::SituationType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
@overload
def toString(ad) -> Any:
    """
    toString( (LateralRelativePosition)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::situation::LateralRelativePosition)

    toString( (LongitudinalRelativePosition)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::situation::LongitudinalRelativePosition)

    toString( (SituationType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::situation::SituationType)"""
@overload
def toString(ad) -> Any:
    """
    toString( (LateralRelativePosition)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::situation::LateralRelativePosition)

    toString( (LongitudinalRelativePosition)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::situation::LongitudinalRelativePosition)

    toString( (SituationType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::situation::SituationType)"""
@overload
def toString(ad) -> Any:
    """
    toString( (LateralRelativePosition)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::situation::LateralRelativePosition)

    toString( (LongitudinalRelativePosition)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::situation::LongitudinalRelativePosition)

    toString( (SituationType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::situation::SituationType)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LateralRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LateralRelativePosition)

    to_string( (LongitudinalRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LongitudinalRelativePosition)

    to_string( (RelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::RelativePosition)

    to_string( (SituationType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationType)

    to_string( (VelocityRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VelocityRange)

    to_string( (VehicleState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VehicleState)

    to_string( (Situation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::Situation)

    to_string( (SituationVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> >)

    to_string( (SituationSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationSnapshot)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LateralRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LateralRelativePosition)

    to_string( (LongitudinalRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LongitudinalRelativePosition)

    to_string( (RelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::RelativePosition)

    to_string( (SituationType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationType)

    to_string( (VelocityRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VelocityRange)

    to_string( (VehicleState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VehicleState)

    to_string( (Situation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::Situation)

    to_string( (SituationVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> >)

    to_string( (SituationSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationSnapshot)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LateralRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LateralRelativePosition)

    to_string( (LongitudinalRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LongitudinalRelativePosition)

    to_string( (RelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::RelativePosition)

    to_string( (SituationType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationType)

    to_string( (VelocityRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VelocityRange)

    to_string( (VehicleState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VehicleState)

    to_string( (Situation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::Situation)

    to_string( (SituationVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> >)

    to_string( (SituationSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationSnapshot)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LateralRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LateralRelativePosition)

    to_string( (LongitudinalRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LongitudinalRelativePosition)

    to_string( (RelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::RelativePosition)

    to_string( (SituationType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationType)

    to_string( (VelocityRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VelocityRange)

    to_string( (VehicleState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VehicleState)

    to_string( (Situation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::Situation)

    to_string( (SituationVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> >)

    to_string( (SituationSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationSnapshot)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LateralRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LateralRelativePosition)

    to_string( (LongitudinalRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LongitudinalRelativePosition)

    to_string( (RelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::RelativePosition)

    to_string( (SituationType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationType)

    to_string( (VelocityRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VelocityRange)

    to_string( (VehicleState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VehicleState)

    to_string( (Situation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::Situation)

    to_string( (SituationVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> >)

    to_string( (SituationSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationSnapshot)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LateralRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LateralRelativePosition)

    to_string( (LongitudinalRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LongitudinalRelativePosition)

    to_string( (RelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::RelativePosition)

    to_string( (SituationType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationType)

    to_string( (VelocityRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VelocityRange)

    to_string( (VehicleState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VehicleState)

    to_string( (Situation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::Situation)

    to_string( (SituationVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> >)

    to_string( (SituationSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationSnapshot)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LateralRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LateralRelativePosition)

    to_string( (LongitudinalRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LongitudinalRelativePosition)

    to_string( (RelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::RelativePosition)

    to_string( (SituationType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationType)

    to_string( (VelocityRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VelocityRange)

    to_string( (VehicleState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VehicleState)

    to_string( (Situation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::Situation)

    to_string( (SituationVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> >)

    to_string( (SituationSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationSnapshot)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LateralRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LateralRelativePosition)

    to_string( (LongitudinalRelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::LongitudinalRelativePosition)

    to_string( (RelativePosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::RelativePosition)

    to_string( (SituationType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationType)

    to_string( (VelocityRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VelocityRange)

    to_string( (VehicleState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::VehicleState)

    to_string( (Situation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::Situation)

    to_string( (SituationVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::situation::Situation, std::allocator<ad::rss::situation::Situation> >)

    to_string( (SituationSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::situation::SituationSnapshot)"""
