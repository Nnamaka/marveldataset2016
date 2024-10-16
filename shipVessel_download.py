# import requests
import os
import time
import platform
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import Request, urlopen
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options



# Function to check if running in Google Colab
def is_colab():
    try:
        from google.colab import drive  # Will throw an ImportError if not in Colab
        return True
    except ImportError:
        return False


def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode (no UI)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    if is_colab():
        # If running in Google Colab
        os.system('apt-get update')
        os.system('apt-get install -y chromium-browser chromium-driver')
        os.environ['PATH'] += ":/usr/lib/chromium-browser/:/usr/lib/chromium-browser/chromedriver"
        driver = webdriver.Chrome(service=Service("/usr/lib/chromium-browser/chromedriver"), options=chrome_options)
    else:
        # If running on a Windows machine
        if platform.system() == 'Windows':
            driver_path = r'C:\Users\USER\Downloads\Programs\chromedriver.exe' # Set your Windows chromedriver path
        else:
            driver_path = '/usr/lib/chromium-browser/chromedriver'  # Default for other systems

        driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
    
    return driver

# Function to download images
def download_images(image_urls, folder_name):
    # Create folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Download each image
    for i, url in enumerate(image_urls):
        # img_data = requests.get(url).content
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        img_data = response.read()
        img_name = f"{folder_name}/image_{i+1}.jpg"
        with open(img_name, 'wb') as handler:
            handler.write(img_data)
        print(f"Downloaded {img_name}")

# Function to scroll down and load more images
def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Read ship names from the text file
with open('shipvesselNames.txt', 'r') as file:
    ship_names = [line.strip() for line in file]

# Set up Selenium WebDriver (make sure you have the appropriate driver installed)
driver = setup_chrome_driver()

# Base URL (parameter will be inserted into `shipName`)
base_url = "https://www.shipspotting.com/photos/gallery?shipName={}&shipNameSearchMode=exact"

# for ship_name in ship_names:
#     print(f"Processing {ship_name}...")

#     # Replace spaces with '%20' for URL encoding
#     encoded_ship_name = ship_name.replace(' ', '%20')
#     url = base_url.format(encoded_ship_name)

#     # Open the URL using Selenium
#     driver.get(url)
    
#     # Scroll down to load more images (if applicable)
#     scroll_down(driver)
    
#     # Get the page source and parse it with BeautifulSoup
#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     # Find all image URLs on the page (adjust the selector based on the website's structure)
#     image_tags = soup.find_all('img')  # Adjust the selector to target the correct images
#     image_urls = [img['src'] for img in image_tags if img.get('src')]

#     # Download the images to a folder named after the ship vessel
#     download_images(image_urls, ship_name)

# # Close the browser
driver.quit()

print("Script finished.")
