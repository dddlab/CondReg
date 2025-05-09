#include "condreg/condreg.hpp"
#include <limits>
#include <algorithm>
#include <random>
#include <cmath>

namespace condreg {

MLSolverResult ml_solver(const Eigen::VectorXd& L, const Eigen::VectorXd& k, 
                        const std::string& direction) {
    int p = L.size();
    int k_size = k.size();
    
    // Initialize result
    MLSolverResult result;
    result.Lbar = Eigen::MatrixXd::Zero(k_size, p);
    result.uopt = Eigen::VectorXd::Zero(k_size);
    result.intv = Eigen::VectorXi::Zero(k_size);
    
    // Handle small eigenvalues
    double eps = std::numeric_limits<double>::epsilon();
    Eigen::VectorXd L_copy = L;
    for (int i = 0; i < p; i++) {
        if (L_copy(i) < eps) {
            L_copy(i) = eps;
        }
    }
    
    // Handle degenerate cases: k > (L[0] / L[p-1])
    double ratio = L_copy(0) / L_copy(p-1);
    for (int i = 0; i < k_size; i++) {
        if (k(i) > ratio) {
            // Degenerate case
            for (int j = 0; j < p; j++) {
                result.Lbar(i, j) = L_copy(j);
            }
            result.uopt(i) = std::max(1.0 / (k(i) * L_copy(p-1)), 1.0 / L_copy(0));
            result.intv(i) = 1;
        }
    }
    
    // Handle non-degenerate cases
    bool has_nondegenerate = false;
    for (int i = 0; i < k_size; i++) {
        if (k(i) <= ratio) {
            has_nondegenerate = true;
            break;
        }
    }
    
    if (has_nondegenerate) {
        // Collect non-degenerate k values
        std::vector<double> kmax1;
        std::vector<int> non_degen_indices;
        
        for (int i = 0; i < k_size; i++) {
            if (k(i) <= ratio) {
                kmax1.push_back(k(i));
                non_degen_indices.push_back(i);
            }
        }
        
        // Choose path algorithm
        PathResult path;
        if (direction == "forward") {
            path = path_forward(L_copy);
        } else if (direction == "backward") {
            path = path_backward(L_copy);
        } else {
            throw std::invalid_argument("direction must be either 'forward' or 'backward'");
        }
        
        // Linear interpolation for each non-degenerate kmax value
        Eigen::VectorXd uopt_nondegenerate(kmax1.size());
        
        for (size_t i = 0; i < kmax1.size(); i++) {
            double kval = kmax1[i];
            
            // Find the two adjacent points in the path
            int idx = 0;
            while (idx < path.k.size() - 1 && path.k(idx) < kval) {
                idx++;
            }
            
            // Perform linear interpolation
            double k0, k1, u0, u1;
            if (idx == 0) {
                uopt_nondegenerate(i) = path.u(0);
            } else if (idx >= path.k.size() || std::isinf(path.k(idx))) {
                uopt_nondegenerate(i) = path.u(idx - 1);
            } else {
                k0 = path.k(idx - 1);
                k1 = path.k(idx);
                u0 = 1.0 / path.u(idx - 1);
                u1 = 1.0 / path.u(idx);
                
                double t = (kval - k0) / (k1 - k0);
                uopt_nondegenerate(i) = 1.0 / ((1 - t) * u0 + t * u1);
            }
        }
        
        // Compute shrunken eigenvalues
        for (size_t i = 0; i < kmax1.size(); i++) {
            int idx = non_degen_indices[i];
            double u_val = uopt_nondegenerate(i);
            
            for (int j = 0; j < p; j++) {
                // min(k*u, max(u, 1/L))
                double lambda = std::min(
                    kmax1[i] * u_val,
                    std::max(u_val, 1.0 / L_copy(j))
                );
                result.Lbar(idx, j) = 1.0 / lambda;
            }
            
            result.uopt(idx) = u_val;
            result.intv(idx) = 0;
        }
    }
    
    return result;
}

CRBulkResult crbulk(const Eigen::MatrixXd& S, const Eigen::VectorXd& k) {
    int n = S.rows();
    int p = S.cols();
    int k_size = k.size();
    
    // Compute eigendecomposition
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> eig(S);
    Eigen::MatrixXd Q = eig.eigenvectors();
    Eigen::VectorXd L = eig.eigenvalues();
    
    // Sort eigenvalues and eigenvectors in descending order
    // (SelfAdjointEigenSolver returns them in ascending order)
    Eigen::VectorXd L_sorted(p);
    Eigen::MatrixXd Q_sorted(p, p);
    
    for (int i = 0; i < p; i++) {
        L_sorted(i) = L(p - 1 - i);
        Q_sorted.col(i) = Q.col(p - 1 - i);
    }
    
    // Compute shrinkage
    MLSolverResult soln = ml_solver(L_sorted, k);
    
    // Prepare result
    CRBulkResult result;
    result.Q = Q_sorted;
    result.Lbar = soln.Lbar;
    result.L = L_sorted;
    
    return result;
}

CondregResult condreg(const Eigen::MatrixXd& data_in, double kmax) {
    // Check if input is a data matrix or covariance matrix
    if (data_in.rows() > data_in.cols()) {
        // Input is a data matrix
        int n = data_in.rows();
        
        // Compute sample covariance
        Eigen::MatrixXd centered = data_in.rowwise() - data_in.colwise().mean();
        Eigen::MatrixXd S = (centered.transpose() * centered) / (n - 1);
        
        // Compute eigendecomposition
        Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> eig(S);
        
        // Sort eigenvalues and eigenvectors in descending order
        int p = S.cols();
        Eigen::VectorXd L(p);
        Eigen::MatrixXd Q(p, p);
        
        for (int i = 0; i < p; i++) {
            L(i) = eig.eigenvalues()(p - 1 - i);
            Q.col(i) = eig.eigenvectors().col(p - 1 - i);
        }
        
        SpectralDecomposition decomp{Q, L};
        return condreg(decomp, kmax);
    } else {
        // Input is likely a covariance matrix
        Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> eig(data_in);
        
        // Sort eigenvalues and eigenvectors in descending order
        int p = data_in.cols();
        Eigen::VectorXd L(p);
        Eigen::MatrixXd Q(p, p);
        
        for (int i = 0; i < p; i++) {
            L(i) = eig.eigenvalues()(p - 1 - i);
            Q.col(i) = eig.eigenvectors().col(p - 1 - i);
        }
        
        SpectralDecomposition decomp{Q, L};
        return condreg(decomp, kmax);
    }
}

CondregResult condreg(const SpectralDecomposition& decomp, double kmax) {
    // Create vector of single kmax value
    Eigen::VectorXd k(1);
    k(0) = kmax;
    
    // Apply ml_solver
    MLSolverResult sol = ml_solver(decomp.L, k);
    Eigen::VectorXd Lbar = sol.Lbar.row(0);
    
    // Reconstruct matrices
    CondregResult result;
    result.S = decomp.Q * Lbar.asDiagonal() * decomp.Q.transpose();
    
    // Compute inverse
    Eigen::VectorXd invLbar = Lbar.array().inverse();
    result.invS = decomp.Q * invLbar.asDiagonal() * decomp.Q.transpose();
    
    return result;
}

SelectKmaxResult select_kmax(const Eigen::MatrixXd& X, const Eigen::VectorXd& k, int folds) {
    int n = X.rows();
    int p = X.cols();
    int k_size = k.size();
    
    // Set number of folds if not specified
    if (folds <= 0) {
        folds = std::min(n, 10);
    }
    
    // Prepare cross-validation
    Eigen::MatrixXd neg_loglikelihood = Eigen::MatrixXd::Zero(folds, k_size);
    double condmax = 1.0;
    
    // Create random indices for cross-validation
    std::vector<int> indices(n);
    for (int i = 0; i < n; i++) {
        indices[i] = i;
    }
    
    // Shuffle indices
    std::random_device rd;
    std::mt19937 rng(rd());
    std::shuffle(indices.begin(), indices.end(), rng);
    
    // Calculate fold sizes
    std::vector<int> fold_sizes(folds, n / folds);
    for (int i = 0; i < n % folds; i++) {
        fold_sizes[i]++;
    }
    
    // Create fold indices
    std::vector<std::vector<int>> fold_indices(folds);
    int start_idx = 0;
    for (int i = 0; i < folds; i++) {
        fold_indices[i].resize(fold_sizes[i]);
        for (int j = 0; j < fold_sizes[i]; j++) {
            fold_indices[i][j] = indices[start_idx + j];
        }
        start_idx += fold_sizes[i];
    }
    
    // Cross-validation loop
    for (int i = 0; i < folds; i++) {
        // Split data into training and test sets
        std::vector<int> test_indices = fold_indices[i];
        std::vector<int> train_indices;
        for (int j = 0; j < folds; j++) {
            if (j != i) {
                train_indices.insert(train_indices.end(), 
                                    fold_indices[j].begin(), 
                                    fold_indices[j].end());
            }
        }
        
        // Create training and test matrices
        int n_train = train_indices.size();
        int n_test = test_indices.size();
        
        Eigen::MatrixXd X_train(n_train, p);
        Eigen::MatrixXd X_test(n_test, p);
        
        for (int j = 0; j < n_train; j++) {
            X_train.row(j) = X.row(train_indices[j]);
        }
        
        for (int j = 0; j < n_test; j++) {
            X_test.row(j) = X.row(test_indices[j]);
        }
        
        // Compute sample covariance on training data
        Eigen::MatrixXd centered_train = X_train.rowwise() - X_train.colwise().mean();
        Eigen::MatrixXd S_train = (centered_train.transpose() * centered_train) / (n_train - 1);
        
        // Compute bulk solutions
        CRBulkResult soln = crbulk(S_train, k);
        
        // Transform test data
        Eigen::MatrixXd y_test = X_test * soln.Q;
        
        // Compute negative log-likelihood
        for (int j = 0; j < k_size; j++) {
            double nll = 0.0;
            
            // Log-determinant term
            for (int l = 0; l < p; l++) {
                nll += std::log(soln.Lbar(j, l));
            }
            
            // Quadratic form term
            for (int l = 0; l < n_test; l++) {
                for (int m = 0; m < p; m++) {
                    nll += (y_test(l, m) * y_test(l, m)) / soln.Lbar(j, m);
                }
            }
            
            neg_loglikelihood(i, j) = nll / n_test;
        }
        
        // Update condmax
        int min_dim = std::min(n_train, p);
        double largest_eig = soln.L(0);
        double smallest_eig = soln.L(min_dim - 1);
        condmax = std::max(condmax, largest_eig / smallest_eig);
    }
    
    // Sum negative log-likelihood across folds
    Eigen::VectorXd nL = neg_loglikelihood.colwise().sum();
    
    // Find minimum negative log-likelihood
    int min_idx = 0;
    double min_val = nL(0);
    for (int i = 1; i < k_size; i++) {
        if (nL(i) < min_val) {
            min_val = nL(i);
            min_idx = i;
        }
    }
    
    // Take minimum of k[min_idx] and condmax
    double kmaxopt = std::min(k(min_idx), condmax);
    
    // Return result
    SelectKmaxResult result;
    result.kmax = kmaxopt;
    result.negL = nL;
    
    return result;
}

CondregResult select_condreg(const Eigen::MatrixXd& X, const Eigen::VectorXd& k, int folds) {
    int n = X.rows();
    int p = X.cols();
    
    // Select optimal kmax via cross-validation
    SelectKmaxResult kmax_result = select_kmax(X, k, folds);
    
    // Compute sample covariance
    Eigen::MatrixXd centered = X.rowwise() - X.colwise().mean();
    Eigen::MatrixXd S = (centered.transpose() * centered) / (n - 1);
    
    // Compute eigendecomposition
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> eig(S);
    
    // Sort eigenvalues and eigenvectors in descending order
    Eigen::VectorXd L(p);
    Eigen::MatrixXd Q(p, p);
    
    for (int i = 0; i < p; i++) {
        L(i) = eig.eigenvalues()(p - 1 - i);
        Q.col(i) = eig.eigenvectors().col(p - 1 - i);
    }
    
    // Create spectral decomposition
    SpectralDecomposition QLQ{Q, L};
    
    // Apply condreg with selected kmax
    CondregResult soln = condreg(QLQ, kmax_result.kmax);
    
    return soln;
}

} // namespace condreg
