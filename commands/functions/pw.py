from seleniumwire import webdriver
import json
def check_region(browser):
    try: 
        browser.get('http://ip-api.com/json/')
        for request in browser.requests:
            if request.response and 'ip-api.com/json' in request.url:
                response_body = request.response.body.decode('utf-8')
                data = json.loads(response_body)
                if data['countryCode'] != 'US':
                    browser.quit()
                    return False
        browser.quit()
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

print(check_region(webdriver.Firefox(seleniumwire_options=options)))

