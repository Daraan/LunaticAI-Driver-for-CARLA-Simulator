import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

ACCESS_FORBIDDEN: TrafficSignType
ACCESS_FORBIDDEN_BICYCLE: TrafficSignType
ACCESS_FORBIDDEN_HEIGHT: TrafficSignType
ACCESS_FORBIDDEN_MOTORVEHICLES: TrafficSignType
ACCESS_FORBIDDEN_TRUCKS: TrafficSignType
ACCESS_FORBIDDEN_WEIGHT: TrafficSignType
ACCESS_FORBIDDEN_WIDTH: TrafficSignType
ACCESS_FORBIDDEN_WRONG_DIR: TrafficSignType
BIKE_PEDESTRIAN_RED_GREEN: TrafficLightType
BIKE_PEDESTRIAN_RED_YELLOW_GREEN: TrafficLightType
BIKE_RED_GREEN: TrafficLightType
BIKE_RED_YELLOW_GREEN: TrafficLightType
BOLLARD: LandmarkType
BYBICLE_PATH: TrafficSignType
CAUTION_ANIMALS: TrafficSignType
CAUTION_BICYCLE: TrafficSignType
CAUTION_CHILDREN: TrafficSignType
CAUTION_PEDESTRIAN: TrafficSignType
CAUTION_RAIL_CROSSING: TrafficSignType
CAUTION_RAIL_CROSSING_WITH_BARRIER: TrafficSignType
CITY_BEGIN: TrafficSignType
CITY_END: TrafficSignType
CUL_DE_SAC: TrafficSignType
CUL_DE_SAC_EXCEPT_PED_BICYCLE: TrafficSignType
DANGER: TrafficSignType
DESTINATION_BOARD: TrafficSignType
DIRECTION_TURN_TO_AUTOBAHN: TrafficSignType
DIRECTION_TURN_TO_LOCAL: TrafficSignType
ENVIORNMENT_ZONE_BEGIN: TrafficSignType
ENVIORNMENT_ZONE_END: TrafficSignType
FIRE_HYDRANT: LandmarkType
FOOTWALK: TrafficSignType
FOOTWALK_BICYCLE_SEP_LEFT: TrafficSignType
FOOTWALK_BICYCLE_SEP_RIGHT: TrafficSignType
FOOTWALK_BICYCLE_SHARED: TrafficSignType
FREE_TEXT: TrafficSignType
GUIDE_POST: LandmarkType
HAS_WAY_NEXT_INTERSECTION: TrafficSignType
INFO_MOTORWAY_INFO: TrafficSignType
INFO_NUMBER_OF_AUTOBAHN: TrafficSignType
INVALID: TrafficSignType
LANES_MERGING: TrafficSignType
LEFT_RED_YELLOW_GREEN: TrafficLightType
LEFT_STRAIGHT_RED_YELLOW_GREEN: TrafficLightType
MANHOLE: LandmarkType
MAX_SPEED: TrafficSignType
MOTORVEHICLE_BEGIN: TrafficSignType
MOTORVEHICLE_END: TrafficSignType
MOTORWAY_BEGIN: TrafficSignType
MOTORWAY_END: TrafficSignType
OTHER: LandmarkType
PASS_LEFT: TrafficSignType
PASS_RIGHT: TrafficSignType
PEDESTRIAN_AREA_BEGIN: TrafficSignType
PEDESTRIAN_RED_GREEN: TrafficLightType
PEDESTRIAN_RED_YELLOW_GREEN: TrafficLightType
POLE: LandmarkType
POSTBOX: LandmarkType
POWERCABINET: LandmarkType
PRIORITY_WAY: TrafficSignType
REQUIRED_LEFT_TURN: TrafficSignType
REQUIRED_RIGHT_TURN: TrafficSignType
REQUIRED_STRAIGHT: TrafficSignType
REQUIRED_STRAIGHT_OR_LEFT_TURN: TrafficSignType
REQUIRED_STRAIGHT_OR_RIGHT_TURN: TrafficSignType
RIGHT_RED_YELLOW_GREEN: TrafficLightType
RIGHT_STRAIGHT_RED_YELLOW_GREEN: TrafficLightType
ROUNDABOUT: TrafficSignType
SOLID_RED_YELLOW: TrafficLightType
SOLID_RED_YELLOW_GREEN: TrafficLightType
SPEED_ZONE_30_BEGIN: TrafficSignType
SPEED_ZONE_30_END: TrafficSignType
STOP: TrafficSignType
STRAIGHT_RED_YELLOW_GREEN: TrafficLightType
STREET_LAMP: LandmarkType
SUPPLEMENT_APPLIES_FOR_WEIGHT: TrafficSignType
SUPPLEMENT_APPLIES_NEXT_N_KM_TIME: TrafficSignType
SUPPLEMENT_ARROW_APPLIES_LEFT: TrafficSignType
SUPPLEMENT_ARROW_APPLIES_LEFT_RIGHT: TrafficSignType
SUPPLEMENT_ARROW_APPLIES_LEFT_RIGHT_BICYCLE: TrafficSignType
SUPPLEMENT_ARROW_APPLIES_RIGHT: TrafficSignType
SUPPLEMENT_ARROW_APPLIES_UP_DOWN: TrafficSignType
SUPPLEMENT_ARROW_APPLIES_UP_DOWN_BICYCLE: TrafficSignType
SUPPLEMENT_BICYCLE_ALLOWED: TrafficSignType
SUPPLEMENT_CONSTRUCTION_VEHICLE_ALLOWED: TrafficSignType
SUPPLEMENT_ENDS: TrafficSignType
SUPPLEMENT_ENVIRONMENT_ZONE_YELLOW_GREEN: TrafficSignType
SUPPLEMENT_FORESTAL_ALLOWED: TrafficSignType
SUPPLEMENT_MOPED_ALLOWED: TrafficSignType
SUPPLEMENT_RAILWAY_ONLY: TrafficSignType
SUPPLEMENT_RESIDENTS_ALLOWED: TrafficSignType
SUPPLEMENT_TRAM_ALLOWED: TrafficSignType
TRAFFIC_LIGHT: LandmarkType
TRAFFIC_SIGN: LandmarkType
TREE: LandmarkType
UNKNOWN: TrafficSignType
YIELD: TrafficSignType
YIELD_TRAIN: TrafficSignType

