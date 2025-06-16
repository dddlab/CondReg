#pragma once

#include <Eigen/Dense>
#include <Eigen/SVD>
#include <Eigen/Eigenvalues>
#include <string>
#include <vector>
#include <memory>
#include "condreg/path_solvers.hpp"
#include "condreg/utils.hpp"

namespace condreg {

/**
 * @brief Result structure for the ml_solver function
 */
struct MLSolverResult {
    Eigen::MatrixXd Lbar;  // Shrunken eigenvalues
    Eigen::VectorXd uopt;  // Optimal u value
    Eigen::VectorXi intv;  // Interval indicator
};

/**
 * @brief Result structure for the condreg function
 */
struct CondregResult {
    Eigen::MatrixXd S;     // Regularized covariance matrix
    Eigen::MatrixXd invS;  // Inverse of regularized covariance matrix
};

/**
 * @brief Structure for spectral decomposition components
 */
struct SpectralDecomposition {
    Eigen::MatrixXd Q;   // Eigenvectors (orthogonal matrix)
    Eigen::VectorXd L;   // Eigenvalues
};

/**
 * @brief Result of bulk computation for different penalty parameters
 */
struct CRBulkResult {
    Eigen::MatrixXd Q;     // Orthogonal matrix (eigenvectors)
    Eigen::MatrixXd Lbar;  // Shrunken eigenvalues
    Eigen::VectorXd L;     // Original eigenvalues
};

/**
 * @brief Result of cross-validation for penalty selection
 */
struct SelectKmaxResult {
    double kmax;          // Selected penalty parameter
    Eigen::VectorXd negL; // Negative log-likelihood values
};

/**
 * @brief Compute shrinkage of eigenvalues for condreg
 * 
 * @param L Vector of eigenvalues
 * @param k Vector of penalties
 * @param direction Direction of path solver ('forward' or 'backward')
 * @return MLSolverResult Shrinkage result
 */
MLSolverResult ml_solver(const Eigen::VectorXd& L, const Eigen::VectorXd& k, 
                        const std::string& direction = "forward");

/**
 * @brief Compute multiple solutions for different penalty parameters
 * 
 * @param S Sample covariance matrix
 * @param k Vector of regularization parameters
 * @return CRBulkResult Bulk computation result
 */
CRBulkResult crbulk(const Eigen::MatrixXd& S, const Eigen::VectorXd& k);

/**
 * @brief Compute the condition number regularized covariance matrix
 * 
 * @param data_in Input data matrix or spectral decomposition
 * @param kmax Regularization parameter
 * @return CondregResult Regularized covariance matrix and its inverse
 */
CondregResult condreg(const Eigen::MatrixXd& data_in, double kmax);

/**
 * @brief Overloaded condreg function that takes a spectral decomposition
 * 
 * @param decomp Spectral decomposition (eigenvectors and eigenvalues)
 * @param kmax Regularization parameter
 * @return CondregResult Regularized covariance matrix and its inverse
 */
CondregResult condreg(const SpectralDecomposition& decomp, double kmax);

/**
 * @brief Selection of penalty parameter based on cross-validation
 * 
 * @param X n-by-p data matrix
 * @param k Vector of penalties for cross-validation
 * @param folds Number of folds for cross-validation
 * @return SelectKmaxResult Selected penalty and negative log-likelihood values
 */
SelectKmaxResult select_kmax(const Eigen::MatrixXd& X, const Eigen::VectorXd& k, int folds = 0);

/**
 * @brief Compute the best condition number regularized based on cross-validation
 * 
 * @param X n-by-p data matrix
 * @param k Vector of penalties for cross-validation
 * @param folds Number of folds for cross-validation
 * @return CondregResult Regularized covariance matrix and its inverse
 */
CondregResult select_condreg(const Eigen::MatrixXd& X, const Eigen::VectorXd& k, int folds = 0);

} // namespace condreg
