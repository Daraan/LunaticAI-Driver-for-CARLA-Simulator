# pylint: disable=unused-import, ungrouped-imports
"""
This submodule provides necessary imports that are not available in all python versions.
"""

__all__ = ['singledispatchmethod', 'Literal', 'ast_parse']

# singledispatchmethod

try:
    from functools import singledispatchmethod # Python 3.8+
except ImportError:
    from functools import singledispatch, update_wrapper

    def singledispatchmethod(func):
        """
        Works like functools.singledispatch, but for methods. Backward compatible code
        """
        dispatcher = singledispatch(func)
        def wrapper(*args, **kw):
            return dispatcher.dispatch(args[1].__class__)(*args, **kw)
        wrapper.register = dispatcher.register
        update_wrapper(wrapper, func)
        return wrapper

# Literal
 
try:
    # If installed, note that for python 3.10+ this is identical to the built-in typing.Literal
    from typing_extensions import Literal
except ImportError:
    try:
        # requires: python 3.8+
        # However for < 3.10 there were some bugs, which is why typing_extensions is prefered
        from typing import Literal
    except ImportError:
        print("Warning: Literal not found. Literal requires python3.8+ or typing_extensions.")
        class __LiteralMeta(type): # noqa
            def __getitem__(cls, _):
                return cls.__repr__()
            
            def __repr__(cls) -> str:
                return "'Warning: Literal requires python3.8+ or typing_extensions. This is a dummy substitution.'"

        class Literal(metaclass=__LiteralMeta):
            pass
       
# ast_parse       
            
from ast import parse
from functools import partial
import sys

if sys.version_info >= (3, 8):
    ast_parse = partial(parse, type_comments=True) # new signature we want
else:
    ast_parse = parse
