import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

AltitudeUnknown: Altitude

class Altitude(Boost.Python.instance):
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

        __init__( (object)arg1, (object)iAltitude) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (Altitude)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::Altitude)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Altitude)arg1, (Altitude)other) -> Altitude :

            C++ signature :
                ad::map::point::Altitude {lvalue} assign(ad::map::point::Altitude {lvalue},ad::map::point::Altitude)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (Altitude)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::Altitude {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (Altitude)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::Altitude {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> Altitude :

            C++ signature :
                ad::map::point::Altitude getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> Altitude :

            C++ signature :
                ad::map::point::Altitude getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> Altitude :

            C++ signature :
                ad::map::point::Altitude getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (Altitude)arg1, (Altitude)arg2) -> object :

            C++ signature :
                _object* __add__(ad::map::point::Altitude {lvalue},ad::map::point::Altitude)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Altitude)arg1, (Altitude)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::Altitude {lvalue},ad::map::point::Altitude)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (Altitude)arg1) -> float :

            C++ signature :
                double __float__(ad::map::point::Altitude {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (Altitude)arg1, (Altitude)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::map::point::Altitude {lvalue},ad::map::point::Altitude)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (Altitude)arg1, (Altitude)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::map::point::Altitude {lvalue},ad::map::point::Altitude)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (Altitude)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::map::point::Altitude&>,ad::map::point::Altitude)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (Altitude)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::map::point::Altitude&>,ad::map::point::Altitude)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (Altitude)arg1, (Altitude)arg2) -> object :

            C++ signature :
                _object* __le__(ad::map::point::Altitude {lvalue},ad::map::point::Altitude)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (Altitude)arg1, (Altitude)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::map::point::Altitude {lvalue},ad::map::point::Altitude)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (Altitude)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::map::point::Altitude {lvalue},double)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Altitude)arg1, (Altitude)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::Altitude {lvalue},ad::map::point::Altitude)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (Altitude)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::map::point::Altitude {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (Altitude)arg1, (Altitude)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::map::point::Altitude {lvalue},ad::map::point::Altitude)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (Altitude)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::Altitude {lvalue},double)

        __truediv__( (Altitude)arg1, (Altitude)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::Altitude {lvalue},ad::map::point::Altitude)"""
    @property
    def Valid(self): ...

class BoundingSphere(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    center: Incomplete
    radius: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (BoundingSphere)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::BoundingSphere)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (BoundingSphere)arg1, (BoundingSphere)other) -> BoundingSphere :

            C++ signature :
                ad::map::point::BoundingSphere {lvalue} assign(ad::map::point::BoundingSphere {lvalue},ad::map::point::BoundingSphere)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (BoundingSphere)arg1, (BoundingSphere)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::BoundingSphere {lvalue},ad::map::point::BoundingSphere)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (BoundingSphere)arg1, (BoundingSphere)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::BoundingSphere {lvalue},ad::map::point::BoundingSphere)"""
    @classmethod
    def __reduce__(cls): ...

class CoordinateTransform(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    ENUReferencePoint: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def ECEF2ENU(cls, *args, **kwargs):
        """
        ECEF2ENU( (CoordinateTransform)arg1, (ECEFPoint)pt) -> ENUPoint :

            C++ signature :
                ad::map::point::ENUPoint ECEF2ENU(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ECEFPoint)"""
    @classmethod
    def ECEF2Geo(cls, *args, **kwargs):
        """
        ECEF2Geo( (CoordinateTransform)arg1, (ECEFPoint)pt) -> GeoPoint :

            C++ signature :
                ad::map::point::GeoPoint ECEF2Geo(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ECEFPoint)"""
    @classmethod
    def ENU2ECEF(cls, *args, **kwargs):
        """
        ENU2ECEF( (CoordinateTransform)arg1, (ENUPoint)pt) -> ECEFPoint :

            C++ signature :
                ad::map::point::ECEFPoint ENU2ECEF(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ENUPoint)"""
    @classmethod
    def ENU2Geo(cls, *args, **kwargs):
        """
        ENU2Geo( (CoordinateTransform)arg1, (ENUPoint)pt) -> GeoPoint :

            C++ signature :
                ad::map::point::GeoPoint ENU2Geo(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ENUPoint)"""
    @classmethod
    def Geo2ECEF(cls, *args, **kwargs):
        """
        Geo2ECEF( (CoordinateTransform)arg1, (GeoPoint)pt) -> ECEFPoint :

            C++ signature :
                ad::map::point::ECEFPoint Geo2ECEF(ad::map::point::CoordinateTransform {lvalue},ad::map::point::GeoPoint)"""
    @classmethod
    def Geo2ENU(cls, *args, **kwargs):
        """
        Geo2ENU( (CoordinateTransform)arg1, (GeoPoint)pt) -> ENUPoint :

            C++ signature :
                ad::map::point::ENUPoint Geo2ENU(ad::map::point::CoordinateTransform {lvalue},ad::map::point::GeoPoint)"""
    @staticmethod
    def WGS84_R(ad) -> Any:
        """
        WGS84_R( (Latitude)lat) -> Distance :

            C++ signature :
                ad::physics::Distance WGS84_R(ad::map::point::Latitude)"""
    @classmethod
    def convert(cls, *args, **kwargs):
        """
        convert( (CoordinateTransform)arg1, (GeoPoint)x, (ENUPoint)y) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},ad::map::point::GeoPoint,ad::map::point::ENUPoint {lvalue})

        convert( (CoordinateTransform)arg1, (ENUPoint)x, (GeoPoint)y) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ENUPoint,ad::map::point::GeoPoint {lvalue})

        convert( (CoordinateTransform)arg1, (GeoPoint)x, (ECEFPoint)y) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},ad::map::point::GeoPoint,ad::map::point::ECEFPoint {lvalue})

        convert( (CoordinateTransform)arg1, (ECEFPoint)x, (GeoPoint)y) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ECEFPoint,ad::map::point::GeoPoint {lvalue})

        convert( (CoordinateTransform)arg1, (ECEFPoint)x, (ENUPoint)y) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ECEFPoint,ad::map::point::ENUPoint {lvalue})

        convert( (CoordinateTransform)arg1, (ENUPoint)x, (ECEFPoint)y) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ENUPoint,ad::map::point::ECEFPoint {lvalue})

        convert( (CoordinateTransform)arg1, (GeoEdge)xs, (ECEFEdge)ys) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >,std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue})

        convert( (CoordinateTransform)arg1, (ENUEdge)xs, (ECEFEdge)ys) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >,std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue})

        convert( (CoordinateTransform)arg1, (ECEFEdge)xs, (GeoEdge)ys) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue})

        convert( (CoordinateTransform)arg1, (ENUEdge)xs, (GeoEdge)ys) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue})

        convert( (CoordinateTransform)arg1, (ECEFEdge)xs, (ENUEdge)ys) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >,std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue})

        convert( (CoordinateTransform)arg1, (GeoEdge)xs, (ENUEdge)ys) -> None :

            C++ signature :
                void convert(ad::map::point::CoordinateTransform {lvalue},std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >,std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue})"""
    @staticmethod
    def geocentricLatitude(ad) -> Any:
        """
        geocentricLatitude( (Latitude)lat) -> float :

            C++ signature :
                double geocentricLatitude(ad::map::point::Latitude)"""
    @classmethod
    def setGeoProjection(cls, *args, **kwargs):
        """
        setGeoProjection( (CoordinateTransform)arg1, (str)geo_projection) -> bool :

            C++ signature :
                bool setGeoProjection(ad::map::point::CoordinateTransform {lvalue},std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
    @classmethod
    def __reduce__(cls): ...
    @property
    def ENURef(self): ...
    @property
    def ENUValid(self): ...

class ECEFCoordinate(Boost.Python.instance):
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

        __init__( (object)arg1, (object)iECEFCoordinate) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (ECEFCoordinate)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::ECEFCoordinate)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ECEFCoordinate)arg1, (ECEFCoordinate)other) -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate {lvalue} assign(ad::map::point::ECEFCoordinate {lvalue},ad::map::point::ECEFCoordinate)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (ECEFCoordinate)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::ECEFCoordinate {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (ECEFCoordinate)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::ECEFCoordinate {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (ECEFCoordinate)arg1, (ECEFCoordinate)arg2) -> object :

            C++ signature :
                _object* __add__(ad::map::point::ECEFCoordinate {lvalue},ad::map::point::ECEFCoordinate)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ECEFCoordinate)arg1, (ECEFCoordinate)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::ECEFCoordinate {lvalue},ad::map::point::ECEFCoordinate)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (ECEFCoordinate)arg1) -> float :

            C++ signature :
                double __float__(ad::map::point::ECEFCoordinate {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (ECEFCoordinate)arg1, (ECEFCoordinate)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::map::point::ECEFCoordinate {lvalue},ad::map::point::ECEFCoordinate)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (ECEFCoordinate)arg1, (ECEFCoordinate)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::map::point::ECEFCoordinate {lvalue},ad::map::point::ECEFCoordinate)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (ECEFCoordinate)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::map::point::ECEFCoordinate&>,ad::map::point::ECEFCoordinate)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (ECEFCoordinate)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::map::point::ECEFCoordinate&>,ad::map::point::ECEFCoordinate)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (ECEFCoordinate)arg1, (ECEFCoordinate)arg2) -> object :

            C++ signature :
                _object* __le__(ad::map::point::ECEFCoordinate {lvalue},ad::map::point::ECEFCoordinate)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (ECEFCoordinate)arg1, (ECEFCoordinate)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::map::point::ECEFCoordinate {lvalue},ad::map::point::ECEFCoordinate)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (ECEFCoordinate)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::map::point::ECEFCoordinate {lvalue},double)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ECEFCoordinate)arg1, (ECEFCoordinate)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::ECEFCoordinate {lvalue},ad::map::point::ECEFCoordinate)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (ECEFCoordinate)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::map::point::ECEFCoordinate {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (ECEFCoordinate)arg1, (ECEFCoordinate)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::map::point::ECEFCoordinate {lvalue},ad::map::point::ECEFCoordinate)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (ECEFCoordinate)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::ECEFCoordinate {lvalue},double)

        __truediv__( (ECEFCoordinate)arg1, (ECEFCoordinate)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::ECEFCoordinate {lvalue},ad::map::point::ECEFCoordinate)"""
    @property
    def Valid(self): ...

class ECEFEdge(Boost.Python.instance):
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
        append( (ECEFEdge)arg1, (ECEFPoint)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},ad::map::point::ECEFPoint)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ECEFEdge)arg1, (ECEFPoint)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},ad::map::point::ECEFPoint)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ECEFEdge)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ECEFEdge)arg1, (ECEFPoint)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},ad::map::point::ECEFPoint)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ECEFEdge)arg1, (int)arg2, (ECEFPoint)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},long,ad::map::point::ECEFPoint)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ECEFEdge)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ECEFEdge)arg1, (ECEFPoint)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},ad::map::point::ECEFPoint)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ECEFEdge)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},long)

        __delitem__( (ECEFEdge)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ECEFEdge)arg1, (int)arg2) -> ECEFPoint :

            C++ signature :
                ad::map::point::ECEFPoint {lvalue} __getitem__(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},long)

        __getitem__( (ECEFEdge)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ECEFEdge)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ECEFEdge)arg1, (int)arg2, (ECEFPoint)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},long,ad::map::point::ECEFPoint)

        __setitem__( (ECEFEdge)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class ECEFHeading(Boost.Python.instance):
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

        __init__( (object)arg1, (ECEFHeading)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::ECEFHeading)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ECEFHeading)arg1, (ECEFHeading)other) -> ECEFHeading :

            C++ signature :
                ad::map::point::ECEFHeading {lvalue} assign(ad::map::point::ECEFHeading {lvalue},ad::map::point::ECEFHeading)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ECEFHeading)arg1, (ECEFHeading)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::ECEFHeading {lvalue},ad::map::point::ECEFHeading)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ECEFHeading)arg1, (ECEFHeading)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::ECEFHeading {lvalue},ad::map::point::ECEFHeading)"""
    @classmethod
    def __reduce__(cls): ...

class ECEFPoint(Boost.Python.instance):
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

        __init__( (object)arg1, (ECEFPoint)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::ECEFPoint)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ECEFPoint)arg1, (ECEFPoint)other) -> ECEFPoint :

            C++ signature :
                ad::map::point::ECEFPoint {lvalue} assign(ad::map::point::ECEFPoint {lvalue},ad::map::point::ECEFPoint)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ECEFPoint)arg1, (ECEFPoint)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::ECEFPoint {lvalue},ad::map::point::ECEFPoint)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ECEFPoint)arg1, (ECEFPoint)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::ECEFPoint {lvalue},ad::map::point::ECEFPoint)"""
    @classmethod
    def __reduce__(cls): ...

