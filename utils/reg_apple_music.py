import random
import string
import datetime
import time
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def generate_random_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def generate_name(length):
    random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    letter = random_string.capitalize()
    
    return letter
def generate_random_date_of_birth():
    day = str(random.randint(1, 28)).zfill(2)  
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(1900, datetime.datetime.now().year - 18))  
    
    date_of_birth = day + month + year
    
    return date_of_birth
def random_data():
    password = generate_random_password(8)
    frist_name = generate_name(5)
    last_name = generate_name(5)
    date_of_birth = generate_random_date_of_birth()
    return frist_name, last_name, date_of_birth,password

def generate_random_email(username):
    digit = ''.join(random.choice(string.digits) for _ in range(random.randint(3, 4)))

    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "example.com"]

    domain = random.choice(domains)

    email = username + digit + "@" + domain

    return email

def reg_apple_music():
    first_name, last_name, date_of_birth, password = random_data()
    data = {
        "first_name": first_name,
        "account": generate_random_email(first_name),
        "password": password,
        "last_name": last_name,
        "date_of_birth": date_of_birth 
    }
    
    print(data)
    
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
    wait = WebDriverWait(browser, 20)
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
        time.sleep(10)
        # WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#aid-auth-widget-iFrame")))
        # iframe_auth = browser.find_element(By.CSS_SELECTOR, "#aid-auth-widget-iFrame")
        # browser.switch_to.frame(iframe_auth)
    except Exception as e:
        print(e)
    
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
    
    time.sleep(100)
reg_apple_music()