#include <Rcpp.h>
#include <RcppEigen.h>
#include "condreg/condreg.hpp"
#include "condreg/utils.hpp"

// [[Rcpp::depends(RcppEigen)]]

// [[Rcpp::export]]
Rcpp::NumericVector kgrid_cpp(double gridmax, int numpts) {
  try {
    if (gridmax <= 1.0) {
      Rcpp::stop("gridmax must be greater than 1");
    }
    if (numpts <= 0) {
      Rcpp::stop("numpts must be positive");
    }
    
    Eigen::VectorXd result = condreg::kgrid(gridmax, numpts);
    return Rcpp::wrap(result);
  } catch (const std::exception& e) {
    Rcpp::stop("Error in kgrid: " + std::string(e.what()));
  }
}

// [[Rcpp::export]]
Rcpp::List condreg_cpp(const Rcpp::NumericMatrix& data_in, double kmax) {
  try {
    if (kmax < 1.0) {
      Rcpp::stop("kmax must be greater than or equal to 1");
    }
    
    // Convert R matrix to Eigen matrix
    Eigen::MatrixXd X = Rcpp::as<Eigen::MatrixXd>(data_in);
    
    // Call C++ function
    condreg::CondregResult result = condreg::condreg(X, kmax);
    
    // Return results as R list
    return Rcpp::List::create(
      Rcpp::Named("S") = Rcpp::wrap(result.S),
      Rcpp::Named("invS") = Rcpp::wrap(result.invS)
    );
  } catch (const std::exception& e) {
    Rcpp::stop("Error in condreg: " + std::string(e.what()));
  }
}

// [[Rcpp::export]]
Rcpp::List select_kmax_cpp(const Rcpp::NumericMatrix& X, const Rcpp::NumericVector& k, int folds = 0) {
  try {
    if (X.nrow() < 2) {
      Rcpp::stop("X must have at least 2 rows");
    }
    if (k.size() == 0) {
      Rcpp::stop("k must be non-empty");
    }
    
    // Convert R matrix/vector to Eigen
    Eigen::MatrixXd X_eigen = Rcpp::as<Eigen::MatrixXd>(X);
    Eigen::VectorXd k_eigen = Rcpp::as<Eigen::VectorXd>(k);
    
    // Validate k values
    for (int i = 0; i < k_eigen.size(); i++) {
      if (k_eigen(i) < 1.0) {
        Rcpp::stop("All k values must be greater than or equal to 1");
      }
    }
    
    // Call C++ function
    condreg::SelectKmaxResult result = condreg::select_kmax(X_eigen, k_eigen, folds);
    
    return Rcpp::List::create(
      Rcpp::Named("kmax") = result.kmax,
      Rcpp::Named("negL") = Rcpp::wrap(result.negL)
    );
  } catch (const std::exception& e) {
    Rcpp::stop("Error in select_kmax: " + std::string(e.what()));
  }
}

// [[Rcpp::export]]
Rcpp::List select_condreg_cpp(const Rcpp::NumericMatrix& X, const Rcpp::NumericVector& k, int folds = 0) {
  try {
    if (X.nrow() < 2) {
      Rcpp::stop("X must have at least 2 rows");
    }
    if (k.size() == 0) {
      Rcpp::stop("k must be non-empty");
    }
    
    // Convert R matrix/vector to Eigen
    Eigen::MatrixXd X_eigen = Rcpp::as<Eigen::MatrixXd>(X);
    Eigen::VectorXd k_eigen = Rcpp::as<Eigen::VectorXd>(k);
    
    // Validate k values
    for (int i = 0; i < k_eigen.size(); i++) {
      if (k_eigen(i) < 1.0) {
        Rcpp::stop("All k values must be greater than or equal to 1");
      }
    }
    
    // Call C++ function
    condreg::CondregResult result = condreg::select_condreg(X_eigen, k_eigen, folds);
    
    // Get kmax through additional call to select_kmax
    condreg::SelectKmaxResult kmax_result = condreg::select_kmax(X_eigen, k_eigen, folds);
    
    return Rcpp::List::create(
      Rcpp::Named("S") = Rcpp::wrap(result.S),
      Rcpp::Named("invS") = Rcpp::wrap(result.invS),
      Rcpp::Named("kmax") = kmax_result.kmax
    );
  } catch (const std::exception& e) {
    Rcpp::stop("Error in select_condreg: " + std::string(e.what()));
  }
}

// [[Rcpp::export]]
Rcpp::NumericVector pfweights_cpp(const Rcpp::NumericMatrix& sigma) {
  try {
    if (sigma.nrow() != sigma.ncol()) {
      Rcpp::stop("sigma must be a square matrix");
    }
    
    // Convert R matrix to Eigen
    Eigen::MatrixXd sigma_eigen = Rcpp::as<Eigen::MatrixXd>(sigma);
    
    Eigen::VectorXd result = condreg::pfweights(sigma_eigen);
    return Rcpp::wrap(result);
  } catch (const std::exception& e) {
    Rcpp::stop("Error in pfweights: " + std::string(e.what()));
  }
}

// [[Rcpp::export]]
double transcost_cpp(const Rcpp::NumericVector& wnew, const Rcpp::NumericVector& wold, 
                     double lastearnings, double reltc, double wealth) {
  try {
    if (wnew.size() != wold.size()) {
      Rcpp::stop("wnew and wold must have the same length");
    }
    if (reltc < 0) {
      Rcpp::stop("reltc must be non-negative");
    }
    if (wealth <= 0) {
      Rcpp::stop("wealth must be positive");
    }
    
    Eigen::VectorXd wnew_eigen = Rcpp::as<Eigen::VectorXd>(wnew);
    Eigen::VectorXd wold_eigen = Rcpp::as<Eigen::VectorXd>(wold);
    
    return condreg::transcost(wnew_eigen, wold_eigen, lastearnings, reltc, wealth);
  } catch (const std::exception& e) {
    Rcpp::stop("Error in transcost: " + std::string(e.what()));
  }
}
