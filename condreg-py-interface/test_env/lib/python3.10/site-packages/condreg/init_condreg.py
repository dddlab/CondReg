"""
Initialize CondrReg module
"""
import numpy as np
import sys
import os
import importlib.util

def init_condreg():
    """
    Initialize the CondrReg module and return key functions
    """
    # Instead of loading the module directly, use the one already loaded in __init__.py
    from . import condreg_cpp
    
    # Initialize functions from the module
    kgrid_func = condreg_cpp.kgrid
    
    # Define any wrapper classes or functions
    class CondrReg:
        def __init__(self):
            self.module = condreg_cpp
            
        def kgrid(self, *args, **kwargs):
            return self.module.kgrid(*args, **kwargs)
            
        # Add other methods that wrap C++ functions
        def fit(self, X, y, *args, **kwargs):
            # Call the appropriate C++ function
            return self.module.fit(X, y, *args, **kwargs)
            
        def path(self, X, y, *args, **kwargs):
            # Call the appropriate C++ function
            return self.module.path(X, y, *args, **kwargs)
    
    # Return an instance of the wrapper class
    return CondrReg()