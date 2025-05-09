#include <iostream>
#include <iomanip>
#include "condreg/path_solvers.hpp"

int main() {
    // Create a test eigenvalue vector
    const int p = 10;
    Eigen::VectorXd L(p);
    
    // Fill with descending eigenvalues
    for (int i = 0; i < p; i++) {
        L(i) = 100.0 / (i + 1);  // Creates eigenvalues 100, 50, 33.3, 25, ...
    }
    
    std::cout << "Eigenvalues: " << std::endl << L.transpose() << std::endl << std::endl;
    
    // Test path_forward
    std::cout << "Testing path_forward:" << std::endl;
    condreg::PathResult fwd_result = condreg::path_forward(L);
    
    std::cout << "k values: " << std::endl;
    for (int i = 0; i < fwd_result.k.size(); i++) {
        if (std::isinf(fwd_result.k(i))) {
            std::cout << "inf ";
        } else {
            std::cout << std::fixed << std::setprecision(4) << fwd_result.k(i) << " ";
        }
    }
    std::cout << std::endl;
    
    std::cout << "u values: " << std::endl;
    for (int i = 0; i < fwd_result.u.size(); i++) {
        std::cout << std::fixed << std::setprecision(6) << fwd_result.u(i) << " ";
    }
    std::cout << std::endl;
    
    // Test path_backward
    std::cout << "\nTesting path_backward:" << std::endl;
    condreg::PathResult bwd_result = condreg::path_backward(L);
    
    std::cout << "k values: " << std::endl;
    for (int i = 0; i < bwd_result.k.size(); i++) {
        if (std::isinf(bwd_result.k(i))) {
            std::cout << "inf ";
        } else {
            std::cout << std::fixed << std::setprecision(4) << bwd_result.k(i) << " ";
        }
    }
    std::cout << std::endl;
    
    std::cout << "u values: " << std::endl;
    for (int i = 0; i < bwd_result.u.size(); i++) {
        std::cout << std::fixed << std::setprecision(6) << bwd_result.u(i) << " ";
    }
    std::cout << std::endl;
    
    // Verify that both methods produce similar results
    std::cout << "\nVerifying that both methods produce similar results:" << std::endl;
    
    // Check a few condition numbers like 2, a 4, 10
    double test_k[] = {2.0, 4.0, 10.0};
    
    for (double k : test_k) {
        // Find closest k values in both paths
        int fwd_idx = 0;
        int bwd_idx = 0;
        
        for (int i = 0; i < fwd_result.k.size(); i++) {
            if (!std::isinf(fwd_result.k(i)) && fwd_result.k(i) >= k) {
                fwd_idx = i;
                break;
            }
        }
        
        for (int i = 0; i < bwd_result.k.size(); i++) {
            if (!std::isinf(bwd_result.k(i)) && bwd_result.k(i) >= k) {
                bwd_idx = i;
                break;
            }
        }
        
        std::cout << "k = " << k << ":" << std::endl;
        std::cout << "Forward: u = " << fwd_result.u(fwd_idx) 
                  << ", k = " << fwd_result.k(fwd_idx) << std::endl;
        std::cout << "Backward: u = " << bwd_result.u(bwd_idx) 
                  << ", k = " << bwd_result.k(bwd_idx) << std::endl;
        std::cout << std::endl;
    }
    
    return 0;
}
