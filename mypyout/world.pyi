import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

ArtificialObject: ObjectType
Bidirectional: LaneDrivingDirection
EgoVehicle: ObjectType
Intersection: LaneSegmentType
Invalid: ObjectType
Negative: LaneDrivingDirection
Normal: LaneSegmentType
OtherVehicle: ObjectType
Pedestrian: ObjectType
Positive: LaneDrivingDirection

class LaneDrivingDirection(Boost.Python.enum):
    Bidirectional: ClassVar[LaneDrivingDirection] = ...
    Negative: ClassVar[LaneDrivingDirection] = ...
    Positive: ClassVar[LaneDrivingDirection] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class LaneSegment(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    drivingDirection: Incomplete
    id: Incomplete
    length: Incomplete
    type: Incomplete
    width: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (LaneSegment)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::world::LaneSegment)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (LaneSegment)arg1, (LaneSegment)other) -> LaneSegment :

            C++ signature :
                ad::rss::world::LaneSegment {lvalue} assign(ad::rss::world::LaneSegment {lvalue},ad::rss::world::LaneSegment)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (LaneSegment)arg1, (LaneSegment)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::world::LaneSegment {lvalue},ad::rss::world::LaneSegment)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (LaneSegment)arg1, (LaneSegment)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::world::LaneSegment {lvalue},ad::rss::world::LaneSegment)"""
    @classmethod
    def __reduce__(cls): ...

class LaneSegmentType(Boost.Python.enum):
    Intersection: ClassVar[LaneSegmentType] = ...
    Normal: ClassVar[LaneSegmentType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class LateralRssAccelerationValues(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    accelMax: Incomplete
    brakeMin: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (LateralRssAccelerationValues)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::world::LateralRssAccelerationValues)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (LateralRssAccelerationValues)arg1, (LateralRssAccelerationValues)other) -> LateralRssAccelerationValues :

            C++ signature :
                ad::rss::world::LateralRssAccelerationValues {lvalue} assign(ad::rss::world::LateralRssAccelerationValues {lvalue},ad::rss::world::LateralRssAccelerationValues)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (LateralRssAccelerationValues)arg1, (LateralRssAccelerationValues)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::world::LateralRssAccelerationValues {lvalue},ad::rss::world::LateralRssAccelerationValues)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (LateralRssAccelerationValues)arg1, (LateralRssAccelerationValues)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::world::LateralRssAccelerationValues {lvalue},ad::rss::world::LateralRssAccelerationValues)"""
    @classmethod
    def __reduce__(cls): ...

class LongitudinalRssAccelerationValues(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    accelMax: Incomplete
    brakeMax: Incomplete
    brakeMin: Incomplete
    brakeMinCorrect: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (LongitudinalRssAccelerationValues)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::world::LongitudinalRssAccelerationValues)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (LongitudinalRssAccelerationValues)arg1, (LongitudinalRssAccelerationValues)other) -> LongitudinalRssAccelerationValues :

            C++ signature :
                ad::rss::world::LongitudinalRssAccelerationValues {lvalue} assign(ad::rss::world::LongitudinalRssAccelerationValues {lvalue},ad::rss::world::LongitudinalRssAccelerationValues)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (LongitudinalRssAccelerationValues)arg1, (LongitudinalRssAccelerationValues)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::world::LongitudinalRssAccelerationValues {lvalue},ad::rss::world::LongitudinalRssAccelerationValues)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (LongitudinalRssAccelerationValues)arg1, (LongitudinalRssAccelerationValues)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::world::LongitudinalRssAccelerationValues {lvalue},ad::rss::world::LongitudinalRssAccelerationValues)"""
    @classmethod
    def __reduce__(cls): ...

class Object(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    objectId: Incomplete
    objectType: Incomplete
    occupiedRegions: Incomplete
    state: Incomplete
    velocity: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Object)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::world::Object)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Object)arg1, (Object)other) -> Object :

            C++ signature :
                ad::rss::world::Object {lvalue} assign(ad::rss::world::Object {lvalue},ad::rss::world::Object)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Object)arg1, (Object)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::world::Object {lvalue},ad::rss::world::Object)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Object)arg1, (Object)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::world::Object {lvalue},ad::rss::world::Object)"""
    @classmethod
    def __reduce__(cls): ...

