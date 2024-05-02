from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import logging
import sys
import mysql.connector

# Class
class Tool_Exception:
    DONE = "done"
    DISSABLE = "Your account has been disabled. Contact Apple Support for more details."
    INVALID_PASSWORD = "Your Apple ID or password was incorrect."
    LOCK = "This Apple ID has been locked for security reasons."
    SUPPORT = "Contact Apple Support for more information."
    MANY = "This payment method is associated with too many Apple IDs. To continue, choose another payment method."
    INVALID_CARD = "Your credit card was declined. Please enter a valid credit card information."
    BOTH ="Thông tin thẻ bị sai"
    DIE = "This payment method can’t be used with the iTunes Store. Try again using another payment method."
    ACC_SPAM = "There was a problem when trying to add this payment method. Try again at a later time."

class Config:
    #web
    WEB_URL = "https://music.apple.com/us/login"
    # proxy config 
    PROXY_URL = {'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225'}
    
    #  config 
    DB_HOST = "159.65.2.46"
    DB_PORT = 3306
    DB_USER = "kaiser"
    DB_PASSWORD = "r!8R%OMm@=H{cVH6LZpqV]nye1G"
    DB_NAME = "apple_music"
    
    
class Account:
    def __init__(self, account, password):
        self._account = account
        self._password = password

    def get_account(self):
        return self._account

    def set_account(self, new_account):
        self._account = new_account

    def get_password(self):
        return self._password

    def set_password(self, new_password):
        self._password = new_password

class Card:
    def __init__(self, card_number, card_expiration, card_ccv):
        self._card_number = card_number
        self._card_expiration = card_expiration
        self._card_ccv = card_ccv

    def get_card_number(self):
        return self._card_number

    def set_card_number(self, new_card_number):
        self._card_number = new_card_number

    def get_card_expiration(self):
        return self._card_expiration

    def set_card_expiration(self, new_card_expiration):
        self._card_expiration = new_card_expiration

    def get_card_ccv(self):
        return self._card_ccv

    def set_card_ccv(self, new_card_ccv):
        self._card_ccv = new_card_ccv

class MySQLDatabase:
    def __init__(self, ):
        self.connection = mysql.connector.connect(
            host= Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        column_str = ', '.join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_str})"
        self.cursor.execute(query)
        self.connection.commit()

    def insert_data(self, table_name, data):
        placeholders = ', '.join(['%s' for _ in range(len(data))])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(query, data)
        self.connection.commit()

    def update_data(self, table_name, set_values, condition):
        set_clause = ', '.join([f"{key} = %s" for key in set_values.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.cursor.execute(query, list(set_values.values()))
        self.connection.commit()

    def delete_data(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)
        self.connection.commit()

    def fetch_data(self, table_name, columns="*", condition=None):
        column_str = ', '.join(columns)
        query = f"SELECT {column_str} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
        
tool_exception = Tool_Exception()
config = Config()
def check_account_is_block(browser):
    try:
        if_lid = browser.find_element(By.CSS_SELECTOR,"#aid-auth-widget-iFrame")
        browser.switch_to.frame(if_lid)
        text = browser.find_elements(By.TAG_NAME, 'h2')[0].text
        if text == tool_exception.LOCK:
            return True
        else:
            return False    
    except:
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


#cài đặt proxy
option = {
    'proxy': 
        config.PROXY_URL
    
}

# cài đặt webdriver


# Mở instance tới web


# Bắt đầu thao tác
# Đổi instance qua popup login
db_instance = MySQLDatabase()
logging.basicConfig(filename='./logs/errors.log', level=logging.ERROR, format='%(asctime)s - %(message)s',encoding='utf-8')
while(data := db_instance.fetch_data(table_name="mail", columns=["*"], condition="status = 1 limit 1")):
    browser = webdriver.Firefox(
        seleniumwire_options=option
    )
# cấu hình cài đặt
    wait = WebDriverWait(browser, 20)
    if(data[0] is None): # Trường hợp hết mail
        logging.error("Error Account: %s", str("Hết account khả dụng trong database"))
        browser.close()
        break
    
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
        # continue
        sys.exit()
    
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
            continue
        
        if check_account_login_invalid_password(browser):
            logging.error("Error Account: Id - %s", str(data[0][1] +"-" +tool_exception.INVALID_PASSWORD))
            db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "SaiPass"}, condition=f"id = {data[0][0]}")
            continue
        time.sleep(5)
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
            # WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ck-container"]')))
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
        browser.close()
        continue
    browser.switch_to.default_content()
    # Đoạn này là đăng nhập đã thành công
    # Chuyển hướng sang trang cài đặt
    browser.get("https://music.apple.com/us/account/settings")
    if click_on_setting:
    # time.sleep(5)
        # time.sleep(5)
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')))
        iframe_hello = browser.find_element(By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')
        browser.switch_to.frame(iframe_hello)
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[4]/div/div[2]/div/div/div/div[5]/button')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[4]/div/div[2]/div/div/div/div[5]/button').click()
        time.sleep(5)
        browser.switch_to.default_content()
        browser.get("https://music.apple.com/us/account/settings")
# Đợi cái frame cài đặt hiển thị lên 
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
    iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")

    iframe_setting = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
    browser.switch_to.frame(iframe_setting)
    # click nút change payment 
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button')))
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button').click()
    browser.switch_to.default_content()
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
    iframe_payment = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
    browser.switch_to.frame(iframe_payment)
    # Kiểm tra đã add thẻ 
    
    wait_child = WebDriverWait(browser, 5)
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
        # browser.close()
        # break
    # Vào lại iframe thanh toán
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
    iframe_payment = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
    browser.switch_to.frame(iframe_payment)
    # Nhấn nút add payment method
    wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div/main/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/div[2]/button')))
    browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div/div/div/div/div[2]/camk-section/camk-section-grid/camk-banner-card/div[2]/div/div[2]/div[2]/button').click()
    browser.switch_to.default_content()
    iframe_add_payment = browser.find_element(By.CSS_SELECTOR, "#ck-container > iframe:nth-child(1)")
    browser.switch_to.frame(iframe_add_payment)
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
            browser.close()
            sys.exit()
            pass  # hoặc thực hiện các hành động khác tương ứng
           
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
                    browser.close()
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
                    browser.close()
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
            db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "Done","card_add" : card.get_card_number()}, condition=f"id = {data[0][0]}")
            run_add_card = False
            browser.close()
            # wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
            # browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
        