class ENULandmark(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    heading: Incomplete
    id: Incomplete
    position: Incomplete
    trafficLightType: Incomplete
    type: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (ENULandmark)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::landmark::ENULandmark)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (ENULandmark)arg1, (ENULandmark)other) -> ENULandmark :

            C++ signature :
                ad::map::landmark::ENULandmark {lvalue} assign(ad::map::landmark::ENULandmark {lvalue},ad::map::landmark::ENULandmark)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (ENULandmark)arg1, (ENULandmark)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::landmark::ENULandmark {lvalue},ad::map::landmark::ENULandmark)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (ENULandmark)arg1, (ENULandmark)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::landmark::ENULandmark {lvalue},ad::map::landmark::ENULandmark)"""
    @classmethod
    def __reduce__(cls): ...

class ENULandmarkList(Boost.Python.instance):
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
        append( (ENULandmarkList)arg1, (ENULandmark)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},ad::map::landmark::ENULandmark)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (ENULandmarkList)arg1, (ENULandmark)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},ad::map::landmark::ENULandmark)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (ENULandmarkList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (ENULandmarkList)arg1, (ENULandmark)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},ad::map::landmark::ENULandmark)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (ENULandmarkList)arg1, (int)arg2, (ENULandmark)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},long,ad::map::landmark::ENULandmark)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (ENULandmarkList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (ENULandmarkList)arg1, (ENULandmark)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},ad::map::landmark::ENULandmark)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (ENULandmarkList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},long)

        __delitem__( (ENULandmarkList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (ENULandmarkList)arg1, (int)arg2) -> ENULandmark :

            C++ signature :
                ad::map::landmark::ENULandmark {lvalue} __getitem__(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},long)

        __getitem__( (ENULandmarkList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (ENULandmarkList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (ENULandmarkList)arg1, (int)arg2, (ENULandmark)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},long,ad::map::landmark::ENULandmark)

        __setitem__( (ENULandmarkList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class Landmark(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    boundingBox: Incomplete
    id: Incomplete
    orientation: Incomplete
    position: Incomplete
    supplementaryText: Incomplete
    trafficLightType: Incomplete
    trafficSignType: Incomplete
    type: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (Landmark)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::landmark::Landmark)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (Landmark)arg1, (Landmark)other) -> Landmark :

            C++ signature :
                ad::map::landmark::Landmark {lvalue} assign(ad::map::landmark::Landmark {lvalue},ad::map::landmark::Landmark)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (Landmark)arg1, (Landmark)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::landmark::Landmark {lvalue},ad::map::landmark::Landmark)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (Landmark)arg1, (Landmark)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::landmark::Landmark {lvalue},ad::map::landmark::Landmark)"""
    @classmethod
    def __reduce__(cls): ...

