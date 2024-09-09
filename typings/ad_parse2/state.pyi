import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

Brake: UnstructuredSceneResponse
BrakeMin: LongitudinalResponse
BrakeMinCorrect: LongitudinalResponse
ContinueForward: UnstructuredSceneResponse
DriveAway: UnstructuredSceneResponse
IntersectionEgoInFront: RssStateEvaluator
IntersectionEgoPriorityOtherAbleToStop: RssStateEvaluator
IntersectionOtherInFront: RssStateEvaluator
IntersectionOtherPriorityEgoAbleToStop: RssStateEvaluator
IntersectionOverlap: RssStateEvaluator
LateralDistance: RssStateEvaluator
LongitudinalDistanceOppositeDirection: RssStateEvaluator
LongitudinalDistanceOppositeDirectionEgoCorrectLane: RssStateEvaluator
LongitudinalDistanceSameDirectionEgoFront: RssStateEvaluator
LongitudinalDistanceSameDirectionOtherInFront: RssStateEvaluator

class AccelerationRestriction(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    lateralLeftRange: Incomplete
    lateralRightRange: Incomplete
    longitudinalRange: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (AccelerationRestriction)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::state::AccelerationRestriction)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (AccelerationRestriction)arg1, (AccelerationRestriction)other) -> AccelerationRestriction :

            C++ signature :
                ad::rss::state::AccelerationRestriction {lvalue} assign(ad::rss::state::AccelerationRestriction {lvalue},ad::rss::state::AccelerationRestriction)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (AccelerationRestriction)arg1, (AccelerationRestriction)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::state::AccelerationRestriction {lvalue},ad::rss::state::AccelerationRestriction)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (AccelerationRestriction)arg1, (AccelerationRestriction)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::state::AccelerationRestriction {lvalue},ad::rss::state::AccelerationRestriction)"""
    @classmethod
    def __reduce__(cls): ...

class HeadingRange(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    begin: Incomplete
    end: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (HeadingRange)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::state::HeadingRange)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (HeadingRange)arg1, (HeadingRange)other) -> HeadingRange :

            C++ signature :
                ad::rss::state::HeadingRange {lvalue} assign(ad::rss::state::HeadingRange {lvalue},ad::rss::state::HeadingRange)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (HeadingRange)arg1, (HeadingRange)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::state::HeadingRange {lvalue},ad::rss::state::HeadingRange)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (HeadingRange)arg1, (HeadingRange)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::state::HeadingRange {lvalue},ad::rss::state::HeadingRange)"""
    @classmethod
    def __reduce__(cls): ...

class HeadingRangeVector(Boost.Python.instance):
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
        append( (HeadingRangeVector)arg1, (HeadingRange)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},ad::rss::state::HeadingRange)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (HeadingRangeVector)arg1, (HeadingRange)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},ad::rss::state::HeadingRange)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (HeadingRangeVector)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (HeadingRangeVector)arg1, (HeadingRange)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},ad::rss::state::HeadingRange)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (HeadingRangeVector)arg1, (int)arg2, (HeadingRange)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},long,ad::rss::state::HeadingRange)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (HeadingRangeVector)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (HeadingRangeVector)arg1, (HeadingRange)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},ad::rss::state::HeadingRange)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (HeadingRangeVector)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},long)

        __delitem__( (HeadingRangeVector)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (HeadingRangeVector)arg1, (int)arg2) -> HeadingRange :

            C++ signature :
                ad::rss::state::HeadingRange {lvalue} __getitem__(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},long)

        __getitem__( (HeadingRangeVector)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (HeadingRangeVector)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (HeadingRangeVector)arg1, (int)arg2, (HeadingRange)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},long,ad::rss::state::HeadingRange)

        __setitem__( (HeadingRangeVector)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class LateralResponse(Boost.Python.enum):
    BrakeMin: ClassVar[LateralResponse] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class LateralRssState(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    alphaLat: Incomplete
    isSafe: Incomplete
    response: Incomplete
    rssStateInformation: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (LateralRssState)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::state::LateralRssState)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (LateralRssState)arg1, (LateralRssState)other) -> LateralRssState :

            C++ signature :
                ad::rss::state::LateralRssState {lvalue} assign(ad::rss::state::LateralRssState {lvalue},ad::rss::state::LateralRssState)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (LateralRssState)arg1, (LateralRssState)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::state::LateralRssState {lvalue},ad::rss::state::LateralRssState)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (LateralRssState)arg1, (LateralRssState)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::state::LateralRssState {lvalue},ad::rss::state::LateralRssState)"""
    @classmethod
    def __reduce__(cls): ...

class LongitudinalResponse(Boost.Python.enum):
    BrakeMin: ClassVar[LongitudinalResponse] = ...
    BrakeMinCorrect: ClassVar[LongitudinalResponse] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class LongitudinalRssState(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    alphaLon: Incomplete
    isSafe: Incomplete
    response: Incomplete
    rssStateInformation: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (LongitudinalRssState)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::state::LongitudinalRssState)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (LongitudinalRssState)arg1, (LongitudinalRssState)other) -> LongitudinalRssState :

            C++ signature :
                ad::rss::state::LongitudinalRssState {lvalue} assign(ad::rss::state::LongitudinalRssState {lvalue},ad::rss::state::LongitudinalRssState)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (LongitudinalRssState)arg1, (LongitudinalRssState)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::state::LongitudinalRssState {lvalue},ad::rss::state::LongitudinalRssState)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (LongitudinalRssState)arg1, (LongitudinalRssState)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::state::LongitudinalRssState {lvalue},ad::rss::state::LongitudinalRssState)"""
    @classmethod
    def __reduce__(cls): ...

