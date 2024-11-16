from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import pprint
from fake_useragent import UserAgent
ua = UserAgent()

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument(f"user-agent={ua.random}")
chrome_options.add_argument('--log-level=3')

# Set the path for the ChromeDriver
webdriver_service = Service('chromedriver-win64\chromedriver-win64\chromedriver.exe')  # Change this to the path to your chromedriver

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
url = 'https://www.amazon.in/QUBO-Essential-Unlocking-Fingerprint-Mechanical/dp/B0BDFMGZVD/ref=sr_1_7?sr=8-7'
driver.get(url)
time.sleep(40)
soup_test = BeautifulSoup(driver.page_source,'html.parser')
#soup_test2 = soup_test.find_all("td", class_ = "a-size-base prodDetAttrValue")

#pprint.pp(soup_test2)
time.sleep(10)
brand_name = soup_test.find("span",attrs={"id":"productTitle","class":"a-size-large product-title-word-break"}).get_text().split()[0]

price = soup_test.find("span",class_ = "a-price-whole").get_text()

rating = soup_test.find("span",class_ = "a-icon-alt").get_text().split()[0]

rating_count = soup_test.find("span", attrs={"id":"acrCustomerReviewText","class":"a-size-base"}).get_text().split()[0]

print(f'brand {brand_name} \nrating {rating} \ncount {rating_count} \nprice {price}')


