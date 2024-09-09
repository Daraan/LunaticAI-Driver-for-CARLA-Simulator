import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

Center: ObjectReferencePoints
FrontLeft: ObjectReferencePoints
FrontRight: ObjectReferencePoints
INVALID: MapMatchedPositionType
LANE_IN: MapMatchedPositionType
LANE_LEFT: MapMatchedPositionType
LANE_RIGHT: MapMatchedPositionType
NumPoints: ObjectReferencePoints
RearLeft: ObjectReferencePoints
RearRight: ObjectReferencePoints
UNKNOWN: MapMatchedPositionType

class AdMapMatching(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    MaxHeadingHintFactor: Incomplete
    RouteHintFactor: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def addHeadingHint(cls, *args, **kwargs):
        """
        addHeadingHint( (AdMapMatching)arg1, (ECEFHeading)headingHint) -> None :

            C++ signature :
                void addHeadingHint(ad::map::match::AdMapMatching {lvalue},ad::map::point::ECEFHeading)

        addHeadingHint( (AdMapMatching)arg1, (ENUHeading)yaw, (GeoPoint)enuReferencePoint) -> None :

            C++ signature :
                void addHeadingHint(ad::map::match::AdMapMatching {lvalue},ad::map::point::ENUHeading,ad::map::point::GeoPoint)"""
    @classmethod
    def addRouteHint(cls, *args, **kwargs):
        """
        addRouteHint( (AdMapMatching)arg1, (FullRoute)routeHint) -> None :

            C++ signature :
                void addRouteHint(ad::map::match::AdMapMatching {lvalue},ad::map::route::FullRoute)"""
    @classmethod
    def clearHeadingHints(cls, ad) -> Any:
        """
        clearHeadingHints( (AdMapMatching)arg1) -> None :

            C++ signature :
                void clearHeadingHints(ad::map::match::AdMapMatching {lvalue})"""
    @classmethod
    def clearHints(cls, ad) -> Any:
        """
        clearHints( (AdMapMatching)arg1) -> None :

            C++ signature :
                void clearHints(ad::map::match::AdMapMatching {lvalue})"""
    @classmethod
    def clearRelevantLanes(cls, ad) -> Any:
        """
        clearRelevantLanes( (AdMapMatching)arg1) -> None :

            C++ signature :
                void clearRelevantLanes(ad::map::match::AdMapMatching {lvalue})"""
    @classmethod
    def clearRouteHints(cls, ad) -> Any:
        """
        clearRouteHints( (AdMapMatching)arg1) -> None :

            C++ signature :
                void clearRouteHints(ad::map::match::AdMapMatching {lvalue})"""
    @staticmethod
    def findLanes(*args, **kwargs):
        """
        findLanes( (ECEFPoint)ecefPoint, (Distance)distance [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c85741f0>]) -> vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_ :

            C++ signature :
                std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > findLanes(ad::map::point::ECEFPoint,ad::physics::Distance [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c85741f0>])

        findLanes( (GeoPoint)geoPoint, (Distance)distance [, (LaneIdSet)relevantLanes=<lane.LaneIdSet object at 0x7752c8575ab0>]) -> vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_ :

            C++ signature :
                std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > findLanes(ad::map::point::GeoPoint,ad::physics::Distance [,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >=<lane.LaneIdSet object at 0x7752c8575ab0>])"""
    @staticmethod
    def findRouteLanes(*args, **kwargs):
        """
        findRouteLanes( (ECEFPoint)ecefPoint, (FullRoute)route) -> vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_ :

            C++ signature :
                std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > findRouteLanes(ad::map::point::ECEFPoint,ad::map::route::FullRoute)"""
    @classmethod
    def getLaneENUHeading(cls, *args, **kwargs):
        """
        getLaneENUHeading( (AdMapMatching)arg1, (MapMatchedPosition)mapMatchedPosition) -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading getLaneENUHeading(ad::map::match::AdMapMatching {lvalue},ad::map::match::MapMatchedPosition)"""
    @classmethod
    def getLaneOccupiedRegions(cls, *args, **kwargs):
        """
        getLaneOccupiedRegions( (AdMapMatching)arg1, (ENUObjectPositionList)enuObjectPositionList [, (Distance)samplingDistance=<physics.Distance object at 0x7752c8de2e30>]) -> LaneOccupiedRegionList :

            C++ signature :
                std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > getLaneOccupiedRegions(ad::map::match::AdMapMatching {lvalue},std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > [,ad::physics::Distance=<physics.Distance object at 0x7752c8de2e30>])"""
    @classmethod
    def getMapMatchedBoundingBox(cls, *args, **kwargs):
        """
        getMapMatchedBoundingBox( (AdMapMatching)arg1, (ENUObjectPosition)enuObjectPosition [, (Distance)samplingDistance=<physics.Distance object at 0x7752c8de2500>]) -> MapMatchedObjectBoundingBox :

            C++ signature :
                ad::map::match::MapMatchedObjectBoundingBox getMapMatchedBoundingBox(ad::map::match::AdMapMatching {lvalue},ad::map::match::ENUObjectPosition [,ad::physics::Distance=<physics.Distance object at 0x7752c8de2500>])"""
    @classmethod
    def getMapMatchedPositions(cls, *args, **kwargs):
        """
        getMapMatchedPositions( (AdMapMatching)arg1, (GeoPoint)geoPoint, (Distance)distance, (Probability)minProbability) -> vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_ :

            C++ signature :
                std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > getMapMatchedPositions(ad::map::match::AdMapMatching {lvalue},ad::map::point::GeoPoint,ad::physics::Distance,ad::physics::Probability)

        getMapMatchedPositions( (AdMapMatching)arg1, (ENUPoint)enuPoint, (GeoPoint)enuReferencePoint, (Distance)distance, (Probability)minProbability) -> vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_ :

            C++ signature :
                std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > getMapMatchedPositions(ad::map::match::AdMapMatching {lvalue},ad::map::point::ENUPoint,ad::map::point::GeoPoint,ad::physics::Distance,ad::physics::Probability)

        getMapMatchedPositions( (AdMapMatching)arg1, (ENUPoint)enuPoint, (Distance)distance, (Probability)minProbability) -> vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_ :

            C++ signature :
                std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > getMapMatchedPositions(ad::map::match::AdMapMatching {lvalue},ad::map::point::ENUPoint,ad::physics::Distance,ad::physics::Probability)

        getMapMatchedPositions( (AdMapMatching)arg1, (ENUObjectPosition)enuObjectPosition, (Distance)distance, (Probability)minProbability) -> vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_ :

            C++ signature :
                std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > getMapMatchedPositions(ad::map::match::AdMapMatching {lvalue},ad::map::match::ENUObjectPosition,ad::physics::Distance,ad::physics::Probability)"""
    @classmethod
    def setRelevantLanes(cls, *args, **kwargs):
        """
        setRelevantLanes( (AdMapMatching)arg1, (LaneIdSet)relevantLanes) -> None :

            C++ signature :
                void setRelevantLanes(ad::map::match::AdMapMatching {lvalue},std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
    @classmethod
    def __reduce__(cls): ...

class ENUObjectPosition(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    centerPoint: Incomplete
    dimension: Incomplete
    enuReferencePoint: Incomplete
    heading: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (ENUObjectPosition)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::match::ENUObjectPosition)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ENUObjectPosition)arg1, (ENUObjectPosition)other) -> ENUObjectPosition :

            C++ signature :
                ad::map::match::ENUObjectPosition {lvalue} assign(ad::map::match::ENUObjectPosition {lvalue},ad::map::match::ENUObjectPosition)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ENUObjectPosition)arg1, (ENUObjectPosition)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::match::ENUObjectPosition {lvalue},ad::map::match::ENUObjectPosition)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ENUObjectPosition)arg1, (ENUObjectPosition)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::match::ENUObjectPosition {lvalue},ad::map::match::ENUObjectPosition)"""
    @classmethod
    def __reduce__(cls): ...

class ENUObjectPositionList(Boost.Python.instance):
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
        append( (ENUObjectPositionList)arg1, (ENUObjectPosition)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},ad::map::match::ENUObjectPosition)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ENUObjectPositionList)arg1, (ENUObjectPosition)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},ad::map::match::ENUObjectPosition)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ENUObjectPositionList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ENUObjectPositionList)arg1, (ENUObjectPosition)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},ad::map::match::ENUObjectPosition)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ENUObjectPositionList)arg1, (int)arg2, (ENUObjectPosition)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},long,ad::map::match::ENUObjectPosition)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ENUObjectPositionList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ENUObjectPositionList)arg1, (ENUObjectPosition)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},ad::map::match::ENUObjectPosition)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ENUObjectPositionList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},long)

        __delitem__( (ENUObjectPositionList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ENUObjectPositionList)arg1, (int)arg2) -> ENUObjectPosition :

            C++ signature :
                ad::map::match::ENUObjectPosition {lvalue} __getitem__(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},long)

        __getitem__( (ENUObjectPositionList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ENUObjectPositionList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ENUObjectPositionList)arg1, (int)arg2, (ENUObjectPosition)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},long,ad::map::match::ENUObjectPosition)

        __setitem__( (ENUObjectPositionList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class LaneOccupiedRegion(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    laneId: Incomplete
    lateralRange: Incomplete
    longitudinalRange: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (LaneOccupiedRegion)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::match::LaneOccupiedRegion)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (LaneOccupiedRegion)arg1, (LaneOccupiedRegion)other) -> LaneOccupiedRegion :

            C++ signature :
                ad::map::match::LaneOccupiedRegion {lvalue} assign(ad::map::match::LaneOccupiedRegion {lvalue},ad::map::match::LaneOccupiedRegion)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (LaneOccupiedRegion)arg1, (LaneOccupiedRegion)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::match::LaneOccupiedRegion {lvalue},ad::map::match::LaneOccupiedRegion)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (LaneOccupiedRegion)arg1, (LaneOccupiedRegion)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::match::LaneOccupiedRegion {lvalue},ad::map::match::LaneOccupiedRegion)"""
    @classmethod
    def __reduce__(cls): ...

class LaneOccupiedRegionList(Boost.Python.instance):
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
        append( (LaneOccupiedRegionList)arg1, (LaneOccupiedRegion)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},ad::map::match::LaneOccupiedRegion)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (LaneOccupiedRegionList)arg1, (LaneOccupiedRegion)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},ad::map::match::LaneOccupiedRegion)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (LaneOccupiedRegionList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (LaneOccupiedRegionList)arg1, (LaneOccupiedRegion)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},ad::map::match::LaneOccupiedRegion)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (LaneOccupiedRegionList)arg1, (int)arg2, (LaneOccupiedRegion)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},long,ad::map::match::LaneOccupiedRegion)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (LaneOccupiedRegionList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (LaneOccupiedRegionList)arg1, (LaneOccupiedRegion)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},ad::map::match::LaneOccupiedRegion)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (LaneOccupiedRegionList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},long)

        __delitem__( (LaneOccupiedRegionList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (LaneOccupiedRegionList)arg1, (int)arg2) -> LaneOccupiedRegion :

            C++ signature :
                ad::map::match::LaneOccupiedRegion {lvalue} __getitem__(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},long)

        __getitem__( (LaneOccupiedRegionList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (LaneOccupiedRegionList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (LaneOccupiedRegionList)arg1, (int)arg2, (LaneOccupiedRegion)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},long,ad::map::match::LaneOccupiedRegion)

        __setitem__( (LaneOccupiedRegionList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class LanePoint(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    laneLength: Incomplete
    laneWidth: Incomplete
    lateralT: Incomplete
    paraPoint: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (LanePoint)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::match::LanePoint)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (LanePoint)arg1, (LanePoint)other) -> LanePoint :

            C++ signature :
                ad::map::match::LanePoint {lvalue} assign(ad::map::match::LanePoint {lvalue},ad::map::match::LanePoint)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (LanePoint)arg1, (LanePoint)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::match::LanePoint {lvalue},ad::map::match::LanePoint)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (LanePoint)arg1, (LanePoint)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::match::LanePoint {lvalue},ad::map::match::LanePoint)"""
    @classmethod
    def __reduce__(cls): ...

