import numpy as np
from sklearn.model_selection import KFold

def select_kmax(X, k, folds=None):
    """
    Selection of penalty parameter based on cross-validation.
    
    Parameters
    ----------
    X : array-like
        n-by-p data matrix
    k : array-like
        Vector of penalties for cross-validation
    folds : int, optional
        Number of folds for cross-validation
        
    Returns
    -------
    dict
        Dictionary with optimal kmax and negative log-likelihood values
    """
    n, p = X.shape
    g = len(k)
    
    if folds is None:
        folds = min(n, 10)
    
    kf = KFold(n_splits=folds)
    
    neg_loglikelihood = np.zeros((folds, g))
    condmax = 1
    
    for i, (train_idx, test_idx) in enumerate(kf.split(X)):
        X_train = X[train_idx]
        X_test = X[test_idx]
        
        n_train = len(X_train)
        n_test = len(X_test)
        
        # Compute sample covariance on training data
        S_train = (X_train.T @ X_train) / n_train
        
        # Compute bulk solutions
        soln = crbulk(S_train, k)
        
        # Transform test data
        y_test = X_test @ soln['Q']
        
        # Compute negative log-likelihood
        a = np.zeros((n_test, p, g))
        for j in range(g):
            a[:, :, j] = y_test**2
        
        a = np.transpose(a, (1, 0, 2))
        b = np.zeros((p, n_test, g))
        for j in range(g):
            b[:, :, j] = 1 / soln['Lbar'][j, :][:, np.newaxis]
        
        z_test = a * b
        
        # Sum across dimensions
        for j in range(g):
            neg_loglikelihood[i, j] = (np.sum(z_test[:, :, j]) / n_test + 
                                      np.sum(np.log(soln['Lbar'][j, :])))
        
        # Update condmax
        L_train = np.zeros(p)
        L_train[:min(n_train, p)] = soln['L'][:min(n_train, p)]
        condmax = max(condmax, L_train[0] / L_train[min(n_train, p)-1])
    
    # Select optimal kmax
    nL = np.sum(neg_loglikelihood, axis=0)
    min_indices = np.where(nL == np.min(nL))[0]
    min_idx = int(np.floor(np.median(min_indices)))
    kmax_opt = min(k[min_idx], condmax)
    
    return {'kmax': kmax_opt, 'negL': nL}

def crbulk(S, k):
    """
    Compute multiple solutions for different penalty parameters.
    
    Parameters
    ----------
    S : array-like
        Sample covariance matrix
    k : array-like
        Vector of regularization parameters
        
    Returns
    -------
    dict
        Dictionary containing matrices Q, Lbar, and L
    """
    # Import ml_solver inside the function to break circular import
    from .core import ml_solver
    
    n, p = S.shape
    g = len(k)
    
    # Compute SVD
    u, d, _ = np.linalg.svd(S, full_matrices=False)
    soln = ml_solver(d, k)
    
    # Handle case when n < p
    if n < p:
        soln['Lbar'] = np.hstack((soln['Lbar'], np.zeros((g, max(p-n, 0)))))
    
    return {'Q': u, 'Lbar': soln['Lbar'], 'L': d}