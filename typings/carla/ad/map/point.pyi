from typing import overload
from carla import ad
from . import *

class Altitude():
    @property
    def Valid(self) -> bool: ...

    def assign(self, arg1: Altitude, other: Altitude) -> Altitude:
        '''

        assign( (Altitude)arg1, (Altitude)other) -> Altitude :

            C++ signature :
                ad::map::point::Altitude {lvalue} assign(ad::map::point::Altitude {lvalue},ad::map::point::Altitude)
        '''
        ...

    cMaxValue = 1.7976931348623157e+308

    cMinValue = -1.7976931348623157e+308

    cPrecisionValue = 0.001

    def ensureValid(self, arg1: Altitude) -> None:
        '''

        ensureValid( (Altitude)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::Altitude {lvalue})
        '''
        ...

    def ensureValidNonZero(self, arg1: Altitude) -> None:
        '''

        ensureValidNonZero( (Altitude)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::Altitude {lvalue})
        '''
        ...

    def getMax(self, ) -> Altitude:
        '''

        getMax() -> Altitude :

            C++ signature :
                ad::map::point::Altitude getMax()
        '''
        ...

    def getMin(self, ) -> Altitude:
        '''

        getMin() -> Altitude :

            C++ signature :
                ad::map::point::Altitude getMin()
        '''
        ...

    def getPrecision(self, ) -> Altitude:
        '''

        getPrecision() -> Altitude :

            C++ signature :
                ad::map::point::Altitude getPrecision()
        '''
        ...


class BoundingSphere():
    def assign(self, arg1: BoundingSphere, other: BoundingSphere) -> BoundingSphere:
        '''

        assign( (BoundingSphere)arg1, (BoundingSphere)other) -> BoundingSphere :

            C++ signature :
                ad::map::point::BoundingSphere {lvalue} assign(ad::map::point::BoundingSphere {lvalue},ad::map::point::BoundingSphere)
        '''
        ...

    @property
    def center(self) -> ECEFPoint: ...

    @property
    def radius(self) -> ad.physics.Distance: ...


