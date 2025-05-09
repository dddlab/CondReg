import sys
import os
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import condreg
    print("Successfully imported condreg")
    print("Available functions:", dir(condreg))
except ImportError as e:
    print(f"Import error: {e}")
    
    # Print Python path for debugging
    import sys
    print("\nPython path:")
    for p in sys.path:
        print(f"  {p}")