class ProperResponse(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    accelerationRestrictions: Incomplete
    dangerousObjects: Incomplete
    headingRanges: Incomplete
    isSafe: Incomplete
    lateralResponseLeft: Incomplete
    lateralResponseRight: Incomplete
    longitudinalResponse: Incomplete
    timeIndex: Incomplete
    unstructuredSceneResponse: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (ProperResponse)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::state::ProperResponse)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ProperResponse)arg1, (ProperResponse)other) -> ProperResponse :

            C++ signature :
                ad::rss::state::ProperResponse {lvalue} assign(ad::rss::state::ProperResponse {lvalue},ad::rss::state::ProperResponse)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ProperResponse)arg1, (ProperResponse)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::state::ProperResponse {lvalue},ad::rss::state::ProperResponse)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ProperResponse)arg1, (ProperResponse)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::state::ProperResponse {lvalue},ad::rss::state::ProperResponse)"""
    @classmethod
    def __reduce__(cls): ...

class RssState(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    lateralStateLeft: Incomplete
    lateralStateRight: Incomplete
    longitudinalState: Incomplete
    objectId: Incomplete
    situationId: Incomplete
    situationType: Incomplete
    unstructuredSceneState: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (RssState)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::state::RssState)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (RssState)arg1, (RssState)other) -> RssState :

            C++ signature :
                ad::rss::state::RssState {lvalue} assign(ad::rss::state::RssState {lvalue},ad::rss::state::RssState)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (RssState)arg1, (RssState)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::state::RssState {lvalue},ad::rss::state::RssState)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (RssState)arg1, (RssState)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::state::RssState {lvalue},ad::rss::state::RssState)"""
    @classmethod
    def __reduce__(cls): ...

