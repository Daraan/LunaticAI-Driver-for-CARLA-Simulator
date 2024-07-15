# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# Autodoc command:
# sphinx-apidoc -H "Modules and Packages" -d 3 -f -o docs/webview/source/ ./  scenario_runner agents/navigation* agents/dynamic_planning  examples/ launch_tools classes/carla_originals classes/driver* classes/vehicle* classes/rss* classes/camera*  classes.HUD classes/rule_interpreter.py classes/traffic_manager.py *logging.py  docs venv *lane_changes classes/HUD.py *keyboard_controls.py *misc.py *tools.py launch_tools* docs/* conf/ *car_detection_matrix/[im]* _* *lane_explorer*
# sphinx-build -M html docs/webview/source/ docs/webview/build/ -v -E 

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
PROJECT_ROOT = '../../../'
#sys.path.insert(1, os.path.abspath('../../../agents'))
#sys.path.insert(1, os.path.abspath('../../../scenario_runner'))
sys.path.insert(0, os.path.abspath(PROJECT_ROOT))
if "LEADERBOARD_ROOT" in os.environ:
    sys.path.append(os.path.abspath(os.environ["LEADERBOARD_ROOT"]))
sys.path.insert(0, os.path.abspath('./'))

# already present at readthedocs, still want it for some code safeguards
os.environ.setdefault("READTHEDOCS", "local")
print("Are we local or on readthedocs (True)?", os.environ["READTHEDOCS"])



# Some hints for this file

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Literal
    from typing import Optional

# -- Project information -----------------------------------------------------

project = 'LunaticAI'
copyright = ""
author = ""


# -- General configuration ---------------------------------------------------

suppress_warnings = [
#    "autodoc2.*",  # suppress all
#    "autodoc2.config_error",  # suppress specific
            "config.cache",
]

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["myst_parser",
              'sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
              
              # https://pypi.org/project/sphinx-autodoc-typehints/
              #'sphinx_autodoc_typehints',
              
              #'autodoc2',
              # https://github.com/sphinx-extensions2/sphinx-autodoc2
              
              
              # https://sphinxemojicodes.readthedocs.io/en/stable/
              # https://sphinxemojicodes.readthedocs.io/#supported-codes
              'sphinxemoji.sphinxemoji',
              'sphinx.ext.intersphinx',
              #"sphinxawesome_theme", # Slow
              
              # https://www.sphinx-doc.org/en/master/usage/extensions/githubpages.html
              
              #'sphinx.ext.autosectionlabel', # many duplicates
              
              # https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html
              # 'sphinx.ext.viewcode',
              
              #https://sphinx-tippy.readthedocs.io/en/latest/
              #'sphinx_tippy',
              ]

rst_prolog = """
.. role:: python(code)
    :language: python
    :class: highlight

.. _Hydra: https://hydra.cc/

"""

intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
                                       'omegaconf' : ('https://omegaconf.readthedocs.io/en/latest/', '_omegaconf-inv_patch.inv'),
                                       'carla' : ('https://carla.readthedocs.io/en/latest/', '_carla-inv.inv'),
                                       'scenario_runner' : ('https://github.com/carla-simulator/scenario_runner/', '_scenario_runner-inv.inv'),
                                       'pygame' : ("https://www.pygame.org/docs/", None),
                                       #'cachetools' : ("https://cachetools.readthedocs.io/en/stable/", None),
                       }

# Autodoc settings
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

# See https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_default_options
autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': '__init__',
    'private-members': "_auto_init_",
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'inherited-members': True,
}
"""
The supported options are 'members', 'member-order', 'undoc-members', 'private-members', 
'special-members', 'inherited-members', 'show-inheritance', 'ignore-module-all', 
'imported-members', 'exclude-members', 'class-doc-from' and 'no-value'.
"""

autodoc_member_order = 'groupwise' # type: Literal["alphabetical", "bysource", "groupwise"]
autodoc_class_signature = "mixed" # "separated" or "mixed"

autodoc_mock_imports = ["leaderboard", "pygame", "shapely", 
                                   "py_trees", "pandas", "numpy", "matplotlib", 
                                   "pylab", "networkx", "graphviz", "cachetools", "six", "scenario_runner", "srunner"]

