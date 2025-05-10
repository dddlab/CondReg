"""
CondrReg Python package
"""
# First load the C++ module
from .condreg_loader import import_condreg_cpp
condreg_cpp = import_condreg_cpp()

# Then import other modules that might use it
from .init_condreg import init_condreg
from .init_path import add_library_path as init_path

# Define what gets imported with "from condreg import *"
__all__ = ['condreg_cpp', 'init_condreg', 'init_path']

# Export relevant classes and functions
# (Update this based on what should be exposed to users)
