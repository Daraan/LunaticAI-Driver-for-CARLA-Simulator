import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

from carla.libcarla import _CarlaEnum

INVALID: TrafficType = TrafficType.INVALID
LEFT_HAND_TRAFFIC: TrafficType = TrafficType.LEFT_HAND_TRAFFIC
RIGHT_HAND_TRAFFIC: TrafficType = TrafficType.RIGHT_HAND_TRAFFIC

class MapMetaData(Boost.Python.instance):
    __instance_size__: ClassVar[int] = 32
    trafficType: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (MapMetaData)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::access::MapMetaData)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (MapMetaData)arg1, (MapMetaData)other) -> MapMetaData :

            C++ signature :
                ad::map::access::MapMetaData {lvalue} assign(ad::map::access::MapMetaData {lvalue},ad::map::access::MapMetaData)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (MapMetaData)arg1, (MapMetaData)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::access::MapMetaData {lvalue},ad::map::access::MapMetaData)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (MapMetaData)arg1, (MapMetaData)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::access::MapMetaData {lvalue},ad::map::access::MapMetaData)"""
    @classmethod
    def __reduce__(cls): ...

class PartitionId(Boost.Python.instance):
    cMaxValue: ClassVar[int] = ...  # read-only
    cMinValue: ClassVar[int] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iPartitionId) -> None :

            C++ signature :
                void __init__(_object*,unsigned long)

        __init__( (object)arg1, (PartitionId)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::access::PartitionId)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (PartitionId)arg1, (PartitionId)other) -> PartitionId :

            C++ signature :
                ad::map::access::PartitionId {lvalue} assign(ad::map::access::PartitionId {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (PartitionId)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::access::PartitionId {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (PartitionId)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::access::PartitionId {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> PartitionId :

            C++ signature :
                ad::map::access::PartitionId getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> PartitionId :

            C++ signature :
                ad::map::access::PartitionId getMin()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (PartitionId)arg1, (PartitionId)arg2) -> object :

            C++ signature :
                _object* __add__(ad::map::access::PartitionId {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (PartitionId)arg1, (PartitionId)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::access::PartitionId {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (PartitionId)arg1, (PartitionId)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::map::access::PartitionId {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (PartitionId)arg1, (PartitionId)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::map::access::PartitionId {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (PartitionId)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::map::access::PartitionId&>,ad::map::access::PartitionId)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (PartitionId)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::map::access::PartitionId&>,ad::map::access::PartitionId)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (PartitionId)arg1, (PartitionId)arg2) -> object :

            C++ signature :
                _object* __le__(ad::map::access::PartitionId {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def __long__(cls, ad) -> Any:
        """
        __long__( (PartitionId)arg1) -> int :

            C++ signature :
                unsigned long __long__(ad::map::access::PartitionId {lvalue})"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (PartitionId)arg1, (PartitionId)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::map::access::PartitionId {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (PartitionId)arg1, (PartitionId)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::access::PartitionId {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (PartitionId)arg1, (PartitionId)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::map::access::PartitionId {lvalue},ad::map::access::PartitionId)"""
    @property
    def Valid(self): ...

