# browserstack_tests.py
import os
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import project as p

options = webdriver.ChromeOptions()
import yaml

def fetch_yaml_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

config_data = fetch_yaml_data('browserstack.yaml')

BROWSERSTACK_USERNAME = config_data['userName']
BROWSERSTACK_ACCESS_KEY = config_data['accessKey']
if not BROWSERSTACK_USERNAME or not BROWSERSTACK_ACCESS_KEY:
    raise RuntimeError("Set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY env vars.")

BS_HUB = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub.browserstack.com/wd/hub"

# Define 5 desired capabilities for 5 parallel runs (mix desktop + mobile)
CAPABILITIES = [
    # Desktop Chrome
    {
        "browserName": "Chrome",
        "browserVersion": "120.0",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "ElPais Opinion - Desktop Chrome",
            "local": False,
        }
    },
    # Desktop Firefox
    {
        "browserName": "Firefox",
        "browserVersion": "120.0",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Monterey",
            "sessionName": "ElPais Opinion - Desktop Firefox",
            "local": False,
        }
    },
    # Edge
    {
        "browserName": "Edge",
        "browserVersion": "120.0",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "ElPais Opinion - Desktop Edge",
            "local": False,
        }
    },
    # iPhone Safari
    {
        "browserName": "Safari",
        "browserVersion": "16.0",
        "bstack:options": {
            "realMobile": True,
            "deviceName": "iPhone 14",
            "osVersion": "16",
            "sessionName": "ElPais Opinion - iPhone Safari",
            "local": False,
        }
    },
    # Android Chrome
    {
        "browserName": "Chrome",
        "browserVersion": "120.0",
        "bstack:options": {
            "realMobile": True,
            "deviceName": "Samsung Galaxy S22",
            "osVersion": "12.0",
            "sessionName": "ElPais Opinion - Android Chrome",
            "local": False,
        }
    },
]

TARGET_URL = "https://elpais.com/opinion/"


def run_test(cap):
    session_name = cap["bstack:options"]["sessionName"]
    try:
        print(f"[{session_name}] Starting session...")

        # Use ChromeOptions for compatibility with Selenium 4
        options = webdriver.ChromeOptions()
        for key, value in cap.items():
            options.set_capability(key, value)

        browser = cap['browserName']
        driver = webdriver.Remote(
            command_executor=BS_HUB,
            options=options
        )

        driver.set_page_load_timeout(6)
        driver.get(TARGET_URL)

        p.first(driver,browser)

        driver.close()

    except Exception as e:
        print(f"[{session_name}] Error:", e)



def main():
    threads = []
    for cap in CAPABILITIES:
        t = threading.Thread(target=run_test, args=(cap,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("All BrowserStack sessions finished.")

if __name__ == "__main__":
    main()
