#' Generate Grid of Penalty Parameters
#'
#' Create a grid of penalty parameters for cross-validation.
#'
#' @param gridmax Maximum value in penalty grid
#' @param numpts Number of points in penalty grid
#' @return Vector of penalties between 1 and approximately gridmax
#' @export
#' @examples
#' # Generate 10 penalty values between 1 and 20
#' penalties <- kgrid(20, 10)
kgrid <- function(gridmax, numpts) {
  return(kgrid_cpp(gridmax, numpts))
}

#' Condition Number Regularized Covariance Estimation
#'
#' Compute a condition-number-regularized covariance matrix.
#'
#' @param data_in Input data matrix (n observations x p variables)
#' @param kmax Condition number bound
#' @return List with components:
#'   \item{S}{Regularized covariance matrix}
#'   \item{invS}{Inverse of regularized covariance matrix}
#' @export
#' @examples
#' \dontrun{
#' # Generate random data
#' X <- matrix(rnorm(500), 100, 5)
#' 
#' # Regularize with condition number bound of 10
#' result <- condreg(X, 10)
#' 
#' # Examine resulting matrices
#' cov_matrix <- result$S
#' precision_matrix <- result$invS
#' }
condreg <- function(data_in, kmax) {
  # Validate inputs
  if (!is.matrix(data_in))
    data_in <- as.matrix(data_in)
  
  if (!is.numeric(kmax) || length(kmax) != 1 || kmax <= 0)
    stop("kmax must be a positive scalar")
  
  # Call C++ function
  result <- condreg_cpp(data_in, kmax)
  return(result)
}

#' Select Penalty Parameter via Cross-validation
#'
#' Selection of penalty parameter based on cross-validation.
#'
#' @param X n-by-p data matrix
#' @param k Vector of penalties for cross-validation
#' @param fold Number of folds for cross-validation
#' @return List with components:
#'   \item{kmax}{Selected penalty parameter}
#'   \item{negL}{Negative log-likelihood values for each penalty}
#' @export
#' @examples
#' \dontrun{
#' # Generate random data
#' X <- matrix(rnorm(500), 100, 5)
#' 
#' # Create penalty grid
#' k_grid <- kgrid(50, 20)
#' 
#' # Find optimal penalty
#' result <- select_kmax(X, k_grid)
#' optimal_k <- result$kmax
#' }
select_kmax <- function(X, k, fold = NULL) {
  # Validate inputs
  if (!is.matrix(X))
    X <- as.matrix(X)
  
  if (!is.numeric(k))
    stop("k must be a numeric vector")
  
  # Set default for fold
  if (is.null(fold))
    fold <- min(nrow(X), 10)
  
  # Call C++ function
  result <- select_kmax_cpp(X, k, fold)
  return(result)
}

#' Compute Condition Number Regularized Covariance with Cross-validation
#'
#' Compute the best condition number regularized covariance matrix
#' based on cross-validation selected penalty parameter.
#'
#' @param X n-by-p data matrix
#' @param k Vector of penalties for cross-validation
#' @param ... additional parameters passed to select_kmax
#' @return List with components:
#'   \item{S}{Regularized covariance matrix}
#'   \item{invS}{Inverse of regularized covariance matrix}
#'   \item{kmax}{Selected penalty parameter}
#' @export
#' @examples
#' \dontrun{
#' # Generate random data
#' X <- matrix(rnorm(500), 100, 5)
#' 
#' # Create penalty grid
#' k_grid <- kgrid(50, 20)
#' 
#' # Estimate covariance with cross-validation
#' result <- select_condreg(X, k_grid)
#' 
#' # Extract results
#' cov_matrix <- result$S
#' precision_matrix <- result$invS
#' optimal_k <- result$kmax
#' }
select_condreg <- function(X, k, ...) {
  # Process additional arguments
  args <- list(...)
  fold <- args$fold
  
  # Set default for fold
  if (is.null(fold))
    fold <- min(nrow(X), 10)
  
  # Validate inputs
  if (!is.matrix(X))
    X <- as.matrix(X)
  
  if (!is.numeric(k))
    stop("k must be a numeric vector")
  
  # Call C++ function
  result <- select_condreg_cpp(X, k, fold)
  return(result)
}

#' Compute Optimal Portfolio Weights
#'
#' @param sigma Covariance matrix
#' @return Vector of portfolio weights
#' @export
#' @examples
#' \dontrun{
#' # Generate a sample covariance matrix
#' sigma <- matrix(c(1.0, 0.3, 0.3, 1.0), 2, 2)
#' 
#' # Compute optimal weights
#' weights <- pfweights(sigma)
#' }
pfweights <- function(sigma) {
  # Validate input
  if (!is.matrix(sigma))
    sigma <- as.matrix(sigma)
  
  if (nrow(sigma) != ncol(sigma))
    stop("sigma must be a square matrix")
  
  # Call C++ function
  return(pfweights_cpp(sigma))
}

#' Compute Transaction Cost of Rebalancing Portfolio
#'
#' @param wnew New portfolio weights
#' @param wold Old portfolio weights
#' @param lastearnings Earnings from last period
#' @param reltc Relative transaction cost
#' @param wealth Current wealth
#' @return Transaction cost
#' @export
#' @examples
#' \dontrun{
#' # Define portfolio weights
#' old_weights <- c(0.3, 0.3, 0.4)
#' new_weights <- c(0.4, 0.3, 0.3)
#' 
#' # Calculate transaction cost
#' cost <- transcost(new_weights, old_weights, 
#'                   lastearnings=1.02, reltc=0.005, wealth=10000)
#' }
transcost <- function(wnew, wold, lastearnings, reltc, wealth) {
  # Validate inputs
  if (!is.numeric(wnew) || !is.numeric(wold))
    stop("wnew and wold must be numeric vectors")
  
  if (length(wnew) != length(wold))
    stop("wnew and wold must have the same length")
  
  # Call C++ function
  return(transcost_cpp(wnew, wold, lastearnings, reltc, wealth))
} 