class MapMatchedObjectBoundingBox(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    laneOccupiedRegions: Incomplete
    matchRadius: Incomplete
    referencePointPositions: Incomplete
    samplingDistance: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (MapMatchedObjectBoundingBox)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (MapMatchedObjectBoundingBox)arg1, (MapMatchedObjectBoundingBox)other) -> MapMatchedObjectBoundingBox :

            C++ signature :
                ad::map::match::MapMatchedObjectBoundingBox {lvalue} assign(ad::map::match::MapMatchedObjectBoundingBox {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (MapMatchedObjectBoundingBox)arg1, (MapMatchedObjectBoundingBox)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::match::MapMatchedObjectBoundingBox {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (MapMatchedObjectBoundingBox)arg1, (MapMatchedObjectBoundingBox)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::match::MapMatchedObjectBoundingBox {lvalue},ad::map::match::MapMatchedObjectBoundingBox)"""
    @classmethod
    def __reduce__(cls): ...

class MapMatchedObjectReferencePositionList(Boost.Python.instance):
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
        append( (MapMatchedObjectReferencePositionList)arg1, (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg2) -> None :

            C++ signature :
                void append(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > > {lvalue},std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (MapMatchedObjectReferencePositionList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > > {lvalue},boost::python::api::object)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (MapMatchedObjectReferencePositionList)arg1, (int)arg2, (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg3) -> None :

            C++ signature :
                void insert(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > > {lvalue},long,std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (MapMatchedObjectReferencePositionList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > > {lvalue})"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (MapMatchedObjectReferencePositionList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > > {lvalue},long)

        __delitem__( (MapMatchedObjectReferencePositionList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (MapMatchedObjectReferencePositionList)arg1, (int)arg2) -> vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_ :

            C++ signature :
                std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue} __getitem__(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > > {lvalue},long)

        __getitem__( (MapMatchedObjectReferencePositionList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (MapMatchedObjectReferencePositionList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (MapMatchedObjectReferencePositionList)arg1, (int)arg2, (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > > {lvalue},long,std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)

        __setitem__( (MapMatchedObjectReferencePositionList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class MapMatchedPosition(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    lanePoint: Incomplete
    matchedPoint: Incomplete
    matchedPointDistance: Incomplete
    probability: Incomplete
    queryPoint: Incomplete
    type: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (MapMatchedPosition)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::match::MapMatchedPosition)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (MapMatchedPosition)arg1, (MapMatchedPosition)other) -> MapMatchedPosition :

            C++ signature :
                ad::map::match::MapMatchedPosition {lvalue} assign(ad::map::match::MapMatchedPosition {lvalue},ad::map::match::MapMatchedPosition)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (MapMatchedPosition)arg1, (MapMatchedPosition)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::match::MapMatchedPosition {lvalue},ad::map::match::MapMatchedPosition)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (MapMatchedPosition)arg1, (MapMatchedPosition)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::match::MapMatchedPosition {lvalue},ad::map::match::MapMatchedPosition)"""
    @classmethod
    def __reduce__(cls): ...

class MapMatchedPositionType(Boost.Python.enum):
    INVALID: ClassVar[MapMatchedPositionType] = ...
    LANE_IN: ClassVar[MapMatchedPositionType] = ...
    LANE_LEFT: ClassVar[MapMatchedPositionType] = ...
    LANE_RIGHT: ClassVar[MapMatchedPositionType] = ...
    UNKNOWN: ClassVar[MapMatchedPositionType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class Object(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    enuPosition: Incomplete
    mapMatchedBoundingBox: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Object)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::match::Object)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Object)arg1, (Object)other) -> Object :

            C++ signature :
                ad::map::match::Object {lvalue} assign(ad::map::match::Object {lvalue},ad::map::match::Object)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Object)arg1, (Object)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::match::Object {lvalue},ad::map::match::Object)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Object)arg1, (Object)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::match::Object {lvalue},ad::map::match::Object)"""
    @classmethod
    def __reduce__(cls): ...

class ObjectReferencePoints(Boost.Python.enum):
    Center: ClassVar[ObjectReferencePoints] = ...
    FrontLeft: ClassVar[ObjectReferencePoints] = ...
    FrontRight: ClassVar[ObjectReferencePoints] = ...
    NumPoints: ClassVar[ObjectReferencePoints] = ...
    RearLeft: ClassVar[ObjectReferencePoints] = ...
    RearRight: ClassVar[ObjectReferencePoints] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_(Boost.Python.instance):
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
        append( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (MapMatchedPosition)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},ad::map::match::MapMatchedPosition)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (MapMatchedPosition)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},ad::map::match::MapMatchedPosition)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (MapMatchedPosition)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},ad::map::match::MapMatchedPosition)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (int)arg2, (MapMatchedPosition)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},long,ad::map::match::MapMatchedPosition)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (MapMatchedPosition)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},ad::map::match::MapMatchedPosition)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},long)

        __delitem__( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (int)arg2) -> MapMatchedPosition :

            C++ signature :
                ad::map::match::MapMatchedPosition {lvalue} __getitem__(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},long)

        __getitem__( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (int)arg2, (MapMatchedPosition)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},long,ad::map::match::MapMatchedPosition)

        __setitem__( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

def fromString(*args, **kwargs):
    """
    fromString( (str)str) -> MapMatchedPositionType :

        C++ signature :
            ad::map::match::MapMatchedPositionType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> ObjectReferencePoints :

        C++ signature :
            ad::map::match::ObjectReferencePoints fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
