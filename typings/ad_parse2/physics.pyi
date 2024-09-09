import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

c2PI: Angle
cPI: Angle
cPI_2: Angle

class Acceleration(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iAcceleration) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (Acceleration)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Acceleration)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Acceleration)arg1, (Acceleration)other) -> Acceleration :

            C++ signature :
                ad::physics::Acceleration {lvalue} assign(ad::physics::Acceleration {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (Acceleration)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::Acceleration {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (Acceleration)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::Acceleration {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> Acceleration :

            C++ signature :
                ad::physics::Acceleration getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> Acceleration :

            C++ signature :
                ad::physics::Acceleration getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> Acceleration :

            C++ signature :
                ad::physics::Acceleration getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (Acceleration)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::Acceleration {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Acceleration)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Acceleration {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (Acceleration)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::Acceleration {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (Acceleration)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::Acceleration {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (Acceleration)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::Acceleration {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::Acceleration&>,ad::physics::Acceleration)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::Acceleration&>,ad::physics::Acceleration)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (Acceleration)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::Acceleration {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (Acceleration)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::Acceleration {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (Acceleration)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Acceleration {lvalue},double)

        __mul__( (Acceleration)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Acceleration {lvalue},ad::physics::ParametricValue)

        __mul__( (Acceleration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Acceleration {lvalue},ad::physics::Duration)

        __mul__( (Acceleration)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Acceleration {lvalue},ad::physics::DurationSquared)

        __mul__( (Acceleration)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Acceleration {lvalue},ad::physics::Distance)

        __mul__( (Acceleration)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Acceleration {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Acceleration)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Acceleration {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (Acceleration)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::Acceleration {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (Acceleration)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::Acceleration {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (Acceleration)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::Acceleration {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (Acceleration)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Acceleration {lvalue},double)

        __truediv__( (Acceleration)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Acceleration {lvalue},ad::physics::Acceleration)

        __truediv__( (Acceleration)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Acceleration {lvalue},ad::physics::ParametricValue)

        __truediv__( (Acceleration)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Acceleration {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class Acceleration3D(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    x: Incomplete
    y: Incomplete
    z: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Acceleration3D)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Acceleration3D)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Acceleration3D)arg1, (Acceleration3D)other) -> Acceleration3D :

            C++ signature :
                ad::physics::Acceleration3D {lvalue} assign(ad::physics::Acceleration3D {lvalue},ad::physics::Acceleration3D)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Acceleration3D)arg1, (Acceleration3D)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Acceleration3D {lvalue},ad::physics::Acceleration3D)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Acceleration3D)arg1, (Acceleration3D)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Acceleration3D {lvalue},ad::physics::Acceleration3D)"""
    @classmethod
    def __reduce__(cls): ...

class Acceleration3DList(Boost.Python.instance):
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
        append( (Acceleration3DList)arg1, (Acceleration3D)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},ad::physics::Acceleration3D)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (Acceleration3DList)arg1, (Acceleration3D)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},ad::physics::Acceleration3D)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (Acceleration3DList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (Acceleration3DList)arg1, (Acceleration3D)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},ad::physics::Acceleration3D)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (Acceleration3DList)arg1, (int)arg2, (Acceleration3D)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},long,ad::physics::Acceleration3D)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (Acceleration3DList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (Acceleration3DList)arg1, (Acceleration3D)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},ad::physics::Acceleration3D)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (Acceleration3DList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},long)

        __delitem__( (Acceleration3DList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (Acceleration3DList)arg1, (int)arg2) -> Acceleration3D :

            C++ signature :
                ad::physics::Acceleration3D {lvalue} __getitem__(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},long)

        __getitem__( (Acceleration3DList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (Acceleration3DList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (Acceleration3DList)arg1, (int)arg2, (Acceleration3D)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},long,ad::physics::Acceleration3D)

        __setitem__( (Acceleration3DList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class AccelerationList(Boost.Python.instance):
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
        append( (AccelerationList)arg1, (Acceleration)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (AccelerationList)arg1, (Acceleration)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (AccelerationList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (AccelerationList)arg1, (Acceleration)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (AccelerationList)arg1, (int)arg2, (Acceleration)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},long,ad::physics::Acceleration)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (AccelerationList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (AccelerationList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (AccelerationList)arg1, (Acceleration)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},ad::physics::Acceleration)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (AccelerationList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},long)

        __delitem__( (AccelerationList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (AccelerationList)arg1, (int)arg2) -> Acceleration :

            C++ signature :
                ad::physics::Acceleration {lvalue} __getitem__(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},long)

        __getitem__( (AccelerationList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (AccelerationList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (AccelerationList)arg1, (int)arg2, (Acceleration)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},long,ad::physics::Acceleration)

        __setitem__( (AccelerationList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class AccelerationRange(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    maximum: Incomplete
    minimum: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (AccelerationRange)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::AccelerationRange)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (AccelerationRange)arg1, (AccelerationRange)other) -> AccelerationRange :

            C++ signature :
                ad::physics::AccelerationRange {lvalue} assign(ad::physics::AccelerationRange {lvalue},ad::physics::AccelerationRange)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (AccelerationRange)arg1, (AccelerationRange)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::AccelerationRange {lvalue},ad::physics::AccelerationRange)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (AccelerationRange)arg1, (AccelerationRange)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::AccelerationRange {lvalue},ad::physics::AccelerationRange)"""
    @classmethod
    def __reduce__(cls): ...

class AccelerationRangeList(Boost.Python.instance):
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
        append( (AccelerationRangeList)arg1, (AccelerationRange)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},ad::physics::AccelerationRange)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (AccelerationRangeList)arg1, (AccelerationRange)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},ad::physics::AccelerationRange)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (AccelerationRangeList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (AccelerationRangeList)arg1, (AccelerationRange)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},ad::physics::AccelerationRange)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (AccelerationRangeList)arg1, (int)arg2, (AccelerationRange)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},long,ad::physics::AccelerationRange)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (AccelerationRangeList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (AccelerationRangeList)arg1, (AccelerationRange)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},ad::physics::AccelerationRange)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (AccelerationRangeList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},long)

        __delitem__( (AccelerationRangeList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (AccelerationRangeList)arg1, (int)arg2) -> AccelerationRange :

            C++ signature :
                ad::physics::AccelerationRange {lvalue} __getitem__(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},long)

        __getitem__( (AccelerationRangeList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (AccelerationRangeList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (AccelerationRangeList)arg1, (int)arg2, (AccelerationRange)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},long,ad::physics::AccelerationRange)

        __setitem__( (AccelerationRangeList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Angle(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iAngle) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (Angle)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Angle)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Angle)arg1, (Angle)other) -> Angle :

            C++ signature :
                ad::physics::Angle {lvalue} assign(ad::physics::Angle {lvalue},ad::physics::Angle)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (Angle)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::Angle {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (Angle)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::Angle {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> Angle :

            C++ signature :
                ad::physics::Angle getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> Angle :

            C++ signature :
                ad::physics::Angle getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> Angle :

            C++ signature :
                ad::physics::Angle getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (Angle)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::Angle {lvalue},ad::physics::Angle)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Angle)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Angle {lvalue},ad::physics::Angle)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (Angle)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::Angle {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (Angle)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::Angle {lvalue},ad::physics::Angle)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (Angle)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::Angle {lvalue},ad::physics::Angle)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::Angle&>,ad::physics::Angle)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::Angle&>,ad::physics::Angle)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (Angle)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::Angle {lvalue},ad::physics::Angle)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (Angle)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::Angle {lvalue},ad::physics::Angle)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (Angle)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Angle {lvalue},double)

        __mul__( (Angle)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Angle {lvalue},ad::physics::ParametricValue)

        __mul__( (Angle)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Angle {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Angle)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Angle {lvalue},ad::physics::Angle)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (Angle)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::Angle {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (Angle)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::Angle {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (Angle)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::Angle {lvalue},ad::physics::Angle)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (Angle)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Angle {lvalue},double)

        __truediv__( (Angle)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Angle {lvalue},ad::physics::Angle)

        __truediv__( (Angle)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Angle {lvalue},ad::physics::ParametricValue)

        __truediv__( (Angle)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Angle {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class AngleList(Boost.Python.instance):
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
        append( (AngleList)arg1, (Angle)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},ad::physics::Angle)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (AngleList)arg1, (Angle)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},ad::physics::Angle)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (AngleList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (AngleList)arg1, (Angle)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},ad::physics::Angle)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (AngleList)arg1, (int)arg2, (Angle)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},long,ad::physics::Angle)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (AngleList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (AngleList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (AngleList)arg1, (Angle)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},ad::physics::Angle)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (AngleList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},long)

        __delitem__( (AngleList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (AngleList)arg1, (int)arg2) -> Angle :

            C++ signature :
                ad::physics::Angle {lvalue} __getitem__(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},long)

        __getitem__( (AngleList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (AngleList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (AngleList)arg1, (int)arg2, (Angle)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},long,ad::physics::Angle)

        __setitem__( (AngleList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class AngleRange(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    maximum: Incomplete
    minimum: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (AngleRange)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::AngleRange)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (AngleRange)arg1, (AngleRange)other) -> AngleRange :

            C++ signature :
                ad::physics::AngleRange {lvalue} assign(ad::physics::AngleRange {lvalue},ad::physics::AngleRange)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (AngleRange)arg1, (AngleRange)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::AngleRange {lvalue},ad::physics::AngleRange)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (AngleRange)arg1, (AngleRange)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::AngleRange {lvalue},ad::physics::AngleRange)"""
    @classmethod
    def __reduce__(cls): ...

class AngleRangeList(Boost.Python.instance):
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
        append( (AngleRangeList)arg1, (AngleRange)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},ad::physics::AngleRange)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (AngleRangeList)arg1, (AngleRange)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},ad::physics::AngleRange)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (AngleRangeList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (AngleRangeList)arg1, (AngleRange)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},ad::physics::AngleRange)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (AngleRangeList)arg1, (int)arg2, (AngleRange)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},long,ad::physics::AngleRange)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (AngleRangeList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (AngleRangeList)arg1, (AngleRange)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},ad::physics::AngleRange)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (AngleRangeList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},long)

        __delitem__( (AngleRangeList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (AngleRangeList)arg1, (int)arg2) -> AngleRange :

            C++ signature :
                ad::physics::AngleRange {lvalue} __getitem__(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},long)

        __getitem__( (AngleRangeList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (AngleRangeList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (AngleRangeList)arg1, (int)arg2, (AngleRange)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},long,ad::physics::AngleRange)

        __setitem__( (AngleRangeList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class AngularAcceleration(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iAngularAcceleration) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (AngularAcceleration)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::AngularAcceleration)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (AngularAcceleration)arg1, (AngularAcceleration)other) -> AngularAcceleration :

            C++ signature :
                ad::physics::AngularAcceleration {lvalue} assign(ad::physics::AngularAcceleration {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (AngularAcceleration)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::AngularAcceleration {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (AngularAcceleration)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::AngularAcceleration {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> AngularAcceleration :

            C++ signature :
                ad::physics::AngularAcceleration getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> AngularAcceleration :

            C++ signature :
                ad::physics::AngularAcceleration getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> AngularAcceleration :

            C++ signature :
                ad::physics::AngularAcceleration getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (AngularAcceleration)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::AngularAcceleration {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (AngularAcceleration)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::AngularAcceleration {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (AngularAcceleration)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::AngularAcceleration {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (AngularAcceleration)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::AngularAcceleration {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (AngularAcceleration)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::AngularAcceleration {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::AngularAcceleration&>,ad::physics::AngularAcceleration)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::AngularAcceleration&>,ad::physics::AngularAcceleration)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (AngularAcceleration)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::AngularAcceleration {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (AngularAcceleration)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::AngularAcceleration {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (AngularAcceleration)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::AngularAcceleration {lvalue},double)

        __mul__( (AngularAcceleration)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::AngularAcceleration {lvalue},ad::physics::ParametricValue)

        __mul__( (AngularAcceleration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::AngularAcceleration {lvalue},ad::physics::Duration)

        __mul__( (AngularAcceleration)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::AngularAcceleration {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (AngularAcceleration)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::AngularAcceleration {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (AngularAcceleration)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::AngularAcceleration {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (AngularAcceleration)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::AngularAcceleration {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (AngularAcceleration)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::AngularAcceleration {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (AngularAcceleration)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::AngularAcceleration {lvalue},double)

        __truediv__( (AngularAcceleration)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::AngularAcceleration {lvalue},ad::physics::AngularAcceleration)

        __truediv__( (AngularAcceleration)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::AngularAcceleration {lvalue},ad::physics::ParametricValue)

        __truediv__( (AngularAcceleration)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::AngularAcceleration {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class AngularAccelerationList(Boost.Python.instance):
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
        append( (AngularAccelerationList)arg1, (AngularAcceleration)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (AngularAccelerationList)arg1, (AngularAcceleration)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (AngularAccelerationList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (AngularAccelerationList)arg1, (AngularAcceleration)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (AngularAccelerationList)arg1, (int)arg2, (AngularAcceleration)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},long,ad::physics::AngularAcceleration)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (AngularAccelerationList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (AngularAccelerationList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (AngularAccelerationList)arg1, (AngularAcceleration)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},ad::physics::AngularAcceleration)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (AngularAccelerationList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},long)

        __delitem__( (AngularAccelerationList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (AngularAccelerationList)arg1, (int)arg2) -> AngularAcceleration :

            C++ signature :
                ad::physics::AngularAcceleration {lvalue} __getitem__(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},long)

        __getitem__( (AngularAccelerationList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (AngularAccelerationList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (AngularAccelerationList)arg1, (int)arg2, (AngularAcceleration)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},long,ad::physics::AngularAcceleration)

        __setitem__( (AngularAccelerationList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class AngularVelocity(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iAngularVelocity) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (AngularVelocity)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::AngularVelocity)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (AngularVelocity)arg1, (AngularVelocity)other) -> AngularVelocity :

            C++ signature :
                ad::physics::AngularVelocity {lvalue} assign(ad::physics::AngularVelocity {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (AngularVelocity)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::AngularVelocity {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (AngularVelocity)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::AngularVelocity {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> AngularVelocity :

            C++ signature :
                ad::physics::AngularVelocity getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> AngularVelocity :

            C++ signature :
                ad::physics::AngularVelocity getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> AngularVelocity :

            C++ signature :
                ad::physics::AngularVelocity getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (AngularVelocity)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::AngularVelocity {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (AngularVelocity)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::AngularVelocity {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (AngularVelocity)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::AngularVelocity {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (AngularVelocity)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::AngularVelocity {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (AngularVelocity)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::AngularVelocity {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::AngularVelocity&>,ad::physics::AngularVelocity)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::AngularVelocity&>,ad::physics::AngularVelocity)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (AngularVelocity)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::AngularVelocity {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (AngularVelocity)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::AngularVelocity {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (AngularVelocity)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::AngularVelocity {lvalue},double)

        __mul__( (AngularVelocity)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::AngularVelocity {lvalue},ad::physics::ParametricValue)

        __mul__( (AngularVelocity)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::AngularVelocity {lvalue},ad::physics::Duration)

        __mul__( (AngularVelocity)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::AngularVelocity {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (AngularVelocity)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::AngularVelocity {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (AngularVelocity)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::AngularVelocity {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (AngularVelocity)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::AngularVelocity {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (AngularVelocity)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::AngularVelocity {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (AngularVelocity)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::AngularVelocity {lvalue},double)

        __truediv__( (AngularVelocity)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::AngularVelocity {lvalue},ad::physics::AngularVelocity)

        __truediv__( (AngularVelocity)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::AngularVelocity {lvalue},ad::physics::ParametricValue)

        __truediv__( (AngularVelocity)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::AngularVelocity {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class AngularVelocity3D(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    x: Incomplete
    y: Incomplete
    z: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (AngularVelocity3D)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::AngularVelocity3D)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (AngularVelocity3D)arg1, (AngularVelocity3D)other) -> AngularVelocity3D :

            C++ signature :
                ad::physics::AngularVelocity3D {lvalue} assign(ad::physics::AngularVelocity3D {lvalue},ad::physics::AngularVelocity3D)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (AngularVelocity3D)arg1, (AngularVelocity3D)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::AngularVelocity3D {lvalue},ad::physics::AngularVelocity3D)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (AngularVelocity3D)arg1, (AngularVelocity3D)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::AngularVelocity3D {lvalue},ad::physics::AngularVelocity3D)"""
    @classmethod
    def __reduce__(cls): ...

