import os
import sys
import numpy as np

# Add current directory to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import our flexible loader
from condreg_loader import import_condreg_cpp

try:
    # Get the appropriate module for our Python version
    condreg_cpp = import_condreg_cpp()
    
    # Generate sample data
    n, p = 100, 10
    np.random.seed(42)
    X = np.random.randn(n, p)
    
    # Generate grid of penalties
    gridpts = condreg_cpp.kgrid(50.0, 10)
    print("Penalty grid:", gridpts)
    
    # Test condreg with a fixed penalty
    S, invS = condreg_cpp.condreg(X, 10.0)
    eigs = np.linalg.eigvalsh(S)
    print("Condition number with k=10:", eigs[-1] / eigs[0])
    
    print("Test completed successfully!")
except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()