def getCenterParaPoint(ad) -> Any:
    """
    getCenterParaPoint( (LaneOccupiedRegion)occupiedRegion) -> ParaPoint :

        C++ signature :
            ad::map::point::ParaPoint getCenterParaPoint(ad::map::match::LaneOccupiedRegion)"""
def getObjectENUHeading(ad) -> Any:
    """
    getObjectENUHeading( (MapMatchedObjectBoundingBox)mapMatchedBoundingBox) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading getObjectENUHeading(ad::map::match::MapMatchedObjectBoundingBox)"""
def getParaPoints(*args, **kwargs):
    """
    getParaPoints( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)inMapMatchedPositions) -> ParaPointList :

        C++ signature :
            std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > getParaPoints(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)"""
def isLaneType(ad) -> Any:
    """
    isLaneType( (MapMatchedPositionType)mapMatchedPositionType) -> bool :

        C++ signature :
            bool isLaneType(ad::map::match::MapMatchedPositionType)"""
def signedDistanceToLane(*args, **kwargs):
    """
    signedDistanceToLane( (LaneId)checkLaneId, (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)mapMatchedPositions) -> Distance :

        C++ signature :
            ad::physics::Distance signedDistanceToLane(ad::map::lane::LaneId,std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)"""
@overload
def toString(ad) -> Any:
    """
    toString( (MapMatchedPositionType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::match::MapMatchedPositionType)

    toString( (ObjectReferencePoints)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::match::ObjectReferencePoints)"""
