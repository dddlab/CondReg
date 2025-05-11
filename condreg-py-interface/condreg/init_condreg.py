"""
Initialize CondrReg module to match the R implementation
"""
import numpy as np
import sys
import os
import importlib.util

def init_condreg():
    """
    Initialize the CondrReg module and return a wrapper class that matches
    the original R implementation
    """
    # Use the module already loaded in __init__.py
    from . import condreg_cpp
    
    class CondrReg:
        """
        Python wrapper for the conditional regression C++ module that
        exactly matches the R implementation's API
        """
        def __init__(self):
            self.module = condreg_cpp
        
        def kgrid(self, gridmax, numpts):
            """
            Return a vector of grid of penalties for cross-validation
            
            Parameters:
                gridmax (float): maximum value in penalty grid
                numpts (int): number of points in penalty grid
                
            Returns:
                numpy.ndarray: vector of penalties between 1 and approximately
                gridmax with logarithmic spacing
            """
            return np.asarray(self.module.kgrid(gridmax, numpts))
        
        def select_condreg(self, X, k, **kwargs):
            """
            Compute the best condition number regularized based 
            based on cross-validation selected penalty parameter
            
            Parameters:
                X (numpy.ndarray): n-by-p matrix of data
                k (numpy.ndarray): vector of penalties for cross-validation
                **kwargs: additional parameters for select_kmax
                
            Returns:
                dict: Dictionary with keys:
                    S: condition number regularized covariance matrix
                    invS: inverse of the regularized covariance matrix
                    kmax: selected penalty parameter
            """
            # Process kwargs
            cv_folds = kwargs.get('fold', min(X.shape[0], 10))
            
            # Convert X to numpy array if it's not
            X = np.asarray(X, dtype=np.float64)
            k = np.asarray(k, dtype=np.float64)
            
            # Call select_condreg from C++
            result = self.module.select_condreg(X, k, cv_folds)
            
            # Return dictionary to match R's list return
            return {
                'S': result.S,
                'invS': result.invS,
                'kmax': result.kmax if hasattr(result, 'kmax') else None
            }
        
        def condreg(self, data_in, kmax):
            """
            Compute the condition number with given penalty parameter
            
            Parameters:
                data_in (numpy.ndarray): input data or decomposition
                kmax (float): scalar regularization parameter
                
            Returns:
                dict: Dictionary with keys:
                    S: condition number regularized covariance matrix
                    invS: inverse of the regularized covariance matrix
            """
            # Convert to numpy array if it's not
            data_in = np.asarray(data_in, dtype=np.float64)
            
            # Call condreg from C++
            result = self.module.condreg(data_in, kmax)
            
            # Return dictionary to match R's list return
            return {
                'S': result.S,
                'invS': result.invS
            }
        
        def pfweights(self, sigma):
            """
            Compute optimal portfolio weights
            
            Parameters:
                sigma (numpy.ndarray): covariance matrix
                
            Returns:
                numpy.ndarray: new portfolio weights
            """
            sigma = np.asarray(sigma, dtype=np.float64)
            return np.asarray(self.module.pfweights(sigma))
        
        def transcost(self, wnew, wold, lastearnings, reltc, wealth):
            """
            Compute transaction cost
            
            Parameters:
                wnew (numpy.ndarray): new portfolio weights
                wold (numpy.ndarray): old portfolio weights
                lastearnings (float): earnings from last period
                reltc (float): relative transaction cost
                wealth (float): current wealth
                
            Returns:
                float: transaction cost of rebalancing portfolio
            """
            wnew = np.asarray(wnew, dtype=np.float64)
            wold = np.asarray(wold, dtype=np.float64)
            return self.module.transcost(wnew, wold, lastearnings, reltc, wealth)
        
        def select_kmax(self, X, k, fold=None):
            """
            Selection of penalty parameter based on cross-validation
            
            Parameters:
                X (numpy.ndarray): n-by-p data matrix
                k (numpy.ndarray): vector of penalties for cross-validation
                fold (int, optional): number of folds for cross-validation
                
            Returns:
                dict: Dictionary with keys:
                    kmax: selected penalty parameter
                    negL: negative log-likelihood values
            """
            if fold is None:
                fold = min(X.shape[0], 10)
                
            X = np.asarray(X, dtype=np.float64)
            k = np.asarray(k, dtype=np.float64)
            
            result = self.module.select_kmax(X, k, fold)
            
            return {
                'kmax': result.kmax,
                'negL': result.negL
            }
    
    # Return an instance of the wrapper class
    return CondrReg()