# see https://carla.readthedocs.io/en/latest/core_map/#changing-the-map
"""
Command line script to change the map. 
TODO: This file is not so useful, maybe we can remove it.
"""


def change_map(client, town):
    return client.load_world(town)


if __name__ == "__main__":
    import glob
    import os
    import sys

    CARLA_ROOT = os.environ.get("CARLA_ROOT", "./")

    if len(sys.argv) > 1:
        town = sys.argv[-1]
    else:
        town = 'Town04'  # maybe 'Town04_Opt'

    try:
        sys.path.append(glob.glob(os.path.join(CARLA_ROOT, "PythonAPI", "carla", "dist", 'carla-*%d.%d-%s.egg' % (
            sys.version_info.major,
            sys.version_info.minor,
            'win-amd64' if os.name == 'nt' else 'linux-x86_64')))[0])
        print("Using .egg file")
    except IndexError:
        print("Trying to use carla installation")
        pass

    import carla

    print("Changing map to {}".format(town))
    client = carla.Client('localhost', 2000)

    # Once we have a client we can retrieve the world that is currently
    # running.
    world = change_map(client, town)
