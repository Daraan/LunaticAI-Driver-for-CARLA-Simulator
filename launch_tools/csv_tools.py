# Functions which not yet have a good grouping in their own files
"""Contains snippets that can can import/export vehicle positions from/to csv files."""

from typing import List
import pandas as pd
from carla.libcarla import Location, Rotation, Transform # pylint: disable=no-name-in-module

__all__ = ["transform_to_pandas", "vehicle_location_to_dataframe", "csv_to_transformations"]


# A dataframe template to store the locations of vehicles
LOC_DF = pd.DataFrame(columns=["x", "y", "z", "pitch", "yaw", "roll"])

# -----------------------------------

def transform_to_pandas(transform : Transform) -> pd.Series:
    """
    Format a carla.Transform object to a pandas.Series.
    """
    loc = transform.location
    rot = transform.rotation
    s = pd.Series({"x": loc.x, "y": loc.y, "z": loc.z,
                   "pitch": rot.pitch, "yaw": rot.yaw, "roll": rot.roll})
    return s


def vehicle_location_to_dataframe(vehicles: list):
    """
    Exports the locations of vehicles to a pandas dataframe.
    """
    df = LOC_DF.copy()
    for i, v in enumerate(vehicles):
        df.loc[i] = transform_to_pandas(v.get_transform())
    return df


def csv_to_transformations(path) -> List[Transform]:
    """
    Read a csv file and return a list of Transform objects.
    Expected columns: x, y, z, pitch, yaw, roll
    """
    df = pd.read_csv(path)
    transformations = []
    for _, data in df.iterrows():
        loc = Location(data.x, data.y, data.z)
        rot = Rotation(pitch=data.pitch, yaw=data.yaw, roll=data.roll)
        t = Transform(loc, rot)
        transformations.append(t)
    return transformations

