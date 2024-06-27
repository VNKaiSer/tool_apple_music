from const import *
from faker import Faker
fake = Faker()
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

# Định nghĩa các element cho dễ bảo trì 
IFRAME_AUTH = '#aid-auth-widget-iFrame'
ID_USERNAME = 'account_name_text_field'
ID_PASSWORD = 'password_text_field'
ID_QUESTION_1 = 'question-1'
ANSWER1 = 'input'
ID_QUESTION_2 = 'question-2'
BTN_CONTINUTE_AT_QUESTION = 'button'
IF_REPAIR = "#repairFrame"
BTN_CHANGE_PASS = '//*[@id="root"]/div[3]/main/div/div[2]/div[1]/div/div/div/div[2]/div/button'
class Question:
    SCHOOL = 'What is the first name of your best friend in high school?'
    PARENT = 'In what city did your parents meet?'
data = None
driver = None
def login_apple_id():
    global driver
    global data
    try:
        data = {
            "email" : "wemeclom@hotmail.com",
            "password" : "A5YSYjNjU44@",
            "question" : {
                "school" : "bpjwdn",
                "dream" : "fn1h",
                "parent" : "fih2c"
            }
        }
        print(data)
    
    except:
        print("error")
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
    # {
    #     'proxy':  
    #         {
    #             'http': f'socks5://usa.rotating.proxyrack.net:{random_port}',
    #             'https': f'socks5://usa.rotating.proxyrack.net:{random_port}',
    #             'https': f'https://usa.rotating.proxyrack.net:{random_port}',
    #             'http': f'http://usa.rotating.proxyrack.net:{random_port}',
    #             'no_proxy': 'localhost,127.0.0.1'
    #         },
    #     'port': generate_random_port()
    # }
    ]
    proxy = random.choice(random_proxy)
    
    
    
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--log-level=3')  # Selenium log level
    
    driver = uc.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
        seleniumwire_options=proxy,
        service_log_path=os.path.devnull  # Chuyển hướng log của ChromeDriver
    )
    try: 
        
        
        driver.get("https://appleid.apple.com/sign-in")
        time.sleep(10) 
    except Exception as e:
        # làm lại
        return
    
    try:
        # Tìm frame login
        WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.CSS_SELECTOR, IFRAME_AUTH)))
        ifreame_auth = driver.find_element(By.CSS_SELECTOR, value= IFRAME_AUTH)
        driver.switch_to.frame(ifreame_auth)
        # Nhập tài khoản
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.ID, ID_USERNAME )))
        username = driver.find_element(By.ID,value= ID_USERNAME)
        username.send_keys(data['email'])
        username.send_keys(Keys.ENTER)
        # Nhập mật khẩu 
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.ID, ID_PASSWORD)))
        password = driver.find_element(By.ID,value= ID_PASSWORD)
        password.send_keys(data['password'])
        password.send_keys(Keys.ENTER)
        # Câu hỏi 1
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.ID, ID_QUESTION_1)))
        question_1 = driver.find_element(By.ID,value= ID_QUESTION_1).text
        ansewer_1 = ""
        if question_1 == Question.SCHOOL:
            ansewer_1 = data['question']['school']
        elif question_1 == Question.PARENT:
            ansewer_1 = data['question']['parent']
        else:
            ansewer_1 = data['question']['dream']
        
        # Trả lời 
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.TAG_NAME, ANSWER1)))
        answeres = driver.find_elements(By.TAG_NAME,value= ANSWER1)
        answeres[0].send_keys(ansewer_1)
        # Câu hỏi 2
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.ID, ID_QUESTION_2)))
        question_2 = driver.find_element(By.ID,value= ID_QUESTION_2).text
        ansewer_2 = ""
        if question_2 == Question.SCHOOL:
            ansewer_2 = data['question']['school']
        elif question_2 == Question.PARENT:
            ansewer_2 = data['question']['parent']
        else:
            ansewer_2 = data['question']['dream']
        
        # Trả lời câu hỏi 2
        answeres[1].send_keys(ansewer_2)
        
        # Nhấn nút continute
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.TAG_NAME, BTN_CONTINUTE_AT_QUESTION)))
        btns = driver.find_elements(By.TAG_NAME,value= BTN_CONTINUTE_AT_QUESTION)
        btns[1].click()
        
        # Nhấn các nút rồi tới frame chính
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.CSS_SELECTOR, IF_REPAIR)))
        repairFrame = driver.find_element(By.CSS_SELECTOR,value=IF_REPAIR)
        driver.switch_to.frame(repairFrame)
        # Nhấn nút continute
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.TAG_NAME, "button")))
        btns = driver.find_elements(By.TAG_NAME,value= "button")
        btns[1].click()
        time.sleep(5)
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.TAG_NAME, "button")))
        btns = driver.find_elements(By.TAG_NAME,value= "button")
        btns[1].click()
        time.sleep(5)
        
    except Exception as e:
        # làm lại
        return

def change_password():
    global driver
    global data
    driver.get("https://appleid.apple.com/account/manage")
    # Mở modal thay đổi mật khẩu
    WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.XPATH, BTN_CHANGE_PASS)))
    btns = driver.find_element(By.XPATH,value= BTN_CHANGE_PASS)
    btns.click()
    # Đổi pass
    WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-body")))
    modal_change_pass = driver.find_element(By.CLASS_NAME,value= "modal-body")
    ipunts = modal_change_pass.find_elements(By.TAG_NAME,value= "input")
    newPass = generate_random_password(10)
    ipunts[0].send_keys(data['password'])
    ipunts[1].send_keys(newPass)
    ipunts[2].send_keys(newPass) 
    
    

login_apple_id()
change_password()
time.sleep(10)