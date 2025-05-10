"""
Test cases for CondrReg package
"""
import numpy as np
import unittest
import sys
import os

# Add the parent directory to the path so we can import condreg
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the condreg package properly
import condreg

class TestCondrReg(unittest.TestCase):
    def setUp(self):
        # This runs before each test
        self.condreg = condreg
        
    def test_import(self):
        """Test that the module imports successfully"""
        self.assertIsNotNone(self.condreg)
        
    def test_init(self):
        """Test module initialization"""
        model = self.condreg.init_condreg()
        self.assertIsNotNone(model)
        
    def test_basic_functionality(self):
        """Test basic functionality with synthetic data"""
        # Generate synthetic data
        n = 20  # samples
        p = 10  # features
        X = np.random.randn(n, p)
        y = np.random.randn(n)
        
        # Initialize and test model
        model = self.condreg.init_condreg()
        
        # Add your actual functionality tests here
        # For example:
        # result = model.fit(X, y)
        # self.assertIsNotNone(result)
        
if __name__ == '__main__':
    unittest.main()
