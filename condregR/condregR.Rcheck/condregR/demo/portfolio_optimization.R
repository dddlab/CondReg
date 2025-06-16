# Portfolio Optimization with Condition Number Regularization
# This demo shows how to use the condregR package for portfolio optimization

library(condregR)

# Load simulation data
data(simulationdata)
cat("Loaded simulation data with dimensions:", dim(R), "\n")

# Parameters for the analysis
M <- 45            # estimation horizon
p <- ncol(R)       # number of assets
n_periods <- 5     # number of rebalancing periods for demo

cat("Number of assets:", p, "\n")
cat("Estimation horizon:", M, "\n")

# Generate penalty grid for cross-validation
k_grid <- kgrid(gridmax = 20, numpts = 30)
cat("Generated penalty grid with", length(k_grid), "values\n")
cat("Penalty range: [", min(k_grid), ",", max(k_grid), "]\n")

# Function to estimate covariance using different methods
estimate_covariance <- function(X, method = "condreg") {
  if (method == "sample") {
    # Sample covariance
    return(cov(X))
  } else if (method == "condreg") {
    # Condition number regularized covariance
    result <- select_condreg(X, k_grid)
    cat("Selected penalty parameter:", result$kmax, "\n")
    return(result$S)
  }
}

# Simulate portfolio optimization over multiple periods
set.seed(123)
start_period <- 100
results <- list()

for (t in 1:n_periods) {
  cat("\n--- Period", t, "---\n")
  
  # Define training period
  train_start <- start_period + (t-1) * 10
  train_end <- train_start + M - 1
  
  if (train_end > nrow(R)) break
  
  # Extract training data
  X_train <- R[train_start:train_end, ]
  cat("Training period:", train_start, "to", train_end, "\n")
  
  # Estimate covariance matrices using different methods
  Sigma_sample <- estimate_covariance(X_train, "sample")
  Sigma_condreg <- estimate_covariance(X_train, "condreg")
  
  # Compute condition numbers
  eig_sample <- eigen(Sigma_sample, only.values = TRUE)$values
  eig_condreg <- eigen(Sigma_condreg, only.values = TRUE)$values
  
  cond_sample <- max(eig_sample) / min(eig_sample)
  cond_condreg <- max(eig_condreg) / min(eig_condreg)
  
  cat("Sample covariance condition number:", round(cond_sample, 2), "\n")
  cat("Condreg covariance condition number:", round(cond_condreg, 2), "\n")
  
  # Compute optimal portfolio weights
  w_sample <- pfweights(Sigma_sample)
  w_condreg <- pfweights(Sigma_condreg)
  
  # Store results
  results[[t]] <- list(
    period = t,
    train_start = train_start,
    train_end = train_end,
    cond_sample = cond_sample,
    cond_condreg = cond_condreg,
    weights_sample = w_sample,
    weights_condreg = w_condreg
  )
  
  cat("Sample weights range: [", round(min(w_sample), 4), ",", round(max(w_sample), 4), "]\n")
  cat("Condreg weights range: [", round(min(w_condreg), 4), ",", round(max(w_condreg), 4), "]\n")
}

# Summary analysis
cat("\n=== SUMMARY ===\n")
cat("Condition Number Comparison:\n")
for (i in 1:length(results)) {
  cat("Period", i, ": Sample =", round(results[[i]]$cond_sample, 2), 
      ", Condreg =", round(results[[i]]$cond_condreg, 2), "\n")
}

# Compute average condition numbers
avg_cond_sample <- mean(sapply(results, function(x) x$cond_sample))
avg_cond_condreg <- mean(sapply(results, function(x) x$cond_condreg))

cat("\nAverage condition numbers:\n")
cat("Sample covariance:", round(avg_cond_sample, 2), "\n")
cat("Condreg covariance:", round(avg_cond_condreg, 2), "\n")
cat("Improvement factor:", round(avg_cond_sample / avg_cond_condreg, 2), "\n")

# Demonstrate transaction cost calculation
if (length(results) >= 2) {
  cat("\n=== TRANSACTION COST EXAMPLE ===\n")
  
  # Compare transaction costs between periods 1 and 2
  w_old <- results[[1]]$weights_condreg
  w_new <- results[[2]]$weights_condreg
  
  # Simulate some parameters
  lastearnings <- 1.02  # 2% return
  reltc <- 0.005        # 0.5% transaction cost
  wealth <- 10000       # $10,000 portfolio
  
  tc <- transcost(w_new, w_old, lastearnings, reltc, wealth)
  cat("Transaction cost for rebalancing: $", round(tc, 2), "\n")
  cat("As percentage of wealth:", round(100 * tc / wealth, 3), "%\n")
}

cat("\nDemo completed successfully!\n") 