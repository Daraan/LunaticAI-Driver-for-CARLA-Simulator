import access as access
import config as config
import intersection as intersection
import landmark as landmark
import lane as lane
import match as match
import point as point
import restriction as restriction
import route as route
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

from carla.libcarla import _CarlaEnum

NotRelevant: RssMode
Structured: RssMode
Unstructured: RssMode

class RssMode(int, _CarlaEnum):
    NotRelevant = 0
    Structured = 1
    Unstructured = 2

class RssObjectData:
    __instance_size__: ClassVar[int] = 360
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

class RssSceneCreation:
    class AppendRoadBoundariesMode(_CarlaEnum):
        ExpandRouteToAllNeighbors: ClassVar[AppendRoadBoundariesMode] = ...
        ExpandRouteToOppositeLanes: ClassVar[AppendRoadBoundariesMode] = ...
        RouteOnly: ClassVar[AppendRoadBoundariesMode] = ...


    class RestrictSpeedLimitMode(int, _CarlaEnum):
        None = 0  # type: ignore
        ExactSpeedLimit = 1
        IncreasedSpeedLimit10 = 2
        IncreasedSpeedLimit5 = 3

    ExactSpeedLimit = RestrictSpeedLimitMode.ExactSpeedLimit
    ExpandRouteToAllNeighbors = AppendRoadBoundariesMode.ExpandRouteToAllNeighbors
    ExpandRouteToOppositeLanes = AppendRoadBoundariesMode.ExpandRouteToOppositeLanes
    IncreasedSpeedLimit10 = RestrictSpeedLimitMode.IncreasedSpeedLimit10
    IncreasedSpeedLimit5 = RestrictSpeedLimitMode.IncreasedSpeedLimit5
    RouteOnly = AppendRoadBoundariesMode.RouteOnly
    
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
