from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from utils import set_password_human_alike, open_new_tab, wait_and_perform

import re
import time
import os
import get_bigcommecre_token

load_dotenv('.env')

email = os.getenv('USER')
password = os.getenv('PASSWORD')

###################################
#                                 #
# prepare driver to work headless #
#                                 #
###################################

# function to take care of downloading file
def enable_download_headless(driver, download_dir):
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command'
    )
    params = {
        'cmd':'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': download_dir
        }
    }
    driver.execute("send_command", params)

download_path = os.path.join(os.getcwd(), 'downloads')

# set options to make browser headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
    })
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

##################################
#                                #
# initialize driver with options #
#                                #
##################################

driver = webdriver.Chrome(
    options=chrome_options,
    executable_path=ChromeDriverManager().install()
)
driver.implicitly_wait(10)

########################
#                      #
# make download happen #
#                      #
########################
if not os.path.exists(download_path):
    os.mkdir(download_path)
enable_download_headless(driver, download_path)

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
    # just to be a little bit cautious here
    time.sleep(1)

    # this will trigger 2fp (gmail entry)
    submit_button = driver.find_element_by_css_selector(
        '.login-form input[type=submit]'
    )
    submit_button.click()

print('# login in to bigcommerce')
trigger_bigcommerce_token()

# let token to arrive to your email
print('# get bigcommerce token from your GMAIL account')
seconds = 6
print(f'# waiting {seconds} seconds...')
time.sleep(seconds)
token = get_bigcommecre_token.main()

print('# enter token in the input field')
# enter verification code and hit enter
token_field = driver.find_element_by_css_selector(
    '#device_verification_otp_code'
)
token_field.clear()
set_password_human_alike(token_field, token)
token_field.send_keys(Keys.RETURN)

# select store
store_name = 'artbeads'
print(f'# select your store {store_name}')
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
print('# click download theme')
download_theme_button = driver.find_element_by_link_text('Download Current Theme')
download_theme_button.click()

# click confirm download
confirm_download = driver.find_element_by_css_selector('[for=confirm_download]')
confirm_download.click()

confirm_button = driver.find_element_by_css_selector('.modal-footer button')
confirm_button.click()

driver.switch_to.default_content()

# end log
print(f'# you should check \'{download_path}\' to see the theme')