class LandmarkId(Boost.Python.instance):
    cMaxValue: ClassVar[int] = ...  # read-only
    cMinValue: ClassVar[int] = ...  # read-only
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (object)iLandmarkId) -> None :

            C++ signature :
                void __init__(_object*,unsigned long)

        __init__( (object)arg1, (LandmarkId)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::landmark::LandmarkId)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (LandmarkId)arg1, (LandmarkId)other) -> LandmarkId :

            C++ signature :
                ad::map::landmark::LandmarkId {lvalue} assign(ad::map::landmark::LandmarkId {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def ensureValid(cls, ad) -> Any:
        """
        ensureValid( (LandmarkId)arg1) -> None :

            C++ signature :
                void ensureValid(ad::map::landmark::LandmarkId {lvalue})"""
    @classmethod
    def ensureValidNonZero(cls, ad) -> Any:
        """
        ensureValidNonZero( (LandmarkId)arg1) -> None :

            C++ signature :
                void ensureValidNonZero(ad::map::landmark::LandmarkId {lvalue})"""
    @staticmethod
    def getMax() -> Any:
        """
        getMax() -> LandmarkId :

            C++ signature :
                ad::map::landmark::LandmarkId getMax()"""
    @staticmethod
    def getMin() -> Any:
        """
        getMin() -> LandmarkId :

            C++ signature :
                ad::map::landmark::LandmarkId getMin()"""
    @classmethod
    def __add__(cls, other):
        """
        __add__( (LandmarkId)arg1, (LandmarkId)arg2) -> object :

            C++ signature :
                _object* __add__(ad::map::landmark::LandmarkId {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (LandmarkId)arg1, (LandmarkId)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::landmark::LandmarkId {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __ge__(cls, other: object) -> bool:
        """
        __ge__( (LandmarkId)arg1, (LandmarkId)arg2) -> object :

            C++ signature :
                _object* __ge__(ad::map::landmark::LandmarkId {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __gt__(cls, other: object) -> bool:
        """
        __gt__( (LandmarkId)arg1, (LandmarkId)arg2) -> object :

            C++ signature :
                _object* __gt__(ad::map::landmark::LandmarkId {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __iadd__(cls, boost, ad) -> Any:
        """
        __iadd__( (object)arg1, (LandmarkId)arg2) -> object :

            C++ signature :
                _object* __iadd__(boost::python::back_reference<ad::map::landmark::LandmarkId&>,ad::map::landmark::LandmarkId)"""
    @classmethod
    def __isub__(cls, boost, ad) -> Any:
        """
        __isub__( (object)arg1, (LandmarkId)arg2) -> object :

            C++ signature :
                _object* __isub__(boost::python::back_reference<ad::map::landmark::LandmarkId&>,ad::map::landmark::LandmarkId)"""
    @classmethod
    def __le__(cls, other: object) -> bool:
        """
        __le__( (LandmarkId)arg1, (LandmarkId)arg2) -> object :

            C++ signature :
                _object* __le__(ad::map::landmark::LandmarkId {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __long__(cls, ad) -> Any:
        """
        __long__( (LandmarkId)arg1) -> int :

            C++ signature :
                unsigned long __long__(ad::map::landmark::LandmarkId {lvalue})"""
    @classmethod
    def __lt__(cls, other: object) -> bool:
        """
        __lt__( (LandmarkId)arg1, (LandmarkId)arg2) -> object :

            C++ signature :
                _object* __lt__(ad::map::landmark::LandmarkId {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (LandmarkId)arg1, (LandmarkId)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::landmark::LandmarkId {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __sub__(cls, other):
        """
        __sub__( (LandmarkId)arg1, (LandmarkId)arg2) -> object :

            C++ signature :
                _object* __sub__(ad::map::landmark::LandmarkId {lvalue},ad::map::landmark::LandmarkId)"""
    @property
    def Valid(self): ...

class LandmarkIdList(Boost.Python.instance):
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
        append( (LandmarkIdList)arg1, (LandmarkId)arg2) -> None :

            C++ signature :
                void append(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (LandmarkIdList)arg1, (LandmarkId)arg2) -> int :

            C++ signature :
                unsigned long count(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def extend(cls, *args, **kwargs):
        """
        extend( (LandmarkIdList)arg1, (object)arg2) -> None :

            C++ signature :
                void extend(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},boost::python::api::object)"""
    @classmethod
    def index(cls, *args, **kwargs):
        """
        index( (LandmarkIdList)arg1, (LandmarkId)arg2) -> int :

            C++ signature :
                unsigned long index(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (LandmarkIdList)arg1, (int)arg2, (LandmarkId)arg3) -> None :

            C++ signature :
                void insert(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},long,ad::map::landmark::LandmarkId)"""
    @classmethod
    def reverse(cls, *args, **kwargs):
        """
        reverse( (LandmarkIdList)arg1) -> None :

            C++ signature :
                void reverse(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue})"""
    @classmethod
    def sort(cls, *args, **kwargs):
        """
        sort( (LandmarkIdList)arg1) -> None :

            C++ signature :
                void sort(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue})"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (LandmarkIdList)arg1, (LandmarkId)arg2) -> bool :

            C++ signature :
                bool __contains__(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (LandmarkIdList)arg1, (int)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},long)

        __delitem__( (LandmarkIdList)arg1, (object)arg2) -> None :

            C++ signature :
                void __delitem__(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (LandmarkIdList)arg1, (int)arg2) -> LandmarkId :

            C++ signature :
                ad::map::landmark::LandmarkId {lvalue} __getitem__(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},long)

        __getitem__( (LandmarkIdList)arg1, (object)arg2) -> list :

            C++ signature :
                boost::python::list __getitem__(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},boost::python::indexing::slice)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (LandmarkIdList)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @classmethod
    def __setitem__(cls, index, object) -> None:
        """
        __setitem__( (LandmarkIdList)arg1, (int)arg2, (LandmarkId)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},long,ad::map::landmark::LandmarkId)

        __setitem__( (LandmarkIdList)arg1, (object)arg2, (object)arg3) -> None :

            C++ signature :
                void __setitem__(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},boost::python::indexing::slice,boost::python::api::object)"""