class AngularVelocity3DList(Boost.Python.instance):
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
        append( (AngularVelocity3DList)arg1, (AngularVelocity3D)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},ad::physics::AngularVelocity3D)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (AngularVelocity3DList)arg1, (AngularVelocity3D)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},ad::physics::AngularVelocity3D)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (AngularVelocity3DList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (AngularVelocity3DList)arg1, (AngularVelocity3D)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},ad::physics::AngularVelocity3D)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (AngularVelocity3DList)arg1, (int)arg2, (AngularVelocity3D)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},long,ad::physics::AngularVelocity3D)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (AngularVelocity3DList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (AngularVelocity3DList)arg1, (AngularVelocity3D)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},ad::physics::AngularVelocity3D)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (AngularVelocity3DList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},long)

        __delitem__( (AngularVelocity3DList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (AngularVelocity3DList)arg1, (int)arg2) -> AngularVelocity3D :

            C++ signature :
                ad::physics::AngularVelocity3D {lvalue} __getitem__(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},long)

        __getitem__( (AngularVelocity3DList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (AngularVelocity3DList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (AngularVelocity3DList)arg1, (int)arg2, (AngularVelocity3D)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},long,ad::physics::AngularVelocity3D)

        __setitem__( (AngularVelocity3DList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class AngularVelocityList(Boost.Python.instance):
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
        append( (AngularVelocityList)arg1, (AngularVelocity)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (AngularVelocityList)arg1, (AngularVelocity)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (AngularVelocityList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (AngularVelocityList)arg1, (AngularVelocity)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (AngularVelocityList)arg1, (int)arg2, (AngularVelocity)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},long,ad::physics::AngularVelocity)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (AngularVelocityList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (AngularVelocityList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (AngularVelocityList)arg1, (AngularVelocity)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},ad::physics::AngularVelocity)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (AngularVelocityList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},long)

        __delitem__( (AngularVelocityList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (AngularVelocityList)arg1, (int)arg2) -> AngularVelocity :

            C++ signature :
                ad::physics::AngularVelocity {lvalue} __getitem__(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},long)

        __getitem__( (AngularVelocityList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (AngularVelocityList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (AngularVelocityList)arg1, (int)arg2, (AngularVelocity)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},long,ad::physics::AngularVelocity)

        __setitem__( (AngularVelocityList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Dimension2D(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    length: Incomplete
    width: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Dimension2D)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Dimension2D)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Dimension2D)arg1, (Dimension2D)other) -> Dimension2D :

            C++ signature :
                ad::physics::Dimension2D {lvalue} assign(ad::physics::Dimension2D {lvalue},ad::physics::Dimension2D)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Dimension2D)arg1, (Dimension2D)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Dimension2D {lvalue},ad::physics::Dimension2D)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Dimension2D)arg1, (Dimension2D)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Dimension2D {lvalue},ad::physics::Dimension2D)"""
    @classmethod
    def __reduce__(cls): ...

class Dimension2DList(Boost.Python.instance):
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
        append( (Dimension2DList)arg1, (Dimension2D)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},ad::physics::Dimension2D)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (Dimension2DList)arg1, (Dimension2D)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},ad::physics::Dimension2D)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (Dimension2DList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (Dimension2DList)arg1, (Dimension2D)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},ad::physics::Dimension2D)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (Dimension2DList)arg1, (int)arg2, (Dimension2D)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},long,ad::physics::Dimension2D)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (Dimension2DList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (Dimension2DList)arg1, (Dimension2D)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},ad::physics::Dimension2D)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (Dimension2DList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},long)

        __delitem__( (Dimension2DList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (Dimension2DList)arg1, (int)arg2) -> Dimension2D :

            C++ signature :
                ad::physics::Dimension2D {lvalue} __getitem__(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},long)

        __getitem__( (Dimension2DList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (Dimension2DList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (Dimension2DList)arg1, (int)arg2, (Dimension2D)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},long,ad::physics::Dimension2D)

        __setitem__( (Dimension2DList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Dimension3D(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    height: Incomplete
    length: Incomplete
    width: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Dimension3D)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Dimension3D)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Dimension3D)arg1, (Dimension3D)other) -> Dimension3D :

            C++ signature :
                ad::physics::Dimension3D {lvalue} assign(ad::physics::Dimension3D {lvalue},ad::physics::Dimension3D)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Dimension3D)arg1, (Dimension3D)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Dimension3D {lvalue},ad::physics::Dimension3D)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Dimension3D)arg1, (Dimension3D)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Dimension3D {lvalue},ad::physics::Dimension3D)"""
    @classmethod
    def __reduce__(cls): ...

