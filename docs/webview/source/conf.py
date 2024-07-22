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
import re
import sys
import docutils


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

# Some hints for this file

from typing import TYPE_CHECKING, cast
if TYPE_CHECKING:
    from typing import Literal
    from typing import Optional
    import sphinx
    import sphinx.application
    import sphinx.environment
    import sphinx.addnodes
    import docutils.nodes
    docutils_Node = docutils.nodes.Node 

# -- Project information -----------------------------------------------------

project = 'LunaticAI'
copyright = ""
author = ""

REMOTE_URL = "https://github.com/Daraan/LunaticAI-Driver-for-CARLA-Simulator"

if RTD_ONLINE:
    GIT_BRANCH = os.environ.get("READTHEDOCS_GIT_IDENTIFIER")
else:
    import subprocess
    GIT_BRANCH = subprocess.check_output("git rev-parse --abbrev-ref HEAD", shell=True, text=True).strip()
    
if RTD_ONLINE:
    GIT_URL = os.environ.get("READTHEDOCS_GIT_CLONE_URL")
    if not GIT_URL.startswith("https://"):
        GIT_URL = REMOTE_URL
else:
    GIT_URL = REMOTE_URL
    
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
    extensions.append('sphinx.ext.viewcode')
    extensions.append('sphinx.ext.githubpages')
    # https://sphinxemojicodes.readthedocs.io/en/stable/
    # https://sphinxemojicodes.readthedocs.io/#supported-codes
if VERSION == "latest" and not RTD_ONLINE:
    extensions.append("sphinx_tippy")
elif VERSION == "latest" and RTD_ONLINE:
    extensions.append("hoverxref.extension")

print("Using extensions:", extensions)

rst_prolog = """
.. role:: python(code)
    :language: python
    :class: highlight

.. role:: raw-inject

.. role:: external-icon-role
    :class: external-icon

.. _Hydra: https://hydra.cc/

"""

intersphinx_mapping = {'python': ('https://docs.python.org/3/', None),
                                       'typing_extensions' : ("https://docs.python.org/3/", None),
                                       'omegaconf' : ('https://omegaconf.readthedocs.io/en/latest/', '_omegaconf-inv_patch.inv'),
                                       'pygame' : ("https://www.pygame.org/docs/", None),
                                       'carla' : ('https://carla.readthedocs.io/en/latest/', '_carla-inv.inv'),
                                       'scenario_runner' : ('https://github.com/carla-simulator/scenario_runner/', '_scenario_runner-inv.inv'),
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
                                   "hydra"]

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

if "sphinx_autodoc_typehints" in extensions:
    config_clone = None 
    from sphinx.config import Config
    from sphinx_autodoc_typehints import get_annotation_module, format_annotation

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

from collections import defaultdict

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
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', "requirements", "spawn_points.txt", "venv", "scenario_runner", "srunner", "_*"]
exclude_patterns.extend(["launch_tools.blueprint_helpers", "agents.navigation", "dynamic_planning", "agents.tools"])


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
    'external_py_mod' : ['external-icon-role', 'py:mod'],
}
"""
The value can be list[str] with an optional bool. The list[str] is a list of existing role name to be composited, see Composite Roles for more details.

The optional bool is flag of nested_parse, indicates whether the Nested Parse function is enabled. If no optional bool is given, nested_parse is disabled by default.
"""


def setup(app : "sphinx.application.Sphinx"):
    #app.add_js_file("stripcss.js", priority=199) # should have higher priority
    # if imported might be too slow, want to execute it before tippy
    from textwrap import indent
    try:
        # local from root
        with open("docs/webview/source/_static/stripcss.js", "r") as f:
            app.add_js_file(None, body=indent(f.read(), " "*8, predicate=lambda x: not x.startswith("// disables")))
    except FileNotFoundError:
        with open("_static/stripcss.js", "r") as f:
            app.add_js_file(None, body=indent(f.read(), " "*8, predicate=lambda x: not x.startswith("// disables")))
    

    #py_external = sphinx.domains.python.PyXRefRole(nodeclass="py-module", innernodeclass="py-module py-external")
    #app.add_role_to_domain("py", "external", py_external)
    
    from sphinxnotes.comboroles import CompositeRole
    
    class InjectClassRole(CompositeRole):
        """Insert css classes into an existing node without creating a new node"""
        
        def __init__(self, rolenames: list[str]=[], nested_parse: bool=True, *, classes: list[str] ):
            super().__init__(["raw-inject"] + rolenames, nested_parse)
            self.classes = classes
        
        def run(self):
            allnodes, messages = super().run()
            # remove raw-inject node and insert classes
            inner: "docutils_Node" = allnodes[0].children[0]
            inner.parent = None
            inner.attributes["classes"].extend(self.classes) # type: ignore[attr-defined]
            return [inner], messages

    app.add_role("external-icon-parse", InjectClassRole(classes=["external-icon"]))
    #app.connect("missing-reference", missing_reference_handle, priority=2000)
    app.connect("include-read", include_read_listener)
    app.connect("source-read", source_read_listener, priority=1000)
    #app.connect("doctree-read", doctree_read_listener, priority=1000)
    
    app.add_transform(TestResolver)

