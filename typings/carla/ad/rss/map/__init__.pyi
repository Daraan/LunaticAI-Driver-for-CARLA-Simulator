from . import access, config, intersection, landmark, lane, match, point, restriction, route
from .. import world

from carla import ad

class RssMode(int,):
    NotRelevant = 0

    Structured = 1

    Unstructured = 2


class RssObjectData():
    @property
    def id(self) -> int: ...

    @property
    def matchObject(self) -> match.Object: ...

    @property
    def rssDynamics(self) -> world.RssDynamics: ...

    @property
    def speed(self) -> ad.physics.Speed: ...

    @property
    def steeringAngle(self) -> ad.physics.Angle: ...

    @property
    def type(self) -> world.ObjectType: ...

    @property
    def yawRate(self) -> ad.physics.AngularVelocity: ...

    ...

class RssSceneCreation():
    class AppendRoadBoundariesMode(int):
        RouteOnly = 0
        ExpandRouteToOppositeLanes = 1
        ExpandRouteToAllNeighbors = 2
    class RestrictSpeedLimitMode(int):
        None = 0  # attribute is named "None" in the C++ code
        ExactSpeedLimit = 1
        IncreasedSpeedLimit5 = 2
        IncreasedSpeedLimit10 = 3

    RouteOnly = 0
    ExpandRouteToOppositeLanes = 1
    ExpandRouteToAllNeighbors = 2

    None = 0  # attribute is named "None" in the C++ code
    ExactSpeedLimit = 1
    IncreasedSpeedLimit5 = 2
    IncreasedSpeedLimit10 = 3


    def appendRoadBoundaries(self, arg1: RssSceneCreation, egoObjectData: RssObjectData, route: route.FullRoute, operationMode: AppendRoadBoundariesMode) -> bool:
        '''

        appendRoadBoundaries( (RssSceneCreation)arg1, (RssObjectData)egoObjectData, (FullRoute)route, (AppendRoadBoundariesMode)operationMode) -> bool :

            C++ signature :
                bool appendRoadBoundaries(ad::rss::map::RssSceneCreation {lvalue},ad::rss::map::RssObjectData,ad::map::route::FullRoute,ad::rss::map::RssSceneCreation::AppendRoadBoundariesMode)
        '''
        ...

    def appendScenes(self, arg1: RssSceneCreation, egoObjectData: RssObjectData, egoRoute: route.FullRoute, otherObjectData: RssObjectData, restrictSpeedLimitMode: RestrictSpeedLimitMode, greenTrafficLights: landmark.LandmarkIdSet, mode: RssMode) -> bool:
        '''

        appendScenes( (RssSceneCreation)arg1, (RssObjectData)egoObjectData, (FullRoute)egoRoute, (RssObjectData)otherObjectData, (RestrictSpeedLimitMode)restrictSpeedLimitMode, (LandmarkIdSet)greenTrafficLights, (RssMode)mode) -> bool :

            C++ signature :
                bool appendScenes(ad::rss::map::RssSceneCreation {lvalue},ad::rss::map::RssObjectData,ad::map::route::FullRoute,ad::rss::map::RssObjectData,ad::rss::map::RssSceneCreation::RestrictSpeedLimitMode,std::set<ad::map::landmark::LandmarkId, std::less<ad::map::landmark::LandmarkId>, std::allocator<ad::map::landmark::LandmarkId> >,ad::rss::map::RssMode)
        '''
        ...

    def getWorldModel(self, arg1: RssSceneCreation) -> world.WorldModel:
        '''

        getWorldModel( (RssSceneCreation)arg1) -> WorldModel :

            C++ signature :
                ad::rss::world::WorldModel getWorldModel(ad::rss::map::RssSceneCreation {lvalue})
        '''
        ...

