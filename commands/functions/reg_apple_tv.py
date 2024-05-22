import sys
import seleniumwire.undetected_chromedriver as uc
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import logging
import os
from selenium.webdriver.common.keys import Keys

logging.getLogger('seleniumwire').setLevel(logging.ERROR)

# Cấu hình proxy
proxy = {
    'proxy': {
        'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
        'http': 'http://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
        'no_proxy': 'localhost,127.0.0.1'
    }
}

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--log-level=3')  # Selenium log level

    driver = uc.Chrome(
        options=chrome_options,
        seleniumwire_options=proxy,
        service_log_path=os.path.devnull  # Chuyển hướng log của ChromeDriver
    )
    return driver

driver = create_driver()
driver.get("https://tv.apple.com/login")
time.sleep(10)  # Điều chỉnh thời gian ngủ cho phù hợp với yêu cầu của bạn
try:
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
    iframe_login = driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe')
    driver.switch_to.frame(iframe_login)
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="accountName"]')))
    # Nhập tài khoản
    user_name = driver.find_element(By.XPATH, '//*[@id="accountName"]')
    user_name.send_keys("tandatvo999@gmail.com")
    print(iframe_login.find_elements(By.TAG_NAME, 'button')[0])
    time.sleep(10)
except Exception as e:
    print(e)
    driver.quit()
    sys.exit()
time.sleep(5)
WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe'))    
WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys("123456")
time.sleep(10)
driver.quit()
