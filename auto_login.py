# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005FE1C685C1D558C13F5A887FD96DD3BC5D8F08B7CD729B28F5B2F3C4849100DA829E750E8109FCBE15F5274CA22E21C3E838ECB4D1F719C2009961F3AE67F1E7FF4FF1F1533946AC9E9571EE737C273F3CA29775C32080DF6C3E3ABE218BBF72B542EE8575138CC13CB75CB44C94C6F60F59FB62DBF4A72AD96B3C1972772451806CD3B3C209D8A98572166A258C4E2A50A66FC773BDF3B6EA6F7830285CC7769FE2AB7CC0ED90CCEFC860E17B40CEE4A560B4A2995EB48DA0CF604B42180202EA1A0541B3940B882F19B43265DF176900DED411F1B967AF039BD26A73E7CB140A014CCE73894F82931DF27B843A5EC2FECA6B642A7B258C58E08877EBA337A9ABDAAF203E8C268ED2603694CC59B36AC76ADB8BD43038DADCE76198430D19EC08E1C230DC85E5E9F1DA508D222DEDF5BF5ABA0A1BFBC756F37F8744205ABED7A54CDD9523E7677F10EB5277C4F4D02CDBE8F2C425B6D56A85E07EE884812A87"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
