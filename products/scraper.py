import requests
from bs4 import BeautifulSoup
import pandas as pd

class Scraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Accept-Language": "en-US, en;q=0.5"
        }
        self.soup = None

    def fetch_page(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")

    def get_title(self):
        try:
            title = self.soup.find(id="productTitle").get_text().strip()
            return title
        except AttributeError:
            return "Title not found"

    def get_price(self):
        try:
            price = self.soup.find("span", {"class": "a-offscreen"}).get_text().strip()
            return price
        except AttributeError:
            return "Price not found"

    def get_hero_image_url(self):
        try:
            img_tag = self.soup.find(id="landingImage")
            img_url = img_tag['src'] if img_tag else "Image URL not found"
            return img_url
        except AttributeError:
            return "Image URL not found"

    def scrape(self):
        self.fetch_page()
        return {
            "title": self.get_title(),
            "price": self.get_price(),
            "hero_image_url": self.get_hero_image_url()
        }

    def save_to_csv(self, data):
        file_path = 'product_data.csv'
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['URL', 'Title', 'Price', 'Hero Image URL'])

        if not df[df['URL'] == data[0]].empty:
            print("URL already exists in the CSV file.")
        else:
            df = df.append({
                'URL': data[0],
                'Title': data[1],
                'Price': data[2],
                'Hero Image URL': data[3]
            }, ignore_index=True)
            df.to_csv(file_path, index=False)