import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

from carla.libcarla import _CarlaEnum

AllNeighborLanes: RouteCreationMode
AllRoutableLanes: RouteCreationMode
AllRouteLanes: RouteSectionCreationMode
DONT_CARE: RoutingDirection
Differ: CompareRouteResult
DontCutIntersectionAndPrependIfSucceededBeforeRoute: ShortenRouteMode
Equal: CompareRouteResult
FailedRouteEmpty: ShortenRouteResult
Following: ConnectingRouteType
Invalid: LaneChangeDirection
LeftToRight: LaneChangeDirection
Longer: CompareRouteResult
Merging: ConnectingRouteType
NEGATIVE: RoutingDirection
Normal: ShortenRouteMode
Off: FilterDuplicatesMode
OnlyEqual: FilterDuplicatesMode
Opposing: ConnectingRouteType
POSITIVE: RoutingDirection
PrependIfSucceededBeforeRoute: ShortenRouteMode
RightToLeft: LaneChangeDirection
SameDrivingDirection: RouteCreationMode
Shorter: CompareRouteResult
SingleLane: RouteSectionCreationMode
SubRoutesPreferLongerOnes: FilterDuplicatesMode
SubRoutesPreferShorterOnes: FilterDuplicatesMode
Succeeded: ShortenRouteResult
SucceededBeforeRoute: ShortenRouteResult
SucceededIntersectionNotCut: ShortenRouteResult
SucceededRouteEmpty: ShortenRouteResult
Undefined: RouteCreationMode

class CompareRouteResult(Boost.Python.enum):
    Differ: ClassVar[CompareRouteResult] = ...
    Equal: ClassVar[CompareRouteResult] = ...
    Longer: ClassVar[CompareRouteResult] = ...
    Shorter: ClassVar[CompareRouteResult] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class ConnectingRoute(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    routeA: Incomplete
    routeB: Incomplete
    type: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (ConnectingRoute)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::ConnectingRoute)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ConnectingRoute)arg1, (ConnectingRoute)other) -> ConnectingRoute :

            C++ signature :
                ad::map::route::ConnectingRoute {lvalue} assign(ad::map::route::ConnectingRoute {lvalue},ad::map::route::ConnectingRoute)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ConnectingRoute)arg1, (ConnectingRoute)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::route::ConnectingRoute {lvalue},ad::map::route::ConnectingRoute)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ConnectingRoute)arg1, (ConnectingRoute)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::route::ConnectingRoute {lvalue},ad::map::route::ConnectingRoute)"""
    @classmethod
    def __reduce__(cls): ...

class ConnectingRouteType(Boost.Python.enum):
    Following: ClassVar[ConnectingRouteType] = ...
    Invalid: ClassVar[ConnectingRouteType] = ...
    Merging: ClassVar[ConnectingRouteType] = ...
    Opposing: ClassVar[ConnectingRouteType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class FilterDuplicatesMode(Boost.Python.enum):
    Off: ClassVar[FilterDuplicatesMode] = ...
    OnlyEqual: ClassVar[FilterDuplicatesMode] = ...
    SubRoutesPreferLongerOnes: ClassVar[FilterDuplicatesMode] = ...
    SubRoutesPreferShorterOnes: ClassVar[FilterDuplicatesMode] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class FindLaneChangeResult(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    laneChangeDirection: Incomplete
    laneChangeEndLaneSegmentIterator: Incomplete
    laneChangeEndRouteIterator: Incomplete
    laneChangeStartLaneSegmentIterator: Incomplete
    laneChangeStartRouteIterator: Incomplete
    numberOfConnectedLaneChanges: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1, (FullRoute)route) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::FullRoute)"""
    @classmethod
    def get_queryRoute(cls, ad) -> Any:
        """
        get_queryRoute( (FindLaneChangeResult)arg1) -> FullRoute :

            C++ signature :
                ad::map::route::FullRoute get_queryRoute(ad::map::route::FindLaneChangeResult {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @property
    def Valid(self): ...
    @property
    def calcZoneLength(self): ...

class FindWaypointResult(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    laneSegmentIterator: Incomplete
    queryPosition: Incomplete
    roadSegmentIterator: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1, (FullRoute)route) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::FullRoute)

        __init__( (object)arg1, (FullRoute)route, (ParaPoint)iQueryPosition, (object)roadSegmentIter, (object)laneIntervalIter) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::FullRoute,ad::map::point::ParaPoint,__gnu_cxx::__normal_iterator<ad::map::route::RoadSegment const*, std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > >,__gnu_cxx::__normal_iterator<ad::map::route::LaneSegment const*, std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > >)

        __init__( (object)arg1, (FindWaypointResult)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::FindWaypointResult)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (FindWaypointResult)arg1, (FindWaypointResult)other) -> FindWaypointResult :

            C++ signature :
                ad::map::route::FindWaypointResult {lvalue} assign(ad::map::route::FindWaypointResult {lvalue},ad::map::route::FindWaypointResult)"""
    @classmethod
    def get_queryRoute(cls, ad) -> Any:
        """
        get_queryRoute( (FindWaypointResult)arg1) -> FullRoute :

            C++ signature :
                ad::map::route::FullRoute get_queryRoute(ad::map::route::FindWaypointResult {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @property
    def LeftLane(self): ...
    @property
    def PredecessorLanes(self): ...
    @property
    def RightLane(self): ...
    @property
    def SuccessorLanes(self): ...
    @property
    def Valid(self): ...

class FullRoute(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    destinationLaneOffset: Incomplete
    fullRouteSegmentCount: Incomplete
    maxLaneOffset: Incomplete
    minLaneOffset: Incomplete
    roadSegments: Incomplete
    routeCreationMode: Incomplete
    routePlanningCounter: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (FullRoute)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::FullRoute)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (FullRoute)arg1, (FullRoute)other) -> FullRoute :

            C++ signature :
                ad::map::route::FullRoute {lvalue} assign(ad::map::route::FullRoute {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (FullRoute)arg1, (FullRoute)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::route::FullRoute {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (FullRoute)arg1, (FullRoute)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::route::FullRoute {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def __reduce__(cls): ...

class FullRouteList(Boost.Python.instance):
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
        append( (FullRouteList)arg1, (FullRoute)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (FullRouteList)arg1, (FullRoute)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (FullRouteList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (FullRouteList)arg1, (FullRoute)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (FullRouteList)arg1, (int)arg2, (FullRoute)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},long,ad::map::route::FullRoute)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (FullRouteList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (FullRouteList)arg1, (FullRoute)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (FullRouteList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},long)

        __delitem__( (FullRouteList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (FullRouteList)arg1, (int)arg2) -> FullRoute :

            C++ signature :
                ad::map::route::FullRoute {lvalue} __getitem__(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},long)

        __getitem__( (FullRouteList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (FullRouteList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (FullRouteList)arg1, (int)arg2, (FullRoute)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},long,ad::map::route::FullRoute)

        __setitem__( (FullRouteList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class LaneChangeDirection(Boost.Python.enum):
    Invalid: ClassVar[LaneChangeDirection] = ...
    LeftToRight: ClassVar[LaneChangeDirection] = ...
    RightToLeft: ClassVar[LaneChangeDirection] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class LaneInterval(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    end: Incomplete
    laneId: Incomplete
    start: Incomplete
    wrongWay: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (LaneInterval)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::LaneInterval)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (LaneInterval)arg1, (LaneInterval)other) -> LaneInterval :

            C++ signature :
                ad::map::route::LaneInterval {lvalue} assign(ad::map::route::LaneInterval {lvalue},ad::map::route::LaneInterval)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (LaneInterval)arg1, (LaneInterval)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::route::LaneInterval {lvalue},ad::map::route::LaneInterval)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (LaneInterval)arg1, (LaneInterval)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::route::LaneInterval {lvalue},ad::map::route::LaneInterval)"""
    @classmethod
    def __reduce__(cls): ...

class LaneSegment(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    laneInterval: Incomplete
    leftNeighbor: Incomplete
    predecessors: Incomplete
    rightNeighbor: Incomplete
    routeLaneOffset: Incomplete
    successors: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (LaneSegment)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::LaneSegment)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (LaneSegment)arg1, (LaneSegment)other) -> LaneSegment :

            C++ signature :
                ad::map::route::LaneSegment {lvalue} assign(ad::map::route::LaneSegment {lvalue},ad::map::route::LaneSegment)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (LaneSegment)arg1, (LaneSegment)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::route::LaneSegment {lvalue},ad::map::route::LaneSegment)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (LaneSegment)arg1, (LaneSegment)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::route::LaneSegment {lvalue},ad::map::route::LaneSegment)"""
    @classmethod
    def __reduce__(cls): ...

class LaneSegmentList(Boost.Python.instance):
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
        append( (LaneSegmentList)arg1, (LaneSegment)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},ad::map::route::LaneSegment)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (LaneSegmentList)arg1, (LaneSegment)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},ad::map::route::LaneSegment)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (LaneSegmentList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (LaneSegmentList)arg1, (LaneSegment)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},ad::map::route::LaneSegment)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (LaneSegmentList)arg1, (int)arg2, (LaneSegment)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},long,ad::map::route::LaneSegment)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (LaneSegmentList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (LaneSegmentList)arg1, (LaneSegment)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},ad::map::route::LaneSegment)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (LaneSegmentList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},long)

        __delitem__( (LaneSegmentList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (LaneSegmentList)arg1, (int)arg2) -> LaneSegment :

            C++ signature :
                ad::map::route::LaneSegment {lvalue} __getitem__(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},long)

        __getitem__( (LaneSegmentList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (LaneSegmentList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (LaneSegmentList)arg1, (int)arg2, (LaneSegment)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},long,ad::map::route::LaneSegment)

        __setitem__( (LaneSegmentList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class RoadSegment(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    boundingSphere: Incomplete
    drivableLaneSegments: Incomplete
    segmentCountFromDestination: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (RoadSegment)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::RoadSegment)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (RoadSegment)arg1, (RoadSegment)other) -> RoadSegment :

            C++ signature :
                ad::map::route::RoadSegment {lvalue} assign(ad::map::route::RoadSegment {lvalue},ad::map::route::RoadSegment)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (RoadSegment)arg1, (RoadSegment)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::route::RoadSegment {lvalue},ad::map::route::RoadSegment)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (RoadSegment)arg1, (RoadSegment)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::route::RoadSegment {lvalue},ad::map::route::RoadSegment)"""
    @classmethod
    def __reduce__(cls): ...

