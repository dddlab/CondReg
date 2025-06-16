#include "condreg/utils.hpp"

namespace condreg {

Eigen::VectorXd kgrid(double gridmax, int numpts) {
    // Create a vector of linearly spaced points from 1 to gridmax
    Eigen::VectorXd x = Eigen::VectorXd::LinSpaced(numpts, 1.0, gridmax);
    
    // Calculate y = 1/x
    Eigen::VectorXd y = x.array().inverse();
    
    // Normalize: y = y - min(y)
    double min_y = y.minCoeff();
    y = y.array() - min_y;
    
    // Scale: y = y / max(y)
    double max_y = y.maxCoeff();
    y = y.array() / max_y;
    
    // Final transformation: y = (y * (gridmax-1)) + 1
    y = (y.array() * (gridmax - 1.0)) + 1.0;
    
    return y;
}

Eigen::VectorXd pfweights(const Eigen::MatrixXd& sigma) {
    // Get the number of columns (variables)
    int p = sigma.cols();
    
    // Create a vector of ones
    Eigen::VectorXd ones = Eigen::VectorXd::Ones(p);
    
    // Solve: w = sigma^(-1) * ones
    Eigen::VectorXd w = sigma.ldlt().solve(ones);
    
    // Normalize: w = w / sum(w)
    double sum_w = w.sum();
    
    // If sum is very close to zero, return equal weights to avoid division by zero
    if (std::abs(sum_w) < 1e-10) {
        return Eigen::VectorXd::Constant(p, 1.0 / p);
    }
    
    return w / sum_w;
}

double transcost(const Eigen::VectorXd& wnew, const Eigen::VectorXd& wold, 
                double lastearnings, double reltc, double wealth) {
    
    // Calculate adjusted old weights: wold = lastearnings * wold
    Eigen::VectorXd wold_adjusted = lastearnings * wold;
    
    // Normalize if sum is not zero: wold = wold / sum(wold)
    double sum_wold = wold_adjusted.sum();
    if (std::abs(sum_wold) > 1e-10) {
        wold_adjusted /= sum_wold;
    }
    
    // Calculate transaction cost: wealth * reltc * sum(abs(wnew - wold))
    double abs_diff_sum = (wnew - wold_adjusted).array().abs().sum();
    
    return wealth * reltc * abs_diff_sum;
}

} // namespace condreg