@overload
def toString(ad) -> Any:
    """
    toString( (MapMatchedPositionType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::match::MapMatchedPositionType)

    toString( (ObjectReferencePoints)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::match::ObjectReferencePoints)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneOccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LaneOccupiedRegion)

    to_string( (LaneOccupiedRegionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> >)

    to_string( (ENUObjectPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ENUObjectPosition)

    to_string( (LanePoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LanePoint)

    to_string( (MapMatchedPositionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPositionType)

    to_string( (MapMatchedPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPosition)

    to_string( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)

    to_string( (MapMatchedObjectReferencePositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > >)

    to_string( (MapMatchedObjectBoundingBox)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedObjectBoundingBox)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::Object)

    to_string( (ENUObjectPositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> >)

    to_string( (ObjectReferencePoints)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ObjectReferencePoints)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneOccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LaneOccupiedRegion)

    to_string( (LaneOccupiedRegionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> >)

    to_string( (ENUObjectPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ENUObjectPosition)

    to_string( (LanePoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LanePoint)

    to_string( (MapMatchedPositionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPositionType)

    to_string( (MapMatchedPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPosition)

    to_string( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)

    to_string( (MapMatchedObjectReferencePositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > >)

    to_string( (MapMatchedObjectBoundingBox)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedObjectBoundingBox)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::Object)

    to_string( (ENUObjectPositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> >)

    to_string( (ObjectReferencePoints)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ObjectReferencePoints)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneOccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LaneOccupiedRegion)

    to_string( (LaneOccupiedRegionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> >)

    to_string( (ENUObjectPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ENUObjectPosition)

    to_string( (LanePoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LanePoint)

    to_string( (MapMatchedPositionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPositionType)

    to_string( (MapMatchedPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPosition)

    to_string( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)

    to_string( (MapMatchedObjectReferencePositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > >)

    to_string( (MapMatchedObjectBoundingBox)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedObjectBoundingBox)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::Object)

    to_string( (ENUObjectPositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> >)

    to_string( (ObjectReferencePoints)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ObjectReferencePoints)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneOccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LaneOccupiedRegion)

    to_string( (LaneOccupiedRegionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> >)

    to_string( (ENUObjectPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ENUObjectPosition)

    to_string( (LanePoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LanePoint)

    to_string( (MapMatchedPositionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPositionType)

    to_string( (MapMatchedPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPosition)

    to_string( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)

    to_string( (MapMatchedObjectReferencePositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > >)

    to_string( (MapMatchedObjectBoundingBox)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedObjectBoundingBox)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::Object)

    to_string( (ENUObjectPositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> >)

    to_string( (ObjectReferencePoints)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ObjectReferencePoints)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneOccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LaneOccupiedRegion)

    to_string( (LaneOccupiedRegionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> >)

    to_string( (ENUObjectPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ENUObjectPosition)

    to_string( (LanePoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LanePoint)

    to_string( (MapMatchedPositionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPositionType)

    to_string( (MapMatchedPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPosition)

    to_string( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)

    to_string( (MapMatchedObjectReferencePositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > >)

    to_string( (MapMatchedObjectBoundingBox)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedObjectBoundingBox)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::Object)

    to_string( (ENUObjectPositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> >)

    to_string( (ObjectReferencePoints)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ObjectReferencePoints)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneOccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LaneOccupiedRegion)

    to_string( (LaneOccupiedRegionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> >)

    to_string( (ENUObjectPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ENUObjectPosition)

    to_string( (LanePoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LanePoint)

    to_string( (MapMatchedPositionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPositionType)

    to_string( (MapMatchedPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPosition)

    to_string( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)

    to_string( (MapMatchedObjectReferencePositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > >)

    to_string( (MapMatchedObjectBoundingBox)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedObjectBoundingBox)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::Object)

    to_string( (ENUObjectPositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> >)

    to_string( (ObjectReferencePoints)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ObjectReferencePoints)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneOccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LaneOccupiedRegion)

    to_string( (LaneOccupiedRegionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> >)

    to_string( (ENUObjectPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ENUObjectPosition)

    to_string( (LanePoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LanePoint)

    to_string( (MapMatchedPositionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPositionType)

    to_string( (MapMatchedPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPosition)

    to_string( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)

    to_string( (MapMatchedObjectReferencePositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > >)

    to_string( (MapMatchedObjectBoundingBox)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedObjectBoundingBox)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::Object)

    to_string( (ENUObjectPositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> >)

    to_string( (ObjectReferencePoints)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ObjectReferencePoints)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneOccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LaneOccupiedRegion)

    to_string( (LaneOccupiedRegionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::LaneOccupiedRegion, std::allocator<ad::map::match::LaneOccupiedRegion> >)

    to_string( (ENUObjectPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ENUObjectPosition)

    to_string( (LanePoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::LanePoint)

    to_string( (MapMatchedPositionType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPositionType)

    to_string( (MapMatchedPosition)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedPosition)

    to_string( (vector_less_ad_scope_map_scope_match_scope_MapMatchedPosition_greater_)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >)

    to_string( (MapMatchedObjectReferencePositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> >, std::allocator<std::vector<ad::map::match::MapMatchedPosition, std::allocator<ad::map::match::MapMatchedPosition> > > >)

    to_string( (MapMatchedObjectBoundingBox)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::MapMatchedObjectBoundingBox)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::Object)

    to_string( (ENUObjectPositionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::match::ENUObjectPosition, std::allocator<ad::map::match::ENUObjectPosition> >)

    to_string( (ObjectReferencePoints)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::match::ObjectReferencePoints)"""
