import requests
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


class ImageScraper:
    def __init__(self, search_terms, num_images=50, output_dir='pothole_images_new', unsplash_api_key=None):
        self.search_terms = search_terms
        self.num_images = num_images
        self.output_dir = output_dir
        self.unsplash_api_key = unsplash_api_key
        os.makedirs(self.output_dir, exist_ok=True)
        self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-gpu')  # Use GPU optimization
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def fetch_images(self, search_term, source="bing"):
        """Fetch image URLs from Bing, DuckDuckGo, Yahoo, or Unsplash."""
        print(f"Fetching images from {source} for: {search_term}")
        if source == "bing":
            self.driver.get(f'https://www.bing.com/images/search?q={search_term}')
            img_selector = 'img.mimg'
        elif source == "duckduckgo":
            self.driver.get(f'https://duckduckgo.com/?q={search_term}&iax=images&ia=images')
            img_selector = 'img[src]'  # Updated selector
        elif source == "yahoo":
            self.driver.get(f'https://images.search.yahoo.com/search/images?p={search_term}')
            img_selector = 'img[src]'  # Updated selector
        elif source == "unsplash":
            return self.fetch_images_from_unsplash(search_term)
        else:
            raise ValueError("Unsupported source. Choose 'bing', 'duckduckgo', 'yahoo', or 'unsplash'.")

        time.sleep(3)  # Allow the page to load
        urls = set()
        scroll_pause_time = 2

        max_scroll_attempts = 5  # Prevent infinite loops
        scroll_attempts = 0

        while len(urls) < self.num_images and scroll_attempts < max_scroll_attempts:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            scroll_attempts += 1
            images = self.driver.find_elements(By.CSS_SELECTOR, img_selector)

            for img in images:
                if len(urls) >= self.num_images:
                    break
                try:
                    url = img.get_attribute('src')
                    if url and url.startswith('http'):
                        urls.add(url)
                except Exception:
                    continue

        return list(urls)


    def fetch_images_from_unsplash(self, search_term):
        """Fetch image URLs from Unsplash API with pagination."""
        if not self.unsplash_api_key:
            raise ValueError("Unsplash API key is not provided.")

        print(f"Fetching images from Unsplash for: {search_term}")
        headers = {"Authorization": f"Client-ID {self.unsplash_api_key}"}
        urls = []
        per_page = 30  # Maximum allowed by Unsplash API
        total_pages = (self.num_images // per_page) + 1

        for page in range(1, total_pages + 1):
            if len(urls) >= self.num_images:
                break

            url = f"https://api.unsplash.com/search/photos?query={search_term}&per_page={per_page}&page={page}"
            response = requests.get(url, headers=headers).json()

            if 'results' in response:
                urls.extend([item['urls']['regular'] for item in response['results']])

        return urls[:self.num_images]


    def download_image(self, url, path):
        """Download an image from a URL to the specified path."""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception:
            return False

    def download_images(self, urls):
        """Download a list of images in parallel."""
        download_args = [
            (url, os.path.join(self.output_dir, f'image_{i}.jpg'))
            for i, url in enumerate(urls)
        ]

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(tqdm(
                executor.map(lambda args: self.download_image(*args), download_args),
                total=len(download_args),
                desc="Downloading Images"
            ))

        return sum(results)

    def run(self):
        try:
            all_urls = set()
            for term in self.search_terms:
                # Fetch Bing images
                bing_urls = self.fetch_images(term, source="bing")
                print(f"Bing: Found {len(bing_urls)} images for '{term}'.")

                # Fetch DuckDuckGo images
                duckduckgo_urls = self.fetch_images(term, source="duckduckgo")
                print(f"DuckDuckGo: Found {len(duckduckgo_urls)} images for '{term}'.")

                # Fetch Yahoo images
                yahoo_urls = self.fetch_images(term, source="yahoo")
                print(f"Yahoo: Found {len(yahoo_urls)} images for '{term}'.")

                # Fetch Unsplash images
                unsplash_urls = self.fetch_images(term, source="unsplash")
                print(f"Unsplash: Found {len(unsplash_urls)} images for '{term}'.")

                # Combine results
                all_urls.update(bing_urls + duckduckgo_urls + yahoo_urls + unsplash_urls)

            print(f"Total {len(all_urls)} unique images collected.")

            # Download images
            successful_downloads = self.download_images(list(all_urls))
            print(f"\n{successful_downloads} images successfully downloaded.")

        finally:
            self.driver.quit()


if __name__ == "__main__":
    search_terms = [
        "road pothole damage street",
        "pothole repair road",
        "damaged roads",
        "asphalt cracks potholes"
    ]
    unsplash_api_key = "LPCGn5kzSUXx4a8NEc6D8pbgeu76w5zQYDNwcuU5v28"  # Replace with your Unsplash API key
    scraper = ImageScraper(search_terms, num_images=100, unsplash_api_key=unsplash_api_key)
    scraper.run()
