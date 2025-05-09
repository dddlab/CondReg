import sys
import os
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from condreg import condreg, kgrid

# Set random seed for reproducibility
np.random.seed(42)

def generate_ill_conditioned_matrix(n=100, p=20, condition_number=1000):
    """Generate a random covariance matrix with high condition number."""
    # Create random eigenvalues with desired condition number
    min_eig = 1.0
    max_eig = condition_number * min_eig
    
    # Generate logarithmically spaced eigenvalues
    eigenvalues = np.exp(np.linspace(np.log(min_eig), np.log(max_eig), p))
    
    # Generate random orthogonal matrix (eigenvectors)
    X = np.random.randn(p, p)
    Q, _ = np.linalg.qr(X)
    
    # Construct covariance matrix: Q * diag(eigenvalues) * Q.T
    cov_matrix = Q @ np.diag(eigenvalues) @ Q.T
    
    # Generate sample data from this covariance
    X = np.random.multivariate_normal(np.zeros(p), cov_matrix, size=n)
    
    return X, cov_matrix, eigenvalues

def main():
    # Generate sample data with high condition number
    n, p = 200, 30
    X, true_cov, true_eigenvalues = generate_ill_conditioned_matrix(n, p, condition_number=1000)
    
    # Compute sample covariance matrix
    sample_cov = np.cov(X, rowvar=False)
    
    # Get eigenvalues of sample covariance
    sample_eigenvalues = np.linalg.eigvalsh(sample_cov)
    sample_eigenvalues = np.sort(sample_eigenvalues)[::-1]  # Sort in descending order
    
    # Apply condreg with different regularization parameters
    kmax_values = [1, 2, 5, 10, 20, 50, 100]
    shrunk_eigenvalues = []
    
    for k in kmax_values:
        # Apply condreg
        result = condreg(X, k)
        
        # Get eigenvalues of regularized covariance
        reg_eigenvalues = np.linalg.eigvalsh(result['S'])
        reg_eigenvalues = np.sort(reg_eigenvalues)[::-1]  # Sort in descending order
        
        shrunk_eigenvalues.append(reg_eigenvalues)
    
    # Log scale is easier to visualize condition number effects
    plt.figure(figsize=(12, 8))
    
    # Plot original eigenvalues
    plt.loglog(range(1, p+1), true_eigenvalues, 'k-', linewidth=2, label='True eigenvalues')
    plt.loglog(range(1, p+1), sample_eigenvalues, 'ro--', linewidth=1.5, label='Sample eigenvalues')
    
    # Plot regularized eigenvalues
    colors = plt.cm.viridis(np.linspace(0, 1, len(kmax_values)))
    for i, (k, reg_eig) in enumerate(zip(kmax_values, shrunk_eigenvalues)):
        plt.loglog(range(1, p+1), reg_eig, '-', color=colors[i], linewidth=1.5, 
                 label=f'Regularized (k={k})')
    
    plt.xlabel('Eigenvalue index', fontsize=12)
    plt.ylabel('Eigenvalue', fontsize=12)
    plt.title('Effect of Condition Number Regularization on Eigenvalues', fontsize=14)
    plt.grid(True, which="both", ls="--", alpha=0.3)
    plt.legend(fontsize=10)
    
    # Calculate and display condition numbers
    true_cond = true_eigenvalues[0] / true_eigenvalues[-1]
    sample_cond = sample_eigenvalues[0] / sample_eigenvalues[-1]
    
    reg_conds = [eig[0] / eig[-1] for eig in shrunk_eigenvalues]
    
    cond_text = f"True condition #: {true_cond:.1f}\n"
    cond_text += f"Sample condition #: {sample_cond:.1f}\n"
    for k, cond in zip(kmax_values, reg_conds):
        cond_text += f"Regularized (k={k}) condition #: {cond:.1f}\n"
    
    # Add text box with condition numbers
    plt.figtext(0.15, 0.02, cond_text, fontsize=9, 
                bbox=dict(facecolor='white', alpha=0.8))
    
    plt.tight_layout(rect=[0, 0.1, 1, 0.95])  # Adjust layout to make room for text
    plt.savefig('eigenvalue_shrinkage.png')
    
    # Create another plot showing how the eigenvalue shrinkage depends on the original values
    plt.figure(figsize=(10, 8))
    
    # Use different marker styles for clarity
    markers = ['o', 's', '^', 'D', 'v', '<', '>']
    
    for i, (k, reg_eig) in enumerate(zip(kmax_values, shrunk_eigenvalues)):
        plt.scatter(sample_eigenvalues, reg_eig, s=40, marker=markers[i % len(markers)], 
                  label=f'k={k}', alpha=0.7, color=colors[i])
    
    # Add the y=x line for reference
    max_val = max(np.max(sample_eigenvalues), np.max(shrunk_eigenvalues[0]))
    min_val = min(np.min(sample_eigenvalues), np.min(shrunk_eigenvalues[-1]))
    plt.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, label='No shrinkage')
    
    plt.xlabel('Sample eigenvalues', fontsize=12)
    plt.ylabel('Regularized eigenvalues', fontsize=12)
    plt.title('Eigenvalue Shrinkage vs. Original Eigenvalues', fontsize=14)
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, which="both", ls="--", alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig('eigenvalue_shrinkage_comparison.png')
    
    print("Plots saved as 'eigenvalue_shrinkage.png' and 'eigenvalue_shrinkage_comparison.png'")
    
    # Create another plot showing the effect of k on condition number
    k_range = np.linspace(1, 100, 100)
    condition_numbers = []
    
    for k in k_range:
        result = condreg(X, k)
        evals = np.linalg.eigvalsh(result['S'])
        condition_numbers.append(evals.max() / evals.min())
    
    plt.figure(figsize=(10, 6))
    plt.plot(k_range, condition_numbers, 'b-', linewidth=2)
    plt.axhline(y=sample_cond, color='r', linestyle='--', alpha=0.7, 
               label=f'Sample condition # = {sample_cond:.1f}')
    plt.xlabel('Regularization parameter (k)', fontsize=12)
    plt.ylabel('Condition number', fontsize=12)
    plt.title('Effect of Regularization Parameter on Condition Number', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    
    # Annotate the relationship: condition number ≤ k
    for i, k in enumerate(kmax_values):
        if k <= 100:  # Only annotate points within our k range
            idx = np.searchsorted(k_range, k)
            if idx < len(condition_numbers):
                cond = condition_numbers[idx]
                plt.scatter([k], [cond], color=colors[i], s=50, zorder=10)
                plt.annotate(f'k={k}', xy=(k, cond), xytext=(10, 0), 
                           textcoords='offset points', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('condition_number_vs_k.png')
    
    print("Additional plot saved as 'condition_number_vs_k.png'")

if __name__ == "__main__":
    main()
