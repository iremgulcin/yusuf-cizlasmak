"""
Bu kodun amacı, pothole.csv dosyasındaki gömme (embedding) vektörlerini PCA (Principal Component Analysis) kullanarak analiz etmektir.

İlk versiyondur. İlgili gömme vektörlerinin kümülatif açıklanan varyansını gösteren bir grafik oluşturur.

Literatürde, PCA analizinde kümülatif açıklanan varyansın %80-95 aralığında tutulması yaygın bir uygulamadır.
(Kaynak: https://stats.oarc.ucla.edu/spss/seminars/efa-spss/?utm_source=chatgpt.com)
"""

import os
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def create_dir(path):
    """Belirtilen dizin mevcut değilse oluşturur."""
    if not os.path.exists(path):
        os.makedirs(path)

def analyze_pothole_embeddings(csv_dosya_yolu, pca_boyut=50):
    """
    Pothole gömme vektörlerini analiz eder ve PCA uygular.
    - Kümülatif açıklanan varyansı gösteren bir grafik oluşturur.
    - Belirtilen boyutta PCA uygular.
    """
    
    # Çıktı klasörünü oluştur
    create_dir("./pca_grafikleri")
    
    # Gömme vektörlerini yükle
    df = pd.read_csv(csv_dosya_yolu)
    
    # Dosya yollarını içeren sütunu kaldır
    if 'filepaths' in df.columns:
        embeddings = df.drop('filepaths', axis=1).values
    else:
        embeddings = df.values
    
    print(f"Orijinal gömme vektörü boyutu: {embeddings.shape}")
    
    # PCA ile tüm bileşenleri analiz et (varyans grafiği için)
    tam_pca = PCA()
    tam_pca.fit(embeddings)
    varyans_oranlari = tam_pca.explained_variance_ratio_
    
    # Kümülatif açıklanan varyansı görselleştir
    plt.figure(figsize=(8, 6))
    kümülatif_varyans = np.cumsum(varyans_oranlari)
    plt.plot(range(1, len(kümülatif_varyans) + 1), kümülatif_varyans, marker='o', 
             markersize=2, color='blue', linestyle='-', linewidth=1)
    
    plt.xlabel("Bileşen Sayısı")
    plt.ylabel("Kümülatif Açıklanan Varyans")
    plt.title("PCA ile Pothole Analizi")
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Grafik sınırlarını belirle
    plt.xlim(0, 50)
    plt.ylim(0.1, 0.8)
    
    # Düzeni ayarla
    plt.tight_layout()
    
    # Grafiği kaydet
    plt.savefig("./pca_grafikleri/pca_pothole.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Belirtilen bileşen sayısı ile PCA uygula
    pca = PCA(n_components=pca_boyut)
    pca_embeddings = pca.fit_transform(embeddings)
    print(f"PCA sonrası gömme vektörü boyutu: {pca_embeddings.shape}")
    
    # Seçilen PCA bileşenleriyle açıklanan toplam varyansı hesapla
    açıklanan_varyans = np.sum(pca.explained_variance_ratio_) * 100
    print(f"{pca_boyut} bileşen ile açıklanan toplam varyans: {açıklanan_varyans:.2f}%")
    
    return pca_embeddings, pca.explained_variance_ratio_

# Ana çalıştırma bloğu
if __name__ == "__main__":
    csv_dosya_yolu = './embeddings/pothole.csv'  # Gömme vektörleri dosya yolu
    pca_boyut = 120  # PCA için bileşen sayısı
    
    # Analizi çalıştır
    pca_embeddings, varyans_oranlari = analyze_pothole_embeddings(
        csv_dosya_yolu=csv_dosya_yolu,
        pca_boyut=pca_boyut
    )