class ObjectIdVector(Boost.Python.instance):
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
        append( (ObjectIdVector)arg1, (object)arg2) -> None :

            C++ signature :
                void append(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},unsigned long)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ObjectIdVector)arg1, (object)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},unsigned long)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ObjectIdVector)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ObjectIdVector)arg1, (object)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},unsigned long)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ObjectIdVector)arg1, (int)arg2, (object)arg3) -> None :

            C++ signature :
                void insert(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},long,unsigned long)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ObjectIdVector)arg1) -> None :

            C++ signature :
                void reverse(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (ObjectIdVector)arg1) -> None :

            C++ signature :
                void sort(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ObjectIdVector)arg1, (object)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},unsigned long)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ObjectIdVector)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},long)

        __delitem__( (ObjectIdVector)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ObjectIdVector)arg1, (int)arg2) -> int :

            C++ signature :
                unsigned long {lvalue} __getitem__(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},long)

        __getitem__( (ObjectIdVector)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ObjectIdVector)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ObjectIdVector)arg1, (int)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},long,unsigned long)

        __setitem__( (ObjectIdVector)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<unsigned long, std::allocator<unsigned long> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class ObjectState(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    centerPoint: Incomplete
    dimension: Incomplete
    speed: Incomplete
    steeringAngle: Incomplete
    yaw: Incomplete
    yawRate: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (ObjectState)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::world::ObjectState)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ObjectState)arg1, (ObjectState)other) -> ObjectState :

            C++ signature :
                ad::rss::world::ObjectState {lvalue} assign(ad::rss::world::ObjectState {lvalue},ad::rss::world::ObjectState)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ObjectState)arg1, (ObjectState)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::world::ObjectState {lvalue},ad::rss::world::ObjectState)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ObjectState)arg1, (ObjectState)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::world::ObjectState {lvalue},ad::rss::world::ObjectState)"""
    @classmethod
    def __reduce__(cls): ...

class ObjectType(Boost.Python.enum):
    ArtificialObject: ClassVar[ObjectType] = ...
    EgoVehicle: ClassVar[ObjectType] = ...
    Invalid: ClassVar[ObjectType] = ...
    OtherVehicle: ClassVar[ObjectType] = ...
    Pedestrian: ClassVar[ObjectType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class OccupiedRegion(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    latRange: Incomplete
    lonRange: Incomplete
    segmentId: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (OccupiedRegion)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::world::OccupiedRegion)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (OccupiedRegion)arg1, (OccupiedRegion)other) -> OccupiedRegion :

            C++ signature :
                ad::rss::world::OccupiedRegion {lvalue} assign(ad::rss::world::OccupiedRegion {lvalue},ad::rss::world::OccupiedRegion)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (OccupiedRegion)arg1, (OccupiedRegion)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::world::OccupiedRegion {lvalue},ad::rss::world::OccupiedRegion)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (OccupiedRegion)arg1, (OccupiedRegion)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::world::OccupiedRegion {lvalue},ad::rss::world::OccupiedRegion)"""
    @classmethod
    def __reduce__(cls): ...

