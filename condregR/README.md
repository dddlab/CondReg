# condregR: Condition Number Regularized Covariance Estimation

[![R-CMD-check](https://github.com/dddlab/CondReg/workflows/R-CMD-check/badge.svg)](https://github.com/dddlab/CondReg/actions)

## Overview

The `condregR` package implements condition-number-regularized covariance estimation based on Won et al. (2013). This method regularizes covariance matrices by constraining their condition number, which improves statistical efficiency and numerical stability, particularly in high-dimensional settings.

## Key Features

- **Condition Number Regularization**: Constrains the condition number of covariance matrices to improve numerical stability
- **Cross-Validation**: Automatic penalty parameter selection via cross-validation
- **Portfolio Optimization**: Tools for computing optimal portfolio weights and transaction costs
- **High Performance**: C++ backend with Eigen linear algebra library for efficient computation
- **CRAN Ready**: Follows all CRAN submission standards with comprehensive documentation and tests

## Installation

```r
# Install from CRAN (when available)
install.packages("condregR")

# Or install development version from GitHub
# devtools::install_github("dddlab/CondReg", subdir = "condregR")
```

## Quick Start

```r
library(condregR)

# Generate example data
set.seed(123)
X <- matrix(rnorm(100*5), 100, 5)

# Basic usage: regularize with condition number bound of 10
result <- condreg(X, kmax = 10)
cov_matrix <- result$S
precision_matrix <- result$invS

# Automatic penalty selection via cross-validation
k_grid <- kgrid(gridmax = 20, numpts = 30)
cv_result <- select_condreg(X, k_grid)

# Portfolio optimization
weights <- pfweights(cv_result$S)
```

## Main Functions

### Core Functions

- `condreg(data_in, kmax)`: Compute condition-number-regularized covariance matrix
- `select_condreg(X, k)`: Automatic penalty selection via cross-validation
- `select_kmax(X, k)`: Cross-validation for penalty parameter selection
- `kgrid(gridmax, numpts)`: Generate penalty parameter grid

### Portfolio Functions

- `pfweights(sigma)`: Compute optimal portfolio weights
- `transcost(wnew, wold, lastearnings, reltc, wealth)`: Calculate transaction costs

## Example: Portfolio Optimization

```r
library(condregR)

# Load simulation data
data(simulationdata)

# Set up parameters
M <- 45  # estimation horizon
X_train <- R[1:M, ]  # training data

# Generate penalty grid and select optimal regularization
k_grid <- kgrid(20, 30)
result <- select_condreg(X_train, k_grid)

cat("Selected penalty parameter:", result$kmax, "\n")

# Compare condition numbers
sample_cov <- cov(X_train)
eig_sample <- eigen(sample_cov, only.values = TRUE)$values
eig_condreg <- eigen(result$S, only.values = TRUE)$values

cat("Sample covariance condition number:", max(eig_sample)/min(eig_sample), "\n")
cat("Regularized condition number:", max(eig_condreg)/min(eig_condreg), "\n")

# Compute optimal portfolio weights
weights <- pfweights(result$S)
cat("Portfolio weights sum to:", sum(weights), "\n")
```

## Method Details

The condition number regularization method works by:

1. Computing the eigendecomposition of the sample covariance matrix
2. Shrinking eigenvalues to ensure the condition number doesn't exceed the specified bound
3. Reconstructing the regularized covariance matrix

The method is particularly effective when:
- The sample size is small relative to the number of variables
- The sample covariance matrix is ill-conditioned
- Numerical stability is important for downstream applications

## References

Won, J.-H., Lim, J., Kim, S.-J., and Rajaratnam, B. (2013). Condition-number-regularized covariance estimation. *Journal of the Royal Statistical Society: Series B*, 75(3), 427-450. [doi:10.1111/j.1467-9868.2012.01049.x](https://doi.org/10.1111/j.1467-9868.2012.01049.x)

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Authors

- Sang Yun Oh (syoh@ucsb.edu)
- Lixing Guo (lixing_guo@ucsb.edu) 