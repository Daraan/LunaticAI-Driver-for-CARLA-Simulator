# Functions which not yet have a good grouping in their own files
"""Contains snippets that can can import/export vehicle positions from/to csv files."""

import pandas as pd
from carla.libcarla import Location, Rotation, Transform


def get_actor_display_name(actor, truncate=250):
    """Method to get actor display name"""
    name = ' '.join(actor.type_id.replace('_', '.').title().split('.')[1:])
    return (name[:truncate - 1] + u'\u2026') if len(name) > truncate else name


# A dataframe template to store the locations of vehicles
LOC_DF = pd.DataFrame(columns=["x", "y", "z", "pitch", "yaw", "roll"])


# -----------------------------------
# 

# helper class, similar to @ property but which works on classes directly
class _classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


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


def csv_to_transformations(path):
    df = pd.read_csv(path)
    transformations = []
    for idx, data in df.iterrows():
        loc = Location(data.x, data.y, data.z)
        rot = Rotation(pitch=data.pitch, yaw=data.yaw, roll=data.roll)
        t = Transform(loc, rot)
        transformations.append(t)
    return transformations


# -----------------------------------

def enable_synchronous_mode(world, timedelta=0.05):
    """
    Timedelta in seconds
    NOTE: If synchronous mode is enabled, and there is a Traffic Manager running,
    this must be set to sync mode too. Read this to learn how to do it.
    https://carla.readthedocs.io/en/latest/adv_traffic_manager/#synchronous-mode

    NOTE2: There is a default way in the original config
    cd PythonAPI/util && python3 config.py --no-sync # Disables synchronous mode

    use with a
    while:
        world.tick()

    useful:
    # Wait for the next tick and retrieve the snapshot of the tick.
    world_snapshot = world.wait_for_tick()

    # Register a callback to get called every time we receive a new snapshot.
    world.on_tick(lambda world_snapshot: do_something(world_snapshot))
    """
    settings = world.get_settings()
    settings.synchronous_mode = True  # Enables synchronous mode
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)
