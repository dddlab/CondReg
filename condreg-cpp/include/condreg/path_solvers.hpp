#pragma once

#include <Eigen/Dense>
#include <vector>
#include <limits>
#include <cmath>
#include <algorithm>

namespace condreg {

/**
 * @brief Result structure for path algorithms
 * 
 * Contains the regularization path information with:
 * - k: Vector of regularization parameters (condition numbers)
 * - u: Vector of u values (related to minimum eigenvalues)
 * - v: Vector of v values (related to maximum eigenvalues)
 */
struct PathResult {
    Eigen::VectorXd k;  // Regularization parameters
    Eigen::VectorXd u;  // Lower bounds for eigenvalues
    Eigen::VectorXd v;  // Upper bounds for eigenvalues
};

/**
 * @brief Compute optimal u using the forward algorithm
 * 
 * This function implements the forward path-finding algorithm for
 * condition number regularization as described in the JRSSB paper.
 * 
 * @param L Vector of eigenvalues (in descending order)
 * @return PathResult containing the regularization path
 */
PathResult path_forward(const Eigen::VectorXd& L);

/**
 * @brief Compute optimal u using the backward algorithm
 * 
 * This function implements the backward path-finding algorithm for
 * condition number regularization as described in the JRSSB paper.
 * 
 * @param L Vector of eigenvalues (in descending order)
 * @return PathResult containing the regularization path
 */
PathResult path_backward(const Eigen::VectorXd& L);

} // namespace condreg
