# CondrReg: Conditional Regression for Statistical Modeling

[![PyPI version](https://badge.fury.io/py/condreg.svg)](https://badge.fury.io/py/condreg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CondrReg is a high-performance library for conditional regression, implemented in C++ with Python bindings. It provides efficient algorithms for working with sparse covariance matrices and conditional linear regression models.

## Installation

```bash
pip install condreg
```

## Features

- **High Performance**: Core algorithms implemented in C++ for speed
- **Sparse Matrix Support**: Efficient handling of sparse matrices for high-dimensional data
- **Regularization Paths**: Computation of solution paths for a range of regularization parameters
- **NumPy Integration**: Seamless integration with NumPy arrays
- **Statistical Inference**: Tools for conditional statistical inference

## Quick Example

```python
import numpy as np
import condreg

# Generate synthetic data
n = 100  # samples
p = 20   # features
X = np.random.randn(n, p)
beta = np.zeros(p)
beta[0:5] = np.array([1.5, -1.0, 0.8, -0.5, 1.2])  # True coefficients
y = X @ beta + 0.5 * np.random.randn(n)  # Add noise

# Initialize CondrReg model
model = condreg.init_condreg()

# Fit the model
result = model.fit(X, y, lambda_val=0.1)

# Print coefficients
print("Estimated coefficients:")
print(result.coef)

# Compute a regularization path
path = model.path(X, y, lambda_sequence=np.logspace(-3, 0, 20))

# Access path results
for i, lambda_val in enumerate(path.lambdas):
    print(f"Lambda: {lambda_val:.4f}, Non-zero coefficients: {np.sum(path.coefs[i] != 0)}")
```

## Requirements

- Python 3.6+
- NumPy 1.18.0+

## Documentation

For detailed documentation and examples, please visit:
[https://github.com/dddlab/CondReg](https://github.com/dddlab/CondReg)

## Citation

If you use CondrReg in your research, please cite:

@article{oh2015solution,
title={On the Solution Path of Regularized Covariance Estimators},
author={Oh, Sang-Yun and Rajaratnam, Bala and Won, Joong-Ho},
year={2015},
doi={10.1080/10618600.2014.932811}
}

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Sang Yun Oh (syoh@ucsb.edu)
- Lixing Guo (lixing_guo@ucsb.edu)

## Acknowledgments

This research was supported by [funding source or acknowledgment here].