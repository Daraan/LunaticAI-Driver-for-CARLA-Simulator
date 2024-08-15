from inspect import Signature
import re
from typing import TYPE_CHECKING, Any, Iterable, Optional
from typing_extensions import Literal

import docutils.nodes
import sphinx
import sphinx.addnodes
import sphinx.application
import sphinx.environment
from sphinx.transforms import post_transforms
from sphinxnotes.comboroles import CompositeRole

if TYPE_CHECKING:
    import docutils
    

check_doctree = None
IGNORE_INCLUDE_MD = True

RE_MATCH_FILE = re.compile(r"^(?P<path>[a-zA-Z0-9_/.]*/)(?P<file>[a-zA-Z0-9_.]+\.(?P<ext>\w+))?(?P<fragment>#.*)?$")
"""Pattern for ./path/to/file.md#fragment"""

REMOTE_URL = "https://github.com/Daraan/LunaticAI-Driver-for-CARLA-Simulator" # might be overwritten by conf.py

class InjectClassRole(CompositeRole):
    """Insert css classes into an existing node without creating a new node"""

    def __init__(self, roles: list[str]=[], nested_parse: bool=True, *, classes: list[str] ):
        super().__init__(["raw-inject"] + roles, nested_parse)
        self.classes = classes

    def run(self):
        allnodes, messages = super().run()
        # remove raw-inject node and insert classes
        inner: "docutils.nodes.Node" = allnodes[0].children[0]
        inner.parent = None
        inner.attributes["classes"].extend(self.classes) # type: ignore[attr-defined]
        return [inner], messages


def missing_reference_handle(app : "sphinx.application.Sphinx", 
                             env : "sphinx.environment.BuildEnvironment", 
                             node : "sphinx.addnodes.pending_xref", 
                             contnode : "docutils.nodes.Node") -> "docutils.nodes.Node | None":
    """
    Depending on the priority might not trigger
    """
    print(node)
    #breakpoint()
    if node.attributes["refdomain"] == "py" or ":py:" in node.rawsource or node.attributes["reftype"] == "term":
        if node.rawsource and ":py:" not in node.rawsource:
            print("Missing reference: skipping", node.rawsource)
        return None
    print(env.docname, node.rawsource) # doc currently parsed
    print("missing:  " + str(node), "  in :" + str(contnode), sep="\n")


def doctree_read_listener(app, doctree : "docutils.nodes.document"):
    # disabled
    global check_doctree
    if not check_doctree:
        return
    _fix_node_targets(doctree.findall(sphinx.addnodes.pending_xref))
    check_doctree = None
    

def _fix_node_targets(nodes : "Iterable[docutils.nodes.Node]"):
    for node in nodes:
        FileResolver.fix_taget_of_node(node)

class FileResolver(post_transforms.ReferencesResolver):

    default_priority = 11 # before myst parser
    document : "docutils.nodes.document"

    _py_node = []
    """Store correct nodes here for comparison during debugging"""

    @staticmethod
    def get_py_nodes(document=None):
        if not document:
            return FileResolver._py_node
        return [node for node in FileResolver._py_node if node.attributes.get("refdoc", False) == document]

    @staticmethod
    def fix_taget_of_node(node : sphinx.addnodes.pending_xref):
        """
        Assure that .py and .md links in markdown point to the correct target.
        """
        # Special cases
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
                # Point to github conf/
                node["reftarget"] = "/".join((REMOTE_URL, "tree/main/conf/")) # if left untouched will point to local conf/
                node["classes"].extend(["github", "fa", "fa-github"])         # type: ignore[attr-defined]
                newnode = docutils.nodes.reference(node.rawsource, "", *node.children, **node.attributes, internal=False, refuri=node["reftarget"])
                node.replace_self(newnode)
                return
            if check_doctree and check_doctree[1] == "index":
                # add xref class
                current_node = node
                while current_node.children:
                    current_node = current_node.children[0]
                    if isinstance(current_node, docutils.nodes.literal):
                        if "xref" not in current_node["classes"]:
                            current_node["classes"].append("xref")   # type: ignore[attr-defined]
            
            # Check for file links
            match = RE_MATCH_FILE.match(reftarget)
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
                        fragment = match.group("fragment")
                        if fragment:
                            node.attributes["reftargetid"] = fragment.lstrip("#")
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


