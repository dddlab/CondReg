import sys
import os
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.gridspec import GridSpec
import seaborn as sns
from condreg import condreg, kgrid
from scipy import linalg

# Set style and colors
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("talk")
colors = plt.cm.viridis(np.linspace(0, 1, 8))

# Set random seed for reproducibility
np.random.seed(42)

def generate_structured_matrix(n=200, p=50, condition_number=2000):
    """
    Generate a covariance matrix with a specific structure and condition number.
    This creates a more realistic example than random eigenvalues.
    """
    # Create cluster structure for eigenvalues
    eig_cluster1 = np.linspace(800, 1000, 5)  # High eigenvalues
    eig_cluster2 = np.linspace(100, 300, 15)  # Medium eigenvalues
    eig_cluster3 = np.linspace(1, 10, 20)     # Low eigenvalues
    eig_cluster4 = np.linspace(0.5, 0.9, p-40) # Very low eigenvalues
    
    # Combine all eigenvalues
    eigenvalues = np.concatenate([eig_cluster1, eig_cluster2, eig_cluster3, eig_cluster4])
    
    # Scale eigenvalues to achieve desired condition number
    target_cond = condition_number
    current_cond = eigenvalues[0] / eigenvalues[-1]
    scaling_factor = (target_cond / current_cond) ** 0.5
    eigenvalues = np.concatenate([
        eigenvalues[:5] * scaling_factor,
        eigenvalues[5:] / scaling_factor
    ])
    
    # Generate random orthogonal matrix (eigenvectors)
    X = np.random.randn(p, p)
    Q, _ = np.linalg.qr(X)
    
    # Construct covariance matrix: Q * diag(eigenvalues) * Q.T
    cov_matrix = Q @ np.diag(eigenvalues) @ Q.T
    
    # Generate sample data from this covariance
    X = np.random.multivariate_normal(np.zeros(p), cov_matrix, size=n)
    
    return X, cov_matrix, eigenvalues

