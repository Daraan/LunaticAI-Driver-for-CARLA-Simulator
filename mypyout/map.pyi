import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

NotRelevant: RssMode
Structured: RssMode
Unstructured: RssMode

class RssMode(Boost.Python.enum):
    NotRelevant: ClassVar[RssMode] = ...
    Structured: ClassVar[RssMode] = ...
    Unstructured: ClassVar[RssMode] = ...
    names: ClassVar[dict] = ...
    values: ClassVar[dict] = ...

class RssObjectData(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    id: Incomplete
    matchObject: Incomplete
    rssDynamics: Incomplete
    speed: Incomplete
    steeringAngle: Incomplete
    type: Incomplete
    yawRate: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def __reduce__(cls): ...

class RssSceneCreation(Boost.Python.instance):
    class AppendRoadBoundariesMode(Boost.Python.enum):
        ExpandRouteToAllNeighbors: ClassVar[AppendRoadBoundariesMode] = ...
        ExpandRouteToOppositeLanes: ClassVar[AppendRoadBoundariesMode] = ...
        RouteOnly: ClassVar[AppendRoadBoundariesMode] = ...
        names: ClassVar[dict] = ...
        values: ClassVar[dict] = ...

    class RestrictSpeedLimitMode(Boost.Python.enum):
        ExactSpeedLimit: ClassVar[RestrictSpeedLimitMode] = ...
        IncreasedSpeedLimit10: ClassVar[RestrictSpeedLimitMode] = ...
        IncreasedSpeedLimit5: ClassVar[RestrictSpeedLimitMode] = ...
        names: ClassVar[dict] = ...
        values: ClassVar[dict] = ...
    ExactSpeedLimit: ClassVar[RestrictSpeedLimitMode] = ...
    ExpandRouteToAllNeighbors: ClassVar[AppendRoadBoundariesMode] = ...
    ExpandRouteToOppositeLanes: ClassVar[AppendRoadBoundariesMode] = ...
    IncreasedSpeedLimit10: ClassVar[RestrictSpeedLimitMode] = ...
    IncreasedSpeedLimit5: ClassVar[RestrictSpeedLimitMode] = ...
    RouteOnly: ClassVar[AppendRoadBoundariesMode] = ...
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1, (object)timeIndex, (RssDynamics)defaultEgoRssDynamics) -> None :

            C++ signature :
                void __init__(_object*,unsigned long,ad::rss::world::RssDynamics)"""
    @classmethod
    def appendRoadBoundaries(cls, *args, **kwargs):
        """
        appendRoadBoundaries( (RssSceneCreation)arg1, (RssObjectData)egoObjectData, (FullRoute)route, (AppendRoadBoundariesMode)operationMode) -> bool :

            C++ signature :
                bool appendRoadBoundaries(ad::rss::map::RssSceneCreation {lvalue},ad::rss::map::RssObjectData,ad::map::route::FullRoute,ad::rss::map::RssSceneCreation::AppendRoadBoundariesMode)"""
    @classmethod
    def appendScenes(cls, *args, **kwargs):
        """
        appendScenes( (RssSceneCreation)arg1, (RssObjectData)egoObjectData, (FullRoute)egoRoute, (RssObjectData)otherObjectData, (RestrictSpeedLimitMode)restrictSpeedLimitMode, (LandmarkIdSet)greenTrafficLights, (RssMode)mode) -> bool :

            C++ signature :
                bool appendScenes(ad::rss::map::RssSceneCreation {lvalue},ad::rss::map::RssObjectData,ad::map::route::FullRoute,ad::rss::map::RssObjectData,ad::rss::map::RssSceneCreation::RestrictSpeedLimitMode,std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> >,ad::rss::map::RssMode)"""
    @classmethod
    def getWorldModel(cls, ad) -> Any:
        """
        getWorldModel( (RssSceneCreation)arg1) -> WorldModel :

            C++ signature :
                ad::rss::world::WorldModel getWorldModel(ad::rss::map::RssSceneCreation {lvalue})"""
    @classmethod
    def __reduce__(cls): ...

def getLogger() -> Any:
    """
    getLogger() -> object :

        C++ signature :
            std::shared_ptr<spdlog::logger> getLogger()"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (RestrictSpeedLimitMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::map::RssSceneCreation::RestrictSpeedLimitMode)

    to_string( (RssMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::map::RssMode)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (RestrictSpeedLimitMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::map::RssSceneCreation::RestrictSpeedLimitMode)

    to_string( (RssMode)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::rss::map::RssMode)"""