def include_read_listener(app, relative_path:str, parent_docname:str, content: list[str]):
    if IGNORE_INCLUDE_MD and any("include:: _include.md" in line for line in content): # problem if two includes!
        return
    global check_doctree
    check_doctree = (relative_path, parent_docname, content)
    print("Include read:", relative_path, parent_docname)


def source_read_listener(app : "sphinx.application.Sphinx", docname : str, content : list[str]):
    """Trigger to check for simple rst <- .md includes"""
    for line in content[:10]:
        if ":parser: myst_parser.sphinx_" in line and not (IGNORE_INCLUDE_MD and any("include:: _include.md" in line for line in content)):
            global check_doctree
            print("setting check doctree from source read")
            check_doctree = (None, docname, content)
            
            
def autodoc_skip_member(app : "sphinx.application.Sphinx",
                        what : Literal["module", "class", "exception", 
                                       "function", "method", "attribute"], 
                        name : str, obj, skip: "bool | None", options) -> "bool | None":
    """
    options: autodoc options, like in agents.rst
    
    Emitted when autodoc has to decide whether a member should be included in the documentation. 
    The member is excluded if a handler returns True. It is included if the handler returns False.

    If more than one enabled extension handles the autodoc-skip-member event, autodoc will use the 
    first non-None value returned by a handler. Handlers should return None to fall back to the 
    skipping behavior of autodoc and other enabled extensions.
    
    Args:
        options : the options given to the directive: an object with attributes inherited_members, 
                  undoc_members, show_inheritance and no-index that are true if the flag option of 
                  same name was given to the auto directive
    """
    return skip



from _autodoc_type_aliases import autodoc_type_aliases

_convert = {
    '_ActionType[_Rule, _P, _T]' : autodoc_type_aliases["_ActionType"],
    '_ConditionType[_Rule, _CP, _CH]' : autodoc_type_aliases["_ConditionType"],
    '_CallableCondition[_Rule, _CP, _CH]' : autodoc_type_aliases["_ConditionType"],
    '_ActionTypeAlias' : autodoc_type_aliases["_ActionType"],
    '_ActorList' : 'list',
    'CallableAction' : autodoc_type_aliases["_ActionType"],
    'ConditionFunctionLike[Self, _P, _H]' : autodoc_type_aliases["_ConditionType"],
    'NoReturn' : 'typing.NoReturn',
    'Iterable' : 'typing.Iterable',
}


# autodoc-before-process-signature
def before_type_hint_cleaner(app : sphinx.application.Sphinx, obj : Any, bound_method : bool):
    """
    Process object signature
    
    Note: processes
    """
    try:
        # signature = sphinx.util.inspect.signature(obj, type_aliases=options.autodoc_type_aliases)
        signature: str | None | Signature = getattr(obj, "__signature__", None)
        if not signature:
            return
        for replace_th, new_hint in _convert.items():
            for keyword, typehint in obj.__annotations__.items():
                if isinstance(typehint, str):
                    obj.__annotations__[keyword] = typehint.replace(replace_th, new_hint)
                if isinstance(signature, str):
                    signature = signature.replace(replace_th, new_hint)
                elif keyword == "return":
                    if isinstance(signature.return_annotation, str):
                        signature.replace(return_annotation=signature.return_annotation.replace(replace_th, new_hint))
                elif isinstance(signature.parameters[keyword].annotation, str):
                    signature.parameters[keyword]._annotation = signature.parameters[keyword]._annotation.replace(replace_th, new_hint)
                else:
                    continue
            
        if bound_method and hasattr(obj, "__func__"):
            setattr(obj.__func__, "__signature__", signature)
        else:
            setattr(obj, "__signature__", signature)
    except Exception as e:
        print("Error in before_type_hint_cleaner", e)
        #breakpoint()

import re


# autodoc-process-signature
def type_hint_cleaner(app : sphinx.application.Sphinx, 
                      what : Literal["module", "class", "exception", 
                                       "function", "method", "attribute"],
                      name : str, 
                      obj : Any, 
                      options : dict, 
                      signature : Optional[str], 
                      return_annotation : Optional[str]):
    
    for replace_th, new_hint in _convert.items():
        if return_annotation:
            return_annotation = return_annotation.replace(replace_th, new_hint)
        if signature:
            signature = signature.replace(replace_th, new_hint)

    return signature, return_annotation