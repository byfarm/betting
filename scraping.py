from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

web_path = r"C:\Users\bucks\Downloads\chromedriver_win32\chromedriver"
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(web_path), options=chrome_options)

url = 'https://betway.com/en/sports/grp/baseball/usa/mlb'
driver.get(url)

odds = driver.find_elements(By.CLASS_NAME, 'odds')  # Replace 'your-odds-class-name' with the correct class name

od = [element.text for element in odds]
driver.quit()
print(od)