class ENUCoordinate(Boost.Python.instance):
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

        __init__( (object)arg1, (object)iENUCoordinate) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (ENUCoordinate)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::ENUCoordinate)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ENUCoordinate)arg1, (ENUCoordinate)other) -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate {lvalue} assign(ad::map::point::ENUCoordinate {lvalue},ad::map::point::ENUCoordinate)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (ENUCoordinate)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::ENUCoordinate {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (ENUCoordinate)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::ENUCoordinate {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (ENUCoordinate)arg1, (ENUCoordinate)arg2) -> object :

            C++ signature :
                _object* __add__(ad::map::point::ENUCoordinate {lvalue},ad::map::point::ENUCoordinate)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ENUCoordinate)arg1, (ENUCoordinate)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::ENUCoordinate {lvalue},ad::map::point::ENUCoordinate)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (ENUCoordinate)arg1) -> float :

            C++ signature :
                double __float__(ad::map::point::ENUCoordinate {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (ENUCoordinate)arg1, (ENUCoordinate)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::map::point::ENUCoordinate {lvalue},ad::map::point::ENUCoordinate)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (ENUCoordinate)arg1, (ENUCoordinate)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::map::point::ENUCoordinate {lvalue},ad::map::point::ENUCoordinate)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (ENUCoordinate)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::map::point::ENUCoordinate&>,ad::map::point::ENUCoordinate)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (ENUCoordinate)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::map::point::ENUCoordinate&>,ad::map::point::ENUCoordinate)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (ENUCoordinate)arg1, (ENUCoordinate)arg2) -> object :

            C++ signature :
                _object* __le__(ad::map::point::ENUCoordinate {lvalue},ad::map::point::ENUCoordinate)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (ENUCoordinate)arg1, (ENUCoordinate)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::map::point::ENUCoordinate {lvalue},ad::map::point::ENUCoordinate)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (ENUCoordinate)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::map::point::ENUCoordinate {lvalue},double)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ENUCoordinate)arg1, (ENUCoordinate)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::ENUCoordinate {lvalue},ad::map::point::ENUCoordinate)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (ENUCoordinate)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::map::point::ENUCoordinate {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (ENUCoordinate)arg1, (ENUCoordinate)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::map::point::ENUCoordinate {lvalue},ad::map::point::ENUCoordinate)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (ENUCoordinate)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::ENUCoordinate {lvalue},double)

        __truediv__( (ENUCoordinate)arg1, (ENUCoordinate)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::ENUCoordinate {lvalue},ad::map::point::ENUCoordinate)"""
    @property
    def Valid(self): ...

class ENUEdge(Boost.Python.instance):
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
        append( (ENUEdge)arg1, (ENUPoint)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},ad::map::point::ENUPoint)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ENUEdge)arg1, (ENUPoint)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},ad::map::point::ENUPoint)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ENUEdge)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ENUEdge)arg1, (ENUPoint)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},ad::map::point::ENUPoint)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ENUEdge)arg1, (int)arg2, (ENUPoint)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},long,ad::map::point::ENUPoint)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ENUEdge)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ENUEdge)arg1, (ENUPoint)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},ad::map::point::ENUPoint)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ENUEdge)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},long)

        __delitem__( (ENUEdge)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ENUEdge)arg1, (int)arg2) -> ENUPoint :

            C++ signature :
                ad::map::point::ENUPoint {lvalue} __getitem__(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},long)

        __getitem__( (ENUEdge)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ENUEdge)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ENUEdge)arg1, (int)arg2, (ENUPoint)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},long,ad::map::point::ENUPoint)

        __setitem__( (ENUEdge)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class ENUEdgeCache(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    enuEdge: Incomplete
    enuVersion: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (ENUEdgeCache)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::ENUEdgeCache)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ENUEdgeCache)arg1, (ENUEdgeCache)other) -> ENUEdgeCache :

            C++ signature :
                ad::map::point::ENUEdgeCache {lvalue} assign(ad::map::point::ENUEdgeCache {lvalue},ad::map::point::ENUEdgeCache)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ENUEdgeCache)arg1, (ENUEdgeCache)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::ENUEdgeCache {lvalue},ad::map::point::ENUEdgeCache)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ENUEdgeCache)arg1, (ENUEdgeCache)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::ENUEdgeCache {lvalue},ad::map::point::ENUEdgeCache)"""
    @classmethod
    def __reduce__(cls): ...

