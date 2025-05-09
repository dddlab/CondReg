# condreg-py

A Python implementation of condition number regularization for covariance matrices.

## Installation

```bash
pip install condreg
```

## Usage

```python
import numpy as np
from condreg import select_condreg, kgrid, pfweights

# Create a sample dataset
X = np.random.randn(100, 10)  # 100 observations, 10 variables

# Generate grid of penalties
gridpts = kgrid(50, 100)

# Estimate regularized covariance matrix
result = select_condreg(X, gridpts)

# Access results
sigma_hat = result['S']       # Regularized covariance matrix
omega_hat = result['invS']    # Inverse of regularized covariance matrix
kmax = result['kmax']         # Selected regularization parameter

# Compute optimal portfolio weights
weights = pfweights(sigma_hat)
```

## Features

- Condition number regularization of covariance matrices
- Automatic selection of regularization parameter via cross-validation
- Efficient path algorithms for computing regularization paths
- Utilities for portfolio optimization

## References

- [Original R implementation](https://github.com/yourlinkhere)
- [Paper reference]
