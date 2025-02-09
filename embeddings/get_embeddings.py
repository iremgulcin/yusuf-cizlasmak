import pandas as pd
from img2vec_pytorch import Img2Vec
import numpy as np
from PIL import Image
from tqdm import tqdm
import os

def check_is_dir(path):
    if not os.path.isdir(path):
        raise ValueError(f"{path} is not a valid directory")
    return True

def load_image(image_path):
    image = Image.open(image_path).convert("RGB")
    return image

def filter_images(list_of_files):
    istenilen_uzantilar = [".jpg", ".jpeg", ".png", ".webp"]
    return [
        file for file in list_of_files
        if any(file.endswith(ext) for ext in istenilen_uzantilar)
    ]

def get_images_from_dir(path):
    check_is_dir(path)
    files = os.listdir(path)
    images = filter_images(files)
    images_path = [os.path.join(path, img) for img in images]
    return images_path

# Resim dosyalarını alma
paths = get_images_from_dir("all_pothole_images")

# Path'den gelen resimleri pillow formatında okuma (tqdm ile ilerleme çubuğu)
print("Resimler yükleniyor...")
images = [load_image(path) for path in tqdm(paths, desc="Loading Images")]

# Embedding modeli
img2vec = Img2Vec(cuda=True)  # GPU üzerinde çalıştırma

# Embedding çıkarma işlemi (tqdm ile ilerleme çubuğu)
print("Embedding çıkarılıyor...")
embeddings = [img2vec.get_vec(image) for image in tqdm(images, desc="Extracting Embeddings")]

# Embeddingleri numpy array formatına dönüştürme
embeddings = np.vstack(embeddings)

# Embeddingleri pandas dataframe'e çevirme
df = pd.DataFrame(embeddings)
df['filepaths'] = paths

# CSV olarak kaydetme
os.makedirs("embeddings", exist_ok=True)
output_path = "./embeddings/pothole.csv"
df.to_csv(output_path, index=False)

print(f"Embeddingler başarıyla kaydedildi: {output_path}")