class ENUHeading(Boost.Python.instance):
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

        __init__( (object)arg1, (object)iENUHeading) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (ENUHeading)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::ENUHeading)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ENUHeading)arg1, (ENUHeading)other) -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading {lvalue} assign(ad::map::point::ENUHeading {lvalue},ad::map::point::ENUHeading)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (ENUHeading)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::ENUHeading {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (ENUHeading)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::ENUHeading {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (ENUHeading)arg1, (ENUHeading)arg2) -> object :

            C++ signature :
                _object* __add__(ad::map::point::ENUHeading {lvalue},ad::map::point::ENUHeading)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ENUHeading)arg1, (ENUHeading)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::ENUHeading {lvalue},ad::map::point::ENUHeading)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (ENUHeading)arg1) -> float :

            C++ signature :
                double __float__(ad::map::point::ENUHeading {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (ENUHeading)arg1, (ENUHeading)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::map::point::ENUHeading {lvalue},ad::map::point::ENUHeading)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (ENUHeading)arg1, (ENUHeading)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::map::point::ENUHeading {lvalue},ad::map::point::ENUHeading)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (ENUHeading)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::map::point::ENUHeading&>,ad::map::point::ENUHeading)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (ENUHeading)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::map::point::ENUHeading&>,ad::map::point::ENUHeading)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (ENUHeading)arg1, (ENUHeading)arg2) -> object :

            C++ signature :
                _object* __le__(ad::map::point::ENUHeading {lvalue},ad::map::point::ENUHeading)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (ENUHeading)arg1, (ENUHeading)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::map::point::ENUHeading {lvalue},ad::map::point::ENUHeading)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (ENUHeading)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::map::point::ENUHeading {lvalue},double)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ENUHeading)arg1, (ENUHeading)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::ENUHeading {lvalue},ad::map::point::ENUHeading)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (ENUHeading)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::map::point::ENUHeading {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (ENUHeading)arg1, (ENUHeading)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::map::point::ENUHeading {lvalue},ad::map::point::ENUHeading)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (ENUHeading)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::ENUHeading {lvalue},double)

        __truediv__( (ENUHeading)arg1, (ENUHeading)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::ENUHeading {lvalue},ad::map::point::ENUHeading)"""
    @property
    def Valid(self): ...

class ENUPoint(Boost.Python.instance):
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

        __init__( (object)arg1, (ENUPoint)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::ENUPoint)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ENUPoint)arg1, (ENUPoint)other) -> ENUPoint :

            C++ signature :
                ad::map::point::ENUPoint {lvalue} assign(ad::map::point::ENUPoint {lvalue},ad::map::point::ENUPoint)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ENUPoint)arg1, (ENUPoint)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::ENUPoint {lvalue},ad::map::point::ENUPoint)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ENUPoint)arg1, (ENUPoint)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::ENUPoint {lvalue},ad::map::point::ENUPoint)"""
    @classmethod
    def __reduce__(cls): ...

class GeoEdge(Boost.Python.instance):
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
        append( (GeoEdge)arg1, (GeoPoint)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},ad::map::point::GeoPoint)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (GeoEdge)arg1, (GeoPoint)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},ad::map::point::GeoPoint)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (GeoEdge)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (GeoEdge)arg1, (GeoPoint)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},ad::map::point::GeoPoint)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (GeoEdge)arg1, (int)arg2, (GeoPoint)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},long,ad::map::point::GeoPoint)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (GeoEdge)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (GeoEdge)arg1, (GeoPoint)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},ad::map::point::GeoPoint)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (GeoEdge)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},long)

        __delitem__( (GeoEdge)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (GeoEdge)arg1, (int)arg2) -> GeoPoint :

            C++ signature :
                ad::map::point::GeoPoint {lvalue} __getitem__(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},long)

        __getitem__( (GeoEdge)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (GeoEdge)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (GeoEdge)arg1, (int)arg2, (GeoPoint)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},long,ad::map::point::GeoPoint)

        __setitem__( (GeoEdge)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class GeoPoint(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    altitude: Incomplete
    latitude: Incomplete
    longitude: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (GeoPoint)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::GeoPoint)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (GeoPoint)arg1, (GeoPoint)other) -> GeoPoint :

            C++ signature :
                ad::map::point::GeoPoint {lvalue} assign(ad::map::point::GeoPoint {lvalue},ad::map::point::GeoPoint)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (GeoPoint)arg1, (GeoPoint)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::GeoPoint {lvalue},ad::map::point::GeoPoint)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (GeoPoint)arg1, (GeoPoint)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::GeoPoint {lvalue},ad::map::point::GeoPoint)"""
    @classmethod
    def __reduce__(cls): ...

class Geometry(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    ecefEdge: Incomplete
    isClosed: Incomplete
    isValid: Incomplete
    length: Incomplete
    private_enuEdgeCache: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Geometry)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::Geometry)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Geometry)arg1, (Geometry)other) -> Geometry :

            C++ signature :
                ad::map::point::Geometry {lvalue} assign(ad::map::point::Geometry {lvalue},ad::map::point::Geometry)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Geometry)arg1, (Geometry)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::Geometry {lvalue},ad::map::point::Geometry)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Geometry)arg1, (Geometry)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::Geometry {lvalue},ad::map::point::Geometry)"""
    @classmethod
    def __reduce__(cls): ...