class RoadSegmentList(Boost.Python.instance):
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
        append( (RoadSegmentList)arg1, (RoadSegment)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},ad::map::route::RoadSegment)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (RoadSegmentList)arg1, (RoadSegment)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},ad::map::route::RoadSegment)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (RoadSegmentList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (RoadSegmentList)arg1, (RoadSegment)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},ad::map::route::RoadSegment)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (RoadSegmentList)arg1, (int)arg2, (RoadSegment)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},long,ad::map::route::RoadSegment)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (RoadSegmentList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (RoadSegmentList)arg1, (RoadSegment)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},ad::map::route::RoadSegment)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (RoadSegmentList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},long)

        __delitem__( (RoadSegmentList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (RoadSegmentList)arg1, (int)arg2) -> RoadSegment :

            C++ signature :
                ad::map::route::RoadSegment {lvalue} __getitem__(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},long)

        __getitem__( (RoadSegmentList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (RoadSegmentList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (RoadSegmentList)arg1, (int)arg2, (RoadSegment)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},long,ad::map::route::RoadSegment)

        __setitem__( (RoadSegmentList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Route(Boost.Python.instance):
    class RawRoute(Boost.Python.instance):
        __instance_size__: ClassVar[int] = ...
        paraPointList: Incomplete
        routeDistance: Incomplete
        routeDuration: Incomplete
        @classmethod
        def __init__(cls, *args, **kwargs) -> None:
            """
            __init__( (object)arg1) -> None :

                C++ signature :
                    void __init__(_object*)"""
        @classmethod
        def __reduce__(cls): ...

    class Type(int, _CarlaEnum):
        INVALID = 0
        SHORTEST = 1
        SHORTEST_IGNORE_DIRECTION = 2
    INVALID: ClassVar[Type] = ...
    SHORTEST: ClassVar[Type] = ...
    SHORTEST_IGNORE_DIRECTION: ClassVar[Type] = ...
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1, (RoutingParaPoint)start, (RoutingParaPoint)dest, (Distance)maxDistance, (Duration)maxDuration, (Type)routingType) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::planning::RoutingParaPoint,ad::map::route::planning::RoutingParaPoint,ad::physics::Distance,ad::physics::Duration,ad::map::route::planning::Route::Type)"""
    @classmethod
    def calculate(cls, ad) -> Any:
        """
        calculate( (Route)arg1) -> bool :

            C++ signature :
                bool calculate(ad::map::route::planning::Route {lvalue})

        calculate( (Route)arg1) -> None :

            C++ signature :
                void calculate(Route_wrapper {lvalue})"""
    @classmethod
    def getBasicRoute(cls, ad) -> Any:
        """
        getBasicRoute( (Route)arg1 [, (object)routeIndex=0]) -> object :

            C++ signature :
                std::vector<std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >, std::allocator<std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > > > getBasicRoute(ad::map::route::planning::Route {lvalue} [,unsigned long=0])"""
    @classmethod
    def getRawRoute(cls, ad) -> Any:
        """
        getRawRoute( (Route)arg1 [, (object)routeIndex=0]) -> RawRoute :

            C++ signature :
                ad::map::route::planning::Route::RawRoute getRawRoute(ad::map::route::planning::Route {lvalue} [,unsigned long=0])"""
    @classmethod
    def getType(cls, ad) -> Any:
        """
        getType( (Route)arg1) -> Type :

            C++ signature :
                ad::map::route::planning::Route::Type getType(ad::map::route::planning::Route {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @property
    def BasicRoutes(self): ...
    @property
    def Dest(self): ...
    @property
    def RawRoutes(self): ...
    @property
    def RoutingDest(self): ...
    @property
    def RoutingStart(self): ...
    @property
    def Start(self): ...
    @property
    def Valid(self): ...
    @property
    def laneDirectionIsIgnored(self): ...

class RouteCreationMode(Boost.Python.enum):
    AllNeighborLanes: ClassVar[RouteCreationMode] = ...
    AllRoutableLanes: ClassVar[RouteCreationMode] = ...
    SameDrivingDirection: ClassVar[RouteCreationMode] = ...
    Undefined: ClassVar[RouteCreationMode] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class RouteIterator(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    roadSegmentIterator: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1, (FullRoute)iRoute, (object)iRoadSegmentIterator) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::FullRoute,__gnu_cxx::__normal_iterator<ad::map::route::RoadSegment const*, std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > >)"""
    @classmethod
    def get_route(cls, ad) -> Any:
        """
        get_route( (RouteIterator)arg1) -> FullRoute :

            C++ signature :
                ad::map::route::FullRoute get_route(ad::map::route::RouteIterator {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @property
    def Valid(self): ...

class RouteParaPoint(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    parametricOffset: Incomplete
    routePlanningCounter: Incomplete
    segmentCountFromDestination: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (RouteParaPoint)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::route::RouteParaPoint)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (RouteParaPoint)arg1, (RouteParaPoint)other) -> RouteParaPoint :

            C++ signature :
                ad::map::route::RouteParaPoint {lvalue} assign(ad::map::route::RouteParaPoint {lvalue},ad::map::route::RouteParaPoint)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (RouteParaPoint)arg1, (RouteParaPoint)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::route::RouteParaPoint {lvalue},ad::map::route::RouteParaPoint)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (RouteParaPoint)arg1, (RouteParaPoint)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::route::RouteParaPoint {lvalue},ad::map::route::RouteParaPoint)"""
    @classmethod
    def __reduce__(cls): ...

class RouteSectionCreationMode(Boost.Python.enum):
    AllRouteLanes: ClassVar[RouteSectionCreationMode] = ...
    SingleLane: ClassVar[RouteSectionCreationMode] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class RoutingDirection(Boost.Python.enum):
    DONT_CARE: ClassVar[RoutingDirection] = ...
    NEGATIVE: ClassVar[RoutingDirection] = ...
    POSITIVE: ClassVar[RoutingDirection] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class RoutingParaPoint(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    direction: Incomplete
    point: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (RoutingParaPoint)arg1, (RoutingParaPoint)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::route::planning::RoutingParaPoint {lvalue},ad::map::route::planning::RoutingParaPoint)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (RoutingParaPoint)arg1, (RoutingParaPoint)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::map::route::planning::RoutingParaPoint {lvalue},ad::map::route::planning::RoutingParaPoint)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (RoutingParaPoint)arg1, (RoutingParaPoint)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::route::planning::RoutingParaPoint {lvalue},ad::map::route::planning::RoutingParaPoint)"""
    @classmethod
    def __reduce__(cls): ...

class ShortenRouteMode(Boost.Python.enum):
    DontCutIntersectionAndPrependIfSucceededBeforeRoute: ClassVar[ShortenRouteMode] = ...
    Normal: ClassVar[ShortenRouteMode] = ...
    PrependIfSucceededBeforeRoute: ClassVar[ShortenRouteMode] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class ShortenRouteResult(Boost.Python.enum):
    FailedRouteEmpty: ClassVar[ShortenRouteResult] = ...
    Succeeded: ClassVar[ShortenRouteResult] = ...
    SucceededBeforeRoute: ClassVar[ShortenRouteResult] = ...
    SucceededIntersectionNotCut: ClassVar[ShortenRouteResult] = ...
    SucceededRouteEmpty: ClassVar[ShortenRouteResult] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_(Boost.Python.instance):
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
        append( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (RoutingParaPoint)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},ad::map::route::planning::RoutingParaPoint)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (RoutingParaPoint)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},ad::map::route::planning::RoutingParaPoint)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (RoutingParaPoint)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},ad::map::route::planning::RoutingParaPoint)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (int)arg2, (RoutingParaPoint)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},long,ad::map::route::planning::RoutingParaPoint)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (RoutingParaPoint)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},ad::map::route::planning::RoutingParaPoint)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},long)

        __delitem__( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (int)arg2) -> RoutingParaPoint :

            C++ signature :
                ad::map::route::planning::RoutingParaPoint {lvalue} __getitem__(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},long)

        __getitem__( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (int)arg2, (RoutingParaPoint)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},long,ad::map::route::planning::RoutingParaPoint)

        __setitem__( (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

def addOpposingLaneSegmentToRoadSegment(*args, **kwargs):
    """
    addOpposingLaneSegmentToRoadSegment( (ParaPoint)startpoint, (Distance)distance, (RoadSegment)roadSegment, (FullRoute)route) -> Distance :

        C++ signature :
            ad::physics::Distance addOpposingLaneSegmentToRoadSegment(ad::map::point::ParaPoint,ad::physics::Distance,ad::map::route::RoadSegment {lvalue},ad::map::route::FullRoute {lvalue})"""
def addOpposingLaneToRoute(*args, **kwargs):
    """
    addOpposingLaneToRoute( (ParaPoint)pointOnOppositeLane, (Distance)distanceOnWrongLane, (FullRoute)route, (Distance)coveredDistance) -> bool :

        C++ signature :
            bool addOpposingLaneToRoute(ad::map::point::ParaPoint,ad::physics::Distance,ad::map::route::FullRoute {lvalue},ad::physics::Distance {lvalue})"""
def appendLaneSegmentToRoute(*args, **kwargs):
    """
    appendLaneSegmentToRoute( (LaneInterval)laneInterval, (FullRoute)route [, (object)segmentCountFromDestination=0]) -> None :

        C++ signature :
            void appendLaneSegmentToRoute(ad::map::route::LaneInterval,ad::map::route::FullRoute {lvalue} [,unsigned long=0])"""
def appendRoadSegmentToRoute(*args, **kwargs):
    """
    appendRoadSegmentToRoute( (LaneInterval)laneInverval, (GBufferTextureID)laneOffset, (FullRoute)route, (LaneIdSet)relevantLanes) -> None :

        C++ signature :
            void appendRoadSegmentToRoute(ad::map::route::LaneInterval,int,ad::map::route::FullRoute {lvalue},std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
@overload
def calcDuration(ad) -> Any:
    """
    calcDuration( (FullRoute)fullRoute) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::FullRoute)

    calcDuration( (RoadSegment)roadSegment) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::RoadSegment)

    calcDuration( (LaneSegment)laneSegment) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::LaneSegment)

    calcDuration( (ConnectingRoute)connectingRoute) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::ConnectingRoute)

    calcDuration( (LaneInterval)laneInterval) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::LaneInterval)"""
@overload
def calcDuration(ad) -> Any:
    """
    calcDuration( (FullRoute)fullRoute) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::FullRoute)

    calcDuration( (RoadSegment)roadSegment) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::RoadSegment)

    calcDuration( (LaneSegment)laneSegment) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::LaneSegment)

    calcDuration( (ConnectingRoute)connectingRoute) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::ConnectingRoute)

    calcDuration( (LaneInterval)laneInterval) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::LaneInterval)"""
@overload
def calcDuration(ad) -> Any:
    """
    calcDuration( (FullRoute)fullRoute) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::FullRoute)

    calcDuration( (RoadSegment)roadSegment) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::RoadSegment)

    calcDuration( (LaneSegment)laneSegment) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::LaneSegment)

    calcDuration( (ConnectingRoute)connectingRoute) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::ConnectingRoute)

    calcDuration( (LaneInterval)laneInterval) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::LaneInterval)"""
@overload
def calcDuration(ad) -> Any:
    """
    calcDuration( (FullRoute)fullRoute) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::FullRoute)

    calcDuration( (RoadSegment)roadSegment) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::RoadSegment)

    calcDuration( (LaneSegment)laneSegment) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::LaneSegment)

    calcDuration( (ConnectingRoute)connectingRoute) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::ConnectingRoute)

    calcDuration( (LaneInterval)laneInterval) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::LaneInterval)"""
@overload
def calcDuration(ad) -> Any:
    """
    calcDuration( (FullRoute)fullRoute) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::FullRoute)

    calcDuration( (RoadSegment)roadSegment) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::RoadSegment)

    calcDuration( (LaneSegment)laneSegment) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::LaneSegment)

    calcDuration( (ConnectingRoute)connectingRoute) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::ConnectingRoute)

    calcDuration( (LaneInterval)laneInterval) -> Duration :

        C++ signature :
            ad::physics::Duration calcDuration(ad::map::route::LaneInterval)"""
@overload
def calcLength(ad) -> Any:
    """
    calcLength( (FullRoute)fullRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FullRoute)

    calcLength( (RoadSegment)roadSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RoadSegment)

    calcLength( (LaneSegment)laneSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneSegment)

    calcLength( (ConnectingRoute)connectingRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::ConnectingRoute)

    calcLength( (RouteIterator)startIterator, (RouteIterator)endIterator) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteIterator,ad::map::route::RouteIterator)

    calcLength( (RouteParaPoint)startRouteParaPoint, (RouteParaPoint)endRouteParaPoint, (FullRoute)route) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteParaPoint,ad::map::route::RouteParaPoint,ad::map::route::FullRoute)

    calcLength( (FindWaypointResult)findWaypointResult) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FindWaypointResult)

    calcLength( (LaneInterval)laneInterval) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneInterval)"""
@overload
def calcLength(ad) -> Any:
    """
    calcLength( (FullRoute)fullRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FullRoute)

    calcLength( (RoadSegment)roadSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RoadSegment)

    calcLength( (LaneSegment)laneSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneSegment)

    calcLength( (ConnectingRoute)connectingRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::ConnectingRoute)

    calcLength( (RouteIterator)startIterator, (RouteIterator)endIterator) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteIterator,ad::map::route::RouteIterator)

    calcLength( (RouteParaPoint)startRouteParaPoint, (RouteParaPoint)endRouteParaPoint, (FullRoute)route) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteParaPoint,ad::map::route::RouteParaPoint,ad::map::route::FullRoute)

    calcLength( (FindWaypointResult)findWaypointResult) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FindWaypointResult)

    calcLength( (LaneInterval)laneInterval) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneInterval)"""
@overload
def calcLength(ad) -> Any:
    """
    calcLength( (FullRoute)fullRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FullRoute)

    calcLength( (RoadSegment)roadSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RoadSegment)

    calcLength( (LaneSegment)laneSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneSegment)

    calcLength( (ConnectingRoute)connectingRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::ConnectingRoute)

    calcLength( (RouteIterator)startIterator, (RouteIterator)endIterator) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteIterator,ad::map::route::RouteIterator)

    calcLength( (RouteParaPoint)startRouteParaPoint, (RouteParaPoint)endRouteParaPoint, (FullRoute)route) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteParaPoint,ad::map::route::RouteParaPoint,ad::map::route::FullRoute)

    calcLength( (FindWaypointResult)findWaypointResult) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FindWaypointResult)

    calcLength( (LaneInterval)laneInterval) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneInterval)"""
@overload
def calcLength(ad) -> Any:
    """
    calcLength( (FullRoute)fullRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FullRoute)

    calcLength( (RoadSegment)roadSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RoadSegment)

    calcLength( (LaneSegment)laneSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneSegment)

    calcLength( (ConnectingRoute)connectingRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::ConnectingRoute)

    calcLength( (RouteIterator)startIterator, (RouteIterator)endIterator) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteIterator,ad::map::route::RouteIterator)

    calcLength( (RouteParaPoint)startRouteParaPoint, (RouteParaPoint)endRouteParaPoint, (FullRoute)route) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteParaPoint,ad::map::route::RouteParaPoint,ad::map::route::FullRoute)

    calcLength( (FindWaypointResult)findWaypointResult) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FindWaypointResult)

    calcLength( (LaneInterval)laneInterval) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneInterval)"""
@overload
def calcLength(ad) -> Any:
    """
    calcLength( (FullRoute)fullRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FullRoute)

    calcLength( (RoadSegment)roadSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RoadSegment)

    calcLength( (LaneSegment)laneSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneSegment)

    calcLength( (ConnectingRoute)connectingRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::ConnectingRoute)

    calcLength( (RouteIterator)startIterator, (RouteIterator)endIterator) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteIterator,ad::map::route::RouteIterator)

    calcLength( (RouteParaPoint)startRouteParaPoint, (RouteParaPoint)endRouteParaPoint, (FullRoute)route) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteParaPoint,ad::map::route::RouteParaPoint,ad::map::route::FullRoute)

    calcLength( (FindWaypointResult)findWaypointResult) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FindWaypointResult)

    calcLength( (LaneInterval)laneInterval) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneInterval)"""
@overload
def calcLength(ad) -> Any:
    """
    calcLength( (FullRoute)fullRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FullRoute)

    calcLength( (RoadSegment)roadSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RoadSegment)

    calcLength( (LaneSegment)laneSegment) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneSegment)

    calcLength( (ConnectingRoute)connectingRoute) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::ConnectingRoute)

    calcLength( (RouteIterator)startIterator, (RouteIterator)endIterator) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteIterator,ad::map::route::RouteIterator)

    calcLength( (RouteParaPoint)startRouteParaPoint, (RouteParaPoint)endRouteParaPoint, (FullRoute)route) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::RouteParaPoint,ad::map::route::RouteParaPoint,ad::map::route::FullRoute)

    calcLength( (FindWaypointResult)findWaypointResult) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::FindWaypointResult)

    calcLength( (LaneInterval)laneInterval) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::route::LaneInterval)"""
def calcParametricLength(ad) -> Any:
    """
    calcParametricLength( (LaneInterval)laneInterval) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue calcParametricLength(ad::map::route::LaneInterval)"""
def calculateBypassingRoute(*args, **kwargs):
    """
    calculateBypassingRoute( (FullRoute)route, (FullRoute)bypassingRoute) -> bool :

        C++ signature :
            bool calculateBypassingRoute(ad::map::route::FullRoute,ad::map::route::FullRoute {lvalue})"""
def calculateConnectingRoute(*args, **kwargs):
    """
    calculateConnectingRoute( (Object)startObject, (Object)destObject, (Distance)maxDistance, (Duration)maxDuration [, (FullRouteList)startObjectPredictionHints=<route.FullRouteList object at 0x7752c8570640> [, (FullRouteList)destObjectPredictionHints=<route.FullRouteList object at 0x7752c8570c40> [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c8577370>]]]) -> ConnectingRoute :

        C++ signature :
            ad::map::route::ConnectingRoute calculateConnectingRoute(ad::map::match::Object,ad::map::match::Object,ad::physics::Distance,ad::physics::Duration [,std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >=<route.FullRouteList object at 0x7752c8570640> [,std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >=<route.FullRouteList object at 0x7752c8570c40> [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c8577370>]]])

    calculateConnectingRoute( (Object)startObject, (Object)destObject, (Distance)maxDistance [, (FullRouteList)startObjectPredictionHints=<route.FullRouteList object at 0x7752c85702c0> [, (FullRouteList)destObjectPredictionHints=<route.FullRouteList object at 0x7752c8571040> [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c8577910>]]]) -> ConnectingRoute :

        C++ signature :
            ad::map::route::ConnectingRoute calculateConnectingRoute(ad::map::match::Object,ad::map::match::Object,ad::physics::Distance [,std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >=<route.FullRouteList object at 0x7752c85702c0> [,std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >=<route.FullRouteList object at 0x7752c8571040> [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c8577910>]]])

    calculateConnectingRoute( (Object)startObject, (Object)destObject, (Duration)maxDuration [, (FullRouteList)startObjectPredictionHints=<route.FullRouteList object at 0x7752c8571a40> [, (FullRouteList)destObjectPredictionHints=<route.FullRouteList object at 0x7752c8570040> [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c8574ee0>]]]) -> ConnectingRoute :

        C++ signature :
            ad::map::route::ConnectingRoute calculateConnectingRoute(ad::map::match::Object,ad::map::match::Object,ad::physics::Duration [,std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >=<route.FullRouteList object at 0x7752c8571a40> [,std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >=<route.FullRouteList object at 0x7752c8570040> [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c8574ee0>]]])"""
def calculateRouteParaPointAtDistance(*args, **kwargs):
    """
    calculateRouteParaPointAtDistance( (FullRoute)route, (RouteParaPoint)origin, (Distance)distance, (RouteParaPoint)resultingPoint) -> bool :

        C++ signature :
            bool calculateRouteParaPointAtDistance(ad::map::route::FullRoute,ad::map::route::RouteParaPoint,ad::physics::Distance,ad::map::route::RouteParaPoint {lvalue})"""
def compareRoutesOnIntervalLevel(*args, **kwargs):
    """
    compareRoutesOnIntervalLevel( (FullRoute)left, (FullRoute)right) -> CompareRouteResult :

        C++ signature :
            ad::map::route::planning::CompareRouteResult compareRoutesOnIntervalLevel(ad::map::route::FullRoute,ad::map::route::FullRoute)"""
def createFullRoute(*args, **kwargs):
    """
    createFullRoute( (RawRoute)rawRoute, (RouteCreationMode)routeCreationMode, (LaneIdSet)relevantLanes) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute createFullRoute(ad::map::route::planning::Route::RawRoute,ad::map::route::RouteCreationMode,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
def createRoutingParaPoint(*args, **kwargs):
    """
    createRoutingParaPoint( (LaneId)laneId, (ParametricValue)parametricOffset [, (RoutingDirection)routingDirection=route.RoutingDirection.DONT_CARE]) -> RoutingParaPoint :

        C++ signature :
            ad::map::route::planning::RoutingParaPoint createRoutingParaPoint(ad::map::lane::LaneId,ad::physics::ParametricValue [,ad::map::route::planning::RoutingDirection=route.RoutingDirection.DONT_CARE])"""
@overload
def createRoutingPoint(ad) -> Any:
    """
    createRoutingPoint( (LaneId)laneId, (ParametricValue)parametricOffset [, (RoutingDirection)routingDirection=route.RoutingDirection.DONT_CARE]) -> RoutingParaPoint :

        C++ signature :
            ad::map::route::planning::RoutingParaPoint createRoutingPoint(ad::map::lane::LaneId,ad::physics::ParametricValue [,ad::map::route::planning::RoutingDirection=route.RoutingDirection.DONT_CARE])

    createRoutingPoint( (ParaPoint)paraPoint [, (RoutingDirection)routingDirection=route.RoutingDirection.DONT_CARE]) -> RoutingParaPoint :

        C++ signature :
            ad::map::route::planning::RoutingParaPoint createRoutingPoint(ad::map::point::ParaPoint [,ad::map::route::planning::RoutingDirection=route.RoutingDirection.DONT_CARE])

    createRoutingPoint( (LaneOccupiedRegion)occupiedRegion [, (RoutingDirection)routingDirection=route.RoutingDirection.DONT_CARE]) -> RoutingParaPoint :

        C++ signature :
            ad::map::route::planning::RoutingParaPoint createRoutingPoint(ad::map::match::LaneOccupiedRegion [,ad::map::route::planning::RoutingDirection=route.RoutingDirection.DONT_CARE])

    createRoutingPoint( (ParaPoint)paraPoint, (ENUHeading)heading) -> RoutingParaPoint :

        C++ signature :
            ad::map::route::planning::RoutingParaPoint createRoutingPoint(ad::map::point::ParaPoint,ad::map::point::ENUHeading)

    createRoutingPoint( (LaneOccupiedRegion)occupiedRegion, (ENUHeading)heading) -> RoutingParaPoint :

        C++ signature :
            ad::map::route::planning::RoutingParaPoint createRoutingPoint(ad::map::match::LaneOccupiedRegion,ad::map::point::ENUHeading)"""
@overload
def createRoutingPoint(ad) -> Any:
    """
    createRoutingPoint( (LaneId)laneId, (ParametricValue)parametricOffset [, (RoutingDirection)routingDirection=route.RoutingDirection.DONT_CARE]) -> RoutingParaPoint :

        C++ signature :
            ad::map::route::planning::RoutingParaPoint createRoutingPoint(ad::map::lane::LaneId,ad::physics::ParametricValue [,ad::map::route::planning::RoutingDirection=route.RoutingDirection.DONT_CARE])

    createRoutingPoint( (ParaPoint)paraPoint [, (RoutingDirection)routingDirection=route.RoutingDirection.DONT_CARE]) -> RoutingParaPoint :

        C++ signature :
            ad::map::route::planning::RoutingParaPoint createRoutingPoint(ad::map::point::ParaPoint [,ad::map::route::planning::RoutingDirection=route.RoutingDirection.DONT_CARE])

    createRoutingPoint( (LaneOccupiedRegion)occupiedRegion [, (RoutingDirection)routingDirection=route.RoutingDirection.DONT_CARE]) -> RoutingParaPoint :

        C++ signature :
            ad::map::route::planning::RoutingParaPoint createRoutingPoint(ad::map::match::LaneOccupiedRegion [,ad::map::route::planning::RoutingDirection=route.RoutingDirection.DONT_CARE])

    createRoutingPoint( (ParaPoint)paraPoint, (ENUHeading)heading) -> RoutingParaPoint :

        C++ signature :
            ad::map::route::planning::RoutingParaPoint createRoutingPoint(ad::map::point::ParaPoint,ad::map::point::ENUHeading)

    createRoutingPoint( (LaneOccupiedRegion)occupiedRegion, (ENUHeading)heading) -> RoutingParaPoint :

        C++ signature :
            ad::map::route::planning::RoutingParaPoint createRoutingPoint(ad::map::match::LaneOccupiedRegion,ad::map::point::ENUHeading)"""
def cutIntervalAtEnd(*args, **kwargs):
    """
    cutIntervalAtEnd( (LaneInterval)laneInterval, (ParametricValue)newIntervalEnd) -> LaneInterval :

        C++ signature :
            ad::map::route::LaneInterval cutIntervalAtEnd(ad::map::route::LaneInterval,ad::physics::ParametricValue)"""
def cutIntervalAtStart(*args, **kwargs):
    """
    cutIntervalAtStart( (LaneInterval)laneInterval, (ParametricValue)newIntervalStart) -> LaneInterval :

        C++ signature :
            ad::map::route::LaneInterval cutIntervalAtStart(ad::map::route::LaneInterval,ad::physics::ParametricValue)"""
def extendIntervalFromEnd(*args, **kwargs):
    """
    extendIntervalFromEnd( (LaneInterval)laneInterval, (Distance)distance) -> LaneInterval :

        C++ signature :
            ad::map::route::LaneInterval extendIntervalFromEnd(ad::map::route::LaneInterval,ad::physics::Distance)"""
def extendIntervalFromStart(*args, **kwargs):
    """
    extendIntervalFromStart( (LaneInterval)laneInterval, (Distance)distance) -> LaneInterval :

        C++ signature :
            ad::map::route::LaneInterval extendIntervalFromStart(ad::map::route::LaneInterval,ad::physics::Distance)"""
def extendIntervalUntilEnd(ad) -> Any:
    """
    extendIntervalUntilEnd( (LaneInterval)laneInterval) -> LaneInterval :

        C++ signature :
            ad::map::route::LaneInterval extendIntervalUntilEnd(ad::map::route::LaneInterval)"""
def extendIntervalUntilStart(ad) -> Any:
    """
    extendIntervalUntilStart( (LaneInterval)laneInterval) -> LaneInterval :

        C++ signature :
            ad::map::route::LaneInterval extendIntervalUntilStart(ad::map::route::LaneInterval)"""
def extendRouteToDestinations(*args, **kwargs):
    """
    extendRouteToDestinations( (FullRoute)route, (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)dest) -> bool :

        C++ signature :
            bool extendRouteToDestinations(ad::map::route::FullRoute {lvalue},std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> >)

    extendRouteToDestinations( (FullRoute)route, (GeoEdge)dest) -> bool :

        C++ signature :
            bool extendRouteToDestinations(ad::map::route::FullRoute {lvalue},std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    extendRouteToDestinations( (FullRoute)route, (ENUEdge)dest) -> bool :

        C++ signature :
            bool extendRouteToDestinations(ad::map::route::FullRoute {lvalue},std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)"""
def extendRouteToDistance(*args, **kwargs):
    """
    extendRouteToDistance( (FullRoute)route, (Distance)length, (FullRouteList)additionalRoutes [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c8574c10>]) -> bool :

        C++ signature :
            bool extendRouteToDistance(ad::map::route::FullRoute {lvalue},ad::physics::Distance,std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > {lvalue} [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c8574c10>])"""
def filterDuplicatedRoutes(*args, **kwargs):
    """
    filterDuplicatedRoutes( (FullRouteList)fullRoutes, (FilterDuplicatesMode)filterMode) -> FullRouteList :

        C++ signature :
            std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > filterDuplicatedRoutes(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >,ad::map::route::planning::FilterDuplicatesMode)"""
def findCenterWaypoint(*args, **kwargs):
    """
    findCenterWaypoint( (Object)object, (FullRoute)route) -> FindWaypointResult :

        C++ signature :
            ad::map::route::FindWaypointResult findCenterWaypoint(ad::map::match::Object,ad::map::route::FullRoute)"""
def findFirstLaneChange(*args, **kwargs):
    """
    findFirstLaneChange( (MapMatchedPosition)currentPositionEgoVehicle, (FullRoute)route) -> FindLaneChangeResult :

        C++ signature :
            ad::map::route::FindLaneChangeResult findFirstLaneChange(ad::map::match::MapMatchedPosition,ad::map::route::FullRoute)"""
def findNearestWaypoint(*args, **kwargs):
    """
    findNearestWaypoint( (ParaPointList)positions, (FullRoute)route) -> FindWaypointResult :

        C++ signature :
            ad::map::route::FindWaypointResult findNearestWaypoint(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >,ad::map::route::FullRoute)

    findNearestWaypoint( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)mapMatchedPositions, (FullRoute)route) -> FindWaypointResult :

        C++ signature :
            ad::map::route::FindWaypointResult findNearestWaypoint(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >,ad::map::route::FullRoute)"""
def findWaypoint(*args, **kwargs):
    """
    findWaypoint( (ParaPoint)position, (FullRoute)route) -> FindWaypointResult :

        C++ signature :
            ad::map::route::FindWaypointResult findWaypoint(ad::map::point::ParaPoint,ad::map::route::FullRoute)

    findWaypoint( (LaneId)laneId, (FullRoute)route) -> FindWaypointResult :

        C++ signature :
            ad::map::route::FindWaypointResult findWaypoint(ad::map::lane::LaneId,ad::map::route::FullRoute)"""
def fromString(*args, **kwargs):
    """
    fromString( (str)str) -> ConnectingRouteType :

        C++ signature :
            ad::map::route::ConnectingRouteType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> RouteCreationMode :

        C++ signature :
            ad::map::route::RouteCreationMode fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> LaneChangeDirection :

        C++ signature :
            ad::map::route::LaneChangeDirection fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
def getECEFBorder(ad) -> Any:
    """
    getECEFBorder( (LaneInterval)laneInterval) -> ECEFBorder :

        C++ signature :
            ad::map::lane::ECEFBorder getECEFBorder(ad::map::route::LaneInterval)"""
def getECEFBorderOfRoadSegment(ad) -> Any:
    """
    getECEFBorderOfRoadSegment( (RoadSegment)roadSegment [, (ParametricValue)parametricOffset]) -> ECEFBorder :

        C++ signature :
            ad::map::lane::ECEFBorder getECEFBorderOfRoadSegment(ad::map::route::RoadSegment [,ad::physics::ParametricValue])"""
def getECEFBorderOfRoute(ad) -> Any:
    """
    getECEFBorderOfRoute( (FullRoute)route) -> ECEFBorderList :

        C++ signature :
            std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > getECEFBorderOfRoute(ad::map::route::FullRoute)"""
def getENUBorder(ad) -> Any:
    """
    getENUBorder( (LaneInterval)laneInterval) -> ENUBorder :

        C++ signature :
            ad::map::lane::ENUBorder getENUBorder(ad::map::route::LaneInterval)"""
def getENUBorderOfRoadSegment(ad) -> Any:
    """
    getENUBorderOfRoadSegment( (RoadSegment)roadSegment [, (ParametricValue)parametricOffset]) -> ENUBorder :

        C++ signature :
            ad::map::lane::ENUBorder getENUBorderOfRoadSegment(ad::map::route::RoadSegment [,ad::physics::ParametricValue])"""
def getENUBorderOfRoute(ad) -> Any:
    """
    getENUBorderOfRoute( (FullRoute)route) -> ENUBorderList :

        C++ signature :
            std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > getENUBorderOfRoute(ad::map::route::FullRoute)"""
def getENUHeadingOfRoute(*args, **kwargs):
    """
    getENUHeadingOfRoute( (Object)object, (FullRoute)route) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading getENUHeadingOfRoute(ad::map::match::Object,ad::map::route::FullRoute)"""
def getENUProjectedBorder(ad) -> Any:
    """
    getENUProjectedBorder( (LaneInterval)laneInterval) -> ENUBorder :

        C++ signature :
            ad::map::lane::ENUBorder getENUProjectedBorder(ad::map::route::LaneInterval)"""
def getGeoBorder(ad) -> Any:
    """
    getGeoBorder( (LaneInterval)laneInterval) -> GeoBorder :

        C++ signature :
            ad::map::lane::GeoBorder getGeoBorder(ad::map::route::LaneInterval)"""
def getGeoBorderOfRoadSegment(ad) -> Any:
    """
    getGeoBorderOfRoadSegment( (RoadSegment)roadSegment [, (ParametricValue)parametricOffset]) -> GeoBorder :

        C++ signature :
            ad::map::lane::GeoBorder getGeoBorderOfRoadSegment(ad::map::route::RoadSegment [,ad::physics::ParametricValue])"""
def getGeoBorderOfRoute(ad) -> Any:
    """
    getGeoBorderOfRoute( (FullRoute)route) -> GeoBorderList :

        C++ signature :
            std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > getGeoBorderOfRoute(ad::map::route::FullRoute)"""
def getIntervalEnd(ad) -> Any:
    """
    getIntervalEnd( (LaneInterval)laneInterval) -> ParaPoint :

        C++ signature :
            ad::map::point::ParaPoint getIntervalEnd(ad::map::route::LaneInterval)"""
def getIntervalStart(ad) -> Any:
    """
    getIntervalStart( (LaneInterval)laneInterval) -> ParaPoint :

        C++ signature :
            ad::map::point::ParaPoint getIntervalStart(ad::map::route::LaneInterval)

    getIntervalStart( (FullRoute)route, (LaneId)laneId) -> ParaPoint :

        C++ signature :
            ad::map::point::ParaPoint getIntervalStart(ad::map::route::FullRoute,ad::map::lane::LaneId)"""
def getLaneParaPoint(*args, **kwargs):
    """
    getLaneParaPoint( (ParametricValue)routeParametricOffset, (LaneInterval)laneInterval) -> ParaPoint :

        C++ signature :
            ad::map::point::ParaPoint getLaneParaPoint(ad::physics::ParametricValue,ad::map::route::LaneInterval)"""
def getLaneParaPoints(*args, **kwargs):
    """
    getLaneParaPoints( (RouteParaPoint)routePosition, (FullRoute)route) -> ParaPointList :

        C++ signature :
            std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > getLaneParaPoints(ad::map::route::RouteParaPoint,ad::map::route::FullRoute)"""
def getLeftECEFEdge(ad) -> Any:
    """
    getLeftECEFEdge( (LaneInterval)laneInterval) -> ECEFEdge :

        C++ signature :
            std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > getLeftECEFEdge(ad::map::route::LaneInterval)"""
def getLeftENUEdge(ad) -> Any:
    """
    getLeftENUEdge( (LaneInterval)laneInterval) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > getLeftENUEdge(ad::map::route::LaneInterval)"""
def getLeftEdge(*args, **kwargs):
    """
    getLeftEdge( (LaneInterval)laneInterval, (ENUEdge)enuEdge) -> None :

        C++ signature :
            void getLeftEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue})

    getLeftEdge( (LaneInterval)laneInterval, (ECEFEdge)ecefEdge) -> None :

        C++ signature :
            void getLeftEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue})

    getLeftEdge( (LaneInterval)laneInterval, (GeoEdge)geoEdge) -> None :

        C++ signature :
            void getLeftEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue})"""
def getLeftGeoEdge(ad) -> Any:
    """
    getLeftGeoEdge( (LaneInterval)laneInterval) -> GeoEdge :

        C++ signature :
            std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > getLeftGeoEdge(ad::map::route::LaneInterval)"""
def getLeftProjectedECEFEdge(ad) -> Any:
    """
    getLeftProjectedECEFEdge( (LaneInterval)laneInterval) -> ECEFEdge :

        C++ signature :
            std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > getLeftProjectedECEFEdge(ad::map::route::LaneInterval)"""
def getLeftProjectedENUEdge(ad) -> Any:
    """
    getLeftProjectedENUEdge( (LaneInterval)laneInterval) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > getLeftProjectedENUEdge(ad::map::route::LaneInterval)"""
def getLeftProjectedEdge(*args, **kwargs):
    """
    getLeftProjectedEdge( (LaneInterval)laneInterval, (ENUEdge)enuEdge) -> None :

        C++ signature :
            void getLeftProjectedEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue})

    getLeftProjectedEdge( (LaneInterval)laneInterval, (ECEFEdge)ecefEdge) -> None :

        C++ signature :
            void getLeftProjectedEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue})

    getLeftProjectedEdge( (LaneInterval)laneInterval, (GeoEdge)geoEdge) -> None :

        C++ signature :
            void getLeftProjectedEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue})"""
def getLeftProjectedGeoEdge(ad) -> Any:
    """
    getLeftProjectedGeoEdge( (LaneInterval)laneInterval) -> GeoEdge :

        C++ signature :
            std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > getLeftProjectedGeoEdge(ad::map::route::LaneInterval)"""
def getMetricRanges(*args, **kwargs):
    """
    getMetricRanges( (LaneInterval)laneInterval, (MetricRange)lengthRange, (MetricRange)widthRange) -> None :

        C++ signature :
            void getMetricRanges(ad::map::route::LaneInterval,ad::physics::MetricRange {lvalue},ad::physics::MetricRange {lvalue})"""
def getProjectedParametricOffsetOnNeighborLane(*args, **kwargs):
    """
    getProjectedParametricOffsetOnNeighborLane( (LaneInterval)currentInterval, (LaneInterval)neighborInterval, (ParametricValue)parametricOffset) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue getProjectedParametricOffsetOnNeighborLane(ad::map::route::LaneInterval,ad::map::route::LaneInterval,ad::physics::ParametricValue)"""
def getRightECEFEdge(ad) -> Any:
    """
    getRightECEFEdge( (LaneInterval)laneInterval) -> ECEFEdge :

        C++ signature :
            std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > getRightECEFEdge(ad::map::route::LaneInterval)"""
def getRightENUEdge(ad) -> Any:
    """
    getRightENUEdge( (LaneInterval)laneInterval) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > getRightENUEdge(ad::map::route::LaneInterval)"""
def getRightEdge(*args, **kwargs):
    """
    getRightEdge( (LaneInterval)laneInterval, (ENUEdge)enuEdge) -> None :

        C++ signature :
            void getRightEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue})

    getRightEdge( (LaneInterval)laneInterval, (ECEFEdge)ecefEdge) -> None :

        C++ signature :
            void getRightEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue})

    getRightEdge( (LaneInterval)laneInterval, (GeoEdge)geoEdge) -> None :

        C++ signature :
            void getRightEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue})"""
def getRightGeoEdge(ad) -> Any:
    """
    getRightGeoEdge( (LaneInterval)laneInterval) -> GeoEdge :

        C++ signature :
            std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > getRightGeoEdge(ad::map::route::LaneInterval)"""
def getRightProjectedECEFEdge(ad) -> Any:
    """
    getRightProjectedECEFEdge( (LaneInterval)laneInterval) -> ECEFEdge :

        C++ signature :
            std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > getRightProjectedECEFEdge(ad::map::route::LaneInterval)"""
def getRightProjectedENUEdge(ad) -> Any:
    """
    getRightProjectedENUEdge( (LaneInterval)laneInterval) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > getRightProjectedENUEdge(ad::map::route::LaneInterval)"""
def getRightProjectedEdge(*args, **kwargs):
    """
    getRightProjectedEdge( (LaneInterval)laneInterval, (ENUEdge)enuEdge) -> None :

        C++ signature :
            void getRightProjectedEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue})

    getRightProjectedEdge( (LaneInterval)laneInterval, (ECEFEdge)ecefEdge) -> None :

        C++ signature :
            void getRightProjectedEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue})

    getRightProjectedEdge( (LaneInterval)laneInterval, (GeoEdge)geoEdge) -> None :

        C++ signature :
            void getRightProjectedEdge(ad::map::route::LaneInterval,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue})"""
def getRightProjectedGeoEdge(ad) -> Any:
    """
    getRightProjectedGeoEdge( (LaneInterval)laneInterval) -> GeoEdge :

        C++ signature :
            std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > getRightProjectedGeoEdge(ad::map::route::LaneInterval)"""
def getRouteExpandedToAllNeighborLanes(ad) -> Any:
    """
    getRouteExpandedToAllNeighborLanes( (FullRoute)route) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute getRouteExpandedToAllNeighborLanes(ad::map::route::FullRoute)"""
def getRouteExpandedToOppositeLanes(ad) -> Any:
    """
    getRouteExpandedToOppositeLanes( (FullRoute)route) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute getRouteExpandedToOppositeLanes(ad::map::route::FullRoute)"""
def getRouteIterator(*args, **kwargs):
    """
    getRouteIterator( (RouteParaPoint)routePosition, (FullRoute)route) -> RouteIterator :

        C++ signature :
            ad::map::route::RouteIterator getRouteIterator(ad::map::route::RouteParaPoint,ad::map::route::FullRoute)"""
def getRouteParaPointFromParaPoint(*args, **kwargs):
    """
    getRouteParaPointFromParaPoint( (ParaPoint)paraPoint, (FullRoute)route, (RouteParaPoint)routeParaPoint) -> bool :

        C++ signature :
            bool getRouteParaPointFromParaPoint(ad::map::point::ParaPoint,ad::map::route::FullRoute,ad::map::route::RouteParaPoint {lvalue})"""
def getRouteSection(*args, **kwargs):
    """
    getRouteSection( (FindWaypointResult)currentLane, (Distance)distanceFront, (Distance)distanceEnd, (FullRoute)route [, (RouteSectionCreationMode)routeSectionCreationMode=route.RouteSectionCreationMode.SingleLane]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute getRouteSection(ad::map::route::FindWaypointResult,ad::physics::Distance,ad::physics::Distance,ad::map::route::FullRoute [,ad::map::route::RouteSectionCreationMode=route.RouteSectionCreationMode.SingleLane])

    getRouteSection( (ParaPoint)centerPoint, (Distance)distanceFront, (Distance)distanceEnd, (FullRoute)route [, (RouteSectionCreationMode)routeSectionCreationMode=route.RouteSectionCreationMode.SingleLane]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute getRouteSection(ad::map::point::ParaPoint,ad::physics::Distance,ad::physics::Distance,ad::map::route::FullRoute [,ad::map::route::RouteSectionCreationMode=route.RouteSectionCreationMode.SingleLane])

    getRouteSection( (Object)object, (FullRoute)route [, (RouteSectionCreationMode)routeSectionCreationMode=route.RouteSectionCreationMode.SingleLane]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute getRouteSection(ad::map::match::Object,ad::map::route::FullRoute [,ad::map::route::RouteSectionCreationMode=route.RouteSectionCreationMode.SingleLane])"""
def getSignedDistance(*args, **kwargs):
    """
    getSignedDistance( (LaneInterval)laneInterval, (ParaPoint)first, (ParaPoint)second) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue getSignedDistance(ad::map::route::LaneInterval,ad::map::point::ParaPoint,ad::map::point::ParaPoint)"""
@overload
def getSpeedLimits(ad) -> Any:
    """
    getSpeedLimits( (RoadSegment)roadSegment) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::RoadSegment)

    getSpeedLimits( (LaneSegment)laneSegment) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::LaneSegment)

    getSpeedLimits( (RouteIterator)startIterator, (RouteIterator)endIterator) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::RouteIterator,ad::map::route::RouteIterator)

    getSpeedLimits( (FullRoute)fullRoute) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::FullRoute)

    getSpeedLimits( (ConnectingRoute)connectingRoute) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::ConnectingRoute)

    getSpeedLimits( (LaneInterval)laneInterval) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::LaneInterval)"""
@overload
def getSpeedLimits(ad) -> Any:
    """
    getSpeedLimits( (RoadSegment)roadSegment) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::RoadSegment)

    getSpeedLimits( (LaneSegment)laneSegment) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::LaneSegment)

    getSpeedLimits( (RouteIterator)startIterator, (RouteIterator)endIterator) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::RouteIterator,ad::map::route::RouteIterator)

    getSpeedLimits( (FullRoute)fullRoute) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::FullRoute)

    getSpeedLimits( (ConnectingRoute)connectingRoute) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::ConnectingRoute)

    getSpeedLimits( (LaneInterval)laneInterval) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::LaneInterval)"""
@overload
def getSpeedLimits(ad) -> Any:
    """
    getSpeedLimits( (RoadSegment)roadSegment) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::RoadSegment)

    getSpeedLimits( (LaneSegment)laneSegment) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::LaneSegment)

    getSpeedLimits( (RouteIterator)startIterator, (RouteIterator)endIterator) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::RouteIterator,ad::map::route::RouteIterator)

    getSpeedLimits( (FullRoute)fullRoute) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::FullRoute)

    getSpeedLimits( (ConnectingRoute)connectingRoute) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::ConnectingRoute)

    getSpeedLimits( (LaneInterval)laneInterval) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::LaneInterval)"""
@overload
def getSpeedLimits(ad) -> Any:
    """
    getSpeedLimits( (RoadSegment)roadSegment) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::RoadSegment)

    getSpeedLimits( (LaneSegment)laneSegment) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::LaneSegment)

    getSpeedLimits( (RouteIterator)startIterator, (RouteIterator)endIterator) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::RouteIterator,ad::map::route::RouteIterator)

    getSpeedLimits( (FullRoute)fullRoute) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::FullRoute)

    getSpeedLimits( (ConnectingRoute)connectingRoute) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::ConnectingRoute)

    getSpeedLimits( (LaneInterval)laneInterval) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::LaneInterval)"""
@overload
def getSpeedLimits(ad) -> Any:
    """
    getSpeedLimits( (RoadSegment)roadSegment) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::RoadSegment)

    getSpeedLimits( (LaneSegment)laneSegment) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::LaneSegment)

    getSpeedLimits( (RouteIterator)startIterator, (RouteIterator)endIterator) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::RouteIterator,ad::map::route::RouteIterator)

    getSpeedLimits( (FullRoute)fullRoute) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::FullRoute)

    getSpeedLimits( (ConnectingRoute)connectingRoute) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::ConnectingRoute)

    getSpeedLimits( (LaneInterval)laneInterval) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::route::LaneInterval)"""
def getUnsignedDistance(*args, **kwargs):
    """
    getUnsignedDistance( (LaneInterval)laneInterval, (ParaPoint)first, (ParaPoint)second) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue getUnsignedDistance(ad::map::route::LaneInterval,ad::map::point::ParaPoint,ad::map::point::ParaPoint)"""
def intersectionOnRoute(*args, **kwargs):
    """
    intersectionOnRoute( (Intersection)intersection, (FullRoute)route) -> FindWaypointResult :

        C++ signature :
            ad::map::route::FindWaypointResult intersectionOnRoute(ad::map::intersection::Intersection,ad::map::route::FullRoute)"""
def isAfterInterval(*args, **kwargs):
    """
    isAfterInterval( (LaneInterval)laneInterval, (ParametricValue)parametricOffset) -> bool :

        C++ signature :
            bool isAfterInterval(ad::map::route::LaneInterval,ad::physics::ParametricValue)

    isAfterInterval( (LaneInterval)laneInterval, (ParaPoint)point) -> bool :

        C++ signature :
            bool isAfterInterval(ad::map::route::LaneInterval,ad::map::point::ParaPoint)"""
def isBeforeInterval(*args, **kwargs):
    """
    isBeforeInterval( (LaneInterval)laneInterval, (ParametricValue)parametricOffset) -> bool :

        C++ signature :
            bool isBeforeInterval(ad::map::route::LaneInterval,ad::physics::ParametricValue)

    isBeforeInterval( (LaneInterval)laneInterval, (ParaPoint)point) -> bool :

        C++ signature :
            bool isBeforeInterval(ad::map::route::LaneInterval,ad::map::point::ParaPoint)"""
def isConnectedRoutePartOfAnIntersection(ad) -> Any:
    """
    isConnectedRoutePartOfAnIntersection( (ConnectingRoute)connectingRoute) -> bool :

        C++ signature :
            bool isConnectedRoutePartOfAnIntersection(ad::map::route::ConnectingRoute)"""
def isDegenerated(ad) -> Any:
    """
    isDegenerated( (LaneInterval)laneInterval) -> bool :

        C++ signature :
            bool isDegenerated(ad::map::route::LaneInterval)"""
def isEndOfInterval(*args, **kwargs):
    """
    isEndOfInterval( (LaneInterval)laneInterval, (ParaPoint)point) -> bool :

        C++ signature :
            bool isEndOfInterval(ad::map::route::LaneInterval,ad::map::point::ParaPoint)"""
def isObjectHeadingInRouteDirection(*args, **kwargs):
    """
    isObjectHeadingInRouteDirection( (Object)object, (FullRoute)route) -> bool :

        C++ signature :
            bool isObjectHeadingInRouteDirection(ad::map::match::Object,ad::map::route::FullRoute)"""
def isRouteDirectionAlignedWithDrivingDirection(ad) -> Any:
    """
    isRouteDirectionAlignedWithDrivingDirection( (LaneInterval)laneInterval) -> bool :

        C++ signature :
            bool isRouteDirectionAlignedWithDrivingDirection(ad::map::route::LaneInterval)"""
def isRouteDirectionNegative(ad) -> Any:
    """
    isRouteDirectionNegative( (LaneInterval)laneInterval) -> bool :

        C++ signature :
            bool isRouteDirectionNegative(ad::map::route::LaneInterval)"""
def isRouteDirectionPositive(ad) -> Any:
    """
    isRouteDirectionPositive( (LaneInterval)laneInterval) -> bool :

        C++ signature :
            bool isRouteDirectionPositive(ad::map::route::LaneInterval)"""
def isStartOfInterval(*args, **kwargs):
    """
    isStartOfInterval( (LaneInterval)laneInterval, (ParaPoint)point) -> bool :

        C++ signature :
            bool isStartOfInterval(ad::map::route::LaneInterval,ad::map::point::ParaPoint)"""
def isWithinInterval(*args, **kwargs):
    """
    isWithinInterval( (RoadSegment)roadSegment, (ParaPoint)point) -> bool :

        C++ signature :
            bool isWithinInterval(ad::map::route::RoadSegment,ad::map::point::ParaPoint)

    isWithinInterval( (LaneInterval)laneInterval, (ParametricValue)parametricOffset) -> bool :

        C++ signature :
            bool isWithinInterval(ad::map::route::LaneInterval,ad::physics::ParametricValue)

    isWithinInterval( (LaneInterval)laneInterval, (ParaPoint)point) -> bool :

        C++ signature :
            bool isWithinInterval(ad::map::route::LaneInterval,ad::map::point::ParaPoint)"""
def objectOnRoute(*args, **kwargs):
    """
    objectOnRoute( (MapMatchedObjectBoundingBox)object, (FullRoute)route) -> FindWaypointResult :

        C++ signature :
            ad::map::route::FindWaypointResult objectOnRoute(ad::map::match::MapMatchedObjectBoundingBox,ad::map::route::FullRoute)"""
def overlapsInterval(*args, **kwargs):
    """
    overlapsInterval( (LaneInterval)laneInterval, (ParametricRange)range) -> bool :

        C++ signature :
            bool overlapsInterval(ad::map::route::LaneInterval,ad::physics::ParametricRange)"""
def planRoute(*args, **kwargs):
    """
    planRoute( (RoutingParaPoint)start, (RoutingParaPoint)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::route::planning::RoutingParaPoint,ad::map::route::planning::RoutingParaPoint [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (ParaPoint)start, (ParaPoint)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::point::ParaPoint,ad::map::point::ParaPoint [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (ParaPoint)start, (ENUHeading)startHeading, (ParaPoint)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::point::ParaPoint,ad::map::point::ENUHeading,ad::map::point::ParaPoint [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (ParaPoint)start, (ENUHeading)startHeading, (ParaPoint)dest, (ENUHeading)destHeading [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::point::ParaPoint,ad::map::point::ENUHeading,ad::map::point::ParaPoint,ad::map::point::ENUHeading [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (RoutingParaPoint)start, (GeoPoint)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::route::planning::RoutingParaPoint,ad::map::point::GeoPoint [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (RoutingParaPoint)start, (ENUPoint)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::route::planning::RoutingParaPoint,ad::map::point::ENUPoint [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (ParaPoint)start, (GeoPoint)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::point::ParaPoint,ad::map::point::GeoPoint [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (ParaPoint)start, (ENUHeading)startHeading, (GeoPoint)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::point::ParaPoint,ad::map::point::ENUHeading,ad::map::point::GeoPoint [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (ParaPoint)start, (PointOfInterest)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::point::ParaPoint,ad::map::config::PointOfInterest [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (RoutingParaPoint)start, (GeoEdge)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::route::planning::RoutingParaPoint,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (RoutingParaPoint)start, (ENUEdge)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::route::planning::RoutingParaPoint,std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (RoutingParaPoint)start, (vector_less_ad_scope_map_scope_route_scope_planning_scope_RoutingParaPoint_greater_)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::route::planning::RoutingParaPoint,std::vector<ad::map::route::planning::RoutingParaPoint, std::allocator<ad::map::route::planning::RoutingParaPoint> > [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])

    planRoute( (ParaPoint)start, (ENUHeading)startHeading, (GeoEdge)dest [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection]) -> FullRoute :

        C++ signature :
            ad::map::route::FullRoute planRoute(ad::map::point::ParaPoint,ad::map::point::ENUHeading,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection])"""
def predictRoutes(*args, **kwargs):
    """
    predictRoutes( (RoutingParaPoint)start, (Distance)predictionDistance, (Duration)predictionDuration [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection [, (FilterDuplicatesMode)filterMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c8577880>]]]) -> FullRouteList :

        C++ signature :
            std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > predictRoutes(ad::map::route::planning::RoutingParaPoint,ad::physics::Distance,ad::physics::Duration [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection [,ad::map::route::planning::FilterDuplicatesMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c8577880>]]])

    predictRoutes( (MapMatchedObjectBoundingBox)start, (Distance)predictionDistance, (Duration)predictionDuration [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection [, (FilterDuplicatesMode)filterMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c8574700>]]]) -> FullRouteList :

        C++ signature :
            std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > predictRoutes(ad::map::match::MapMatchedObjectBoundingBox,ad::physics::Distance,ad::physics::Duration [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection [,ad::map::route::planning::FilterDuplicatesMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c8574700>]]])"""
def predictRoutesDirectionless(*args, **kwargs):
    """
    predictRoutesDirectionless( (ParaPoint)start, (Distance)predictionDistance, (Duration)predictionDuration [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.AllRoutableLanes [, (FilterDuplicatesMode)filterMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c8574430>]]]) -> FullRouteList :

        C++ signature :
            std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > predictRoutesDirectionless(ad::map::point::ParaPoint,ad::physics::Distance,ad::physics::Duration [,ad::map::route::RouteCreationMode=route.RouteCreationMode.AllRoutableLanes [,ad::map::route::planning::FilterDuplicatesMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c8574430>]]])"""
def predictRoutesOnDistance(*args, **kwargs):
    """
    predictRoutesOnDistance( (RoutingParaPoint)start, (Distance)predictionDistance [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection [, (FilterDuplicatesMode)filterMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c8575f30>]]]) -> FullRouteList :

        C++ signature :
            std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > predictRoutesOnDistance(ad::map::route::planning::RoutingParaPoint,ad::physics::Distance [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection [,ad::map::route::planning::FilterDuplicatesMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c8575f30>]]])

    predictRoutesOnDistance( (MapMatchedObjectBoundingBox)start, (Distance)predictionDistance [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection [, (FilterDuplicatesMode)filterMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c85779a0>]]]) -> FullRouteList :

        C++ signature :
            std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > predictRoutesOnDistance(ad::map::match::MapMatchedObjectBoundingBox,ad::physics::Distance [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection [,ad::map::route::planning::FilterDuplicatesMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c85779a0>]]])"""
def predictRoutesOnDuration(*args, **kwargs):
    """
    predictRoutesOnDuration( (RoutingParaPoint)start, (Duration)predictionDuration [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection [, (FilterDuplicatesMode)filterMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c85753f0>]]]) -> FullRouteList :

        C++ signature :
            std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > predictRoutesOnDuration(ad::map::route::planning::RoutingParaPoint,ad::physics::Duration [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection [,ad::map::route::planning::FilterDuplicatesMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c85753f0>]]])

    predictRoutesOnDuration( (MapMatchedObjectBoundingBox)start, (Duration)predictionDuration [, (RouteCreationMode)routeCreationMode=route.RouteCreationMode.SameDrivingDirection [, (FilterDuplicatesMode)filterMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c85756c0>]]]) -> FullRouteList :

        C++ signature :
            std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> > predictRoutesOnDuration(ad::map::match::MapMatchedObjectBoundingBox,ad::physics::Duration [,ad::map::route::RouteCreationMode=route.RouteCreationMode.SameDrivingDirection [,ad::map::route::planning::FilterDuplicatesMode=route.FilterDuplicatesMode.SubRoutesPreferLongerOnes [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c85756c0>]]])"""
def restrictIntervalFromBegin(*args, **kwargs):
    """
    restrictIntervalFromBegin( (LaneInterval)laneInterval, (Distance)distance) -> LaneInterval :

        C++ signature :
            ad::map::route::LaneInterval restrictIntervalFromBegin(ad::map::route::LaneInterval,ad::physics::Distance)"""
def shortenIntervalFromBegin(*args, **kwargs):
    """
    shortenIntervalFromBegin( (LaneInterval)laneInterval, (Distance)distance) -> LaneInterval :

        C++ signature :
            ad::map::route::LaneInterval shortenIntervalFromBegin(ad::map::route::LaneInterval,ad::physics::Distance)"""
def shortenIntervalFromEnd(*args, **kwargs):
    """
    shortenIntervalFromEnd( (LaneInterval)laneInterval, (Distance)distance) -> LaneInterval :

        C++ signature :
            ad::map::route::LaneInterval shortenIntervalFromEnd(ad::map::route::LaneInterval,ad::physics::Distance)"""
def shortenRoute(*args, **kwargs):
    """
    shortenRoute( (ParaPoint)currentPosition, (FullRoute)route [, (ShortenRouteMode)shortenRouteMode=route.ShortenRouteMode.Normal]) -> ShortenRouteResult :

        C++ signature :
            ad::map::route::ShortenRouteResult shortenRoute(ad::map::point::ParaPoint,ad::map::route::FullRoute {lvalue} [,ad::map::route::ShortenRouteMode=route.ShortenRouteMode.Normal])

    shortenRoute( (ParaPointList)currentPositions, (FullRoute)route [, (ShortenRouteMode)shortenRouteMode=route.ShortenRouteMode.Normal]) -> ShortenRouteResult :

        C++ signature :
            ad::map::route::ShortenRouteResult shortenRoute(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >,ad::map::route::FullRoute {lvalue} [,ad::map::route::ShortenRouteMode=route.ShortenRouteMode.Normal])

    shortenRoute( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)mapMatchedPositions, (FullRoute)route [, (ShortenRouteMode)shortenRouteMode=route.ShortenRouteMode.Normal]) -> ShortenRouteResult :

        C++ signature :
            ad::map::route::ShortenRouteResult shortenRoute(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >,ad::map::route::FullRoute {lvalue} [,ad::map::route::ShortenRouteMode=route.ShortenRouteMode.Normal])"""
def shortenRouteToDistance(*args, **kwargs):
    """
    shortenRouteToDistance( (FullRoute)route, (Distance)length) -> None :

        C++ signature :
            void shortenRouteToDistance(ad::map::route::FullRoute {lvalue},ad::physics::Distance)"""
def shortenSegmentFromBegin(*args, **kwargs):
    """
    shortenSegmentFromBegin( (RoadSegment)roadSegment, (Distance)distance) -> None :

        C++ signature :
            void shortenSegmentFromBegin(ad::map::route::RoadSegment {lvalue},ad::physics::Distance)"""
def shortenSegmentFromEnd(*args, **kwargs):
    """
    shortenSegmentFromEnd( (RoadSegment)roadSegment, (Distance)distance) -> None :

        C++ signature :
            void shortenSegmentFromEnd(ad::map::route::RoadSegment {lvalue},ad::physics::Distance)"""
def signedDistanceToLane(*args, **kwargs):
    """
    signedDistanceToLane( (LaneId)checkLaneId, (FullRoute)route, (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)mapMatchedPositions) -> Distance :

        C++ signature :
            ad::physics::Distance signedDistanceToLane(ad::map::lane::LaneId,ad::map::route::FullRoute,std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)"""
def toParametricRange(ad) -> Any:
    """
    toParametricRange( (LaneInterval)laneInterval) -> ParametricRange :

        C++ signature :
            ad::physics::ParametricRange toParametricRange(ad::map::route::LaneInterval)"""
@overload
def toString(ad) -> Any:
    """
    toString( (ConnectingRouteType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::route::ConnectingRouteType)

    toString( (RouteCreationMode)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::route::RouteCreationMode)

    toString( (LaneChangeDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::route::LaneChangeDirection)"""
@overload
def toString(ad) -> Any:
    """
    toString( (ConnectingRouteType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::route::ConnectingRouteType)

    toString( (RouteCreationMode)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::route::RouteCreationMode)

    toString( (LaneChangeDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::route::LaneChangeDirection)"""
@overload
def toString(ad) -> Any:
    """
    toString( (ConnectingRouteType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::route::ConnectingRouteType)

    toString( (RouteCreationMode)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::route::RouteCreationMode)

    toString( (LaneChangeDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::route::LaneChangeDirection)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ConnectingRouteType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRouteType)

    to_string( (LaneInterval)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneInterval)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneSegment)

    to_string( (LaneSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> >)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RoadSegment)

    to_string( (RoadSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> >)

    to_string( (RouteCreationMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteCreationMode)

    to_string( (FullRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::FullRoute)

    to_string( (ConnectingRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRoute)

    to_string( (FullRouteList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >)

    to_string( (LaneChangeDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneChangeDirection)

    to_string( (RouteParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteParaPoint)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ConnectingRouteType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRouteType)

    to_string( (LaneInterval)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneInterval)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneSegment)

    to_string( (LaneSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> >)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RoadSegment)

    to_string( (RoadSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> >)

    to_string( (RouteCreationMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteCreationMode)

    to_string( (FullRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::FullRoute)

    to_string( (ConnectingRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRoute)

    to_string( (FullRouteList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >)

    to_string( (LaneChangeDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneChangeDirection)

    to_string( (RouteParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteParaPoint)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ConnectingRouteType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRouteType)

    to_string( (LaneInterval)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneInterval)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneSegment)

    to_string( (LaneSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> >)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RoadSegment)

    to_string( (RoadSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> >)

    to_string( (RouteCreationMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteCreationMode)

    to_string( (FullRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::FullRoute)

    to_string( (ConnectingRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRoute)

    to_string( (FullRouteList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >)

    to_string( (LaneChangeDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneChangeDirection)

    to_string( (RouteParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteParaPoint)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ConnectingRouteType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRouteType)

    to_string( (LaneInterval)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneInterval)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneSegment)

    to_string( (LaneSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> >)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RoadSegment)

    to_string( (RoadSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> >)

    to_string( (RouteCreationMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteCreationMode)

    to_string( (FullRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::FullRoute)

    to_string( (ConnectingRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRoute)

    to_string( (FullRouteList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >)

    to_string( (LaneChangeDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneChangeDirection)

    to_string( (RouteParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteParaPoint)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ConnectingRouteType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRouteType)

    to_string( (LaneInterval)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneInterval)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneSegment)

    to_string( (LaneSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> >)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RoadSegment)

    to_string( (RoadSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> >)

    to_string( (RouteCreationMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteCreationMode)

    to_string( (FullRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::FullRoute)

    to_string( (ConnectingRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRoute)

    to_string( (FullRouteList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >)

    to_string( (LaneChangeDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneChangeDirection)

    to_string( (RouteParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteParaPoint)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ConnectingRouteType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRouteType)

    to_string( (LaneInterval)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneInterval)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneSegment)

    to_string( (LaneSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> >)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RoadSegment)

    to_string( (RoadSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> >)

    to_string( (RouteCreationMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteCreationMode)

    to_string( (FullRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::FullRoute)

    to_string( (ConnectingRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRoute)

    to_string( (FullRouteList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >)

    to_string( (LaneChangeDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneChangeDirection)

    to_string( (RouteParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteParaPoint)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ConnectingRouteType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRouteType)

    to_string( (LaneInterval)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneInterval)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneSegment)

    to_string( (LaneSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> >)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RoadSegment)

    to_string( (RoadSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> >)

    to_string( (RouteCreationMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteCreationMode)

    to_string( (FullRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::FullRoute)

    to_string( (ConnectingRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRoute)

    to_string( (FullRouteList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >)

    to_string( (LaneChangeDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneChangeDirection)

    to_string( (RouteParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteParaPoint)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ConnectingRouteType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRouteType)

    to_string( (LaneInterval)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneInterval)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneSegment)

    to_string( (LaneSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> >)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RoadSegment)

    to_string( (RoadSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> >)

    to_string( (RouteCreationMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteCreationMode)

    to_string( (FullRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::FullRoute)

    to_string( (ConnectingRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRoute)

    to_string( (FullRouteList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >)

    to_string( (LaneChangeDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneChangeDirection)

    to_string( (RouteParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteParaPoint)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ConnectingRouteType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRouteType)

    to_string( (LaneInterval)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneInterval)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneSegment)

    to_string( (LaneSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::LaneSegment, std::allocator<ad::map::route::LaneSegment> >)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RoadSegment)

    to_string( (RoadSegmentList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> >)

    to_string( (RouteCreationMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteCreationMode)

    to_string( (FullRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::FullRoute)

    to_string( (ConnectingRoute)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::ConnectingRoute)

    to_string( (FullRouteList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::route::FullRoute, std::allocator<ad::map::route::FullRoute> >)

    to_string( (LaneChangeDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::LaneChangeDirection)

    to_string( (RouteParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::route::RouteParaPoint)"""
def updateRoutePlanningCounters(ad) -> Any:
    """
    updateRoutePlanningCounters( (FullRoute)route) -> None :

        C++ signature :
            void updateRoutePlanningCounters(ad::map::route::FullRoute {lvalue})"""
