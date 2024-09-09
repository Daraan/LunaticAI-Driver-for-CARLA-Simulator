import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

BICYCLE: RoadUserType
BUS: RoadUserType
CAR: RoadUserType
CAR_DIESEL: RoadUserType
CAR_ELECTRIC: RoadUserType
CAR_HYBRID: RoadUserType
CAR_PETROL: RoadUserType
INVALID: RoadUserType
MOTORBIKE: RoadUserType
PEDESTRIAN: RoadUserType
TRUCK: RoadUserType
UNKNOWN: RoadUserType

class Restriction(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    negated: Incomplete
    passengersMin: Incomplete
    roadUserTypes: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Restriction)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::restriction::Restriction)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Restriction)arg1, (Restriction)other) -> Restriction :

            C++ signature :
                ad::map::restriction::Restriction {lvalue} assign(ad::map::restriction::Restriction {lvalue},ad::map::restriction::Restriction)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Restriction)arg1, (Restriction)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::restriction::Restriction {lvalue},ad::map::restriction::Restriction)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Restriction)arg1, (Restriction)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::restriction::Restriction {lvalue},ad::map::restriction::Restriction)"""
    @classmethod
    def __reduce__(cls): ...

class RestrictionList(Boost.Python.instance):
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
        append( (RestrictionList)arg1, (Restriction)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},ad::map::restriction::Restriction)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (RestrictionList)arg1, (Restriction)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},ad::map::restriction::Restriction)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (RestrictionList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (RestrictionList)arg1, (Restriction)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},ad::map::restriction::Restriction)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (RestrictionList)arg1, (int)arg2, (Restriction)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},long,ad::map::restriction::Restriction)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (RestrictionList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (RestrictionList)arg1, (Restriction)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},ad::map::restriction::Restriction)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (RestrictionList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},long)

        __delitem__( (RestrictionList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (RestrictionList)arg1, (int)arg2) -> Restriction :

            C++ signature :
                ad::map::restriction::Restriction {lvalue} __getitem__(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},long)

        __getitem__( (RestrictionList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (RestrictionList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (RestrictionList)arg1, (int)arg2, (Restriction)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},long,ad::map::restriction::Restriction)

        __setitem__( (RestrictionList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Restrictions(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    conjunctions: Incomplete
    disjunctions: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Restrictions)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::restriction::Restrictions)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Restrictions)arg1, (Restrictions)other) -> Restrictions :

            C++ signature :
                ad::map::restriction::Restrictions {lvalue} assign(ad::map::restriction::Restrictions {lvalue},ad::map::restriction::Restrictions)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Restrictions)arg1, (Restrictions)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::restriction::Restrictions {lvalue},ad::map::restriction::Restrictions)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Restrictions)arg1, (Restrictions)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::restriction::Restrictions {lvalue},ad::map::restriction::Restrictions)"""
    @classmethod
    def __reduce__(cls): ...