class CoordinateTransform():
    def ECEF2ENU(self, arg1: CoordinateTransform, pt: ECEFPoint) -> ENUPoint:
        '''

        ECEF2ENU( (CoordinateTransform)arg1, (ECEFPoint)pt) -> ENUPoint :

            C++ signature :
                ad::map::point::ENUPoint ECEF2ENU(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ECEFPoint)
        '''
        ...

    def ECEF2Geo(self, arg1: CoordinateTransform, pt: ECEFPoint) -> GeoPoint:
        '''

        ECEF2Geo( (CoordinateTransform)arg1, (ECEFPoint)pt) -> GeoPoint :

            C++ signature :
                ad::map::point::GeoPoint ECEF2Geo(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ECEFPoint)
        '''
        ...

    def ENU2ECEF(self, arg1: CoordinateTransform, pt: ENUPoint) -> ECEFPoint:
        '''

        ENU2ECEF( (CoordinateTransform)arg1, (ENUPoint)pt) -> ECEFPoint :

            C++ signature :
                ad::map::point::ECEFPoint ENU2ECEF(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ENUPoint)
        '''
        ...

    def ENU2Geo(self, arg1: CoordinateTransform, pt: ENUPoint) -> GeoPoint:
        '''

        ENU2Geo( (CoordinateTransform)arg1, (ENUPoint)pt) -> GeoPoint :

            C++ signature :
                ad::map::point::GeoPoint ENU2Geo(ad::map::point::CoordinateTransform {lvalue},ad::map::point::ENUPoint)
        '''
        ...

    @property
    def ENURef(self) -> int: ...

    @property
    def ENUReferencePoint(self) -> GeoPoint: ...

    @property
    def ENUValid(self) -> bool: ...

    def Geo2ECEF(self, arg1: CoordinateTransform, pt: GeoPoint) -> ECEFPoint:
        '''

        Geo2ECEF( (CoordinateTransform)arg1, (GeoPoint)pt) -> ECEFPoint :

            C++ signature :
                ad::map::point::ECEFPoint Geo2ECEF(ad::map::point::CoordinateTransform {lvalue},ad::map::point::GeoPoint)
        '''
        ...

    def Geo2ENU(self, arg1: CoordinateTransform, pt: GeoPoint) -> ENUPoint:
        '''

        Geo2ENU( (CoordinateTransform)arg1, (GeoPoint)pt) -> ENUPoint :

            C++ signature :
                ad::map::point::ENUPoint Geo2ENU(ad::map::point::CoordinateTransform {lvalue},ad::map::point::GeoPoint)
        '''
        ...

    def WGS84_R(self, lat: Latitude) -> ad.physics.Distance:
        '''

        WGS84_R( (Latitude)lat) -> Distance :

            C++ signature :
                ad::physics::Distance WGS84_R(ad::map::point::Latitude)
        '''
        ...

    # NOTE: Overloads might not be correct, # TODO

    @overload
    def convert(self, arg1: CoordinateTransform, x: ENUPoint, y: GeoPoint) -> None: 
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, x: GeoPoint, y: ECEFPoint) -> None:
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, x: ECEFPoint, y: GeoPoint) -> None:
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, x: ECEFPoint, y: ENUPoint) -> None:
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, x: ENUPoint, y: ECEFPoint) -> None:
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, x: GeoPoint, y: ENUPoint) -> None:
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, x: ENUPoint, y: GeoPoint) -> None:
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, xs: GeoEdge, ys: ECEFEdge) -> None:
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, xs: ENUEdge, ys: ECEFEdge) -> None:
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, xs: ECEFEdge, ys: GeoEdge) -> None:
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, xs: ENUEdge, ys: GeoEdge) -> None:
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, xs: ECEFEdge, ys: ENUEdge) -> None:
        ...

    @overload
    def convert(self, arg1: CoordinateTransform, xs: GeoEdge, ys: ENUEdge) -> None:
        ...

    def convert(self, arg1: CoordinateTransform, x, y) -> None:
        '''
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
                void convert(ad::map::point::CoordinateTransform {lvalue},std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> >,std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue})
        '''
        ...

    def geocentricLatitude(self, lat: Latitude) -> float:
        '''

        geocentricLatitude( (Latitude)lat) -> float :

            C++ signature :
                double geocentricLatitude(ad::map::point::Latitude)
        '''
        ...

    def setGeoProjection(self, arg1: CoordinateTransform, geo_projection: str) -> bool:
        '''

        setGeoProjection( (CoordinateTransform)arg1, (str)geo_projection) -> bool :

            C++ signature :
                bool setGeoProjection(ad::map::point::CoordinateTransform {lvalue},std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)
        '''
        ...


class ECEFCoordinate():
    @property
    def Valid(self) -> bool: ...

    def assign(self, arg1: ECEFCoordinate, other: ECEFCoordinate) -> ECEFCoordinate:
        '''

        assign( (ECEFCoordinate)arg1, (ECEFCoordinate)other) -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate {lvalue} assign(ad::map::point::ECEFCoordinate {lvalue},ad::map::point::ECEFCoordinate)
        '''
        ...

    cMaxValue = 1000000000.0

    cMinValue = -1000000000.0

    cPrecisionValue = 0.001

    def ensureValid(self, arg1: ECEFCoordinate) -> None:
        '''

        ensureValid( (ECEFCoordinate)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::ECEFCoordinate {lvalue})
        '''
        ...

    def ensureValidNonZero(self, arg1: ECEFCoordinate) -> None:
        '''

        ensureValidNonZero( (ECEFCoordinate)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::ECEFCoordinate {lvalue})
        '''
        ...

    def getMax(self, ) -> ECEFCoordinate:
        '''

        getMax() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate getMax()
        '''
        ...

    def getMin(self, ) -> ECEFCoordinate:
        '''

        getMin() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate getMin()
        '''
        ...

    def getPrecision(self, ) -> ECEFCoordinate:
        '''

        getPrecision() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate getPrecision()
        '''
        ...


