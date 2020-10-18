def open_new_tab(driver, url):
    # open new tab
    driver.execute_script(
        "window.open(arguments[0], '_blank');",
        url,
    )
    last_handler = None
    # get latest handler/tab
    for handler in driver.window_handles:
        last_handler = handler
    # switch to the last handler
    driver.switch_to.window(last_handler)
