from const import *
def check_account_is_block(browser):
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        text = browser.find_elements(By.TAG_NAME, 'h2')[0].text
        print(text)
        if text == tool_exception.LOCK:
            return True
        else:
            return False    
    except Exception as e:
            print(e)
            return False
def check_account_login_invalid_password(browser):
    try:
        err_element = browser.find_element(By.CSS_SELECTOR, 'p.fat#errMsg')
        if tool_exception.INVALID_PASSWORD == err_element.text:
            return True
        else:
            return False
    except:
        return False

def check_account_has_otp(browser):
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'verify-phone')))
        print("Has OTP")
        return True    
    except Exception as e:
            print(e)
            return False

#cài đặt proxy
option = {
    'proxy': 
        config.PROXY_URL
    
}
# Bắt đầu thao tác
# Đổi instance qua popup login
db_instance = MySQLDatabase()
logging.basicConfig(filename='./logs/errors.log', level=logging.ERROR, format='%(asctime)s - %(message)s',encoding='utf-8')
def run():
    global RUN_APP
    data = db_instance.fetch_data(table_name="mail", columns=["*"], condition="status = 1 and isRunning = 'N' limit 1") 
    if RUN_APP == False:
        return
    db_instance.update_data(table_name="mail", set_values={"isRunning": "Y"}, condition="id = %s" % data[0][0])
    time.sleep(2)
    if USE_PROXY == True:
        browser = webdriver.Firefox(
        seleniumwire_options=  option
        )
        print("Dùng proxy")
    else:
        browser = webdriver.Firefox()
        print("Không dùng proxy")
    wait = WebDriverWait(browser, 20)

    if(data[0] is None): # Trường hợp hết mail
        logging.error("Error Account: %s", str("Hết account khả dụng trong database"))
        browser.quit()
        sys.exit()
        return
    
    browser.get(config.WEB_URL)

    account = Account(data[0][1], data[0][2])
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,  "#ck-container > iframe")))
        iframe = browser.find_element(By.CSS_SELECTOR, value= "#ck-container > iframe")
        browser.switch_to.frame(iframe)
    
    #Nhập account name
        wait.until(EC.visibility_of_element_located((By.ID, "accountName")))
        inputAccount = browser.find_element(By.ID, "accountName")
        inputAccount.send_keys(account.get_account())
    
    # Nhấn nút login
        browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/div/div/div[3]/button").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#aid-auth-widget-iFrame")))
        iframe_auth = browser.find_element(By.CSS_SELECTOR, "#aid-auth-widget-iFrame")
        browser.switch_to.frame(iframe_auth)
    except Exception as e:
        logging.error("Error Tool: %s", str("Không bắt kịp request! Vui lòng kiểm tra mạng hoặc proxy"))
        db_instance.update_data(table_name="mail", set_values={"isRunning": "N"}, condition="id = %s" % data[0][0])
        browser.quit()
        return
        # sys.exit()