class Latitude(Boost.Python.instance):
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

        __init__( (object)arg1, (object)iLatitude) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (Latitude)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::Latitude)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Latitude)arg1, (Latitude)other) -> Latitude :

            C++ signature :
                ad::map::point::Latitude {lvalue} assign(ad::map::point::Latitude {lvalue},ad::map::point::Latitude)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (Latitude)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::Latitude {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (Latitude)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::Latitude {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> Latitude :

            C++ signature :
                ad::map::point::Latitude getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> Latitude :

            C++ signature :
                ad::map::point::Latitude getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> Latitude :

            C++ signature :
                ad::map::point::Latitude getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (Latitude)arg1, (Latitude)arg2) -> object :

            C++ signature :
                _object* __add__(ad::map::point::Latitude {lvalue},ad::map::point::Latitude)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Latitude)arg1, (Latitude)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::Latitude {lvalue},ad::map::point::Latitude)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (Latitude)arg1) -> float :

            C++ signature :
                double __float__(ad::map::point::Latitude {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (Latitude)arg1, (Latitude)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::map::point::Latitude {lvalue},ad::map::point::Latitude)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (Latitude)arg1, (Latitude)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::map::point::Latitude {lvalue},ad::map::point::Latitude)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (Latitude)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::map::point::Latitude&>,ad::map::point::Latitude)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (Latitude)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::map::point::Latitude&>,ad::map::point::Latitude)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (Latitude)arg1, (Latitude)arg2) -> object :

            C++ signature :
                _object* __le__(ad::map::point::Latitude {lvalue},ad::map::point::Latitude)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (Latitude)arg1, (Latitude)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::map::point::Latitude {lvalue},ad::map::point::Latitude)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (Latitude)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::map::point::Latitude {lvalue},double)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Latitude)arg1, (Latitude)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::Latitude {lvalue},ad::map::point::Latitude)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (Latitude)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::map::point::Latitude {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (Latitude)arg1, (Latitude)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::map::point::Latitude {lvalue},ad::map::point::Latitude)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (Latitude)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::Latitude {lvalue},double)

        __truediv__( (Latitude)arg1, (Latitude)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::Latitude {lvalue},ad::map::point::Latitude)"""
    @property
    def Valid(self): ...

class Longitude(Boost.Python.instance):
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

        __init__( (object)arg1, (object)iLongitude) -> None :

            C++ signature :
                void __init__(_object*,double)

        __init__( (object)arg1, (Longitude)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::Longitude)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Longitude)arg1, (Longitude)other) -> Longitude :

            C++ signature :
                ad::map::point::Longitude {lvalue} assign(ad::map::point::Longitude {lvalue},ad::map::point::Longitude)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (Longitude)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::Longitude {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (Longitude)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::Longitude {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> Longitude :

            C++ signature :
                ad::map::point::Longitude getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> Longitude :

            C++ signature :
                ad::map::point::Longitude getMin()"""
    @staticmethod
    def getPrecision() -> Any:
        """
        getPrecision() -> Longitude :

            C++ signature :
                ad::map::point::Longitude getPrecision()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (Longitude)arg1, (Longitude)arg2) -> object :

            C++ signature :
                _object* __add__(ad::map::point::Longitude {lvalue},ad::map::point::Longitude)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Longitude)arg1, (Longitude)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::Longitude {lvalue},ad::map::point::Longitude)"""
    @classmethod
    def __float__(cls, ad) -> Any:
        """
        __float__( (Longitude)arg1) -> float :

            C++ signature :
                double __float__(ad::map::point::Longitude {lvalue})"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (Longitude)arg1, (Longitude)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::map::point::Longitude {lvalue},ad::map::point::Longitude)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (Longitude)arg1, (Longitude)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::map::point::Longitude {lvalue},ad::map::point::Longitude)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (Longitude)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::map::point::Longitude&>,ad::map::point::Longitude)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (Longitude)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::map::point::Longitude&>,ad::map::point::Longitude)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (Longitude)arg1, (Longitude)arg2) -> object :

            C++ signature :
                _object* __le__(ad::map::point::Longitude {lvalue},ad::map::point::Longitude)"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (Longitude)arg1, (Longitude)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::map::point::Longitude {lvalue},ad::map::point::Longitude)"""
    @classmethod
    def __mul__(cls, ad, double) -> Any:
        """
        __mul__( (Longitude)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __mul__(ad::map::point::Longitude {lvalue},double)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Longitude)arg1, (Longitude)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::Longitude {lvalue},ad::map::point::Longitude)"""
    @classmethod
    def __neg__(cls, ad) -> Any:
        """
        __neg__( (Longitude)arg1) -> object :

            C++ signature :
                _object* __neg__(ad::map::point::Longitude {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (Longitude)arg1, (Longitude)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::map::point::Longitude {lvalue},ad::map::point::Longitude)"""
    @classmethod
    def __truediv__(cls, ad, double) -> Any:
        """
        __truediv__( (Longitude)arg1, (object)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::Longitude {lvalue},double)

        __truediv__( (Longitude)arg1, (Longitude)arg2) -> object :

            C++ signature :
                _object* __truediv__(ad::map::point::Longitude {lvalue},ad::map::point::Longitude)"""
    @property
    def Valid(self): ...

class ParaPoint(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    laneId: Incomplete
    parametricOffset: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (ParaPoint)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::point::ParaPoint)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ParaPoint)arg1, (ParaPoint)other) -> ParaPoint :

            C++ signature :
                ad::map::point::ParaPoint {lvalue} assign(ad::map::point::ParaPoint {lvalue},ad::map::point::ParaPoint)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ParaPoint)arg1, (ParaPoint)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::point::ParaPoint {lvalue},ad::map::point::ParaPoint)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ParaPoint)arg1, (ParaPoint)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::point::ParaPoint {lvalue},ad::map::point::ParaPoint)"""
    @classmethod
    def __reduce__(cls): ...

class ParaPointList(Boost.Python.instance):
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
        append( (ParaPointList)arg1, (ParaPoint)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},ad::map::point::ParaPoint)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ParaPointList)arg1, (ParaPoint)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},ad::map::point::ParaPoint)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ParaPointList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ParaPointList)arg1, (ParaPoint)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},ad::map::point::ParaPoint)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ParaPointList)arg1, (int)arg2, (ParaPoint)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},long,ad::map::point::ParaPoint)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ParaPointList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ParaPointList)arg1, (ParaPoint)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},ad::map::point::ParaPoint)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ParaPointList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},long)

        __delitem__( (ParaPointList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ParaPointList)arg1, (int)arg2) -> ParaPoint :

            C++ signature :
                ad::map::point::ParaPoint {lvalue} __getitem__(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},long)

        __getitem__( (ParaPointList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ParaPointList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ParaPointList)arg1, (int)arg2, (ParaPoint)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},long,ad::map::point::ParaPoint)

        __setitem__( (ParaPointList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class numeric_limits_less__ad_scope_map_scope_point_scope_Altitude__greater_(Boost.Python.instance):
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
        epsilon() -> Altitude :

            C++ signature :
                ad::map::point::Altitude epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> Altitude :

            C++ signature :
                ad::map::point::Altitude lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> Altitude :

            C++ signature :
                ad::map::point::Altitude max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_map_scope_point_scope_ECEFCoordinate__greater_(Boost.Python.instance):
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
        epsilon() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_map_scope_point_scope_ENUCoordinate__greater_(Boost.Python.instance):
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
        epsilon() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_map_scope_point_scope_ENUHeading__greater_(Boost.Python.instance):
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
        epsilon() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_map_scope_point_scope_Latitude__greater_(Boost.Python.instance):
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
        epsilon() -> Latitude :

            C++ signature :
                ad::map::point::Latitude epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> Latitude :

            C++ signature :
                ad::map::point::Latitude lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> Latitude :

            C++ signature :
                ad::map::point::Latitude max()"""
    @classmethod
    def __reduce__(cls): ...

