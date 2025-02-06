import os
import random
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tqdm import tqdm

#! Data Augmentation

class DataAugmentation:
    def __init__(self, input_dir, output_base_dir):
        self.input_dir = input_dir
        self.output_base_dir = output_base_dir

        # Klasörleri oluştur
        self.folders = {
            "original": "original",
            "rotation": "rotation",
            "flip": "flip",
            "brightness": "brightness",
            "noise": "noise",
            "blur": "blur",
        }

        self.create_directories()

        # İşlenmiş görüntüleri saklamak için dictionary
        self.processed_images = {}

    def create_directories(self):
        """Gerekli klasörleri oluştur"""
        for folder in self.folders.values():
            path = os.path.join(self.output_base_dir, folder)
            os.makedirs(path, exist_ok=True)

    def apply_rotation(self, image, angle):
        """Görüntüyü döndür"""
        height, width = image.shape[:2]
        center = (width / 2, height / 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, rotation_matrix, (width, height))
        return rotated

    def apply_flip(self, image, flip_code):
        """Görüntüyü çevir"""
        return cv2.flip(image, flip_code)

    def apply_brightness(self, image, factor):
        """Parlaklığı ayarla"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv = hsv.astype(np.float32)
        hsv[:, :, 2] = hsv[:, :, 2] * factor
        hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
        hsv = hsv.astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def apply_noise(self, image, mean=0, sigma=25):
        """Gaussian gürültü ekle"""
        row, col, ch = image.shape
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy = image + gauss
        return np.clip(noisy, 0, 255).astype(np.uint8)

    def apply_blur(self, image, kernel_size=(5, 5)):
        """Gaussian bulanıklaştırma uygula"""
        return cv2.GaussianBlur(image, kernel_size, 0)

    def process_single_image(self, image_path):
        """Tek bir görüntüye tüm teknikleri uygula ve sonuçları sakla"""
        image = cv2.imread(image_path)
        if image is None:
            return None

        results = {
            "original": image,
            "rotation": self.apply_rotation(image.copy(), 90),
            "flip": self.apply_flip(image.copy(), 1),  # yatay çevirme
            "brightness": self.apply_brightness(image.copy(), 1.3),
            "noise": self.apply_noise(image.copy()),
            "blur": self.apply_blur(image.copy(), (5, 5)),
        }

        return results

    def visualize_augmentations(self, image_path):
        """Bir görüntü için tüm tekniklerin sonuçlarını görselleştir"""
        results = self.process_single_image(image_path)
        if results is None:
            print(f"Hata: {image_path} okunamadı")
            return

        # Matplotlib figure oluştur
        plt.figure(figsize=(20, 8))

        techniques = [
            ("Original", "original"),
            ("Rotation 90°", "rotation"),
            ("Horizontal Flip", "flip"),
            ("Brightness +30%", "brightness"),
            ("Noise", "noise"),
            ("Blur 5x5", "blur"),
        ]

        for idx, (title, key) in enumerate(techniques, 1):
            plt.subplot(2, 5, idx)
            img = cv2.cvtColor(results[key], cv2.COLOR_BGR2RGB)
            plt.imshow(img)
            plt.title(title)
            plt.axis("off")

        plt.tight_layout()
        plt.show()

        # Sonuçları kaydet
        for technique, img in results.items():
            output_path = os.path.join(
                self.output_base_dir,
                technique,
                f"{technique}_{os.path.basename(image_path)}",
            )
            cv2.imwrite(output_path, img)


##########? FOR CUTMIX ###########################################




def read_yolo_annotations(txt_path):
    """
    YOLO formatındaki .txt dosyasını okur.

    Args:
        txt_path (str): .txt dosyasının yolu

    Returns:
        list: [class_id, x_center, y_center, width, height] formatında anotasyonlar
    """
    annotations = []
    if os.path.exists(txt_path):
        with open(txt_path, "r") as f:
            for line in f:
                values = list(map(float, line.strip().split()))
                if len(values) == 5:
                    annotations.append(values)
    return annotations


def convert_yolo_to_bbox(yolo_anno, img_width, img_height):
    """
    YOLO formatından pixel koordinatlarına dönüştürür.

    Args:
        yolo_anno (list): [class_id, x_center, y_center, width, height]
        img_width (int): Görüntü genişliği
        img_height (int): Görüntü yüksekliği

    Returns:
        tuple: (class_id, x_min, y_min, width, height)
    """
    class_id, x_center, y_center, width, height = yolo_anno

    x_min = int((x_center - width / 2) * img_width)
    y_min = int((y_center - height / 2) * img_height)
    bbox_width = int(width * img_width)
    bbox_height = int(height * img_height)

    return class_id, x_min, y_min, bbox_width, bbox_height


def convert_bbox_to_yolo(class_id, x_min, y_min, width, height, img_width, img_height):
    """
    Pixel koordinatlarından YOLO formatına dönüştürür.
    """
    x_center = (x_min + width / 2) / img_width
    y_center = (y_min + height / 2) / img_height
    width = width / img_width
    height = height / img_height

    return [class_id, x_center, y_center, width, height]


def cutmix_images(img1, img2, bbox):
    """
    İki görüntü arasında CutMix işlemi yapar.
    """
    h, w, _ = img1.shape
    x_min, y_min, bbox_width, bbox_height = bbox

    x_max = min(x_min + bbox_width, w)
    y_max = min(y_min + bbox_height, h)

    mixed_img = img1.copy()
    mixed_img[y_min:y_max, x_min:x_max] = img2[y_min:y_max, x_min:x_max]

    return mixed_img, (x_min, y_min, x_max - x_min, y_max - y_min)


def get_image_pairs(input_dir):
    """
    Etiketli görüntü çiftlerini bulur.
    """
    image_files = []

    for file in os.listdir(input_dir):
        if file.endswith(".txt"):
            img_name = file.replace(".txt", ".jpg")
            if os.path.exists(os.path.join(input_dir, img_name)):
                image_files.append(img_name)

    return image_files


def perform_cutmix_augmentation(input_dir, output_dir, num_augmentations=50):
    """
    CutMix veri artırma işlemini gerçekleştirir.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Etiketli görüntüleri bul
    image_files = get_image_pairs(input_dir)
    print(f"Toplam etiketli görüntü sayısı: {len(image_files)}")

    if len(image_files) < 2:
        print("Yeterli görüntü bulunamadı!")
        return

    for i in tqdm(range(num_augmentations), desc="CutMix işlemi"):
        # Rastgele iki görüntü seç
        source_img_name = random.choice(image_files)
        target_img_name = random.choice(image_files)

        while source_img_name == target_img_name:  # Aynı görüntüyü seçmemek için
            target_img_name = random.choice(image_files)

        # Görüntüleri yükle
        source_img = cv2.imread(os.path.join(input_dir, source_img_name))
        target_img = cv2.imread(os.path.join(input_dir, target_img_name))

        if source_img is None or target_img is None:
            continue

        # Kaynak görüntünün anotasyonlarını al
        source_annotations = read_yolo_annotations(
            os.path.join(input_dir, source_img_name.replace(".jpg", ".txt"))
        )

        if not source_annotations:
            continue

        # Rastgele bir bounding box seç
        ann = random.choice(source_annotations)
        _, x_min, y_min, width, height = convert_yolo_to_bbox(
            ann, source_img.shape[1], source_img.shape[0]
        )

        # CutMix uygula
        mixed_img, mixed_bbox = cutmix_images(
            target_img, source_img, (x_min, y_min, width, height)
        )

        # Yeni görüntüyü kaydet
        output_img_name = f"cutmix_{i}.jpg"
        cv2.imwrite(os.path.join(output_dir, output_img_name), mixed_img)

        # Hedef görüntünün anotasyonlarını al
        target_annotations = read_yolo_annotations(
            os.path.join(input_dir, target_img_name.replace(".jpg", ".txt"))
        )

        # Yeni anotasyonları oluştur
        new_annotations = []

        # Hedef görüntü anotasyonlarını ekle (CutMix bölgesi ile çakışanları hariç tut)
        for ann in target_annotations:
            _, x_min, y_min, width, height = convert_yolo_to_bbox(
                ann, target_img.shape[1], target_img.shape[0]
            )
            bbox1 = (x_min, y_min, width, height)
            bbox2 = mixed_bbox

            # Bounding box'lar çakışmıyorsa ekle
            if not (
                bbox1[0] > bbox2[0] + bbox2[2]
                or bbox1[0] + bbox1[2] < bbox2[0]
                or bbox1[1] > bbox2[1] + bbox2[3]
                or bbox1[1] + bbox1[3] < bbox2[1]
            ):
                continue

            new_annotations.append(ann)

        # CutMix bölgesini ekle
        new_annotations.append(
            convert_bbox_to_yolo(
                0,
                mixed_bbox[0],
                mixed_bbox[1],
                mixed_bbox[2],
                mixed_bbox[3],
                mixed_img.shape[1],
                mixed_img.shape[0],
            )
        )

        # Yeni anotasyonları kaydet
        with open(os.path.join(output_dir, f"cutmix_{i}.txt"), "w") as f:
            for ann in new_annotations:
                f.write(f"{int(ann[0])} {ann[1]} {ann[2]} {ann[3]} {ann[4]}\n")