def missing_reference_handle(app : "sphinx.application.Sphinx", 
                             env : "sphinx.environment.BuildEnvironment", 
                             node : "sphinx.addnodes.pending_xref", 
                             contnode : "docutils_Node"):
    if node.attributes["refdomain"] == "py" or ":py:" in node.rawsource or node.attributes["reftype"] == "term":
        if node.rawsource and ":py:" not in node.rawsource:
            print("Missing reference: skipping", node.rawsource)
        return None
    print(env.docname, node.rawsource) # doc currently parsed
    print("missing:  " + str(node), "  in :" + str(contnode), sep="\n")


check_doctree = None

# Slugs

IGNORE_INCLUDE_MD = True

def include_read_listener(app, relative_path, parent_docname, content):
    if IGNORE_INCLUDE_MD and any("include:: _include.md" in line for line in content): # problem if two includes!
        return
    global check_doctree
    check_doctree = (relative_path, parent_docname, content)
    print("Include read:", relative_path, parent_docname)
    
def source_read_listener(app : "sphinx.application.Sphinx", docname : str, content : list[str]):
    for line in content[:10]:
        if ":parser: myst_parser.sphinx_" in line and not (IGNORE_INCLUDE_MD and any("include:: _include.md" in line for line in content)):
            global check_doctree
            print("setting check doctree freom soruce read")
            check_doctree = (None, docname, content)
    
import sphinx.addnodes


def doctree_read_listener(app, doctree : "docutils.nodes.document"):
    # disabled
    global check_doctree
    if not check_doctree:
        return
    _fix_node_targets(doctree.findall(sphinx.addnodes.pending_xref))

    check_doctree = None
    

def _fix_node_targets(nodes : "list[docutils_Node]"):
    for node in nodes:
        TestResolver.fix_taget_of_node(node)

import sphinx
from  sphinx.transforms import post_transforms
import sphinx.errors
re_match_file = re.compile(r"^(?P<path>[a-zA-Z0-9_/.]*/)(?P<file>[a-zA-Z0-9_.]+\.(?P<ext>\w+))?(?P<fragment>#.*)?$")

