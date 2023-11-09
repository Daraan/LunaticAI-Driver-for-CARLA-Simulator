
import os
import sys
import __allow_imports_from_root

# List files

def list_py_files(directory):
    """
    Lists all .py files in the given directory and its subdirectories.
    """
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and not file.startswith("_") and file != "example_runner.py":
                py_files.append(os.path.join(root, file))
    return py_files

os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # run from main folder
py_files = sorted(list_py_files("./examples"))

# Choose file

for i, file in enumerate(py_files):
    print(f"{i+1}. {file}")

try:
    # Pass file pathor index directly
    if sys.argv[-1] in py_files:
        file_path = py_files.index(sys.argv[-1])
        idx = None
    else:
        idx = int(sys.argv[-1]) -1 # use last argument as index
except ValueError:
    idx = int(input("Enter number of file to run: ")) -1
if idx is not None:
    file_path = py_files[idx]

# run file

import importlib.util

module_name = os.path.basename(file_path).split(".")[0]
print(f"Running {module_name}...")

spec = importlib.util.spec_from_file_location("__main__", file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
