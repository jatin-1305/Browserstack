import os
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import project as p
import concurrent.futures
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

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

TARGET_URL = "https://elpais.com/opinion/"


def run_test(browsers):

    session_name = browsers["name"]
    print(session_name)
    try:
        print(f"[{session_name}] Starting session...")

        options = browsers["options"]
        driver = webdriver.Remote(command_executor=BS_HUB, options=options)

        driver.get(TARGET_URL)

        p.first(driver,session_name)

        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", '
            '"arguments": {"status":"passed", "reason": "Project Scraping completed with Browserstack"}}'
        )

        driver.close()

    except Exception as e:
        print(f"[{session_name}] Error:", e)
        driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", '
                '"arguments": {"status":"failed", "reason": "Error: %s"}}' % str(e)
            )


browsers = [
    {"name": "Chrome-Win11", "options": webdriver.ChromeOptions()},
    {"name": "Edge-Win11", "options": webdriver.EdgeOptions()},
    {"name": "Safari-macOS", "options": webdriver.SafariOptions()},
    {"name": "Chrome-Android", "options": webdriver.ChromeOptions()},
    {"name": "Safari-iPhone", "options": webdriver.SafariOptions()},
]



with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(run_test, browsers)
print("All BrowserStack sessions finished.")

