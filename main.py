from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import time

zillow = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.65528766040039%2C%22east%22%3A-122.21137133959961%2C%22south%22%3A37.6457357086336%2C%22north%22%3A37.90462156329883%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A628295%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
google_forms = "https://docs.google.com/forms/d/e/1FAIpQLSfQl5nXIxz-baCzBWOe2ix1t0fdUmfbXdR-xtgOlPGbIfWd-A/viewform?usp=sf_link"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
response = requests.get(url=zillow, headers=header)
URL = response.text
soup = BeautifulSoup(URL, "html.parser")

# Properties Links:
properties_links = soup.find_all(name="a", class_='property-card-link')
properties_links_1 = []
for prop in properties_links:
    properties_links_1.append(prop["href"])

properties_links_2 = []
for prop in properties_links_1:
    if "https://www.zillow.com" not in prop:
        prop = f"https://www.zillow.com{prop}"
        properties_links_2.append(prop)
    else:
        properties_links_2.append(prop)
properties_links_final = list(dict.fromkeys(properties_links_2))
print(properties_links_final)
print(len(properties_links_final))

# Prices:
prices_website = soup.find_all(name="span", attrs={'data-test': 'property-card-price'})
prices = []
for price in prices_website:
    cost = price.getText().strip("+ 1 bd /mo 2 bds")
    prices.append(cost)
print(prices)
print(len(prices))

# Addresses:
addresses_website = soup.find_all(name='address', attrs={'data-test': 'property-card-addr'})
addresses = []
for address in addresses_website:
    location = address.get_text()
    addresses.append(location)
print(addresses)
print(len(addresses))



for num in range(9):
    chrome_driver_path = Service("/Users/faisalalnamlah/Desktop/Python Practice/chromedriver")
    driver = webdriver.Chrome(service=chrome_driver_path)
    driver.get(google_forms)
    time.sleep(5)
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(addresses[num])

    time.sleep(3)
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(prices[num])

    time.sleep(3)
    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(properties_links_final[num])

    time.sleep(3)
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    time.sleep(3)

time.sleep(1000)
