from seleniumwire import webdriver  # Import Selenium Wire WebDriver
import time
# Cấu hình proxy
proxy = {
    'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225'
}

# Cấu hình Selenium Wire
options = {
    'proxy': {
        'https': proxy['https'],
    }
}

# Khởi tạo WebDriver với Selenium Wire
driver = webdriver.Chrome(seleniumwire_options=options)

# Thử truy cập một trang web
driver.get("https://httpbin.org/ip")  # Trang web để kiểm tra IP

# In kết quả IP
print(driver.page_source)

time.sleep(500000)
# Đóng trình duyệt
# driver.quit()
