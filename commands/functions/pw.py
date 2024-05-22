from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import json
def check_region(browser):
    try: 
        browser.get('https://ip-api.com/')
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="codeOutput"]/span[12]')))
        contry_code = browser.find_element(By.XPATH, '//*[@id="codeOutput"]/span[12]').text
        if contry_code != 'US':
            browser.quit()
            return False
        return True
    except Exception as e:
        browser.quit()
        return False
# Cấu hình Selenium Wire
options = {
    'proxy':  
            {
                'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
                'http': 'http://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
                'no_proxy': 'localhost,127.0.0.1'
            }
}

print(check_region(webdriver.Chrome(seleniumwire_options=options)))

