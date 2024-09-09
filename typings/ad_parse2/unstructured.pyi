import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar

class DebugDrawing(Boost.Python.instance):
    class DebugLine(Boost.Python.instance):
        __instance_size__: ClassVar[int] = ...
        color: Incomplete
        line: Incomplete
        ns: Incomplete
        @classmethod
        def __init__(cls, *args, **kwargs) -> None:
            """
            __init__( (object)arg1, (object)iLine, (str)iColor, (str)iNs) -> None :

                C++ signature :
                    void __init__(_object*,boost::geometry::model::linestring<boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>, std::vector, std::allocator>,std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >,std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
        @classmethod
        def getVector(cls, ad) -> Any:
            """
            getVector( (DebugLine)arg1) -> vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_ :

                C++ signature :
                    std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > getVector(ad::rss::unstructured::DebugDrawing::DebugLine {lvalue})"""
        @classmethod
        def __reduce__(cls): ...

    class DebugPoint(Boost.Python.instance):
        __instance_size__: ClassVar[int] = ...
        x: Incomplete
        y: Incomplete
        @classmethod
        def __init__(cls, *args, **kwargs) -> None:
            """
            __init__( (object)arg1, (object)inX, (object)inY) -> None :

                C++ signature :
                    void __init__(_object*,double,double)"""
        @classmethod
        def __reduce__(cls): ...

    class DebugPolygon(Boost.Python.instance):
        __instance_size__: ClassVar[int] = ...
        color: Incomplete
        ns: Incomplete
        polygon: Incomplete
        @classmethod
        def __init__(cls, *args, **kwargs) -> None:
            """
            __init__( (object)arg1, (object)iPolygon, (str)iColor, (str)iNs) -> None :

                C++ signature :
                    void __init__(_object*,boost::geometry::model::polygon<boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>, false, true, std::vector, std::vector, std::allocator, std::allocator>,std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >,std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
        @classmethod
        def getVector(cls, ad) -> Any:
            """
            getVector( (DebugPolygon)arg1) -> vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_ :

                C++ signature :
                    std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > getVector(ad::rss::unstructured::DebugDrawing::DebugPolygon {lvalue})"""
        @classmethod
        def __reduce__(cls): ...

    class NullDeleter(Boost.Python.instance):
        __instance_size__: ClassVar[int] = ...
        @classmethod
        def __init__(cls, *args, **kwargs) -> None:
            """
            __init__( (object)arg1) -> None :

                C++ signature :
                    void __init__(_object*)"""
        @classmethod
        def __call__(cls, *args, **kwargs):
            """
            __call__( (NullDeleter)arg1, (object)arg0) -> None :

                C++ signature :
                    void __call__(ad::rss::unstructured::DebugDrawing::NullDeleter {lvalue},void const*)"""
        @classmethod
        def __reduce__(cls): ...
    __instance_size__: ClassVar[int] = ...
    mEnabled: Incomplete
    mLines: Incomplete
    mPolygons: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def drawLine(cls, *args, **kwargs):
        """
        drawLine( (DebugDrawing)arg1, (object)line [, (str)color='white' [, (str)ns='']]) -> None :

            C++ signature :
                void drawLine(ad::rss::unstructured::DebugDrawing {lvalue},boost::geometry::model::linestring<boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>, std::vector, std::allocator> [,std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >='white' [,std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >='']])"""
    @classmethod
    def drawPolygon(cls, *args, **kwargs):
        """
        drawPolygon( (DebugDrawing)arg1, (object)polygon [, (str)color='white' [, (str)ns='']]) -> None :

            C++ signature :
                void drawPolygon(ad::rss::unstructured::DebugDrawing {lvalue},boost::geometry::model::polygon<boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>, false, true, std::vector, std::vector, std::allocator, std::allocator> [,std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >='white' [,std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >='']])"""
    @classmethod
    def enable(cls, ad, bool) -> Any:
        """
        enable( (DebugDrawing)arg1, (bool)value) -> None :

            C++ signature :
                void enable(ad::rss::unstructured::DebugDrawing {lvalue},bool)"""
    @staticmethod
    def getInstance() -> Any:
        """
        getInstance() -> DebugDrawing :

            C++ signature :
                std::shared_ptr<ad::rss::unstructured::DebugDrawing> getInstance()"""
    @classmethod
    def isEnabled(cls, ad) -> Any:
        """
        isEnabled( (DebugDrawing)arg1) -> bool :

            C++ signature :
                bool isEnabled(ad::rss::unstructured::DebugDrawing {lvalue})"""
    @classmethod
    def reset(cls, ad) -> Any:
        """
        reset( (DebugDrawing)arg1) -> None :

            C++ signature :
                void reset(ad::rss::unstructured::DebugDrawing {lvalue})"""
    @classmethod
    def __reduce__(cls): ...

class vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_(Boost.Python.instance):
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
        append( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_)arg1, (DebugLine)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::rss::unstructured::DebugDrawing::DebugLine, std::allocator<ad::rss::unstructured::DebugDrawing::DebugLine> > {lvalue},ad::rss::unstructured::DebugDrawing::DebugLine)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::rss::unstructured::DebugDrawing::DebugLine, std::allocator<ad::rss::unstructured::DebugDrawing::DebugLine> > {lvalue},boost::python::api::object)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_)arg1, (int)arg2, (DebugLine)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::rss::unstructured::DebugDrawing::DebugLine, std::allocator<ad::rss::unstructured::DebugDrawing::DebugLine> > {lvalue},long,ad::rss::unstructured::DebugDrawing::DebugLine)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::rss::unstructured::DebugDrawing::DebugLine, std::allocator<ad::rss::unstructured::DebugDrawing::DebugLine> > {lvalue})"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugLine, std::allocator<ad::rss::unstructured::DebugDrawing::DebugLine> > {lvalue},long)

        __delitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugLine, std::allocator<ad::rss::unstructured::DebugDrawing::DebugLine> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_)arg1, (int)arg2) -> DebugLine :

            C++ signature :
                ad::rss::unstructured::DebugDrawing::DebugLine {lvalue} __getitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugLine, std::allocator<ad::rss::unstructured::DebugDrawing::DebugLine> > {lvalue},long)

        __getitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugLine, std::allocator<ad::rss::unstructured::DebugDrawing::DebugLine> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::rss::unstructured::DebugDrawing::DebugLine, std::allocator<ad::rss::unstructured::DebugDrawing::DebugLine> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_)arg1, (int)arg2, (DebugLine)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugLine, std::allocator<ad::rss::unstructured::DebugDrawing::DebugLine> > {lvalue},long,ad::rss::unstructured::DebugDrawing::DebugLine)

        __setitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugLine_greater_)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugLine, std::allocator<ad::rss::unstructured::DebugDrawing::DebugLine> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_(Boost.Python.instance):
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
        append( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_)arg1, (DebugPoint)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > {lvalue},ad::rss::unstructured::DebugDrawing::DebugPoint)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > {lvalue},boost::python::api::object)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_)arg1, (int)arg2, (DebugPoint)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > {lvalue},long,ad::rss::unstructured::DebugDrawing::DebugPoint)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > {lvalue})"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > {lvalue},long)

        __delitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_)arg1, (int)arg2) -> DebugPoint :

            C++ signature :
                ad::rss::unstructured::DebugDrawing::DebugPoint {lvalue} __getitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > {lvalue},long)

        __getitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_)arg1, (int)arg2, (DebugPoint)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > {lvalue},long,ad::rss::unstructured::DebugDrawing::DebugPoint)

        __setitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPoint_greater_)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPoint, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPoint> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_(Boost.Python.instance):
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
        append( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_)arg1, (DebugPolygon)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::rss::unstructured::DebugDrawing::DebugPolygon, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPolygon> > {lvalue},ad::rss::unstructured::DebugDrawing::DebugPolygon)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::rss::unstructured::DebugDrawing::DebugPolygon, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPolygon> > {lvalue},boost::python::api::object)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_)arg1, (int)arg2, (DebugPolygon)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::rss::unstructured::DebugDrawing::DebugPolygon, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPolygon> > {lvalue},long,ad::rss::unstructured::DebugDrawing::DebugPolygon)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::rss::unstructured::DebugDrawing::DebugPolygon, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPolygon> > {lvalue})"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPolygon, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPolygon> > {lvalue},long)

        __delitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPolygon, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPolygon> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_)arg1, (int)arg2) -> DebugPolygon :

            C++ signature :
                ad::rss::unstructured::DebugDrawing::DebugPolygon {lvalue} __getitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPolygon, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPolygon> > {lvalue},long)

        __getitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPolygon, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPolygon> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPolygon, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPolygon> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_)arg1, (int)arg2, (DebugPolygon)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPolygon, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPolygon> > {lvalue},long,ad::rss::unstructured::DebugDrawing::DebugPolygon)

        __setitem__( (vector_less_ad_scope_rss_scope_unstructured_scope_DebugDrawing_scope_DebugPolygon_greater_)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::rss::unstructured::DebugDrawing::DebugPolygon, std::allocator<ad::rss::unstructured::DebugDrawing::DebugPolygon> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

def collides(*args, **kwargs):
    """
    collides( (Distance2DList)trajectorySet1, (Distance2DList)trajectorySet2) -> bool :

        C++ signature :
            bool collides(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >,std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >)"""
def combinePolygon(*args, **kwargs):
    """
    combinePolygon( (object)a, (object)b, (object)result) -> bool :

        C++ signature :
            bool combinePolygon(boost::geometry::model::polygon<boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>, false, true, std::vector, std::vector, std::allocator, std::allocator>,boost::geometry::model::polygon<boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>, false, true, std::vector, std::vector, std::allocator, std::allocator>,boost::geometry::model::polygon<boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>, false, true, std::vector, std::vector, std::allocator, std::allocator> {lvalue})"""
def getCircleOrigin(*args, **kwargs):
    """
    getCircleOrigin( (object)point, (Distance)radius, (Angle)angle) -> object :

        C++ signature :
            boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian> getCircleOrigin(boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>,ad::physics::Distance,ad::physics::Angle)"""
def getHeadingOverlap(*args, **kwargs):
    """
    getHeadingOverlap( (HeadingRange)a, (HeadingRange)b, (HeadingRangeVector)overlapRanges) -> bool :

        C++ signature :
            bool getHeadingOverlap(ad::rss::state::HeadingRange,ad::rss::state::HeadingRange,std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue})

    getHeadingOverlap( (HeadingRange)headingRange, (HeadingRangeVector)overlapRanges) -> bool :

        C++ signature :
            bool getHeadingOverlap(ad::rss::state::HeadingRange,std::vector<ad::rss::state::HeadingRange, std::allocator<ad::rss::state::HeadingRange> > {lvalue})"""
def getPointOnCircle(*args, **kwargs):
    """
    getPointOnCircle( (object)origin, (Distance)radius, (Angle)angle) -> object :

        C++ signature :
            boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian> getPointOnCircle(boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>,ad::physics::Distance,ad::physics::Angle)"""
def isInsideHeadingRange(*args, **kwargs):
    """
    isInsideHeadingRange( (Angle)angle, (HeadingRange)range) -> bool :

        C++ signature :
            bool isInsideHeadingRange(ad::physics::Angle,ad::rss::state::HeadingRange)"""
def rotateAroundPoint(*args, **kwargs):
    """
    rotateAroundPoint( (object)origin, (object)relativePoint, (Angle)angle) -> object :

        C++ signature :
            boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian> rotateAroundPoint(boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>,boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>,ad::physics::Angle)"""
def toDistance(*args, **kwargs):
    """
    toDistance( (object)point) -> Distance2D :

        C++ signature :
            ad::physics::Distance2D toDistance(boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>)"""
def toPoint(ad) -> Any:
    """
    toPoint( (Distance2D)distance) -> object :

        C++ signature :
            boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian> toPoint(ad::physics::Distance2D)

    toPoint( (Distance)distanceX, (Distance)distanceY) -> object :

        C++ signature :
            boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian> toPoint(ad::physics::Distance,ad::physics::Distance)"""
def toPolygon(*args, **kwargs):
    """
    toPolygon( (Distance2DList)trajectorySet, (object)polygon) -> None :

        C++ signature :
            void toPolygon(std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> >,boost::geometry::model::polygon<boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>, false, true, std::vector, std::vector, std::allocator, std::allocator> {lvalue})"""
def toTrajectorySet(*args, **kwargs):
    """
    toTrajectorySet( (object)polygon, (Distance2DList)trajectorySet) -> None :

        C++ signature :
            void toTrajectorySet(boost::geometry::model::polygon<boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>, false, true, std::vector, std::vector, std::allocator, std::allocator>,std::vector<ad::physics::Distance2D, std::allocator<ad::physics::Distance2D> > {lvalue})"""
def to_string(*args, **kwargs):
    """
    to_string( (object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>)

    to_string( (object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(boost::geometry::model::polygon<boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>, false, true, std::vector, std::vector, std::allocator, std::allocator>)

    to_string( (object)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(boost::geometry::model::linestring<boost::geometry::model::d2::point_xy<double, boost::geometry::cs::cartesian>, std::vector, std::allocator>)"""
