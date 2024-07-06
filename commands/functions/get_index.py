from const import *
from faker import Faker
fake = Faker(locale='en_US')

data = None
driver = None
def login():
    global driver
    global data
    try:
        data = {
            "username" : "7577125653",
            "password" : "ALiGyP4@",
            "phone_send": fake.phone_number(),
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
        'port': generate_random_port(),
        'disable_encoding': True
    
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
        service_log_path=os.path.devnul  # Chuyển hướng log của ChromeDriver
    )
    try: 
        driver.get("https://app.getindex.com/login")
    except Exception as e:
        # làm lại
        return
    
    WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.ID, 'ion-input-0')))
    inputs = driver.find_elements(By.ID,value= "input")
    time.sleep(5000)
    inputs[0].send_keys(data["username"])
    inputs[1].send_keys(data["password"])
    
    driver.find_element(By.TAG_NAME,value= "button").click()
    time.sleep(5)
    
login()