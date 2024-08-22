# import libraries (bs4, requests, pandas, time, logging, os)
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import logging
import os
import argparse
from fake_useragent import UserAgent

def get_headers():
    ua = UserAgent()
    return {'User-Agent': ua.random}

def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrape product data from Rozetka.')
    parser.add_argument('--num_page', type=int, default=2, help='Number of pages to scrape')
    parser.add_argument('--delay', type=int, default=2,help='Delay between requests in seconds.')
    parser.add_argument('--output', type=str, default='product.сsv', help='Output file name')
    return parser.parse_args()

# set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('scrape.log'), logging.StreamHandler()])

# directory of images (create folder for images)
image_dir = 'images'
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# url for parsing category
base_url = "https://hard.rozetka.com.ua/videocards/c80087/page={page_num};21330=geforce-rtx-3080/"

# Make get request and recieve statuse code of page
def get_page_content(url):
    try:
        response = requests.get(url, headers=get_headers(),timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        logging.error(f"Timeout occurred while trying to fetch {url}")
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
        product_name = product.text.strip() if product else "N/A"
        product_price = price.text.strip() if price else "N/A"
        product_availability = avail.text.strip() if avail else "N/A"
        image_url = image['src'] if image else None
        image_filename = download_image(image_url, product_name) if image_url else "No Image"

        # Check for attribute 'src'
        image_url = image.get('src') or image.get('data-src')
        if not image_url:
            logging.warning(f"No image URL found for product: {product_name}")
            image_filename = "No image"
        else:
            image_filename = download_image(image_url, product_name)

        parsed_data.append((product_name, product_price, product_availability, image_filename))
    return parsed_data
# Main function to perform the scraping
def scrape_site(base_url, num_page=2, delay=2, output_filename='product.csv'):
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
args = parse_arguments()
scrape_site(base_url, num_page=args.num_page, delay=args.delay, output_filename=args.output)