class TestResolver(post_transforms.ReferencesResolver):
    
    default_priority = 8 # before myst parser
    document : docutils.nodes.document
    
    _py_node = []
    
    @staticmethod
    def get_py_nodes(document=None):
        if not document:
            return TestResolver._py_node
        return [node for node in TestResolver._py_node if node.attributes.get("refdoc", False) == document]
    
    @staticmethod
    def fix_taget_of_node(node : sphinx.addnodes.pending_xref):
        if "reftarget" in node.attributes:
            reftarget :str = node.attributes["reftarget"]
            if node.attributes.get("reftargetid") == "readme-workflow":
                layers = node["refdoc"].count("/")
                newnode = docutils.nodes.reference(node.rawsource, "", *node.children, **node.attributes, internal=True, 
                                                   refid=node["reftargetid"], refuri= "../"*layers + reftarget + ".html#" + node["reftargetid"])
                #breakpoint()
                node.replace_self(newnode)
                return
            if reftarget == "conf/":
                node["reftarget"] = "/".join((GIT_URL, "tree/main/conf/")) # if left untouched will point to local conf/
                node["classes"].extend(["github", "fa", "fa-github"])
                newnode = docutils.nodes.reference(node.rawsource, "", *node.children, **node.attributes, internal=False, refuri=node["reftarget"])
                node.replace_self(newnode)
                return
            if check_doctree and check_doctree[1] == "index":
                cnode = node
                while cnode.children:
                    cnode = cnode.children[0]
                    if isinstance(cnode, docutils.nodes.literal):
                        if "xref" not in cnode["classes"]:
                            cnode["classes"].append("xref")
            match = re_match_file.match(reftarget)
            # debug
            #if node.attributes.get("refdomain") == "py":
            #    TestResolver._py_node.append(node)
            #    return
            if not match:
                return
                
            if match.group("ext"):
                if match.group("ext") == "md":
                    # e.g. ../docs/README.md -> ../docs/README, myst should be able to resolve it
                    path = match.group("path") or ""
                    node.attributes["reftarget"] = path.lstrip("./ ") + match.group("file").replace(".md", "")
                    if not node.attributes.get("refdomain"):
                        node.attributes["refdomain"] = "doc"
                    if not node.attributes.get("reftargetid"):
                        fragmet = match.group("fragment")
                        if fragmet:
                            node.attributes["reftargetid"] = fragmet.lstrip("#")
                        else:
                            node.attributes["reftargetid"] = None
                    return
                elif match.group("ext") == "py":
                    # This is more tricky
                    # could link to autodoc module or source code _modules/agents/rules.html#create_default_rules
                    
                    # Link to audodoc module
                    file = match.group("file")[:-3] # remove .py
                    # change ../agents/rules.py -> agents.
                    path = match.group("path").replace(".", "/").lstrip("/") if match.group("path") else ""
                    dotpath = path.replace("/", ".")
                    
                    # Note:
                    # node.attributes["py:class"] and node.attributes["py:module"] are refereres not the target
                    node.attributes["refdomain"] = "py"
                    if match.group("fragment"):
                        #Should be
                        #'<pending_xref py:class="True" py:module="True" refdoc="index" refdomain="py" refexplicit="True" refspecific="True" 
                        #reftarget="Phase" reftype="class" refwarn="False"><literal classes="xref py py-class">XXX</literal></pending_xref>'
                        
                        fragment = match.group("fragment").lstrip("#.")
                        node.attributes["reftargetid"] = dotpath + file + "." + fragment
                        #if "." in fragment:
                        #    node.attributes["py:class"] = fragment.split(".")[0]
                        
                        node["reftarget"] = fragment
                        node.attributes["reftype"] = "obj"
                    else:
                        #node.attributes["reftargetid"] = "module-" + dotpath + file # link to module top
                        """
                        -> Should be
                        '<pending_xref py:class="True" py:module="True" refdoc="index" refdomain="py" refexplicit="False" refspecific="True" 
                        reftarget="lunatic_agent" reftype="mod" refwarn="False"><literal classes="xref py py-mod">lunatic_agent</literal></pending_xref>'
                        """
                        node["reftarget"] = file
                        node.attributes["reftype"] = "mod"
                    
                    node.attributes["py:class"] = None
                    node.attributes["py:module"] = None
                    
                    node.attributes["refspecific"] = True # see domains.python.parse_reftarget
                    #breakpoint()

    def fix_node_targets(self, **kwargs):
        for node in self.document.findall(sphinx.addnodes.pending_xref):
            target = node['reftarget']
            if not target:
                continue
            if target in ("genindex", "modindex", "search"):
                continue
            self.fix_taget_of_node(node)
            continue
            content = self.find_pending_xref_condition(node, ("resolved", "*"))
            if content:
                contnode = cast(docutils.nodes.Element, content[0].deepcopy())
            else:
                contnode = cast(docutils.nodes.Element, node[0].deepcopy())
            
            typ = node['reftype']
            refdoc = node.get('refdoc')
            if node.get('refdomain', False):
                try:
                    domain = self.env.domains[node['refdomain']]
                except KeyError:
                    domain = None
                    newnode = None
                else:
                    if node["refdomain"] == "py" or typ == "term" or node["reftarget"] in ("genindex", "modindex", "search"):
                        continue
                    breakpoint()
                    newnode = domain.resolve_xref(self.env, node.attributes["refdoc"], self.app.builder,
                                                        typ, target, node, contnode)
            else:    
                # get node by missing-reference event
                newnode = self.app.emit_firstresult('missing-reference', self.env,
                                                                node, contnode,
                                                                allowed_exceptions=(sphinx.errors.NoUri,))
            matched = self.find_pending_xref_condition(node, ("*",))
                
            if not newnode and not matched:
                self.fix_taget_of_node(node)
                continue
            
    
    def run(self, **kwargs):
        global check_doctree
        docname = self.env.docname # is with dir/docname # no extension
        if docname == "index":
            titles = self.document.findall(docutils.nodes.section)
            for title in titles:
                if len(title.attributes["ids"]) > 1:
                    print("Multiple ids", title.attributes["ids"])
                title.attributes["ids"] = ["readme-" + title.attributes["ids"][0]]
        if check_doctree:
            (relative_path, parent_docname, content) = check_doctree
            print(check_doctree)
            
            self.fix_node_targets(**kwargs)
            check_doctree = None
        
class PreTransform(sphinx.transforms.SphinxTransform):
    pass