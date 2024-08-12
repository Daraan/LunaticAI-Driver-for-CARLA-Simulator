"""
Executing this files allows to run all files in the examples folder.
"""
import os
import sys
import importlib.util


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


if os.path.basename(os.getcwd()) == "examples":
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # run from main folder
    print("Changed to directory", os.getcwd(), "from", os.path.basename(os.getcwd()))
py_files = sorted(list_py_files("examples"))
sys.path.insert(0,"")  # for import __allow_imports_from_root to work
# Choose file

for i, file in enumerate(py_files):
    print(f"{i + 1}. {file}")

try:
    # Pass file pathor index directly
    if sys.argv[-1] in py_files:
        file_path = sys.argv[-1]
        idx = None
    else:
        idx = int(sys.argv[-1]) - 1  # use last argument as index
except ValueError:
    try:
        idx = int(input("Enter number of file to run: ")) - 1
    except KeyboardInterrupt:
        exit()
if idx is not None:
    file_path = py_files[idx]

# run file



module_name = os.path.basename(file_path).split(".")[0]
print("\n----------------------------", f"Example Running {module_name}...", "\n----------------------------")
print("\n\n")

spec = importlib.util.spec_from_file_location("__main__", file_path)
if not spec:
    raise FileNotFoundError(f"File {file_path} not found.")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)  # type: ignore[attr-defined]
