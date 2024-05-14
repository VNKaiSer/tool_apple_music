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

def run_check():
    global RUN_APP
    data = db_instance.fetch_data(table_name="mail", columns=["*"], condition="loginCheck = 'Y' and isRunningLoginCheck = 'N' limit 1")
    if RUN_APP == False:
        return
    db_instance.update_data(table_name="mail", set_values={"isRunningLoginCheck": "Y"}, condition="id = %s" % data[0][0])
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
        db_instance.update_data(table_name="mail", set_values={"isRunningLoginCheck": "N"}, condition="id = %s" % data[0][0])
        logging.error("Error Tool: %s", str("Không bắt kịp request! Vui lòng kiểm tra mạng hoặc proxy"))
        browser.quit()
        return
        

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
            db_instance.insert_mail_check([data[0][1], data[0][2],"UnLock",0])
            browser.quit()
            return
    
        if check_account_login_invalid_password(browser):
            logging.error("Error Account: Id - %s", str(data[0][1] +"-" +tool_exception.INVALID_PASSWORD))
            db_instance.insert_mail_check([data[0][1], data[0][2],"sai pass",0])
            browser.quit()
            return
    
        time.sleep(5)
    # Kiểm tra acc có otp 
        if check_account_has_otp(browser):
            logging.error("Error Account: Id - %s", str(data[0][1] +"-"+"2FA"))
            db_instance.insert_mail_check([data[0][1], data[0][2],"2FA",0])
            browser.quit()
            return
    # Lần đầu đăng nhập
        try:
            click_on_setting = False
            active_element = browser.switch_to.active_element
            active_element.send_keys(Keys.TAB)
            active_element.send_keys(Keys.TAB)
            active_element.send_keys(Keys.TAB)
            active_element.send_keys(Keys.ENTER)
            time.sleep(5)
            click_on_setting = True
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
            click_on_setting = False
            print(e)
        
    
        browser.switch_to.default_content()
    # time.sleep(5)
    
    
    except Exception as e:
        logging.error("Error: %s", str("Không bắt kịp request! Vui lòng kiểm tra mạng hoặc proxy"))
        db_instance.update_data(table_name="mail", set_values={"isRunningLoginCheck": "N"}, condition="id = %s" % data[0][0])
        browser.quit()
        return
    browser.switch_to.default_content()
# Đoạn này là đăng nhập đã thành công
# Chuyển hướng sang trang cài đặt
    browser.get("https://music.apple.com/us/account/settings")
    if click_on_setting:
# time.sleep(5)
    # time.sleep(5)
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')))
        iframe_hello = browser.find_element(By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')
        browser.switch_to.frame(iframe_hello)
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[4]/div/div[2]/div/div/div/div[5]/button')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[4]/div/div[2]/div/div/div/div[5]/button').click()
        time.sleep(5)
        browser.switch_to.default_content()
        browser.get("https://music.apple.com/us/account/settings")
# Đợi cái frame cài đặt hiển thị lên 


    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
    iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")

    iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
    browser.switch_to.frame(iframe_setting)

    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li')))
    country = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[3]/ul/li').text
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[3]/div/ul/li')))
    balance = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[3]/div/ul/li').text
    
    db_instance.insert_mail_check([data[0][1], data[0][2],country,float(balance.replace("$",""))])
    browser.quit()
        
time.sleep(10)
run_check()
