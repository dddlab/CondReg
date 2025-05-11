# CondrReg: Condition-Number-Regularized Covariance Estimation

[![PyPI version](https://badge.fury.io/py/condreg.svg)](https://badge.fury.io/py/condreg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for condition-number-regularized covariance estimation, based on Won et al. (2013).

## Installation

```bash
pip install condreg
```

## Features

- **High Performance**: Core algorithms implemented in C++ for speed
- **Condition Number Regularization**: Implementation of the algorithm from Won et al. (2013)
- **Solution Paths**: Computation of regularization paths for multiple penalty parameters
- **Portfolio Optimization**: Tools for portfolio weight calculation and transaction cost estimation
- **NumPy Integration**: Integration with NumPy arrays

## Quickstart

```python
import numpy as np
import condreg

# Generate synthetic data
n = 100  # samples
p = 20   # features
X = np.random.randn(n, p)

# Generate a grid of condition number bounds
k_grid = condreg.kgrid(gridmax=100.0, numpts=50)

# Estimate covariance with cross-validation
result = condreg.select_condreg(X, k_grid)

# Extract results
Sigma_hat = result['S']        # Regularized covariance matrix
Omega_hat = result['invS']     # Precision matrix estimate
k_optimal = result['kmax']     # Selected condition number bound

# Direct usage with a known condition number
direct_result = condreg.condreg(X, 10.0)
Sigma_direct = direct_result['S']
Omega_direct = direct_result['invS']

# Compute optimal portfolio weights
weights = condreg.pfweights(Sigma_hat)
```

## API Reference

### `condreg.kgrid(gridmax, numpts)`

Return a vector of grid of penalties for cross-validation.

* **Parameters**:
  * `gridmax` (float): Maximum value in penalty grid
  * `numpts` (int): Number of points in penalty grid
* **Returns**: Array of penalties between 1 and approximately gridmax with logarithmic spacing

### `condreg.select_condreg(X, k, **kwargs)`

Compute the best condition number regularized based on cross-validation selected penalty parameter.

* **Parameters**:
  * `X` (numpy.ndarray): n-by-p matrix of data
  * `k` (numpy.ndarray): Vector of penalties for cross-validation
  * `fold` (int, optional): Number of folds for cross-validation (default: min(n, 10))
* **Returns**: Dictionary with keys:
  * `S`: Condition number regularized covariance matrix
  * `invS`: Inverse of the regularized covariance matrix
  * `kmax`: Selected penalty parameter

### `condreg.condreg(data_in, kmax)`

Compute the condition number with given penalty parameter.

* **Parameters**:
  * `data_in` (numpy.ndarray): Input data matrix
  * `kmax` (float): Scalar regularization parameter
* **Returns**: Dictionary with keys:
  * `S`: Condition number regularized covariance matrix
  * `invS`: Inverse of the regularized covariance matrix

### `condreg.pfweights(sigma)`

Compute optimal portfolio weights.

* **Parameters**:
  * `sigma` (numpy.ndarray): Covariance matrix
* **Returns**: Array of portfolio weights

### `condreg.transcost(wnew, wold, lastearnings, reltc, wealth)`

Compute transaction cost.

* **Parameters**:
  * `wnew` (numpy.ndarray): New portfolio weights
  * `wold` (numpy.ndarray): Old portfolio weights
  * `lastearnings` (float): Earnings from last period
  * `reltc` (float): Relative transaction cost
  * `wealth` (float): Current wealth
* **Returns**: Transaction cost of rebalancing portfolio

### `condreg.select_kmax(X, k, fold=None)`

Selection of penalty parameter based on cross-validation.

* **Parameters**:
  * `X` (numpy.ndarray): n-by-p data matrix
  * `k` (numpy.ndarray): Vector of penalties for cross-validation
  * `fold` (int, optional): Number of folds for cross-validation (default: min(n, 10))
* **Returns**: Dictionary with keys:
  * `kmax`: Selected penalty parameter
  * `negL`: Negative log-likelihood values

### `condreg.init_condreg()`

Initialize the CondrReg model. This function returns an instance of the CondrReg class, which provides all the functionality directly. Most users should use the top-level functions instead.

* **Returns**: CondrReg model instance with methods matching the top-level functions

## Citation

```
@article{won2013condition,
  title={Condition-number-regularized covariance estimation},
  author={Won, Joong-Ho and Lim, Johan and Kim, Seung-Jean and Rajaratnam, Bala},
  journal={Journal of the Royal Statistical Society: Series B (Statistical Methodology)},
  volume={75},
  number={3},
  pages={427--450},
  year={2013},
  publisher={Wiley Online Library},
  doi={10.1111/j.1467-9868.2012.01049.x}
}
```

## References

* Won, J. H., Lim, J., Kim, S. J., & Rajaratnam, B. (2013). *Condition-number-regularized covariance estimation*. Journal of the Royal Statistical Society: Series B (Statistical Methodology), 75(3), 427–450.
* [Original R implementation on GitHub](https://github.com/dddlab/CondReg/tree/archive_main)

## License

MIT License. See [LICENSE](LICENSE) for details.