class RssStateEvaluator(Boost.Python.enum):
    IntersectionEgoInFront: ClassVar[RssStateEvaluator] = ...
    IntersectionEgoPriorityOtherAbleToStop: ClassVar[RssStateEvaluator] = ...
    IntersectionOtherInFront: ClassVar[RssStateEvaluator] = ...
    IntersectionOtherPriorityEgoAbleToStop: ClassVar[RssStateEvaluator] = ...
    IntersectionOverlap: ClassVar[RssStateEvaluator] = ...
    LateralDistance: ClassVar[RssStateEvaluator] = ...
    LongitudinalDistanceOppositeDirection: ClassVar[RssStateEvaluator] = ...
    LongitudinalDistanceOppositeDirectionEgoCorrectLane: ClassVar[RssStateEvaluator] = ...
    LongitudinalDistanceSameDirectionEgoFront: ClassVar[RssStateEvaluator] = ...
    LongitudinalDistanceSameDirectionOtherInFront: ClassVar[RssStateEvaluator] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class RssStateInformation(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    currentDistance: Incomplete
    evaluator: Incomplete
    safeDistance: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (RssStateInformation)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::state::RssStateInformation)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (RssStateInformation)arg1, (RssStateInformation)other) -> RssStateInformation :

            C++ signature :
                ad::rss::state::RssStateInformation {lvalue} assign(ad::rss::state::RssStateInformation {lvalue},ad::rss::state::RssStateInformation)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (RssStateInformation)arg1, (RssStateInformation)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::state::RssStateInformation {lvalue},ad::rss::state::RssStateInformation)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (RssStateInformation)arg1, (RssStateInformation)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::state::RssStateInformation {lvalue},ad::rss::state::RssStateInformation)"""
    @classmethod
    def __reduce__(cls): ...

class RssStateSnapshot(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    defaultEgoVehicleRssDynamics: Incomplete
    individualResponses: Incomplete
    timeIndex: Incomplete
    unstructuredSceneEgoInformation: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (RssStateSnapshot)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::state::RssStateSnapshot)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (RssStateSnapshot)arg1, (RssStateSnapshot)other) -> RssStateSnapshot :

            C++ signature :
                ad::rss::state::RssStateSnapshot {lvalue} assign(ad::rss::state::RssStateSnapshot {lvalue},ad::rss::state::RssStateSnapshot)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (RssStateSnapshot)arg1, (RssStateSnapshot)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::state::RssStateSnapshot {lvalue},ad::rss::state::RssStateSnapshot)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (RssStateSnapshot)arg1, (RssStateSnapshot)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::state::RssStateSnapshot {lvalue},ad::rss::state::RssStateSnapshot)"""
    @classmethod
    def __reduce__(cls): ...

class RssStateVector(Boost.Python.instance):
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
        append( (RssStateVector)arg1, (RssState)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},ad::rss::state::RssState)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (RssStateVector)arg1, (RssState)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},ad::rss::state::RssState)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (RssStateVector)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (RssStateVector)arg1, (RssState)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},ad::rss::state::RssState)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (RssStateVector)arg1, (int)arg2, (RssState)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},long,ad::rss::state::RssState)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (RssStateVector)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (RssStateVector)arg1, (RssState)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},ad::rss::state::RssState)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (RssStateVector)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},long)

        __delitem__( (RssStateVector)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (RssStateVector)arg1, (int)arg2) -> RssState :

            C++ signature :
                ad::rss::state::RssState {lvalue} __getitem__(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},long)

        __getitem__( (RssStateVector)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (RssStateVector)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (RssStateVector)arg1, (int)arg2, (RssState)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},long,ad::rss::state::RssState)

        __setitem__( (RssStateVector)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class UnstructuredSceneResponse(Boost.Python.enum):
    Brake: ClassVar[UnstructuredSceneResponse] = ...
    ContinueForward: ClassVar[UnstructuredSceneResponse] = ...
    DriveAway: ClassVar[UnstructuredSceneResponse] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class UnstructuredSceneRssState(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    alphaLon: Incomplete
    headingRange: Incomplete
    isSafe: Incomplete
    response: Incomplete
    rssStateInformation: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (UnstructuredSceneRssState)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::state::UnstructuredSceneRssState)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (UnstructuredSceneRssState)arg1, (UnstructuredSceneRssState)other) -> UnstructuredSceneRssState :

            C++ signature :
                ad::rss::state::UnstructuredSceneRssState {lvalue} assign(ad::rss::state::UnstructuredSceneRssState {lvalue},ad::rss::state::UnstructuredSceneRssState)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (UnstructuredSceneRssState)arg1, (UnstructuredSceneRssState)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::state::UnstructuredSceneRssState {lvalue},ad::rss::state::UnstructuredSceneRssState)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (UnstructuredSceneRssState)arg1, (UnstructuredSceneRssState)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::state::UnstructuredSceneRssState {lvalue},ad::rss::state::UnstructuredSceneRssState)"""
    @classmethod
    def __reduce__(cls): ...

class UnstructuredSceneStateInformation(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    brakeTrajectorySet: Incomplete
    continueForwardTrajectorySet: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (UnstructuredSceneStateInformation)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::state::UnstructuredSceneStateInformation)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (UnstructuredSceneStateInformation)arg1, (UnstructuredSceneStateInformation)other) -> UnstructuredSceneStateInformation :

            C++ signature :
                ad::rss::state::UnstructuredSceneStateInformation {lvalue} assign(ad::rss::state::UnstructuredSceneStateInformation {lvalue},ad::rss::state::UnstructuredSceneStateInformation)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (UnstructuredSceneStateInformation)arg1, (UnstructuredSceneStateInformation)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::state::UnstructuredSceneStateInformation {lvalue},ad::rss::state::UnstructuredSceneStateInformation)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (UnstructuredSceneStateInformation)arg1, (UnstructuredSceneStateInformation)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::state::UnstructuredSceneStateInformation {lvalue},ad::rss::state::UnstructuredSceneStateInformation)"""
    @classmethod
    def __reduce__(cls): ...