#Nhập password
    try:   # Chọn tới vị trí con trỏ hiện tại
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password_text_field"]')))
        inputPassword = browser.find_element(By.XPATH, '//*[@id="password_text_field"]')
        inputPassword.send_keys(account.get_password())
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sign-in"]')))
        browser.find_element(By.XPATH, '//*[@id="sign-in"]').click()
    #active_element = browser.switch_to.active_element
    #time.sleep(2)
    #active_element.send_keys(account.get_password())
    # Nhấn enter
    #active_element.send_keys(Keys.ENTER)
    #time.sleep(3)
    # Kiểm tra trường hợp bị lock
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
   
        # time.sleep(10)
        # browser.switch_to.default_content()
        # WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ck-container"]')))
        # iframe_hello = browser.find_element(By.XPATH,'//*[@id="ck-container"]').find_element(By.TAG_NAME, 'iframe')
        # # src_value = iframe_hello.get_attribute("src")
        # browser.switch_to.frame(iframe_hello)
        # browser.find_element(By.TAG_NAME, 'button')
        
        # browser.find_element(By.TAG_NAME, 'button').click()
        # time.sleep(5)
    # time.sleep(5)
    
    
    except Exception as e:
        logging.error("Error: %s", str("Không bắt kịp request! Vui lòng kiểm tra mạng hoặc proxy"))
        db_instance.update_data(table_name="mail", set_values={"isRunning": "N"}, condition="id = %s" % data[0][0])
        
        browser.quit()
        return
    try:
        active_element = browser.switch_to.active_element
        active_element.send_keys(Keys.TAB)
        active_element.send_keys(Keys.TAB)
        active_element.send_keys(Keys.TAB)
        active_element.send_keys(Keys.ENTER)
        time.sleep(5)
    # time.sleep(10)
    # browser.switch_to.default_content()
    # WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ck-container"]')))
    # iframe_hello = browser.find_element(By.XPATH,'//*[@id="ck-container"]').find_element(By.TAG_NAME, 'iframe')
    # # src_value = iframe_hello.get_attribute("src")
    # browser.switch_to.frame(iframe_hello)
    # browser.find_element(By.TAG_NAME, 'button')
    
    # browser.find_element(By.TAG_NAME, 'button').click()
    # time.sleep(5)


    except Exception as e:
        print(e)
    

    browser.switch_to.default_content()
# Đoạn này là đăng nhập đã thành công
    # Kiểm tra có iframe lần đầu đăng nhập
    try:
        time.sleep(5)
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ck-container > iframe:nth-child(1)')))
        iframe_hello = browser.find_element(By.CSS_SELECTOR, '#ck-container > iframe:nth-child(1)')
        browser.switch_to.frame(iframe_hello)
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'button')))
        browser.find_elements(By.TAG_NAME, 'button')[1].click()
        time.sleep(5)
        browser.switch_to.default_content()
    except Exception as e:
        print('')
    browser.get("https://music.apple.com/us/account/settings")

    try: 
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
        iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")

        iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_setting)

        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li')))
        country = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li').text
        print(country)
        if country != "United States":
            db_instance.update_data(table_name="mail", set_values={"status": 0, "country": country}, condition=f"id = {data[0][0]}")
            browser.quit()
            return
    # click nút change payment 
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button').click()
        browser.switch_to.default_content()

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
        iframe_payment = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_payment)
    except Exception as e:
        browser.get("https://music.apple.com/us/account/settings")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
        iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")

        iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_setting)

        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li')))
        country = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li').text
        print(country)
        if country != "United States":
            db_instance.update_data(table_name="mail", set_values={"status": 0, "country": country}, condition=f"id = {data[0][0]}")
            browser.quit()
            return
    # click nút change payment 
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button').click()
        browser.switch_to.default_content()

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
        iframe_payment = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_payment)
        print('')