class OccupiedRegionVector(Boost.Python.instance):
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
        append( (OccupiedRegionVector)arg1, (OccupiedRegion)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},ad::rss::world::OccupiedRegion)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (OccupiedRegionVector)arg1, (OccupiedRegion)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},ad::rss::world::OccupiedRegion)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (OccupiedRegionVector)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (OccupiedRegionVector)arg1, (OccupiedRegion)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},ad::rss::world::OccupiedRegion)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (OccupiedRegionVector)arg1, (int)arg2, (OccupiedRegion)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},long,ad::rss::world::OccupiedRegion)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (OccupiedRegionVector)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (OccupiedRegionVector)arg1, (OccupiedRegion)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},ad::rss::world::OccupiedRegion)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (OccupiedRegionVector)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},long)

        __delitem__( (OccupiedRegionVector)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (OccupiedRegionVector)arg1, (int)arg2) -> OccupiedRegion :

            C++ signature :
                ad::rss::world::OccupiedRegion {lvalue} __getitem__(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},long)

        __getitem__( (OccupiedRegionVector)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (OccupiedRegionVector)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (OccupiedRegionVector)arg1, (int)arg2, (OccupiedRegion)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},long,ad::rss::world::OccupiedRegion)

        __setitem__( (OccupiedRegionVector)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class RoadArea(Boost.Python.instance):
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
        append( (RoadArea)arg1, (RoadSegment)arg2) -> None :

            C++ signature :
                void append(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > > {lvalue},std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (RoadArea)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > > {lvalue},boost::python::api::object)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (RoadArea)arg1, (int)arg2, (RoadSegment)arg3) -> None :

            C++ signature :
                void insert(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > > {lvalue},long,std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (RoadArea)arg1) -> None :

            C++ signature :
                void reverse(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > > {lvalue})"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (RoadArea)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > > {lvalue},long)

        __delitem__( (RoadArea)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (RoadArea)arg1, (int)arg2) -> RoadSegment :

            C++ signature :
                std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue} __getitem__(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > > {lvalue},long)

        __getitem__( (RoadArea)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (RoadArea)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (RoadArea)arg1, (int)arg2, (RoadSegment)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > > {lvalue},long,std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

        __setitem__( (RoadArea)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class RoadSegment(Boost.Python.instance):
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
        append( (RoadSegment)arg1, (LaneSegment)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},ad::rss::world::LaneSegment)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (RoadSegment)arg1, (LaneSegment)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},ad::rss::world::LaneSegment)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (RoadSegment)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (RoadSegment)arg1, (LaneSegment)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},ad::rss::world::LaneSegment)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (RoadSegment)arg1, (int)arg2, (LaneSegment)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},long,ad::rss::world::LaneSegment)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (RoadSegment)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (RoadSegment)arg1, (LaneSegment)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},ad::rss::world::LaneSegment)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (RoadSegment)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},long)

        __delitem__( (RoadSegment)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (RoadSegment)arg1, (int)arg2) -> LaneSegment :

            C++ signature :
                ad::rss::world::LaneSegment {lvalue} __getitem__(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},long)

        __getitem__( (RoadSegment)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (RoadSegment)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (RoadSegment)arg1, (int)arg2, (LaneSegment)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},long,ad::rss::world::LaneSegment)

        __setitem__( (RoadSegment)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class RssDynamics(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    alphaLat: Incomplete
    alphaLon: Incomplete
    lateralFluctuationMargin: Incomplete
    maxSpeedOnAcceleration: Incomplete
    responseTime: Incomplete
    unstructuredSettings: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (RssDynamics)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::world::RssDynamics)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (RssDynamics)arg1, (RssDynamics)other) -> RssDynamics :

            C++ signature :
                ad::rss::world::RssDynamics {lvalue} assign(ad::rss::world::RssDynamics {lvalue},ad::rss::world::RssDynamics)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (RssDynamics)arg1, (RssDynamics)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::world::RssDynamics {lvalue},ad::rss::world::RssDynamics)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (RssDynamics)arg1, (RssDynamics)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::world::RssDynamics {lvalue},ad::rss::world::RssDynamics)"""
    @classmethod
    def __reduce__(cls): ...

class Scene(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    egoVehicle: Incomplete
    egoVehicleRoad: Incomplete
    egoVehicleRssDynamics: Incomplete
    intersectingRoad: Incomplete
    object: Incomplete
    objectRssDynamics: Incomplete
    situationType: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Scene)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::world::Scene)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Scene)arg1, (Scene)other) -> Scene :

            C++ signature :
                ad::rss::world::Scene {lvalue} assign(ad::rss::world::Scene {lvalue},ad::rss::world::Scene)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Scene)arg1, (Scene)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::world::Scene {lvalue},ad::rss::world::Scene)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Scene)arg1, (Scene)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::world::Scene {lvalue},ad::rss::world::Scene)"""
    @classmethod
    def __reduce__(cls): ...

class SceneVector(Boost.Python.instance):
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
        append( (SceneVector)arg1, (Scene)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},ad::rss::world::Scene)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (SceneVector)arg1, (Scene)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},ad::rss::world::Scene)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (SceneVector)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (SceneVector)arg1, (Scene)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},ad::rss::world::Scene)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (SceneVector)arg1, (int)arg2, (Scene)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},long,ad::rss::world::Scene)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (SceneVector)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (SceneVector)arg1, (Scene)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},ad::rss::world::Scene)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (SceneVector)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},long)

        __delitem__( (SceneVector)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (SceneVector)arg1, (int)arg2) -> Scene :

            C++ signature :
                ad::rss::world::Scene {lvalue} __getitem__(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},long)

        __getitem__( (SceneVector)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (SceneVector)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (SceneVector)arg1, (int)arg2, (Scene)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},long,ad::rss::world::Scene)

        __setitem__( (SceneVector)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class UnstructuredSettings(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    driveAwayMaxAngle: Incomplete
    pedestrianBackIntermediateHeadingChangeRatioSteps: Incomplete
    pedestrianBrakeIntermediateAccelerationSteps: Incomplete
    pedestrianContinueForwardIntermediateAccelerationSteps: Incomplete
    pedestrianContinueForwardIntermediateHeadingChangeRatioSteps: Incomplete
    pedestrianFrontIntermediateHeadingChangeRatioSteps: Incomplete
    pedestrianTurningRadius: Incomplete
    vehicleBackIntermediateYawRateChangeRatioSteps: Incomplete
    vehicleBrakeIntermediateAccelerationSteps: Incomplete
    vehicleContinueForwardIntermediateAccelerationSteps: Incomplete
    vehicleContinueForwardIntermediateYawRateChangeRatioSteps: Incomplete
    vehicleFrontIntermediateYawRateChangeRatioSteps: Incomplete
    vehicleMinRadius: Incomplete
    vehicleTrajectoryCalculationStep: Incomplete
    vehicleYawRateChange: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (UnstructuredSettings)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::world::UnstructuredSettings)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (UnstructuredSettings)arg1, (UnstructuredSettings)other) -> UnstructuredSettings :

            C++ signature :
                ad::rss::world::UnstructuredSettings {lvalue} assign(ad::rss::world::UnstructuredSettings {lvalue},ad::rss::world::UnstructuredSettings)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (UnstructuredSettings)arg1, (UnstructuredSettings)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::world::UnstructuredSettings {lvalue},ad::rss::world::UnstructuredSettings)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (UnstructuredSettings)arg1, (UnstructuredSettings)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::world::UnstructuredSettings {lvalue},ad::rss::world::UnstructuredSettings)"""
    @classmethod
    def __reduce__(cls): ...

class Velocity(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    speedLatMax: Incomplete
    speedLatMin: Incomplete
    speedLonMax: Incomplete
    speedLonMin: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Velocity)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::world::Velocity)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Velocity)arg1, (Velocity)other) -> Velocity :

            C++ signature :
                ad::rss::world::Velocity {lvalue} assign(ad::rss::world::Velocity {lvalue},ad::rss::world::Velocity)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Velocity)arg1, (Velocity)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::world::Velocity {lvalue},ad::rss::world::Velocity)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Velocity)arg1, (Velocity)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::world::Velocity {lvalue},ad::rss::world::Velocity)"""
    @classmethod
    def __reduce__(cls): ...

