"""Helper classes"""

from omegaconf import OmegaConf, DictConfig

# -----------------
# Categories of settings
# -----------------

# -----------------
# IMPORTANT: When creating a new dict at to the XXX marked locations
# -----------------

# Create other categories if you see it fit
# Add them to the BaseCategories class below

# Contains settings that change over time through other means
live_info : DictConfig = OmegaConf.create()

speed : DictConfig=  OmegaConf.create()
distance : DictConfig = OmegaConf.create()
lane_change : DictConfig = OmegaConf.create()
obstacles : DictConfig = OmegaConf.create()
controls : DictConfig = OmegaConf.create()

planner : DictConfig = OmegaConf.create()

# Try to group these into meaningful categories
other : DictConfig = OmegaConf.create()

# Use this if the reason is not yet clear
unknown : DictConfig = OmegaConf.create()


# -----------------

# Do not set this now, else it will create copies of empty dicts
default_options = None

# -----------------

class BaseCategories:
    """A class that holds all default values, to be overwritten by the user."""

    @property
    def default_options(self) -> DictConfig:
        """Returns the global default options."""
        return default_options 

    @staticmethod 
    def init_default_options():
        # XXX
        global default_options
        if default_options is None:
            default_options = OmegaConf.create()
            default_options.speed = speed
            default_options.distance = distance
            default_options.lane_change = lane_change
            default_options.obstacles = obstacles
            default_options.controls = controls
            default_options.planner = planner
            default_options.other = other
            default_options.unknown = unknown
            default_options.live_info = live_info

            # Flat interface to be compatible with original settings.

        return default_options

    @staticmethod 
    def _flatten_dict(source, target):
        for k, v in source.items():
            if isinstance(v, dict):
                BaseCategories._flatten_dict(v, target)
            else:
                target[k] = v

    def get_flat_options(self) -> dict:
        """
        Note these return a copy of the data but in a flat hierarchy.
        Also note interpolations do not exist anymore.
        E.g. target_speed and max_speed are two different references.
        """
        options ={}
        resolved = OmegaConf.to_container(self._options, resolve=True)
        self._flatten_dict(resolved, options)
        return options
    
    #def __setattr__(self, key, value):
    #    raise ValueError("Set attributes via. self.options.<category>.<key> = <value>")

    def __init__(self):
        # Insert every dict from above XXX
        
        # XXX
        self._options = self.init_default_options().copy()
        self.live_info = self._options.live_info

        self.speed = self._options.speed
        self.distance = self._options.distance
        self.lane_change = self._options.lane_change
        self.obstacles = self._options.obstacles # vehicles, traffic signs, walkers

        self.controls = self._options.controls

        self.planner = self._options.planner

        # try to group these
        self.other = self._options.other
        self.unknown = self._options.unknown

    @property
    def options(self): # we do not want to overwrite this
        return self._options
    
    def get_options(self, category=None, *, yaml=False) -> DictConfig:
        """Returns a dictionary of all options."""
        if category is None:
            options = self._options
        else:
            options = self._options[category]
        if yaml:
            return OmegaConf.to_yaml(options)
        return options
    
    def export_options(self, path, category=None, resolve=False) -> None:
        """Exports the options to a yaml file."""
        if category is None:
            options = self._options
        else:
            options = self._options[category]
        OmegaConf.save(options, path, resolve=resolve)


    

# TODO: Using a a json/yaml file in the future


# NOTE: maybe we can get rid of this. dataclasses work nicely with OmegaConf was the original idea.
from dataclasses import dataclass, field

@dataclass
class _AnnotationChecker:
    """Helper class to check if all attributes have a type annotation when using dataclasses ."""
    def __init_subclass__(cls) -> None:
        cls().__post_init__() # call check of post init

    def __post_init__(self) -> None:
        """
        Assures that every attribute has a type annotation to be valid for dataclass.
        private (__) attributes are ignored.
        """
        cls = self.__class__
        annotations = cls.__annotations__

        for key, value in vars(cls).items():
            #print(key)
            if key.startswith('__') or key.startswith("_"+cls.__name__) or key in annotations:
                continue
            if isinstance(value, (property, classmethod, staticmethod)) or callable(value):
                continue
            raise TypeError(f"Class {cls.__name__} has no type annotation for '{key}'. Please annotate with the type.")

# unused
class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        print("get", obj, owner)
        return self.f(owner)
    
    def __set__(self, obj, value):
        print("set", obj, value)
        self.f(obj, value)

    def __delete__(self, obj):
        print("del", obj)
        pass


        