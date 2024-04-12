__all__ = ['singledispatchmethod', 'Literal']

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
    
try:
    # If installed, note that for python 3.10+ this is identical to the built-in typing.Literal
    from typing_extensions import Literal # noqa # pylint: disable=unused-import
except ImportError:
    try:
        # requires: python 3.8+
        # However <3.10 there were some bugs
        from typing import Literal # noqa # pylint: disable=unused-import
    except ImportError:
        print("Warning: Literal not found. Literal requires python3.8+ or typing_extensions.")
        class __LiteralMeta(type):
            def __getitem__(cls, key):
                return cls.__repr__()
            
            def __repr__(self) -> str:
                return """'Warning: Literal requires python3.8+ or typing_extensions. This is a dummy substitution.'"""

        class Literal(metaclass=__LiteralMeta):
            pass
            
        