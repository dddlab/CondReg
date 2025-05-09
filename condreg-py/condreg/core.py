import numpy as np
from scipy import linalg
from .path_solvers import path_forward, path_backward

def condreg(data_in, kmax):
    """
    Compute the condition number regularized covariance matrix.
    
    Parameters
    ----------
    data_in : array-like or dict
        Input data matrix (n x p) or dict with spectral decomposition
    kmax : float
        Regularization parameter
        
    Returns
    -------
    dict
        Dictionary containing regularized covariance matrix S and its inverse invS
    """
    if not isinstance(data_in, dict):
        n, p = data_in.shape
        S = (data_in.T @ data_in) / n
        # Compute SVD
        u, d, _ = linalg.svd(S, full_matrices=False)
        data_in = {'Q': u, 'L': d}
    
    sol = ml_solver(data_in['L'], kmax)
    Lbar = sol['Lbar'].flatten()
    
    # Reconstruct matrices
    S = data_in['Q'] @ np.diag(Lbar) @ data_in['Q'].T
    invS = data_in['Q'] @ np.diag(1/Lbar) @ data_in['Q'].T
    
    return {'S': S, 'invS': invS}

def ml_solver(L, k, direction='forward'):
    """
    Compute shrinkage of eigenvalues for condreg.
    
    Parameters
    ----------
    L : array-like
        Vector of eigenvalues
    k : float or array-like
        Penalty parameter(s)
    direction : str, optional
        Direction of path solver ('forward' or 'backward')
        
    Returns
    -------
    dict
        Dictionary containing shrinked eigenvalues and optimization details
    """
    L = np.asarray(L)
    if np.isscalar(k):
        k = np.array([k])
    else:
        k = np.asarray(k)
    
    p = len(L)
    g = len(k)
    
    Lbar = np.zeros((g, p))
    uopt = np.zeros(g)
    intv = np.zeros(g, dtype=bool)
    
    # Replace small eigenvalues with machine epsilon
    L[L < np.finfo(float).eps] = np.finfo(float).eps
    
    # Handle degenerate cases
    degenidx = k > (L[0] / L[-1])
    if np.any(degenidx):
        Lbar[degenidx, :] = np.tile(L, (np.sum(degenidx), 1))
        uopt[degenidx] = np.maximum(1 / (k[degenidx] * L[-1]), 1 / L[0])
        intv[degenidx] = True
    
    # Handle non-degenerate cases
    if np.any(~degenidx):
        kmax1 = k[~degenidx]
        
        # Choose path algorithm
        if direction == 'forward':
            path = path_forward(L)
        elif direction == 'backward':
            path = path_backward(L)
        else:
            raise ValueError("direction must be either 'forward' or 'backward'")
        
        # Linear interpolation
        from scipy.interpolate import interp1d
        interp_func = interp1d(path['k'], 1/path['u'], assume_sorted=True)
        uopt_nondegenerate = 1/interp_func(kmax1)
        
        # Compute lambda (shrinkage parameters)
        lambda_mat = np.minimum(
            np.tile(kmax1[:, np.newaxis] * uopt_nondegenerate[:, np.newaxis], (1, p)),
            np.maximum(
                np.tile(uopt_nondegenerate[:, np.newaxis], (1, p)),
                np.tile(1/L, (len(kmax1), 1))
            )
        )
        
        # Compute shrinked eigenvalues
        d_shrunk = 1 / lambda_mat
        
        # Update results
        Lbar[~degenidx, :] = d_shrunk
        uopt[~degenidx] = uopt_nondegenerate
        intv[~degenidx] = False
    
    return {'Lbar': Lbar, 'uopt': uopt, 'intv': intv}
