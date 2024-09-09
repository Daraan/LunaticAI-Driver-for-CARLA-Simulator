import Boost.Python
from typing import Any, ClassVar, overload

AllWayStop: IntersectionType
Crosswalk: IntersectionType
HasWay: IntersectionType
Left: TurnDirection
PriorityToRight: IntersectionType
PriorityToRightAndStraight: IntersectionType
Right: TurnDirection
Stop: IntersectionType
Straight: TurnDirection
TrafficLight: IntersectionType
UTurn: TurnDirection
Unknown: TurnDirection
Yield: IntersectionType

class CoreIntersection(Boost.Python.instance):
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def extractLanesOfCoreIntersection(cls, *args, **kwargs):
        """
        extractLanesOfCoreIntersection( (CoreIntersection)arg1, (LaneId)laneId) -> None :

            C++ signature :
                void extractLanesOfCoreIntersection(CoreIntersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @overload
    @staticmethod
    def getCoreIntersectionFor(ad) -> Any:
        """
        getCoreIntersectionFor( (LaneId)laneId) -> CoreIntersection :

            C++ signature :
                std::shared_ptr<ad::map::intersection::CoreIntersection> getCoreIntersectionFor(ad::map::lane::LaneId)

        getCoreIntersectionFor( (MapMatchedPosition)mapMatchedPosition) -> CoreIntersection :

            C++ signature :
                std::shared_ptr<ad::map::intersection::CoreIntersection> getCoreIntersectionFor(ad::map::match::MapMatchedPosition)"""
    @overload
    @staticmethod
    def getCoreIntersectionFor(ad) -> Any:
        """
        getCoreIntersectionFor( (LaneId)laneId) -> CoreIntersection :

            C++ signature :
                std::shared_ptr<ad::map::intersection::CoreIntersection> getCoreIntersectionFor(ad::map::lane::LaneId)

        getCoreIntersectionFor( (MapMatchedPosition)mapMatchedPosition) -> CoreIntersection :

            C++ signature :
                std::shared_ptr<ad::map::intersection::CoreIntersection> getCoreIntersectionFor(ad::map::match::MapMatchedPosition)"""
    @staticmethod
    def getCoreIntersectionsFor(*args, **kwargs):
        """
        getCoreIntersectionsFor( (LaneIdSet)laneIds) -> vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_ :

            C++ signature :
                std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > getCoreIntersectionsFor(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)

        getCoreIntersectionsFor( (LaneIdList)laneIds) -> vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_ :

            C++ signature :
                std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > getCoreIntersectionsFor(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> >)"""
    @overload
    @staticmethod
    def getCoreIntersectionsForInLaneMatches(ad) -> Any:
        """
        getCoreIntersectionsForInLaneMatches( (ENUPoint)position) -> vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_ :

            C++ signature :
                std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > getCoreIntersectionsForInLaneMatches(ad::map::point::ENUPoint)

        getCoreIntersectionsForInLaneMatches( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)mapMatchedPositionConfidenceList) -> vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_ :

            C++ signature :
                std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > getCoreIntersectionsForInLaneMatches(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)

        getCoreIntersectionsForInLaneMatches( (MapMatchedObjectBoundingBox)object) -> vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_ :

            C++ signature :
                std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > getCoreIntersectionsForInLaneMatches(ad::map::match::MapMatchedObjectBoundingBox)"""
    @overload
    @staticmethod
    def getCoreIntersectionsForInLaneMatches(ad) -> Any:
        """
        getCoreIntersectionsForInLaneMatches( (ENUPoint)position) -> vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_ :

            C++ signature :
                std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > getCoreIntersectionsForInLaneMatches(ad::map::point::ENUPoint)

        getCoreIntersectionsForInLaneMatches( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)mapMatchedPositionConfidenceList) -> vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_ :

            C++ signature :
                std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > getCoreIntersectionsForInLaneMatches(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)

        getCoreIntersectionsForInLaneMatches( (MapMatchedObjectBoundingBox)object) -> vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_ :

            C++ signature :
                std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > getCoreIntersectionsForInLaneMatches(ad::map::match::MapMatchedObjectBoundingBox)"""
    @staticmethod
    def getCoreIntersectionsForMap() -> Any:
        """
        getCoreIntersectionsForMap() -> vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_ :

            C++ signature :
                std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > getCoreIntersectionsForMap()"""
    @classmethod
    def getEntryParaPointOfExternalLane(cls, *args, **kwargs):
        """
        getEntryParaPointOfExternalLane( (CoreIntersection)arg1, (LaneId)laneId) -> ParaPoint :

            C++ signature :
                ad::map::point::ParaPoint getEntryParaPointOfExternalLane(CoreIntersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def getEntryParaPointOfInternalLane(cls, *args, **kwargs):
        """
        getEntryParaPointOfInternalLane( (CoreIntersection)arg1, (LaneId)laneId) -> ParaPoint :

            C++ signature :
                ad::map::point::ParaPoint getEntryParaPointOfInternalLane(CoreIntersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def getExitParaPointOfExternalLane(cls, *args, **kwargs):
        """
        getExitParaPointOfExternalLane( (CoreIntersection)arg1, (LaneId)laneId) -> ParaPoint :

            C++ signature :
                ad::map::point::ParaPoint getExitParaPointOfExternalLane(CoreIntersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def getExitParaPointOfInternalLane(cls, *args, **kwargs):
        """
        getExitParaPointOfInternalLane( (CoreIntersection)arg1, (LaneId)laneId) -> ParaPoint :

            C++ signature :
                ad::map::point::ParaPoint getExitParaPointOfInternalLane(CoreIntersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @staticmethod
    def isIntersectionOnRoute(ad) -> Any:
        """
        isIntersectionOnRoute( (FullRoute)route) -> bool :

            C++ signature :
                bool isIntersectionOnRoute(ad::map::route::FullRoute)"""
    @staticmethod
    def isLanePartOfAnIntersection(ad) -> Any:
        """
        isLanePartOfAnIntersection( (LaneId)laneId) -> bool :

            C++ signature :
                bool isLanePartOfAnIntersection(ad::map::lane::LaneId)"""
    @classmethod
    def isLanePartOfCoreIntersection(cls, *args, **kwargs):
        """
        isLanePartOfCoreIntersection( (CoreIntersection)arg1, (LaneId)laneId) -> bool :

            C++ signature :
                bool isLanePartOfCoreIntersection(CoreIntersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @staticmethod
    def isRoadSegmentEnteringIntersection(*args, **kwargs):
        """
        isRoadSegmentEnteringIntersection( (RouteIterator)routeIterator, (object)routePreviousSegmentIter) -> bool :

            C++ signature :
                bool isRoadSegmentEnteringIntersection(ad::map::route::RouteIterator,__gnu_cxx::__normal_iterator<ad::map::route::RoadSegment const*, std::vector<ad::map::route::RoadSegment, std::allocator<ad::map::route::RoadSegment> > > {lvalue})"""
    @staticmethod
    def isRoutePartOfAnIntersection(ad) -> Any:
        """
        isRoutePartOfAnIntersection( (FullRoute)route) -> bool :

            C++ signature :
                bool isRoutePartOfAnIntersection(ad::map::route::FullRoute)"""
    @classmethod
    def objectDistanceToIntersection(cls, *args, **kwargs):
        """
        objectDistanceToIntersection( (CoreIntersection)arg1, (Object)object) -> Distance :

            C++ signature :
                ad::physics::Distance objectDistanceToIntersection(ad::map::intersection::CoreIntersection {lvalue},ad::map::match::Object)"""
    @classmethod
    def objectRouteCrossesIntersection(cls, *args, **kwargs):
        """
        objectRouteCrossesIntersection( (CoreIntersection)arg1, (FullRoute)objectRoute) -> bool :

            C++ signature :
                bool objectRouteCrossesIntersection(ad::map::intersection::CoreIntersection {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def objectWithinIntersection(cls, *args, **kwargs):
        """
        objectWithinIntersection( (CoreIntersection)arg1, (MapMatchedObjectBoundingBox)object) -> bool :

            C++ signature :
                bool objectWithinIntersection(ad::map::intersection::CoreIntersection {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def __reduce__(cls): ...
    @property
    def BoundingSphere(self): ...
    @property
    def entryLanes(self): ...
    @property
    def entryParaPoints(self): ...
    @property
    def exitLanes(self): ...
    @property
    def exitParaPoints(self): ...
    @property
    def internalLanes(self): ...

class Intersection(CoreIntersection):
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """Raises an exception
        This class cannot be instantiated from Python
        """
    @classmethod
    def extractLanesOfCoreIntersection(cls, *args, **kwargs):
        """
        extractLanesOfCoreIntersection( (Intersection)arg1, (LaneId)laneId) -> None :

            C++ signature :
                void extractLanesOfCoreIntersection(Intersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def getEntryParaPointOfExternalLane(cls, *args, **kwargs):
        """
        getEntryParaPointOfExternalLane( (Intersection)arg1, (LaneId)laneId) -> ParaPoint :

            C++ signature :
                ad::map::point::ParaPoint getEntryParaPointOfExternalLane(Intersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def getEntryParaPointOfInternalLane(cls, *args, **kwargs):
        """
        getEntryParaPointOfInternalLane( (Intersection)arg1, (LaneId)laneId) -> ParaPoint :

            C++ signature :
                ad::map::point::ParaPoint getEntryParaPointOfInternalLane(Intersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def getExitParaPointOfExternalLane(cls, *args, **kwargs):
        """
        getExitParaPointOfExternalLane( (Intersection)arg1, (LaneId)laneId) -> ParaPoint :

            C++ signature :
                ad::map::point::ParaPoint getExitParaPointOfExternalLane(Intersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def getExitParaPointOfInternalLane(cls, *args, **kwargs):
        """
        getExitParaPointOfInternalLane( (Intersection)arg1, (LaneId)laneId) -> ParaPoint :

            C++ signature :
                ad::map::point::ParaPoint getExitParaPointOfInternalLane(Intersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @staticmethod
    def getIntersectionForRoadSegment(ad) -> Any:
        """
        getIntersectionForRoadSegment( (RouteIterator)routeIterator) -> Intersection :

            C++ signature :
                std::shared_ptr<ad::map::intersection::Intersection> getIntersectionForRoadSegment(ad::map::route::RouteIterator)"""
    @staticmethod
    def getIntersectionsForRoute(ad) -> Any:
        """
        getIntersectionsForRoute( (FullRoute)route) -> vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_ :

            C++ signature :
                std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > getIntersectionsForRoute(ad::map::route::FullRoute)"""
    @staticmethod
    def getNextIntersectionOnRoute(ad) -> Any:
        """
        getNextIntersectionOnRoute( (FullRoute)route) -> Intersection :

            C++ signature :
                std::shared_ptr<ad::map::intersection::Intersection> getNextIntersectionOnRoute(ad::map::route::FullRoute)"""
    @classmethod
    def isLanePartOfCoreIntersection(cls, *args, **kwargs):
        """
        isLanePartOfCoreIntersection( (Intersection)arg1, (LaneId)laneId) -> bool :

            C++ signature :
                bool isLanePartOfCoreIntersection(Intersection_wrapper {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def objectInterpenetrationDistanceWithIntersection(cls, *args, **kwargs):
        """
        objectInterpenetrationDistanceWithIntersection( (Intersection)arg1, (Object)object) -> Distance :

            C++ signature :
                ad::physics::Distance objectInterpenetrationDistanceWithIntersection(ad::map::intersection::Intersection {lvalue},ad::map::match::Object)"""
    @classmethod
    def objectOnCrossingLane(cls, *args, **kwargs):
        """
        objectOnCrossingLane( (Intersection)arg1, (MapMatchedObjectBoundingBox)object) -> bool :

            C++ signature :
                bool objectOnCrossingLane(ad::map::intersection::Intersection {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def objectOnIncomingLane(cls, *args, **kwargs):
        """
        objectOnIncomingLane( (Intersection)arg1, (MapMatchedObjectBoundingBox)object) -> bool :

            C++ signature :
                bool objectOnIncomingLane(ad::map::intersection::Intersection {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def objectOnIncomingLaneWithHigherPriority(cls, *args, **kwargs):
        """
        objectOnIncomingLaneWithHigherPriority( (Intersection)arg1, (MapMatchedObjectBoundingBox)object) -> bool :

            C++ signature :
                bool objectOnIncomingLaneWithHigherPriority(ad::map::intersection::Intersection {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def objectOnIncomingLaneWithLowerPriority(cls, *args, **kwargs):
        """
        objectOnIncomingLaneWithLowerPriority( (Intersection)arg1, (MapMatchedObjectBoundingBox)object) -> bool :

            C++ signature :
                bool objectOnIncomingLaneWithLowerPriority(ad::map::intersection::Intersection {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def objectOnInternalLaneWithHigherPriority(cls, *args, **kwargs):
        """
        objectOnInternalLaneWithHigherPriority( (Intersection)arg1, (MapMatchedObjectBoundingBox)object) -> bool :

            C++ signature :
                bool objectOnInternalLaneWithHigherPriority(ad::map::intersection::Intersection {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def objectOnInternalLaneWithLowerPriority(cls, *args, **kwargs):
        """
        objectOnInternalLaneWithLowerPriority( (Intersection)arg1, (MapMatchedObjectBoundingBox)object) -> bool :

            C++ signature :
                bool objectOnInternalLaneWithLowerPriority(ad::map::intersection::Intersection {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def objectOnIntersectionRoute(cls, *args, **kwargs):
        """
        objectOnIntersectionRoute( (Intersection)arg1, (MapMatchedObjectBoundingBox)object) -> bool :

            C++ signature :
                bool objectOnIntersectionRoute(ad::map::intersection::Intersection {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def objectOnLaneWithHigherPriority(cls, *args, **kwargs):
        """
        objectOnLaneWithHigherPriority( (Intersection)arg1, (MapMatchedObjectBoundingBox)object) -> bool :

            C++ signature :
                bool objectOnLaneWithHigherPriority(ad::map::intersection::Intersection {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def objectOnLaneWithLowerPriority(cls, *args, **kwargs):
        """
        objectOnLaneWithLowerPriority( (Intersection)arg1, (MapMatchedObjectBoundingBox)object) -> bool :

            C++ signature :
                bool objectOnLaneWithLowerPriority(ad::map::intersection::Intersection {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def objectRouteCrossesIntersectionRoute(cls, *args, **kwargs):
        """
        objectRouteCrossesIntersectionRoute( (Intersection)arg1, (FullRoute)objectRoute) -> bool :

            C++ signature :
                bool objectRouteCrossesIntersectionRoute(ad::map::intersection::Intersection {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def objectRouteCrossesLanesWithHigherPriority(cls, *args, **kwargs):
        """
        objectRouteCrossesLanesWithHigherPriority( (Intersection)arg1, (FullRoute)objectRoute) -> bool :

            C++ signature :
                bool objectRouteCrossesLanesWithHigherPriority(ad::map::intersection::Intersection {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def objectRouteFromSameArmAsIntersectionRoute(cls, *args, **kwargs):
        """
        objectRouteFromSameArmAsIntersectionRoute( (Intersection)arg1, (FullRoute)objectRoute) -> bool :

            C++ signature :
                bool objectRouteFromSameArmAsIntersectionRoute(ad::map::intersection::Intersection {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def objectRouteOppositeToIntersectionRoute(cls, *args, **kwargs):
        """
        objectRouteOppositeToIntersectionRoute( (Intersection)arg1, (FullRoute)objectRoute) -> bool :

            C++ signature :
                bool objectRouteOppositeToIntersectionRoute(ad::map::intersection::Intersection {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def onlySolidTrafficLightsOnRoute(cls, ad) -> Any:
        """
        onlySolidTrafficLightsOnRoute( (Intersection)arg1) -> bool :

            C++ signature :
                bool onlySolidTrafficLightsOnRoute(ad::map::intersection::Intersection {lvalue})"""
    @classmethod
    def updateRouteCounters(cls, *args, **kwargs):
        """
        updateRouteCounters( (Intersection)arg1, (object)newRoutePlanningCounter, (object)newRouteSegmentCounter) -> None :

            C++ signature :
                void updateRouteCounters(ad::map::intersection::Intersection {lvalue},unsigned long,unsigned long)"""
    @classmethod
    def __reduce__(cls): ...
    @property
    def IntersectionStartOnRoute(self): ...
    @property
    def RoutePlanningCounter(self): ...
    @property
    def RouteSegmentCountFromDestination(self): ...
    @property
    def SpeedLimit(self): ...
    @property
    def applicableTrafficLights(self): ...
    @property
    def crossingLanes(self): ...
    @property
    def incomingLanes(self): ...
    @property
    def incomingLanesOnRoute(self): ...
    @property
    def incomingLanesWithHigherPriority(self): ...
    @property
    def incomingLanesWithLowerPriority(self): ...
    @property
    def incomingParaPoints(self): ...
    @property
    def incomingParaPointsOnRoute(self): ...
    @property
    def incomingParaPointsWithHigherPriority(self): ...
    @property
    def incomingParaPointsWithLowerPriority(self): ...
    @property
    def internalLanesWithHigherPriority(self): ...
    @property
    def internalLanesWithLowerPriority(self): ...
    @property
    def intersectionType(self): ...
    @property
    def lanesOnRoute(self): ...
    @property
    def outgoingLanes(self): ...
    @property
    def outgoingLanesOnRoute(self): ...
    @property
    def outgoingParaPoints(self): ...
    @property
    def outgoingParaPointsOnRoute(self): ...
    @property
    def paraPointsOnRoute(self): ...
    @property
    def turnDirection(self): ...

class IntersectionType(Boost.Python.enum):
    AllWayStop: ClassVar[IntersectionType] = ...
    Crosswalk: ClassVar[IntersectionType] = ...
    HasWay: ClassVar[IntersectionType] = ...
    PriorityToRight: ClassVar[IntersectionType] = ...
    PriorityToRightAndStraight: ClassVar[IntersectionType] = ...
    Stop: ClassVar[IntersectionType] = ...
    TrafficLight: ClassVar[IntersectionType] = ...
    Unknown: ClassVar[IntersectionType] = ...
    Yield: ClassVar[IntersectionType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class TurnDirection(Boost.Python.enum):
    Left: ClassVar[TurnDirection] = ...
    Right: ClassVar[TurnDirection] = ...
    Straight: ClassVar[TurnDirection] = ...
    UTurn: ClassVar[TurnDirection] = ...
    Unknown: ClassVar[TurnDirection] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_(Boost.Python.instance):
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
        append( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void append(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},std::shared_ptr<ad::map::intersection::CoreIntersection>)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (object)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},std::shared_ptr<ad::map::intersection::CoreIntersection>)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (object)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},std::shared_ptr<ad::map::intersection::CoreIntersection>)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (int)arg2, (object)arg3) -> None :

            C++ signature :
                void insert(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},long,std::shared_ptr<ad::map::intersection::CoreIntersection>)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1) -> None :

            C++ signature :
                void reverse(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1) -> None :

            C++ signature :
                void sort(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (object)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},std::shared_ptr<ad::map::intersection::CoreIntersection>)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},long)

        __delitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (int)arg2) -> CoreIntersection :

            C++ signature :
                std::shared_ptr<ad::map::intersection::CoreIntersection> {lvalue} __getitem__(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},long)

        __getitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (int)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},long,std::shared_ptr<ad::map::intersection::CoreIntersection>)

        __setitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_CoreIntersection_greater__greater_)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<std::shared_ptr<ad::map::intersection::CoreIntersection>, std::allocator<std::shared_ptr<ad::map::intersection::CoreIntersection> > > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_(Boost.Python.instance):
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
        append( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (Intersection)arg2) -> None :

            C++ signature :
                void append(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},std::shared_ptr<ad::map::intersection::Intersection>)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (Intersection)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},std::shared_ptr<ad::map::intersection::Intersection>)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (Intersection)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},std::shared_ptr<ad::map::intersection::Intersection>)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (int)arg2, (Intersection)arg3) -> None :

            C++ signature :
                void insert(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},long,std::shared_ptr<ad::map::intersection::Intersection>)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1) -> None :

            C++ signature :
                void reverse(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1) -> None :

            C++ signature :
                void sort(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (Intersection)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},std::shared_ptr<ad::map::intersection::Intersection>)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},long)

        __delitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (int)arg2) -> Intersection :

            C++ signature :
                std::shared_ptr<ad::map::intersection::Intersection> {lvalue} __getitem__(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},long)

        __getitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (int)arg2, (Intersection)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},long,std::shared_ptr<ad::map::intersection::Intersection>)

        __setitem__( (vector_less_std_scope_shared_ptr_less_ad_scope_map_scope_intersection_scope_Intersection_greater__greater_)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<std::shared_ptr<ad::map::intersection::Intersection>, std::allocator<std::shared_ptr<ad::map::intersection::Intersection> > > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

def fromString(*args, **kwargs):
    """
    fromString( (str)str) -> IntersectionType :

        C++ signature :
            ad::map::intersection::IntersectionType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> TurnDirection :

        C++ signature :
            ad::map::intersection::TurnDirection fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
@overload
def toString(ad) -> Any:
    """
    toString( (IntersectionType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::intersection::IntersectionType)

    toString( (TurnDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::intersection::TurnDirection)"""
@overload
def toString(ad) -> Any:
    """
    toString( (IntersectionType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::intersection::IntersectionType)

    toString( (TurnDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::intersection::TurnDirection)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (IntersectionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::IntersectionType)

    to_string( (CoreIntersection)intersection) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::CoreIntersection)

    to_string( (TurnDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::TurnDirection)

    to_string( (Intersection)intersection) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::Intersection)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (IntersectionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::IntersectionType)

    to_string( (CoreIntersection)intersection) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::CoreIntersection)

    to_string( (TurnDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::TurnDirection)

    to_string( (Intersection)intersection) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::Intersection)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (IntersectionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::IntersectionType)

    to_string( (CoreIntersection)intersection) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::CoreIntersection)

    to_string( (TurnDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::TurnDirection)

    to_string( (Intersection)intersection) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::Intersection)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (IntersectionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::IntersectionType)

    to_string( (CoreIntersection)intersection) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::CoreIntersection)

    to_string( (TurnDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::TurnDirection)

    to_string( (Intersection)intersection) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::intersection::Intersection)"""
