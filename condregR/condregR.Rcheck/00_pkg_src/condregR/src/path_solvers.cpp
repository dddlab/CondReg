#include "condreg/path_solvers.hpp"

namespace condreg {

PathResult path_forward(const Eigen::VectorXd& L) {
    // Get the size of eigenvalue vector
    int p = L.size();
    
    // Create a copy of L to avoid modifying the input
    Eigen::VectorXd L_copy = L;
    
    // Handle zero eigenvalues
    double eps = std::numeric_limits<double>::epsilon();
    Eigen::Array<bool, Eigen::Dynamic, 1> idxzero = (L_copy.array() < eps);
    int numzero = idxzero.count();
    
    // Replace small values with epsilon
    for (int i = 0; i < p; i++) {
        if (L_copy(i) < eps) {
            L_copy(i) = eps;
        }
    }
    
    // Initial point: 1/mean(L)
    double u_cur = 1.0 / L_copy.mean();
    double v_cur = u_cur;
    
    // Find starting alpha
    int alpha = 0;
    while (alpha < p - 1 && u_cur > 1.0 / L_copy(alpha)) {
        alpha++;
    }
    
    // Set beta and initialize slopes
    int beta = alpha + 1;
    double slope_num = 0.0;
    for (int i = 0; i < alpha; i++) {
        slope_num += L_copy(i);
    }
    
    double slope_denom = 0.0;
    for (int i = beta; i < p; i++) {
        slope_denom += L_copy(i);
    }
    
    // Initialize path vectors
    std::vector<double> u_vec = {u_cur};
    std::vector<double> v_vec = {v_cur};
    std::vector<double> kmax_vec = {1.0}; // Start with condition number 1
    
    int r = p - numzero;
    
    // Main path-finding loop
    while (alpha >= 0 && beta <= r - 1) {
        // Rectangle boundaries
        double h_top = 1.0 / L_copy(beta);
        double v_left = 1.0 / L_copy(alpha);
        
        // Compute intersection with horizontal line v=h_top
        double v_new = h_top;
        double u_new = u_cur - slope_denom * (v_new - v_cur) / slope_num;
        
        // If outside rectangle, compute intersection with vertical line u=v_left
        if (u_new < v_left) {
            u_new = v_left;
            v_new = v_cur - slope_num * (u_new - u_cur) / slope_denom;
        }
        
        // Update alpha/beta and slopes
        if (std::abs(u_new - v_left) < eps) {
            // Keep this order! First update slope, then index
            slope_num -= L_copy(alpha);
            alpha--;
        }
        
        if (std::abs(v_new - h_top) < eps) {
            // Keep this order! First update slope, then index
            slope_denom -= L_copy(beta);
            beta++;
        }
        
        // Calculate new condition number and update path
        double new_kmax = v_new / u_new;
        u_vec.push_back(u_new);
        v_vec.push_back(v_new);
        kmax_vec.push_back(new_kmax);
        
        // Update current point
        u_cur = u_new;
        v_cur = v_new;
    }
    
    // Add vertical line segment for infinity condition number
    double inf_val = std::numeric_limits<double>::infinity();
    kmax_vec.push_back(inf_val);
    u_vec.push_back(u_vec.back());
    v_vec.push_back(inf_val);
    
    // Convert vectors to Eigen vectors
    PathResult result;
    result.k = Eigen::Map<Eigen::VectorXd>(kmax_vec.data(), kmax_vec.size());
    result.u = Eigen::Map<Eigen::VectorXd>(u_vec.data(), u_vec.size());
    result.v = Eigen::Map<Eigen::VectorXd>(v_vec.data(), v_vec.size());
    
    return result;
}

PathResult path_backward(const Eigen::VectorXd& L) {
    // Get the size of eigenvalue vector
    int p = L.size();
    
    // Create a copy of L to avoid modifying the input
    Eigen::VectorXd L_copy = L;
    
    // Handle zero eigenvalues
    double eps = std::numeric_limits<double>::epsilon();
    Eigen::Array<bool, Eigen::Dynamic, 1> idxzero = (L_copy.array() < eps);
    int numzero = idxzero.count();
    
    // Replace small values with epsilon
    for (int i = 0; i < p; i++) {
        if (L_copy(i) < eps) {
            L_copy(i) = eps;
        }
    }
    
    int r = p - numzero;  // Rank of the matrix
    
    // Finding ending point algorithm
    int alpha = 0;
    double slope_num = L_copy(0);  // Initialize with first eigenvalue
    double u_cur = (alpha + 1 + p - r) / slope_num;
    
    // Find proper alpha
    while (u_cur < 1.0 / L_copy(alpha) || 
          (alpha < p - 1 && u_cur > 1.0 / L_copy(alpha + 1))) {
        alpha++;
        slope_num += L_copy(alpha);
        u_cur = (alpha + 1 + p - r) / slope_num;
    }
    
    double v_cur = 1.0 / L_copy(r - 1);
    
    int beta = r - 1;
    double slope_denom = L_copy(beta);
    
    // Initialize path with vertical half-infinite line segment
    std::vector<double> u_vec = {u_cur, u_cur};
    std::vector<double> v_vec = {v_cur, std::numeric_limits<double>::infinity()};
    std::vector<double> kmax_vec = {v_cur / u_cur, std::numeric_limits<double>::infinity()};
    
    bool isDone = false;
    while (!isDone) {
        // Rectangle boundaries
        double h_bottom = (beta > 0) ? 1.0 / L_copy(beta - 1) : std::numeric_limits<double>::infinity();
        double v_right = (alpha < p - 1) ? 1.0 / L_copy(alpha + 1) : 0.0;
        
        // Check intersection with the diagonal line v=u
        double u_new = (slope_num * u_cur + slope_denom * v_cur) / (slope_num + slope_denom);
        double v_new = u_new;
        
        if (u_new < v_right && v_new > h_bottom) {
            isDone = true;
            u_vec.insert(u_vec.begin(), u_new);
            v_vec.insert(v_vec.begin(), v_new);
            kmax_vec.insert(kmax_vec.begin(), 1.0);  // Diagonal has condition number 1
            break;
        }
        
        // Intersection with horizontal line v=h_bottom
        v_new = h_bottom;
        u_new = u_cur - slope_denom * (v_new - v_cur) / slope_num;
        
        // If outside rectangle, compute intersection with vertical line u=v_right
        if (u_new > v_right) {
            u_new = v_right;
            v_new = v_cur - slope_num * (u_new - u_cur) / slope_denom;
        }
        
        // Update alpha/beta and slopes
        if (std::abs(u_new - v_right) < eps) {
            // Keep this order! First update index, then slope
            alpha++;
            slope_num += L_copy(alpha);
        }
        
        if (std::abs(v_new - h_bottom) < eps) {
            // Keep this order! First update index, then slope
            beta--;
            slope_denom += L_copy(beta);
        }
        
        // Calculate new condition number
        double new_kmax = v_new / u_new;
        
        // Insert at the beginning because we're going backward
        u_vec.insert(u_vec.begin(), u_new);
        v_vec.insert(v_vec.begin(), v_new);
        kmax_vec.insert(kmax_vec.begin(), new_kmax);
        
        // Update current point
        u_cur = u_new;
        v_cur = v_new;
    }
    
    // Convert vectors to Eigen vectors
    PathResult result;
    result.k = Eigen::Map<Eigen::VectorXd>(kmax_vec.data(), kmax_vec.size());
    result.u = Eigen::Map<Eigen::VectorXd>(u_vec.data(), u_vec.size());
    result.v = Eigen::Map<Eigen::VectorXd>(v_vec.data(), v_vec.size());
    
    return result;
}

} // namespace condreg