def visualize_results(output_dir, num_images=5):
    """
    CutMix sonuçlarını görselleştirir.
    """
    image_files = [f for f in os.listdir(output_dir) if f.endswith(".jpg")]

    for image_file in random.sample(image_files, min(num_images, len(image_files))):
        img = Image.open(os.path.join(output_dir, image_file))
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(np.array(img))

        # Anotasyonları görselleştir
        txt_file = image_file.replace(".jpg", ".txt")
        txt_path = os.path.join(output_dir, txt_file)

        if os.path.exists(txt_path):
            annotations = read_yolo_annotations(txt_path)
            for ann in annotations:
                class_id, x_center, y_center, width, height = ann

                left = (x_center - width / 2) * img.width
                top = (y_center - height / 2) * img.height
                box_width = width * img.width
                box_height = height * img.height

                rect = plt.Rectangle(
                    (left, top),
                    box_width,
                    box_height,
                    fill=False,
                    edgecolor="red",
                    linewidth=2,
                )
                ax.add_patch(rect)
                ax.text(
                    left,
                    top - 5,
                    f"Class {int(class_id)}",
                    color="red",
                    fontsize=12,
                    backgroundcolor="white",
                )

        plt.title(f"CutMix Result: {image_file}")
        plt.axis("off")
        plt.show()
