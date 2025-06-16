#pragma once

#include <Eigen/Dense>
#include <vector>
#include <cmath>

namespace condreg {

/**
 * @brief Generate a vector of grid of penalties for cross-validation
 * 
 * Returns a vector of penalties between 1 and approximately gridmax
 * with logarithmic spacing
 * 
 * @param gridmax Maximum value in the penalty grid
 * @param numpts Number of points in the penalty grid
 * @return Eigen::VectorXd Vector of penalties
 */
Eigen::VectorXd kgrid(double gridmax, int numpts);

/**
 * @brief Compute optimal portfolio weights
 * 
 * @param sigma Covariance matrix
 * @return Eigen::VectorXd New portfolio weights
 */
Eigen::VectorXd pfweights(const Eigen::MatrixXd& sigma);

/**
 * @brief Compute transaction cost of rebalancing portfolio
 * 
 * @param wnew New portfolio weights
 * @param wold Old portfolio weights
 * @param lastearnings Earnings from last period
 * @param reltc Relative transaction cost
 * @param wealth Current wealth
 * @return double Transaction cost
 */
double transcost(const Eigen::VectorXd& wnew, const Eigen::VectorXd& wold, 
                double lastearnings, double reltc, double wealth);

} // namespace condreg
