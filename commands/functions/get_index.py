from const import *
from faker import Faker
fake = Faker(locale='en_US')

def generate_phone_number():
    area_codes = [
        205, 251, 256, 334, 659, 938, 907, 480, 520, 602, 623, 928,
        479, 501, 870, 209, 213, 279, 310, 341, 350, 408, 415,
        424, 442, 510, 530, 559, 562, 619, 626, 628, 650, 657, 661,
        669, 707, 714, 747, 760, 805, 818, 820, 831, 840, 858, 909,
        916, 925, 949, 951, 303, 719, 720, 970, 983, 203, 475, 860,
        959, 239, 305, 321, 352, 386, 407, 448, 561, 656, 689, 727,
        754, 772, 786, 813, 850, 863, 904, 941, 954, 229, 404, 470,
        478, 678, 706, 762, 770, 912, 943
    ]
    area_code = random.choice(area_codes)
    central_office_code = random.randint(200, 999)
    line_number = random.randint(1000, 9999)
    return f"{area_code}{central_office_code}{line_number}"

def getData():
    acc_get = db_instance.get_acc_get_index()
    if acc_get == '':
        return None
    username = acc_get[1]
    password = acc_get[2]
    return username, password

def login():
    data = None
    try:
        tmp = getData()
        if tmp is None:
            print("No acc! Input more acc.")
            return
        
        username, password = tmp
        data = {
            "username": username,
            "password": password,
            "phone_send": generate_phone_number(),
        }
        print(data)
        
        random_port = random.randint(10000, 10249)
        random_proxy = [{
            'proxy': {
                'https': 'https://adz56789:Zxcv123123=5@gate.dc.smartproxy.com:20000',
                'http': 'http://adz56789@Zxcv123123=5@gate.dc.smartproxy.com:20000',
                'no_proxy': 'localhost,127.0.0.1'
            },
            'mitm_http2': False
        }]
        proxy = random.choice(random_proxy)
        
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--log-level=3')  # Selenium log level
        # service=Service(ChromeDriverManager().install()),
        # service.service_log_path = os.path.devnull
        driver = webdriver.Chrome(
            
            options=chrome_options,
            seleniumwire_options=proxy,
            # service_log_path=os.path.devnull  # Chuyển hướng log của ChromeDriver
        )
        
        driver.get("https://app.getindex.com/login")
        
        WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
        app_root = driver.find_element(By.TAG_NAME, 'app-root')
        inputs = app_root.find_elements(By.TAG_NAME, "input")
        inputs[0].send_keys(data["username"])
        time.sleep(0.5)
        inputs[1].send_keys(data["password"])
        time.sleep(0.5)
        inputs[1].send_keys(Keys.ENTER)
        
        # Kiểm tra lỗi đăng nhập
        time.sleep(8)
        for request in driver.requests:
            if 'https://api.pinger.com/2.0/account/username/switchDeviceAndUserAuth' in request.url:
                body = request.response.body
                dataReq = json.loads(body)
                if 'errNo' in dataReq and dataReq['errNo'] is not None:
                    if dataReq['errNo'] == 119:
                        db_instance.result_acc_getindex(username, "sai pass")
                        driver.quit()
                        return
                    if dataReq['errNo'] == 2218:
                        db_instance.result_acc_getindex(username, "NoSub")
                        driver.quit()
                        return

        try:
        # Gửi tin nhắn
            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
            driver.get("https://app.getindex.com/conversation/empty")
            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
            input_phone = driver.find_element(By.TAG_NAME, "input")
            input_phone.send_keys(data["phone_send"])
            input_phone.send_keys(Keys.ENTER)
            
            while input_phone.get_attribute('value') == '':
                time.sleep(1)
                input_phone.send_keys(data["phone_send"])
                time.sleep(0.3)
                input_phone.send_keys(Keys.ENTER)
                break
        except Exception as e:
            db_instance.result_acc_getindex(username, "NoTrial")
            driver.quit()
            return
        
        # Kiểm tra lỗi Nosub 
        
        
        WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'textarea')))
        input_message = driver.find_element(By.TAG_NAME, "textarea")
        time.sleep(1)
        input_message.send_keys("ALi Check")
        time.sleep(0.3)
        input_message.send_keys(Keys.ENTER)
        
        # Kiểm tra trường hợp hỗ trợ
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'sc-modal')))
            sc_modal = driver.find_element(By.TAG_NAME, "sc-modal")
            WebDriverWait(sc_modal, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-title')))
            modal_title = sc_modal.find_element(By.CLASS_NAME, "modal-title")
            print(modal_title.text)
            if modal_title.text == "Well, That Didn't Work...":
                db_instance.result_acc_getindex(username, "Didnt Work")
                driver.quit()
                return
            
            db_instance.result_acc_getindex(username, modal_title.text)
            driver.quit()
            return
        except:
            print('')
        
        # Kiểm tra lỗi không gửi được tin nhắn
        for request in driver.requests:
            if 'https://api.pinger.com/2.2/message' in request.url:
                body = request.response.body
                dataReq = json.loads(body)
                if 'errNo' in dataReq and dataReq['errNo'] is not None:
                    db_instance.result_acc_getindex(username, "no sent text")
                    driver.quit()
                    return
        
        db_instance.result_acc_getindex(username, "done")
        driver.quit()


        
    except Exception as e:
        db_instance.update_rerun_acc_get_index(username)