class ECEFEdge():
    def append(self, arg1: ECEFEdge, arg2: ECEFPoint) -> None:
        '''

        append( (ECEFEdge)arg1, (ECEFPoint)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},ad::map::point::ECEFPoint)
        '''
        ...

    def count(self, arg1: ECEFEdge, arg2: ECEFPoint) -> int:
        '''

        count( (ECEFEdge)arg1, (ECEFPoint)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},ad::map::point::ECEFPoint)
        '''
        ...

    def extend(self, arg1: ECEFEdge, arg2: object) -> None:
        '''

        extend( (ECEFEdge)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},boost::python::api::object)
        '''
        ...

    def index(self, arg1: ECEFEdge, arg2: ECEFPoint) -> int:
        '''

        index( (ECEFEdge)arg1, (ECEFPoint)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},ad::map::point::ECEFPoint)
        '''
        ...

    def insert(self, arg1: ECEFEdge, arg2: int, arg3: ECEFPoint) -> None:
        '''

        insert( (ECEFEdge)arg1, (int)arg2, (ECEFPoint)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue},long,ad::map::point::ECEFPoint)
        '''
        ...

    def reverse(self, arg1: ECEFEdge) -> None:
        '''

        reverse( (ECEFEdge)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::point::ECEFPoint, std::allocator<ad::map::point::ECEFPoint> > {lvalue})
        '''
        ...


class ECEFHeading():
    def assign(self, arg1: ECEFHeading, other: ECEFHeading) -> ECEFHeading:
        '''

        assign( (ECEFHeading)arg1, (ECEFHeading)other) -> ECEFHeading :

            C++ signature :
                ad::map::point::ECEFHeading {lvalue} assign(ad::map::point::ECEFHeading {lvalue},ad::map::point::ECEFHeading)
        '''
        ...

    @property
    def x(self) -> ECEFCoordinate: ...

    @property
    def y(self) -> ECEFCoordinate: ...

    @property
    def z(self) -> ECEFCoordinate: ...


class ECEFPoint():
    def assign(self, arg1: ECEFPoint, other: ECEFPoint) -> ECEFPoint:
        '''

        assign( (ECEFPoint)arg1, (ECEFPoint)other) -> ECEFPoint :

            C++ signature :
                ad::map::point::ECEFPoint {lvalue} assign(ad::map::point::ECEFPoint {lvalue},ad::map::point::ECEFPoint)
        '''
        ...

    @property
    def x(self) -> ECEFCoordinate: ...

    @property
    def y(self) -> ECEFCoordinate: ...

    @property
    def z(self) -> ECEFCoordinate: ...


class ENUCoordinate():
    @property
    def Valid(self) -> bool: ...

    def assign(self, arg1: ENUCoordinate, other: ENUCoordinate) -> ENUCoordinate:
        '''

        assign( (ENUCoordinate)arg1, (ENUCoordinate)other) -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate {lvalue} assign(ad::map::point::ENUCoordinate {lvalue},ad::map::point::ENUCoordinate)
        '''
        ...

    cMaxValue = 1000000.0

    cMinValue = -1000000.0

    cPrecisionValue = 0.001

    def ensureValid(self, arg1: ENUCoordinate) -> None:
        '''

        ensureValid( (ENUCoordinate)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::ENUCoordinate {lvalue})
        '''
        ...

    def ensureValidNonZero(self, arg1: ENUCoordinate) -> None:
        '''

        ensureValidNonZero( (ENUCoordinate)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::ENUCoordinate {lvalue})
        '''
        ...

    def getMax(self, ) -> ENUCoordinate:
        '''

        getMax() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate getMax()
        '''
        ...

    def getMin(self, ) -> ENUCoordinate:
        '''

        getMin() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate getMin()
        '''
        ...

    def getPrecision(self, ) -> ENUCoordinate:
        '''

        getPrecision() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate getPrecision()
        '''
        ...


class ENUEdge():
    def append(self, arg1: ENUEdge, arg2: ENUPoint) -> None:
        '''

        append( (ENUEdge)arg1, (ENUPoint)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},ad::map::point::ENUPoint)
        '''
        ...

    def count(self, arg1: ENUEdge, arg2: ENUPoint) -> int:
        '''

        count( (ENUEdge)arg1, (ENUPoint)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},ad::map::point::ENUPoint)
        '''
        ...

    def extend(self, arg1: ENUEdge, arg2: object) -> None:
        '''

        extend( (ENUEdge)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},boost::python::api::object)
        '''
        ...

    def index(self, arg1: ENUEdge, arg2: ENUPoint) -> int:
        '''

        index( (ENUEdge)arg1, (ENUPoint)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},ad::map::point::ENUPoint)
        '''
        ...

    def insert(self, arg1: ENUEdge, arg2: int, arg3: ENUPoint) -> None:
        '''

        insert( (ENUEdge)arg1, (int)arg2, (ENUPoint)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue},long,ad::map::point::ENUPoint)
        '''
        ...

    def reverse(self, arg1: ENUEdge) -> None:
        '''

        reverse( (ENUEdge)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::point::ENUPoint, std::allocator<ad::map::point::ENUPoint> > {lvalue})
        '''
        ...


