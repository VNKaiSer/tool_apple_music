import sys
import seleniumwire.undetected_chromedriver as uc
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import time
import logging
import os
from selenium.webdriver.common.keys import Keys
import random
import string
import datetime
import requests
import json
from commands.functions.reg_apple_id import get_max_card_add
from const import *
logging.getLogger('seleniumwire').setLevel(logging.ERROR)

# Cấu hình proxy
proxy = {
    'proxy': {
        'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
        'http': 'http://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
        'no_proxy': 'localhost,127.0.0.1'
    }
}
from faker import Faker
fake = Faker()
CODE_MAIL = ''
def generate_random_password():
    while True:
        password = fake.password(length=10, special_chars=False, upper_case=True, lower_case=True)
        # Kiểm tra xem có 3 ký tự giống nhau không phân biệt hoa thường
        if has_three_consecutive_characters(password):
            continue  # Tạo mật khẩu mới nếu có
        else:
            return 'A' + password + '@'  # Trả về mật khẩu nếu không có 3 ký tự giống nhau

def has_three_consecutive_characters(password):
    # Chuyển đổi mật khẩu thành chữ thường để so sánh không phân biệt hoa thường
    password = password.lower()
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            return True
    return False

def generate_name(length):
    random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    letter = random_string.capitalize()
    
    return letter

def generate_random_date_of_birth():
    day = str(random.randint(1, 28)).zfill(2)  
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(1904, datetime.datetime.now().year - 18))  
    
    date_of_birth = month + day + year
    print(date_of_birth)
    return date_of_birth

def random_data():
    password = generate_random_password()
    frist_name = generate_name(5)
    last_name = generate_name(5)
    date_of_birth = generate_random_date_of_birth()
    return frist_name, last_name, date_of_birth,password

def random_address():
    json_file = './assets/data/addresses.json'  
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Lấy danh sách các địa chỉ từ khóa 'addresses'
    addresses = data.get('addresses', [])

    # Lựa chọn ngẫu nhiên một địa chỉ từ danh sách
    while True:
        random_address = random.choice(addresses)
        # Kiểm tra xem có bất kỳ trường nào bị thiếu không
        if all(key in random_address for key in ['address1', 'address2', 'city', 'state', 'postalCode']):
            break  # Nếu không thiếu trường nào, thoát khỏi vòng lặp

    return random_address['address1'], random_address['address2'], random_address['city'], random_address['state'], random_address['postalCode']

def generate_random_email():
        # time.sleep(3)
        # mail_wait = db_instance.get_mail_wait()
        # if mail_wait is not None:
        #     print(mail_wait)
        #     db_instance.update_data(table_name="mail_reg_apple_music_wait", set_values={"status": "N"}, condition=f"mail = '{mail_wait[0][1]}'")
        #     return mail_wait[0],'wait'
        # else:
            while True:
                thue_mail_url = 'https://api.sptmail.com/api/otp-services/gmail-otp-rental?apiKey=CMFI1WCKSY339AIA&otpServiceCode=apple'
                response = requests.get(thue_mail_url)
                print(response.json())
                # if response.json()['message'] == 200:
                if response.status_code == 200:
                    response_data = response.json()
                    return response_data['gmail'], 'rent'
                time.sleep(20) 
def getOTP(gmail):
    while True:
        thue_mail_url = f'https://api.sptmail.com/api/otp-services/gmail-otp-lookup?apiKey=CMFI1WCKSY339AIA&otpServiceCode=apple&gmail={gmail}'
        response = requests.get(thue_mail_url)
        resp = response.json()
        if resp['status'] == 'PENDING':
            time.sleep(5)
        if resp['status'] == 'SUCCESS':
            return resp['otp']
    
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

# tạo data 
first_name, last_name, date_of_birth, password = random_data()
data = None
address1, address2, city, state, postalCode = random_address()
type_mail = None
try:
    # mail, type_mail = generate_random_email()
    # if type_mail == 'wait':
    #     password = mail[2]
    #     mail = mail[1]   
    
    
    data = {
        "first_name": first_name,
        "account": "santanaevan098@gmail.com",
        "type": "rent",
        "password": "A9aYJJpjWtX@",
        # "password": password,
        "last_name": last_name,
        "date_of_birth": date_of_birth,
        "address1": address1,
        "address2": address2,
        "city": city,
        "state": state,
        "postalCode": postalCode
    }
    print(data)
    # Ngăn mail wait chạy nhiều tab
    # if type_mail == 'wait':
    #     db_instance.update_data(table_name="mail_reg_apple_music_wait", condition=f"mail = '{mail}'", set_values={"status": "N"})
    
