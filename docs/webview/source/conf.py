# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# Autodoc command:
# sphinx-apidoc -H "Modules and Packages" -d 3 -f -o docs/webview/source/ ./  scenario_runner agents/navigation* agents/dynamic_planning  examples/ launch_tools  classes/driver* classes/vehicle* classes/rss* classes/camera*  classes.HUD classes/rule_interpreter.py classes/traffic_manager.py  docs venv *lane_changes classes/HUD.py *keyboard_controls.py *misc.py *tools.py launch_tools* docs/* conf/ *car_detection_matrix/[im]* _* *lane_explorer*
# sphinx-build -M html docs/webview/source/ docs/webview/build/ -v -E

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

# ruff: noqa: FA102
import os
from pathlib import Path
import sys

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    import sphinx
    import sphinx.application
    import sphinx.environment
    import sphinx.addnodes


PROJECT_ROOT = '../../../'
#sys.path.insert(1, os.path.abspath('../../../agents'))
#sys.path.insert(1, os.path.abspath('../../../scenario_runner'))
sys.path.insert(0, os.path.abspath(PROJECT_ROOT))
if "LEADERBOARD_ROOT" in os.environ:
    sys.path.append(os.path.abspath(os.environ["LEADERBOARD_ROOT"]))
sys.path.insert(0, os.path.abspath('./'))

# already present at readthedocs, still want it for some code safeguards
os.environ.setdefault("READTHEDOCS", "local")

RTD_ONLINE = os.environ["READTHEDOCS"] != "local"

print("Are we local or on readthedocs (True)?", os.environ["READTHEDOCS"])

# ruff: noqa: E402
# must be done after adjusting the sys.path
from docs.webview.source import _conf_extensions
from docs.webview.source._conf_extensions import (
    InjectClassRole,
    FileResolver,
    before_type_hint_cleaner,
    missing_reference_handle,  # noqa: F401
    source_read_listener, include_read_listener,
    REMOTE_URL, type_hint_cleaner,
)
from docs.webview.source._autodoc_type_aliases import autodoc_type_aliases


# -- Project information -----------------------------------------------------

project = 'LunaticAI'
copyright = ""  # noqa: A001
author = ""


if RTD_ONLINE:
    GIT_BRANCH : str  = os.environ.get("READTHEDOCS_GIT_IDENTIFIER", "unknown")
else:
    import subprocess
    GIT_BRANCH = subprocess.check_output("git rev-parse --abbrev-ref HEAD", shell=True, text=True).strip()
    
if RTD_ONLINE:
    GIT_URL = os.environ.get("READTHEDOCS_GIT_CLONE_URL", "unknown")
    if not GIT_URL.startswith("https://"):
        GIT_URL = REMOTE_URL
else:
    GIT_URL = REMOTE_URL

_conf_extensions.REMOTE_URL = GIT_URL

base_url = html_baseurl = r"/html/"


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
              'sphinxemoji.sphinxemoji',
              'sphinx.ext.autodoc',
              # https://www.sphinx-doc.org/en/master/usage/extensions/todo.html
              'sphinx.ext.todo',
              'sphinx.ext.napoleon',
              
              # https://pypi.org/project/sphinx-autodoc-typehints/
              #'sphinx_autodoc_typehints',
              
              #'autodoc2',
              # https://github.com/sphinx-extensions2/sphinx-autodoc2
              
              'sphinx.ext.intersphinx',
              #"sphinxawesome_theme", # Slow
              
              # --- On demand ---
              
              # https://www.sphinx-doc.org/en/master/usage/extensions/githubpages.html
              
              # https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html
              # 'sphinx.ext.viewcode',
              
              # Hover tooltips on demand
              #https://sphinx-tippy.readthedocs.io/en/latest/
              #'sphinx_tippy',
              # https://github.com/readthedocs/sphinx-hoverxref
              
              'sphinxnotes.comboroles',
              ]

VERSION = os.environ.get("READTHEDOCS_VERSION", "latest")

if VERSION in ("latest", "main"):
    extensions.extend([
        'sphinx.ext.viewcode',
        'sphinx.ext.githubpages',
    ])
    # https://sphinxemojicodes.readthedocs.io/en/stable/
    # https://sphinxemojicodes.readthedocs.io/#supported-codes
if VERSION == "latest" and not RTD_ONLINE:
    extensions.append("sphinx_tippy")
elif VERSION == "latest" and RTD_ONLINE:
    extensions.append("hoverxref.extension")

todo_include_todos = VERSION != "main"
todo_emit_warnings = not RTD_ONLINE
todo_link_only = False
"""If this is True, todolist produce output without file path and line, The default is False."""

