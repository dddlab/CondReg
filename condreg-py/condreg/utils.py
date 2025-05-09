import numpy as np

def kgrid(gridmax, numpts):
    """
    Return a vector of grid of penalties for cross-validation.
    
    Parameters
    ----------
    gridmax : float
        Maximum value in penalty grid
    numpts : int
        Number of points in penalty grid
        
    Returns
    -------
    array
        Vector of penalties between 1 and approximately gridmax with logarithmic spacing
    """
    x = np.linspace(1, gridmax, numpts)
    y = 1 / x
    y = y - np.min(y)
    y = y / np.max(y)
    y = (y * (gridmax - 1)) + 1
    return y

def pfweights(sigma):
    """
    Compute optimal portfolio weights.
    
    Parameters
    ----------
    sigma : array-like
        Covariance matrix
        
    Returns
    -------
    array
        New portfolio weights
    """
    p = sigma.shape[1]
    w = np.linalg.solve(sigma, np.ones(p))
    return w / np.sum(w)

def transcost(wnew, wold, lastearnings, reltc, wealth):
    """
    Compute transaction cost.
    
    Parameters
    ----------
    wnew : array-like
        New portfolio weights
    wold : array-like
        Old portfolio weights
    lastearnings : float
        Earnings from last period
    reltc : float
        Relative transaction cost
    wealth : float
        Current wealth
        
    Returns
    -------
    float
        Transaction cost of rebalancing portfolio
    """
    wold = lastearnings * wold
    if np.sum(wold) != 0:
        wold = wold / np.sum(wold)
    return wealth * reltc * np.sum(np.abs(wnew - wold))