def fromString(*args, **kwargs):
    """
    fromString( (str)str) -> UnstructuredSceneResponse :

        C++ signature :
            ad::rss::state::UnstructuredSceneResponse fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> LateralResponse :

        C++ signature :
            ad::rss::state::LateralResponse fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> RssStateEvaluator :

        C++ signature :
            ad::rss::state::RssStateEvaluator fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> LongitudinalResponse :

        C++ signature :
            ad::rss::state::LongitudinalResponse fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
def isDangerous(ad) -> Any:
    """
    isDangerous( (RssState)rssState) -> bool :

        C++ signature :
            bool isDangerous(ad::rss::state::RssState)"""
def isLateralSafe(ad) -> Any:
    """
    isLateralSafe( (RssState)rssState) -> bool :

        C++ signature :
            bool isLateralSafe(ad::rss::state::RssState)"""
def isLongitudinalSafe(ad) -> Any:
    """
    isLongitudinalSafe( (RssState)rssState) -> bool :

        C++ signature :
            bool isLongitudinalSafe(ad::rss::state::RssState)"""
def isUnstructuredSceneSafe(ad) -> Any:
    """
    isUnstructuredSceneSafe( (RssState)rssState) -> bool :

        C++ signature :
            bool isUnstructuredSceneSafe(ad::rss::state::RssState)"""
@overload
def toString(ad) -> Any:
    """
    toString( (UnstructuredSceneResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::UnstructuredSceneResponse)

    toString( (LateralResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::LateralResponse)

    toString( (RssStateEvaluator)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::RssStateEvaluator)

    toString( (LongitudinalResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::LongitudinalResponse)"""
@overload
def toString(ad) -> Any:
    """
    toString( (UnstructuredSceneResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::UnstructuredSceneResponse)

    toString( (LateralResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::LateralResponse)

    toString( (RssStateEvaluator)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::RssStateEvaluator)

    toString( (LongitudinalResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::LongitudinalResponse)"""
@overload
def toString(ad) -> Any:
    """
    toString( (UnstructuredSceneResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::UnstructuredSceneResponse)

    toString( (LateralResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::LateralResponse)

    toString( (RssStateEvaluator)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::RssStateEvaluator)

    toString( (LongitudinalResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::LongitudinalResponse)"""
@overload
def toString(ad) -> Any:
    """
    toString( (UnstructuredSceneResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::UnstructuredSceneResponse)

    toString( (LateralResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::LateralResponse)

    toString( (RssStateEvaluator)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::RssStateEvaluator)

    toString( (LongitudinalResponse)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::state::LongitudinalResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (HeadingRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::HeadingRange)

    to_string( (UnstructuredSceneResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneResponse)

    to_string( (UnstructuredSceneStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneStateInformation)

    to_string( (UnstructuredSceneRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::UnstructuredSceneRssState)

    to_string( (LateralResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralResponse)

    to_string( (RssStateEvaluator)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateEvaluator)

    to_string( (RssStateInformation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateInformation)

    to_string( (LateralRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LateralRssState)

    to_string( (LongitudinalResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalResponse)

    to_string( (LongitudinalRssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::LongitudinalRssState)

    to_string( (RssState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssState)

    to_string( (RssStateVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::RssState, std::allocator<ad::rss::state::RssState> >)

    to_string( (RssStateSnapshot)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::RssStateSnapshot)

    to_string( (HeadingRangeVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> >)

    to_string( (AccelerationRestriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::AccelerationRestriction)

    to_string( (ProperResponse)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::state::ProperResponse)"""
