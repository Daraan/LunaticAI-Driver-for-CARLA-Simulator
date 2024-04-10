# Functions which not yet have a good grouping in their own files
"""Contains snippets that can can import/export vehicle positions from/to csv files."""

from typing import List
import pandas as pd
from carla.libcarla import Location, Rotation, Transform

__all__ = ["transform_to_pandas", "vehicle_location_to_dataframe", "csv_to_transformations", "singledispatchmethod"]

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


# A dataframe template to store the locations of vehicles
LOC_DF = pd.DataFrame(columns=["x", "y", "z", "pitch", "yaw", "roll"])

# -----------------------------------

def transform_to_pandas(transform):
    loc = transform.location
    rot = transform.rotation
    s = pd.Series({"x": loc.x, "y": loc.y, "z": loc.z,
                   "pitch": rot.pitch, "yaw": rot.yaw, "roll": rot.roll})
    return s


def vehicle_location_to_dataframe(vehicles: list):
    df = LOC_DF.copy()
    for i, v in enumerate(vehicles):
        df.loc[i] = transform_to_pandas(v.get_transform())
    return df


def csv_to_transformations(path) -> List[Transform]:
    df = pd.read_csv(path)
    transformations = []
    for idx, data in df.iterrows():
        loc = Location(data.x, data.y, data.z)
        rot = Rotation(pitch=data.pitch, yaw=data.yaw, roll=data.roll)
        t = Transform(loc, rot)
        transformations.append(t)
    return transformations

