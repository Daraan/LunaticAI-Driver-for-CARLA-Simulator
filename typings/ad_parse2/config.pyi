import Boost.Python
from _typeshed import Incomplete
from typing import Any, ClassVar, overload

class MapConfigFileHandler(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)"""
    @classmethod
    def isInitializedWithFilename(cls, *args, **kwargs):
        """
        isInitializedWithFilename( (MapConfigFileHandler)arg1, (str)configFileName) -> bool :

            C++ signature :
                bool isInitializedWithFilename(ad::map::config::MapConfigFileHandler {lvalue},std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
    @classmethod
    def readConfig(cls, *args, **kwargs):
        """
        readConfig( (MapConfigFileHandler)arg1, (str)configFileName) -> bool :

            C++ signature :
                bool readConfig(ad::map::config::MapConfigFileHandler {lvalue},std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >)"""
    @classmethod
    def reset(cls, ad) -> Any:
        """
        reset( (MapConfigFileHandler)arg1) -> None :

            C++ signature :
                void reset(ad::map::config::MapConfigFileHandler {lvalue})"""
    @classmethod
    def __reduce__(cls): ...
    @property
    def Initialized(self): ...
    @property
    def adMapEntry(self): ...
    @property
    def configFileName(self): ...
    @property
    def defaultEnuReference(self): ...
    @property
    def defaultEnuReferenceAvailable(self): ...
    @property
    def pointsOfInterest(self): ...

class MapEntry(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    filename: Incomplete
    openDriveDefaultIntersectionType: Incomplete
    openDriveDefaultTrafficLightType: Incomplete
    openDriveOverlapMargin: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (MapEntry)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::config::MapEntry)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (MapEntry)arg1, (MapEntry)other) -> MapEntry :

            C++ signature :
                ad::map::config::MapEntry {lvalue} assign(ad::map::config::MapEntry {lvalue},ad::map::config::MapEntry)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (MapEntry)arg1, (MapEntry)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::config::MapEntry {lvalue},ad::map::config::MapEntry)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (MapEntry)arg1, (MapEntry)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::config::MapEntry {lvalue},ad::map::config::MapEntry)"""
    @classmethod
    def __reduce__(cls): ...

class PointOfInterest(Boost.Python.instance):
    __instance_size__: ClassVar[int] = ...
    geoPoint: Incomplete
    name: Incomplete
    @classmethod
    def __init__(cls, *args, **kwargs) -> None:
        """
        __init__( (object)arg1) -> None :

            C++ signature :
                void __init__(_object*)

        __init__( (object)arg1, (PointOfInterest)other) -> None :

            C++ signature :
                void __init__(_object*,ad::map::config::PointOfInterest)"""
    @classmethod
    def assign(cls, *args, **kwargs):
        """
        assign( (PointOfInterest)arg1, (PointOfInterest)other) -> PointOfInterest :

            C++ signature :
                ad::map::config::PointOfInterest {lvalue} assign(ad::map::config::PointOfInterest {lvalue},ad::map::config::PointOfInterest)"""
    @classmethod
    def __eq__(cls, other: object) -> bool:
        """
        __eq__( (PointOfInterest)arg1, (PointOfInterest)arg2) -> object :

            C++ signature :
                _object* __eq__(ad::map::config::PointOfInterest {lvalue},ad::map::config::PointOfInterest)"""
    @classmethod
    def __ne__(cls, other: object) -> bool:
        """
        __ne__( (PointOfInterest)arg1, (PointOfInterest)arg2) -> object :

            C++ signature :
                _object* __ne__(ad::map::config::PointOfInterest {lvalue},ad::map::config::PointOfInterest)"""
    @classmethod
    def __reduce__(cls): ...

@overload
def to_string(ad) -> Any:
    """
    to_string( (MapEntry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::config::MapEntry)

    to_string( (PointOfInterest)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::config::PointOfInterest)"""
@overload
def to_string(ad) -> Any:
    """
    to_string( (MapEntry)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::config::MapEntry)

    to_string( (PointOfInterest)value) -> str :

        C++ signature :
            std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > to_string(ad::map::config::PointOfInterest)"""
