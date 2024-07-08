# Installation

## Requirements

To setup CARLA refer to the [official documentation](https://carla.readthedocs.io/en/latest/). Ensure all environment variables and dependencies are correctly configured.

### Minimum Setup

```bash
# Clone the repository
git clone --recurse-submodules https://github.com/Daraan/LunaticAI-Driver-for-CARLA-Simulator.git LunaticAI
cd LunaticAI

# Install the dependencies
pip install -r docs/requirements/requirements.txt

# Use these two commands if you forgot the --recurse-submodules in the first step
git submodule init 
git submodule update
```

### Leaderboard Setup

If you want to use the [`LunaticChallenger`](#agents.leaderboard_agent.LunaticChallenger) additional requirements need to be installed to setup the [`Leaderboard 2.0`](https://leaderboard.carla.org/get_started/). The [`scenario_runner`](https://github.com/carla-simulator/scenario_runner) is already included as a submodule.

Follow the instructions in the [Leaderboard 2.0](https://leaderboard.carla.org/get_started/), **however apply the following changes**:

1. Use the newer `master` branch
    `git clone -b master --single-branch https://github.com/carla-simulator/leaderboard.git`
2. Skip the requirements if you are using Python 3.10, they are already included our requirements.
3. If you are using Python 3.9+ check if the pull request [Python 3.9+ support](https://github.com/carla-simulator/leaderboard/pull/182) is included yet; if not, apply the changes manually:

    ```bash
    # Alternatively use the patch file from docs/requirements/leaderboard_8e5eda.patch
    cd leaderboard
    git remote add other https://github.com/Daraan/leaderboard-fork.git
    git fetch patch upgrade-dependencies
    git cherry-pick 8e5eda14e96c05387d9714086b5f7b90b13fd4df --no-commit
    ```

### Documentation

If you locally want to build the documentation you need to additionally install sphinx.
More information you can find in `docs/webview/source/conf.py`.

```bash
pip install -r docs/requirements/_readthedocs.txt
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

```sh
set CARLA_ROOT=<path to carla folder>
```

#### Linux

```bash
export CARLA_ROOT=<path to carla folder>
```

### Python Path

If you do not use a packaged version of CARLA, e.g. installed via pip, but the distributed `.egg` files that come with carla locate the appropriate files and add them to your `PYTHONPATH` variable.
You find them in `${CARLA_ROOT}/PythonAPI/carla/dist`.

Adjust the file name depending on your system and Python version, for example it could look like this:

```bash
# Linux; temporary
export PYTHONPATH=$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.15-py3.10-linux-x86_64.egg:$PYTHONPATH

# or conda
conda activate <your_env>

conda env var create PYTHONPATH=$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.15-py3.10-linux-x86_64.egg:$PYTHONPATH

conda activate <your_env>
```

## Troubleshooting

### Importing Carla fails

There are multiple reasons for that. First consult the [CARLA documentation](https://carla.readthedocs.io/en/latest/getting_started/) and check if you have installed all necessary dependencies.

### AttributeError: `xml.etree.ElementTree.Element' object has no attribute 'getchildren'

This is caused by the fact that the `xml.etree.ElementTree.Element.getchildren()` method was removed in Python 3.9.
Recent versions of the `scenario_runner` include this patch. For the[Leaderboard Setup](#leaderboard-setup) see how to acquire this patch.

For all other cases, you can apply the patch manually at the error location; exchange:

```diff
- for elem in scenario.getchildren():
+ for elem in list(scenario):
```

### RuntimeError: Spawn failed because of collision at spawn position

An actor is tried to spawned at a blocked position. Restart your simulation and try again.

### 'GLIBCXX_3.4.30' not found

In case you run into this error, be sure to first import carla and pygame afterwards.

```python
ImportError: ./lib/libstdc++.so.6: version 'GLIBCXX_3.4.30' not found (required by /home/.cache/Python-Eggs/carla-0.9.15-py3.10-linux-x86_64.egg-tmp/carla/libcarla.cpython-310-x86_64-linux-gnu.so)
```

This issue is tracked [here](https://github.com/carla-simulator/carla/issues/7862#issuecomment-2194905685).