# Kiểm tra đã add thẻ 

    wait_child = WebDriverWait(browser, 10)
    try: 
        wait_child.until(EC.visibility_of_element_located((By.CLASS_NAME, 'payment-method-module-card')))
        browser.find_element(By.CLASS_NAME, 'payment-method-module-card').click()
    
    #Nhấn vào thẻ 
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div/main/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-section-item[1]/div/button')))
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-section-item[1]/div/button').click()
    
    # Chuyển sang iframe thanh toán 
        browser.switch_to.default_content()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#ck-container > iframe:nth-child(1)")))
        iframe_child_payment = browser.find_element(By.CSS_SELECTOR, "#ck-container > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_child_payment)
        print(iframe_child_payment)
    #Remove thẻ 
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div/div/div[2]/div/div[4]/csk-button/button')))
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[2]/div/div[4]/csk-button/button').click()
    
    # Nhấn nút remove
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button')))
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button').click()
    except Exception as e:
        print(e)
        browser.switch_to.default_content()
    # run_add_card = False
    # browser.quit()
    # break
# Vào lại iframe thanh toán
    try: 
        browser.switch_to.default_content()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
        iframe_payment = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_payment)
    # Nhấn nút add payment method
        wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div/main/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/div[2]/button')))
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/div[2]/button').click()
        browser.switch_to.default_content()
        iframe_add_payment = browser.find_element(By.CSS_SELECTOR, "#ck-container > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_add_payment)
    except Exception as e:
        print('')
        db_instance.update_data(table_name='mail', set_values={"isRunning": "N"}, condition="id = %s" % data[0][0])
        browser.quit()
        return
#Tìm thông tin thẻ 
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
    # browser.find_element(By.XPATH,'//*[@id="creditCardNumber"]').send_keys("")

        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]')))
        card_expiration_element = browser.find_element(By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]')
        card_expiration_element.clear()
        for i in card.get_card_expiration():
            card_expiration_element.send_keys(i)
            time.sleep(0.1)
    # browser.find_element(By.XPATH,'//*[@id="creditCardExpirationMonth-creditCardExpirationYear"]').send_keys("")

        wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="creditVerificationNumber"]')))
        card_ccv_element = browser.find_element(By.XPATH,'//*[@id="creditVerificationNumber"]')
        card_ccv_element.clear()
        for i in card.get_card_ccv():
            card_ccv_element.send_keys(i)
            time.sleep(0.1)
    # browser.find_element(By.XPATH,'//*[@id="creditVerificationNumber"]').send_keys("658")
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[3]/div/button').click()

    # Kiểm tra các trường hợp lỗi của thẻ 
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal")))
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
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                case tool_exception.INVALID_CARD:
                # Thông tin thẻ sai
                    logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is invalid"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Invalid Card"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                case tool_exception.SUPPORT:
                    logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is support"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "contact suport"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                case tool_exception.DONE:
                    logging.info("Success Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is done"))
                    logging.info("Success Account: Id - %s", str(data[0][1] +" - "+"Account is done"))
                    db_instance.update_data(table_name="pay", set_values={"number_use": data_card[0][6]+1}, condition=f"id = {data_card[0][0]}")
                    db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "Done"}, condition=f"id = {data[0][0]}")
                    break
                case tool_exception.DIE:
                    logging.error("Die Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is die"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                case tool_exception.ACC_SPAM:
                    logging.error("Error Account: Id - %s", str(data[0][1] +" - "+"Account is spam"))
                    db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "add sup"}, condition=f"id = {data[0][0]}")
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "add sup"}, condition=f"id = {data_card[0][0]}")
                    run_add_card = False
                    browser.quit()
                case tool_exception.ISSUE_METHOD:
                    logging.error("Error Card: Id - %s", str(data[0][1] +" - "+"Card Die"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    continue
                case tool_exception.DEC:
                    logging.error("Error Card: Id - %s", str(data[0][1] +" - "+"Card DEC"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    continue
                case tool_exception.DECLINED:
                    logging.error("Error Card: Id - %s", str(data[0][1] +" - "+"Card DEC"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    continue
                case _:
                    logging.error("Error Card: Lỗi không xác định - %s", str(add_payment_result.text))
        except NoSuchElementException as e:
            logging.error("Error Card: Thông tin thẻ không hợp lệ - %s")
            db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Invalid Card"}, condition=f"id = {data_card[0][0]}")
            continue
        # wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
        # browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()

        except Exception as e: # Không có thông báo. => Add thẻ thành công
            logging.info("Success Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is done"))
            logging.info("Success Account: Id - %s", str(data[0][1] +" - "+"Account is done"))
            db_instance.update_data(table_name="pay", set_values={"number_use": data_card[0][6]+1}, condition=f"id = {data_card[0][0]}")
            # Lưu thông tin lên db
            db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "Done","card_add" : card.get_card_ccv()}, condition=f"id = {data[0][0]}")
            run_add_card = False
            browser.quit()

# from functions import reg_apple_id as reg
# import json
# import time
print("Đang login Apple Music và thêm thẻ")
# def check_run_app():
#     f = open ('./config/tool-config.json', "r")
#     data = json.loads(f.read())
#     f.close()
#     return data['RUN']
# while check_run_app():
run()