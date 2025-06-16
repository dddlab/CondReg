#' Simulation Data for Portfolio Optimization
#'
#' A dataset containing simulated financial returns for testing
#' condition number regularized covariance estimation methods.
#'
#' @format A matrix R with dimensions representing:
#' \describe{
#'   \item{rows}{Time periods (observations)}
#'   \item{columns}{Assets (variables)}
#' }
#' @source Simulated data for demonstrating the condregR package
#' @name simulationdata
#' @docType data
#' @keywords datasets
#' @examples
#' \dontrun{
#' data(simulationdata)
#' # R contains the return matrix
#' dim(R)
#' head(R)
#' }
NULL 