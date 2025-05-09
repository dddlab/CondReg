#include <iostream>
#include <iomanip>
#include <random>
#include "condreg/condreg.hpp"
#include "condreg/utils.hpp"

// Helper function to generate a random positive definite matrix
Eigen::MatrixXd generateRandomCovarianceMatrix(int p, double condition_number) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<> d(0, 1);
    
    // Create random eigenvalues with desired condition number
    Eigen::VectorXd eigenvalues(p);
    double min_eig = 1.0;
    double max_eig = condition_number * min_eig;
    
    // Create logarithmically spaced eigenvalues
    for (int i = 0; i < p; i++) {
        double t = static_cast<double>(i) / (p - 1);
        eigenvalues(i) = min_eig * std::pow(max_eig / min_eig, 1.0 - t);
    }
    
    // Create random orthogonal matrix
    Eigen::MatrixXd A(p, p);
    for (int i = 0; i < p; i++) {
        for (int j = 0; j < p; j++) {
            A(i, j) = d(gen);
        }
    }
    
    // QR decomposition to get orthogonal matrix
    Eigen::HouseholderQR<Eigen::MatrixXd> qr(A);
    Eigen::MatrixXd Q = qr.householderQ();
    
    // Create covariance matrix
    return Q * eigenvalues.asDiagonal() * Q.transpose();
}

// Helper function to generate data from a multivariate normal
Eigen::MatrixXd generateMVN(int n, const Eigen::MatrixXd& sigma) {
    int p = sigma.cols();
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<> d(0, 1);
    
    // Generate random standard normal samples
    Eigen::MatrixXd Z(n, p);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < p; j++) {
            Z(i, j) = d(gen);
        }
    }
    
    // Compute Cholesky decomposition
    Eigen::LLT<Eigen::MatrixXd> llt(sigma);
    Eigen::MatrixXd L = llt.matrixL();
    
    // Transform Z to have the desired covariance
    return Z * L.transpose();
}

int main() {
    // Set random seed for reproducibility
    std::srand(42);
    
    std::cout << "Testing condreg implementation..." << std::endl;
    
    // Test parameters
    int n = 100;  // Number of observations
    int p = 10;   // Number of variables
    double condition_number = 100.0;  // Condition number of true covariance
    
    // Generate true covariance matrix
    Eigen::MatrixXd true_cov = generateRandomCovarianceMatrix(p, condition_number);
    
    // Generate data
    Eigen::MatrixXd X = generateMVN(n, true_cov);
    
    // Compute sample covariance
    Eigen::MatrixXd centered = X.rowwise() - X.colwise().mean();
    Eigen::MatrixXd sample_cov = (centered.transpose() * centered) / (n - 1);
    
    // Get eigenvalues of true and sample covariance
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> eig_true(true_cov);
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> eig_sample(sample_cov);
    
    // Sort eigenvalues in descending order
    Eigen::VectorXd true_eigs(p);
    Eigen::VectorXd sample_eigs(p);
    
    for (int i = 0; i < p; i++) {
        true_eigs(i) = eig_true.eigenvalues()(p - 1 - i);
        sample_eigs(i) = eig_sample.eigenvalues()(p - 1 - i);
    }
    
    // Compute condition numbers
    double true_cond = true_eigs(0) / true_eigs(p - 1);
    double sample_cond = sample_eigs(0) / sample_eigs(p - 1);
    
    std::cout << "True condition number: " << true_cond << std::endl;
    std::cout << "Sample condition number: " << sample_cond << std::endl;
    
    // Test different regularization parameters
    std::vector<double> k_values = {1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0};
    
    std::cout << "\nTesting condreg with different regularization parameters:" << std::endl;
    std::cout << std::setw(10) << "kmax" << std::setw(20) << "Condition Number" << std::endl;
    
    for (double k : k_values) {
        // Apply condreg
        condreg::CondregResult result = condreg::condreg(sample_cov, k);
        
        // Compute eigenvalues of regularized covariance
        Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> eig_reg(result.S);
        
        // Sort eigenvalues in descending order
        Eigen::VectorXd reg_eigs(p);
        for (int i = 0; i < p; i++) {
            reg_eigs(i) = eig_reg.eigenvalues()(p - 1 - i);
        }
        
        // Compute condition number
        double reg_cond = reg_eigs(0) / reg_eigs(p - 1);
        
        std::cout << std::setw(10) << k << std::setw(20) << reg_cond << std::endl;
    }
    
    // Test cross-validation
    std::cout << "\nTesting cross-validation:" << std::endl;
    
    // Create grid of penalties
    Eigen::VectorXd penalties = condreg::kgrid(50.0, 10);
    
    // Perform cross-validation
    condreg::SelectKmaxResult cv_result = condreg::select_kmax(X, penalties, 5);
    
    std::cout << "Selected kmax: " << cv_result.kmax << std::endl;
    
    // Test select_condreg
    std::cout << "\nTesting select_condreg:" << std::endl;
    
    condreg::CondregResult cv_condreg = condreg::select_condreg(X, penalties, 5);
    
    // Compute eigenvalues of regularized covariance
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> eig_cv(cv_condreg.S);
    
    // Sort eigenvalues in descending order
    Eigen::VectorXd cv_eigs(p);
    for (int i = 0; i < p; i++) {
        cv_eigs(i) = eig_cv.eigenvalues()(p - 1 - i);
    }
    
    // Compute condition number
    double cv_cond = cv_eigs(0) / cv_eigs(p - 1);
    
    std::cout << "Condition number of CV-selected regularization: " << cv_cond << std::endl;
    
    return 0;
}
