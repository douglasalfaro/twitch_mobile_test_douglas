import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_mobile_driver(device_name: str):
    # Configure Chrome to emulate a mobile device
    mobile_emulation = {"deviceName": device_name}
    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    # Common stability and CI-friendly flags
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=en-US")

    # Run headless ONLY when running in GitHub Actions (CI)
    if os.getenv("CI"):
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        print("⚙️ Running in CI mode: Chrome is headless")

    # Initialize Chrome with WebDriver Manager (auto installs driver)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.set_page_load_timeout(45)
    return driver