class numeric_limits_less__ad_scope_map_scope_point_scope_Longitude__greater_(Boost.Python.instance):
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
        epsilon() -> Longitude :

            C++ signature :
                ad::map::point::Longitude epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> Longitude :

            C++ signature :
                ad::map::point::Longitude lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> Longitude :

            C++ signature :
                ad::map::point::Longitude max()"""
    @classmethod
    def __reduce__(cls): ...

def approxAltitude(*args, **kwargs):
    """
    approxAltitude( (GeoPoint)point, (GeoEdge)pts) -> GeoPoint :

        C++ signature :
            ad::map::point::GeoPoint approxAltitude(ad::map::point::GeoPoint,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)"""
def calcBoundingSphere(*args, **kwargs):
    """
    calcBoundingSphere( (Geometry)edgeLeft, (Geometry)edgeRight) -> BoundingSphere :

        C++ signature :
            ad::map::point::BoundingSphere calcBoundingSphere(ad::map::point::Geometry,ad::map::point::Geometry)"""
def calcLength(*args, **kwargs):
    """
    calcLength( (ENUEdge)edge) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    calcLength( (ECEFEdge)edge) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    calcLength( (GeoEdge)edge) -> Distance :

        C++ signature :
            ad::physics::Distance calcLength(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)"""
def createECEFHeading(*args, **kwargs):
    """
    createECEFHeading( (ECEFPoint)start, (ECEFPoint)end) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading createECEFHeading(ad::map::point::ECEFPoint,ad::map::point::ECEFPoint)

    createECEFHeading( (ENUHeading)yaw, (GeoPoint)enuReferencePoint) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading createECEFHeading(ad::map::point::ENUHeading,ad::map::point::GeoPoint)"""
def createECEFPoint(*args, **kwargs):
    """
    createECEFPoint( (object)x, (object)y, (object)z) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint createECEFPoint(double,double,double)

    createECEFPoint( (ECEFCoordinate)x, (ECEFCoordinate)y, (ECEFCoordinate)z) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint createECEFPoint(ad::map::point::ECEFCoordinate,ad::map::point::ECEFCoordinate,ad::map::point::ECEFCoordinate)"""
@overload
def createENUHeading(double) -> Any:
    """
    createENUHeading( (object)yawAngleRadian) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(double)

    createENUHeading( (Angle)angle) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::physics::Angle)

    createENUHeading( (ECEFHeading)ecefHeading) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ECEFHeading)

    createENUHeading( (ECEFHeading)ecefHeading, (GeoPoint)enuReferencePoint) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ECEFHeading,ad::map::point::GeoPoint)

    createENUHeading( (ECEFHeading)ecefHeading, (ECEFPoint)enuReferencePoint) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ECEFHeading,ad::map::point::ECEFPoint)

    createENUHeading( (ENUPoint)start, (ENUPoint)end) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ENUPoint,ad::map::point::ENUPoint)"""
@overload
def createENUHeading(ad) -> Any:
    """
    createENUHeading( (object)yawAngleRadian) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(double)

    createENUHeading( (Angle)angle) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::physics::Angle)

    createENUHeading( (ECEFHeading)ecefHeading) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ECEFHeading)

    createENUHeading( (ECEFHeading)ecefHeading, (GeoPoint)enuReferencePoint) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ECEFHeading,ad::map::point::GeoPoint)

    createENUHeading( (ECEFHeading)ecefHeading, (ECEFPoint)enuReferencePoint) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ECEFHeading,ad::map::point::ECEFPoint)

    createENUHeading( (ENUPoint)start, (ENUPoint)end) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ENUPoint,ad::map::point::ENUPoint)"""
@overload
def createENUHeading(ad) -> Any:
    """
    createENUHeading( (object)yawAngleRadian) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(double)

    createENUHeading( (Angle)angle) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::physics::Angle)

    createENUHeading( (ECEFHeading)ecefHeading) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ECEFHeading)

    createENUHeading( (ECEFHeading)ecefHeading, (GeoPoint)enuReferencePoint) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ECEFHeading,ad::map::point::GeoPoint)

    createENUHeading( (ECEFHeading)ecefHeading, (ECEFPoint)enuReferencePoint) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ECEFHeading,ad::map::point::ECEFPoint)

    createENUHeading( (ENUPoint)start, (ENUPoint)end) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading createENUHeading(ad::map::point::ENUPoint,ad::map::point::ENUPoint)"""
def createENUPoint(*args, **kwargs):
    """
    createENUPoint( (object)x, (object)y, (object)z) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint createENUPoint(double,double,double)

    createENUPoint( (ENUCoordinate)x, (ENUCoordinate)y, (ENUCoordinate)z) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint createENUPoint(ad::map::point::ENUCoordinate,ad::map::point::ENUCoordinate,ad::map::point::ENUCoordinate)"""
def createGeoPoint(*args, **kwargs):
    """
    createGeoPoint( (Longitude)longitude, (Latitude)latitude, (Altitude)altitude) -> GeoPoint :

        C++ signature :
            ad::map::point::GeoPoint createGeoPoint(ad::map::point::Longitude,ad::map::point::Latitude,ad::map::point::Altitude)"""
def createGeometry(*args, **kwargs):
    """
    createGeometry( (ECEFEdge)points, (bool)closed) -> Geometry :

        C++ signature :
            ad::map::point::Geometry createGeometry(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >,bool)"""
def createParaPoint(*args, **kwargs):
    """
    createParaPoint( (LaneId)laneId, (ParametricValue)parametricOffset) -> ParaPoint :

        C++ signature :
            ad::map::point::ParaPoint createParaPoint(ad::map::lane::LaneId,ad::physics::ParametricValue)"""
def degree2radians(double) -> Any:
    """
    degree2radians( (object)degree) -> float :

        C++ signature :
            double degree2radians(double)"""
def distance(*args, **kwargs):
    """
    distance( (ENUPoint)point, (ENUPoint)other) -> Distance :

        C++ signature :
            ad::physics::Distance distance(ad::map::point::ENUPoint,ad::map::point::ENUPoint)

    distance( (BoundingSphere)left, (BoundingSphere)right) -> Distance :

        C++ signature :
            ad::physics::Distance distance(ad::map::point::BoundingSphere,ad::map::point::BoundingSphere)

    distance( (ECEFPoint)point, (ECEFPoint)other) -> Distance :

        C++ signature :
            ad::physics::Distance distance(ad::map::point::ECEFPoint,ad::map::point::ECEFPoint)

    distance( (GeoPoint)point, (GeoPoint)other) -> Distance :

        C++ signature :
            ad::physics::Distance distance(ad::map::point::GeoPoint,ad::map::point::GeoPoint)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (ECEFCoordinate)other) -> ECEFCoordinate :

        C++ signature :
            ad::map::point::ECEFCoordinate fabs(ad::map::point::ECEFCoordinate)

    fabs( (Altitude)other) -> Altitude :

        C++ signature :
            ad::map::point::Altitude fabs(ad::map::point::Altitude)

    fabs( (Latitude)other) -> Latitude :

        C++ signature :
            ad::map::point::Latitude fabs(ad::map::point::Latitude)

    fabs( (Longitude)other) -> Longitude :

        C++ signature :
            ad::map::point::Longitude fabs(ad::map::point::Longitude)

    fabs( (ENUCoordinate)other) -> ENUCoordinate :

        C++ signature :
            ad::map::point::ENUCoordinate fabs(ad::map::point::ENUCoordinate)

    fabs( (ENUHeading)other) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading fabs(ad::map::point::ENUHeading)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (ECEFCoordinate)other) -> ECEFCoordinate :

        C++ signature :
            ad::map::point::ECEFCoordinate fabs(ad::map::point::ECEFCoordinate)

    fabs( (Altitude)other) -> Altitude :

        C++ signature :
            ad::map::point::Altitude fabs(ad::map::point::Altitude)

    fabs( (Latitude)other) -> Latitude :

        C++ signature :
            ad::map::point::Latitude fabs(ad::map::point::Latitude)

    fabs( (Longitude)other) -> Longitude :

        C++ signature :
            ad::map::point::Longitude fabs(ad::map::point::Longitude)

    fabs( (ENUCoordinate)other) -> ENUCoordinate :

        C++ signature :
            ad::map::point::ENUCoordinate fabs(ad::map::point::ENUCoordinate)

    fabs( (ENUHeading)other) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading fabs(ad::map::point::ENUHeading)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (ECEFCoordinate)other) -> ECEFCoordinate :

        C++ signature :
            ad::map::point::ECEFCoordinate fabs(ad::map::point::ECEFCoordinate)

    fabs( (Altitude)other) -> Altitude :

        C++ signature :
            ad::map::point::Altitude fabs(ad::map::point::Altitude)

    fabs( (Latitude)other) -> Latitude :

        C++ signature :
            ad::map::point::Latitude fabs(ad::map::point::Latitude)

    fabs( (Longitude)other) -> Longitude :

        C++ signature :
            ad::map::point::Longitude fabs(ad::map::point::Longitude)

    fabs( (ENUCoordinate)other) -> ENUCoordinate :

        C++ signature :
            ad::map::point::ENUCoordinate fabs(ad::map::point::ENUCoordinate)

    fabs( (ENUHeading)other) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading fabs(ad::map::point::ENUHeading)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (ECEFCoordinate)other) -> ECEFCoordinate :

        C++ signature :
            ad::map::point::ECEFCoordinate fabs(ad::map::point::ECEFCoordinate)

    fabs( (Altitude)other) -> Altitude :

        C++ signature :
            ad::map::point::Altitude fabs(ad::map::point::Altitude)

    fabs( (Latitude)other) -> Latitude :

        C++ signature :
            ad::map::point::Latitude fabs(ad::map::point::Latitude)

    fabs( (Longitude)other) -> Longitude :

        C++ signature :
            ad::map::point::Longitude fabs(ad::map::point::Longitude)

    fabs( (ENUCoordinate)other) -> ENUCoordinate :

        C++ signature :
            ad::map::point::ENUCoordinate fabs(ad::map::point::ENUCoordinate)

    fabs( (ENUHeading)other) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading fabs(ad::map::point::ENUHeading)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (ECEFCoordinate)other) -> ECEFCoordinate :

        C++ signature :
            ad::map::point::ECEFCoordinate fabs(ad::map::point::ECEFCoordinate)

    fabs( (Altitude)other) -> Altitude :

        C++ signature :
            ad::map::point::Altitude fabs(ad::map::point::Altitude)

    fabs( (Latitude)other) -> Latitude :

        C++ signature :
            ad::map::point::Latitude fabs(ad::map::point::Latitude)

    fabs( (Longitude)other) -> Longitude :

        C++ signature :
            ad::map::point::Longitude fabs(ad::map::point::Longitude)

    fabs( (ENUCoordinate)other) -> ENUCoordinate :

        C++ signature :
            ad::map::point::ENUCoordinate fabs(ad::map::point::ENUCoordinate)

    fabs( (ENUHeading)other) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading fabs(ad::map::point::ENUHeading)"""
@overload
def fabs(ad) -> Any:
    """
    fabs( (ECEFCoordinate)other) -> ECEFCoordinate :

        C++ signature :
            ad::map::point::ECEFCoordinate fabs(ad::map::point::ECEFCoordinate)

    fabs( (Altitude)other) -> Altitude :

        C++ signature :
            ad::map::point::Altitude fabs(ad::map::point::Altitude)

    fabs( (Latitude)other) -> Latitude :

        C++ signature :
            ad::map::point::Latitude fabs(ad::map::point::Latitude)

    fabs( (Longitude)other) -> Longitude :

        C++ signature :
            ad::map::point::Longitude fabs(ad::map::point::Longitude)

    fabs( (ENUCoordinate)other) -> ENUCoordinate :

        C++ signature :
            ad::map::point::ENUCoordinate fabs(ad::map::point::ENUCoordinate)

    fabs( (ENUHeading)other) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading fabs(ad::map::point::ENUHeading)"""
def findNearestPointOnEdge(*args, **kwargs):
    """
    findNearestPointOnEdge( (Geometry)geometry, (ECEFPoint)pt) -> ParametricValue :

        C++ signature :
            ad::physics::ParametricValue findNearestPointOnEdge(ad::map::point::Geometry,ad::map::point::ECEFPoint)"""
def flatDistance(*args, **kwargs):
    """
    flatDistance( (GeoPoint)point, (GeoPoint)other) -> Distance :

        C++ signature :
            ad::physics::Distance flatDistance(ad::map::point::GeoPoint,ad::map::point::GeoPoint)"""
def getCachedENUEdge(ad) -> Any:
    """
    getCachedENUEdge( (Geometry)geometry) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > getCachedENUEdge(ad::map::point::Geometry)"""
def getDirectionVectorsZPlane(*args, **kwargs):
    """
    getDirectionVectorsZPlane( (ENUHeading)heading, (ENUPoint)directionalVector, (ENUPoint)orthogonalVector) -> None :

        C++ signature :
            void getDirectionVectorsZPlane(ad::map::point::ENUHeading,ad::map::point::ENUPoint {lvalue},ad::map::point::ENUPoint {lvalue})"""
def getDirectionalVectorZPlane(ad) -> Any:
    """
    getDirectionalVectorZPlane( (ENUHeading)heading) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint getDirectionalVectorZPlane(ad::map::point::ENUHeading)"""
def getEnuEastAxis() -> Any:
    """
    getEnuEastAxis() -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint getEnuEastAxis()"""
def getEnuNorthAxis() -> Any:
    """
    getEnuNorthAxis() -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint getEnuNorthAxis()"""
def getEnuUpAxis() -> Any:
    """
    getEnuUpAxis() -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint getEnuUpAxis()"""
def getMiddleEdge(*args, **kwargs):
    """
    getMiddleEdge( (Geometry)geometry, (Geometry)other) -> ECEFEdge :

        C++ signature :
            std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > getMiddleEdge(ad::map::point::Geometry,ad::map::point::Geometry)"""
def getOrthogonalVectorZPlane(ad) -> Any:
    """
    getOrthogonalVectorZPlane( (ENUHeading)heading) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint getOrthogonalVectorZPlane(ad::map::point::ENUHeading)"""
def getParametricPoint(*args, **kwargs):
    """
    getParametricPoint( (Geometry)geometry, (ParametricValue)t) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint getParametricPoint(ad::map::point::Geometry,ad::physics::ParametricValue)"""
def getParametricRange(*args, **kwargs):
    """
    getParametricRange( (Geometry)geometry, (ParametricRange)trange, (ECEFEdge)outputEdge [, (bool)revertOrder=False]) -> None :

        C++ signature :
            void getParametricRange(ad::map::point::Geometry,ad::physics::ParametricRange,std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue} [,bool=False])

    getParametricRange( (Geometry)geometry, (ParametricRange)trange, (GeoEdge)outputEdge [, (bool)revertOrder=False]) -> None :

        C++ signature :
            void getParametricRange(ad::map::point::Geometry,ad::physics::ParametricRange,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue} [,bool=False])

    getParametricRange( (Geometry)geometry, (ParametricRange)trange, (ENUEdge)outputEdge [, (bool)revertOrder=False]) -> None :

        C++ signature :
            void getParametricRange(ad::map::point::Geometry,ad::physics::ParametricRange,std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue} [,bool=False])"""
def haveSameEnd(*args, **kwargs):
    """
    haveSameEnd( (Geometry)edge, (Geometry)other) -> bool :

        C++ signature :
            bool haveSameEnd(ad::map::point::Geometry,ad::map::point::Geometry)"""
def haveSameOrientation(*args, **kwargs):
    """
    haveSameOrientation( (GeoEdge)pts0, (GeoEdge)pts1) -> bool :

        C++ signature :
            bool haveSameOrientation(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)"""
def haveSameStart(*args, **kwargs):
    """
    haveSameStart( (Geometry)edge, (Geometry)other) -> bool :

        C++ signature :
            bool haveSameStart(ad::map::point::Geometry,ad::map::point::Geometry)"""
def isOnTheLeft(*args, **kwargs):
    """
    isOnTheLeft( (GeoPoint)point, (GeoPoint)pt0, (GeoPoint)pt1) -> bool :

        C++ signature :
            bool isOnTheLeft(ad::map::point::GeoPoint,ad::map::point::GeoPoint,ad::map::point::GeoPoint)

    isOnTheLeft( (GeoEdge)pts0, (GeoEdge)pts1) -> bool :

        C++ signature :
            bool isOnTheLeft(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >,std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)"""
def isPredecessor(*args, **kwargs):
    """
    isPredecessor( (Geometry)edge, (Geometry)other) -> bool :

        C++ signature :
            bool isPredecessor(ad::map::point::Geometry,ad::map::point::Geometry)"""
def isSuccessor(*args, **kwargs):
    """
    isSuccessor( (Geometry)edge, (Geometry)other) -> bool :

        C++ signature :
            bool isSuccessor(ad::map::point::Geometry,ad::map::point::Geometry)"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (ENUPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::ENUPoint [,bool=True])

    isValid( (ENUEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > [,bool=True])

    isValid( (ECEFPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::ECEFPoint [,bool=True])

    isValid( (ECEFEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > [,bool=True])

    isValid( (GeoPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::GeoPoint [,bool=True])

    isValid( (GeoEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > [,bool=True])

    isValid( (Geometry)geometry) -> bool :

        C++ signature :
            bool isValid(ad::map::point::Geometry)"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (ENUPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::ENUPoint [,bool=True])

    isValid( (ENUEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > [,bool=True])

    isValid( (ECEFPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::ECEFPoint [,bool=True])

    isValid( (ECEFEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > [,bool=True])

    isValid( (GeoPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::GeoPoint [,bool=True])

    isValid( (GeoEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > [,bool=True])

    isValid( (Geometry)geometry) -> bool :

        C++ signature :
            bool isValid(ad::map::point::Geometry)"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (ENUPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::ENUPoint [,bool=True])

    isValid( (ENUEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > [,bool=True])

    isValid( (ECEFPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::ECEFPoint [,bool=True])

    isValid( (ECEFEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > [,bool=True])

    isValid( (GeoPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::GeoPoint [,bool=True])

    isValid( (GeoEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > [,bool=True])

    isValid( (Geometry)geometry) -> bool :

        C++ signature :
            bool isValid(ad::map::point::Geometry)"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (ENUPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::ENUPoint [,bool=True])

    isValid( (ENUEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > [,bool=True])

    isValid( (ECEFPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::ECEFPoint [,bool=True])

    isValid( (ECEFEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > [,bool=True])

    isValid( (GeoPoint)point [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::point::GeoPoint [,bool=True])

    isValid( (GeoEdge)edge [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > [,bool=True])

    isValid( (Geometry)geometry) -> bool :

        C++ signature :
            bool isValid(ad::map::point::Geometry)"""
def normalizeENUHeading(ad) -> Any:
    """
    normalizeENUHeading( (ENUHeading)heading) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading normalizeENUHeading(ad::map::point::ENUHeading)"""
def radians2degree(double) -> Any:
    """
    radians2degree( (object)radians) -> float :

        C++ signature :
            double radians2degree(double)"""
@overload
def toECEF(ad) -> Any:
    """
    toECEF( (GeoPoint)point) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint toECEF(ad::map::point::GeoPoint)

    toECEF( (ENUPoint)point) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint toECEF(ad::map::point::ENUPoint)

    toECEF( (ENUPoint)point, (GeoPoint)enuReferencePoint) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint toECEF(ad::map::point::ENUPoint,ad::map::point::GeoPoint)

    toECEF( (GeoEdge)edge) -> ECEFEdge :

        C++ signature :
            std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > toECEF(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    toECEF( (ENUEdge)edge) -> ECEFEdge :

        C++ signature :
            std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > toECEF(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    toECEF( (ENUEdge)edge, (GeoPoint)enuReferencePoint) -> ECEFEdge :

        C++ signature :
            std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > toECEF(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >,ad::map::point::GeoPoint)"""
@overload
def toECEF(ad) -> Any:
    """
    toECEF( (GeoPoint)point) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint toECEF(ad::map::point::GeoPoint)

    toECEF( (ENUPoint)point) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint toECEF(ad::map::point::ENUPoint)

    toECEF( (ENUPoint)point, (GeoPoint)enuReferencePoint) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint toECEF(ad::map::point::ENUPoint,ad::map::point::GeoPoint)

    toECEF( (GeoEdge)edge) -> ECEFEdge :

        C++ signature :
            std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > toECEF(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    toECEF( (ENUEdge)edge) -> ECEFEdge :

        C++ signature :
            std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > toECEF(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    toECEF( (ENUEdge)edge, (GeoPoint)enuReferencePoint) -> ECEFEdge :

        C++ signature :
            std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > toECEF(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >,ad::map::point::GeoPoint)"""
@overload
def toENU(ad) -> Any:
    """
    toENU( (ECEFPoint)point) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint toENU(ad::map::point::ECEFPoint)

    toENU( (GeoPoint)point) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint toENU(ad::map::point::GeoPoint)

    toENU( (ECEFPoint)point, (GeoPoint)enuReferencePoint) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint toENU(ad::map::point::ECEFPoint,ad::map::point::GeoPoint)

    toENU( (GeoPoint)point, (GeoPoint)enuReferencePoint) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint toENU(ad::map::point::GeoPoint,ad::map::point::GeoPoint)

    toENU( (ECEFEdge)edge) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > toENU(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    toENU( (GeoEdge)edge) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > toENU(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    toENU( (ECEFEdge)edge, (GeoPoint)enuReferencePoint) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > toENU(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >,ad::map::point::GeoPoint)

    toENU( (GeoEdge)edge, (GeoPoint)enuReferencePoint) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > toENU(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >,ad::map::point::GeoPoint)"""
@overload
def toENU(ad) -> Any:
    """
    toENU( (ECEFPoint)point) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint toENU(ad::map::point::ECEFPoint)

    toENU( (GeoPoint)point) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint toENU(ad::map::point::GeoPoint)

    toENU( (ECEFPoint)point, (GeoPoint)enuReferencePoint) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint toENU(ad::map::point::ECEFPoint,ad::map::point::GeoPoint)

    toENU( (GeoPoint)point, (GeoPoint)enuReferencePoint) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint toENU(ad::map::point::GeoPoint,ad::map::point::GeoPoint)

    toENU( (ECEFEdge)edge) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > toENU(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    toENU( (GeoEdge)edge) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > toENU(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    toENU( (ECEFEdge)edge, (GeoPoint)enuReferencePoint) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > toENU(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >,ad::map::point::GeoPoint)

    toENU( (GeoEdge)edge, (GeoPoint)enuReferencePoint) -> ENUEdge :

        C++ signature :
            std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > toENU(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >,ad::map::point::GeoPoint)"""
@overload
def toGeo(ad) -> Any:
    """
    toGeo( (ECEFPoint)point) -> GeoPoint :

        C++ signature :
            ad::map::point::GeoPoint toGeo(ad::map::point::ECEFPoint)

    toGeo( (ENUPoint)point) -> GeoPoint :

        C++ signature :
            ad::map::point::GeoPoint toGeo(ad::map::point::ENUPoint)

    toGeo( (ENUPoint)point, (GeoPoint)enuReferencePoint) -> GeoPoint :

        C++ signature :
            ad::map::point::GeoPoint toGeo(ad::map::point::ENUPoint,ad::map::point::GeoPoint)

    toGeo( (ECEFEdge)edge) -> GeoEdge :

        C++ signature :
            std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > toGeo(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    toGeo( (ENUEdge)edge) -> GeoEdge :

        C++ signature :
            std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > toGeo(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    toGeo( (ENUEdge)edge, (GeoPoint)enuReferencePoint) -> GeoEdge :

        C++ signature :
            std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > toGeo(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >,ad::map::point::GeoPoint)"""
@overload
def toGeo(ad) -> Any:
    """
    toGeo( (ECEFPoint)point) -> GeoPoint :

        C++ signature :
            ad::map::point::GeoPoint toGeo(ad::map::point::ECEFPoint)

    toGeo( (ENUPoint)point) -> GeoPoint :

        C++ signature :
            ad::map::point::GeoPoint toGeo(ad::map::point::ENUPoint)

    toGeo( (ENUPoint)point, (GeoPoint)enuReferencePoint) -> GeoPoint :

        C++ signature :
            ad::map::point::GeoPoint toGeo(ad::map::point::ENUPoint,ad::map::point::GeoPoint)

    toGeo( (ECEFEdge)edge) -> GeoEdge :

        C++ signature :
            std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > toGeo(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    toGeo( (ENUEdge)edge) -> GeoEdge :

        C++ signature :
            std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > toGeo(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    toGeo( (ENUEdge)edge, (GeoPoint)enuReferencePoint) -> GeoEdge :

        C++ signature :
            std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > toGeo(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >,ad::map::point::GeoPoint)"""
@overload
def toRadians(ad) -> Any:
    """
    toRadians( (Latitude)latitude) -> float :

        C++ signature :
            double toRadians(ad::map::point::Latitude)

    toRadians( (Longitude)longitude) -> float :

        C++ signature :
            double toRadians(ad::map::point::Longitude)"""
@overload
def toRadians(ad) -> Any:
    """
    toRadians( (Latitude)latitude) -> float :

        C++ signature :
            double toRadians(ad::map::point::Latitude)

    toRadians( (Longitude)longitude) -> float :

        C++ signature :
            double toRadians(ad::map::point::Longitude)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (ECEFCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFCoordinate)

    to_string( (ECEFPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFPoint)

    to_string( (ECEFEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> >)

    to_string( (Altitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Altitude)

    to_string( (Latitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Latitude)

    to_string( (Longitude)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Longitude)

    to_string( (GeoPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::GeoPoint)

    to_string( (GeoEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >)

    to_string( (ENUCoordinate)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUCoordinate)

    to_string( (ENUPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUPoint)

    to_string( (ENUEdge)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> >)

    to_string( (ENUEdgeCache)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUEdgeCache)

    to_string( (ENUHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ENUHeading)

    to_string( (ParaPoint)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ParaPoint)

    to_string( (ParaPointList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> >)

    to_string( (BoundingSphere)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::BoundingSphere)

    to_string( (Geometry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::Geometry)

    to_string( (ECEFHeading)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::point::ECEFHeading)"""
def vectorAdd(*args, **kwargs):
    """
    vectorAdd( (ECEFPoint)a, (ECEFPoint)b) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint vectorAdd(ad::map::point::ECEFPoint,ad::map::point::ECEFPoint)

    vectorAdd( (ENUPoint)a, (ENUPoint)b) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint vectorAdd(ad::map::point::ENUPoint,ad::map::point::ENUPoint)

    vectorAdd( (ECEFHeading)a, (ECEFHeading)b) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading vectorAdd(ad::map::point::ECEFHeading,ad::map::point::ECEFHeading)"""
def vectorDotProduct(*args, **kwargs):
    """
    vectorDotProduct( (ECEFPoint)a, (ECEFPoint)b) -> float :

        C++ signature :
            double vectorDotProduct(ad::map::point::ECEFPoint,ad::map::point::ECEFPoint)

    vectorDotProduct( (ENUPoint)a, (ENUPoint)b) -> float :

        C++ signature :
            double vectorDotProduct(ad::map::point::ENUPoint,ad::map::point::ENUPoint)

    vectorDotProduct( (ECEFHeading)a, (ECEFHeading)b) -> float :

        C++ signature :
            double vectorDotProduct(ad::map::point::ECEFHeading,ad::map::point::ECEFHeading)"""
def vectorExtrapolate(*args, **kwargs):
    """
    vectorExtrapolate( (GeoPoint)a, (GeoPoint)b, (object)scalar) -> GeoPoint :

        C++ signature :
            ad::map::point::GeoPoint vectorExtrapolate(ad::map::point::GeoPoint,ad::map::point::GeoPoint,double)"""
@overload
def vectorLength(ad) -> Any:
    """
    vectorLength( (ECEFPoint)a) -> Distance :

        C++ signature :
            ad::physics::Distance vectorLength(ad::map::point::ECEFPoint)

    vectorLength( (ENUPoint)a) -> Distance :

        C++ signature :
            ad::physics::Distance vectorLength(ad::map::point::ENUPoint)"""
@overload
def vectorLength(ad) -> Any:
    """
    vectorLength( (ECEFPoint)a) -> Distance :

        C++ signature :
            ad::physics::Distance vectorLength(ad::map::point::ECEFPoint)

    vectorLength( (ENUPoint)a) -> Distance :

        C++ signature :
            ad::physics::Distance vectorLength(ad::map::point::ENUPoint)"""
@overload
def vectorMultiplyScalar(ad, double) -> Any:
    """
    vectorMultiplyScalar( (ECEFPoint)a, (object)b) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint vectorMultiplyScalar(ad::map::point::ECEFPoint,double)

    vectorMultiplyScalar( (ENUPoint)a, (object)b) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint vectorMultiplyScalar(ad::map::point::ENUPoint,double)

    vectorMultiplyScalar( (ECEFHeading)a, (object)b) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading vectorMultiplyScalar(ad::map::point::ECEFHeading,double)

    vectorMultiplyScalar( (ECEFPoint)a, (Distance)b) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint vectorMultiplyScalar(ad::map::point::ECEFPoint,ad::physics::Distance)

    vectorMultiplyScalar( (ENUPoint)a, (Distance)b) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint vectorMultiplyScalar(ad::map::point::ENUPoint,ad::physics::Distance)

    vectorMultiplyScalar( (ECEFHeading)a, (Distance)b) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading vectorMultiplyScalar(ad::map::point::ECEFHeading,ad::physics::Distance)"""
@overload
def vectorMultiplyScalar(ad, double) -> Any:
    """
    vectorMultiplyScalar( (ECEFPoint)a, (object)b) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint vectorMultiplyScalar(ad::map::point::ECEFPoint,double)

    vectorMultiplyScalar( (ENUPoint)a, (object)b) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint vectorMultiplyScalar(ad::map::point::ENUPoint,double)

    vectorMultiplyScalar( (ECEFHeading)a, (object)b) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading vectorMultiplyScalar(ad::map::point::ECEFHeading,double)

    vectorMultiplyScalar( (ECEFPoint)a, (Distance)b) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint vectorMultiplyScalar(ad::map::point::ECEFPoint,ad::physics::Distance)

    vectorMultiplyScalar( (ENUPoint)a, (Distance)b) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint vectorMultiplyScalar(ad::map::point::ENUPoint,ad::physics::Distance)

    vectorMultiplyScalar( (ECEFHeading)a, (Distance)b) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading vectorMultiplyScalar(ad::map::point::ECEFHeading,ad::physics::Distance)"""
@overload
def vectorMultiplyScalar(ad, double) -> Any:
    """
    vectorMultiplyScalar( (ECEFPoint)a, (object)b) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint vectorMultiplyScalar(ad::map::point::ECEFPoint,double)

    vectorMultiplyScalar( (ENUPoint)a, (object)b) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint vectorMultiplyScalar(ad::map::point::ENUPoint,double)

    vectorMultiplyScalar( (ECEFHeading)a, (object)b) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading vectorMultiplyScalar(ad::map::point::ECEFHeading,double)

    vectorMultiplyScalar( (ECEFPoint)a, (Distance)b) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint vectorMultiplyScalar(ad::map::point::ECEFPoint,ad::physics::Distance)

    vectorMultiplyScalar( (ENUPoint)a, (Distance)b) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint vectorMultiplyScalar(ad::map::point::ENUPoint,ad::physics::Distance)

    vectorMultiplyScalar( (ECEFHeading)a, (Distance)b) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading vectorMultiplyScalar(ad::map::point::ECEFHeading,ad::physics::Distance)"""
def vectorSub(*args, **kwargs):
    """
    vectorSub( (ECEFPoint)a, (ECEFPoint)b) -> ECEFPoint :

        C++ signature :
            ad::map::point::ECEFPoint vectorSub(ad::map::point::ECEFPoint,ad::map::point::ECEFPoint)

    vectorSub( (ENUPoint)a, (ENUPoint)b) -> ENUPoint :

        C++ signature :
            ad::map::point::ENUPoint vectorSub(ad::map::point::ENUPoint,ad::map::point::ENUPoint)

    vectorSub( (ECEFHeading)a, (ECEFHeading)b) -> ECEFHeading :

        C++ signature :
            ad::map::point::ECEFHeading vectorSub(ad::map::point::ECEFHeading,ad::map::point::ECEFHeading)"""
def zeroAltitude(ad) -> Any:
    """
    zeroAltitude( (GeoPoint)point) -> GeoPoint :

        C++ signature :
            ad::map::point::GeoPoint zeroAltitude(ad::map::point::GeoPoint)"""
