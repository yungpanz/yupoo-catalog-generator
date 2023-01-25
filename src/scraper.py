from bs4 import BeautifulSoup
import re
from extract_price import ExtractPrice

def replace_url_string(url: str):
    return url.replace("small", "medium")


class Scraper:
    def __init__(self, html):
        self.html = html

    def extract_products(self):
        # Create a Beautiful Soup object
        soup = BeautifulSoup(self.html, 'html.parser')

        # Find all the "album__main" "a" tags
        album_main_a_tags = soup.find_all('a', class_='album__main')

        # Initialize an empty list to store the extracted products
        products = []
        
        # Create a instance of the ExtractPrice class
        extractor = ExtractPrice()

        # Iterate over the "album__main" "a" tags
        for album_main_a_tag in album_main_a_tags:
            try:
                # Extract the product name and price from the "title" attribute of the "a" tag
                product_name_and_price = album_main_a_tag['title']
                
                # Extract the product name and price
                extracted_data = extractor.extract(product_name_and_price)
                
                product_name = extracted_data['name']
                product_price = extracted_data['price']
                
                # Skip the item if the price is not found
                if product_price == None:
                    raise Exception("Price not found")

                # Find the "img" tag inside the "album__imgwrap" div
                img_tag = album_main_a_tag.find('div', class_='album__imgwrap').find('img')

                # Extract the image URL from the "data-src" attribute of the "img" tag
                image_url = img_tag['data-src']
                
                # Replace the image url with the high resolution one
                image_url = replace_url_string(image_url)

                # Add "https:" to the beginning of the image URL
                image_url = 'https:' + image_url

                # Add the product name, price, and image URL to the list of products
                products.append({
                    'name': product_name,
                    'price': product_price,
                    'image_url': image_url
                })
            except Exception as e:
                print(e)

        # Return the list of products
        return products
