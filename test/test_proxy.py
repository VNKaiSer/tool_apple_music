import json
import random
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

# IP bạn đã cho trước
expected_ip = "123.456.789.000"  # Thay thế bằng IP bạn muốn kiểm tra

# Proxy của bạn
proxy_address= f'atlas.p.shifter.io:{random.randint(20035,20084)}'

# Thiết lập proxy cho Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--proxy-server={proxy_address}')

# Khởi tạo driver với proxy
driver = webdriver.Chrome(options=chrome_options)

# Mở trang API
driver.get("https://api.ipify.org/?format=json")

# Đợi trang tải xong
time.sleep(2)  # Thay đổi thời gian nếu cần

# Lấy nội dung của thẻ body
body_text = driver.find_element("tag name", "body").text

# Phân tích JSON để lấy IP
ip_data = json.loads(body_text)
current_ip = ip_data['ip']
print(current_ip)
# So sánh IP
if current_ip != expected_ip:
    # Mở Google nếu IP khác
    driver.get("https://www.google.com")
else:
    print(f"IP vẫn là {current_ip}, không mở Google.")

# Đóng driver sau khi xong
driver.quit()