class RoadUserType(Boost.Python.enum):
    BICYCLE: ClassVar[RoadUserType] = ...
    BUS: ClassVar[RoadUserType] = ...
    CAR: ClassVar[RoadUserType] = ...
    CAR_DIESEL: ClassVar[RoadUserType] = ...
    CAR_ELECTRIC: ClassVar[RoadUserType] = ...
    CAR_HYBRID: ClassVar[RoadUserType] = ...
    CAR_PETROL: ClassVar[RoadUserType] = ...
    INVALID: ClassVar[RoadUserType] = ...
    MOTORBIKE: ClassVar[RoadUserType] = ...
    PEDESTRIAN: ClassVar[RoadUserType] = ...
    TRUCK: ClassVar[RoadUserType] = ...
    UNKNOWN: ClassVar[RoadUserType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class RoadUserTypeList(Boost.Python.instance):
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
        append( (RoadUserTypeList)arg1, (RoadUserType)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},ad::map::restriction::RoadUserType)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (RoadUserTypeList)arg1, (RoadUserType)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},ad::map::restriction::RoadUserType)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (RoadUserTypeList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (RoadUserTypeList)arg1, (RoadUserType)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},ad::map::restriction::RoadUserType)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (RoadUserTypeList)arg1, (int)arg2, (RoadUserType)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},long,ad::map::restriction::RoadUserType)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (RoadUserTypeList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (RoadUserTypeList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (RoadUserTypeList)arg1, (RoadUserType)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},ad::map::restriction::RoadUserType)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (RoadUserTypeList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},long)

        __delitem__( (RoadUserTypeList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (RoadUserTypeList)arg1, (int)arg2) -> RoadUserType :

            C++ signature :
                ad::map::restriction::RoadUserType {lvalue} __getitem__(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},long)

        __getitem__( (RoadUserTypeList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (RoadUserTypeList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (RoadUserTypeList)arg1, (int)arg2, (RoadUserType)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},long,ad::map::restriction::RoadUserType)

        __setitem__( (RoadUserTypeList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class SpeedLimit(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    lanePiece: Incomplete
    speedLimit: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (SpeedLimit)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::restriction::SpeedLimit)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (SpeedLimit)arg1, (SpeedLimit)other) -> SpeedLimit :

            C++ signature :
                ad::map::restriction::SpeedLimit {lvalue} assign(ad::map::restriction::SpeedLimit {lvalue},ad::map::restriction::SpeedLimit)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (SpeedLimit)arg1, (SpeedLimit)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::restriction::SpeedLimit {lvalue},ad::map::restriction::SpeedLimit)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (SpeedLimit)arg1, (SpeedLimit)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::restriction::SpeedLimit {lvalue},ad::map::restriction::SpeedLimit)"""
    @classmethod
    def __reduce__(cls): ...

class SpeedLimitList(Boost.Python.instance):
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
        append( (SpeedLimitList)arg1, (SpeedLimit)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},ad::map::restriction::SpeedLimit)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (SpeedLimitList)arg1, (SpeedLimit)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},ad::map::restriction::SpeedLimit)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (SpeedLimitList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (SpeedLimitList)arg1, (SpeedLimit)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},ad::map::restriction::SpeedLimit)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (SpeedLimitList)arg1, (int)arg2, (SpeedLimit)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},long,ad::map::restriction::SpeedLimit)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (SpeedLimitList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (SpeedLimitList)arg1, (SpeedLimit)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},ad::map::restriction::SpeedLimit)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (SpeedLimitList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},long)

        __delitem__( (SpeedLimitList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (SpeedLimitList)arg1, (int)arg2) -> SpeedLimit :

            C++ signature :
                ad::map::restriction::SpeedLimit {lvalue} __getitem__(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},long)

        __getitem__( (SpeedLimitList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (SpeedLimitList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (SpeedLimitList)arg1, (int)arg2, (SpeedLimit)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},long,ad::map::restriction::SpeedLimit)

        __setitem__( (SpeedLimitList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class VehicleDescriptor(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    height: Incomplete
    length: Incomplete
    passengers: Incomplete
    type: Incomplete
    weight: Incomplete
    width: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (VehicleDescriptor)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::restriction::VehicleDescriptor)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (VehicleDescriptor)arg1, (VehicleDescriptor)other) -> VehicleDescriptor :

            C++ signature :
                ad::map::restriction::VehicleDescriptor {lvalue} assign(ad::map::restriction::VehicleDescriptor {lvalue},ad::map::restriction::VehicleDescriptor)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (VehicleDescriptor)arg1, (VehicleDescriptor)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::restriction::VehicleDescriptor {lvalue},ad::map::restriction::VehicleDescriptor)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (VehicleDescriptor)arg1, (VehicleDescriptor)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::restriction::VehicleDescriptor {lvalue},ad::map::restriction::VehicleDescriptor)"""
    @classmethod
    def __reduce__(cls): ...

def areAttributesEqual(*args, **kwargs):
    """
    areAttributesEqual( (SpeedLimit)left, (SpeedLimit)right) -> bool :

        C++ signature :
            bool areAttributesEqual(ad::map::restriction::SpeedLimit,ad::map::restriction::SpeedLimit)"""
