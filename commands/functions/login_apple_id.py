from const import *
from faker import Faker

# Định nghĩa các element cho dễ bảo trì 
IFRAME_AUTH = '#aid-auth-widget-iFrame'
ID_USERNAME = 'account_name_text_field'
ID_PASSWORD = 'password_text_field'
ID_QUESTION_1 = 'question-1'
ID_ANSWER_1 = 'form-textbox-1719221840276-0'
ID_QUESTION_2 = 'question-2'
ID_ANSWER_2 = 'form-textbox-1719221840278-0'
class Question:
    SCHOOL = 'What is the first name of your best friend in high school?'
    PARENT = 'In what city did your parents meet?'
def login_apple_id():
    data = None
    driver = None
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
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.ID, ID_ANSWER_1)))
        answer_1 = driver.find_element(By.ID,value= ID_ANSWER_1)
        answer_1.send_keys(ansewer_1)
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
        
        # Trả lựi 
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.ID, ID_ANSWER_2)))
        answer_2 = driver.find_element(By.ID,value= ID_ANSWER_2)
        answer_2.send_keys(ansewer_2)
        
        
        time.sleep(10) 
    except Exception as e:
        # làm lại
        return

login_apple_id()