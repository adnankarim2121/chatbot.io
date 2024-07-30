import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from parsel import Selector
import json

# IS SCRAPING GOOGLE REVIEWS ILLEGAAL? INTERNET AND GPT SEEMS DIVIDED
# URL for Google Maps
# Look at SERP api
url = 'https://www.google.com/maps'

# Path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\AdnanKarim\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Create a Service object with the path to the ChromeDriver
service = Service(chrome_driver_path)

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# Open Google Maps
driver.get(url)

# Maximize the browser window
driver.maximize_window()

# Wait for the search box to be present
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'searchboxinput'))
)

# Type the location into the search box
#chachi's chinook
#Codo Agave Social House
location = "Phil & Sebastian Coffee Roasters Chinook"
search_box.send_keys(location)

# Wait for the dropdown to appear and click the first result based on data-index
first_dropdown_result = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@data-index='0']"))
)
first_dropdown_result.click()

# Wait for the reviews button to be clickable
reviews_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'reviews')]"))
)

# Click the reviews button
reviews_button.click()
more_reviews_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'More reviews')]"))
)

# Click the "More reviews" button
more_reviews_button.click()

# Wait for a few seconds to load the reviews
time.sleep(5)

# Scroll to the bottom of the reviews section
scrollable_div = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'm6QErb DxyBCb kA9KIf dS8AEf XiKgde')]"))
)

last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

while True:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
    time.sleep(2)  # Wait for the page to load
    new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
    if new_height == last_height:
        break
    last_height = new_height

# click see more button 

# Wait until the "More" button is clickable and then click it
try:
    more_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//button[contains(@aria-label, "See more")]'))
    )
    for button in more_buttons:
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)  # Give it a moment to load more content

except TimeoutException:
    print("Timeout while waiting for the 'More' buttons.")


page_content = driver.page_source  

# Wait for a few seconds to load the reviews
time.sleep(5)

response = Selector(page_content)
# print(response)

time.sleep(1)


results = []

#need to get names of each review
# names =[]
# for el in response.xpath('//div/div[contains(@class, "d4r55")]'):
# 	text = el.xpath('text()').get()
# 	names.append(text)

# <span class="wiI7pd">
for el in response.xpath('//div/div[@data-review-id]'):
	# print("elemt new: ", el)
	results.append({
	    # 'title': el.xpath('.//div[contains(@class, "d4r55")]/span/text()').extract_first(''),
	    'rating': el.xpath('.//span[contains(@aria-label, "stars")]/@aria-label').extract_first('').replace('stars' ,'').strip(),
	    'body': el.xpath('.//span[contains(@class, "wiI7pd")]/text()').extract_first(''),
	})

print(results)

# Define the file name where you want to save the JSON data
filename = 'results.json'

# Open the file in write mode and dump the JSON data into it
with open(filename, 'w') as f:
    json.dump(results, f, indent=4)  # 'indent=4' is used for pretty printing the JSON data

print(f"Results saved to {filename}")

# Close the driver
driver.quit()

#now, lets do something with the reviews.
