import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

class DataAugmentation:
    def __init__(self, input_dir, output_base_dir):
        self.input_dir = input_dir
        self.output_base_dir = output_base_dir
        
        # Klasörleri oluştur
        self.folders = {
            'original': 'original',
            'rotation': 'rotation',
            'flip': 'flip',
            'brightness': 'brightness',
            'noise': 'noise',
            'zoom': 'zoom',
            'blur': 'blur'
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
        center = (width/2, height/2)
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
        hsv[:,:,2] = hsv[:,:,2] * factor
        hsv[:,:,2] = np.clip(hsv[:,:,2], 0, 255)
        hsv = hsv.astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    def apply_noise(self, image, mean=0, sigma=25):
        """Gaussian gürültü ekle"""
        row, col, ch = image.shape
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy = image + gauss
        return np.clip(noisy, 0, 255).astype(np.uint8)
    
    def apply_zoom(self, image, zoom_factor):
        """Yakınlaştır ve kırp"""
        height, width = image.shape[:2]
        center_x, center_y = width//2, height//2
        
        crop_width = int(width/zoom_factor)
        crop_height = int(height/zoom_factor)
        
        x1 = center_x - crop_width//2
        y1 = center_y - crop_height//2
        x2 = x1 + crop_width
        y2 = y1 + crop_height
        
        cropped = image[y1:y2, x1:x2]
        return cv2.resize(cropped, (width, height))
    
    def apply_blur(self, image, kernel_size=(5,5)):
        """Gaussian bulanıklaştırma uygula"""
        return cv2.GaussianBlur(image, kernel_size, 0)
    
    def process_single_image(self, image_path):
        """Tek bir görüntüye tüm teknikleri uygula ve sonuçları sakla"""
        image = cv2.imread(image_path)
        if image is None:
            return None
            
        results = {
            'original': image,
            'rotation': self.apply_rotation(image.copy(), 90),
            'flip': self.apply_flip(image.copy(), 1),  # yatay çevirme
            'brightness': self.apply_brightness(image.copy(), 1.3),
            'noise': self.apply_noise(image.copy()),
            'zoom': self.apply_zoom(image.copy(), 1.2),
            'blur': self.apply_blur(image.copy(), (5,5))
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
            ('Original', 'original'),
            ('Rotation 90°', 'rotation'),
            ('Horizontal Flip', 'flip'),
            ('Brightness +30%', 'brightness'),
            ('Noise', 'noise'),
            ('Zoom 120%', 'zoom'),
            ('Blur 5x5', 'blur'),
        ]
        
        for idx, (title, key) in enumerate(techniques, 1):
            plt.subplot(2, 5, idx)
            img = cv2.cvtColor(results[key], cv2.COLOR_BGR2RGB)
            plt.imshow(img)
            plt.title(title)
            plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        # Sonuçları kaydet
        for technique, img in results.items():
            output_path = os.path.join(self.output_base_dir, technique, 
                                     f"{technique}_{os.path.basename(image_path)}")
            cv2.imwrite(output_path, img)