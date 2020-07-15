from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import time
import os

load_dotenv('.env')

user = os.getenv('USER')
password = os.getenv('PASSWORD')

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get('https://login.bigcommerce.com/login')

email_field = driver.find_element_by_css_selector('#user_email')
password_field = driver.find_element_by_css_selector('#user_password')
submit_button = driver.find_element_by_css_selector('.login-form input[type=submit]')

email_field.clear()
email_field.send_keys(user)

password_field.clear()
password_field.send_keys(password)

submit_button.click()

# 2fp problem here :'/

time.sleep(6)
driver.quit()