class Dimension3DList(Boost.Python.instance):
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
        append( (Dimension3DList)arg1, (Dimension3D)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},ad::physics::Dimension3D)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (Dimension3DList)arg1, (Dimension3D)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},ad::physics::Dimension3D)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (Dimension3DList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (Dimension3DList)arg1, (Dimension3D)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},ad::physics::Dimension3D)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (Dimension3DList)arg1, (int)arg2, (Dimension3D)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},long,ad::physics::Dimension3D)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (Dimension3DList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (Dimension3DList)arg1, (Dimension3D)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},ad::physics::Dimension3D)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (Dimension3DList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},long)

        __delitem__( (Dimension3DList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (Dimension3DList)arg1, (int)arg2) -> Dimension3D :

            C++ signature :
                ad::physics::Dimension3D {lvalue} __getitem__(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},long)

        __getitem__( (Dimension3DList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (Dimension3DList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (Dimension3DList)arg1, (int)arg2, (Dimension3D)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},long,ad::physics::Dimension3D)

        __setitem__( (Dimension3DList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Distance(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iDistance) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (Distance)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Distance)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Distance)arg1, (Distance)other) -> Distance :

            C++ signature :
                ad::physics::Distance {lvalue} assign(ad::physics::Distance {lvalue},ad::physics::Distance)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (Distance)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::Distance {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (Distance)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::Distance {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> Distance :

            C++ signature :
                ad::physics::Distance getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> Distance :

            C++ signature :
                ad::physics::Distance getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> Distance :

            C++ signature :
                ad::physics::Distance getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (Distance)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::Distance {lvalue},ad::physics::Distance)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Distance)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Distance {lvalue},ad::physics::Distance)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (Distance)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::Distance {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (Distance)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::Distance {lvalue},ad::physics::Distance)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (Distance)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::Distance {lvalue},ad::physics::Distance)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::Distance&>,ad::physics::Distance)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::Distance&>,ad::physics::Distance)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (Distance)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::Distance {lvalue},ad::physics::Distance)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (Distance)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::Distance {lvalue},ad::physics::Distance)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (Distance)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Distance {lvalue},ad::physics::Distance)

        __mul__( (Distance)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Distance {lvalue},double)

        __mul__( (Distance)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Distance {lvalue},ad::physics::ParametricValue)

        __mul__( (Distance)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Distance {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Distance)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Distance {lvalue},ad::physics::Distance)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (Distance)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::Distance {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (Distance)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::Distance {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (Distance)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::Distance {lvalue},ad::physics::Distance)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (Distance)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Distance {lvalue},double)

        __truediv__( (Distance)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Distance {lvalue},ad::physics::Distance)

        __truediv__( (Distance)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Distance {lvalue},ad::physics::ParametricValue)

        __truediv__( (Distance)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Distance {lvalue},ad::physics::Speed)

        __truediv__( (Distance)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Distance {lvalue},ad::physics::Acceleration)

        __truediv__( (Distance)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Distance {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class Distance2D(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    x: Incomplete
    y: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Distance2D)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Distance2D)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Distance2D)arg1, (Distance2D)other) -> Distance2D :

            C++ signature :
                ad::physics::Distance2D {lvalue} assign(ad::physics::Distance2D {lvalue},ad::physics::Distance2D)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Distance2D)arg1, (Distance2D)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Distance2D {lvalue},ad::physics::Distance2D)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Distance2D)arg1, (Distance2D)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Distance2D {lvalue},ad::physics::Distance2D)"""
    @classmethod
    def __reduce__(cls): ...

class Distance2DList(Boost.Python.instance):
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
        append( (Distance2DList)arg1, (Distance2D)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},ad::physics::Distance2D)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (Distance2DList)arg1, (Distance2D)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},ad::physics::Distance2D)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (Distance2DList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (Distance2DList)arg1, (Distance2D)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},ad::physics::Distance2D)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (Distance2DList)arg1, (int)arg2, (Distance2D)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},long,ad::physics::Distance2D)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (Distance2DList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (Distance2DList)arg1, (Distance2D)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},ad::physics::Distance2D)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (Distance2DList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},long)

        __delitem__( (Distance2DList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (Distance2DList)arg1, (int)arg2) -> Distance2D :

            C++ signature :
                ad::physics::Distance2D {lvalue} __getitem__(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},long)

        __getitem__( (Distance2DList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (Distance2DList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (Distance2DList)arg1, (int)arg2, (Distance2D)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},long,ad::physics::Distance2D)

        __setitem__( (Distance2DList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Distance3D(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    x: Incomplete
    y: Incomplete
    z: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Distance3D)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Distance3D)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Distance3D)arg1, (Distance3D)other) -> Distance3D :

            C++ signature :
                ad::physics::Distance3D {lvalue} assign(ad::physics::Distance3D {lvalue},ad::physics::Distance3D)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Distance3D)arg1, (Distance3D)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Distance3D {lvalue},ad::physics::Distance3D)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Distance3D)arg1, (Distance3D)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Distance3D {lvalue},ad::physics::Distance3D)"""
    @classmethod
    def __reduce__(cls): ...

