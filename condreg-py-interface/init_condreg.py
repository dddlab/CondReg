import os
import sys
import importlib.util

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the current directory to the Python path
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Path to the .so file
so_path = os.path.join(current_dir, 'condreg_cpp.cpython-312-darwin.so')

# Check if the .so file exists
if not os.path.exists(so_path):
    # If not, look for other potential .so files
    potential_files = [f for f in os.listdir(current_dir) if f.startswith('condreg_cpp') and f.endswith('.so')]
    if potential_files:
        so_path = os.path.join(current_dir, potential_files[0])
        print(f"Found alternative .so file: {so_path}")
    else:
        raise ImportError("Could not find condreg_cpp shared library")

# Try importing the module from the .so file
spec = importlib.util.spec_from_file_location("condreg_cpp", so_path)
condreg_cpp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(condreg_cpp)

# Set the library path for the condreg shared library
condreg_cpp_build = os.path.abspath(os.path.join(current_dir, '..', 'condreg-cpp', 'build'))
if sys.platform == 'darwin':
    os.environ['DYLD_LIBRARY_PATH'] = condreg_cpp_build
else:
    os.environ['LD_LIBRARY_PATH'] = condreg_cpp_build

# Export the module for ease of use
sys.modules['condreg_cpp'] = condreg_cpp