import sys
import os
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from condreg import select_condreg, kgrid, pfweights

# Create a true covariance matrix
p = 50  # Number of assets
sigma = np.eye(p)
# Add some correlation structure
for i in range(p):
    for j in range(p):
        if i != j:
            sigma[i, j] = 0.5 * np.exp(-0.1 * abs(i-j))

# Generate sample data
n = 100  # Number of observations
np.random.seed(42)
X = np.random.multivariate_normal(np.zeros(p), sigma, size=n)

# Generate grid of penalties
gridpts = kgrid(50, 100)

# Estimate covariance using condition number regularization
print("Estimating regularized covariance matrix...")
crcov = select_condreg(X, gridpts)

# Compute portfolio weights
print("Computing portfolio weights...")
w_true = pfweights(sigma)  # True optimal weights
w_sample = pfweights(X.T @ X / n)  # Sample-based weights
w_reg = pfweights(crcov['S'])  # Regularized weights

# Plot results
plt.figure(figsize=(12, 6))
plt.subplot(131)
plt.imshow(sigma, cmap='viridis')
plt.title('True Covariance')
plt.colorbar()

plt.subplot(132)
plt.imshow(X.T @ X / n, cmap='viridis')
plt.title('Sample Covariance')
plt.colorbar()

plt.subplot(133)
plt.imshow(crcov['S'], cmap='viridis')
plt.title(f'Regularized Covariance\n(kmax={crcov["kmax"]:.2f})')
plt.colorbar()

plt.tight_layout()
plt.savefig('covariance_comparison.png')
plt.close()

# Plot weights
plt.figure(figsize=(12, 5))
plt.subplot(131)
plt.bar(range(p), w_true)
plt.title('True Optimal Weights')
plt.ylim(0, max(w_true)*1.2)

plt.subplot(132)
plt.bar(range(p), w_sample)
plt.title('Sample-Based Weights')
plt.ylim(0, max(w_sample)*1.2)

plt.subplot(133)
plt.bar(range(p), w_reg)
plt.title('Regularized Weights')
plt.ylim(0, max(w_reg)*1.2)

plt.tight_layout()
plt.savefig('weights_comparison.png')

print("Plots saved as 'covariance_comparison.png' and 'weights_comparison.png'")