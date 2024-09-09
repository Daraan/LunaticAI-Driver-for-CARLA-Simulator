import Boost.Python
from typing import ClassVar

class RssCheck(Boost.Python.instance):
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def calculateProperResponse(cls, *args, **kwargs):
        """
        calculateProperResponse( (RssCheck)arg1, (WorldModel)worldModel, (ProperResponse)properResponse) -> bool :

            C++ signature :
                bool calculateProperResponse(ad::rss::core::RssCheck {lvalue},ad::rss::world::WorldModel,ad::rss::state::ProperResponse {lvalue})

        calculateProperResponse( (RssCheck)arg1, (WorldModel)worldModel, (SituationSnapshot)situationSnapshot, (RssStateSnapshot)rssStateSnapshot, (ProperResponse)properResponse) -> bool :

            C++ signature :
                bool calculateProperResponse(ad::rss::core::RssCheck {lvalue},ad::rss::world::WorldModel,ad::rss::situation::SituationSnapshot {lvalue},ad::rss::state::RssStateSnapshot {lvalue},ad::rss::state::ProperResponse {lvalue})"""
    @classmethod
    def __reduce__(cls): ...

class RssResponseResolving(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def provideProperResponse(cls, *args, **kwargs):
        """
        provideProperResponse( (RssResponseResolving)arg1, (RssStateSnapshot)currentStateSnapshot, (ProperResponse)response) -> bool :

            C++ signature :
                bool provideProperResponse(ad::rss::core::RssResponseResolving {lvalue},ad::rss::state::RssStateSnapshot,ad::rss::state::ProperResponse {lvalue})"""
    @classmethod
    def __reduce__(cls): ...

class RssSituationChecking(Boost.Python.instance):
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def checkSituations(cls, *args, **kwargs):
        """
        checkSituations( (RssSituationChecking)arg1, (SituationSnapshot)situationSnapshot, (RssStateSnapshot)rssStateSnapshot) -> bool :

            C++ signature :
                bool checkSituations(ad::rss::core::RssSituationChecking {lvalue},ad::rss::situation::SituationSnapshot,ad::rss::state::RssStateSnapshot {lvalue})"""
    @classmethod
    def __reduce__(cls): ...

class RssSituationExtraction(Boost.Python.instance):
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def extractSituations(cls, *args, **kwargs):
        """
        extractSituations( (RssSituationExtraction)arg1, (WorldModel)worldModel, (SituationSnapshot)situationSnapshot) -> bool :

            C++ signature :
                bool extractSituations(ad::rss::core::RssSituationExtraction {lvalue},ad::rss::world::WorldModel,ad::rss::situation::SituationSnapshot {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