class LandmarkIdSet(Boost.Python.instance):
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
        add( (LandmarkIdSet)arg1, (LandmarkId)arg2) -> None :

            C++ signature :
                void add(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def count(cls, *args, **kwargs):
        """
        count( (LandmarkIdSet)arg1, (LandmarkId)arg2) -> int :

            C++ signature :
                unsigned long count(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def has_key(cls, *args, **kwargs):
        """
        has_key( (LandmarkIdSet)arg1, (LandmarkId)arg2) -> bool :

            C++ signature :
                bool has_key(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def insert(cls, *args, **kwargs):
        """
        insert( (LandmarkIdSet)arg1, (LandmarkId)arg2) -> None :

            C++ signature :
                void insert(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __contains__(cls, other) -> bool:
        """
        __contains__( (LandmarkIdSet)arg1, (LandmarkId)arg2) -> bool :

            C++ signature :
                bool __contains__(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __delitem__(cls, other) -> None:
        """
        __delitem__( (LandmarkIdSet)arg1, (LandmarkId)arg2) -> None :

            C++ signature :
                void __delitem__(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __getitem__(cls, index):
        """
        __getitem__( (LandmarkIdSet)arg1, (LandmarkId)arg2) -> LandmarkId :

            C++ signature :
                ad::map::landmark::LandmarkId __getitem__(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> > {lvalue},ad::map::landmark::LandmarkId)"""
    @classmethod
    def __iter__(cls):
        """
        __iter__( (object)arg1) -> object :

            C++ signature :
                boost::python::objects::iterator_range<boost::python::return_value_policy<boost::python::return_by_value, boost::python::default_call_policies>, std::_Rb_tree_const_iterator<ad::map::landmark::LandmarkId> > __iter__(boost::python::back_reference<std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> >&>)"""
    @classmethod
    def __len__(cls) -> int:
        """
        __len__( (LandmarkIdSet)arg1) -> int :

            C++ signature :
                unsigned long __len__(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> > {lvalue})"""
    @classmethod
    def __reduce__(cls): ...

class LandmarkType(Boost.Python.enum):
    BOLLARD: ClassVar[LandmarkType] = ...
    FIRE_HYDRANT: ClassVar[LandmarkType] = ...
    GUIDE_POST: ClassVar[LandmarkType] = ...
    INVALID: ClassVar[LandmarkType] = ...
    MANHOLE: ClassVar[LandmarkType] = ...
    OTHER: ClassVar[LandmarkType] = ...
    POLE: ClassVar[LandmarkType] = ...
    POSTBOX: ClassVar[LandmarkType] = ...
    POWERCABINET: ClassVar[LandmarkType] = ...
    STREET_LAMP: ClassVar[LandmarkType] = ...
    TRAFFIC_LIGHT: ClassVar[LandmarkType] = ...
    TRAFFIC_SIGN: ClassVar[LandmarkType] = ...
    TREE: ClassVar[LandmarkType] = ...
    UNKNOWN: ClassVar[LandmarkType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class TrafficLightType(Boost.Python.enum):
    BIKE_PEDESTRIAN_RED_GREEN: ClassVar[TrafficLightType] = ...
    BIKE_PEDESTRIAN_RED_YELLOW_GREEN: ClassVar[TrafficLightType] = ...
    BIKE_RED_GREEN: ClassVar[TrafficLightType] = ...
    BIKE_RED_YELLOW_GREEN: ClassVar[TrafficLightType] = ...
    INVALID: ClassVar[TrafficLightType] = ...
    LEFT_RED_YELLOW_GREEN: ClassVar[TrafficLightType] = ...
    LEFT_STRAIGHT_RED_YELLOW_GREEN: ClassVar[TrafficLightType] = ...
    PEDESTRIAN_RED_GREEN: ClassVar[TrafficLightType] = ...
    PEDESTRIAN_RED_YELLOW_GREEN: ClassVar[TrafficLightType] = ...
    RIGHT_RED_YELLOW_GREEN: ClassVar[TrafficLightType] = ...
    RIGHT_STRAIGHT_RED_YELLOW_GREEN: ClassVar[TrafficLightType] = ...
    SOLID_RED_YELLOW: ClassVar[TrafficLightType] = ...
    SOLID_RED_YELLOW_GREEN: ClassVar[TrafficLightType] = ...
    STRAIGHT_RED_YELLOW_GREEN: ClassVar[TrafficLightType] = ...
    UNKNOWN: ClassVar[TrafficLightType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class TrafficSignType(Boost.Python.enum):
    ACCESS_FORBIDDEN: ClassVar[TrafficSignType] = ...
    ACCESS_FORBIDDEN_BICYCLE: ClassVar[TrafficSignType] = ...
    ACCESS_FORBIDDEN_HEIGHT: ClassVar[TrafficSignType] = ...
    ACCESS_FORBIDDEN_MOTORVEHICLES: ClassVar[TrafficSignType] = ...
    ACCESS_FORBIDDEN_TRUCKS: ClassVar[TrafficSignType] = ...
    ACCESS_FORBIDDEN_WEIGHT: ClassVar[TrafficSignType] = ...
    ACCESS_FORBIDDEN_WIDTH: ClassVar[TrafficSignType] = ...
    ACCESS_FORBIDDEN_WRONG_DIR: ClassVar[TrafficSignType] = ...
    BYBICLE_PATH: ClassVar[TrafficSignType] = ...
    CAUTION_ANIMALS: ClassVar[TrafficSignType] = ...
    CAUTION_BICYCLE: ClassVar[TrafficSignType] = ...
    CAUTION_CHILDREN: ClassVar[TrafficSignType] = ...
    CAUTION_PEDESTRIAN: ClassVar[TrafficSignType] = ...
    CAUTION_RAIL_CROSSING: ClassVar[TrafficSignType] = ...
    CAUTION_RAIL_CROSSING_WITH_BARRIER: ClassVar[TrafficSignType] = ...
    CITY_BEGIN: ClassVar[TrafficSignType] = ...
    CITY_END: ClassVar[TrafficSignType] = ...
    CUL_DE_SAC: ClassVar[TrafficSignType] = ...
    CUL_DE_SAC_EXCEPT_PED_BICYCLE: ClassVar[TrafficSignType] = ...
    DANGER: ClassVar[TrafficSignType] = ...
    DESTINATION_BOARD: ClassVar[TrafficSignType] = ...
    DIRECTION_TURN_TO_AUTOBAHN: ClassVar[TrafficSignType] = ...
    DIRECTION_TURN_TO_LOCAL: ClassVar[TrafficSignType] = ...
    ENVIORNMENT_ZONE_BEGIN: ClassVar[TrafficSignType] = ...
    ENVIORNMENT_ZONE_END: ClassVar[TrafficSignType] = ...
    FOOTWALK: ClassVar[TrafficSignType] = ...
    FOOTWALK_BICYCLE_SEP_LEFT: ClassVar[TrafficSignType] = ...
    FOOTWALK_BICYCLE_SEP_RIGHT: ClassVar[TrafficSignType] = ...
    FOOTWALK_BICYCLE_SHARED: ClassVar[TrafficSignType] = ...
    FREE_TEXT: ClassVar[TrafficSignType] = ...
    HAS_WAY_NEXT_INTERSECTION: ClassVar[TrafficSignType] = ...
    INFO_MOTORWAY_INFO: ClassVar[TrafficSignType] = ...
    INFO_NUMBER_OF_AUTOBAHN: ClassVar[TrafficSignType] = ...
    INVALID: ClassVar[TrafficSignType] = ...
    LANES_MERGING: ClassVar[TrafficSignType] = ...
    MAX_SPEED: ClassVar[TrafficSignType] = ...
    MOTORVEHICLE_BEGIN: ClassVar[TrafficSignType] = ...
    MOTORVEHICLE_END: ClassVar[TrafficSignType] = ...
    MOTORWAY_BEGIN: ClassVar[TrafficSignType] = ...
    MOTORWAY_END: ClassVar[TrafficSignType] = ...
    PASS_LEFT: ClassVar[TrafficSignType] = ...
    PASS_RIGHT: ClassVar[TrafficSignType] = ...
    PEDESTRIAN_AREA_BEGIN: ClassVar[TrafficSignType] = ...
    PRIORITY_WAY: ClassVar[TrafficSignType] = ...
    REQUIRED_LEFT_TURN: ClassVar[TrafficSignType] = ...
    REQUIRED_RIGHT_TURN: ClassVar[TrafficSignType] = ...
    REQUIRED_STRAIGHT: ClassVar[TrafficSignType] = ...
    REQUIRED_STRAIGHT_OR_LEFT_TURN: ClassVar[TrafficSignType] = ...
    REQUIRED_STRAIGHT_OR_RIGHT_TURN: ClassVar[TrafficSignType] = ...
    ROUNDABOUT: ClassVar[TrafficSignType] = ...
    SPEED_ZONE_30_BEGIN: ClassVar[TrafficSignType] = ...
    SPEED_ZONE_30_END: ClassVar[TrafficSignType] = ...
    STOP: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_APPLIES_FOR_WEIGHT: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_APPLIES_NEXT_N_KM_TIME: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_ARROW_APPLIES_LEFT: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_ARROW_APPLIES_LEFT_RIGHT: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_ARROW_APPLIES_LEFT_RIGHT_BICYCLE: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_ARROW_APPLIES_RIGHT: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_ARROW_APPLIES_UP_DOWN: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_ARROW_APPLIES_UP_DOWN_BICYCLE: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_BICYCLE_ALLOWED: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_CONSTRUCTION_VEHICLE_ALLOWED: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_ENDS: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_ENVIRONMENT_ZONE_YELLOW_GREEN: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_FORESTAL_ALLOWED: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_MOPED_ALLOWED: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_RAILWAY_ONLY: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_RESIDENTS_ALLOWED: ClassVar[TrafficSignType] = ...
    SUPPLEMENT_TRAM_ALLOWED: ClassVar[TrafficSignType] = ...
    UNKNOWN: ClassVar[TrafficSignType] = ...
    YIELD: ClassVar[TrafficSignType] = ...
    YIELD_TRAIN: ClassVar[TrafficSignType] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class numeric_limits_less__ad_scope_map_scope_landmark_scope_LandmarkId__greater_(Boost.Python.instance):
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
        epsilon() -> LandmarkId :

            C++ signature :
                ad::map::landmark::LandmarkId epsilon()"""
    @staticmethod
    def lowest() -> Any:
        """
        lowest() -> LandmarkId :

            C++ signature :
                ad::map::landmark::LandmarkId lowest()"""
    @staticmethod
    def max() -> Any:
        """
        max() -> LandmarkId :

            C++ signature :
                ad::map::landmark::LandmarkId max()"""
    @classmethod
    def __reduce__(cls): ...

def fromString(*args, **kwargs):
    """
    fromString( (str)str) -> LandmarkType :

        C++ signature :
            ad::map::landmark::LandmarkType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> TrafficLightType :

        C++ signature :
            ad::map::landmark::TrafficLightType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)

    fromString( (str)str) -> TrafficSignType :

        C++ signature :
            ad::map::landmark::TrafficSignType fromString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
def getENUHeading(ad) -> Any:
    """
    getENUHeading( (Landmark)landmark) -> ENUHeading :

        C++ signature :
            ad::map::point::ENUHeading getENUHeading(ad::map::landmark::Landmark)"""
def getENULandmark(ad) -> Any:
    """
    getENULandmark( (LandmarkId)id) -> ENULandmark :

        C++ signature :
            ad::map::landmark::ENULandmark getENULandmark(ad::map::landmark::LandmarkId)"""
def getLandmark(ad) -> Any:
    """
    getLandmark( (LandmarkId)id) -> Landmark :

        C++ signature :
            ad::map::landmark::Landmark getLandmark(ad::map::landmark::LandmarkId)"""
def getLandmarkPtr(ad) -> Any:
    """
    getLandmarkPtr( (LandmarkId)id) -> Landmark :

        C++ signature :
            std::shared_ptr<ad::map::landmark::Landmark const> getLandmarkPtr(ad::map::landmark::LandmarkId)"""
def getLandmarks() -> Any:
    """
    getLandmarks() -> LandmarkIdList :

        C++ signature :
            std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > getLandmarks()"""
def getVisibleLandmarks(ad) -> Any:
    """
    getVisibleLandmarks( (LaneId)laneId) -> LandmarkIdList :

        C++ signature :
            std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > getVisibleLandmarks(ad::map::lane::LaneId)

    getVisibleLandmarks( (LandmarkType)landmarkType, (LaneId)laneId) -> LandmarkIdList :

        C++ signature :
            std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > getVisibleLandmarks(ad::map::landmark::LandmarkType,ad::map::lane::LaneId)"""
def getVisibleTrafficLights(ad) -> Any:
    """
    getVisibleTrafficLights( (LaneId)laneId) -> LandmarkIdList :

        C++ signature :
            std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> > getVisibleTrafficLights(ad::map::lane::LaneId)"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (Landmark)landmark [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::landmark::Landmark [,bool=True])

    isValid( (LandmarkId)landmarkId [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::landmark::LandmarkId [,bool=True])"""
@overload
def isValid(ad) -> Any:
    """
    isValid( (Landmark)landmark [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::landmark::Landmark [,bool=True])

    isValid( (LandmarkId)landmarkId [, (bool)logErrors=True]) -> bool :

        C++ signature :
            bool isValid(ad::map::landmark::LandmarkId [,bool=True])"""
@overload
def toString(ad) -> Any:
    """
    toString( (LandmarkType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::landmark::LandmarkType)

    toString( (TrafficLightType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::landmark::TrafficLightType)

    toString( (TrafficSignType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::landmark::TrafficSignType)"""
@overload
def toString(ad) -> Any:
    """
    toString( (LandmarkType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::landmark::LandmarkType)

    toString( (TrafficLightType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::landmark::TrafficLightType)

    toString( (TrafficSignType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::landmark::TrafficSignType)"""
@overload
def toString(ad) -> Any:
    """
    toString( (LandmarkType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::landmark::LandmarkType)

    toString( (TrafficLightType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::landmark::TrafficLightType)

    toString( (TrafficSignType)e) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > toString(ad::map::landmark::TrafficSignType)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LandmarkId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkId)

    to_string( (LandmarkType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkType)

    to_string( (TrafficLightType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficLightType)

    to_string( (TrafficSignType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficSignType)

    to_string( (Landmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::Landmark)

    to_string( (ENULandmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::ENULandmark)

    to_string( (ENULandmarkList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> >)

    to_string( (LandmarkIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> >)

    to_string( (LandmarkIdSet)landmarkIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LandmarkId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkId)

    to_string( (LandmarkType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkType)

    to_string( (TrafficLightType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficLightType)

    to_string( (TrafficSignType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficSignType)

    to_string( (Landmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::Landmark)

    to_string( (ENULandmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::ENULandmark)

    to_string( (ENULandmarkList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> >)

    to_string( (LandmarkIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> >)

    to_string( (LandmarkIdSet)landmarkIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LandmarkId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkId)

    to_string( (LandmarkType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkType)

    to_string( (TrafficLightType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficLightType)

    to_string( (TrafficSignType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficSignType)

    to_string( (Landmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::Landmark)

    to_string( (ENULandmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::ENULandmark)

    to_string( (ENULandmarkList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> >)

    to_string( (LandmarkIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> >)

    to_string( (LandmarkIdSet)landmarkIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LandmarkId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkId)

    to_string( (LandmarkType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkType)

    to_string( (TrafficLightType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficLightType)

    to_string( (TrafficSignType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficSignType)

    to_string( (Landmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::Landmark)

    to_string( (ENULandmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::ENULandmark)

    to_string( (ENULandmarkList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> >)

    to_string( (LandmarkIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> >)

    to_string( (LandmarkIdSet)landmarkIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LandmarkId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkId)

    to_string( (LandmarkType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkType)

    to_string( (TrafficLightType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficLightType)

    to_string( (TrafficSignType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficSignType)

    to_string( (Landmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::Landmark)

    to_string( (ENULandmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::ENULandmark)

    to_string( (ENULandmarkList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> >)

    to_string( (LandmarkIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> >)

    to_string( (LandmarkIdSet)landmarkIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> >)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (LandmarkId)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkId)

    to_string( (LandmarkType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::LandmarkType)

    to_string( (TrafficLightType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficLightType)

    to_string( (TrafficSignType)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::TrafficSignType)

    to_string( (Landmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::Landmark)

    to_string( (ENULandmark)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::landmark::ENULandmark)

    to_string( (ENULandmarkList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::ENULandmark, std::allocator<ad::map::landmark::ENULandmark> >)

    to_string( (LandmarkIdList)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::vector<ad::map::landmark::LandmarkId, std::allocator<ad::map::landmark::LandmarkId> >)

    to_string( (LandmarkIdSet)landmarkIdSet) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> >)"""
def uniqueLandmarkId(ad) -> Any:
    """
    uniqueLandmarkId( (GeoPoint)geoPoint) -> LandmarkId :

        C++ signature :
            ad::map::landmark::LandmarkId uniqueLandmarkId(ad::map::point::GeoPoint)"""
