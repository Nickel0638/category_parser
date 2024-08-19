# Product Data Scraper for site (example Rozetka)

This Python script is designed to scrape product information from the Rozetka website, specifically targeting the GPU section. The script extracts product names, prices, availability statuses, and downloads product images for each GPU listed on the specified pages. The extracted data is then saved into a CSV file for easy analysis.

## Features

- **Web Scraping with BeautifulSoup**: The script uses the BeautifulSoup library to parse HTML and extract relevant product information from each page.
- **Image Downloading**: Automatically downloads product images and saves them locally, with the file names corresponding to the product names.
- **Data Handling with Pandas**: The scraped data is structured and saved into a CSV file using Pandas, making it easy to analyze and work with the data.
- **Error Handling and Logging**: Includes robust error handling to manage HTTP errors and issues during image downloads. Logging is used to track the progress and any errors that occur during the scraping process.
- **Configurable Parameters**: Easily modify the number of pages to scrape and the delay between requests to avoid overloading the server.

## Usage

1. **Install Dependencies**: Make sure you have the necessary Python libraries installed:

   ```bash
   pip install requests beautifulsoup4 pandas
   ```

2. **Run the Script**: Execute the script in your Python environment:

   ```bash
   python scraper.py
   ```

3. **Check the Output**: The script will generate a `product.csv` file containing the scraped data and an `images` folder with the downloaded product images.

## Configuration

- **Number of Pages**: Modify the `num_page` parameter in the `scrape_rozetka` function call to change how many pages you want to scrape.
- **Delay**: Adjust the `delay` parameter to set the time delay between requests, helping to prevent IP blocking by the server.

## Example Output

  - `product.csv`: A CSV file containing the following columns:
  - `Product_name`: The name of the GPU.
  - `Price`: The price of the GPU.
  - `Availability`: The availability status of the GPU.
  - `Image_Filename`: The filename of the downloaded image for each product.
  - `images/`: A directory containing the product images, named after the products.