def plot_eigenvalue_shrinkage(k_values, true_cov, sample_cov, shrunk_covs):
    """
    Creates a detailed visualization of eigenvalue shrinkage with interactive elements.
    """
    # Get eigenvalues
    true_eigs = np.sort(np.linalg.eigvalsh(true_cov))[::-1]
    sample_eigs = np.sort(np.linalg.eigvalsh(sample_cov))[::-1]
    
    shrunk_eigs_list = []
    for k, cov in zip(k_values, shrunk_covs):
        shrunk_eigs = np.sort(np.linalg.eigvalsh(cov))[::-1]
        shrunk_eigs_list.append(shrunk_eigs)
    
    p = len(true_eigs)
    
    # Create figure with GridSpec for complex layout
    fig = plt.figure(figsize=(20, 15))
    gs = GridSpec(3, 3, figure=fig)
    
    # 1. Main plot: log-scale eigenvalue spectrum
    ax1 = fig.add_subplot(gs[0, :])
    ax1.loglog(range(1, p+1), true_eigs, 'k-', lw=2.5, label='True eigenvalues')
    ax1.loglog(range(1, p+1), sample_eigs, 'r--', lw=2, label='Sample eigenvalues')
    
    # Plot regularized eigenvalues with viridis colormap
    cmap = plt.cm.viridis
    norm = Normalize(vmin=min(k_values), vmax=max(k_values))
    
    for i, (k, eigs) in enumerate(zip(k_values, shrunk_eigs_list)):
        color = cmap(norm(k))
        ax1.loglog(range(1, p+1), eigs, '-', lw=1.5, color=color, label=f'k={k}')
    
    ax1.set_xlabel('Eigenvalue Index')
    ax1.set_ylabel('Eigenvalue (log scale)')
    ax1.set_title('Eigenvalue Spectrum with Different Regularization Parameters', fontsize=16)
    ax1.legend(loc='upper right', fontsize=12)
    ax1.grid(True, which="both", ls="--", alpha=0.3)
    
    # Add colorbar for k values
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, ax=ax1, orientation='horizontal', pad=0.1, 
                     label='Regularization Parameter (k)')
    cb.set_ticks(k_values)
    
    # 2. Waterfall plot: 3D view of shrinkage across k values
    ax2 = fig.add_subplot(gs[1, :2], projection='3d')
    
    # Convert data to suitable format for 3D
    X, Y = np.meshgrid(range(1, p+1), k_values)
    Z = np.array(shrunk_eigs_list)
    
    # Add sample eigenvalues as a reference plane
    ax2.plot(range(1, p+1), [min(k_values)]*p, sample_eigs, 'r--', lw=2, label='Sample')
    
    # Create the surface plot with custom coloring
    surf = ax2.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, 
                           rstride=1, cstride=1, edgecolor='none')
    
    # Set perspectives and labels
    ax2.view_init(30, 45)
    ax2.set_xlabel('Eigenvalue Index')
    ax2.set_ylabel('k Parameter')
    ax2.set_zlabel('Eigenvalue')
    ax2.set_title('3D Visualization of Regularization Effect', fontsize=16)
    ax2.set_zscale('log')
    fig.colorbar(surf, ax=ax2, shrink=0.5, label='Eigenvalue Magnitude')
    
    # 3. Shrinkage map: shows how each eigenvalue is modified
    ax3 = fig.add_subplot(gs[1, 2])
    
    # Create a grid of k values for dense visualization
    k_grid = np.logspace(np.log10(min(k_values)), np.log10(max(k_values)), 100)
    shrinkage_grid = []
    
    # Select a few representative eigenvalues
    eig_indices = [0, 4, 9, 19, 29, 39, 49 if p > 49 else p-1]
    markers = ['o', 's', '^', 'D', '*', 'p', 'X']
    
    for idx in eig_indices:
        if idx < p:
            # Original eigenvalue
            original = sample_eigs[idx]
            # Track how this eigenvalue changes with k
            shrink_values = []
            
            for k in k_grid:
                # We need to recompute for each k
                result = condreg(sample_cov, k)
                eigs = np.sort(np.linalg.eigvalsh(result['S']))[::-1]
                shrink_values.append(eigs[idx])
            
            # Plot the shrinkage path
            ax3.semilogx(k_grid, shrink_values, '-', marker=markers[eig_indices.index(idx)], 
                        markersize=8, markevery=10, label=f'λ{idx+1}')
    
    ax3.axhline(y=np.median(sample_eigs), color='gray', linestyle='--', 
               alpha=0.5, label='Median eigenvalue')
    ax3.set_xlabel('Regularization Parameter (k)')
    ax3.set_ylabel('Regularized Eigenvalue')
    ax3.set_title('Shrinkage Paths for Selected Eigenvalues', fontsize=16)
    ax3.legend(fontsize=10)
    ax3.grid(True)
    
    # 4. Before-after comparison
    ax4 = fig.add_subplot(gs[2, 0])
    
    # Choose a moderate k for demonstration
    mid_k_idx = len(k_values) // 2
    k_demo = k_values[mid_k_idx]
    shrunk_eigs_demo = shrunk_eigs_list[mid_k_idx]
    
    # Compute shrinkage factors
    shrinkage_factors = shrunk_eigs_demo / sample_eigs
    
    # Plot shrinkage factors
    sc = ax4.scatter(range(1, p+1), shrinkage_factors, c=sample_eigs, cmap='coolwarm', 
                    s=50, alpha=0.8, edgecolor='k')
    ax4.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
    ax4.set_xlabel('Eigenvalue Index')
    ax4.set_ylabel('Shrinkage Factor')
    ax4.set_title(f'Eigenvalue Shrinkage Factors (k={k_demo})', fontsize=16)
    fig.colorbar(sc, ax=ax4, label='Original Eigenvalue Magnitude')
    ax4.set_yscale('log')
    ax4.grid(True)
    
    # 5. Comparison to other shrinkage methods
    ax5 = fig.add_subplot(gs[2, 1:])
    
    # Function to compute Ledoit-Wolf shrinkage for comparison
    def ledoit_wolf_shrinkage(X):
        n, p = X.shape
        sample_cov = np.cov(X, rowvar=False)
        # Simplified L-W implementation
        mu = np.trace(sample_cov) / p
        alpha = 0.2  # Simplified shrinkage intensity
        shrunk_cov = (1-alpha) * sample_cov + alpha * mu * np.eye(p)
        return shrunk_cov
    
    # Generate data for this example
    n, p = 200, 50
    X, true_cov, _ = generate_structured_matrix(n, p)
    sample_cov = np.cov(X, rowvar=False)
    
    # Compute various shrinkage estimates
    lw_cov = ledoit_wolf_shrinkage(X)
    condreg_cov = condreg(X, 10)['S']
    
    # Get eigenvalues
    true_eigs = np.sort(np.linalg.eigvalsh(true_cov))[::-1]
    sample_eigs = np.sort(np.linalg.eigvalsh(sample_cov))[::-1]
    lw_eigs = np.sort(np.linalg.eigvalsh(lw_cov))[::-1]
    condreg_eigs = np.sort(np.linalg.eigvalsh(condreg_cov))[::-1]
    
    # Plot comparison
    ax5.loglog(range(1, p+1), true_eigs, 'k-', lw=2.5, label='True')
    ax5.loglog(range(1, p+1), sample_eigs, 'r--', lw=2, label='Sample')
    ax5.loglog(range(1, p+1), lw_eigs, 'g-', lw=1.5, label='Ledoit-Wolf')
    ax5.loglog(range(1, p+1), condreg_eigs, 'b-', lw=1.5, label='CondReg (k=10)')
    
    # Add condition numbers to legend
    true_cond = true_eigs[0] / true_eigs[-1]
    sample_cond = sample_eigs[0] / sample_eigs[-1]
    lw_cond = lw_eigs[0] / lw_eigs[-1]
    condreg_cond = condreg_eigs[0] / condreg_eigs[-1]
    
    legend_labels = [
        f'True (κ={true_cond:.1f})',
        f'Sample (κ={sample_cond:.1f})',
        f'Ledoit-Wolf (κ={lw_cond:.1f})',
        f'CondReg (κ={condreg_cond:.1f})'
    ]
    
    ax5.legend(legend_labels, fontsize=12)
    ax5.set_xlabel('Eigenvalue Index')
    ax5.set_ylabel('Eigenvalue (log scale)')
    ax5.set_title('Comparison with Other Shrinkage Methods', fontsize=16)
    ax5.grid(True, which="both", ls="--", alpha=0.3)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('advanced_eigenvalue_visualization.png', dpi=300, bbox_inches='tight')
    
    return fig