class ENUEdgeCache():
    def assign(self, arg1: ENUEdgeCache, other: ENUEdgeCache) -> ENUEdgeCache:
        '''

        assign( (ENUEdgeCache)arg1, (ENUEdgeCache)other) -> ENUEdgeCache :

            C++ signature :
                ad::map::point::ENUEdgeCache {lvalue} assign(ad::map::point::ENUEdgeCache {lvalue},ad::map::point::ENUEdgeCache)
        '''
        ...

    @property
    def enuEdge(self) -> ENUEdge: ...

    @property
    def enuVersion(self) -> int: ...


class ENUHeading():
    @property
    def Valid(self) -> bool: ...

    def assign(self, arg1: ENUHeading, other: ENUHeading) -> ENUHeading:
        '''

        assign( (ENUHeading)arg1, (ENUHeading)other) -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading {lvalue} assign(ad::map::point::ENUHeading {lvalue},ad::map::point::ENUHeading)
        '''
        ...

    cMaxValue = 1.7976931348623157e+308

    cMinValue = -1.7976931348623157e+308

    cPrecisionValue = 0.0001

    def ensureValid(self, arg1: ENUHeading) -> None:
        '''

        ensureValid( (ENUHeading)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::ENUHeading {lvalue})
        '''
        ...

    def ensureValidNonZero(self, arg1: ENUHeading) -> None:
        '''

        ensureValidNonZero( (ENUHeading)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::ENUHeading {lvalue})
        '''
        ...

    def getMax(self, ) -> ENUHeading:
        '''

        getMax() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading getMax()
        '''
        ...

    def getMin(self, ) -> ENUHeading:
        '''

        getMin() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading getMin()
        '''
        ...

    def getPrecision(self, ) -> ENUHeading:
        '''

        getPrecision() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading getPrecision()
        '''
        ...


class ENUPoint():
    def assign(self, arg1: ENUPoint, other: ENUPoint) -> ENUPoint:
        '''

        assign( (ENUPoint)arg1, (ENUPoint)other) -> ENUPoint :

            C++ signature :
                ad::map::point::ENUPoint {lvalue} assign(ad::map::point::ENUPoint {lvalue},ad::map::point::ENUPoint)
        '''
        ...

    @property
    def x(self) -> ENUCoordinate: ...

    @property
    def y(self) -> ENUCoordinate: ...

    @property
    def z(self) -> ENUCoordinate: ...


class GeoEdge():
    def append(self, arg1: GeoEdge, arg2: GeoPoint) -> None:
        '''

        append( (GeoEdge)arg1, (GeoPoint)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},ad::map::point::GeoPoint)
        '''
        ...

    def count(self, arg1: GeoEdge, arg2: GeoPoint) -> int:
        '''

        count( (GeoEdge)arg1, (GeoPoint)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},ad::map::point::GeoPoint)
        '''
        ...

    def extend(self, arg1: GeoEdge, arg2: object) -> None:
        '''

        extend( (GeoEdge)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},boost::python::api::object)
        '''
        ...

    def index(self, arg1: GeoEdge, arg2: GeoPoint) -> int:
        '''

        index( (GeoEdge)arg1, (GeoPoint)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},ad::map::point::GeoPoint)
        '''
        ...

    def insert(self, arg1: GeoEdge, arg2: int, arg3: GeoPoint) -> None:
        '''

        insert( (GeoEdge)arg1, (int)arg2, (GeoPoint)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue},long,ad::map::point::GeoPoint)
        '''
        ...

    def reverse(self, arg1: GeoEdge) -> None:
        '''

        reverse( (GeoEdge)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::point::GeoPoint, std::allocator<ad::map::point::GeoPoint> > {lvalue})
        '''
        ...


class GeoPoint():
    @property
    def altitude(self) -> Altitude: ...

    def assign(self, arg1: GeoPoint, other: GeoPoint) -> GeoPoint:
        '''

        assign( (GeoPoint)arg1, (GeoPoint)other) -> GeoPoint :

            C++ signature :
                ad::map::point::GeoPoint {lvalue} assign(ad::map::point::GeoPoint {lvalue},ad::map::point::GeoPoint)
        '''
        ...

    @property
    def latitude(self) -> Latitude: ...

    @property
    def longitude(self) -> Longitude: ...


