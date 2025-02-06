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
    """Belirtilen dizin yoksa oluşturur."""
    if not os.path.exists(path):
        os.makedirs(path)

def calculate_pca(embeddings, dim=16):
    """Girdi olarak verilen gömüleri (embeddings) PCA ile boyut azaltma işlemi uygular."""
    pca = PCA(n_components=dim)
    pca_embeddings = pca.fit_transform(embeddings.squeeze())
    logging.info(f"PCA tamamlandı. Yeni şekil: {pca_embeddings.shape}")
    return pca_embeddings, pca.explained_variance_ratio_

def calculate_kmeans(embeddings, k):
    """Belirtilen sayıda küme (k) ile K-Means algoritmasını uygular."""
    centroid, labels = kmeans2(data=embeddings, k=k, minit="points")
    return centroid, labels

def get_embeddings(file_path):
    """CSV dosyasından gömüleri (embeddings) ve ilgili dosya yollarını okur."""
    embeddings = pd.read_csv(file_path)
    file_paths = embeddings["filepaths"]
    embeddings = embeddings.drop("filepaths", axis=1)
    return embeddings.values, file_paths

def plot_clusters_2d(embeddings, labels, title, save_path):
    """t-SNE kullanarak 2D küme görselleştirmesi yapar."""
    print("Görselleştirme için t-SNE boyut indirgeme işlemi uygulanıyor...")
    tsne = TSNE(n_components=2, random_state=42)
    embeddings_2d = tsne.fit_transform(embeddings)
    
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=labels, cmap='tab10', alpha=0.6, s=100)
    
    # Küme merkezlerini gösterme
    for i in range(len(np.unique(labels))):
        mask = labels == i
        centroid = np.mean(embeddings_2d[mask], axis=0)
        plt.annotate(f'Küme {i}', (centroid[0], centroid[1]), fontsize=12, fontweight='bold',
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    plt.colorbar(scatter, label='Küme Etiketleri')
    plt.title(title, fontsize=14, pad=20)
    plt.xlabel('t-SNE Bileşeni 1', fontsize=12)
    plt.ylabel('t-SNE Bileşeni 2', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def analyze_pothole_embeddings(csv_file_path, pca_dims=50, k=10):
    """Verilen gömüleri analiz eder, PCA ve K-Means uygular, sonuçları görselleştirir."""
    # Çıktı klasörlerini oluştur
    create_dir("./pca_plots")
    create_dir("./elbow_plots")
    create_dir("./cluster_plots")
    create_dir("./clustered_images/pothole")
    
    # Gömüleri yükle
    embeddings, image_paths = get_embeddings(csv_file_path)
    print(f"Orijinal gömülerin şekli: {embeddings.shape}")
    
    # PCA uygula
    pca_embeddings, ratio = calculate_pca(embeddings, dim=pca_dims)
    
    # Kümülatif varyans grafiğini çiz
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, len(ratio) + 1), np.cumsum(ratio), marker='o', markersize=2, color='blue', linestyle='-', linewidth=1)
    plt.xlabel("Bileşen Sayısı")
    plt.ylabel("Kümülatif Açıklanan Varyans")
    plt.title("PCA Açıklanan Varyans")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("./pca_plots/pothole.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Elbow yöntemi ile küme sayısını belirleme
    print("Farklı küme sayıları için distortion hesaplanıyor...")
    distortions = []
    for i in tqdm(range(1, k + 1)):
        centroid, labels = calculate_kmeans(embeddings=pca_embeddings, k=i)
        distortions.append(sum(np.min(np.square(pca_embeddings - centroid[labels]), axis=1)) / pca_embeddings.shape[0])
        
        # Küme görselleştirme
        if i > 1:
            plot_clusters_2d(pca_embeddings, labels, f'K-Means Küme Dağılımı (k={i})', f'./cluster_plots/clusters_k{i}.png')
    
    # Elbow grafiğini çiz
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, k + 1), distortions, marker="o", markersize=6)
    plt.xlabel("Küme Sayısı (k)")
    plt.ylabel("Distortion")
    plt.title("Elbow Yöntemi")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.axvline(x=6, color="r", linestyle="--", label="Önerilen k=6")
    plt.legend()
    plt.tight_layout()
    plt.savefig("./elbow_plots/pothole_elbow.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Son kümeleme işlemi
    optimal_k = 6
    print(f"\nSon kümeleme işlemi k={optimal_k} ile yapılıyor...")
    centroid, labels = calculate_kmeans(embeddings=pca_embeddings, k=optimal_k)
    
    # Nihai kümeleme görselleştirme
    plot_clusters_2d(pca_embeddings, labels, 'Nihai K-Means Kümeleme Dağılımı', './cluster_plots/final_clusters.png')
    
    # Görselleri küme klasörlerine yerleştir
    print("Görseller kümelere göre organize ediliyor...")
    for label_number in tqdm(range(optimal_k)):
        path_images = list(compress(image_paths, labels == label_number))
        target_dir = f"./clustered_images/pothole/cluster_{label_number}"
        create_dir(target_dir)
        for image_path in path_images:
            shutil.copy(image_path, target_dir)
    
    return pca_embeddings, labels, distortions


#* Kodu çalıştırma ########################################

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    analyze_pothole_embeddings("pothole_1.csv", pca_dims=120, k=10) 
