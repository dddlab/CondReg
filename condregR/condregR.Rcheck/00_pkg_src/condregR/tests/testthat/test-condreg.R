library(testthat)
library(condregR)

test_that("kgrid works correctly", {
  grid <- kgrid(50, 10)
  expect_equal(length(grid), 10)
  expect_true(all(diff(grid) < 0))  # Monotonically decreasing (correct for penalty grids)
  expect_true(grid[1] >= 1.0)       # First value should be >= 1
  expect_true(grid[length(grid)] >= 1.0)  # Last value should be >= 1
  expect_true(grid[1] <= 50 * 1.01)  # First value should be approximately gridmax
  
  # Test error conditions
  expect_error(kgrid(0.5, 10), "gridmax must be greater than 1")
  expect_error(kgrid(10, 0), "numpts must be positive")
})

test_that("condreg produces valid covariance matrices", {
  set.seed(123)
  X <- matrix(rnorm(100*5), 100, 5)
  result <- condreg(X, 10)
  
  # Check output structure
  expect_true(is.list(result))
  expect_true(all(c("S", "invS") %in% names(result)))
  
  # Check dimensions
  expect_equal(dim(result$S), c(5, 5))
  expect_equal(dim(result$invS), c(5, 5))
  
  # Check properties
  eigenvalues <- eigen(result$S, only.values=TRUE)$values
  expect_true(all(eigenvalues > 0))  # Positive definite
  condition_number <- max(eigenvalues)/min(eigenvalues)
  expect_lte(condition_number, 10 * 1.01)  # Allow small numerical error
  
  # Check that S and invS are inverses
  identity_approx <- result$S %*% result$invS
  expect_true(all(abs(identity_approx - diag(5)) < 1e-10))
  
  # Test error conditions
  expect_error(condreg(X, 0.5), "kmax must be greater than or equal to 1")
})

test_that("select_kmax works correctly", {
  set.seed(123)
  X <- matrix(rnorm(50*4), 50, 4)
  k_grid <- kgrid(20, 10)
  
  result <- select_kmax(X, k_grid)
  
  # Check output structure
  expect_true(is.list(result))
  expect_true(all(c("kmax", "negL") %in% names(result)))
  
  # Check types and dimensions
  expect_true(is.numeric(result$kmax))
  expect_equal(length(result$kmax), 1)
  expect_equal(length(result$negL), length(k_grid))
  
  # Check that selected kmax is in the grid or bounded by condition number
  expect_true(result$kmax >= 1.0)
  
  # Test error conditions
  expect_error(select_kmax(matrix(1, 1, 4), k_grid), "X must have at least 2 rows")
  expect_error(select_kmax(X, c(0.5, 2)), "All k values must be greater than or equal to 1")
})

test_that("select_condreg works correctly", {
  set.seed(123)
  X <- matrix(rnorm(50*4), 50, 4)
  k_grid <- kgrid(20, 10)
  
  result <- select_condreg(X, k_grid)
  
  # Check output structure
  expect_true(is.list(result))
  expect_true(all(c("S", "invS", "kmax") %in% names(result)))
  
  # Check dimensions
  expect_equal(dim(result$S), c(4, 4))
  expect_equal(dim(result$invS), c(4, 4))
  
  # Check properties
  eigenvalues <- eigen(result$S, only.values=TRUE)$values
  expect_true(all(eigenvalues > 0))  # Positive definite
  
  # Check that S and invS are inverses
  identity_approx <- result$S %*% result$invS
  expect_true(all(abs(identity_approx - diag(4)) < 1e-10))
})

test_that("pfweights works correctly", {
  # Test with a simple 2x2 covariance matrix
  sigma <- matrix(c(1.0, 0.3, 0.3, 1.0), 2, 2)
  weights <- pfweights(sigma)
  
  # Check output
  expect_true(is.numeric(weights))
  expect_equal(length(weights), 2)
  
  # Weights should sum to 1 (approximately)
  expect_true(abs(sum(weights) - 1.0) < 1e-10)
  
  # Test error conditions
  expect_error(pfweights(matrix(1:6, 2, 3)), "sigma must be a square matrix")
})

test_that("transcost works correctly", {
  old_weights <- c(0.3, 0.3, 0.4)
  new_weights <- c(0.4, 0.3, 0.3)
  
  cost <- transcost(new_weights, old_weights, 
                   lastearnings=1.02, reltc=0.005, wealth=10000)
  
  # Check output
  expect_true(is.numeric(cost))
  expect_equal(length(cost), 1)
  expect_true(cost >= 0)  # Transaction cost should be non-negative
  
  # Test error conditions
  expect_error(transcost(c(0.5, 0.5), c(0.3, 0.3, 0.4), 1.0, 0.01, 1000), 
               "wnew and wold must have the same length")
  expect_error(transcost(new_weights, old_weights, 1.0, -0.01, 1000), 
               "reltc must be non-negative")
  expect_error(transcost(new_weights, old_weights, 1.0, 0.01, -1000), 
               "wealth must be positive")
})

test_that("integration test with simulation data", {
  # Load simulation data
  data(simulationdata, envir = environment())
  
  # Check that R matrix exists and has reasonable dimensions
  expect_true(exists("R"))
  expect_true(is.matrix(R))
  expect_true(nrow(R) > ncol(R))  # More observations than variables
  
  # Test the full workflow
  n_train <- min(100, nrow(R))
  X_train <- R[1:n_train, ]
  
  # Generate penalty grid
  k_grid <- kgrid(20, 15)
  
  # Estimate covariance with cross-validation
  result <- select_condreg(X_train, k_grid)
  
  # Compute portfolio weights
  weights <- pfweights(result$S)
  
  # Check results
  expect_true(all(c("S", "invS", "kmax") %in% names(result)))
  expect_equal(length(weights), ncol(X_train))
  expect_true(abs(sum(weights) - 1.0) < 1e-10)
})