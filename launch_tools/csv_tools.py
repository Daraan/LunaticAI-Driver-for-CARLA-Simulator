"""Contains snippets that can can import/export vehicle positions from/to csv files."""
from __future__ import annotations

# pyright: reportUnknownMemberType=none
# pyright: reportUnknownVariableType=information
from os import PathLike

import carla
import pandas as pd

__all__ = ["transform_to_pandas",
           "vehicle_location_to_dataframe",
           "csv_to_transformations"]


# A dataframe template to store the locations of vehicles
LOC_DF = pd.DataFrame(columns=["x", "y", "z", "pitch", "yaw", "roll"])

# -----------------------------------
# pyright: strict
def transform_to_pandas(transform: carla.Transform) -> pd.Series[float]:
    """
    Format a :py:class:`carla.Transform` object to a :py:class:`pandas.Series`.
    """
    loc = transform.location
    rot = transform.rotation
    return pd.Series({"x": loc.x, "y": loc.y, "z": loc.z,
                   "pitch": rot.pitch, "yaw": rot.yaw, "roll": rot.roll})


def vehicle_location_to_dataframe(vehicles: list[carla.Actor]) -> pd.DataFrame:
    """
    Exports the locations of vehicles to a :py:class:`pandas.Dataframe`.
    """
    df = LOC_DF.copy()
    for i, v in enumerate(vehicles):
        df.loc[i] = transform_to_pandas(v.get_transform())
    return df


def csv_to_transformations(path: str | PathLike[str]) -> list[carla.Transform]:
    """
    Read a csv file and return a list of Transform objects.
    Expected columns: :code:`x, y, z, pitch, yaw, roll`.
    """
    df = pd.read_csv(path)  # pyright: ignore
    transformations: list[carla.Transform] = []
    for _, data in df.iterrows():  # pyright: ignore
        loc = carla.Location(data.x, data.y, data.z)  # type: ignore[attr-defined]
        rot = carla.Rotation(pitch=data.pitch, yaw=data.yaw, roll=data.roll)  # type: ignore[attr-defined]
        t = carla.Transform(loc, rot)
        transformations.append(t)
    return transformations

