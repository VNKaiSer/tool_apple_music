import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
import time

def perform_action_on_tab(driver, tab_index):
    # Chuyển sang tab tương ứng
    driver.switch_to.window(driver.window_handles[tab_index])
    print(f"Tab {tab_index + 1} đang xử lý")

    # Thực hiện tìm kiếm trên Google
    if "google.com" in driver.current_url:
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(f"Selenium Tab {tab_index + 1}")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

# Khởi tạo trình duyệt
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Mở tab đầu tiên
driver.get("https://www.google.com")

# Mở thêm các tab ngẫu nhiên từ 10 đến 20
tab_run = random.randint(10, 20)
for _ in range(1, tab_run):
    driver.execute_script("window.open('https://www.google.com', '_blank');")

# Sử dụng ThreadPoolExecutor để xử lý song song trên các tab
tabs = driver.window_handles
with ThreadPoolExecutor(max_workers=10) as executor:
    for tab_index in range(len(tabs)):
        executor.submit(perform_action_on_tab, driver, tab_index)

# Dừng lại để quan sát (tùy chỉnh thời gian nếu cần)
time.sleep(10)

# Đóng trình duyệt
driver.quit()
