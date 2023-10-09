import pandas as pd
import carla
from carla import Transform, Location, Rotation

LOC_DF = pd.DataFrame(columns=["x", "y", "z", "pitch", "yaw", "roll"])

def prepare_blueprints(world):
    blueprint_library = world.get_blueprint_library()
    car_blueprint = blueprint_library.filter('vehicle')[0]

    if car_blueprint.has_attribute('color'):
        color = car_blueprint.get_attribute('color').recommended_values[-1]
        car_blueprint.set_attribute('color', color)

    ego_bp = world.get_blueprint_library().find('vehicle.lincoln.mkz_2020')
    if ego_bp.has_attribute('color'):
        color = ego_bp.get_attribute('color').recommended_values[0]
        ego_bp.set_attribute('color', "255,0,0")

    ego_bp.set_attribute('role_name', 'hero')
    return ego_bp, car_blueprint

def transform_to_pandas(transform):
   loc = transform.location
   rot = transform.rotation
   s = pd.Series({"x":loc.x, "y":loc.y, "z":loc.z,
                  "pitch" : rot.pitch,"yaw":rot.yaw, "roll":rot.roll})
   return s
                  
def vehicles_into_df(vehicles : list):
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
    settings.synchronous_mode = True # Enables synchronous mode
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

        

    
