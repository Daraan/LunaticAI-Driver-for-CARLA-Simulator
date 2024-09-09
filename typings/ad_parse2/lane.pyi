import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

BIDIRECTIONAL: LaneDirection
BIKE: LaneType
CROSSWALK: ContactType
CURB_DOWN: ContactType
CURB_UP: ContactType
EMERGENCY: LaneType
FREE: ContactType
GATE_BARRIER: ContactType
GATE_SPIKES: ContactType
GATE_SPIKES_CONTRA: ContactType
GATE_TOLBOOTH: ContactType
INTERSECTION: LaneType
INVALID: LaneType
LANE_CHANGE: ContactType
LANE_CONTINUATION: ContactType
LANE_END: ContactType
LEFT: ContactLocation
MULTI: LaneType
NEGATIVE: LaneDirection
NONE: LaneDirection
NORMAL: LaneType
OVERLAP: ContactLocation
OVERTAKING: LaneType
PEDESTRIAN: LaneType
POSITIVE: LaneDirection
PREDECESSOR: ContactLocation
PRIO_TO_RIGHT: ContactType
PRIO_TO_RIGHT_AND_STRAIGHT: ContactType
REVERSABLE: LaneDirection
RIGHT: ContactLocation
RIGHT_OF_WAY: ContactType
SHOULDER: LaneType
SINGLE_POINT: ContactType
SPEED_BUMP: ContactType
STOP: ContactType
STOP_ALL: ContactType
SUCCESSOR: ContactLocation
TRAFFIC_LIGHT: ContactType
TURN: LaneType
UNKNOWN: LaneType
YIELD: ContactType

class ContactLane(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    location: Incomplete
    restrictions: Incomplete
    toLane: Incomplete
    trafficLightId: Incomplete
    types: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (ContactLane)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::lane::ContactLane)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ContactLane)arg1, (ContactLane)other) -> ContactLane :

            C++ signature :
                ad::map::lane::ContactLane {lvalue} assign(ad::map::lane::ContactLane {lvalue},ad::map::lane::ContactLane)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ContactLane)arg1, (ContactLane)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::lane::ContactLane {lvalue},ad::map::lane::ContactLane)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ContactLane)arg1, (ContactLane)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::lane::ContactLane {lvalue},ad::map::lane::ContactLane)"""
    @classmethod
    def __reduce__(cls): ...

class ContactLaneList(Boost.Python.instance):
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
        append( (ContactLaneList)arg1, (ContactLane)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},ad::map::lane::ContactLane)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ContactLaneList)arg1, (ContactLane)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},ad::map::lane::ContactLane)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ContactLaneList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ContactLaneList)arg1, (ContactLane)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},ad::map::lane::ContactLane)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ContactLaneList)arg1, (int)arg2, (ContactLane)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},long,ad::map::lane::ContactLane)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ContactLaneList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ContactLaneList)arg1, (ContactLane)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},ad::map::lane::ContactLane)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ContactLaneList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},long)

        __delitem__( (ContactLaneList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ContactLaneList)arg1, (int)arg2) -> ContactLane :

            C++ signature :
                ad::map::lane::ContactLane {lvalue} __getitem__(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},long)

        __getitem__( (ContactLaneList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ContactLaneList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ContactLaneList)arg1, (int)arg2, (ContactLane)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},long,ad::map::lane::ContactLane)

        __setitem__( (ContactLaneList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class ContactLocation(Boost.Python.enum):
    INVALID: ClassVar[ContactLocation] = ...
    LEFT: ClassVar[ContactLocation] = ...
    OVERLAP: ClassVar[ContactLocation] = ...
    PREDECESSOR: ClassVar[ContactLocation] = ...
    RIGHT: ClassVar[ContactLocation] = ...
    SUCCESSOR: ClassVar[ContactLocation] = ...
    UNKNOWN: ClassVar[ContactLocation] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class ContactLocationList(Boost.Python.instance):
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
        append( (ContactLocationList)arg1, (ContactLocation)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},ad::map::lane::ContactLocation)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ContactLocationList)arg1, (ContactLocation)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},ad::map::lane::ContactLocation)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ContactLocationList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ContactLocationList)arg1, (ContactLocation)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},ad::map::lane::ContactLocation)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ContactLocationList)arg1, (int)arg2, (ContactLocation)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},long,ad::map::lane::ContactLocation)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ContactLocationList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (ContactLocationList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ContactLocationList)arg1, (ContactLocation)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},ad::map::lane::ContactLocation)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ContactLocationList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},long)

        __delitem__( (ContactLocationList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ContactLocationList)arg1, (int)arg2) -> ContactLocation :

            C++ signature :
                ad::map::lane::ContactLocation {lvalue} __getitem__(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},long)

        __getitem__( (ContactLocationList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ContactLocationList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ContactLocationList)arg1, (int)arg2, (ContactLocation)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},long,ad::map::lane::ContactLocation)

        __setitem__( (ContactLocationList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class ContactType(Boost.Python.enum):
    CROSSWALK: ClassVar[ContactType] = ...
    CURB_DOWN: ClassVar[ContactType] = ...
    CURB_UP: ClassVar[ContactType] = ...
    FREE: ClassVar[ContactType] = ...
    GATE_BARRIER: ClassVar[ContactType] = ...
    GATE_SPIKES: ClassVar[ContactType] = ...
    GATE_SPIKES_CONTRA: ClassVar[ContactType] = ...
    GATE_TOLBOOTH: ClassVar[ContactType] = ...
    INVALID: ClassVar[ContactType] = ...
    LANE_CHANGE: ClassVar[ContactType] = ...
    LANE_CONTINUATION: ClassVar[ContactType] = ...
    LANE_END: ClassVar[ContactType] = ...
    PRIO_TO_RIGHT: ClassVar[ContactType] = ...
    PRIO_TO_RIGHT_AND_STRAIGHT: ClassVar[ContactType] = ...
    RIGHT_OF_WAY: ClassVar[ContactType] = ...
    SINGLE_POINT: ClassVar[ContactType] = ...
    SPEED_BUMP: ClassVar[ContactType] = ...
    STOP: ClassVar[ContactType] = ...
    STOP_ALL: ClassVar[ContactType] = ...
    TRAFFIC_LIGHT: ClassVar[ContactType] = ...
    UNKNOWN: ClassVar[ContactType] = ...
    YIELD: ClassVar[ContactType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class ContactTypeList(Boost.Python.instance):
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
        append( (ContactTypeList)arg1, (ContactType)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},ad::map::lane::ContactType)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ContactTypeList)arg1, (ContactType)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},ad::map::lane::ContactType)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ContactTypeList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ContactTypeList)arg1, (ContactType)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},ad::map::lane::ContactType)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ContactTypeList)arg1, (int)arg2, (ContactType)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},long,ad::map::lane::ContactType)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ContactTypeList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (ContactTypeList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ContactTypeList)arg1, (ContactType)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},ad::map::lane::ContactType)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ContactTypeList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},long)

        __delitem__( (ContactTypeList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ContactTypeList)arg1, (int)arg2) -> ContactType :

            C++ signature :
                ad::map::lane::ContactType {lvalue} __getitem__(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},long)

        __getitem__( (ContactTypeList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ContactTypeList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ContactTypeList)arg1, (int)arg2, (ContactType)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},long,ad::map::lane::ContactType)

        __setitem__( (ContactTypeList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class ECEFBorder(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    left: Incomplete
    right: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (ECEFBorder)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::lane::ECEFBorder)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ECEFBorder)arg1, (ECEFBorder)other) -> ECEFBorder :

            C++ signature :
                ad::map::lane::ECEFBorder {lvalue} assign(ad::map::lane::ECEFBorder {lvalue},ad::map::lane::ECEFBorder)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ECEFBorder)arg1, (ECEFBorder)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::lane::ECEFBorder {lvalue},ad::map::lane::ECEFBorder)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ECEFBorder)arg1, (ECEFBorder)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::lane::ECEFBorder {lvalue},ad::map::lane::ECEFBorder)"""
    @classmethod
    def __reduce__(cls): ...