def create_shrinkage_animation(sample_cov, k_range):
    """
    Creates an animation showing how eigenvalues change as k increases.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    p = sample_cov.shape[0]
    sample_eigs = np.sort(np.linalg.eigvalsh(sample_cov))[::-1]
    
    # Initial plot
    ax.set_yscale('log')
    line_sample, = ax.plot(range(1, p+1), sample_eigs, 'r--', lw=2, label='Sample')
    line_reg, = ax.plot([], [], 'b-', lw=2, label='Regularized')
    
    title = ax.set_title('Condition Number Regularization with k=1', fontsize=14)
    ax.set_xlabel('Eigenvalue Index')
    ax.set_ylabel('Eigenvalue (log scale)')
    ax.legend()
    ax.grid(True, which="both", ls="--", alpha=0.3)
    
    # Animation function
    def animate(i):
        k = k_range[i]
        result = condreg(sample_cov, k)
        reg_eigs = np.sort(np.linalg.eigvalsh(result['S']))[::-1]
        
        line_reg.set_data(range(1, p+1), reg_eigs)
        title.set_text(f'Condition Number Regularization with k={k:.1f}')
        
        return line_reg, title
    
    # Create animation
    ani = FuncAnimation(fig, animate, frames=len(k_range), 
                       interval=200, blit=False, repeat=True)
    
    # Save animation
    ani.save('eigenvalue_animation.gif', writer='pillow', fps=5, dpi=100)
    
    return ani

def main():
    """Main function to run the example."""
    print("Generating dataset...")
    n, p = 200, 50
    X, true_cov, true_eigenvalues = generate_structured_matrix(n, p)
    
    # Compute sample covariance
    sample_cov = np.cov(X, rowvar=False)
    
    # Apply condreg with different regularization parameters
    k_values = [1, 2, 5, 10, 20, 50, 100]
    shrunk_covs = []
    
    print("Computing regularized covariance matrices...")
    for k in k_values:
        result = condreg(X, k)
        shrunk_covs.append(result['S'])
    
    print("Creating advanced visualization...")
    fig = plot_eigenvalue_shrinkage(k_values, true_cov, sample_cov, shrunk_covs)
    
    print("Creating animation...")
    k_range = np.logspace(0, 2, 20)  # 20 frames from k=1 to k=100
    ani = create_shrinkage_animation(sample_cov, k_range)
    
    print("Visualizations saved to:")
    print("- advanced_eigenvalue_visualization.png")
    print("- eigenvalue_animation.gif")
    
if __name__ == "__main__":
    main()