print("Using extensions:", extensions)

rst_prolog = """
.. role:: python(code)
    :language: python
    :class: highlight

.. role:: raw-inject

.. role:: external-icon-role
    :class: external-icon

.. _Hydra: https://hydra.cc/

.. _Leaderboard: https://leaderboard.carla.org
"""

intersphinx_mapping = {'python': ('https://docs.python.org/3/', None),
                                       #'typing_extensions' : ("https://docs.python.org/3/", None),
                                       # Shpinx 8
                                       'typing-extensions' : ("https://typing-extensions.readthedocs.io/en/latest/", None),
                                       'omegaconf' : ('https://omegaconf.readthedocs.io/en/latest/', '_omegaconf-inv_patch.inv'),
                                       'pygame' : ("https://www.pygame.org/docs/", None),
                                       'carla' : ('https://carla.readthedocs.io/en/latest/', '_carla-inv.inv'),
                                       'scenario_runner' : ('https://github.com/carla-simulator/scenario_runner/', '_scenario_runner-inv.inv'),
                                       'shapely' : ('https://shapely.readthedocs.io/en/stable/', None),
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
                                   "pylab", "networkx", "graphviz", "cachetools", "six", "scenario_runner", "srunner",
                                   "hydra", "carla"]


autodoc_type_aliases = autodoc_type_aliases

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


typehints_defaults: Literal["comma", "braces", "braces-after"] | None = "comma"
always_use_bars_union = True # | instead of Union
always_document_param_types = False # default False
typehints_fully_qualified = False # Use full names for types

"""
typehints_formatter = None

If set to a function, this function will be called with annotation as first argument
and sphinx.config.Config argument second. The function is expected to return a string with
reStructuredText code or None to fall back to the default formatter.
"""

if "sphinx_autodoc_typehints" in extensions:
    config_clone = None
    from sphinx.config import Config
    from sphinx_autodoc_typehints import get_annotation_module, format_annotation  #noqa: F401

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


# ------ Viewcode ------

viewcode_line_numbers = True

# -------------- Tippy --------------

tippy_rtd_urls = [
    #"https://carla.readthedocs.io/en/latest/",
    #"https://docs.python.org",
    #"https://docs.python.org/v3/library",
]

tippy_enable_wikitips = False # do not use
tippy_enable_doitips = False # do not use

# tippy_js = ("https://unpkg.com/@popperjs/core@2", "https://unpkg.com/tippy.js@6")
tippy_js = ("popper.min.js", "tippy.js")

tippy_add_class = "has-tippy"

# ------------- hoverxref (RTD only) --------------

hoverxref_auto_ref = True

hoverxref_intersphinx = [
    'https://omegaconf.readthedocs.io/en/latest/',
    'https://carla.readthedocs.io/en/latest/',
    'https://typing-extensions.readthedocs.io/en/latest/',
    'https://docs.python.org/3',
]


def _tooltip_python():
    return "tooltip"

def _hoverxred_python(): # call function, cannot pickle lambda
    return

hoverxref_intersphinx_types = {
    # make specific links to use a particular tooltip type
    'readthdocs': {
        'doc': 'modal',
        'ref': 'tooltip',
    },
    'python': {
        'class': 'modal',
        'ref': 'tooltip',
        'meth': 'tooltip',
        'attr': 'tooltip',
        'exc': 'tooltip',
        'func': 'tooltip',
        'obj': 'tooltip',
    },
 
}

hoverxref_domains = ['py']


hoverxref_role_types = {
    'hoverxref': 'modal',
    'ref': 'modal',  # for hoverxref_auto_ref config
    'mod': 'tooltip',  # for Python Sphinx Domain
    'class': 'tooltip',  # for Python Sphinx Domain
        'meth': 'tooltip',
        'attr': 'tooltip',
        'exc': 'tooltip',
        'func': 'tooltip',
        'obj': 'tooltip',
    'term' : 'tooltip',
}


# -------------- MyST Parser --------------

# see https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-attributes-inline
# and
myst_enable_extensions = ["attrs_inline", "attrs_block", "colon_fence"]
myst_heading_anchors = 4

# Open all external links in a new tab
myst_links_external_new_tab = True
myst_all_links_external=False

# TEST
myst_ref_domains = ["std", "py"]

