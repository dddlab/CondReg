#include <iostream>
#include <iomanip>
#include "condreg/utils.hpp"

int main() {
    // Test kgrid
    std::cout << "Testing kgrid function:" << std::endl;
    Eigen::VectorXd grid = condreg::kgrid(20.0, 10);
    std::cout << "kgrid(20.0, 10) = " << std::endl << grid.transpose() << std::endl << std::endl;
    
    // Test pfweights
    std::cout << "Testing pfweights function:" << std::endl;
    // Create a simple covariance matrix
    Eigen::MatrixXd sigma(3, 3);
    sigma << 1.0, 0.2, 0.3,
             0.2, 1.5, 0.4,
             0.3, 0.4, 2.0;
    
    Eigen::VectorXd weights = condreg::pfweights(sigma);
    std::cout << "Covariance matrix:" << std::endl << sigma << std::endl;
    std::cout << "Portfolio weights:" << std::endl << weights.transpose() << std::endl;
    std::cout << "Sum of weights: " << weights.sum() << std::endl << std::endl;
    
    // Test transcost
    std::cout << "Testing transcost function:" << std::endl;
    Eigen::VectorXd wnew(3);
    wnew << 0.5, 0.3, 0.2;
    
    Eigen::VectorXd wold(3);
    wold << 0.4, 0.4, 0.2;
    
    double lastearnings = 1.1;  // 10% return
    double reltc = 0.001;      // 0.1% transaction cost
    double wealth = 1000000.0; // $1,000,000 portfolio
    
    double cost = condreg::transcost(wnew, wold, lastearnings, reltc, wealth);
    std::cout << "New weights: " << wnew.transpose() << std::endl;
    std::cout << "Old weights: " << wold.transpose() << std::endl;
    std::cout << "Last earnings: " << lastearnings << std::endl;
    std::cout << "Relative transaction cost: " << reltc << std::endl;
    std::cout << "Wealth: " << wealth << std::endl;
    std::cout << "Transaction cost: $" << cost << std::endl;
    
    return 0;
}
