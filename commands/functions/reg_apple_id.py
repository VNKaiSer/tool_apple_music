from const import *
import random
import string
import datetime
import time
import requests
import json
import random
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.service import Service
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

def generate_random_email():
        time.sleep(3)
        mail_wait = db_instance.get_mail_wait()
        if mail_wait is not None:
            print(mail_wait)
            db_instance.update_data(table_name="mail_reg_apple_music_wait", set_values={"status": "N"}, condition=f"mail = '{mail_wait[0][1]}'")
            return mail_wait[0],'wait'
        else:
            while True:
                thue_mail_url = 'https://api.sptmail.com/api/otp-services/gmail-otp-rental?apiKey=CMFI1WCKSY339AIA&otpServiceCode=apple'
                response = requests.get(thue_mail_url)
                print(response.json())
                # if response.json()['message'] == 200:
                if response.status_code == 200:
                    response_data = response.json()
                    return response_data['gmail'], 'rent'
                time.sleep(20) 
                
def generate_random_port():
    return random.randint(49152, 65535)
def get_max_card_add():
    f = open ('./config/tool-config.json', "r")
    data = json.loads(f.read())
    f.close()
    return data['TIME_ADD_CARD']

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

def getOTP(gmail):
    while True:
        thue_mail_url = f'https://api.sptmail.com/api/otp-services/gmail-otp-lookup?apiKey=CMFI1WCKSY339AIA&otpServiceCode=apple&gmail={gmail}'
        response = requests.get(thue_mail_url)
        resp = response.json()
        if resp['status'] == 'PENDING':
            time.sleep(5)
        if resp['status'] == 'SUCCESS':
            return resp['otp']
def click_first_login(browser):
    
    browser.get("https://music.apple.com/us/account/settings")
    time.sleep(5)
    WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')))
    iframe_hello = browser.find_element(By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')
    browser.switch_to.frame(iframe_hello)
    WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div[5]/button')))
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div[5]/button').click()
    time.sleep(5)
    browser.switch_to.default_content()
    browser.get("https://music.apple.com/us/account/settings")
    
def apple_id_done(browser, data):
    browser.get("https://appleid.apple.com/sign-in")
    time.sleep(10)
    try: 
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#aid-auth-widget-iFrame")))
        iframe_login = browser.find_element(By.CSS_SELECTOR, "#aid-auth-widget-iFrame")
        browser.switch_to.frame(iframe_login)
        
        wait = WebDriverWait(browser, 15)
        wait.until(EC.visibility_of_element_located((By.ID, "account_name_text_field")))
        browser.find_element(By.ID, "account_name_text_field").send_keys(data['account'])
        time.sleep(3)
        browser.switch_to.active_element.send_keys(Keys.ENTER)
        browser.switch_to.default_content()
        browser.switch_to.frame(iframe_login)
        wait.until(EC.visibility_of_element_located((By.ID, "password_text_field")))
        browser.find_element(By.ID, "password_text_field").send_keys(data['password'])
        time.sleep(3)
        browser.switch_to.active_element.send_keys(Keys.ENTER)
    except Exception as e:
        db_instance.insert_mail_wait(data["account"], data["password"])
        browser.quit()
        return
    time.sleep(5)
    browser.switch_to.default_content()
    active_element = browser.switch_to.active_element
    # otp = getOTP(data['account'])
    global CODE_MAIL
    otp = '*'
    if data['type'] == 'wait':
        otp = db_instance.get_code_old(data["account"])
    print('Code mail old: ', otp)
    while True:
        otp = getOTP(data['account'])
        if CODE_MAIL != otp:
            print('Code mail: ',otp)
            break
    # time.sleep(5)
    active_element.send_keys(otp)
    time.sleep(5)
    active_element.send_keys(Keys.TAB)
    active_element.send_keys(data['ccv'])
    time.sleep(5)
    active_element.send_keys(Keys.ENTER)
    # Nếu không được thì nhấn 1 lần nữa 
    time.sleep(5)
    
    try:
       active_element.clear()
       active_element.send_keys(data['ccv'])
       active_element.send_keys(Keys.ENTER)
    except requests.exceptions.TooManyRedirects:
        db_instance.insert_mail_wait(data["account"], data["password"]) 
        browser.quit()
        return
    except requests.exceptions.RequestException as e:
        db_instance.insert_mail_wait(data["account"], data["password"]) 
        browser.quit()
    except Exception as e:
        print(e) # Không còn nút đó 
    # Chuỗi ngày tháng năm ban đầu
    
    db_instance.insert_mail_reg_apple_music([data['account'], data['password'], data['card_number'], data['month_exp'], data['year_exp'], data['ccv'], data['date_of_birth']])
    # Lưuvào db 
    #OTP xong
    browser.quit()

def check_account_is_block(browser):
    try:
        browser.switch_to.default_content()
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR,  "#ck-container > iframe")))
        iframe = browser.find_element(By.CSS_SELECTOR, value= "#ck-container > iframe")
        browser.switch_to.frame(iframe)
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#aid-auth-widget-iFrame')))
        iframe_auth = browser.find_element(By.CSS_SELECTOR, value= "#aid-auth-widget-iFrame")
        browser.switch_to.frame(iframe_auth)
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        text = browser.find_elements(By.TAG_NAME, 'h2')[0].text
        print(text)
        if text:
            return True
        else:
            return False
    except Exception as e:
            print(e)
            return False
        
