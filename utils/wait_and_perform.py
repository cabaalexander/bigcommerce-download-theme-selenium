from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def wait_and_perform(driver, css_selector, perform_function = lambda x: x, time = 10):
    wait = WebDriverWait(driver, time)
    return perform_function(wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))))
