"""
This package contains helper classes and constants used in this project.

The classes from :py:mod:`carla_originals` are mostly identical to the
ones provided in the examples from the CARLA PythonAPI.

.. include:: /docs/Classes.rst

----------------

"""
# ruff: noqa: ARG002,ARG003,ANN401

__all__ = [
    "CustomSensorInterface",
    "carla_originals",
]

from classes.constants import READTHEDOCS
from . import carla_originals
from ._sensor_interface import CustomSensorInterface

# Dummy object to easier disable pygame
from typing import Any, Final, Protocol, overload, TYPE_CHECKING

from typing_extensions import Self, Literal, TypeVar, TypeIs, TypeGuard, final, Never

_T = TypeVar("_T")
_BoolT = TypeVar("_BoolT", bound=bool, default=bool)

_TrueDummyT = TypeVar("_TrueDummyT", bound="CanBeDummy[Literal[True]]")
_DummyT = TypeVar("_DummyT", bound="CanBeDummy[bool]")


# HACK If this is a protocol will raise Metaclass conflict later
class CanBeDummy(Protocol[_BoolT] if TYPE_CHECKING else object):
    """
    Abstract base class to clarify that a class can be a dummy object.
    
    Use :python:`CanBeDummy[True]` to indicate that the class is a dummy object.
    Default is :python:`CanBeDummy[False]` to indicate a non-dummy class.
    
    :meta private:
    """
    
    is_dummy_: _BoolT = False
    if READTHEDOCS and not TYPE_CHECKING:
        is_dummy_: bool = False
    
    @overload
    @classmethod
    def is_dummy(cls, obj: "_TrueDummyT") -> TypeIs[_TrueDummyT]: ...
    
    @overload
    @classmethod
    def is_dummy(cls, obj: "CanBeDummy[Literal[False]]") -> TypeGuard[Never]: ...
    
    @overload
    @classmethod
    def is_dummy(cls, obj: "CanBeDummy[bool]") -> TypeGuard["MockDummy"]: ...
    # Assuming only one MockDummy class, else need to put CanBeDummy[Literal[True]] here.
    
    @classmethod
    def is_dummy(cls, obj: "_TrueDummyT | CanBeDummy[Literal[False]] | CanBeDummy[bool]") -> "TypeGuard[MockDummy] | TypeGuard[Never] | TypeIs[_TrueDummyT]":
        """
        :py:obj:`~typing.TypeGuard` check if a variable is a duck-typed dummy object.
        
        Objects might be dummy objects that have no function if :py:attr:`.LaunchConfig.pygame`
        is set to :code:`False`.
        """
        return obj.is_dummy_
    
    if READTHEDOCS and not TYPE_CHECKING:
        # Easier signature for documentation
        @classmethod
        def is_dummy(cls, obj: Any) -> TypeGuard["MockDummy"]:
            """
            :py:obj:`~typing.TypeGuard` check if a variable is a duck-typed dummy object.
            
            Objects might be dummy objects that have no function if :py:attr:`.LaunchConfig.pygame`
            is set to :code:`False`.
            """


class __NoOpMeta(type):
    
    def __getattr__(cls: "type[_TrueDummyT]", key: Any) -> _TrueDummyT:
        return cls()
    
    def __setattr__(cls, key: str, value: Any) -> None:
        pass


@final
class MockDummy(CanBeDummy[Literal[True]] if TYPE_CHECKING else CanBeDummy, metaclass=__NoOpMeta):
    """
    This is a dummy class that does nothing.

    Can be used to create duck types dummy objects.
    """
    
    CanBeDummy: Final = CanBeDummy
    
    is_dummy_ = True
    
    def __init__(self, *args, **kwargs) -> None:
        pass

    def __call__(self, *args, **kwargs) -> Self:
        return self

    def __getitem__(self, *args, **kwargs) -> Self:
        return self

    def __setitem__(self, key: str, value: Any) -> None:
        pass
    
    def __getattr__(self, *args, **kwargs) -> Self:
        return self
    
    def __setattr__(self, key: str, value: Any) -> None:
        pass

    @classmethod
    def exact_dummy(cls, typ: _T) -> _T:
        """
        Creates a duck-typed dummy object of the input.
        """
        return cls()  # type: ignore[return-type]

    @overload
    @classmethod
    def create_dummy(cls, typ: None = None) -> Any: ...
    # allows var: DuckType = MockDummy.create_dummy() to work
    
    @overload
    @classmethod
    def create_dummy(cls, typ: "type[_DummyT]") -> _DummyT: ...

    @classmethod
    def create_dummy(cls, typ: "type[_DummyT] | None" = None) -> "_DummyT | Any":
        """
        Creates a duck-typed instance dummy from the input type.
        
        :python:`var: DuckType = MockDummy.create_dummy()` does also work.
        """
        return cls()  # type: ignore[return-type]


