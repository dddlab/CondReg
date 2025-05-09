from .core import condreg
from .cv import select_kmax, crbulk
from .utils import kgrid, pfweights, transcost
import numpy as np

def select_condreg(X, k, **kwargs):
    """
    Compute the best condition number regularized based on cross-validation.
    
    Parameters
    ----------
    X : array-like
        n-by-p data matrix
    k : array-like
        Vector of penalties for cross-validation
    **kwargs : dict
        Additional parameters for select_kmax
        
    Returns
    -------
    dict
        Dictionary containing regularized covariance matrix S, its inverse invS,
        and the selected penalty parameter kmax
    """
    n, p = X.shape
    
    # Select optimal kmax via cross-validation
    kmax_result = select_kmax(X, k, **kwargs)
    
    # Compute sample covariance
    S = (X.T @ X) / n
    
    # SVD decomposition
    u, d, _ = np.linalg.svd(S, full_matrices=False)
    
    # Spectral decomposition
    QLQ = {'Q': u, 'L': d}
    
    # Apply condreg with selected kmax
    soln = condreg(QLQ, kmax_result['kmax'])
    
    # Return results
    return {
        'S': soln['S'], 
        'invS': soln['invS'],
        'kmax': kmax_result['kmax']
    }

__all__ = [
    'condreg',
    'select_condreg',
    'select_kmax',
    'crbulk',
    'kgrid',
    'pfweights',
    'transcost'
]
