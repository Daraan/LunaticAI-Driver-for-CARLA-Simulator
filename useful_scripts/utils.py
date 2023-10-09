import pandas as pd
import carla
from carla import Transform, Location, Rotation

LOC_DF = pd.DataFrame(columns=["x", "y", "z", "pitch", "yaw", "roll"])

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
        
        
    