class ECEFBorderList(Boost.Python.instance):
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
        append( (ECEFBorderList)arg1, (ECEFBorder)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},ad::map::lane::ECEFBorder)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ECEFBorderList)arg1, (ECEFBorder)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},ad::map::lane::ECEFBorder)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ECEFBorderList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ECEFBorderList)arg1, (ECEFBorder)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},ad::map::lane::ECEFBorder)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ECEFBorderList)arg1, (int)arg2, (ECEFBorder)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},long,ad::map::lane::ECEFBorder)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ECEFBorderList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ECEFBorderList)arg1, (ECEFBorder)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},ad::map::lane::ECEFBorder)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ECEFBorderList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},long)

        __delitem__( (ECEFBorderList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ECEFBorderList)arg1, (int)arg2) -> ECEFBorder :

            C++ signature :
                ad::map::lane::ECEFBorder {lvalue} __getitem__(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},long)

        __getitem__( (ECEFBorderList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ECEFBorderList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ECEFBorderList)arg1, (int)arg2, (ECEFBorder)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},long,ad::map::lane::ECEFBorder)

        __setitem__( (ECEFBorderList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class ENUBorder(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    left: Incomplete
    right: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (ENUBorder)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::lane::ENUBorder)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ENUBorder)arg1, (ENUBorder)other) -> ENUBorder :

            C++ signature :
                ad::map::lane::ENUBorder {lvalue} assign(ad::map::lane::ENUBorder {lvalue},ad::map::lane::ENUBorder)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ENUBorder)arg1, (ENUBorder)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::lane::ENUBorder {lvalue},ad::map::lane::ENUBorder)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ENUBorder)arg1, (ENUBorder)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::lane::ENUBorder {lvalue},ad::map::lane::ENUBorder)"""
    @classmethod
    def __reduce__(cls): ...

class ENUBorderList(Boost.Python.instance):
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
        append( (ENUBorderList)arg1, (ENUBorder)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},ad::map::lane::ENUBorder)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ENUBorderList)arg1, (ENUBorder)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},ad::map::lane::ENUBorder)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ENUBorderList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ENUBorderList)arg1, (ENUBorder)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},ad::map::lane::ENUBorder)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ENUBorderList)arg1, (int)arg2, (ENUBorder)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},long,ad::map::lane::ENUBorder)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ENUBorderList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ENUBorderList)arg1, (ENUBorder)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},ad::map::lane::ENUBorder)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ENUBorderList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},long)

        __delitem__( (ENUBorderList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ENUBorderList)arg1, (int)arg2) -> ENUBorder :

            C++ signature :
                ad::map::lane::ENUBorder {lvalue} __getitem__(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},long)

        __getitem__( (ENUBorderList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ENUBorderList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ENUBorderList)arg1, (int)arg2, (ENUBorder)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},long,ad::map::lane::ENUBorder)

        __setitem__( (ENUBorderList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class GeoBorder(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    left: Incomplete
    right: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (GeoBorder)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::lane::GeoBorder)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (GeoBorder)arg1, (GeoBorder)other) -> GeoBorder :

            C++ signature :
                ad::map::lane::GeoBorder {lvalue} assign(ad::map::lane::GeoBorder {lvalue},ad::map::lane::GeoBorder)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (GeoBorder)arg1, (GeoBorder)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::lane::GeoBorder {lvalue},ad::map::lane::GeoBorder)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (GeoBorder)arg1, (GeoBorder)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::lane::GeoBorder {lvalue},ad::map::lane::GeoBorder)"""
    @classmethod
    def __reduce__(cls): ...

