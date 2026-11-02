import os

import pytest
from selenium import webdriver

from config import BROWSER, DRIVER_PATH, HEADLESS


@pytest.fixture
def driver():
    if BROWSER == "edge":
        options = webdriver.EdgeOptions()
        service = webdriver.EdgeService(DRIVER_PATH) if DRIVER_PATH else None
    else:
        options = webdriver.ChromeOptions()
        service = webdriver.ChromeService(DRIVER_PATH) if DRIVER_PATH else None
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,900")
    # убираем всплывающее окно браузера про пароли — оно мешает кликам
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    if BROWSER == "edge":
        driver = webdriver.Edge(options=options, service=service)
    else:
        driver = webdriver.Chrome(options=options, service=service)
    yield driver
    driver.quit()


# при падении теста сохраняем скриншот в screenshots/<имя_теста>.png
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            driver.save_screenshot(f"screenshots/{item.name}.png")
