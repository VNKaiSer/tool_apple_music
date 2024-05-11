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

def generate_random_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

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
    password = generate_random_password(8)
    frist_name = generate_name(5)
    last_name = generate_name(5)
    date_of_birth = generate_random_date_of_birth()
    return frist_name, last_name, date_of_birth,password

def generate_random_email():
    thue_mail_url = 'https://api.sptmail.com/api/otp-services/gmail-otp-rental?apiKey=CMFI1WCKSY339AIA&otpServiceCode=apple'
    response = requests.get(thue_mail_url)
    print(response.status_code)
    # if response.json()['message'] == 200:
    if response.status_code == 200:
        response_data = response.json()
        return response_data['gmail'] 
    else: 
        return None
    
def random_address():
    json_file = './assets/data/addresses.json'  
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Lấy danh sách các địa chỉ từ khóa 'addresses'
    addresses = data.get('addresses', [])

    # Chọn ngẫu nhiên một địa chỉ từ danh sách
    random_address = random.choice(addresses)
    return random_address['address1'], random_address['address2'], random_address['city'], random_address['state'], random_address['postalCode']

def getOTP(gmail):
    thue_mail_url = f'https://api.sptmail.com/api/otp-services/gmail-otp-lookup?apiKey=CMFI1WCKSY339AIA&otpServiceCode=apple&gmail={gmail}'
    response = requests.get(thue_mail_url)
    print(response.json())
    if response.status_code == 200:
        return response.json()['otp']
    else:
        return None

def reg_apple_music():
    first_name, last_name, date_of_birth, password = random_data()
    data = None
    address1, address2, city, state, postalCode = random_address()
    try:
        data = {
        "first_name": first_name,
        # "account": generate_random_email(),
        "account": "brandtjustice71@gmail.com",
        "password": "Zxcv123123",
        "last_name": last_name,
        "date_of_birth": generate_random_date_of_birth(),
        "address1": address1,
        "address2": address2,
        "city": city,
        "state": state,
        "postalCode": postalCode
        }
        print(data)
    except:
        print("error")
    
    option = {
        'proxy':  
            {
                'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225'
            }
    
    }
    
    browser = webdriver.Firefox(
        seleniumwire_options=option
    )
    
    browser.get('https://music.apple.com/us/login')
    wait = WebDriverWait(browser, 30)
    # vào web 
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,  "#ck-container > iframe")))
        iframe = browser.find_element(By.CSS_SELECTOR, value= "#ck-container > iframe")
        browser.switch_to.frame(iframe)
        
        #Nhập account name
        wait.until(EC.visibility_of_element_located((By.ID, "accountName")))
        inputAccount = browser.find_element(By.ID, "accountName")
        inputAccount.send_keys(data["account"])
        
        # Nhấn nút login
        browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/div/div/div[3]/button").click()
        # time.sleep(10)
        # WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#aid-auth-widget-iFrame")))
        # iframe_auth = browser.find_element(By.CSS_SELECTOR, "#aid-auth-widget-iFrame")
        # browser.switch_to.frame(iframe_auth)
    except Exception as e:
        print(e)
    time.sleep(10)
    browser.switch_to.default_content()
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[5]/iframe")))
    iframe_register = browser.find_element(By.XPATH, "/html/body/div/div[5]/iframe")
    browser.switch_to.frame(iframe_register)
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, "acAccountPassword")))
    browser.find_element(By.ID, "acAccountPassword").send_keys(data["password"])
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, "firstName")))
    browser.find_element(By.ID, "firstName").send_keys(data["first_name"])
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, "lastName")))
    browser.find_element(By.ID, "lastName").send_keys(data["last_name"])
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, "birthday")))
    birth = browser.find_element(By.ID, "birthday")
    print(birth.tag_name)
    for i in data["date_of_birth"]:
        time.sleep(0.2)
        birth.send_keys(i)
    # WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'form-checkbox create-account-v2__checkbox')))
    
    inputs = browser.find_elements(By.TAG_NAME, "input")
    print(inputs[inputs.__len__()-1].get_attribute("id"))
    inputs[inputs.__len__()-1].click()   
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/div/button[2]")))
    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/div/button[2]").click()
    time.sleep(15)
    otp = "  "+getOTP(data["account"])
    active_element = browser.switch_to.active_element
    for i in otp:
        print(i)
        active_element.send_keys(i)
        time.sleep(0.5)
     
    click_first_login(browser)   
    add_payment(browser, data) 
    
    