class Geometry():
    def assign(self, arg1: Geometry, other: Geometry) -> Geometry:
        '''

        assign( (Geometry)arg1, (Geometry)other) -> Geometry :

            C++ signature :
                ad::map::point::Geometry {lvalue} assign(ad::map::point::Geometry {lvalue},ad::map::point::Geometry)
        '''
        ...

    @property
    def ecefEdge(self) -> ECEFEdge: ...

    @property
    def isClosed(self) -> bool: ...

    @property
    def isValid(self) -> bool: ...

    @property
    def length(self) -> ad.physics.Distance: ...

    @property
    def private_enuEdgeCache(self) -> ENUEdgeCache: ...


class Latitude():
    @property
    def Valid(self) -> bool: ...

    def assign(self, arg1: Latitude, other: Latitude) -> Latitude:
        '''

        assign( (Latitude)arg1, (Latitude)other) -> Latitude :

            C++ signature :
                ad::map::point::Latitude {lvalue} assign(ad::map::point::Latitude {lvalue},ad::map::point::Latitude)
        '''
        ...

    cMaxValue = 1.7976931348623157e+308

    cMinValue = -1.7976931348623157e+308

    cPrecisionValue = 1e-08

    def ensureValid(self, arg1: Latitude) -> None:
        '''

        ensureValid( (Latitude)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::Latitude {lvalue})
        '''
        ...

    def ensureValidNonZero(self, arg1: Latitude) -> None:
        '''

        ensureValidNonZero( (Latitude)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::Latitude {lvalue})
        '''
        ...

    def getMax(self, ) -> Latitude:
        '''

        getMax() -> Latitude :

            C++ signature :
                ad::map::point::Latitude getMax()
        '''
        ...

    def getMin(self, ) -> Latitude:
        '''

        getMin() -> Latitude :

            C++ signature :
                ad::map::point::Latitude getMin()
        '''
        ...

    def getPrecision(self, ) -> Latitude:
        '''

        getPrecision() -> Latitude :

            C++ signature :
                ad::map::point::Latitude getPrecision()
        '''
        ...


class Longitude():
    @property
    def Valid(self) -> bool: ...

    def assign(self, arg1: Longitude, other: Longitude) -> Longitude:
        '''

        assign( (Longitude)arg1, (Longitude)other) -> Longitude :

            C++ signature :
                ad::map::point::Longitude {lvalue} assign(ad::map::point::Longitude {lvalue},ad::map::point::Longitude)
        '''
        ...

    cMaxValue = 1.7976931348623157e+308

    cMinValue = -1.7976931348623157e+308

    cPrecisionValue = 1e-08

    def ensureValid(self, arg1: Longitude) -> None:
        '''

        ensureValid( (Longitude)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::point::Longitude {lvalue})
        '''
        ...

    def ensureValidNonZero(self, arg1: Longitude) -> None:
        '''

        ensureValidNonZero( (Longitude)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::point::Longitude {lvalue})
        '''
        ...

    def getMax(self, ) -> Longitude:
        '''

        getMax() -> Longitude :

            C++ signature :
                ad::map::point::Longitude getMax()
        '''
        ...

    def getMin(self, ) -> Longitude:
        '''

        getMin() -> Longitude :

            C++ signature :
                ad::map::point::Longitude getMin()
        '''
        ...

    def getPrecision(self, ) -> Longitude:
        '''

        getPrecision() -> Longitude :

            C++ signature :
                ad::map::point::Longitude getPrecision()
        '''
        ...


class ParaPoint():
    def assign(self, arg1: ParaPoint, other: ParaPoint) -> ParaPoint:
        '''

        assign( (ParaPoint)arg1, (ParaPoint)other) -> ParaPoint :

            C++ signature :
                ad::map::point::ParaPoint {lvalue} assign(ad::map::point::ParaPoint {lvalue},ad::map::point::ParaPoint)
        '''
        ...

    @property
    def laneId(self) -> lane.LaneId: ...

    @property
    def parametricOffset(self) -> ad.physics.ParametricValue: ...


