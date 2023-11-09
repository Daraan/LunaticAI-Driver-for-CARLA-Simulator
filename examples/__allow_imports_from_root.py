"""
TL;DR: Add 
import __allow_imports_from_root 
to the top of your file to allow importing from the project root folder.

--------------------------------------------------------------------------------

Add project folder to sys.path
This allows running examples from the examples subfolder.
"""
import sys, os
p = os.environ.get("LUNATIC_AI_ROOT", None) 
# one-time: export LUNATIC_AI_ROOT=<path_to>/LunaticAI
# non-conda setup, modify: <env path>/bin/activate: export LUNATIC_AI_ROOT=<path_to>/LunaticAI
# conda env config vars set LUNATIC_AI_ROOT=<path_to>/LunaticAI

if p is None:
    print("Warning: CARLA_ROOT not set. Trying to use parent folder of this file.") 
    # TODO: add support for example/<subfolders>
    p = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # todo: could be more elegant and more fail safe. 
sys.path.append(p)
print('Added to sys.path: %s' % p)