from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set the path for the ChromeDriver
webdriver_service = Service('chromedriver-win64\chromedriver-win64\chromedriver.exe')  # Change this to the path to your chromedriver

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Define the base URL for Amazon smart locks category
base_url = "https://www.amazon.in/s?k=smart+lock&page="

# Define the number of pages to scrape
num_pages = 3

# Define lists to store the data
brands = []
prices = []
ratings = []
rating_counts = []
urls = []


# Function to clean text
def clean_text(text):
    return text.strip().replace('\n', '')

# Loop through each page
for page in range(1, num_pages + 1):
    # Construct the URL for the current page
    url = base_url + str(page)
    
    # Use Selenium to open the page
    driver.get(url)
    
    # Pause to ensure the page loads completely
    time.sleep(3)
    
    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find all product elements
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    # Debug: Print the number of products found on the current page
    print(f"Page {page}: Found {len(products)} products")
    
    # Loop through each product and extract data
    for product in products:
        try:
            # URL
            product_url = product.find('a', class_='a-link-normal s-no-outline')
            if product_url:
                urls.append('https://www.amazon.in' + product_url['href'])
            else:
                urls.append(None)



            # Brand name
            brand = product.find('span', class_='a-size-base-plus a-color-base a-text-normal')
            if brand:
                brands.append(clean_text(brand.text))
            else:
                brands.append(None)
            
            # Price
            price_whole = product.find('span', class_='a-price-whole')
            #price_fraction = product.find('span', class_='a-price-fraction')
            if price_whole: #and price_fraction:
                price = clean_text(price_whole.text) #+ clean_text(price_fraction.text)
                prices.append(price)
            else:
                prices.append(None)
            
            # Rating
            rating = product.find('span', class_ = "a-size-medium a-color-base a-text-beside-button a-text-bold")
            if rating:
                ratings.append(clean_text(rating.text).split()[0])
            else:
                ratings.append(None)
            
            # Rating count
            rating_count = product.find('span', class_ = 'a-size-base s-underline-text')
            if rating_count:
                rating_counts.append(clean_text(rating_count.text).replace(',', ''))
            else:
                rating_counts.append(None)
            
            
            
            
        except Exception as e:
            print(f"Error processing product: {e}")
    # Pause to avoid getting blocked by Amazon
    time.sleep(2)

# Close the Selenium driver
driver.quit()

# Create a DataFrame
df = pd.DataFrame({
    'Brand Name': brands,
    'Price': prices,
    'Rating': ratings,
    'Rating Count': rating_counts,
    
    'URL': urls
})

# Save to a CSV file
df.to_csv('smart_locks2.csv', index=False)

# Debug: Print the DataFrame to check the results
print(df)

























































