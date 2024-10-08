# Launch Config Default

```yaml
# LaunchConfig

# If enabled will assert that the loaded config is a subset of the `LaunchConfig` class.
#  
# If set to >= 2, will assert that during runtime the types are correct.
strict_config: 3
# unused kept for compatibility with carla examples.
verbose: true
# If true will print out some more information and draws waypoints
debug: true

# If True will create an interactive session with command line input
# - NOTE: Needs custom code in the main file (Not implemented)
interactive: false
seed:
map: Town04_Opt
host: 127.0.0.1
port: 2000

# Used to fix `carla.WorldSettings.fixed_delta_seconds`
#  
# Experimental also used to cap fps in the simulation.
fps: 20

# If True, the simulation will be set to run in synchronous mode.
# For False, the simulation will be set to run in asynchronous mode.
# If None the world settings for synchronous mode will not be adjusted, 
# assuming this is handled by the user / external system.
sync: true

# Decide if the GameFramework & WoldModel are allowed to call carla.World.tick()
# or if `False` the ticks should be handled by an outside system.
handle_ticks: true

# If True the agent will look for a new waypoint after the initial route is done.
# - NOTE: Needs custom implementation in the main file.
loop: true
# width of pygame window
width: 1280
# height of pygame window
height: 720

# Gamma correction of the camera.
# Depending on the weather and map this might need to be adjusted.
gamma: 2.2

# If False will spawn a vehicle for the agent to control, using the `filter` and `generation` settings.
# Otherwise will not spawn a vehicle but will wait until an actor with the name defined in `rolename` (default: "hero") is found.
#  
# This vehicle needs to be spawned by another process, e.g. through the scenario runner.
externalActor: true
# Actor name to wait for if `externalActor` is True.
rolename: hero
# Filter for the ego blueprint. Kept for compatibility with carla examples.
filter: vehicle.*
# Generation for the ego blueprint. Kept for compatibility with carla examples.
generation: 2

# Whether or not to use the Carla's TrafficManager to autopilot the agent
# Note: 
#     This disables the usage of the LunaticAgent, however needs to be 
#     enabled in the main script by the user to work.
autopilot: false
# The Settings of the agent
agent: ???
# The camera settings
camera:
  width: 1280
  height: 720
  gamma: 2.2
  camera_blueprints:
  - NotImplemented
  hud: ???
  recorder:
    enabled: ???
    output_path: ${hydra:runtime.output_dir}/recorder/session%03d/%08d.bmp
    frame_interval: 4
  detection_matrix:
    draw: true
    values: true
    vertical: true
    imshow_settings:
      cmap: jet
    text_settings:
      color: orange
```
