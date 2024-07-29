from const import *

#cài đặt proxy
option = {
    'proxy': 
        config.PROXY_URL
    
}
# Bắt đầu thao tác
# Đổi instance qua popup login
db_instance = MySQLDatabase()
logging.basicConfig(filename='./logs/errors.log', level=logging.ERROR, format='%(asctime)s - %(message)s',encoding='utf-8')
def run(run_check = False, run_delete = False):
    try: 
        data = db_instance.fetch_data(table_name="mail", columns=["*"], condition="isRunning = 'N' and count_run <= 3 limit 1") 
        print(data)
        db_instance.increment_count_run(table_name="mail", id= data[0][0])
        db_instance.update_data(table_name="mail", set_values={"isRunning": "Y"}, condition="id = %s" % data[0][0])
    except Exception as e:
        print('Có lỗi khi lấy data')
        return
    
    time.sleep(2)
    # if USE_PROXY == True:
    random_port = random.randint(10200, 10499)
    random_proxy = [
    #     {
    #     'proxy': {
    #         'https': 'https://adz56789:Zxcv123123=5@gate.dc.smartproxy.com:20000',
    #         'http': 'http://adz56789@Zxcv123123=5@gate.dc.smartproxy.com:20000',
    #         'no_proxy': 'localhost,127.0.0.1'
    #     },
    #     'mitm_http2': False
    # },
    {'proxy': {'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225'}}
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
    browser = webdriver.Firefox(
        seleniumwire_options=proxy
    )
    # else:
    #     browser = webdriver.Firefox()
        
    wait = WebDriverWait(browser, 20)

    if(data[0] is None): # Trường hợp hết mail
        logging.error("Error Account: %s", str("Hết account khả dụng trong database"))
        browser.quit()
        return
    
    try: 
        browser.get(config.WEB_URL)
    except Exception as e:
        db_instance.update_data(table_name="mail", set_values={"isRunning": "N"}, condition="id = %s" % data[0][0])
        logging.error("Error Tool: %s", str("Lỗi proxy"))
        browser.quit()
        return

    account = Account(data[0][1], data[0][2])
    try:
        WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR,  "#ck-container > iframe")))
        iframe = browser.find_element(By.CSS_SELECTOR, value= "#ck-container > iframe")
        browser.switch_to.frame(iframe)
    
        #Nhập account name
        wait.until(EC.visibility_of_element_located((By.ID, "accountName")))
        inputAccount = browser.find_element(By.ID, "accountName")
        time.sleep(2)
        inputAccount.send_keys(account.get_account())
    
        # Nhấn nút login
        browser.switch_to.active_element.send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#aid-auth-widget-iFrame")))
        iframe_auth = browser.find_element(By.CSS_SELECTOR, "#aid-auth-widget-iFrame")
        browser.switch_to.frame(iframe_auth)
    except Exception as e:
        logging.error("Error Tool: %s", str("Không bắt kịp request! Vui lòng kiểm tra mạng hoặc proxy"))
        db_instance.update_data(table_name="mail", set_values={"isRunning": "N"}, condition="id = %s" % data[0][0])
        browser.quit()
        return

    try:   # Chọn tới vị trí con trỏ hiện tại
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password_text_field"]')))
        inputPassword = browser.find_element(By.XPATH, '//*[@id="password_text_field"]')
        time.sleep(2)
        inputPassword.send_keys(account.get_password())
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sign-in"]')))
        browser.find_element(By.XPATH, '//*[@id="sign-in"]').click()
        if check_account_is_block(browser):
            logging.error("Error Account: Id -  %s", str(data[0][1] +" "+tool_exception.LOCK))
            db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "UnLock"}, condition=f"id = {data[0][0]}")
            browser.quit()
            return
    
        if check_account_login_invalid_password(browser):
            logging.error("Error Account: Id - %s", str(data[0][1] +"-" +tool_exception.INVALID_PASSWORD))
            db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "SaiPass"}, condition=f"id = {data[0][0]}")
            browser.quit()
            return
    
        time.sleep(5)
        # Kiểm tra acc có otp 
        if check_account_has_otp(browser):
            logging.error("Error Account: Id - %s", str(data[0][1] +"-"+"2FA"))
            db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "2FA"}, condition=f"id = {data[0][0]}")
            browser.quit()
            return
    
    except Exception as e:
        logging.error("Error: %s", str("Không bắt kịp request! Vui lòng kiểm tra mạng hoặc proxy"))
        db_instance.update_data(table_name="mail", set_values={"isRunning": "N"}, condition="id = %s" % data[0][0])
        browser.quit()
        return
    # Nhấn vào form privacy
    try:
        browser.switch_to.default_content()
        WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR,  "#ck-container > iframe:nth-child(1)")))
        iframe = browser.find_element(By.CSS_SELECTOR, value= "#ck-container > iframe:nth-child(1)")
        browser.switch_to.frame(iframe)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#aid-auth-widget-iFrame")))
        iframe_auth = browser.find_element(By.CSS_SELECTOR, "#aid-auth-widget-iFrame")
        browser.switch_to.frame(iframe_auth)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#repairFrame")))
        iframe_auth = browser.find_element(By.CSS_SELECTOR, "#repairFrame")
        browser.switch_to.frame(iframe_auth)
        btns = browser.find_elements(By.TAG_NAME, "button")
        btns[0].click()
        time.sleep(10)
    except Exception as e:
        print('')
    

    

    try: # Lần đầu đăng nhập
        browser.get("https://music.apple.com/us/account/settings")
        browser.switch_to.default_content()
        time.sleep(5)
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')))
        iframe_hello = browser.find_element(By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')
        browser.switch_to.frame(iframe_hello)
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.ID, 'modal-body')))
        modal_welcome = browser.find_element(By.ID, 'modal-body')
        
        btns = modal_welcome.find_elements(By.TAG_NAME, 'button')
        btns[0].click()
        time.sleep(5)
        browser.switch_to.default_content()
    except Exception as e:
        print('')
        
    try:
        time_reload = 0
        while time_reload < 2:
            browser.get("https://music.apple.com/us/account/settings")
            time_reload = time_reload + 1
            try: 
                WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
                iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")

                iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
                browser.switch_to.frame(iframe_setting)

                WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'li')))
                lis = browser.find_elements(By.TAG_NAME, 'li')
                country = lis[10].text
                if country != "United States":
                    db_instance.update_data(table_name="mail", set_values={"status": 0, "country": country}, condition=f"id = {data[0][0]}")
                    browser.quit()
                    return
                
                if run_check == True:
                    balance = lis[11].text
                    db_instance.insert_mail_check([data[0][1], data[0][2],country,float(balance.replace("$",""))])
                    browser.quit()
                    return
                
                lis[3].click()
            except Exception as e:
                print('')
    except Exception as e:
        db_instance.update_data(table_name='mail', set_values={"isRunning": "N"}, condition="id = %s" % data[0][0])
        browser.quit()
        return

    try: 
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'payment-method-module-card')))
        browser.find_element(By.CLASS_NAME, 'payment-method-module-card').click()
        time.sleep(5)
        browser.switch_to.default_content()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#ck-container > iframe:nth-child(1)")))
        iframe_payment = browser.find_element(By.CSS_SELECTOR, "#ck-container > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_payment)
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div[5]/csk-button/button')))
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div[5]/csk-button/button').click()
        time.sleep(5)
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button')))
        browser.find_element(By.XPATH,'/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button').click()
        time.sleep(5)
        if run_delete == True:
            db_instance.insert_mail_delete([data[0][1], data[0][2],"",country,"bin"])
            browser.quit()
            return
    except Exception as e:
        if run_delete == True:
            db_instance.insert_mail_delete([data[0][1], data[0][2],"",country,"none"])
            browser.quit()
            return

    try: 
        browser.switch_to.default_content()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
        iframe_payment = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_payment)
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/button')))
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/button').click()
        browser.switch_to.default_content()
        iframe_add_payment = browser.find_element(By.CSS_SELECTOR, "#ck-container > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_add_payment)
    except Exception as e:
        db_instance.update_data(table_name='mail', set_values={"isRunning": "N"}, condition="id = %s" % data[0][0])
        browser.quit()
        return
    
    try:
        run_add_card = True
        while run_add_card:
            data_card = db_instance.fetch_data(table_name="pay", columns=["*"], condition="status = 1 limit 1")
            try:
                if data_card[0] is None:
                    logging.error("Error: %s", str("Hết thẻ"))
                    sys.exit() # Dừng cjương trình
            except IndexError:
                logging.error("Error: %s", str("Hết thẻ"))
                browser.quit()
                sys.exit()
            
            if data_card[0][6] >= get_max_card_add():
                db_instance.update_data(table_name="pay", set_values={"status": 0},condition=f'id = {data_card[0][0]}')
                continue
            
            card = Card(data_card[0][1], data_card[0][2]+""+ data_card[0][3], data_card[0][4])
            wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditCardNumber"]')))
            card_number_element = browser.find_element(By.XPATH,'//*[@id="creditCardNumber"]')
            card_number_element.clear()
            for i in card.get_card_number():
                card_number_element.send_keys(i)
                time.sleep(0.1)

            wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]')))
            card_expiration_element = browser.find_element(By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]')
            card_expiration_element.clear()
            for i in card.get_card_expiration():
                card_expiration_element.send_keys(i)
                time.sleep(0.1)

            wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditVerificationNumber"]')))
            card_ccv_element = browser.find_element(By.XPATH,'//*[@id="creditVerificationNumber"]')
            card_ccv_element.clear()
            for i in card.get_card_ccv():
                card_ccv_element.send_keys(i)
                time.sleep(0.1)
                
            browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/div/button').click()

            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal")))
                add_payment_result = browser.find_element(By.CSS_SELECTOR, ".camk-modal-description")
                match add_payment_result.text:
                    case tool_exception.DISSABLE:
                        logging.error("Error Account: Id - %s", str(data[0][1] +" - "+"Account is disable"))
                        db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "Diss"}, condition=f"id = {data[0][0]}")
                        run_add_card = False # Dừng vì account bị disable
                        browser.quit()
                    case tool_exception.MANY:
                        logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is many account add"))
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "To Many ID"}, condition=f"id = {data_card[0][0]}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    case tool_exception.INVALID_CARD:
                    # Thông tin thẻ sai
                        logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is invalid"))
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Invalid Card"}, condition=f"id = {data_card[0][0]}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    case tool_exception.SUPPORT:
                        logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is support"))
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "contact suport"}, condition=f"id = {data_card[0][0]}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    case tool_exception.DIE:
                        logging.error("Die Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is die"))
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {data_card[0][0]}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    case tool_exception.ACC_SPAM:
                        logging.error("Error Account: Id - %s", str(data[0][1] +" - "+"Account is spam"))
                        db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "add sup"}, condition=f"id = {data[0][0]}")
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "add sup"}, condition=f"id = {data_card[0][0]}")
                        run_add_card = False
                        browser.quit()
                    case tool_exception.ISSUE_METHOD:
                        logging.error("Error Card: Id - %s", str(data[0][1] +" - "+"Card Die"))
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {data_card[0][0]}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                        continue
                    case tool_exception.DEC:
                        logging.error("Error Card: Id - %s", str(data[0][1] +" - "+"Card DEC"))
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {data_card[0][0]}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                        continue
                    case tool_exception.DECLINED:
                        logging.error("Error Card: Id - %s", str(data[0][1] +" - "+"Card DEC"))
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {data_card[0][0]}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                        continue
                    case tool_exception.PAYMENT_ERR:
                        logging.error("Error Card: Id - %s", str(data[0][1] +" - "+"Card DEC"))
                        db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Many add"}, condition=f"id = {data_card[0][0]}")
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                        continue
                    case _:
                        logging.error("Error Card: Lỗi không xác định - %s", str(add_payment_result.text))
                        wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                        browser.find_element(By.XPATH, "/html/body/div[1]/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                        continue
            except NoSuchElementException as e:
                logging.error("Error Card: Thông tin thẻ không hợp lệ - %s")
                db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Invalid Card"}, condition=f"id = {data_card[0][0]}")
                continue
            
            except Exception as e: # Không có thông báo. => Add thẻ thành công
                logging.info("Success Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is done"))
                logging.info("Success Account: Id - %s", str(data[0][1] +" - "+"Account is done"))
                db_instance.update_data(table_name="pay", set_values={"number_use": data_card[0][6]+1}, condition=f"id = {data_card[0][0]}")
                db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "Done","card_add" : card.get_card_ccv()}, condition=f"id = {data[0][0]}")
                run_add_card = False
                browser.quit()
    except Exception as e:
        db_instance.update_data(table_name='mail', set_values={"isRunning": "N"}, condition="id = %s" % data[0][0])
        logging.error("Error Card: Lỗi không xác định - %s", str(e))
        browser.quit()
        return 


