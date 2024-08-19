# import libraries (bs4, requests, pandas, time, logging, os)
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import logging
import os

# set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# directory of images (create folder for images)
image_dir = 'images'
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# url for parsing category
base_url = "https://hard.rozetka.com.ua/videocards/c80087/page={page_num};21330=geforce-rtx-3080/"

# Make get request and recieve statuse code of page
def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
    return None

# Download images
def download_image(url , product_name):
    try:
        image_data = requests.get(url).content
        image_filename = os.path.join(image_dir, f"{product_name.replace('/', '_')}.jpg")
        with open(image_filename, 'wb') as image_file:
            image_file.write(image_data)
        logging.info(f"Download image for {product_name}")
        return image_filename
    except Exception as e:
        logging.error(f"Failed to download image from {url}: {e}")
        return None

# parsing with bs4
def parse_page(html):
    doc = BeautifulSoup(html, "html.parser")
    products = doc.select("span.goods-tile__title")
    prices = doc.select(".goods-tile__price-value")
    availability = doc.select(".goods-tile__availability.goods-tile__availability--available.ng-star-inserted")
    images = doc.select("img.ng-lazyloaded, img.lazy_img_hover")

# parsed data list loop
    parsed_data = []
    for product, price, avail, image in zip(products, prices, availability, images):
        product_name = product.text.strip()
        product_price = price.text.strip()
        product_availability = avail.text.strip()
        image_url = image['src']
        image_filename = download_image(image_url, product_name)
        parsed_data.append((product_name, product_price, product_availability, image_filename))
    return parsed_data

# main function to perform the scrapping
def scrape_site(base_url, num_page=2, delay=2):
    all_products = []

    for page in range(1, num_page + 1):
        url = base_url.format(page_num = page)
        html = get_page_content(url)

        if html is None:
            logging.info(f"Skipping page {page} due to an error")
            continue

        products = parse_page(html)
        all_products.extend(products)
        time.sleep(delay) # pause between iterations

    # Create and save DataFrame
    df = pd.DataFrame(all_products, columns=['Product_name', 'Price', 'Availability', 'Image_Filename'])
    try:
        df.to_csv('product.csv',index=False)
        logging.info(f'Parsed {num_page} pages and saved to product.csv')
    except Exception as e:
        logging.error(f'Failed to save file: {e}')

# start function
scrape_site(base_url, num_page=2, delay=2)
