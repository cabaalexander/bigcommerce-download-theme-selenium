from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from utils import set_password_human_alike, open_new_tab, wait_and_perform

import re
import time
import os
import get_bigcommecre_token

load_dotenv('.env')

email = os.getenv('USER')
password = os.getenv('PASSWORD')

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)

####################################
#                                  #
# get bigcommerce token into gmail #
#                                  #
####################################

def trigger_bigcommerce_token():
    driver.get('https://login.bigcommerce.com/login')

    email_field = driver.find_element_by_css_selector('#user_email')
    email_field.clear()
    email_field.send_keys(email)

    password_field = driver.find_element_by_css_selector('#user_password')
    password_field.clear()
    password_field.send_keys(password)

    # this will trigger 2fp (gmail entry)
    submit_button = driver.find_element_by_css_selector(
        '.login-form input[type=submit]'
    )
    submit_button.click()

trigger_bigcommerce_token()

# let token to arrive to your email
time.sleep(3)
token = get_bigcommecre_token.main()

# enter verification code and hit enter
token_field = driver.find_element_by_css_selector(
    '#device_verification_otp_code'
)
token_field.clear()
set_password_human_alike(token_field, token)
token_field.send_keys(Keys.RETURN)

# select store
store_name = 'artbeads'
stores = driver.find_elements_by_css_selector('#stores a')
current_store = None
for store in stores:
    store_text = store.find_element_by_css_selector('h4')
    inner_text= driver.execute_script(
        "return arguments[0].innerText;",
        store_text
    ).strip()
    match = re.search(r'%s' % store_name, inner_text, re.IGNORECASE)
    if match:
        current_store = store
current_store.click()

# select storefront menu item (go to storefront)
store_front_menu_item = driver.find_element_by_css_selector('#nav-storefront')
store_front_menu_item.click()

# click dropdown button (to download the theme)
content_iframe = driver.find_element_by_css_selector('#content-iframe')
driver.switch_to.frame(content_iframe)
dropdown_button = driver.find_element_by_css_selector(
    'button.currentTheme-button'
)
dropdown_button.click()

# click download current theme
download_theme_button = driver.find_element_by_link_text('Download Current Theme')
download_theme_button.click()

# click confirm download
confirm_download = driver.find_element_by_css_selector('[for=confirm_download]')
confirm_download.click()

confirm_button = driver.find_element_by_css_selector('.modal-footer button')
confirm_button.click()

driver.switch_to.default_content()
