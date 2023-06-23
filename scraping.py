from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to the ChromeDriver executable
webdriver_service = Service(r'C:\Users\bucks\Downloads\chromedriver_win32\chromedriver.exe')

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode

# Initialize ChromeDriver with the configured options
driver = webdriver.Chrome(service=webdriver_service, options=options)

# Navigate to the webpage
url = 'https://betway.com/en/sports/grp/baseball/usa/mlb'
driver.get(url)

# Wait for the page to load (adjust the sleep time if needed)
time.sleep(5)

# Find the desired element using its class name
class_name = 'odds'
element = driver.find_element(By.CLASS_NAME, class_name)

# Extract the text within the element
line = element.text

# Print the extracted line
print(line)

# Quit the browser
driver.quit()



