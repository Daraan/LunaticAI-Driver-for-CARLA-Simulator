# pylint: disable=unused-import, ungrouped-imports
"""
This submodule provides necessary imports that are not available in all python versions.
"""
import sys
__all__ = ['singledispatchmethod', 'Literal', 'ast_parse']


# singledispatchmethod

if sys.version_info >= (3, 8):
    from functools import singledispatchmethod # Python 3.8+
else:
    from functools import singledispatch, update_wrapper
    from typing import Callable, TypeVar, Any
    from typing_extensions import ParamSpec
    _T = TypeVar('_T')
    _P = ParamSpec('_P')
    _C = TypeVar("_C", bound=Callable[..., Any])
    def singledispatchmethod(func : _C) -> _C:
        """
        Works like :py:class:`functools.singledispatch`, but for methods.
        Backward compatible code of :py:class:`functools.singledispatchmethod`
        for python < 3.8.
        """
        dispatcher = singledispatch(func)
        def wrapper(*args: _P.args, **kw: _P.kwargs) -> _T:
            return dispatcher.dispatch(args[1].__class__)(*args, **kw)
        wrapper.register = dispatcher.register  # type: ignore[attr-defined]
        update_wrapper(wrapper, func)
        return wrapper

# Literal
try:
    # If installed, note that for python 3.10+ this is identical to the built-in typing.Literal
    from typing_extensions import Literal
except ImportError:
    if sys.version_info >= (3, 8):
        # requires: python 3.8+
        # However for < 3.10 there were some bugs, which is why typing_extensions is preferred
        from typing import Literal
    else:
        print("Warning: Literal not found. Literal requires python3.8+ or typing_extensions.")
        class __LiteralMeta(type):
            def __getitem__(cls, _):
                return cls.__repr__()
            
            def __repr__(cls) -> str:
                return "'Warning: Literal requires python3.8+ or typing_extensions. This is a dummy substitution.'"

        class Literal(metaclass=__LiteralMeta):
            pass
       
# ast_parse; to export comments in YAML
import sys
from ast import parse
from functools import partial

if sys.version_info >= (3, 8):
    # new signature we want
    ast_parse = partial(parse, type_comments=True)
else:
    ast_parse = parse


# Monkey patch for Concatenate in Python3.7
if False and sys.version_info < (3, 8):
    from typing_extensions import ParamSpec, TypeVar
    from typing import _GenericAlias
    import typing_extensions
    class _ConcatenateGenericAlias(_GenericAlias, _root=True):
        
        def copy_with(self, params):
            if isinstance(params[-1], (list, tuple)):
                return (*params[:-1], *params[-1])
            if isinstance(params[-1], _ConcatenateGenericAlias):
                params = (*params[:-1], *params[-1].__args__)
            elif params[-1] is not ... and not isinstance(params[-1], ParamSpec):
                raise TypeError("Python 3.7 Monkey Patch: The last parameter to Concatenate should be a "
                                "ParamSpec variable or Ellipsis.")
            return super().copy_with(params)
    
    typing_extensions._ConcatenateGenericAlias = _ConcatenateGenericAlias
    
        
