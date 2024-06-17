# Installation

## Requirements

```bash
pip install -r docs/requirements/requirements.txt
```

If you want to use the `LunaticChallenger` additional requirements need to be installed; the ones from the `leaderboard-2.0` and the `scenario_runner`.

```bash
pip install -r docs/requirements/requirements_leaderboard.txt
```

## Clone this repository

```bash
# Navigate to a parent folder in which you want to store the repository
git clone --recurse-submodules https://github.com/Daraan/LunaticAI-Driver-for-CARLA-Simulator.git LunaticAI
cd LunaticAI
git submodule init 
git submodule update
```

## Path Variables

### Carla Folder

Temporarily set the path variables with the following commands or register them permanently in your system, e.g. via `conda env var create`.
For Linux you can also modify your `.bashrc` or `.bash_profile` and for Windows you can use the `setx` command to set them permanently.

#### Windows

`set CARLA_ROOT=<path to carla folder>`

#### Linux

`export CARLA_ROOT=<path to carla folder>`

### Python Path

If you do not use a packaged (wheel) version of CARLA but the distributed `.egg` files locate the appropriate files and add them to your `PYTHONPATH` variable.
You find them in `${CARLA_ROOT}/PythonAPI/carla/dist`.

Adjust the file name depending on your system and Python version, for example it could look like this:

```bash
# Linux
export PYTHONPATH=$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.15-py3.10-linux-x86_64.egg:$PYTHONPATH
# or conda
conda env var create PYTHONPATH=$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.15-py3.10-linux-x86_64.egg:$PYTHONPATH
conda activate <your_env>
```