def click_first_login(browser):
    time.sleep(5) # Đợi cho load xong
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')))
    iframe_hello = browser.find_element(By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')
    browser.switch_to.frame(iframe_hello)
    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div[5]/button')))
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div[5]/button').click()
    time.sleep(5)
    browser.switch_to.default_content()
    browser.get("https://music.apple.com/us/account/settings")
    
def add_payment(browser, data):
    time.sleep(35)
    
    wait = WebDriverWait(browser, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
    iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
    browser.switch_to.frame(iframe_setting)

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li')))
    country = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li').text
    print(country)
    if country != "United States":
        print("Not US") 
    # click nút change payment 
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button')))
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button').click()
    time.sleep(10)
    browser.switch_to.default_content()
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[4]/main/div/div/iframe")))
    iframe_payment = browser.find_element(By.XPATH, "/html/body/div/div[4]/main/div/div/iframe")
    browser.switch_to.frame(iframe_payment)
    # Nhấn nút add payment
    wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div/main/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/div[2]/button')))
    browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/div[2]/button').click()
    browser.switch_to.default_content()
    iframe_add_payment = browser.find_element(By.CSS_SELECTOR, "#ck-container > iframe:nth-child(1)")
    browser.switch_to.frame(iframe_add_payment)
    
    wait.until(EC.visibility_of_element_located((By.ID, "addressOfficialLineFirst")))
    address_1 = browser.find_element(By.ID, "addressOfficialLineFirst")
    for i in data["address1"]:
        address_1.send_keys(i)
        time.sleep(0.06)
    wait.until(EC.visibility_of_element_located((By.ID, "addressOfficialLineSecond")))
    address_2 = browser.find_element(By.ID, "addressOfficialLineSecond")
    for i in data["address2"]:
        address_2.send_keys(i)
        time.sleep(0.06)
    
    wait.until(EC.visibility_of_element_located((By.ID, "addressOfficialCity")))
    city_element = browser.find_element(By.ID, "addressOfficialCity")
    for i in data["city"]:
        city_element.send_keys(i)
        time.sleep(0.06)
    wait.until(EC.visibility_of_element_located((By.ID, "addressOfficialStateProvince")))
    select = Select(browser.find_element(By.ID, "addressOfficialStateProvince"))
    select.select_by_value(data["state"])
    wait.until(EC.visibility_of_element_located((By.ID, "addressOfficialPostalCode")))
    post_code = browser.find_element(By.ID, "addressOfficialPostalCode")
    for i in data["postalCode"]:
        post_code.send_keys(i)
        time.sleep(0.06)
    # Thêm thẻ 
    
    
    time.sleep(100)


def apple_id_done(browser):
    # browser = webdriver.Firefox(seleniumwire_options=option)
    browser.get("https://appleid.apple.com/sign-in")
    
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#aid-auth-widget-iFrame")))
    iframe_login = browser.find_element(By.CSS_SELECTOR, "#aid-auth-widget-iFrame")
    browser.switch_to.frame(iframe_login)
    
    wait = WebDriverWait(browser, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "account_name_text_field")))
    browser.find_element(By.ID, "account_name_text_field").send_keys("tandatvo91@gmail.com")
    
    browser.switch_to.active_element.send_keys(Keys.ENTER)
    browser.switch_to.default_content()
    browser.switch_to.frame(iframe_login)
    
    wait.until(EC.visibility_of_element_located((By.ID, "password_text_field")))
    browser.find_element(By.ID, "password_text_field").send_keys("Zxcv123123")
    browser.switch_to.active_element.send_keys(Keys.ENTER)
    time.sleep(10)
    active_element = browser.switch_to.active_element
    otp = "123456"
    active_element.send_keys(otp)
    
    #OTP xong
    time.sleep(100)
    
# reg_apple_music()

# first_name, last_name, date_of_birth, password = random_data()
# data = None
# address1, address2, city, state, postalCode = random_address()

# data = {
#     "first_name": first_name,
#     "account": generate_random_email(),
#     "password": password,
#     "last_name": last_name,
#     "date_of_birth": date_of_birth,
#     "address1": address1,
#     "address2": address2,
#     "city": city,
#     "state": state,
#     "postalCode": postalCode
# }

# print(data)

# generate_random_email()
# getOTP("cardenasshannon448@gmail.com")
# reg_apple_music()
# generate_random_email()
option = {
        'proxy':  
            {
                'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225'
            }
    
    }
    
browser = webdriver.Firefox(
    seleniumwire_options=option
)

browser.get('https://music.apple.com/us/account/settings')


add_payment(browser, data= {'first_name': 'Bpffe', 'account': 'whitneynataly845@gmail.com', 'password': 'Zxcv123123', 'last_name': 'Mhgux', 'date_of_birth': '04031999', 'address1': '5740 North 59th Avenue', 'address2': '#1156', 'city': 'Glendale', 'state': 'AZ', 'postalCode': '85301'})
# apple_id_done(browser)
# reg_apple_music()