class WorldModel(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    defaultEgoVehicleRssDynamics: Incomplete
    scenes: Incomplete
    timeIndex: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (WorldModel)other) -> None :

            C++ signature :
                void __init__(_object*,ad::rss::world::WorldModel)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (WorldModel)arg1, (WorldModel)other) -> WorldModel :

            C++ signature :
                ad::rss::world::WorldModel {lvalue} assign(ad::rss::world::WorldModel {lvalue},ad::rss::world::WorldModel)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (WorldModel)arg1, (WorldModel)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::rss::world::WorldModel {lvalue},ad::rss::world::WorldModel)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (WorldModel)arg1, (WorldModel)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::rss::world::WorldModel {lvalue},ad::rss::world::WorldModel)"""
    @classmethod
    def __reduce__(cls): ...

def fromString(*args, **kwargs):
    """
    fromString( (str)str) -> LaneDrivingDirection :

        C++ signature :
            ad::rss::world::LaneDrivingDirection fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> LaneSegmentType :

        C++ signature :
            ad::rss::world::LaneSegmentType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> ObjectType :

        C++ signature :
            ad::rss::world::ObjectType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
@overload
def toString(ad) -> Any:
    """
    toString( (LaneDrivingDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::world::LaneDrivingDirection)

    toString( (LaneSegmentType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::world::LaneSegmentType)

    toString( (ObjectType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::world::ObjectType)"""
@overload
def toString(ad) -> Any:
    """
    toString( (LaneDrivingDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::world::LaneDrivingDirection)

    toString( (LaneSegmentType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::world::LaneSegmentType)

    toString( (ObjectType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::world::ObjectType)"""
@overload
def toString(ad) -> Any:
    """
    toString( (LaneDrivingDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::world::LaneDrivingDirection)

    toString( (LaneSegmentType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::world::LaneSegmentType)

    toString( (ObjectType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::rss::world::ObjectType)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (OccupiedRegion)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::OccupiedRegion)

    to_string( (OccupiedRegionVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::OccupiedRegion, std::allocator<ad::rss::world::OccupiedRegion> >)

    to_string( (ObjectIdVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<unsigned long, std::allocator<unsigned long> >)

    to_string( (LongitudinalRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LongitudinalRssAccelerationValues)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Velocity)

    to_string( (LaneDrivingDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneDrivingDirection)

    to_string( (LaneSegmentType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegmentType)

    to_string( (LaneSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LaneSegment)

    to_string( (RoadSegment)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >)

    to_string( (LateralRssAccelerationValues)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::LateralRssAccelerationValues)

    to_string( (UnstructuredSettings)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::UnstructuredSettings)

    to_string( (RssDynamics)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::RssDynamics)

    to_string( (ObjectState)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectState)

    to_string( (ObjectType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::ObjectType)

    to_string( (Object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Object)

    to_string( (RoadArea)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> >, std::allocator<std::vector<ad::rss::world::LaneSegment, std::allocator<ad::rss::world::LaneSegment> > > >)

    to_string( (Scene)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::Scene)

    to_string( (SceneVector)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::rss::world::Scene, std::allocator<ad::rss::world::Scene> >)

    to_string( (WorldModel)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::world::WorldModel)"""