except:
    print("error")

driver = create_driver()
driver.get("https://tv.apple.com/login")
time.sleep(10) 
try:
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
    iframe_login = driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe')
    driver.switch_to.frame(iframe_login)
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="accountName"]')))
    # Nhập tài khoản
    user_name = driver.find_element(By.XPATH, '//*[@id="accountName"]')
    user_name.send_keys(data['account'])
    user_name.send_keys(Keys.ENTER)
    
    active = driver.switch_to.active_element
    active.send_keys(Keys.ENTER)
    time.sleep(10)
except Exception as e:
    print(e)
    driver.quit()
    sys.exit()

# Điền dữ liệu với frame
try: 
    driver.switch_to.default_content()
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe'))
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
    input_elements = driver.find_elements(By.TAG_NAME, 'input')
    input_elements[1].send_keys(password)
    input_elements[2].send_keys(first_name)
    input_elements[3].send_keys(last_name)
    for i in date_of_birth:
        input_elements[4].send_keys(i)
        time.sleep(0.2)
    input_elements[-1].click()
    driver.find_elements(By.TAG_NAME, 'button')[1].click()
    
    # Nhập code OTP
    CODE_MAIL = getOTP(data["account"])
    driver.switch_to.active_element.send_keys(CODE_MAIL)
    time.sleep(10)
except Exception as e: # chưa login nằm ở đây
    print("Xữ lý login")
    # driver.switch_to.default_content()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="aid-auth-widget-iFrame"]')))
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="aid-auth-widget-iFrame"]'))
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
    input_login = driver.find_elements(By.TAG_NAME, 'input')
    input_login[1].send_keys(data['password'])
    driver.find_elements(By.TAG_NAME, 'button')[0].click()
    

# Nhấn nút continute nếu lần đầu login
try:
    driver.switch_to.default_content()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe'))
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'button')))
    driver.find_element(By.TAG_NAME, 'button').click()
    print('Click nhầm')
    time.sleep(10)
except Exception as e:
    print(e)
    # driver.quit()
    # sys.exit()
    
try: 
    driver.switch_to.default_content()
    # Đổi vào https://tv.apple.com/settings thêm thẻ 
    driver.get("https://tv.apple.com/settings")
    # Đổi sang nút chang payment
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe'))
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button')))
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button').click()
    # Nhấn nút add payment
    driver.switch_to.default_content()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe'))
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/div[2]/button')))
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/div[2]/button').click()
except Exception as e:
    print(e)
    driver.quit()
    sys.exit()

# Thêm thẻ 
#1. Điền thông tin trên thẻ
try: 
    driver.switch_to.default_content()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ck-modal"]/iframe')))
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ck-modal"]/iframe'))
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
    input_elements = driver.find_elements(By.TAG_NAME, 'input')
    input_elements[8].send_keys(data['postalCode'])
    input_elements[7].send_keys(data['city'])
    input_elements[6].send_keys(data['address2'])
    input_elements[5].send_keys(data['address1'])
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "addressOfficialStateProvince")))
    select = Select(driver.find_element(By.ID, "addressOfficialStateProvince"))
    select.select_by_value(data["state"])
except Exception as e:
    print(e)
    driver.quit()
    sys.exit()
while run_add_card:
    wait = WebDriverWait(driver, 15)
    data_card = db_instance.fetch_data(table_name="pay", columns=["*"], condition="status = 1 and on_use = 0 limit 1")
    # print(data_card[0])
    db_instance.update_data(table_name="pay", set_values={"on_use": 1},condition=f'id = {data_card[0][0]}')
    # print(data_card[0])
    try:
        if data_card[0] is None:
            logging.error("Error: %s", str("Hết thẻ"))
            sys.exit() # Dừng chương trình
    except IndexError:
        logging.error("Error: %s", str("Hết thẻ"))
        driver.quit()
        sys.exit()
        
    # Kiểm tra thẻ hiện tại đã max chưa
    if data_card[0][6] >= get_max_card_add():
        db_instance.update_data(table_name="pay", set_values={"status": 0},condition=f'id = {data_card[0][0]}')
        continue
    card = Card(data_card[0][1], data_card[0][2]+""+ data_card[0][3], data_card[0][4])
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditCardNumber"]')))
        card_number_element = driver.find_element(By.XPATH,'//*[@id="creditCardNumber"]')
        card_number_element.clear()
    except Exception as e:
        db_instance.insert_mail_wait(mail_wait=data['account'], password=data['password'],code_old= CODE_MAIL)
        driver.quit()
    for i in card.get_card_number():
        card_number_element.send_keys(i)
        time.sleep(0.2)