def fromString(*args, **kwargs):
    """
    fromString( (str)str) -> RoadUserType :

        C++ signature :
            ad::map::restriction::RoadUserType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
def getHOV(ad) -> Any:
    """
    getHOV( (Restrictions)restrictions) -> int :

        C++ signature :
            unsigned short getHOV(ad::map::restriction::Restrictions)"""
def isAccessOk(*args, **kwargs):
    """
    isAccessOk( (Restriction)restriction, (VehicleDescriptor)vehicle) -> bool :

        C++ signature :
            bool isAccessOk(ad::map::restriction::Restriction,ad::map::restriction::VehicleDescriptor)

    isAccessOk( (Restrictions)restrictions, (VehicleDescriptor)vehicle) -> bool :

        C++ signature :
            bool isAccessOk(ad::map::restriction::Restrictions,ad::map::restriction::VehicleDescriptor)"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (VehicleDescriptor)descriptor [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::restriction::VehicleDescriptor [,bool=True])

    isValid( (Restriction)restriction [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::restriction::Restriction [,bool=True])

    isValid( (Restrictions)restrictions [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::restriction::Restrictions [,bool=True])"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (VehicleDescriptor)descriptor [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::restriction::VehicleDescriptor [,bool=True])

    isValid( (Restriction)restriction [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::restriction::Restriction [,bool=True])

    isValid( (Restrictions)restrictions [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::restriction::Restrictions [,bool=True])"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (VehicleDescriptor)descriptor [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::restriction::VehicleDescriptor [,bool=True])

    isValid( (Restriction)restriction [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::restriction::Restriction [,bool=True])

    isValid( (Restrictions)restrictions [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::restriction::Restrictions [,bool=True])"""
def toString(ad) -> Any:
    """
    toString( (RoadUserType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::restriction::RoadUserType)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (RoadUserType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::RoadUserType)

    to_string( (RoadUserTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> >)

    to_string( (Restriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::Restriction)

    to_string( (RestrictionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> >)

    to_string( (Restrictions)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::Restrictions)

    to_string( (VehicleDescriptor)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::VehicleDescriptor)

    to_string( (SpeedLimit)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::SpeedLimit)

    to_string( (SpeedLimitList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (RoadUserType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::RoadUserType)

    to_string( (RoadUserTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> >)

    to_string( (Restriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::Restriction)

    to_string( (RestrictionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> >)

    to_string( (Restrictions)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::Restrictions)

    to_string( (VehicleDescriptor)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::VehicleDescriptor)

    to_string( (SpeedLimit)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::SpeedLimit)

    to_string( (SpeedLimitList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (RoadUserType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::RoadUserType)

    to_string( (RoadUserTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> >)

    to_string( (Restriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::Restriction)

    to_string( (RestrictionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> >)

    to_string( (Restrictions)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::Restrictions)

    to_string( (VehicleDescriptor)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::VehicleDescriptor)

    to_string( (SpeedLimit)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::SpeedLimit)

    to_string( (SpeedLimitList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (RoadUserType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::RoadUserType)

    to_string( (RoadUserTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> >)

    to_string( (Restriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::Restriction)

    to_string( (RestrictionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> >)

    to_string( (Restrictions)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::Restrictions)

    to_string( (VehicleDescriptor)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::VehicleDescriptor)

    to_string( (SpeedLimit)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::SpeedLimit)

    to_string( (SpeedLimitList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (RoadUserType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::RoadUserType)

    to_string( (RoadUserTypeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::RoadUserType, std::allocator<ad::map::restriction::RoadUserType> >)

    to_string( (Restriction)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::Restriction)

    to_string( (RestrictionList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::Restriction, std::allocator<ad::map::restriction::Restriction> >)

    to_string( (Restrictions)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::Restrictions)

    to_string( (VehicleDescriptor)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::VehicleDescriptor)

    to_string( (SpeedLimit)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::restriction::SpeedLimit)

    to_string( (SpeedLimitList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::restriction::SpeedLimit, std::allocator<ad::map::restriction::SpeedLimit> >)"""