class GeoBorderList(Boost.Python.instance):
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
        append( (GeoBorderList)arg1, (GeoBorder)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},ad::map::lane::GeoBorder)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (GeoBorderList)arg1, (GeoBorder)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},ad::map::lane::GeoBorder)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (GeoBorderList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (GeoBorderList)arg1, (GeoBorder)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},ad::map::lane::GeoBorder)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (GeoBorderList)arg1, (int)arg2, (GeoBorder)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},long,ad::map::lane::GeoBorder)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (GeoBorderList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (GeoBorderList)arg1, (GeoBorder)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},ad::map::lane::GeoBorder)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (GeoBorderList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},long)

        __delitem__( (GeoBorderList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (GeoBorderList)arg1, (int)arg2) -> GeoBorder :

            C++ signature :
                ad::map::lane::GeoBorder {lvalue} __getitem__(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},long)

        __getitem__( (GeoBorderList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (GeoBorderList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (GeoBorderList)arg1, (int)arg2, (GeoBorder)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},long,ad::map::lane::GeoBorder)

        __setitem__( (GeoBorderList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Lane(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    boundingSphere: Incomplete
    complianceVersion: Incomplete
    contactLanes: Incomplete
    direction: Incomplete
    edgeLeft: Incomplete
    edgeRight: Incomplete
    id: Incomplete
    length: Incomplete
    lengthRange: Incomplete
    restrictions: Incomplete
    speedLimits: Incomplete
    type: Incomplete
    visibleLandmarks: Incomplete
    width: Incomplete
    widthRange: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Lane)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::lane::Lane)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Lane)arg1, (Lane)other) -> Lane :

            C++ signature :
                ad::map::lane::Lane {lvalue} assign(ad::map::lane::Lane {lvalue},ad::map::lane::Lane)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Lane)arg1, (Lane)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::lane::Lane {lvalue},ad::map::lane::Lane)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Lane)arg1, (Lane)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::lane::Lane {lvalue},ad::map::lane::Lane)"""
    @classmethod
    def __reduce__(cls): ...

class LaneAltitudeRange(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    maximum: Incomplete
    minimum: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def __reduce__(cls): ...

class LaneDirection(Boost.Python.enum):
    BIDIRECTIONAL: ClassVar[LaneDirection] = ...
    INVALID: ClassVar[LaneDirection] = ...
    NEGATIVE: ClassVar[LaneDirection] = ...
    NONE: ClassVar[LaneDirection] = ...
    POSITIVE: ClassVar[LaneDirection] = ...
    REVERSABLE: ClassVar[LaneDirection] = ...
    UNKNOWN: ClassVar[LaneDirection] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class LaneId(Boost.Python.instance):
    cMaxValue: ClassVar[int] = ...  # read-only
    cMinValue: ClassVar[int] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iLaneId) -> None :

            C++ signature :
                void __init__(_object*,unsigned long)

        __init__( (object)arg1, (LaneId)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::lane::LaneId)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (LaneId)arg1, (LaneId)other) -> LaneId :

            C++ signature :
                ad::map::lane::LaneId {lvalue} assign(ad::map::lane::LaneId {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (LaneId)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::lane::LaneId {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (LaneId)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::lane::LaneId {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> LaneId :

            C++ signature :
                ad::map::lane::LaneId getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> LaneId :

            C++ signature :
                ad::map::lane::LaneId getMin()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (LaneId)arg1, (LaneId)arg2) -> object :

            C++ signature :
                _object* __add__(ad::map::lane::LaneId {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (LaneId)arg1, (LaneId)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::lane::LaneId {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (LaneId)arg1, (LaneId)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::map::lane::LaneId {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (LaneId)arg1, (LaneId)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::map::lane::LaneId {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (LaneId)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::map::lane::LaneId&>,ad::map::lane::LaneId)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (LaneId)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::map::lane::LaneId&>,ad::map::lane::LaneId)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (LaneId)arg1, (LaneId)arg2) -> object :

            C++ signature :
                _object* __le__(ad::map::lane::LaneId {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __long__(cls, ad) -> Any:
        """
        __long__( (LaneId)arg1) -> int :

            C++ signature :
                unsigned long __long__(ad::map::lane::LaneId {lvalue})"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (LaneId)arg1, (LaneId)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::map::lane::LaneId {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (LaneId)arg1, (LaneId)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::lane::LaneId {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (LaneId)arg1, (LaneId)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::map::lane::LaneId {lvalue},ad::map::lane::LaneId)"""
    @property
    def Valid(self): ...