def process_login(browser, data, add, apple):
    browser.switch_to.default_content()
    try:
        active_element = browser.switch_to.active_element
        active_element.send_keys(data['password'])
        active_element.send_keys(Keys.ENTER)
        time.sleep(10)
        try:
            if check_account_is_block(browser):
                # logging.error("Error Account: Id -  %s", str(data[0][1] +" "+tool_exception.LOCK))
                # db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "UnLock"}, condition=f"id = {data[0][0]}")
                browser.quit()
                return
        except Exception as e: # Không có lỗi bị block
            print('')
        # browser.get("https://music.apple.com/us/account/settings")
        # Trường hợp lần đầu đăng kí 
        try: 
            browser.switch_to.default_content()
            WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ck-container > iframe:nth-child(1)')))
            iframe_hello = browser.find_element(By.CSS_SELECTOR, '#ck-container > iframe:nth-child(1)')
            browser.switch_to.frame(iframe_hello)
            print(iframe_hello);
            print(len(browser.find_elements(By.TAG_NAME, 'button')))
            WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div[5]/button')))
            browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div[5]/button').click()
            time.sleep(3)
            browser.switch_to.default_content()
            
            browser.get("https://music.apple.com/us/account/settings")
        except Exception as e:
            print("170")
            print(e)
        
        browser.get("https://music.apple.com/us/account/settings")
        if add == True:
            add_payment(browser, data, apple)
        db_instance.insert_mail_reg_apple_music_not_add([data['account'], data['password'],data['date_of_birth']])
        browser.quit()
    except requests.exceptions.TooManyRedirects:
        db_instance.insert_mail_wait(data["account"], data["password"]) 
        browser.quit()
        return 
    except requests.exceptions.RequestException as e:
        db_instance.insert_mail_wait(data["account"], data["password"]) 
        browser.quit()
        return
    except Exception as e:
        db_instance.insert_mail_wait(data['account'], data['password'])
        browser.quit()
        return


