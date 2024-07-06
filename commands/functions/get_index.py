from const import *
from faker import Faker
fake = Faker(locale='en_US')

def generate_phone_number():
    area_codes = [	205, 251, 256, 334, 659, 938, 907,	480, 520, 
                    602, 623, 928,479, 501, 870,	209, 213, 279, 
                    310, 323, 341, 350, 408, 415, 424, 442, 510, 
                    530, 559, 562, 619, 626, 628, 650, 657, 661, 
                    669, 707, 714, 747, 760, 805, 818, 820, 831, 
                    840, 858, 909, 916, 925, 949, 951, 	303, 719, 
                    720, 970, 983, 203, 475, 860, 959, 239, 305, 321, 
                    352, 386, 407, 448, 561, 656, 689, 727, 754, 772,
                    786, 813, 850, 863, 904, 941, 954, 	229, 404, 470, 
                    478, 678, 706, 762, 770, 912, 943]
    area_code = random.choice(area_codes)
    central_office_code = random.randint(200, 999)
    line_number = random.randint(1000, 9999)
    return str(area_code) + str(central_office_code) + str(line_number)
data = None
driver = None
def login():
    global driver
    global data
    try:
        data = {
            "username" : "7742570324",
            "password" : "ALi4ro5@",
            "phone_send": generate_phone_number(),
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
    
    time.sleep(8)
    WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
    app_root = driver.find_element(By.TAG_NAME, 'app-root')
    WebDriverWait(app_root, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'h1')))
    driver.get("https://app.getindex.com/conversation/empty")
    WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
    app_root = driver.find_element(By.TAG_NAME, 'app-root')
    # Input phone number
    WebDriverWait(app_root, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
    input_phone = app_root.find_element(By.TAG_NAME,value= "input")
    time.sleep(0.2)
    input_phone.send_keys(data["phone_send"])
    time.sleep(0.2)
    input_phone.send_keys(Keys.ENTER)
    print(input_phone.get_attribute('value'))
    while input_phone.get_attribute('value') == '':
        try:
            time.sleep(0.2)
            input_phone.send_keys(data["phone_send"])
            time.sleep(0.2)
            input_phone.send_keys(Keys.ENTER)
            break
        except Exception as e:
            print(e)
            time.sleep(1)
    
    WebDriverWait(app_root, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'textarea')))
    input_message = app_root.find_element(By.TAG_NAME,value= "textarea")
    time.sleep(0.3)
    input_message.send_keys("ALi Check") 
    time.sleep(0.5)
    input_message.send_keys(Keys.ENTER)
    time.sleep(5)
    # Kiểm tra kết trường hợp contact support
    try:
        WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'sc-modal')))
        print('contact support')
    except Exception as e:
        print('No contact support')
        
    # Kiểm tra lỗi not sent text 
    for request in driver.requests:
        if 'https://api.pinger.com/2.2/message' in request.url:
            body = request.response.body
            data = json.loads(body)
            if 'errNo' in data and data['errNo'] is not None:
                errNo = data['errNo']
                print(' Có lỗi not sent text. errNo:', errNo)  # Output: 2205
                break
            else:
                break
            

    
    time.sleep(500)
    
login()