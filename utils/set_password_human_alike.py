import time

def set_password_human_alike(driver_element, password, time_step=.1):
    for char in password:
        driver_element.send_keys(char)
        time.sleep(time_step)
