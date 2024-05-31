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
    data = db_instance.fetch_data(table_name="mail", columns=["*"], condition="status = 1 and isRunning = 'N' limit 1")
    db_instance.update_data(table_name="mail", set_values={"isRunning": "Y"}, condition="id = %s" % data[0][0])
    return data[0][0], data[0][1], data[0][2]

def get_card_info():
    data_card = db_instance.fetch_data(table_name="pay", columns=["*"], condition="status = 1 and on_use = 0 limit 1")
    db_instance.update_data(table_name="pay", set_values={"on_use": 1},condition=f'id = {data_card[0][0]}')
    return data_card[0][0], data_card[0][1], data_card[0][2]+""+ data_card[0][3], data_card[0][4], data_card[0][6]
    
def update_mail_re_run(id):
    db_instance.update_data(table_name="mail", set_values={"isRunning": "N"}, condition="id = %s" % id)
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
        db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "UnLock"}, condition=f"id = {mail_id}")
        driver.quit()
        return
    
    if check_account_login_invalid_password(driver):
        print("Sai pass")
        db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "SaiPass"}, condition=f"id = {mail_id}")
        driver.quit()
        return
    # Kiểm tra acc có otp 
    if check_account_has_otp(driver):
        db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "2FA"}, condition=f"id = {mail_id}")
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
        print(country)
        if country != "United States":
            db_instance.update_data(table_name="mail", set_values={"status": 0, "country": country}, condition=f"id = {mail_id}")
            exception = True
    except Exception as e:
        exception = True
    
    if exception == True:
        update_mail_re_run(mail_id)
        driver.quit()
        return
    
    # Nhấn nút trong payment
    try:
        driver.switch_to.default_content()
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe'))
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button')))
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button').click()
    except Exception as e: # Đã có thẻ
        print('')
        
    try:
        # Nhấn nút add payment
        driver.switch_to.default_content()
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe'))
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/button')))
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/button').click()
    except Exception as e: # Đã có thẻ
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'payment-method-module-card')))
        driver.find_element(By.CLASS_NAME, 'payment-method-module-card').click()
        
        driver.switch_to.default_content()
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ck-modal"]/iframe')))
        iframe_child_payment = driver.find_element(By.XPATH, '//*[@id="ck-modal"]/iframe')
        driver.switch_to.frame(iframe_child_payment)
        print('Đã vào iframe thanh toán')
    
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="modal-body"]/div/div[5]/csk-button/button')))
        driver.find_element(By.XPATH,'//*[@id="modal-body"]/div/div[5]/csk-button/button').click()
    
    # Chuyển sang iframe thanh toán 
    #     driver.switch_to.default_content()
    #     WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ck-modal"]/iframe')))
    #     iframe_child_payment = driver.find_element(By.XPATH, '//*[@id="ck-modal"]/iframe')
    #     driver.switch_to.frame(iframe_child_payment)
    #     print('Đã vào iframe thanh toán')
    # #Remove thẻ 
    #     WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="modal-body"]/div/div[5]/csk-button/button')))
    #     driver.find_element(By.XPATH,'//*[@id="modal-body"]/div/div[5]/csk-button/button').click()
    #     print('Đã nhấn xoá thẻ')
    # Nhấn nút remove
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="app"]/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button')))
        driver.find_element(By.XPATH,'//*[@id="app"]/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button').click()
        driver.switch_to.default_content()
        driver.get("https://tv.apple.com/settings")
    # Add thẻ 
    try:
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
        # driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe'))
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button')))
        # driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button').click()
        # # Nhấn nút add payment
        # driver.switch_to.default_content()
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-area"]/div/iframe')))
        # driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="content-area"]/div/iframe'))
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/button')))
        # driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/button').click()
        print('Tới đoạn add thẻ')
        # Điền thẻ 
        while True:
            card_id,card_number, card_expiration, card_ccv, num_add = 1, '', '', '', 0
            try:
                card_id,card_number, card_expiration, card_ccv, num_add = get_card_info()
            
                if num_add >= get_max_card_add():
                    db_instance.update_data(table_name="pay", set_values={"status": 0},condition=f'id = {card_id}')
                    continue
            except Exception as e:
                print('Hết thẻ')
            
            driver.switch_to.default_content()
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ck-modal"]/iframe')))
            print(driver.find_element(By.XPATH, '//*[@id="ck-modal"]/iframe'))
            driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ck-modal"]/iframe'))
            
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditCardNumber"]')))
            card_number_element = driver.find_element(By.XPATH,'//*[@id="creditCardNumber"]')
            card_number_element.clear()
            
            for i in card_number:
                card_number_element.send_keys(i)
                time.sleep(0.2)
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]')))
            card_expiration_element = driver.find_element(By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]')
            card_expiration_element.clear()
            for i in card_expiration:
                card_expiration_element.send_keys(i)
                time.sleep(0.2)


            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditVerificationNumber"]')))
            card_ccv_element = driver.find_element(By.XPATH,'//*[@id="creditVerificationNumber"]')
            card_ccv_element.clear()
            for i in card_ccv:
                card_ccv_element.send_keys(i)
                time.sleep(0.2)
            time.sleep(2)

            driver.find_element(By.XPATH,'//*[@id="modal-footer-0"]/div/button').click()
            wait = WebDriverWait(driver, 15)
            # Kiểm tra lỗi thẻ 
            try:
                driver.switch_to.default_content()
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ck-modal"]/iframe')))
                driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ck-modal"]/iframe'))
                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/camk-modal/div/camk-modal-content/camk-modal-header/camk-modal-description')))
                add_payment_result = driver.find_element(By.XPATH, '//*[@id="app"]/div/camk-modal/div/camk-modal-content/camk-modal-header/camk-modal-description')
                print(add_payment_result.text)
                match add_payment_result.text:
                    case tool_exception.DISSABLE:
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Dissable Card"}, condition=f"id = {card_id}")
                        db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "UnLock"},condition=f'id = {mail_id}')
                        exception = True
                        break
                    case tool_exception.MANY:
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "To Many ID"}, condition=f"id = {card_id}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                        time.sleep(2)
                        continue
                    case tool_exception.INVALID_CARD:
                # Thông tin thẻ sai
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Invalid Card"}, condition=f"id = {card_id}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                        time.sleep(2)
                        continue
                    case tool_exception.SUPPORT:
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "contact suport"}, condition=f"id = {card_id}")
                        exception = True
                        break
                    
                    
                    case tool_exception.DIE:
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {card_id}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                        time.sleep(2)
                        continue
                    case tool_exception.ACC_SPAM:
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "add sup"}, condition=f"id = {card_id}")
                        break
                        
                    # continue
                    case tool_exception.ISSUE_METHOD:
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {card_id}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                        time.sleep(2)
                        continue
                    case tool_exception.DEC:
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {card_id}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                        time.sleep(2)
                        continue
                    case tool_exception.DECLINED:
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {card_id}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                        time.sleep(2)
                        continue
            except NoSuchElementException as e:
                db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Invalid Card"}, condition=f"id = {card_id}")
                continue


            except Exception as e: # Không có thông báo. => Add thẻ thành công
                db_instance.update_data(table_name="pay", set_values={"number_use": num_add+1}, condition=f"id = {card_id}")
                db_instance.update_data(table_name="pay", set_values={"on_use": 0}, condition=f"id = {card_id}")
                db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "Done"}, condition=f"id = {mail_id}")
                break
    except Exception as e:
        exception = True
        
    if exception == True:
        update_mail_re_run(mail_id)
        driver.quit()
        return
    

    
if __name__ == "__main__":
    run()