from const import *
from faker import Faker
fake = Faker(locale='en_US')

def get_phone_random():
    phone = fake.phone_number()
    return phone.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
data = None
driver = None
def login():
    global driver
    global data
    try:
        data = {
            "username" : "7577125653",
            "password" : "ALiGyP4@",
            "phone_send": get_phone_random(),
        }
        print(data)
    
    except:
        print("error")
    random_port = random.randint(10000, 10249)
    random_proxy = [
    # {
    #     'proxy':  
    #         {
    #             'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
    #             'http': 'http://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
    #             'no_proxy': 'localhost,127.0.0.1'
    #         },
    #     'port': generate_random_port(),
    #     'disable_encoding': True
    
    # },
    # {
    #     'proxy':  
    #         {
    #             'https': f'https://usa.rotating.proxyrack.net:{random_port}',
    #             'http': f'http://usa.rotating.proxyrack.net:{random_port}',
    #             'no_proxy': 'localhost,127.0.0.1'
    #         },
    #     'port': generate_random_port(),
    #     'disable_encoding': True
    
    # },
    {
        'proxy':  
            {
                'https': 'https://adz56789:Zxcv123123=5@gate.dc.smartproxy.com:20000',
                'http': 'http://adz56789@Zxcv123123=5@gate.dc.smartproxy.com:20000',
                'no_proxy': 'localhost,127.0.0.1'
            },
            'mitm_http2': False
    }
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
        driver.get("https://app.getindex.com/login")
    except Exception as e:
        # làm lại
        return
    
    WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
    app_root = driver.find_element(By.TAG_NAME, 'app-root')
    inputs = app_root.find_elements(By.TAG_NAME,value= "input")
    inputs[0].send_keys(data["username"])
    time.sleep(0.5)
    inputs[1].send_keys(data["password"])
    time.sleep(0.5)
    inputs[1].send_keys(Keys.ENTER)
    
    # inputs[0].send_keys(data["username"])
    # inputs[1].send_keys(data["password"])
    
    time.sleep(5)
    WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
    app_root = driver.find_element(By.TAG_NAME, 'app-root')
    WebDriverWait(app_root, WAIT_CHILD).until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
    driver.get("https://app.getindex.com/conversation/empty")
    WebDriverWait(app_root, WAIT_CHILD).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
    app_root = driver.find_element(By.TAG_NAME, 'app-root')
    # Input phone number
    WebDriverWait(app_root, WAIT_CHILD).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
    input_phone = app_root.find_element(By.TAG_NAME,value= "input")
    input_phone.send_keys(data["phone_send"])
    
login()