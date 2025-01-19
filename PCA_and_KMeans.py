import logging
import os
import shutil
from itertools import compress
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.vq import kmeans2
from sklearn.decomposition import PCA
from tqdm import tqdm
from sklearn.manifold import TSNE

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def calcuate_pca(embeddings, dim=16):
    pca = PCA(n_components=dim)
    pca_embeddings = pca.fit_transform(embeddings.squeeze())
    logging.info(f"PCA is done. New shape is {pca_embeddings.shape}")
    return pca_embeddings, pca.explained_variance_ratio_

def calcuate_kmeans(embeddings, k):
    centroid, labels = kmeans2(data=embeddings, k=k, minit="points")
    counts = np.bincount(labels)
    return centroid, labels

def get_embeddings(file_path):
    embeddings = pd.read_csv(file_path)
    file_paths = embeddings["filepaths"]
    embeddings = embeddings.drop("filepaths", axis=1)
    return embeddings.values, file_paths

def plot_clusters_2d(embeddings, labels, title, save_path):
    """2D görselleştirme için t-SNE kullanarak kümeleri çizme"""
    print("Performing t-SNE dimensionality reduction for visualization...")
    tsne = TSNE(n_components=2, random_state=42)
    embeddings_2d = tsne.fit_transform(embeddings)
    
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], 
                         c=labels, cmap='tab10', alpha=0.6, s=100)
    
    # Küme merkezlerini göster
    for i in range(len(np.unique(labels))):
        mask = labels == i
        centroid = np.mean(embeddings_2d[mask], axis=0)
        plt.annotate(f'Cluster {i}', 
                    (centroid[0], centroid[1]),
                    fontsize=12, 
                    fontweight='bold',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    plt.colorbar(scatter, label='Cluster Labels')
    plt.title(title, fontsize=14, pad=20)
    plt.xlabel('t-SNE Component 1', fontsize=12)
    plt.ylabel('t-SNE Component 2', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def analyze_pothole_embeddings(csv_file_path, pca_dims=50, k=10):
    # Create output directories
    create_dir("./pca_plots")
    create_dir("./elbow_plots")
    create_dir("./cluster_plots")
    create_dir("./clustered_images/pothole")
    
    # Load embeddings
    embeddings, image_paths = get_embeddings(csv_file_path)
    print(f"Original embeddings shape: {embeddings.shape}")
    
    # Calculate PCA embeddings
    pca_embeddings, ratio = calcuate_pca(embeddings=embeddings, dim=pca_dims)
    
    # Plot cumulative explained variance
    plt.figure(figsize=(8, 6))
    cumsum_variance = np.cumsum(ratio)
    plt.plot(range(1, len(cumsum_variance) + 1), cumsum_variance, 
             marker='o', markersize=2, color='blue', linestyle='-', linewidth=1)
    plt.xlabel("Number of components")
    plt.ylabel("Cumulative explained variance")
    plt.title("PCA for Pothole")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(0, 50)
    plt.ylim(0.1, 0.8)
    plt.tight_layout()
    plt.savefig("./pca_plots/pothole.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Calculate distortions
    print("Calculating distortions for different cluster numbers...")
    distortions = []
    for i in tqdm(range(1, k + 1)):
        centroid, labels = calcuate_kmeans(embeddings=pca_embeddings, k=i)
        distortions.append(
            sum(np.min(np.square(pca_embeddings - centroid[labels]), axis=1))
            / pca_embeddings.shape[0]
        )
        
        # Her k değeri için kümeleri görselleştir
        if i > 1:  # t-SNE en az 2 küme gerektirir
            plot_clusters_2d(pca_embeddings, labels, 
                           f'K-means Clustering Distribution (k={i})',
                           f'./cluster_plots/clusters_k{i}.png')
    
    # Plot the elbow curve
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, k + 1), distortions, marker="o", markersize=6)
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Distortion")
    plt.title("Elbow Curve for Pothole Clustering")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.axvline(x=6, color="r", linestyle="--", label="Suggested k=6")
    plt.legend()
    plt.tight_layout()
    plt.savefig("./elbow_plots/pothole_elbow.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Final clustering with optimal k
    optimal_k = 6
    print(f"\nPerforming final clustering with k={optimal_k}...")
    centroid, labels = calcuate_kmeans(embeddings=pca_embeddings, k=optimal_k)
    
    # Plot final clustering distribution
    plot_clusters_2d(pca_embeddings, labels, 
                    'Final K-means Clustering Distribution',
                    './cluster_plots/final_clusters.png')
    
    # Organize images into clusters
    print("Organizing images into clusters...")
    for label_number in tqdm(range(optimal_k)):
        label_mask = labels == label_number
        path_images = list(compress(image_paths, label_mask))
        target_dir = f"./clustered_images/pothole/cluster_{label_number}"
        create_dir(target_dir)
        for image_path in path_images:
            shutil.copy(image_path, target_dir)
    
    return pca_embeddings, labels, distortions

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    csv_file_path = './embeddings/pothole.csv'
    pca_dims = 120
    k = 10
    
    pca_embeddings, labels, distortions = analyze_pothole_embeddings(
        csv_file_path=csv_file_path,
        pca_dims=pca_dims,
        k=k
    )
    
    # Print final clustering statistics
    unique_labels, counts = np.unique(labels, return_counts=True)
    print("\nFinal clustering statistics:")
    for label, count in zip(unique_labels, counts):
        print(f"Cluster {label}: {count} images")