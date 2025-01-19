import os
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def create_dir(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

def analyze_pothole_embeddings(csv_file_path, pca_dims=50):
    """Analyze pothole embeddings with PCA"""
    # Create output directory
    create_dir("./pca_plots")
    
    # Load embeddings
    df = pd.read_csv(csv_file_path)
    
    # Dosya yollarını içeren sütunu kaldır
    if 'filepaths' in df.columns:
        embeddings = df.drop('filepaths', axis=1).values
    else:
        embeddings = df.values
    
    print(f"Original embeddings shape: {embeddings.shape}")
    
    # Full PCA analysis for variance plot
    full_pca = PCA()
    full_pca.fit(embeddings)
    variance_ratios = full_pca.explained_variance_ratio_
    
    # Plot cumulative explained variance
    plt.figure(figsize=(8, 6))
    cumsum_variance = np.cumsum(variance_ratios)
    plt.plot(range(1, len(cumsum_variance) + 1), cumsum_variance, marker='o', 
             markersize=2, color='blue', linestyle='-', linewidth=1)
    
    plt.xlabel("Number of components")
    plt.ylabel("Cumulative explained variance")
    plt.title("PCA for Pothole")
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Set axis limits similar to the example
    plt.xlim(0, 50)
    plt.ylim(0.1, 0.8)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save plot
    plt.savefig("./pca_plots/pca_pothole.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Reduced dimensionality PCA
    pca = PCA(n_components=pca_dims)
    pca_embeddings = pca.fit_transform(embeddings)
    print(f"PCA embeddings shape: {pca_embeddings.shape}")
    
    # Calculate explained variance for reduced dimensions
    explained_variance = np.sum(pca.explained_variance_ratio_) * 100
    print(f"Explained variance with {pca_dims} components: {explained_variance:.2f}%")
    
    return pca_embeddings, pca.explained_variance_ratio_

# Main execution
if __name__ == "__main__":
    csv_file_path = './embeddings/pothole.csv'
    pca_dims = 100  # PCA boyut sayısı
    
    # Analizi çalıştır
    pca_embeddings, variance_ratios = analyze_pothole_embeddings(
        csv_file_path=csv_file_path,
        pca_dims=pca_dims
    )