myst_url_schemes = {
    "http": None,
    "https": None,
    'mailto': None, 'ftp': None,
    "carla-issue" : {
        "url": "https://github.com/carla-simulator/carla/issues/{{path}}#{{fragment}}",
        "title": "CARLA Issue #{{path}}",
        "classes": ["github", "fa", "fa-github",],
    },
    
    "gh-file" : {
        "url": GIT_URL + "/blob/" + GIT_BRANCH + "/{{path}}#{{fragment}}",
        "title": "{{path}}",
        "classes": ["github", "fa", "fa-github", "file"],
    },
    
    "py-file" : {
        "url": GIT_URL + "/blob/" + GIT_BRANCH + "/{{path}}#{{fragment}}",
        "title": "{{path}}",
        "classes": ["github", "fa", "fa-file", "fa-python", "file"],
    },
    
    "gh" : {
        "url" : "{{path}}#{{fragment}}",
        "title": "{{path}}",
        "classes": ["github", "fa", "fa-github"],
    },
}


# -------------- 'sphinx.ext.napoleon' --------------

# True to convert the type definitions in the docstrings as references. Defaults to False.
napoleon_preprocess_types = True


napoleon_use_param = True
"""Us emultiple :param: instead of :parameters: in the output. Defaults to False."""

napoleon_use_rtype = True
"""Will use `:rtype:` instead of `:returns:`. Defaults to False."""

typehints_use_rtype = True

typehints_document_rtype = False
"""Process by autodoc_type_hints"""

napoleon_type_aliases = {
    "VehicleControl": "carla.VehicleControl",
    "RuleResult.NO_RESULT" : "Rule.NO_RESULT",
}
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
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', "requirements", "spawn_points.txt", "venv", "scenario_runner", "srunner", "_*", "test.py", "test.rst"]
exclude_patterns.extend(["agents.navigation", "dynamic_planning"])
# exclude_patterns.append("launch_tools.blueprint_helpers")
# exclude_patterns.append("agents.tools")
exclude_patterns.append("launch_tools.argument_parsing")


#nitpick_ignore = [(None, None)] # not empty to allow regex
#nitpick_ignore_regex

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

#html_theme_options = {
#    'cssfiles': ["http://netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]
#}

html_theme_options = {
    "style_external_links" : False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    'external_icon.css',
    'external_alternative.css',
]

# also for hoverxref cursor
html_css_files.append("tippy.css")

html_js_files = [
   # 'stripcss.js', # inserted hardcoded
]

# ----- Patching the code -----

# patch only locally, as long as apidoc is run only locally
if os.environ['READTHEDOCS'] == 'local':
    from docs.webview.source._postprocess_autodoc import patch_all
    patch_all()
            
comboroles_roles : dict[str, list[str] | tuple[list[str], bool]] = {
    'strong_literal': ['strong', 'literal'],
    'external_py_class' : ['external-icon-role', 'py:class'],
    'external_py_meth' : ['external-icon-role', 'py:meth'],
    'external_py_mod' : ['external-icon-role', 'py:mod'],
    'external_py' : ['external-icon-role', 'py:obj'],
}
"""
The value can be list[str] with an optional bool. The list[str] is a list of existing role name to be composited, see Composite Roles for more details.

The optional bool is flag of nested_parse, indicates whether the Nested Parse function is enabled. If no optional bool is given, nested_parse is disabled by default.
"""


# ---------------------------------------------


def setup(app: "sphinx.application.Sphinx"):
    #app.add_js_file("stripcss.js", priority=199) # should have higher priority
    # if imported might be too slow, want to execute it before tippy
    from textwrap import indent
    try:
        # local from root
        app.add_js_file(None,
                        body=indent(Path('docs/webview/source/_static/stripcss.js').read_text(),
                                              prefix=" " * 8,
                                              predicate=lambda x: not x.startswith("// disables")))
    except FileNotFoundError:
        app.add_js_file(None,
                        body=indent(Path('_static/stripcss.js').read_text(),
                                    prefix=" " * 8,
                                    predicate=lambda x: not x.startswith("// disables")))
    

    # py_external = sphinx.domains.python.PyXRefRole(nodeclass="py-module", innernodeclass="py-module py-external")
    
    # ------------
    # Roles:
    # ------------
    app.add_role("external-icon-parse", InjectClassRole(classes=["external-icon"]))
    
    # ------------
    # Events:
    # see https://www.sphinx-doc.org/en/master/extdev/event_callbacks.html
    # ------------
    # app.connect("missing-reference", missing_reference_handle, priority=2000)
    app.connect("include-read", include_read_listener)
    app.connect("source-read", source_read_listener, priority=1000)
    # app.connect("doctree-read", doctree_read_listener, priority=1000)
    
    # Manually skip members
    # app.connect("autodoc-skip-member", autodoc_skip_member)
    
    # Clean type-hints
    app.connect("autodoc-before-process-signature", before_type_hint_cleaner, priority=501)
    app.connect("autodoc-process-signature", type_hint_cleaner, priority=501)
    
    app.add_transform(FileResolver)