class LaneIdList(Boost.Python.instance):
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
        append( (LaneIdList)arg1, (LaneId)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (LaneIdList)arg1, (LaneId)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (LaneIdList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (LaneIdList)arg1, (LaneId)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (LaneIdList)arg1, (int)arg2, (LaneId)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},long,ad::map::lane::LaneId)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (LaneIdList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (LaneIdList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (LaneIdList)arg1, (LaneId)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (LaneIdList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},long)

        __delitem__( (LaneIdList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (LaneIdList)arg1, (int)arg2) -> LaneId :

            C++ signature :
                ad::map::lane::LaneId {lvalue} __getitem__(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},long)

        __getitem__( (LaneIdList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (LaneIdList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (LaneIdList)arg1, (int)arg2, (LaneId)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},long,ad::map::lane::LaneId)

        __setitem__( (LaneIdList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class LaneIdSet(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def add(cls, *args, **kwargs):
        """
        add( (LaneIdSet)arg1, (LaneId)arg2) -> None :

            C++ signature :
                void add(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> > {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (LaneIdSet)arg1, (LaneId)arg2) -> int :

            C++ signature :
                unsigned long count(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> > {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def has_key(cls, *args, **kwargs):
        """
        has_key( (LaneIdSet)arg1, (LaneId)arg2) -> bool :

            C++ signature :
                bool has_key(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> > {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (LaneIdSet)arg1, (LaneId)arg2) -> None :

            C++ signature :
                void insert(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> > {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (LaneIdSet)arg1, (LaneId)arg2) -> bool :

            C++ signature :
                bool __contains__(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> > {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (LaneIdSet)arg1, (LaneId)arg2) -> None :

            C++ signature :
                void __delitem__(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> > {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (LaneIdSet)arg1, (LaneId)arg2) -> LaneId :

            C++ signature :
                ad::map::lane::LaneId __getitem__(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> > {lvalue},ad::map::lane::LaneId)"""
    @classmethod
    def __iter__(cls):
        """
        __iter__( (object)arg1) -> object :

            C++ signature :
                boost::python::objects::iterator_range<boost::python::return_value_policy<boost::python::return_by_value, boost::python::default_call_policies>, std::_Rb_tree_const_iterator<ad::map::lane::LaneId> > __iter__(boost::python::back_reference<std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >&>)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (LaneIdSet)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...

class LaneType(Boost.Python.enum):
    BIKE: ClassVar[LaneType] = ...
    EMERGENCY: ClassVar[LaneType] = ...
    INTERSECTION: ClassVar[LaneType] = ...
    INVALID: ClassVar[LaneType] = ...
    MULTI: ClassVar[LaneType] = ...
    NORMAL: ClassVar[LaneType] = ...
    OVERTAKING: ClassVar[LaneType] = ...
    PEDESTRIAN: ClassVar[LaneType] = ...
    SHOULDER: ClassVar[LaneType] = ...
    TURN: ClassVar[LaneType] = ...
    UNKNOWN: ClassVar[LaneType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class numeric_limits_less__ad_scope_map_scope_lane_scope_LaneId__greater_(Boost.Python.instance):
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
        epsilon() -> LaneId :

            C++ signature :
                ad::map::lane::LaneId epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> LaneId :

            C++ signature :
                ad::map::lane::LaneId lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> LaneId :

            C++ signature :
                ad::map::lane::LaneId max()"""
    @classmethod
    def __reduce__(cls): ...

def calcLaneAltitudeRange(ad) -> Any:
    """
    calcLaneAltitudeRange( (Lane)lane) -> LaneAltitudeRange :

        C++ signature :
            ad::map::lane::LaneAltitudeRange calcLaneAltitudeRange(ad::map::lane::Lane)"""
@overload
def calcLength(ad) -> Any:
    """
    calcLength( (LaneId)laneId) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::LaneId)

    calcLength( (LaneOccupiedRegion)laneOccupiedRegion) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::match::LaneOccupiedRegion)

    calcLength( (ENUBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::ENUBorder)

    calcLength( (ECEFBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::ECEFBorder)

    calcLength( (GeoBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::GeoBorder)

    calcLength( (ENUBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    calcLength( (ECEFBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    calcLength( (GeoBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)"""
@overload
def calcLength(ad) -> Any:
    """
    calcLength( (LaneId)laneId) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::LaneId)

    calcLength( (LaneOccupiedRegion)laneOccupiedRegion) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::match::LaneOccupiedRegion)

    calcLength( (ENUBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::ENUBorder)

    calcLength( (ECEFBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::ECEFBorder)

    calcLength( (GeoBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::GeoBorder)

    calcLength( (ENUBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    calcLength( (ECEFBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    calcLength( (GeoBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)"""
@overload
def calcLength(ad) -> Any:
    """
    calcLength( (LaneId)laneId) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::LaneId)

    calcLength( (LaneOccupiedRegion)laneOccupiedRegion) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::match::LaneOccupiedRegion)

    calcLength( (ENUBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::ENUBorder)

    calcLength( (ECEFBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::ECEFBorder)

    calcLength( (GeoBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::GeoBorder)

    calcLength( (ENUBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    calcLength( (ECEFBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    calcLength( (GeoBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)"""
@overload
def calcLength(ad) -> Any:
    """
    calcLength( (LaneId)laneId) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::LaneId)

    calcLength( (LaneOccupiedRegion)laneOccupiedRegion) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::match::LaneOccupiedRegion)

    calcLength( (ENUBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::ENUBorder)

    calcLength( (ECEFBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::ECEFBorder)

    calcLength( (GeoBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::GeoBorder)

    calcLength( (ENUBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    calcLength( (ECEFBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    calcLength( (GeoBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)"""
@overload
def calcLength(ad) -> Any:
    """
    calcLength( (LaneId)laneId) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::LaneId)

    calcLength( (LaneOccupiedRegion)laneOccupiedRegion) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::match::LaneOccupiedRegion)

    calcLength( (ENUBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::ENUBorder)

    calcLength( (ECEFBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::ECEFBorder)

    calcLength( (GeoBorder)border) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(ad::map::lane::GeoBorder)

    calcLength( (ENUBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    calcLength( (ECEFBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    calcLength( (GeoBorderList)borderList) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)"""
@overload
def calcWidth(ad) -> Any:
    """
    calcWidth( (ParaPoint)paraPoint) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::point::ParaPoint)

    calcWidth( (LaneId)laneId, (ParametricValue)longOffset) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::lane::LaneId,ad::physics::ParametricValue)

    calcWidth( (ENUPoint)enuPoint) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::point::ENUPoint)

    calcWidth( (LaneOccupiedRegion)laneOccupiedRegion) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::match::LaneOccupiedRegion)"""
@overload
def calcWidth(ad) -> Any:
    """
    calcWidth( (ParaPoint)paraPoint) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::point::ParaPoint)

    calcWidth( (LaneId)laneId, (ParametricValue)longOffset) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::lane::LaneId,ad::physics::ParametricValue)

    calcWidth( (ENUPoint)enuPoint) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::point::ENUPoint)

    calcWidth( (LaneOccupiedRegion)laneOccupiedRegion) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::match::LaneOccupiedRegion)"""
@overload
def calcWidth(ad) -> Any:
    """
    calcWidth( (ParaPoint)paraPoint) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::point::ParaPoint)

    calcWidth( (LaneId)laneId, (ParametricValue)longOffset) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::lane::LaneId,ad::physics::ParametricValue)

    calcWidth( (ENUPoint)enuPoint) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::point::ENUPoint)

    calcWidth( (LaneOccupiedRegion)laneOccupiedRegion) -> Distance :

        C++ signature :
            ad::physics::Distance calcWidth(ad::map::match::LaneOccupiedRegion)"""
def findNearestPointOnLane(*args, **kwargs):
    """
    findNearestPointOnLane( (Lane)lane, (ECEFPoint)pt, (MapMatchedPosition)mmpos) -> bool :

        C++ signature :
            bool findNearestPointOnLane(ad::map::lane::Lane,ad::map::point::ECEFPoint,ad::map::match::MapMatchedPosition {lvalue})"""
def findNearestPointOnLaneInterval(*args, **kwargs):
    """
    findNearestPointOnLaneInterval( (LaneInterval)laneInterval, (ECEFPoint)pt, (MapMatchedPosition)mmpos) -> bool :

        C++ signature :
            bool findNearestPointOnLaneInterval(ad::map::route::LaneInterval,ad::map::point::ECEFPoint,ad::map::match::MapMatchedPosition {lvalue})"""
def fromString(*args, **kwargs):
    """
    fromString( (str)str) -> ContactLocation :

        C++ signature :
            ad::map::lane::ContactLocation fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> LaneType :

        C++ signature :
            ad::map::lane::LaneType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> ContactType :

        C++ signature :
            ad::map::lane::ContactType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> LaneDirection :

        C++ signature :
            ad::map::lane::LaneDirection fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
def getContactLanes(*args, **kwargs):
    """
    getContactLanes( (Lane)lane, (ContactLocation)location) -> ContactLaneList :

        C++ signature :
            std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > getContactLanes(ad::map::lane::Lane,ad::map::lane::ContactLocation)

    getContactLanes( (Lane)lane, (ContactLocationList)locations) -> ContactLaneList :

        C++ signature :
            std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> > getContactLanes(ad::map::lane::Lane,std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> >)"""
def getContactLocation(*args, **kwargs):
    """
    getContactLocation( (Lane)lane, (LaneId)to_lane_id) -> ContactLocation :

        C++ signature :
            ad::map::lane::ContactLocation getContactLocation(ad::map::lane::Lane,ad::map::lane::LaneId)"""
def getDirectNeighborhoodRelation(*args, **kwargs):
    """
    getDirectNeighborhoodRelation( (LaneId)laneId, (LaneId)checkLaneId) -> ContactLocation :

        C++ signature :
            ad::map::lane::ContactLocation getDirectNeighborhoodRelation(ad::map::lane::LaneId,ad::map::lane::LaneId)"""
def getDistanceEnuPointToLateralAlignmentEdge(*args, **kwargs):
    """
    getDistanceEnuPointToLateralAlignmentEdge( (ENUPoint)enuPoint, (ENUEdge)lateralAlignmentEdge) -> Distance :

        C++ signature :
            ad::physics::Distance getDistanceEnuPointToLateralAlignmentEdge(ad::map::point::ENUPoint,std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)"""
def getDistanceToLane(*args, **kwargs):
    """
    getDistanceToLane( (LaneId)laneId, (Object)object) -> Distance :

        C++ signature :
            ad::physics::Distance getDistanceToLane(ad::map::lane::LaneId,ad::map::match::Object)"""
def getDuration(*args, **kwargs):
    """
    getDuration( (Lane)lane, (ParametricRange)range) -> Duration :

        C++ signature :
            ad::physics::Duration getDuration(ad::map::lane::Lane,ad::physics::ParametricRange)"""
def getENUHeading(*args, **kwargs):
    """
    getENUHeading( (ENUBorderList)borderList, (ENUPoint)enuPoint) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading getENUHeading(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >,ad::map::point::ENUPoint)"""
def getENULanePoint(ad) -> Any:
    """
    getENULanePoint( (ParaPoint)parametricPoint [, (ParametricValue)lateralOffset=<physics.ParametricValue object at 0x7752c8de28f0>]) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint getENULanePoint(ad::map::point::ParaPoint [,ad::physics::ParametricValue=<physics.ParametricValue object at 0x7752c8de28f0>])"""
def getEndPoint(ad) -> Any:
    """
    getEndPoint( (Lane)lane) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint getEndPoint(ad::map::lane::Lane)"""
def getHOV(ad) -> Any:
    """
    getHOV( (Lane)lane) -> int :

        C++ signature :
            unsigned short getHOV(ad::map::lane::Lane)"""
def getLane(ad) -> Any:
    """
    getLane( (LaneId)id) -> Lane :

        C++ signature :
            ad::map::lane::Lane getLane(ad::map::lane::LaneId)"""
@overload
def getLaneECEFHeading(ad) -> Any:
    """
    getLaneECEFHeading( (MapMatchedPosition)mapMatchedPosition) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading getLaneECEFHeading(ad::map::match::MapMatchedPosition)

    getLaneECEFHeading( (ParaPoint)paraPoint) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading getLaneECEFHeading(ad::map::point::ParaPoint)"""
@overload
def getLaneECEFHeading(ad) -> Any:
    """
    getLaneECEFHeading( (MapMatchedPosition)mapMatchedPosition) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading getLaneECEFHeading(ad::map::match::MapMatchedPosition)

    getLaneECEFHeading( (ParaPoint)paraPoint) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading getLaneECEFHeading(ad::map::point::ParaPoint)"""
@overload
def getLaneENUHeading(ad) -> Any:
    """
    getLaneENUHeading( (MapMatchedPosition)mapMatchedPosition) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading getLaneENUHeading(ad::map::match::MapMatchedPosition)

    getLaneENUHeading( (ParaPoint)paraPoint, (GeoPoint)gnssReference) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading getLaneENUHeading(ad::map::point::ParaPoint,ad::map::point::GeoPoint)

    getLaneENUHeading( (ParaPoint)position) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading getLaneENUHeading(ad::map::point::ParaPoint)"""
@overload
def getLaneENUHeading(ad) -> Any:
    """
    getLaneENUHeading( (MapMatchedPosition)mapMatchedPosition) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading getLaneENUHeading(ad::map::match::MapMatchedPosition)

    getLaneENUHeading( (ParaPoint)paraPoint, (GeoPoint)gnssReference) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading getLaneENUHeading(ad::map::point::ParaPoint,ad::map::point::GeoPoint)

    getLaneENUHeading( (ParaPoint)position) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading getLaneENUHeading(ad::map::point::ParaPoint)"""
def getLanePtr(ad) -> Any:
    """
    getLanePtr( (LaneId)id) -> Lane :

        C++ signature :
            std::shared_ptr<ad::map::lane::Lane const> getLanePtr(ad::map::lane::LaneId)"""
def getLanes() -> Any:
    """
    getLanes() -> LaneIdList :

        C++ signature :
            std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> > getLanes()"""
def getLateralAlignmentEdge(*args, **kwargs):
    """
    getLateralAlignmentEdge( (ENUBorder)border, (ParametricValue)lateralAlignment) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > getLateralAlignmentEdge(ad::map::lane::ENUBorder,ad::physics::ParametricValue)"""
def getMaxSpeed(*args, **kwargs):
    """
    getMaxSpeed( (Lane)lane, (ParametricRange)range) -> Speed :

        C++ signature :
            ad::physics::Speed getMaxSpeed(ad::map::lane::Lane,ad::physics::ParametricRange)"""
def getParametricPoint(*args, **kwargs):
    """
    getParametricPoint( (Lane)lane, (ParametricValue)longitudinalOffset, (ParametricValue)lateralOffset) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint getParametricPoint(ad::map::lane::Lane,ad::physics::ParametricValue,ad::physics::ParametricValue)"""
def getProjectedParametricPoint(*args, **kwargs):
    """
    getProjectedParametricPoint( (Lane)lane, (ParametricValue)longitudinalOffset, (ParametricValue)lateralOffset) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint getProjectedParametricPoint(ad::map::lane::Lane,ad::physics::ParametricValue,ad::physics::ParametricValue)"""
def getSpeedLimits(*args, **kwargs):
    """
    getSpeedLimits( (Lane)lane, (ParametricRange)range) -> SpeedLimitList :

        C++ signature :
            std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > getSpeedLimits(ad::map::lane::Lane,ad::physics::ParametricRange)"""
def getStartPoint(ad) -> Any:
    """
    getStartPoint( (Lane)lane) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint getStartPoint(ad::map::lane::Lane)"""
def getWidth(*args, **kwargs):
    """
    getWidth( (Lane)lane, (ParametricValue)longitudinalOffset) -> Distance :

        C++ signature :
            ad::physics::Distance getWidth(ad::map::lane::Lane,ad::physics::ParametricValue)"""
def isAccessOk(*args, **kwargs):
    """
    isAccessOk( (Lane)lane, (VehicleDescriptor)vehicle) -> bool :

        C++ signature :
            bool isAccessOk(ad::map::lane::Lane,ad::map::restriction::VehicleDescriptor)

    isAccessOk( (ContactLane)contactLane, (VehicleDescriptor)vehicle) -> bool :

        C++ signature :
            bool isAccessOk(ad::map::lane::ContactLane,ad::map::restriction::VehicleDescriptor)"""
def isHeadingInLaneDirection(*args, **kwargs):
    """
    isHeadingInLaneDirection( (ParaPoint)position, (ENUHeading)heading) -> bool :

        C++ signature :
            bool isHeadingInLaneDirection(ad::map::point::ParaPoint,ad::map::point::ENUHeading)"""
@overload
def isLaneDirectionNegative(ad) -> Any:
    """
    isLaneDirectionNegative( (Lane)lane) -> bool :

        C++ signature :
            bool isLaneDirectionNegative(ad::map::lane::Lane)

    isLaneDirectionNegative( (LaneId)laneId) -> bool :

        C++ signature :
            bool isLaneDirectionNegative(ad::map::lane::LaneId)"""
@overload
def isLaneDirectionNegative(ad) -> Any:
    """
    isLaneDirectionNegative( (Lane)lane) -> bool :

        C++ signature :
            bool isLaneDirectionNegative(ad::map::lane::Lane)

    isLaneDirectionNegative( (LaneId)laneId) -> bool :

        C++ signature :
            bool isLaneDirectionNegative(ad::map::lane::LaneId)"""
@overload
def isLaneDirectionPositive(ad) -> Any:
    """
    isLaneDirectionPositive( (Lane)lane) -> bool :

        C++ signature :
            bool isLaneDirectionPositive(ad::map::lane::Lane)

    isLaneDirectionPositive( (LaneId)laneId) -> bool :

        C++ signature :
            bool isLaneDirectionPositive(ad::map::lane::LaneId)"""
@overload
def isLaneDirectionPositive(ad) -> Any:
    """
    isLaneDirectionPositive( (Lane)lane) -> bool :

        C++ signature :
            bool isLaneDirectionPositive(ad::map::lane::Lane)

    isLaneDirectionPositive( (LaneId)laneId) -> bool :

        C++ signature :
            bool isLaneDirectionPositive(ad::map::lane::LaneId)"""
def isLanePartOfAnIntersection(ad) -> Any:
    """
    isLanePartOfAnIntersection( (Lane)lane) -> bool :

        C++ signature :
            bool isLanePartOfAnIntersection(ad::map::lane::Lane)"""
def isLaneRelevantForExpansion(*args, **kwargs):
    """
    isLaneRelevantForExpansion( (LaneId)laneId, (LaneIdSet)relevantLanes) -> bool :

        C++ signature :
            bool isLaneRelevantForExpansion(ad::map::lane::LaneId,std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
def isLeftMost(ad) -> Any:
    """
    isLeftMost( (Lane)lane) -> bool :

        C++ signature :
            bool isLeftMost(ad::map::lane::Lane)"""
def isNear(*args, **kwargs):
    """
    isNear( (Lane)lane, (BoundingSphere)boundingSphere) -> bool :

        C++ signature :
            bool isNear(ad::map::lane::Lane,ad::map::point::BoundingSphere)"""
def isPhysicalPredecessor(*args, **kwargs):
    """
    isPhysicalPredecessor( (Lane)lane, (Lane)other) -> bool :

        C++ signature :
            bool isPhysicalPredecessor(ad::map::lane::Lane,ad::map::lane::Lane)"""
def isPyhsicalSuccessor(*args, **kwargs):
    """
    isPyhsicalSuccessor( (Lane)lane, (Lane)other) -> bool :

        C++ signature :
            bool isPyhsicalSuccessor(ad::map::lane::Lane,ad::map::lane::Lane)"""
def isRightMost(ad) -> Any:
    """
    isRightMost( (Lane)lane) -> bool :

        C++ signature :
            bool isRightMost(ad::map::lane::Lane)"""
def isRouteable(ad) -> Any:
    """
    isRouteable( (Lane)lane) -> bool :

        C++ signature :
            bool isRouteable(ad::map::lane::Lane)"""
def isSameOrDirectNeighbor(*args, **kwargs):
    """
    isSameOrDirectNeighbor( (LaneId)id, (LaneId)neighbor) -> bool :

        C++ signature :
            bool isSameOrDirectNeighbor(ad::map::lane::LaneId,ad::map::lane::LaneId)"""
def isSuccessorOrPredecessor(*args, **kwargs):
    """
    isSuccessorOrPredecessor( (LaneId)laneId, (LaneId)checkLaneId) -> bool :

        C++ signature :
            bool isSuccessorOrPredecessor(ad::map::lane::LaneId,ad::map::lane::LaneId)"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (LaneId)laneId [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::lane::LaneId [,bool=True])

    isValid( (Lane)lane [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::lane::Lane [,bool=True])

    isValid( (ContactLane)contactLane [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::lane::ContactLane [,bool=True])"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (LaneId)laneId [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::lane::LaneId [,bool=True])

    isValid( (Lane)lane [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::lane::Lane [,bool=True])

    isValid( (ContactLane)contactLane [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::lane::ContactLane [,bool=True])"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (LaneId)laneId [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::lane::LaneId [,bool=True])

    isValid( (Lane)lane [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::lane::Lane [,bool=True])

    isValid( (ContactLane)contactLane [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::lane::ContactLane [,bool=True])"""
def isVanishingLaneEnd(ad) -> Any:
    """
    isVanishingLaneEnd( (Lane)lane) -> bool :

        C++ signature :
            bool isVanishingLaneEnd(ad::map::lane::Lane)"""
def isVanishingLaneStart(ad) -> Any:
    """
    isVanishingLaneStart( (Lane)lane) -> bool :

        C++ signature :
            bool isVanishingLaneStart(ad::map::lane::Lane)"""
def makeTransitionFromFirstBorderContinuous(*args, **kwargs):
    """
    makeTransitionFromFirstBorderContinuous( (ENUBorder)first, (ENUBorder)second) -> None :

        C++ signature :
            void makeTransitionFromFirstBorderContinuous(ad::map::lane::ENUBorder {lvalue},ad::map::lane::ENUBorder)"""
def makeTransitionFromFirstEdgeContinuous(*args, **kwargs):
    """
    makeTransitionFromFirstEdgeContinuous( (ENUEdge)first, (ENUEdge)second) -> None :

        C++ signature :
            void makeTransitionFromFirstEdgeContinuous(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)"""
def makeTransitionToSecondBorderContinuous(*args, **kwargs):
    """
    makeTransitionToSecondBorderContinuous( (ENUBorder)first, (ENUBorder)second) -> None :

        C++ signature :
            void makeTransitionToSecondBorderContinuous(ad::map::lane::ENUBorder,ad::map::lane::ENUBorder {lvalue})"""
def makeTransitionToSecondEdgeContinuous(*args, **kwargs):
    """
    makeTransitionToSecondEdgeContinuous( (ENUEdge)first, (ENUEdge)second) -> None :

        C++ signature :
            void makeTransitionToSecondEdgeContinuous(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >,std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue})"""
def normalizeBorder(ad) -> Any:
    """
    normalizeBorder( (ENUBorder)border [, (ENUBorder)previousBorder=0]) -> None :

        C++ signature :
            void normalizeBorder(ad::map::lane::ENUBorder {lvalue} [,ad::map::lane::ENUBorder const*=0])"""
def oppositeLocation(ad) -> Any:
    """
    oppositeLocation( (ContactLocation)e) -> ContactLocation :

        C++ signature :
            ad::map::lane::ContactLocation oppositeLocation(ad::map::lane::ContactLocation)"""
def projectParametricPointToEdges(*args, **kwargs):
    """
    projectParametricPointToEdges( (Lane)lane, (ECEFPoint)referencePoint, (ECEFPoint)point_on_left_edge, (ECEFPoint)point_on_right_edge) -> bool :

        C++ signature :
            bool projectParametricPointToEdges(ad::map::lane::Lane,ad::map::point::ECEFPoint,ad::map::point::ECEFPoint {lvalue},ad::map::point::ECEFPoint {lvalue})

    projectParametricPointToEdges( (Lane)lane, (ParametricValue)longitudinalOffset, (ECEFPoint)point_on_left_edge, (ECEFPoint)point_on_right_edge) -> bool :

        C++ signature :
            bool projectParametricPointToEdges(ad::map::lane::Lane,ad::physics::ParametricValue,ad::map::point::ECEFPoint {lvalue},ad::map::point::ECEFPoint {lvalue})"""
def projectPositionToLaneInHeadingDirection(*args, **kwargs):
    """
    projectPositionToLaneInHeadingDirection( (ParaPoint)position, (ENUHeading)heading, (ParaPoint)projectedPosition) -> bool :

        C++ signature :
            bool projectPositionToLaneInHeadingDirection(ad::map::point::ParaPoint,ad::map::point::ENUHeading,ad::map::point::ParaPoint {lvalue})"""
def satisfiesFilter(*args, **kwargs):
    """
    satisfiesFilter( (Lane)lane, (str)typeFilter, (bool)isHov) -> bool :

        C++ signature :
            bool satisfiesFilter(ad::map::lane::Lane,std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >,bool)"""
@overload
def toString(ad) -> Any:
    """
    toString( (ContactLocation)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::ContactLocation)

    toString( (LaneType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::LaneType)

    toString( (ContactType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::ContactType)

    toString( (LaneDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::LaneDirection)"""
@overload
def toString(ad) -> Any:
    """
    toString( (ContactLocation)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::ContactLocation)

    toString( (LaneType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::LaneType)

    toString( (ContactType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::ContactType)

    toString( (LaneDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::LaneDirection)"""
@overload
def toString(ad) -> Any:
    """
    toString( (ContactLocation)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::ContactLocation)

    toString( (LaneType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::LaneType)

    toString( (ContactType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::ContactType)

    toString( (LaneDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::LaneDirection)"""
@overload
def toString(ad) -> Any:
    """
    toString( (ContactLocation)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::ContactLocation)

    toString( (LaneType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::LaneType)

    toString( (ContactType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::ContactType)

    toString( (LaneDirection)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::lane::LaneDirection)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneId)

    to_string( (LaneIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> >)

    to_string( (ContactLocation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLocation)

    to_string( (LaneType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneType)

    to_string( (ENUBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ENUBorder)

    to_string( (GeoBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::GeoBorder)

    to_string( (ContactType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactType)

    to_string( (ContactTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> >)

    to_string( (ContactLane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLane)

    to_string( (ContactLaneList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> >)

    to_string( (LaneDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneDirection)

    to_string( (Lane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::Lane)

    to_string( (GeoBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)

    to_string( (ECEFBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ECEFBorder)

    to_string( (ENUBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    to_string( (ECEFBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    to_string( (ContactLocationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> >)

    to_string( (LaneIdSet)laneIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneId)

    to_string( (LaneIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> >)

    to_string( (ContactLocation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLocation)

    to_string( (LaneType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneType)

    to_string( (ENUBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ENUBorder)

    to_string( (GeoBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::GeoBorder)

    to_string( (ContactType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactType)

    to_string( (ContactTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> >)

    to_string( (ContactLane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLane)

    to_string( (ContactLaneList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> >)

    to_string( (LaneDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneDirection)

    to_string( (Lane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::Lane)

    to_string( (GeoBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)

    to_string( (ECEFBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ECEFBorder)

    to_string( (ENUBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    to_string( (ECEFBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    to_string( (ContactLocationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> >)

    to_string( (LaneIdSet)laneIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneId)

    to_string( (LaneIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> >)

    to_string( (ContactLocation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLocation)

    to_string( (LaneType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneType)

    to_string( (ENUBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ENUBorder)

    to_string( (GeoBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::GeoBorder)

    to_string( (ContactType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactType)

    to_string( (ContactTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> >)

    to_string( (ContactLane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLane)

    to_string( (ContactLaneList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> >)

    to_string( (LaneDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneDirection)

    to_string( (Lane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::Lane)

    to_string( (GeoBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)

    to_string( (ECEFBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ECEFBorder)

    to_string( (ENUBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    to_string( (ECEFBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    to_string( (ContactLocationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> >)

    to_string( (LaneIdSet)laneIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneId)

    to_string( (LaneIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> >)

    to_string( (ContactLocation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLocation)

    to_string( (LaneType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneType)

    to_string( (ENUBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ENUBorder)

    to_string( (GeoBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::GeoBorder)

    to_string( (ContactType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactType)

    to_string( (ContactTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> >)

    to_string( (ContactLane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLane)

    to_string( (ContactLaneList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> >)

    to_string( (LaneDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneDirection)

    to_string( (Lane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::Lane)

    to_string( (GeoBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)

    to_string( (ECEFBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ECEFBorder)

    to_string( (ENUBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    to_string( (ECEFBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    to_string( (ContactLocationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> >)

    to_string( (LaneIdSet)laneIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneId)

    to_string( (LaneIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> >)

    to_string( (ContactLocation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLocation)

    to_string( (LaneType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneType)

    to_string( (ENUBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ENUBorder)

    to_string( (GeoBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::GeoBorder)

    to_string( (ContactType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactType)

    to_string( (ContactTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> >)

    to_string( (ContactLane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLane)

    to_string( (ContactLaneList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> >)

    to_string( (LaneDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneDirection)

    to_string( (Lane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::Lane)

    to_string( (GeoBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)

    to_string( (ECEFBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ECEFBorder)

    to_string( (ENUBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    to_string( (ECEFBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    to_string( (ContactLocationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> >)

    to_string( (LaneIdSet)laneIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneId)

    to_string( (LaneIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> >)

    to_string( (ContactLocation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLocation)

    to_string( (LaneType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneType)

    to_string( (ENUBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ENUBorder)

    to_string( (GeoBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::GeoBorder)

    to_string( (ContactType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactType)

    to_string( (ContactTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> >)

    to_string( (ContactLane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLane)

    to_string( (ContactLaneList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> >)

    to_string( (LaneDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneDirection)

    to_string( (Lane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::Lane)

    to_string( (GeoBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)

    to_string( (ECEFBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ECEFBorder)

    to_string( (ENUBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    to_string( (ECEFBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    to_string( (ContactLocationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> >)

    to_string( (LaneIdSet)laneIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneId)

    to_string( (LaneIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> >)

    to_string( (ContactLocation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLocation)

    to_string( (LaneType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneType)

    to_string( (ENUBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ENUBorder)

    to_string( (GeoBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::GeoBorder)

    to_string( (ContactType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactType)

    to_string( (ContactTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> >)

    to_string( (ContactLane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLane)

    to_string( (ContactLaneList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> >)

    to_string( (LaneDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneDirection)

    to_string( (Lane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::Lane)

    to_string( (GeoBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)

    to_string( (ECEFBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ECEFBorder)

    to_string( (ENUBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    to_string( (ECEFBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    to_string( (ContactLocationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> >)

    to_string( (LaneIdSet)laneIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneId)

    to_string( (LaneIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> >)

    to_string( (ContactLocation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLocation)

    to_string( (LaneType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneType)

    to_string( (ENUBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ENUBorder)

    to_string( (GeoBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::GeoBorder)

    to_string( (ContactType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactType)

    to_string( (ContactTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> >)

    to_string( (ContactLane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLane)

    to_string( (ContactLaneList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> >)

    to_string( (LaneDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneDirection)

    to_string( (Lane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::Lane)

    to_string( (GeoBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)

    to_string( (ECEFBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ECEFBorder)

    to_string( (ENUBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    to_string( (ECEFBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    to_string( (ContactLocationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> >)

    to_string( (LaneIdSet)laneIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneId)

    to_string( (LaneIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> >)

    to_string( (ContactLocation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLocation)

    to_string( (LaneType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneType)

    to_string( (ENUBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ENUBorder)

    to_string( (GeoBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::GeoBorder)

    to_string( (ContactType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactType)

    to_string( (ContactTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> >)

    to_string( (ContactLane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLane)

    to_string( (ContactLaneList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> >)

    to_string( (LaneDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneDirection)

    to_string( (Lane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::Lane)

    to_string( (GeoBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)

    to_string( (ECEFBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ECEFBorder)

    to_string( (ENUBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    to_string( (ECEFBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    to_string( (ContactLocationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> >)

    to_string( (LaneIdSet)laneIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LaneId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneId)

    to_string( (LaneIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::LaneId, std::allocator<ad::map::lane::LaneId> >)

    to_string( (ContactLocation)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLocation)

    to_string( (LaneType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneType)

    to_string( (ENUBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ENUBorder)

    to_string( (GeoBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::GeoBorder)

    to_string( (ContactType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactType)

    to_string( (ContactTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactType, std::allocator<ad::map::lane::ContactType> >)

    to_string( (ContactLane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ContactLane)

    to_string( (ContactLaneList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLane, std::allocator<ad::map::lane::ContactLane> >)

    to_string( (LaneDirection)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::LaneDirection)

    to_string( (Lane)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::Lane)

    to_string( (GeoBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::GeoBorder, std::allocator<ad::map::lane::GeoBorder> >)

    to_string( (ECEFBorder)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::lane::ECEFBorder)

    to_string( (ENUBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ENUBorder, std::allocator<ad::map::lane::ENUBorder> >)

    to_string( (ECEFBorderList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ECEFBorder, std::allocator<ad::map::lane::ECEFBorder> >)

    to_string( (ContactLocationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::lane::ContactLocation, std::allocator<ad::map::lane::ContactLocation> >)

    to_string( (LaneIdSet)laneIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::lane::LaneId, std::less<ad::map::lane::LaneId>, std::allocator<ad::map::lane::LaneId> >)"""
def uniqueLaneId(ad) -> Any:
    """
    uniqueLaneId( (GeoPoint)point) -> LaneId :

        C++ signature :
            ad::map::lane::LaneId uniqueLaneId(ad::map::point::GeoPoint)"""
def uniqueParaPoint(ad) -> Any:
    """
    uniqueParaPoint( (GeoPoint)point) -> ParaPoint :

        C++ signature :
            ad::map::point::ParaPoint uniqueParaPoint(ad::map::point::GeoPoint)"""