class Distance3DList(Boost.Python.instance):
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
        append( (Distance3DList)arg1, (Distance3D)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},ad::physics::Distance3D)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (Distance3DList)arg1, (Distance3D)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},ad::physics::Distance3D)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (Distance3DList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (Distance3DList)arg1, (Distance3D)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},ad::physics::Distance3D)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (Distance3DList)arg1, (int)arg2, (Distance3D)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},long,ad::physics::Distance3D)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (Distance3DList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (Distance3DList)arg1, (Distance3D)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},ad::physics::Distance3D)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (Distance3DList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},long)

        __delitem__( (Distance3DList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (Distance3DList)arg1, (int)arg2) -> Distance3D :

            C++ signature :
                ad::physics::Distance3D {lvalue} __getitem__(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},long)

        __getitem__( (Distance3DList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (Distance3DList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (Distance3DList)arg1, (int)arg2, (Distance3D)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},long,ad::physics::Distance3D)

        __setitem__( (Distance3DList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class DistanceList(Boost.Python.instance):
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
        append( (DistanceList)arg1, (Distance)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},ad::physics::Distance)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (DistanceList)arg1, (Distance)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},ad::physics::Distance)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (DistanceList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (DistanceList)arg1, (Distance)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},ad::physics::Distance)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (DistanceList)arg1, (int)arg2, (Distance)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},long,ad::physics::Distance)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (DistanceList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (DistanceList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (DistanceList)arg1, (Distance)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},ad::physics::Distance)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (DistanceList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},long)

        __delitem__( (DistanceList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (DistanceList)arg1, (int)arg2) -> Distance :

            C++ signature :
                ad::physics::Distance {lvalue} __getitem__(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},long)

        __getitem__( (DistanceList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (DistanceList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (DistanceList)arg1, (int)arg2, (Distance)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},long,ad::physics::Distance)

        __setitem__( (DistanceList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class DistanceSquared(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iDistanceSquared) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (DistanceSquared)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::DistanceSquared)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (DistanceSquared)arg1, (DistanceSquared)other) -> DistanceSquared :

            C++ signature :
                ad::physics::DistanceSquared {lvalue} assign(ad::physics::DistanceSquared {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (DistanceSquared)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::DistanceSquared {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (DistanceSquared)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::DistanceSquared {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> DistanceSquared :

            C++ signature :
                ad::physics::DistanceSquared getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> DistanceSquared :

            C++ signature :
                ad::physics::DistanceSquared getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> DistanceSquared :

            C++ signature :
                ad::physics::DistanceSquared getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (DistanceSquared)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::DistanceSquared {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (DistanceSquared)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::DistanceSquared {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (DistanceSquared)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::DistanceSquared {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (DistanceSquared)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::DistanceSquared {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (DistanceSquared)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::DistanceSquared {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::DistanceSquared&>,ad::physics::DistanceSquared)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::DistanceSquared&>,ad::physics::DistanceSquared)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (DistanceSquared)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::DistanceSquared {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (DistanceSquared)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::DistanceSquared {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (DistanceSquared)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::DistanceSquared {lvalue},double)

        __mul__( (DistanceSquared)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::DistanceSquared {lvalue},ad::physics::ParametricValue)

        __mul__( (DistanceSquared)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::DistanceSquared {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (DistanceSquared)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::DistanceSquared {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (DistanceSquared)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::DistanceSquared {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (DistanceSquared)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::DistanceSquared {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (DistanceSquared)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::DistanceSquared {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (DistanceSquared)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::DistanceSquared {lvalue},double)

        __truediv__( (DistanceSquared)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::DistanceSquared {lvalue},ad::physics::DistanceSquared)

        __truediv__( (DistanceSquared)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::DistanceSquared {lvalue},ad::physics::ParametricValue)

        __truediv__( (DistanceSquared)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::DistanceSquared {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class DistanceSquaredList(Boost.Python.instance):
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
        append( (DistanceSquaredList)arg1, (DistanceSquared)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (DistanceSquaredList)arg1, (DistanceSquared)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (DistanceSquaredList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (DistanceSquaredList)arg1, (DistanceSquared)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (DistanceSquaredList)arg1, (int)arg2, (DistanceSquared)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},long,ad::physics::DistanceSquared)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (DistanceSquaredList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (DistanceSquaredList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (DistanceSquaredList)arg1, (DistanceSquared)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},ad::physics::DistanceSquared)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (DistanceSquaredList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},long)

        __delitem__( (DistanceSquaredList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (DistanceSquaredList)arg1, (int)arg2) -> DistanceSquared :

            C++ signature :
                ad::physics::DistanceSquared {lvalue} __getitem__(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},long)

        __getitem__( (DistanceSquaredList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (DistanceSquaredList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (DistanceSquaredList)arg1, (int)arg2, (DistanceSquared)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},long,ad::physics::DistanceSquared)

        __setitem__( (DistanceSquaredList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Duration(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iDuration) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (Duration)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Duration)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Duration)arg1, (Duration)other) -> Duration :

            C++ signature :
                ad::physics::Duration {lvalue} assign(ad::physics::Duration {lvalue},ad::physics::Duration)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (Duration)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::Duration {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (Duration)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::Duration {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> Duration :

            C++ signature :
                ad::physics::Duration getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> Duration :

            C++ signature :
                ad::physics::Duration getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> Duration :

            C++ signature :
                ad::physics::Duration getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (Duration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::Duration {lvalue},ad::physics::Duration)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Duration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Duration {lvalue},ad::physics::Duration)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (Duration)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::Duration {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (Duration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::Duration {lvalue},ad::physics::Duration)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (Duration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::Duration {lvalue},ad::physics::Duration)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::Duration&>,ad::physics::Duration)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::Duration&>,ad::physics::Duration)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (Duration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::Duration {lvalue},ad::physics::Duration)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (Duration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::Duration {lvalue},ad::physics::Duration)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (Duration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Duration {lvalue},ad::physics::Duration)

        __mul__( (Duration)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Duration {lvalue},double)

        __mul__( (Duration)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Duration {lvalue},ad::physics::ParametricValue)

        __mul__( (Duration)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Duration {lvalue},ad::physics::AngularVelocity)

        __mul__( (Duration)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Duration {lvalue},ad::physics::AngularAcceleration)

        __mul__( (Duration)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Duration {lvalue},ad::physics::Acceleration)

        __mul__( (Duration)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Duration {lvalue},ad::physics::Speed)

        __mul__( (Duration)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Duration {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Duration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Duration {lvalue},ad::physics::Duration)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (Duration)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::Duration {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (Duration)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::Duration {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (Duration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::Duration {lvalue},ad::physics::Duration)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (Duration)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Duration {lvalue},double)

        __truediv__( (Duration)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Duration {lvalue},ad::physics::Duration)

        __truediv__( (Duration)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Duration {lvalue},ad::physics::ParametricValue)

        __truediv__( (Duration)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Duration {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class DurationList(Boost.Python.instance):
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
        append( (DurationList)arg1, (Duration)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},ad::physics::Duration)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (DurationList)arg1, (Duration)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},ad::physics::Duration)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (DurationList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (DurationList)arg1, (Duration)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},ad::physics::Duration)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (DurationList)arg1, (int)arg2, (Duration)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},long,ad::physics::Duration)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (DurationList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (DurationList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (DurationList)arg1, (Duration)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},ad::physics::Duration)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (DurationList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},long)

        __delitem__( (DurationList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (DurationList)arg1, (int)arg2) -> Duration :

            C++ signature :
                ad::physics::Duration {lvalue} __getitem__(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},long)

        __getitem__( (DurationList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (DurationList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (DurationList)arg1, (int)arg2, (Duration)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},long,ad::physics::Duration)

        __setitem__( (DurationList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class DurationSquared(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iDurationSquared) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (DurationSquared)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::DurationSquared)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (DurationSquared)arg1, (DurationSquared)other) -> DurationSquared :

            C++ signature :
                ad::physics::DurationSquared {lvalue} assign(ad::physics::DurationSquared {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (DurationSquared)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::DurationSquared {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (DurationSquared)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::DurationSquared {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> DurationSquared :

            C++ signature :
                ad::physics::DurationSquared getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> DurationSquared :

            C++ signature :
                ad::physics::DurationSquared getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> DurationSquared :

            C++ signature :
                ad::physics::DurationSquared getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (DurationSquared)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::DurationSquared {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (DurationSquared)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::DurationSquared {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (DurationSquared)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::DurationSquared {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (DurationSquared)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::DurationSquared {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (DurationSquared)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::DurationSquared {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::DurationSquared&>,ad::physics::DurationSquared)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::DurationSquared&>,ad::physics::DurationSquared)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (DurationSquared)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::DurationSquared {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (DurationSquared)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::DurationSquared {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (DurationSquared)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::DurationSquared {lvalue},double)

        __mul__( (DurationSquared)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::DurationSquared {lvalue},ad::physics::ParametricValue)

        __mul__( (DurationSquared)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::DurationSquared {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (DurationSquared)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::DurationSquared {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (DurationSquared)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::DurationSquared {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (DurationSquared)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::DurationSquared {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (DurationSquared)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::DurationSquared {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (DurationSquared)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::DurationSquared {lvalue},double)

        __truediv__( (DurationSquared)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::DurationSquared {lvalue},ad::physics::DurationSquared)

        __truediv__( (DurationSquared)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::DurationSquared {lvalue},ad::physics::ParametricValue)

        __truediv__( (DurationSquared)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::DurationSquared {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class DurationSquaredList(Boost.Python.instance):
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
        append( (DurationSquaredList)arg1, (DurationSquared)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (DurationSquaredList)arg1, (DurationSquared)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (DurationSquaredList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (DurationSquaredList)arg1, (DurationSquared)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (DurationSquaredList)arg1, (int)arg2, (DurationSquared)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},long,ad::physics::DurationSquared)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (DurationSquaredList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (DurationSquaredList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (DurationSquaredList)arg1, (DurationSquared)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},ad::physics::DurationSquared)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (DurationSquaredList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},long)

        __delitem__( (DurationSquaredList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (DurationSquaredList)arg1, (int)arg2) -> DurationSquared :

            C++ signature :
                ad::physics::DurationSquared {lvalue} __getitem__(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},long)

        __getitem__( (DurationSquaredList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (DurationSquaredList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (DurationSquaredList)arg1, (int)arg2, (DurationSquared)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},long,ad::physics::DurationSquared)

        __setitem__( (DurationSquaredList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class MetricRange(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    maximum: Incomplete
    minimum: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (MetricRange)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::MetricRange)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (MetricRange)arg1, (MetricRange)other) -> MetricRange :

            C++ signature :
                ad::physics::MetricRange {lvalue} assign(ad::physics::MetricRange {lvalue},ad::physics::MetricRange)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (MetricRange)arg1, (MetricRange)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::MetricRange {lvalue},ad::physics::MetricRange)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (MetricRange)arg1, (MetricRange)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::MetricRange {lvalue},ad::physics::MetricRange)"""
    @classmethod
    def __reduce__(cls): ...

class MetricRangeList(Boost.Python.instance):
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
        append( (MetricRangeList)arg1, (MetricRange)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},ad::physics::MetricRange)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (MetricRangeList)arg1, (MetricRange)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},ad::physics::MetricRange)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (MetricRangeList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (MetricRangeList)arg1, (MetricRange)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},ad::physics::MetricRange)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (MetricRangeList)arg1, (int)arg2, (MetricRange)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},long,ad::physics::MetricRange)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (MetricRangeList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (MetricRangeList)arg1, (MetricRange)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},ad::physics::MetricRange)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (MetricRangeList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},long)

        __delitem__( (MetricRangeList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (MetricRangeList)arg1, (int)arg2) -> MetricRange :

            C++ signature :
                ad::physics::MetricRange {lvalue} __getitem__(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},long)

        __getitem__( (MetricRangeList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (MetricRangeList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (MetricRangeList)arg1, (int)arg2, (MetricRange)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},long,ad::physics::MetricRange)

        __setitem__( (MetricRangeList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class ParametricRange(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    maximum: Incomplete
    minimum: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (ParametricRange)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::ParametricRange)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ParametricRange)arg1, (ParametricRange)other) -> ParametricRange :

            C++ signature :
                ad::physics::ParametricRange {lvalue} assign(ad::physics::ParametricRange {lvalue},ad::physics::ParametricRange)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ParametricRange)arg1, (ParametricRange)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::ParametricRange {lvalue},ad::physics::ParametricRange)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ParametricRange)arg1, (ParametricRange)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::ParametricRange {lvalue},ad::physics::ParametricRange)"""
    @classmethod
    def __reduce__(cls): ...

class ParametricRangeList(Boost.Python.instance):
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
        append( (ParametricRangeList)arg1, (ParametricRange)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},ad::physics::ParametricRange)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ParametricRangeList)arg1, (ParametricRange)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},ad::physics::ParametricRange)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ParametricRangeList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ParametricRangeList)arg1, (ParametricRange)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},ad::physics::ParametricRange)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ParametricRangeList)arg1, (int)arg2, (ParametricRange)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},long,ad::physics::ParametricRange)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ParametricRangeList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ParametricRangeList)arg1, (ParametricRange)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},ad::physics::ParametricRange)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ParametricRangeList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},long)

        __delitem__( (ParametricRangeList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ParametricRangeList)arg1, (int)arg2) -> ParametricRange :

            C++ signature :
                ad::physics::ParametricRange {lvalue} __getitem__(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},long)

        __getitem__( (ParametricRangeList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ParametricRangeList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ParametricRangeList)arg1, (int)arg2, (ParametricRange)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},long,ad::physics::ParametricRange)

        __setitem__( (ParametricRangeList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class ParametricValue(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iParametricValue) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (ParametricValue)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::ParametricValue)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ParametricValue)arg1, (ParametricValue)other) -> ParametricValue :

            C++ signature :
                ad::physics::ParametricValue {lvalue} assign(ad::physics::ParametricValue {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (ParametricValue)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::ParametricValue {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (ParametricValue)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::ParametricValue {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> ParametricValue :

            C++ signature :
                ad::physics::ParametricValue getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> ParametricValue :

            C++ signature :
                ad::physics::ParametricValue getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> ParametricValue :

            C++ signature :
                ad::physics::ParametricValue getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (ParametricValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::ParametricValue {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ParametricValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::ParametricValue {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (ParametricValue)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::ParametricValue {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (ParametricValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::ParametricValue {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (ParametricValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::ParametricValue {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::ParametricValue&>,ad::physics::ParametricValue)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::ParametricValue&>,ad::physics::ParametricValue)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (ParametricValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::ParametricValue {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (ParametricValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::ParametricValue {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (ParametricValue)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},double)

        __mul__( (ParametricValue)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::Acceleration)

        __mul__( (ParametricValue)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::Angle)

        __mul__( (ParametricValue)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::AngularAcceleration)

        __mul__( (ParametricValue)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::AngularVelocity)

        __mul__( (ParametricValue)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::Distance)

        __mul__( (ParametricValue)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::DistanceSquared)

        __mul__( (ParametricValue)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::Duration)

        __mul__( (ParametricValue)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::DurationSquared)

        __mul__( (ParametricValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::ParametricValue)

        __mul__( (ParametricValue)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::Probability)

        __mul__( (ParametricValue)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::Speed)

        __mul__( (ParametricValue)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::SpeedSquared)

        __mul__( (ParametricValue)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::Weight)

        __mul__( (ParametricValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::ParametricValue {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ParametricValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::ParametricValue {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (ParametricValue)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::ParametricValue {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (ParametricValue)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::ParametricValue {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (ParametricValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::ParametricValue {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (ParametricValue)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::ParametricValue {lvalue},double)

        __truediv__( (ParametricValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::ParametricValue {lvalue},ad::physics::ParametricValue)

        __truediv__( (ParametricValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::ParametricValue {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class ParametricValueList(Boost.Python.instance):
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
        append( (ParametricValueList)arg1, (ParametricValue)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ParametricValueList)arg1, (ParametricValue)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ParametricValueList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ParametricValueList)arg1, (ParametricValue)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ParametricValueList)arg1, (int)arg2, (ParametricValue)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},long,ad::physics::ParametricValue)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ParametricValueList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (ParametricValueList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ParametricValueList)arg1, (ParametricValue)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},ad::physics::ParametricValue)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ParametricValueList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},long)

        __delitem__( (ParametricValueList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ParametricValueList)arg1, (int)arg2) -> ParametricValue :

            C++ signature :
                ad::physics::ParametricValue {lvalue} __getitem__(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},long)

        __getitem__( (ParametricValueList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ParametricValueList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ParametricValueList)arg1, (int)arg2, (ParametricValue)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},long,ad::physics::ParametricValue)

        __setitem__( (ParametricValueList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Probability(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iProbability) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (Probability)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Probability)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Probability)arg1, (Probability)other) -> Probability :

            C++ signature :
                ad::physics::Probability {lvalue} assign(ad::physics::Probability {lvalue},ad::physics::Probability)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (Probability)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::Probability {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (Probability)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::Probability {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> Probability :

            C++ signature :
                ad::physics::Probability getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> Probability :

            C++ signature :
                ad::physics::Probability getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> Probability :

            C++ signature :
                ad::physics::Probability getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (Probability)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::Probability {lvalue},ad::physics::Probability)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Probability)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Probability {lvalue},ad::physics::Probability)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (Probability)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::Probability {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (Probability)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::Probability {lvalue},ad::physics::Probability)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (Probability)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::Probability {lvalue},ad::physics::Probability)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::Probability&>,ad::physics::Probability)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::Probability&>,ad::physics::Probability)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (Probability)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::Probability {lvalue},ad::physics::Probability)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (Probability)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::Probability {lvalue},ad::physics::Probability)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (Probability)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Probability {lvalue},double)

        __mul__( (Probability)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Probability {lvalue},ad::physics::ParametricValue)

        __mul__( (Probability)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Probability {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Probability)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Probability {lvalue},ad::physics::Probability)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (Probability)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::Probability {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (Probability)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::Probability {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (Probability)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::Probability {lvalue},ad::physics::Probability)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (Probability)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Probability {lvalue},double)

        __truediv__( (Probability)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Probability {lvalue},ad::physics::Probability)

        __truediv__( (Probability)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Probability {lvalue},ad::physics::ParametricValue)

        __truediv__( (Probability)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Probability {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class ProbabilityList(Boost.Python.instance):
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
        append( (ProbabilityList)arg1, (Probability)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},ad::physics::Probability)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ProbabilityList)arg1, (Probability)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},ad::physics::Probability)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ProbabilityList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ProbabilityList)arg1, (Probability)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},ad::physics::Probability)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ProbabilityList)arg1, (int)arg2, (Probability)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},long,ad::physics::Probability)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ProbabilityList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (ProbabilityList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ProbabilityList)arg1, (Probability)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},ad::physics::Probability)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ProbabilityList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},long)

        __delitem__( (ProbabilityList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ProbabilityList)arg1, (int)arg2) -> Probability :

            C++ signature :
                ad::physics::Probability {lvalue} __getitem__(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},long)

        __getitem__( (ProbabilityList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ProbabilityList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ProbabilityList)arg1, (int)arg2, (Probability)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},long,ad::physics::Probability)

        __setitem__( (ProbabilityList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class RatioValue(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iRatioValue) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (RatioValue)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::RatioValue)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (RatioValue)arg1, (RatioValue)other) -> RatioValue :

            C++ signature :
                ad::physics::RatioValue {lvalue} assign(ad::physics::RatioValue {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (RatioValue)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::RatioValue {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (RatioValue)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::RatioValue {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> RatioValue :

            C++ signature :
                ad::physics::RatioValue getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> RatioValue :

            C++ signature :
                ad::physics::RatioValue getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> RatioValue :

            C++ signature :
                ad::physics::RatioValue getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (RatioValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::RatioValue {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (RatioValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::RatioValue {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (RatioValue)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::RatioValue {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (RatioValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::RatioValue {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (RatioValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::RatioValue {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::RatioValue&>,ad::physics::RatioValue)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::RatioValue&>,ad::physics::RatioValue)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (RatioValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::RatioValue {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (RatioValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::RatioValue {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (RatioValue)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},double)

        __mul__( (RatioValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::ParametricValue)

        __mul__( (RatioValue)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::Acceleration)

        __mul__( (RatioValue)arg1, (Angle)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::Angle)

        __mul__( (RatioValue)arg1, (AngularAcceleration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::AngularAcceleration)

        __mul__( (RatioValue)arg1, (AngularVelocity)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::AngularVelocity)

        __mul__( (RatioValue)arg1, (Distance)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::Distance)

        __mul__( (RatioValue)arg1, (DistanceSquared)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::DistanceSquared)

        __mul__( (RatioValue)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::Duration)

        __mul__( (RatioValue)arg1, (DurationSquared)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::DurationSquared)

        __mul__( (RatioValue)arg1, (Probability)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::Probability)

        __mul__( (RatioValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::RatioValue)

        __mul__( (RatioValue)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::Speed)

        __mul__( (RatioValue)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::SpeedSquared)

        __mul__( (RatioValue)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::RatioValue {lvalue},ad::physics::Weight)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (RatioValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::RatioValue {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (RatioValue)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::RatioValue {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (RatioValue)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::RatioValue {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (RatioValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::RatioValue {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (RatioValue)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::RatioValue {lvalue},double)

        __truediv__( (RatioValue)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::RatioValue {lvalue},ad::physics::RatioValue)

        __truediv__( (RatioValue)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::RatioValue {lvalue},ad::physics::ParametricValue)"""
    @property
    def Valid(self): ...

class RatioValueList(Boost.Python.instance):
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
        append( (RatioValueList)arg1, (RatioValue)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (RatioValueList)arg1, (RatioValue)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (RatioValueList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (RatioValueList)arg1, (RatioValue)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (RatioValueList)arg1, (int)arg2, (RatioValue)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},long,ad::physics::RatioValue)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (RatioValueList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (RatioValueList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (RatioValueList)arg1, (RatioValue)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (RatioValueList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},long)

        __delitem__( (RatioValueList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (RatioValueList)arg1, (int)arg2) -> RatioValue :

            C++ signature :
                ad::physics::RatioValue {lvalue} __getitem__(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},long)

        __getitem__( (RatioValueList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (RatioValueList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (RatioValueList)arg1, (int)arg2, (RatioValue)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},long,ad::physics::RatioValue)

        __setitem__( (RatioValueList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Speed(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iSpeed) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (Speed)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Speed)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Speed)arg1, (Speed)other) -> Speed :

            C++ signature :
                ad::physics::Speed {lvalue} assign(ad::physics::Speed {lvalue},ad::physics::Speed)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (Speed)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::Speed {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (Speed)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::Speed {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> Speed :

            C++ signature :
                ad::physics::Speed getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> Speed :

            C++ signature :
                ad::physics::Speed getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> Speed :

            C++ signature :
                ad::physics::Speed getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (Speed)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::Speed {lvalue},ad::physics::Speed)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Speed)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Speed {lvalue},ad::physics::Speed)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (Speed)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::Speed {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (Speed)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::Speed {lvalue},ad::physics::Speed)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (Speed)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::Speed {lvalue},ad::physics::Speed)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::Speed&>,ad::physics::Speed)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::Speed&>,ad::physics::Speed)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (Speed)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::Speed {lvalue},ad::physics::Speed)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (Speed)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::Speed {lvalue},ad::physics::Speed)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (Speed)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Speed {lvalue},ad::physics::Speed)

        __mul__( (Speed)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Speed {lvalue},double)

        __mul__( (Speed)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Speed {lvalue},ad::physics::ParametricValue)

        __mul__( (Speed)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Speed {lvalue},ad::physics::Duration)

        __mul__( (Speed)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Speed {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Speed)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Speed {lvalue},ad::physics::Speed)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (Speed)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::Speed {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (Speed)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::Speed {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (Speed)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::Speed {lvalue},ad::physics::Speed)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (Speed)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Speed {lvalue},double)

        __truediv__( (Speed)arg1, (Speed)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Speed {lvalue},ad::physics::Speed)

        __truediv__( (Speed)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Speed {lvalue},ad::physics::ParametricValue)

        __truediv__( (Speed)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Speed {lvalue},ad::physics::Acceleration)

        __truediv__( (Speed)arg1, (Duration)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Speed {lvalue},ad::physics::Duration)

        __truediv__( (Speed)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Speed {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class SpeedList(Boost.Python.instance):
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
        append( (SpeedList)arg1, (Speed)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},ad::physics::Speed)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (SpeedList)arg1, (Speed)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},ad::physics::Speed)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (SpeedList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (SpeedList)arg1, (Speed)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},ad::physics::Speed)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (SpeedList)arg1, (int)arg2, (Speed)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},long,ad::physics::Speed)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (SpeedList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (SpeedList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (SpeedList)arg1, (Speed)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},ad::physics::Speed)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (SpeedList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},long)

        __delitem__( (SpeedList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (SpeedList)arg1, (int)arg2) -> Speed :

            C++ signature :
                ad::physics::Speed {lvalue} __getitem__(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},long)

        __getitem__( (SpeedList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (SpeedList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (SpeedList)arg1, (int)arg2, (Speed)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},long,ad::physics::Speed)

        __setitem__( (SpeedList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class SpeedRange(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    maximum: Incomplete
    minimum: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (SpeedRange)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::SpeedRange)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (SpeedRange)arg1, (SpeedRange)other) -> SpeedRange :

            C++ signature :
                ad::physics::SpeedRange {lvalue} assign(ad::physics::SpeedRange {lvalue},ad::physics::SpeedRange)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (SpeedRange)arg1, (SpeedRange)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::SpeedRange {lvalue},ad::physics::SpeedRange)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (SpeedRange)arg1, (SpeedRange)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::SpeedRange {lvalue},ad::physics::SpeedRange)"""
    @classmethod
    def __reduce__(cls): ...

class SpeedRangeList(Boost.Python.instance):
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
        append( (SpeedRangeList)arg1, (SpeedRange)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},ad::physics::SpeedRange)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (SpeedRangeList)arg1, (SpeedRange)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},ad::physics::SpeedRange)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (SpeedRangeList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (SpeedRangeList)arg1, (SpeedRange)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},ad::physics::SpeedRange)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (SpeedRangeList)arg1, (int)arg2, (SpeedRange)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},long,ad::physics::SpeedRange)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (SpeedRangeList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (SpeedRangeList)arg1, (SpeedRange)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},ad::physics::SpeedRange)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (SpeedRangeList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},long)

        __delitem__( (SpeedRangeList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (SpeedRangeList)arg1, (int)arg2) -> SpeedRange :

            C++ signature :
                ad::physics::SpeedRange {lvalue} __getitem__(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},long)

        __getitem__( (SpeedRangeList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (SpeedRangeList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (SpeedRangeList)arg1, (int)arg2, (SpeedRange)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},long,ad::physics::SpeedRange)

        __setitem__( (SpeedRangeList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class SpeedSquared(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iSpeedSquared) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (SpeedSquared)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::SpeedSquared)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (SpeedSquared)arg1, (SpeedSquared)other) -> SpeedSquared :

            C++ signature :
                ad::physics::SpeedSquared {lvalue} assign(ad::physics::SpeedSquared {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (SpeedSquared)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::SpeedSquared {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (SpeedSquared)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::SpeedSquared {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> SpeedSquared :

            C++ signature :
                ad::physics::SpeedSquared getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> SpeedSquared :

            C++ signature :
                ad::physics::SpeedSquared getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> SpeedSquared :

            C++ signature :
                ad::physics::SpeedSquared getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (SpeedSquared)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::SpeedSquared {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (SpeedSquared)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::SpeedSquared {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (SpeedSquared)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::SpeedSquared {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (SpeedSquared)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::SpeedSquared {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (SpeedSquared)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::SpeedSquared {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::SpeedSquared&>,ad::physics::SpeedSquared)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::SpeedSquared&>,ad::physics::SpeedSquared)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (SpeedSquared)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::SpeedSquared {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (SpeedSquared)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::SpeedSquared {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (SpeedSquared)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::SpeedSquared {lvalue},double)

        __mul__( (SpeedSquared)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::SpeedSquared {lvalue},ad::physics::ParametricValue)

        __mul__( (SpeedSquared)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::SpeedSquared {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (SpeedSquared)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::SpeedSquared {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (SpeedSquared)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::SpeedSquared {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (SpeedSquared)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::SpeedSquared {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (SpeedSquared)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::SpeedSquared {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (SpeedSquared)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::SpeedSquared {lvalue},double)

        __truediv__( (SpeedSquared)arg1, (SpeedSquared)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::SpeedSquared {lvalue},ad::physics::SpeedSquared)

        __truediv__( (SpeedSquared)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::SpeedSquared {lvalue},ad::physics::ParametricValue)

        __truediv__( (SpeedSquared)arg1, (Acceleration)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::SpeedSquared {lvalue},ad::physics::Acceleration)

        __truediv__( (SpeedSquared)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::SpeedSquared {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class SpeedSquaredList(Boost.Python.instance):
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
        append( (SpeedSquaredList)arg1, (SpeedSquared)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (SpeedSquaredList)arg1, (SpeedSquared)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (SpeedSquaredList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (SpeedSquaredList)arg1, (SpeedSquared)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (SpeedSquaredList)arg1, (int)arg2, (SpeedSquared)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},long,ad::physics::SpeedSquared)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (SpeedSquaredList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (SpeedSquaredList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (SpeedSquaredList)arg1, (SpeedSquared)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},ad::physics::SpeedSquared)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (SpeedSquaredList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},long)

        __delitem__( (SpeedSquaredList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (SpeedSquaredList)arg1, (int)arg2) -> SpeedSquared :

            C++ signature :
                ad::physics::SpeedSquared {lvalue} __getitem__(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},long)

        __getitem__( (SpeedSquaredList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (SpeedSquaredList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (SpeedSquaredList)arg1, (int)arg2, (SpeedSquared)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},long,ad::physics::SpeedSquared)

        __setitem__( (SpeedSquaredList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Velocity(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    x: Incomplete
    y: Incomplete
    z: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Velocity)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Velocity)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Velocity)arg1, (Velocity)other) -> Velocity :

            C++ signature :
                ad::physics::Velocity {lvalue} assign(ad::physics::Velocity {lvalue},ad::physics::Velocity)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Velocity)arg1, (Velocity)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Velocity {lvalue},ad::physics::Velocity)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Velocity)arg1, (Velocity)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Velocity {lvalue},ad::physics::Velocity)"""
    @classmethod
    def __reduce__(cls): ...

class VelocityList(Boost.Python.instance):
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
        append( (VelocityList)arg1, (Velocity)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},ad::physics::Velocity)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (VelocityList)arg1, (Velocity)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},ad::physics::Velocity)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (VelocityList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (VelocityList)arg1, (Velocity)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},ad::physics::Velocity)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (VelocityList)arg1, (int)arg2, (Velocity)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},long,ad::physics::Velocity)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (VelocityList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (VelocityList)arg1, (Velocity)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},ad::physics::Velocity)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (VelocityList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},long)

        __delitem__( (VelocityList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (VelocityList)arg1, (int)arg2) -> Velocity :

            C++ signature :
                ad::physics::Velocity {lvalue} __getitem__(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},long)

        __getitem__( (VelocityList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (VelocityList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (VelocityList)arg1, (int)arg2, (Velocity)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},long,ad::physics::Velocity)

        __setitem__( (VelocityList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Weight(Boost.Python.instance):
    cMaxValue: ClassVar[float] = ...  # read-only
    cMinValue: ClassVar[float] = ...  # read-only
    cPrecisionValue: ClassVar[float] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iWeight) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (Weight)other) -> None :

            C++ signature :
                void __init__(_object*,ad::physics::Weight)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Weight)arg1, (Weight)other) -> Weight :

            C++ signature :
                ad::physics::Weight {lvalue} assign(ad::physics::Weight {lvalue},ad::physics::Weight)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (Weight)arg1) -> None :

            C++ signature :
                void ensureValid(ad::physics::Weight {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (Weight)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::physics::Weight {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> Weight :

            C++ signature :
                ad::physics::Weight getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> Weight :

            C++ signature :
                ad::physics::Weight getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> Weight :

            C++ signature :
                ad::physics::Weight getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (Weight)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __add__(ad::physics::Weight {lvalue},ad::physics::Weight)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Weight)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::physics::Weight {lvalue},ad::physics::Weight)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (Weight)arg1) -> float :

            C++ signature :
                double __float__(ad::physics::Weight {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (Weight)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::physics::Weight {lvalue},ad::physics::Weight)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (Weight)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::physics::Weight {lvalue},ad::physics::Weight)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::physics::Weight&>,ad::physics::Weight)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::physics::Weight&>,ad::physics::Weight)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (Weight)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __le__(ad::physics::Weight {lvalue},ad::physics::Weight)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (Weight)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::physics::Weight {lvalue},ad::physics::Weight)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (Weight)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Weight {lvalue},double)

        __mul__( (Weight)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Weight {lvalue},ad::physics::ParametricValue)

        __mul__( (Weight)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::physics::Weight {lvalue},ad::physics::RatioValue)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Weight)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::physics::Weight {lvalue},ad::physics::Weight)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (Weight)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::physics::Weight {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __rmul__(cls, ad, double) -> Any:
        """
        __rmul__( (Weight)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __rmul__(ad::physics::Weight {lvalue},double)"""
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (Weight)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::physics::Weight {lvalue},ad::physics::Weight)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (Weight)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Weight {lvalue},double)

        __truediv__( (Weight)arg1, (Weight)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Weight {lvalue},ad::physics::Weight)

        __truediv__( (Weight)arg1, (ParametricValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Weight {lvalue},ad::physics::ParametricValue)

        __truediv__( (Weight)arg1, (RatioValue)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::physics::Weight {lvalue},ad::physics::RatioValue)"""
    @property
    def Valid(self): ...

class WeightList(Boost.Python.instance):
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
        append( (WeightList)arg1, (Weight)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},ad::physics::Weight)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (WeightList)arg1, (Weight)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},ad::physics::Weight)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (WeightList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (WeightList)arg1, (Weight)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},ad::physics::Weight)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (WeightList)arg1, (int)arg2, (Weight)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},long,ad::physics::Weight)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (WeightList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (WeightList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (WeightList)arg1, (Weight)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},ad::physics::Weight)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (WeightList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},long)

        __delitem__( (WeightList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (WeightList)arg1, (int)arg2) -> Weight :

            C++ signature :
                ad::physics::Weight {lvalue} __getitem__(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},long)

        __getitem__( (WeightList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (WeightList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (WeightList)arg1, (int)arg2, (Weight)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},long,ad::physics::Weight)

        __setitem__( (WeightList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class numeric_limits_less__ad_scope_physics_scope_Acceleration__greater_(Boost.Python.instance):
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
        epsilon() -> Acceleration :

            C++ signature :
                ad::physics::Acceleration epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> Acceleration :

            C++ signature :
                ad::physics::Acceleration lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> Acceleration :

            C++ signature :
                ad::physics::Acceleration max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_Angle__greater_(Boost.Python.instance):
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
        epsilon() -> Angle :

            C++ signature :
                ad::physics::Angle epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> Angle :

            C++ signature :
                ad::physics::Angle lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> Angle :

            C++ signature :
                ad::physics::Angle max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_AngularAcceleration__greater_(Boost.Python.instance):
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
        epsilon() -> AngularAcceleration :

            C++ signature :
                ad::physics::AngularAcceleration epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> AngularAcceleration :

            C++ signature :
                ad::physics::AngularAcceleration lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> AngularAcceleration :

            C++ signature :
                ad::physics::AngularAcceleration max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_AngularVelocity__greater_(Boost.Python.instance):
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
        epsilon() -> AngularVelocity :

            C++ signature :
                ad::physics::AngularVelocity epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> AngularVelocity :

            C++ signature :
                ad::physics::AngularVelocity lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> AngularVelocity :

            C++ signature :
                ad::physics::AngularVelocity max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_DistanceSquared__greater_(Boost.Python.instance):
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
        epsilon() -> DistanceSquared :

            C++ signature :
                ad::physics::DistanceSquared epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> DistanceSquared :

            C++ signature :
                ad::physics::DistanceSquared lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> DistanceSquared :

            C++ signature :
                ad::physics::DistanceSquared max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_Distance__greater_(Boost.Python.instance):
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
        epsilon() -> Distance :

            C++ signature :
                ad::physics::Distance epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> Distance :

            C++ signature :
                ad::physics::Distance lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> Distance :

            C++ signature :
                ad::physics::Distance max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_DurationSquared__greater_(Boost.Python.instance):
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
        epsilon() -> DurationSquared :

            C++ signature :
                ad::physics::DurationSquared epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> DurationSquared :

            C++ signature :
                ad::physics::DurationSquared lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> DurationSquared :

            C++ signature :
                ad::physics::DurationSquared max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_Duration__greater_(Boost.Python.instance):
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
        epsilon() -> Duration :

            C++ signature :
                ad::physics::Duration epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> Duration :

            C++ signature :
                ad::physics::Duration lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> Duration :

            C++ signature :
                ad::physics::Duration max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_ParametricValue__greater_(Boost.Python.instance):
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
        epsilon() -> ParametricValue :

            C++ signature :
                ad::physics::ParametricValue epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> ParametricValue :

            C++ signature :
                ad::physics::ParametricValue lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> ParametricValue :

            C++ signature :
                ad::physics::ParametricValue max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_Probability__greater_(Boost.Python.instance):
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
        epsilon() -> Probability :

            C++ signature :
                ad::physics::Probability epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> Probability :

            C++ signature :
                ad::physics::Probability lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> Probability :

            C++ signature :
                ad::physics::Probability max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_RatioValue__greater_(Boost.Python.instance):
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
        epsilon() -> RatioValue :

            C++ signature :
                ad::physics::RatioValue epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> RatioValue :

            C++ signature :
                ad::physics::RatioValue lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> RatioValue :

            C++ signature :
                ad::physics::RatioValue max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_SpeedSquared__greater_(Boost.Python.instance):
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
        epsilon() -> SpeedSquared :

            C++ signature :
                ad::physics::SpeedSquared epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> SpeedSquared :

            C++ signature :
                ad::physics::SpeedSquared lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> SpeedSquared :

            C++ signature :
                ad::physics::SpeedSquared max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_Speed__greater_(Boost.Python.instance):
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
        epsilon() -> Speed :

            C++ signature :
                ad::physics::Speed epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> Speed :

            C++ signature :
                ad::physics::Speed lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> Speed :

            C++ signature :
                ad::physics::Speed max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_physics_scope_Weight__greater_(Boost.Python.instance):
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
        epsilon() -> Weight :

            C++ signature :
                ad::physics::Weight epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> Weight :

            C++ signature :
                ad::physics::Weight lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> Weight :

            C++ signature :
                ad::physics::Weight max()"""
    @classmethod
    def __reduce__(cls): ...

@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (DistanceSquared)other) -> DistanceSquared :

        C++ signature :
            ad::physics::DistanceSquared fabs(ad::physics::DistanceSquared)

    fabs( (Acceleration)other) -> Acceleration :

        C++ signature :
            ad::physics::Acceleration fabs(ad::physics::Acceleration)

    fabs( (DurationSquared)other) -> DurationSquared :

        C++ signature :
            ad::physics::DurationSquared fabs(ad::physics::DurationSquared)

    fabs( (Speed)other) -> Speed :

        C++ signature :
            ad::physics::Speed fabs(ad::physics::Speed)

    fabs( (Weight)other) -> Weight :

        C++ signature :
            ad::physics::Weight fabs(ad::physics::Weight)

    fabs( (Duration)other) -> Duration :

        C++ signature :
            ad::physics::Duration fabs(ad::physics::Duration)

    fabs( (Distance)other) -> Distance :

        C++ signature :
            ad::physics::Distance fabs(ad::physics::Distance)

    fabs( (AngularAcceleration)other) -> AngularAcceleration :

        C++ signature :
            ad::physics::AngularAcceleration fabs(ad::physics::AngularAcceleration)

    fabs( (ParametricValue)other) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue fabs(ad::physics::ParametricValue)

    fabs( (Probability)other) -> Probability :

        C++ signature :
            ad::physics::Probability fabs(ad::physics::Probability)

    fabs( (SpeedSquared)other) -> SpeedSquared :

        C++ signature :
            ad::physics::SpeedSquared fabs(ad::physics::SpeedSquared)

    fabs( (Angle)other) -> Angle :

        C++ signature :
            ad::physics::Angle fabs(ad::physics::Angle)

    fabs( (RatioValue)other) -> RatioValue :

        C++ signature :
            ad::physics::RatioValue fabs(ad::physics::RatioValue)

    fabs( (AngularVelocity)other) -> AngularVelocity :

        C++ signature :
            ad::physics::AngularVelocity fabs(ad::physics::AngularVelocity)"""
def normalizeAngle(ad) -> Any:
    """
    normalizeAngle( (Angle)angle) -> Angle :

        C++ signature :
            ad::physics::Angle normalizeAngle(ad::physics::Angle)"""
def normalizeAngleSigned(ad) -> Any:
    """
    normalizeAngleSigned( (Angle)angle) -> Angle :

        C++ signature :
            ad::physics::Angle normalizeAngleSigned(ad::physics::Angle)"""
@overload
def sqrt(ad) -> Any:
    """
    sqrt( (DistanceSquared)other) -> Distance :

        C++ signature :
            ad::physics::Distance sqrt(ad::physics::DistanceSquared)

    sqrt( (DurationSquared)other) -> Duration :

        C++ signature :
            ad::physics::Duration sqrt(ad::physics::DurationSquared)

    sqrt( (SpeedSquared)other) -> Speed :

        C++ signature :
            ad::physics::Speed sqrt(ad::physics::SpeedSquared)"""
@overload
def sqrt(ad) -> Any:
    """
    sqrt( (DistanceSquared)other) -> Distance :

        C++ signature :
            ad::physics::Distance sqrt(ad::physics::DistanceSquared)

    sqrt( (DurationSquared)other) -> Duration :

        C++ signature :
            ad::physics::Duration sqrt(ad::physics::DurationSquared)

    sqrt( (SpeedSquared)other) -> Speed :

        C++ signature :
            ad::physics::Speed sqrt(ad::physics::SpeedSquared)"""
@overload
def sqrt(ad) -> Any:
    """
    sqrt( (DistanceSquared)other) -> Distance :

        C++ signature :
            ad::physics::Distance sqrt(ad::physics::DistanceSquared)

    sqrt( (DurationSquared)other) -> Duration :

        C++ signature :
            ad::physics::Duration sqrt(ad::physics::DurationSquared)

    sqrt( (SpeedSquared)other) -> Speed :

        C++ signature :
            ad::physics::Speed sqrt(ad::physics::SpeedSquared)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (DistanceSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DistanceSquared)

    to_string( (Acceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration)

    to_string( (AccelerationRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AccelerationRange)

    to_string( (AccelerationRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AccelerationRange, std::allocator<ad::physics::AccelerationRange> >)

    to_string( (DurationSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::DurationSquared)

    to_string( (Speed)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Speed)

    to_string( (SpeedRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedRange)

    to_string( (SpeedRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedRange, std::allocator<ad::physics::SpeedRange> >)

    to_string( (Weight)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Weight)

    to_string( (WeightList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Weight, std::allocator<ad::physics::Weight> >)

    to_string( (Duration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Duration)

    to_string( (DurationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Duration, std::allocator<ad::physics::Duration> >)

    to_string( (Distance)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance)

    to_string( (Dimension2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension2D)

    to_string( (Dimension2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension2D, std::allocator<ad::physics::Dimension2D> >)

    to_string( (MetricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::MetricRange)

    to_string( (MetricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::MetricRange, std::allocator<ad::physics::MetricRange> >)

    to_string( (AngularAcceleration)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularAcceleration)

    to_string( (AngularAccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularAcceleration, std::allocator<ad::physics::AngularAcceleration> >)

    to_string( (ParametricValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricValue)

    to_string( (ParametricValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricValue, std::allocator<ad::physics::ParametricValue> >)

    to_string( (Velocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Velocity)

    to_string( (SpeedList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Speed, std::allocator<ad::physics::Speed> >)

    to_string( (Probability)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Probability)

    to_string( (SpeedSquared)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::SpeedSquared)

    to_string( (SpeedSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::SpeedSquared, std::allocator<ad::physics::SpeedSquared> >)

    to_string( (ParametricRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::ParametricRange)

    to_string( (ParametricRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::ParametricRange, std::allocator<ad::physics::ParametricRange> >)

    to_string( (Distance2D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance2D)

    to_string( (AccelerationList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration, std::allocator<ad::physics::Acceleration> >)

    to_string( (Angle)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Angle)

    to_string( (AngleRange)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngleRange)

    to_string( (RatioValue)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::RatioValue)

    to_string( (RatioValueList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::RatioValue, std::allocator<ad::physics::RatioValue> >)

    to_string( (AngularVelocity)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity)

    to_string( (AngularVelocity3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::AngularVelocity3D)

    to_string( (AngularVelocity3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity3D, std::allocator<ad::physics::AngularVelocity3D> >)

    to_string( (DistanceSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DistanceSquared, std::allocator<ad::physics::DistanceSquared> >)

    to_string( (Distance3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Distance3D)

    to_string( (Distance2DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)

    to_string( (VelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Velocity, std::allocator<ad::physics::Velocity> >)

    to_string( (AngleRangeList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngleRange, std::allocator<ad::physics::AngleRange> >)

    to_string( (DistanceList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance, std::allocator<ad::physics::Distance> >)

    to_string( (DurationSquaredList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::DurationSquared, std::allocator<ad::physics::DurationSquared> >)

    to_string( (Distance3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Distance3D, std::allocator<ad::physics::Distance3D> >)

    to_string( (AngleList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Angle, std::allocator<ad::physics::Angle> >)

    to_string( (AngularVelocityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::AngularVelocity, std::allocator<ad::physics::AngularVelocity> >)

    to_string( (Acceleration3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Acceleration3D)

    to_string( (Acceleration3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Acceleration3D, std::allocator<ad::physics::Acceleration3D> >)

    to_string( (Dimension3D)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::physics::Dimension3D)

    to_string( (Dimension3DList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Dimension3D, std::allocator<ad::physics::Dimension3D> >)

    to_string( (ProbabilityList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::physics::Probability, std::allocator<ad::physics::Probability> >)"""