class PartitionIdList(Boost.Python.instance):
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
        append( (PartitionIdList)arg1, (PartitionId)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (PartitionIdList)arg1, (PartitionId)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (PartitionIdList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (PartitionIdList)arg1, (PartitionId)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (PartitionIdList)arg1, (int)arg2, (PartitionId)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},long,ad::map::access::PartitionId)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (PartitionIdList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (PartitionIdList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (PartitionIdList)arg1, (PartitionId)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},ad::map::access::PartitionId)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (PartitionIdList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},long)

        __delitem__( (PartitionIdList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (PartitionIdList)arg1, (int)arg2) -> PartitionId :

            C++ signature :
                ad::map::access::PartitionId {lvalue} __getitem__(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},long)

        __getitem__( (PartitionIdList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (PartitionIdList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (PartitionIdList)arg1, (int)arg2, (PartitionId)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},long,ad::map::access::PartitionId)

        __setitem__( (PartitionIdList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class TrafficType(int, _CarlaEnum):
    INVALID = 0
    LEFT_HAND_TRAFFIC = 1
    RIGHT_HAND_TRAFFIC = 2


class numeric_limits_less__ad_scope_map_scope_access_scope_PartitionId__greater_(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @staticmethod
    def epsilon() -> Any:
        """
        epsilon() -> PartitionId :

            C++ signature :
                ad::map::access::PartitionId epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> PartitionId :

            C++ signature :
                ad::map::access::PartitionId lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> PartitionId :

            C++ signature :
                ad::map::access::PartitionId max()"""
    @classmethod
    def __reduce__(cls): ...

def cleanup() -> Any:
    """
    cleanup() -> None :

        C++ signature :
            void cleanup()"""
def fromString(*args, **kwargs):
    """
    fromString( (str)str) -> TrafficType :

        C++ signature :
            ad::map::access::TrafficType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
def getCoordinateTransform() -> Any:
    """
    getCoordinateTransform() -> CoordinateTransform :

        C++ signature :
            std::shared_ptr<ad::map::point::CoordinateTransform> getCoordinateTransform()"""
def getENUReferencePoint() -> Any:
    """
    getENUReferencePoint() -> GeoPoint :

        C++ signature :
            ad::map::point::GeoPoint getENUReferencePoint()"""
def getLogger() -> Any:
    """
    getLogger() -> object :

        C++ signature :
            std::shared_ptr<spdlog::logger> getLogger()"""
def getPointOfInterest(*args, **kwargs):
    """
    getPointOfInterest( (str)name, (PointOfInterest)poi) -> bool :

        C++ signature :
            bool getPointOfInterest(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >,ad::map::config::PointOfInterest {lvalue})"""
def getPointsOfInterest() -> Any:
    """
    getPointsOfInterest( (GeoPoint)geoPoint, (Distance)radius) -> object :

        C++ signature :
            std::vector<ad::map::config::PointOfInterest, std::allocator<ad::map::config::PointOfInterest> > getPointsOfInterest(ad::map::point::GeoPoint,ad::physics::Distance)

    getPointsOfInterest() -> object :

        C++ signature :
            std::vector<ad::map::config::PointOfInterest, std::allocator<ad::map::config::PointOfInterest> > getPointsOfInterest()"""
def init(std) -> Any:
    """
    init( (str)configFileName) -> bool :

        C++ signature :
            bool init(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    init( (object)store) -> bool :

        C++ signature :
            bool init(std::shared_ptr<ad::map::access::Store>)"""
def initFromOpenDriveContent(*args, **kwargs):
    """
    initFromOpenDriveContent( (str)openDriveContent, (object)overlapMargin, (IntersectionType)defaultIntersectionType [, (TrafficLightType)defaultTrafficLightType=landmark.TrafficLightType.SOLID_RED_YELLOW_GREEN]) -> bool :

        C++ signature :
            bool initFromOpenDriveContent(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >,double,ad::map::intersection::IntersectionType [,ad::map::landmark::TrafficLightType=landmark.TrafficLightType.SOLID_RED_YELLOW_GREEN])"""
def isENUReferencePointSet() -> Any:
    """
    isENUReferencePointSet() -> bool :

        C++ signature :
            bool isENUReferencePointSet()"""
def isLeftHandedTraffic() -> Any:
    """
    isLeftHandedTraffic() -> bool :

        C++ signature :
            bool isLeftHandedTraffic()"""
def isRightHandedTraffic() -> Any:
    """
    isRightHandedTraffic() -> bool :

        C++ signature :
            bool isRightHandedTraffic()"""
def isValid(ad) -> Any:
    """
    isValid( (MapMetaData)metaData [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::access::MapMetaData [,bool=True])"""
def setENUReferencePoint(ad) -> Any:
    """
    setENUReferencePoint( (GeoPoint)point) -> None :

        C++ signature :
            void setENUReferencePoint(ad::map::point::GeoPoint)"""
def toString(ad) -> Any:
    """
    toString( (TrafficType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::access::TrafficType)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (TrafficType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::TrafficType)

    to_string( (MapMetaData)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::MapMetaData)

    to_string( (PartitionId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::PartitionId)

    to_string( (PartitionIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> >)

    to_string( (object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::GeometryStoreItem)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (TrafficType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::TrafficType)

    to_string( (MapMetaData)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::MapMetaData)

    to_string( (PartitionId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::PartitionId)

    to_string( (PartitionIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> >)

    to_string( (object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::GeometryStoreItem)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (TrafficType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::TrafficType)

    to_string( (MapMetaData)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::MapMetaData)

    to_string( (PartitionId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::PartitionId)

    to_string( (PartitionIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> >)

    to_string( (object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::GeometryStoreItem)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (TrafficType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::TrafficType)

    to_string( (MapMetaData)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::MapMetaData)

    to_string( (PartitionId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::PartitionId)

    to_string( (PartitionIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::access::PartitionId, std::allocator<ad::map::access::PartitionId> >)

    to_string( (object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::access::GeometryStoreItem)"""
