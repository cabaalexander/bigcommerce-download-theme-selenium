def change_attribute(driver, element, name, value):
    driver.execute_script(
        "arguments[0].setAttribute(arguments[1], arguments[2])",
        element,
        name,
        value,
    )
