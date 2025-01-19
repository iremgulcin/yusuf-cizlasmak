import flickrapi
import requests
import os
import io
from PIL import Image
import logging
from datetime import datetime
import imghdr
import cv2
import numpy as np
from pathlib import Path
import time

api_key = '3be520b257a4d4a50671fc8f388e6a1f'
api_secret = 'c7c0603b8f15d8b3'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')


class ImageValidator:
    """Görüntü doğrulama ve format kontrolü sınıfı"""
    
    VALID_FORMATS = {'JPEG', 'PNG', 'JPG'}
    MIN_WIDTH = 800
    MIN_HEIGHT = 600
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def is_valid_image(img_data: bytes) -> bool:
        """Görüntü verilerinin geçerliliğini kontrol eder"""
        try:
            # Format kontrolü
            img_format = imghdr.what(None, img_data)
            if img_format is None or img_format.upper() not in ImageValidator.VALID_FORMATS:
                return False
            
            # PIL ile görüntüyü aç
            img = Image.open(io.BytesIO(img_data))
            
            # Format doğrulama
            if img.format not in ImageValidator.VALID_FORMATS:
                return False
            
            # Boyut kontrolü
            if img.size[0] < ImageValidator.MIN_WIDTH or img.size[1] < ImageValidator.MIN_HEIGHT:
                return False
            
            # Dosya boyutu kontrolü
            if len(img_data) > ImageValidator.MAX_FILE_SIZE:
                return False
            
            # Görüntüyü test amaçlı yükle
            img.verify()
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def convert_to_jpg(img_data: bytes) -> bytes:
        """Görüntüyü JPG formatına dönüştürür"""
        try:
            # Görüntüyü PIL ile aç
            img = Image.open(io.BytesIO(img_data))
            
            # RGB'ye dönüştür (alfa kanalını kaldır)
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                bg = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else img.split()[1])
                img = bg
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # JPG olarak kaydet
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=95)
            return output.getvalue()
        except Exception as e:
            logging.error(f"Image conversion error: {e}")
            return None

def fetch_pothole_images(search_query: str, num_images: int) -> None:
    """Gelişmiş format kontrolü ile görüntüleri indirir"""
    
    # Logging ayarları
    logging.basicConfig(
        filename='image_download.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Çıktı klasörünü oluştur
    output_dir = Path('flickr_pothole_images')
    output_dir.mkdir(exist_ok=True)
    
    # Başarısız indirmeler için klasör
    failed_dir = output_dir / 'failed_downloads'
    failed_dir.mkdir(exist_ok=True)
    
    # İstatistikler
    stats = {
        'attempted': 0,
        'successful': 0,
        'failed': 0,
        'converted': 0
    }
    
    try:
        photos = flickr.photos.search(
            text=search_query,
            tags="pothole, road, asphalt, crack, damage",
            tag_mode="any",
            per_page=num_images * 2,
            extras="url_o, license, tags, title, description",
            sort="relevance",
            media="photos",
            license="4,5,6,7",
            safe_search=1,
            content_type=1
        )

        images = photos['photos']['photo']
        logging.info(f"Found {len(images)} images")

        downloaded = 0
        for idx, photo in enumerate(images):
            if downloaded >= num_images:
                break
                
            stats['attempted'] += 1
            url = photo.get('url_o')
            
            if not url:
                continue
                
            try:
                # Görüntüyü indir
                response = requests.get(url, timeout=10)
                img_data = response.content
                
                # Görüntü doğrulama
                if not ImageValidator.is_valid_image(img_data):
                    # Dönüştürme dene
                    converted_data = ImageValidator.convert_to_jpg(img_data)
                    if converted_data is None:
                        stats['failed'] += 1
                        logging.warning(f"Image {idx + 1} validation failed: {url}")
                        continue
                    
                    img_data = converted_data
                    stats['converted'] += 1
                
                # Dosya adını oluştur
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = output_dir / f"pothole_{timestamp}_{idx + 1}.jpg"
                
                # Görüntüyü kaydet
                with open(filename, 'wb') as f:
                    f.write(img_data)
                
                logging.info(f"Successfully downloaded and saved: {filename}")
                downloaded += 1
                stats['successful'] += 1
                
                # OpenCV ile görüntüyü test et
                img = cv2.imread(str(filename))
                if img is None:
                    raise ValueError("OpenCV could not read the image")
                
            except Exception as e:
                stats['failed'] += 1
                logging.error(f"Error processing image {idx + 1}: {str(e)}")
                
                # Başarısız indirmeyi kaydet
                error_file = failed_dir / f"failed_{timestamp}_{idx + 1}.txt"
                with open(error_file, 'w') as f:
                    f.write(f"URL: {url}\nError: {str(e)}")
                    
            # Rate limiting
            time.sleep(0.5)  # Flickr API sınırlamalarına uyum için

    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        raise

    finally:
        # İstatistikleri göster
        logging.info("\nDownload Statistics:")
        logging.info(f"Attempted: {stats['attempted']}")
        logging.info(f"Successful: {stats['successful']}")
        logging.info(f"Failed: {stats['failed']}")
        logging.info(f"Converted: {stats['converted']}")
        
        print("\nDownload Statistics:")
        print(f"Attempted: {stats['attempted']}")
        print(f"Successful: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        print(f"Converted: {stats['converted']}")

fetch_pothole_images('road pothole', 1000)