# driver.find_element(By.XPATH,'//*[@id="creditCardNumber"]').send_keys("")

    wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]')))
    card_expiration_element = driver.find_element(By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]')
    card_expiration_element.clear()
    for i in card.get_card_expiration():
        card_expiration_element.send_keys(i)
        time.sleep(0.2)
# driver.find_element(By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]').send_keys("")

    wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditVerificationNumber"]')))
    card_ccv_element = driver.find_element(By.XPATH,'//*[@id="creditVerificationNumber"]')
    card_ccv_element.clear()
    for i in card.get_card_ccv():
        card_ccv_element.send_keys(i)
        time.sleep(0.2)
    time.sleep(2)
# driver.find_element(By.XPATH,'//*[@id="creditVerificationNumber"]').send_keys("658")
    driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[3]/div/button').click()
# Kiểm tra các trường hợp lỗi của thẻ 
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal")))
        add_payment_result = driver.find_element(By.CSS_SELECTOR, ".camk-modal-description")
        print(add_payment_result.text)
        match add_payment_result.text:
            case tool_exception.DISSABLE:
                # logging.error("Error Account: Id - %s", str(data[0][1] +" - "+"Account is disable"))
                # db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "Diss"}, condition=f"id = {data[0][0]}")
                run_add_card = False # Dừng vì account bị disable
                driver.quit()
            case tool_exception.MANY:
                # logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is many account add"))
                db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "To Many ID"}, condition=f"id = {data_card[0][0]}")
                wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                time.sleep(2)
                continue
            case tool_exception.INVALID_CARD:
            # Thông tin thẻ sai
                logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is invalid"))
                db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Invalid Card"}, condition=f"id = {data_card[0][0]}")
                wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                time.sleep(2)
                continue
            case tool_exception.SUPPORT:
                # logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is support"))
                db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "contact suport"}, condition=f"id = {data_card[0][0]}")
                # wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                # driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                # time_ctsp = time_ctsp + 1
                # if time_ctsp == 2:
                driver.quit()
                
            case tool_exception.DIE:
                # logging.error("Die Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is die"))
                db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {data_card[0][0]}")
                wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                time.sleep(2)
                continue
            case tool_exception.ACC_SPAM:
                # logging.error("Error Account: Id - %s", str(data[0][1] +" - "+"Account is spam"))
                # db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "add sup"}, condition=f"id = {data[0][0]}")
                db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "add sup"}, condition=f"id = {data_card[0][0]}")
                db_instance.insert_mail_wait(mail_wait=data['account'], password=data['password'], code_old=CODE_MAIL)
                run_add_card = False
                driver.quit()
                # continue
            case tool_exception.ISSUE_METHOD:
                # logging.error("Error Card: Id - %s", str(data_card[0][1] +" - "+"Card Die"))
                db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {data_card[0][0]}")
                wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                time.sleep(2)
                continue
            case tool_exception.DEC:
                logging.error("Error Card: Id - %s", str(data_card[0][1] +" - "+"Card DEC"))
                db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {data_card[0][0]}")
                wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                time.sleep(2)
                continue
            case tool_exception.DECLINED:
                logging.error("Error Card: Id - %s", str(data_card[0][1] +" - "+"Card DEC"))
                # db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {data_card[0][0]}")
                wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                time.sleep(2)
                continue
            case _:
                logging.error("Error Card: Lỗi không xác định - %s", str(add_payment_result.text))
    except NoSuchElementException as e:
        logging.error("Error Card: Thông tin thẻ không hợp lệ - %s")
        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Invalid Card"}, condition=f"id = {data_card[0][0]}")
        continue
    # wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
    # driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()

    except Exception as e: # Không có thông báo. => Add thẻ thành công
        run_add_card = False
        db_instance.update_data(table_name="pay", set_values={"number_use": data_card[0][6]+1}, condition=f"id = {data_card[0][0]}")
        db_instance.update_data(table_name="pay", set_values={"on_use": 0}, condition=f"id = {data_card[0][0]}")
        # if data['type'] == 'wait':
        #     db_instance.update_data(table_name="mail_reg_apple_music_wait", set_values={"status": "Y"}, condition=f"mail = '{data['account']}'")
        data['card_number'] = card.get_card_number()
        data['month_exp'] = data_card[0][2]
        data['year_exp'] = data_card[0][3]
        data['ccv'] = card.get_card_ccv()
        break
time.sleep(1000)

    
        




