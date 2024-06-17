# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# Autodoc command:
# sphinx-apidoc -d 3 -f -M -o docs/webview/source/ ./  scenario_runner agents/navigation* agents/dynamic_planning  examples/ launch_tools classes/carla_originals classes/driver* classes/vehicle* classes/rss* classes/camera*  classes.HUD classes/rule_interpreter.py classes/traffic_manager.py *logging.py  docs venv *lane_changes classes/HUD.py *keyboard_controls.py *misc.py *tools.py launch_tools*
# sphinx-build -M html docs/webview/source/ docs/webview/build/ -v -E 

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../../'))
#sys.path.insert(1, os.path.abspath('../../../agents'))
#sys.path.insert(1, os.path.abspath('../../../scenario_runner'))
if "LEADERBOARD_ROOT" in os.environ:
    sys.path.append(os.path.abspath(os.environ["LEADERBOARD_ROOT"]))
sys.path.insert(0, os.path.abspath('./'))

# already present at readthedocs, still want it for some code safeguards
os.environ.setdefault("READTHEDOCS", "local")

# -- Project information -----------------------------------------------------

project = 'LunatiAI'
copyright = ""
author = ""


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["myst_parser",
              'sphinx.ext.autodoc',
              ]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', "requirements", "spawn_points.txt", "venv", "scenario_runner", "srunner"]
exclude_patterns.extend(["launch_tools.blueprint_helpers", "agents.navigation", "dynamic_planning", "agents.tools"])


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']