class ParaPointList():
    def append(self, arg1: ParaPointList, arg2: ParaPoint) -> None:
        '''

        append( (ParaPointList)arg1, (ParaPoint)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},ad::map::point::ParaPoint)
        '''
        ...

    def count(self, arg1: ParaPointList, arg2: ParaPoint) -> int:
        '''

        count( (ParaPointList)arg1, (ParaPoint)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},ad::map::point::ParaPoint)
        '''
        ...

    def extend(self, arg1: ParaPointList, arg2: object) -> None:
        '''

        extend( (ParaPointList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},boost::python::api::object)
        '''
        ...

    def index(self, arg1: ParaPointList, arg2: ParaPoint) -> int:
        '''

        index( (ParaPointList)arg1, (ParaPoint)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},ad::map::point::ParaPoint)
        '''
        ...

    def insert(self, arg1: ParaPointList, arg2: int, arg3: ParaPoint) -> None:
        '''

        insert( (ParaPointList)arg1, (int)arg2, (ParaPoint)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue},long,ad::map::point::ParaPoint)
        '''
        ...

    def reverse(self, arg1: ParaPointList) -> None:
        '''

        reverse( (ParaPointList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::point::ParaPoint, std::allocator<ad::map::point::ParaPoint> > {lvalue})
        '''
        ...


class numeric_limits_less__ad_scope_map_scope_point_scope_Altitude__greater_():
    def epsilon(self, ) -> Altitude:
        '''

        epsilon() -> Altitude :

            C++ signature :
                ad::map::point::Altitude epsilon()
        '''
        ...

    def lowest(self, ) -> Altitude:
        '''

        lowest() -> Altitude :

            C++ signature :
                ad::map::point::Altitude lowest()
        '''
        ...

    def max(self, ) -> Altitude:
        '''

        max() -> Altitude :

            C++ signature :
                ad::map::point::Altitude max()
        '''
        ...


class numeric_limits_less__ad_scope_map_scope_point_scope_ECEFCoordinate__greater_():
    def epsilon(self, ) -> ECEFCoordinate:
        '''

        epsilon() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate epsilon()
        '''
        ...

    def lowest(self, ) -> ECEFCoordinate:
        '''

        lowest() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate lowest()
        '''
        ...

    def max(self, ) -> ECEFCoordinate:
        '''

        max() -> ECEFCoordinate :

            C++ signature :
                ad::map::point::ECEFCoordinate max()
        '''
        ...


class numeric_limits_less__ad_scope_map_scope_point_scope_ENUCoordinate__greater_():
    def epsilon(self, ) -> ENUCoordinate:
        '''

        epsilon() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate epsilon()
        '''
        ...

    def lowest(self, ) -> ENUCoordinate:
        '''

        lowest() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate lowest()
        '''
        ...

    def max(self, ) -> ENUCoordinate:
        '''

        max() -> ENUCoordinate :

            C++ signature :
                ad::map::point::ENUCoordinate max()
        '''
        ...


class numeric_limits_less__ad_scope_map_scope_point_scope_ENUHeading__greater_():
    def epsilon(self, ) -> ENUHeading:
        '''

        epsilon() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading epsilon()
        '''
        ...

    def lowest(self, ) -> ENUHeading:
        '''

        lowest() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading lowest()
        '''
        ...

    def max(self, ) -> ENUHeading:
        '''

        max() -> ENUHeading :

            C++ signature :
                ad::map::point::ENUHeading max()
        '''
        ...


class numeric_limits_less__ad_scope_map_scope_point_scope_Latitude__greater_():
    def epsilon(self, ) -> Latitude:
        '''

        epsilon() -> Latitude :

            C++ signature :
                ad::map::point::Latitude epsilon()
        '''
        ...

    def lowest(self, ) -> Latitude:
        '''

        lowest() -> Latitude :

            C++ signature :
                ad::map::point::Latitude lowest()
        '''
        ...

    def max(self, ) -> Latitude:
        '''

        max() -> Latitude :

            C++ signature :
                ad::map::point::Latitude max()
        '''
        ...


class numeric_limits_less__ad_scope_map_scope_point_scope_Longitude__greater_():
    def epsilon(self, ) -> Longitude:
        '''

        epsilon() -> Longitude :

            C++ signature :
                ad::map::point::Longitude epsilon()
        '''
        ...

    def lowest(self, ) -> Longitude:
        '''

        lowest() -> Longitude :

            C++ signature :
                ad::map::point::Longitude lowest()
        '''
        ...

    def max(self, ) -> Longitude:
        '''

        max() -> Longitude :

            C++ signature :
                ad::map::point::Longitude max()
        '''
        ...