autodoc_typehints="both"

autodoc_typehints_description_target="all"
"""
This value controls whether the types of undocumented parameters and return values are documented when autodoc_typehints is set to description.
The default value is "all", meaning that types are documented for all parameters and return values, whether they are documented or not.
When set to "documented", types will only be documented for a parameter or a return value that is already documented by the docstring.
With "documented_params", parameter types will only be annotated if the parameter is documented in the docstring. The return type is always annotated (except if it is None).
"""

autodoc_typehints_format = 'short' # "short" or "fully-qualified"

autodoc_preserve_defaults = True #???
"""
If True, the default argument values of functions will be not evaluated on generating document. It preserves them as is in the source code.
"""


# -------------- 'sphinx_autodoc_typehints' --------------
# https://pypi.org/project/sphinx-autodoc-typehints/


typehints_defaults = "comma" # type: Literal["comma", "braces", "braces-after"] | None
always_use_bars_union = True # | instead of Union
always_document_param_types = False # default False
typehints_fully_qualified = False # Use full names for types

"""
typehints_formatter = None

If set to a function, this function will be called with annotation as first argument 
and sphinx.config.Config argument second. The function is expected to return a string with 
reStructuredText code or None to fall back to the default formatter.
"""

from enum import Enum

config_clone = None
from sphinx_autodoc_typehints import get_annotation_module, format_annotation
from sphinx.config import Config
import re

import sphinx_autodoc_typehints

#sphinx_autodoc_typehints.add_type_css_class = lambda x: x

if "sphinx_autodoc_typehints" in extensions:

    def typehints_formatter(annotation, config : Config):
        # Default see: https://github.com/tox-dev/sphinx-autodoc-typehints/blob/df669800eef5da7e952a24b84501846694b27101/src/sphinx_autodoc_typehints/__init__.py#L180
        if annotation is None:
            return None
        global config_clone
        #breakpoint()
        if config_clone is None:
            config_clone = Config(config._raw_config, overrides={"typehints_formatter" : None})
            config_clone._options = config._options
            #config_clone.typehints_fully_qualified = True #maybe
        formatted = format_annotation(annotation, config_clone)
        # has style f":py:{role}:`{prefix}{full_name}`{escape}{formatted_args}"
        formatted = formatted.replace("libcarla.", "")

        #formatted = re.sub(r":py:(\w+):`~?([a-zA-Z0-9_]+\.)*?([a-zA-Z0-9_]+)`", r"\3", formatted)
        
        #return str(annotation)u
        
        return formatted
    
    #typehints_formatter = None

typehints_use_signature = True # (default: False): If True, typehints for parameters in the signature are shown.

typehints_use_signature_return = True # (default: False): If True, return annotations in the signature are shown.


# see https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-attributes-inline
# and 
myst_enable_extensions = ["attrs_inline", "attrs_block", "colon_fence"]
myst_heading_anchors = 3

# Open all external links in a new tab 
myst_links_external_new_tab = True

# True to convert the type definitions in the docstrings as references. Defaults to False.
napoleon_preprocess_types = True


napoleon_use_param = True
"""Us emultiple :param: instead of :parameters: in the output. Defaults to False."""

napoleon_use_rtype = True
"""Will use """
typehints_use_rtype = True

typehints_document_rtype = False
"""Process by autodoc_type_hints"""

#napoleon_type_aliases = {}
"""
A mapping to translate type names to other names or references. Works only when napoleon_use_param = True. Defaults to None.

    With:

    napoleon_type_aliases = {
        "CustomType": "mypackage.CustomType",
        "dict-like": ":term:`dict-like <mapping>`",
    }
"""
    

#
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


# Autodoc2 settings

autodoc2_packages = [
    {
        "path": PROJECT_ROOT,
        "auto_mode": False,
    },
]

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

# ----- Patching the code -----

# patch only locally, as long as apidoc is run only locally
if os.environ['READTHEDOCS'] == 'local':
    import _edit_rules
    for name, foo in vars(_edit_rules).items():
        if name.startswith("_"):
            continue
        if callable(foo):
            foo()