def add_payment(browser, data, apple):
    global CODE_MAIL
    try: 
        wait = WebDriverWait(browser, 15)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
        iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_setting)
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li')))
        country = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li').text
        print(country)
        if country != "United States":
            print("Not US") 
    except Exception as e:
        db_instance.insert_mail_wait(data['account'], data['password'], CODE_MAIL)
        browser.quit()
        return
        # Kiểm tra đã add thẻ chưa 
    try: 
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[1]')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[1]').text
        print('Đã add')
        browser.quit()
        return
    except Exception as e:
        print('chưa add')
    # click nút manage payment 
    try: 
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button').click()
        time.sleep(10)
        browser.switch_to.default_content()
        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[4]/main/div/div/iframe")))
        iframe_payment = browser.find_element(By.XPATH, "/html/body/div/div[4]/main/div/div/iframe")
        browser.switch_to.frame(iframe_payment)
        # except Exception as e:
        #     browser.get("https://music.apple.com/us/account/settings")
        #     wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button')))
        #     browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button').click()
        #     time.sleep(10)
        #     browser.switch_to.default_content()
        #     wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[4]/main/div/div/iframe")))
        #     iframe_payment = browser.find_element(By.XPATH, "/html/body/div/div[4]/main/div/div/iframe")
        #     browser.switch_to.frame(iframe_payment)
        # Nhấn nút add payment
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/button')))
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/button').click()
        browser.switch_to.default_content()
        iframe_add_payment = browser.find_element(By.CSS_SELECTOR, "#ck-container > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_add_payment)
        
        wait.until(EC.visibility_of_element_located((By.ID, "addressOfficialLineFirst")))
        address_1 = browser.find_element(By.ID, "addressOfficialLineFirst")
        for i in data["address1"]:
            address_1.send_keys(i)
            time.sleep(0.1)
        wait.until(EC.visibility_of_element_located((By.ID, "addressOfficialLineSecond")))
        address_2 = browser.find_element(By.ID, "addressOfficialLineSecond")
        for i in data["address2"]:
            address_2.send_keys(i)
            time.sleep(0.1)
        
        wait.until(EC.visibility_of_element_located((By.ID, "addressOfficialCity")))
        city_element = browser.find_element(By.ID, "addressOfficialCity")
        for i in data["city"]:
            city_element.send_keys(i)
            time.sleep(0.1)
        wait.until(EC.visibility_of_element_located((By.ID, "addressOfficialStateProvince")))
        select = Select(browser.find_element(By.ID, "addressOfficialStateProvince"))
        select.select_by_value(data["state"])
        wait.until(EC.visibility_of_element_located((By.ID, "addressOfficialPostalCode")))
        post_code = browser.find_element(By.ID, "addressOfficialPostalCode")
        for i in data["postalCode"]:
            post_code.send_keys(i)
            time.sleep(0.1)
    except Exception as e: # không tìm form add thẻ
        browser.quit()
        return
    
    run_add_card = True
    time_ctsp = 0
    while run_add_card:
        
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
            browser.quit()
            sys.exit()
         
        # Kiểm tra thẻ hiện tại đã max chưa
        if data_card[0][6] >= get_max_card_add():
            db_instance.update_data(table_name="pay", set_values={"status": 0},condition=f'id = {data_card[0][0]}')
            continue
        card = Card(data_card[0][1], data_card[0][2]+""+ data_card[0][3], data_card[0][4])
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditCardNumber"]')))
            card_number_element = browser.find_element(By.XPATH,'//*[@id="creditCardNumber"]')
            card_number_element.clear()
        except Exception as e:
            db_instance.insert_mail_wait(mail_wait=data['account'], password=data['password'],code_old= CODE_MAIL)
            browser.quit()
            return
        for i in card.get_card_number():
            card_number_element.send_keys(i)
            time.sleep(0.2)
    # browser.find_element(By.XPATH,'//*[@id="creditCardNumber"]').send_keys("")

        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]')))
        card_expiration_element = browser.find_element(By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]')
        card_expiration_element.clear()
        for i in card.get_card_expiration():
            card_expiration_element.send_keys(i)
            time.sleep(0.2)
    # browser.find_element(By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]').send_keys("")

        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditVerificationNumber"]')))
        card_ccv_element = browser.find_element(By.XPATH,'//*[@id="creditVerificationNumber"]')
        card_ccv_element.clear()
        for i in card.get_card_ccv():
            card_ccv_element.send_keys(i)
            time.sleep(0.2)
        time.sleep(2)
    # browser.find_element(By.XPATH,'//*[@id="creditVerificationNumber"]').send_keys("658")
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/button').click()
    # Kiểm tra các trường hợp lỗi của thẻ 
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal")))
            add_payment_result = browser.find_element(By.CSS_SELECTOR, ".camk-modal-description")
            print(add_payment_result.text)
            match add_payment_result.text:
                case tool_exception.DISSABLE:
                    # logging.error("Error Account: Id - %s", str(data[0][1] +" - "+"Account is disable"))
                    # db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "Diss"}, condition=f"id = {data[0][0]}")
                    run_add_card = False # Dừng vì account bị disable
                    browser.quit()
                    return
                case tool_exception.MANY:
                    logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is many account add"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "To Many ID"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    time.sleep(2)
                    continue
                case tool_exception.INVALID_CARD:
                # Thông tin thẻ sai
                    logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is invalid"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Invalid Card"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    time.sleep(2)
                    continue
                case tool_exception.SUPPORT:
                    # logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is support"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "contact suport"}, condition=f"id = {data_card[0][0]}")
                    # wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    # browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    # time_ctsp = time_ctsp + 1
                    # if time_ctsp == 2:
                    browser.quit()
                    return
                case tool_exception.DIE:
                    logging.error("Die Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is die"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    time.sleep(2)
                    continue
                case tool_exception.ACC_SPAM:
                    # logging.error("Error Account: Id - %s", str(data[0][1] +" - "+"Account is spam"))
                    # db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "add sup"}, condition=f"id = {data[0][0]}")
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "add sup"}, condition=f"id = {data_card[0][0]}")
                    db_instance.insert_mail_wait(mail_wait=data['account'], password=data['password'], code_old=CODE_MAIL)
                    run_add_card = False
                    browser.quit()
                    return
                    # continue
                case tool_exception.ISSUE_METHOD:
                    logging.error("Error Card: Id - %s", str(data_card[0][1] +" - "+"Card Die"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    time.sleep(2)
                    continue
                case tool_exception.DEC:
                    logging.error("Error Card: Id - %s", str(data_card[0][1] +" - "+"Card DEC"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    time.sleep(2)
                    continue
                case tool_exception.DECLINED:
                    logging.error("Error Card: Id - %s", str(data_card[0][1] +" - "+"Card DEC"))
                    # db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    time.sleep(2)
                    continue
                case _:
                    logging.error("Error Card: Lỗi không xác định - %s", str(add_payment_result.text))
        except NoSuchElementException as e:
            logging.error("Error Card: Thông tin thẻ không hợp lệ - %s")
            db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Invalid Card"}, condition=f"id = {data_card[0][0]}")
            continue
        # wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
        # browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()

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
    # Tiến hành hoàn thành
    if apple == True:
        apple_id_done(browser, data)
    else:
        db_instance.insert_mail_reg_apple_music([data['account'], data['password'], data['card_number'], data['month_exp'], data['year_exp'], data['ccv'], data['date_of_birth']])
        browser.quit()
        return

        
def reg_apple_music(add, apple):
    global RUN_APP
    if RUN_APP == False:
        return 
    
    first_name, last_name, date_of_birth, password = random_data()
    data = None
    address1, address2, city, state, postalCode = random_address()
    type_mail = None
    try:
        mail, type_mail = generate_random_email()
        if type_mail == 'wait':
            password = mail[2]
            mail = mail[1]   
        
        
        data = {
        "first_name": first_name,
        "account": mail,
        "type": type_mail,
        "password": password,
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
        browser.quit()
        return
    
    random_port = random.randint(9000, 9050)
    random_proxy = [
    {
        'proxy':  
            {
                'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
                'http': 'http://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
                'no_proxy': 'localhost,127.0.0.1'
            },
        'port': generate_random_port()
    
    },
    {
        'proxy':  
            {
        'http': f'socks5://usa.rotating.proxyrack.net:{random_port}',
        'https': f'socks5://usa.rotating.proxyrack.net:{random_port}',
        'https': f'https://usa.rotating.proxyrack.net:{random_port}',
        'http': f'http://usa.rotating.proxyrack.net:{random_port}',
                'no_proxy': 'localhost,127.0.0.1'
            },
        'port': generate_random_port()
    }
    ]
    option = random.choice(random_proxy)
    
    global USE_PROXY
    if USE_PROXY == True:
        browser = webdriver.Firefox(
            seleniumwire_options=option
            
        )
    else: 
        browser = webdriver.Firefox(
            seleniumwire_options={
                'port': generate_random_port()
            }
        )
    if check_region(browser) == False:
        browser.quit()
        return
    # vào web 
    try:
        browser.get('https://music.apple.com/us/login')
        wait = WebDriverWait(browser, 30)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,  "#ck-container > iframe")))
        iframe = browser.find_element(By.CSS_SELECTOR, value= "#ck-container > iframe")
        browser.switch_to.frame(iframe)
        
        #Nhập account name
        wait.until(EC.visibility_of_element_located((By.ID, "accountName")))
        inputAccount = browser.find_element(By.ID, "accountName")
        inputAccount.send_keys(data["account"])
        
        # Nhấn nút login
        browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div[3]/button").click()
        # time.sleep(10)
        # WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#aid-auth-widget-iFrame")))
        # iframe_auth = browser.find_element(By.CSS_SELECTOR, "#aid-auth-widget-iFrame")
        # browser.switch_to.frame(iframe_auth)
    except Exception as e: # Trang apple load chậm
        db_instance.insert_mail_wait(data["account"], data["password"])
        browser.quit()
        return
        
    time.sleep(5) # Đợi 5s

    # Kiểm tra login 
    try: 
        browser.switch_to.default_content()
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[5]/iframe")))
        iframe_register = browser.find_element(By.XPATH, "/html/body/div/div[5]/iframe")
        browser.switch_to.frame(iframe_register)
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.ID, "acAccountPassword")))
        
        browser.find_element(By.ID, "acAccountPassword").send_keys(data["password"])
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.ID, "firstName")))
        browser.find_element(By.ID, "firstName").send_keys(data["first_name"])
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.ID, "lastName")))
        browser.find_element(By.ID, "lastName").send_keys(data["last_name"])
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.ID, "birthday")))
        birth = browser.find_element(By.ID, "birthday")
        
        for i in data["date_of_birth"]:
            time.sleep(0.2)
            birth.send_keys(i)
        # WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'form-checkbox create-account-v2__checkbox')))
        
        inputs = browser.find_elements(By.TAG_NAME, "input")
        # print(inputs[inputs.__len__()-1].get_attribute("id"))
        inputs[inputs.__len__()-1].click()   
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/button[2]")))
        browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/button[2]").click()
    except requests.exceptions.TooManyRedirects:
        db_instance.insert_mail_wait(data["account"], data["password"]) 
        browser.quit()
        return
    except requests.exceptions.RequestException as e:
        db_instance.insert_mail_wait(data["account"], data["password"]) 
        browser.quit()
        return
    except Exception as e:
        print('Đã login')
        if data['type'] == 'wait':
            db_instance.update_data(table_name="mail_reg_apple_music_wait", set_values={"status": "N"}, condition=f"mail = '{data['account']}'")
        try: 
            process_login(browser, data, add, apple)
        
        except Exception as e:
            # print(e)
            browser.quit()
            db_instance.update_data(table_name="mail_reg_apple_music_wait", set_values={"status": "Y"}, condition=f"mail = '{data['account']}'")
            return
        # db_instance.insert_mail_wait(data["account"], data["password"]) # Đoạn 
        browser.quit()
        return 
    
    try:
        global CODE_MAIL
        CODE_MAIL = getOTP(data["account"])
        # time.sleep(20)
        # otp = getOTP(data["account"])
        active_element = browser.switch_to.active_element
        active_element.send_keys(CODE_MAIL)
        time.sleep(15)
        browser.switch_to.default_content()
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ck-container > iframe:nth-child(1)')))
        iframe_hello = browser.find_element(By.CSS_SELECTOR, '#ck-container > iframe:nth-child(1)')
        browser.switch_to.frame(iframe_hello)
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div[5]/button')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div[5]/button').click()
        time.sleep(3)
        browser.switch_to.default_content()
        browser.get("https://music.apple.com/us/account/settings")
        # time.sleep(3)
    except requests.exceptions.TooManyRedirects:
        print(e)
        db_instance.insert_mail_wait(data["account"], data["password"], CODE_MAIL) 
        browser.quit()
        return
    except requests.exceptions.RequestException as e:
        print(e)
        db_instance.insert_mail_wait(data["account"], data["password"], CODE_MAIL) 
        browser.quit()
        return
    except Exception as e:
        print(e)
        db_instance.insert_mail_wait(data["account"], data["password"], CODE_MAIL) 
        browser.quit()
        return
    
    if add == True:
        add_payment(browser, data, apple)
    else:
        db_instance.insert_mail_reg_apple_music_not_add([data['account'], data['password'], data['date_of_birth']])
        browser.quit()
        return
    