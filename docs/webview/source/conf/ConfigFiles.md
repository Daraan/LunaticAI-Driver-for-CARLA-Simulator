# Configuration

>intro hydra

## Launch Config

See also [](#LaunchConfig)

## Agent Config vs. Context Config

The context config is a temporary clone of the agent's con

| Agent Config | Context Config |
| ------------ | -------------- |
| `àgent.config` | `ctx.config` |
| permanent    | temporary      |
| updatable by actions *manually* | automatically updated by [](#Rule.overwrite_settings) |
| creates the context config | used to calculate the VehicleControls |