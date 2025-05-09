import numpy as np

def path_forward(L):
    """
    Compute optimal u using the forward algorithm.
    
    Parameters
    ----------
    L : array-like
        Vector of eigenvalues
        
    Returns
    -------
    dict
        Dictionary containing path information
    """
    p = len(L)
    
    # Handle zero eigenvalues
    idxzero = L < np.finfo(float).eps
    numzero = np.sum(idxzero)
    L = L.copy()  # Create a copy to avoid modifying the input
    L[idxzero] = np.finfo(float).eps
    
    # Initial point
    u_cur = 1 / np.mean(L)
    v_cur = u_cur
    
    # Find starting alpha
    alpha = 0
    while u_cur > 1 / L[alpha]:
        alpha += 1
        if alpha >= p-1:
            break
    
    beta = alpha + 1
    slope_num = np.sum(L[:alpha]) # Initialize the path
    slope_denom = np.sum(L[beta:])
    
    # Initialize path
    u = [u_cur]
    v = [v_cur]
    kmax = [1]
    
    r = p - numzero
    is_done = False
    
    # Main path-finding loop
    while alpha >= 0 and beta <= r-1:
        # Rectangle boundaries
        h_top = 1 / L[beta]
        v_left = 1 / L[alpha]
        
        # Compute intersection with horizontal line
        v_new = h_top
        u_new = u_cur - slope_denom * (v_new - v_cur) / slope_num
        
        # If outside rectangle, compute intersection with vertical line
        if u_new < v_left:
            u_new = v_left
            v_new = v_cur - slope_num * (u_new - u_cur) / slope_denom
        
        # Update alpha/beta and slopes
        if abs(u_new - v_left) < np.finfo(float).eps:
            slope_num -= L[alpha]
            alpha -= 1
        
        if abs(v_new - h_top) < np.finfo(float).eps:
            slope_denom -= L[beta]
            beta += 1
        
        # Update path
        new_kmax = v_new / u_new
        u.append(u_new)
        v.append(v_new)
        kmax.append(new_kmax)
        
        u_cur = u_new
        v_cur = v_new
    
    # Add vertical line segment
    kmax.append(float('inf'))
    u.append(u[-1])
    v.append(float('inf'))
    
    return {'k': np.array(kmax), 'u': np.array(u), 'v': np.array(v)}

def path_backward(L):
    """
    Compute optimal u using the backward algorithm.
    
    Parameters
    ----------
    L : array-like
        Vector of eigenvalues
        
    Returns
    -------
    dict
        Dictionary containing path information
    """
    p = len(L)
    
    # Handle zero eigenvalues
    idxzero = L < np.finfo(float).eps
    numzero = np.sum(idxzero)
    L = L.copy()  # Create a copy to avoid modifying the input
    L[idxzero] = np.finfo(float).eps
    
    r = p - numzero  # rank
    
    # Finding ending point algorithm
    alpha = 0
    slope_num = np.sum(L[:alpha+1])
    u_cur = (alpha+1+p-r) / slope_num
    
    while u_cur < 1/L[alpha] or (alpha < p-1 and u_cur > 1/L[alpha+1]):
        alpha += 1
        slope_num += L[alpha]
        u_cur = (alpha+1+p-r) / slope_num
    
    v_cur = 1/L[r-1]
    
    beta = r-1
    slope_denom = L[beta]
    
    # Vertical half-infinite line segment
    u = [u_cur, u_cur]
    v = [v_cur, float('inf')]
    kmax = [v_cur/u_cur, float('inf')]
    
    isDone = False
    while not isDone:
        # Rectangle boundaries
        h_bottom = 1/L[beta-1] if beta > 0 else float('inf')
        v_right = 1/L[alpha+1] if alpha < p-1 else 0
        
        # Check intersection with the diagonal line v=u
        u_new = (slope_num*u_cur + slope_denom*v_cur) / (slope_num + slope_denom)
        v_new = u_new
        
        if u_new < v_right and v_new > h_bottom:
            isDone = True
            u = [u_new] + u
            v = [v_new] + v
            kmax = [1] + kmax
            break
        
        # Intersection with horizontal line v=1/L[beta-1]
        v_new = h_bottom
        u_new = u_cur - slope_denom * (v_new - v_cur) / slope_num
        
        # If outside rectangle, compute intersection with vertical line
        if u_new > v_right:
            u_new = v_right
            v_new = v_cur - slope_num * (u_new - u_cur) / slope_denom
        
        # Update alpha/beta and slopes
        if abs(u_new - v_right) < np.finfo(float).eps:
            alpha += 1
            slope_num += L[alpha]
        
        if abs(v_new - h_bottom) < np.finfo(float).eps:
            beta -= 1
            slope_denom += L[beta]
        
        new_kmax = v_new / u_new
        
        u = [u_new] + u
        v = [v_new] + v
        kmax = [new_kmax] + kmax
        
        u_cur = u_new
        v_cur = v_new
    
    return {'k': np.array(kmax), 'u': np.array(u), 'v': np.array(v)}
