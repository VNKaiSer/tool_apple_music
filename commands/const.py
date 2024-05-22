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
import json
import random
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
    
    def insert_mail_reg_apple_music_not_add(self, mail):
        date_string = mail[2]

    # Chia chuỗi thành các phần để lấy ngày, tháng và năm
        month = date_string[0:2]
        day = date_string[2:4]
        year = date_string[4:]

    # Tạo chuỗi mới với định dạng ngày/tháng/năm
        formatted_date = f"{day}_{month}_{year}"
        query = "INSERT INTO reg_apple_music_id(mail, password, day) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (mail[0], mail[1], formatted_date))
        self.connection.commit()
    
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
    def get_mail_tv_wait(self):
        query = "SELECT * FROM mail_reg_apple_tv_wait WHERE `status` = 'Y'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            return None
    def insert_mail_wait(self, mail_wait, password, code_old = ' '):
            # Kiểm tra xem email đã tồn tại trong cơ sở dữ liệu chưa
        query_check = "SELECT * FROM mail_reg_apple_music_wait WHERE mail = %s"
        self.cursor.execute(query_check, (mail_wait,))
        existing_record = self.cursor.fetchone()

        if existing_record:
        # Nếu email đã tồn tại, cập nhật trạng thái thành 'y'
            query_update = "UPDATE mail_reg_apple_music_wait SET status = 'Y', code_old = %s WHERE mail = %s"
            self.cursor.execute(query_update, (code_old, mail_wait))
            self.connection.commit()
        else:
            # Nếu email chưa tồn tại, thêm email mới vào cơ sở dữ liệu
            query_insert = "INSERT INTO mail_reg_apple_music_wait(mail, password, code_old) VALUES (%s, %s, %s)"
            self.cursor.execute(query_insert, (mail_wait, password, code_old))
            self.connection.commit()
    
    def insert_mail_reg_apple_music(self, mail):
        date_string = mail[6]

    # Chia chuỗi thành các phần để lấy ngày, tháng và năm
        month = date_string[0:2]
        day = date_string[2:4]
        year = date_string[4:]
        formatted_date = f"{day}_{month}_{year}"
        query = "INSERT INTO reg_apple_music_id(mail, password, card_number, month_exp, year_exp, ccv, day) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        self.cursor.execute(query, (mail[0], mail[1], mail[2], mail[3], mail[4], mail[5],formatted_date))
        self.connection.commit()
    
    def get_code_old(self, mail):
        query = "SELECT code_old FROM mail_reg_apple_music_wait WHERE mail = %s"
        self.cursor.execute(query, (mail,))
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            return ' '
    def close(self):
        self.connection.close()
    
    def insert_mail_reg_apple_tv(self, mail):
        date_string = mail[6]

    # Chia chuỗi thành các phần để lấy ngày, tháng và năm
        month = date_string[0:2]
        day = date_string[2:4]
        year = date_string[4:]
        formatted_date = f"{day}_{month}_{year}"
        query = "INSERT INTO reg_apple_tv_id(mail, password, card_number, month_exp, year_exp, ccv, day) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        self.cursor.execute(query, (mail[0], mail[1], mail[2], mail[3], mail[4], mail[5],formatted_date))
        self.connection.commit() 
    
    def insert_mail_tv_wait(self, mail_wait, password, code_old = ' '):
            # Kiểm tra xem email đã tồn tại trong cơ sở dữ liệu chưa
        query_check = "SELECT * FROM mail_reg_apple_tv_wait WHERE mail = %s"
        self.cursor.execute(query_check, (mail_wait,))
        existing_record = self.cursor.fetchone()

        if existing_record:
        # Nếu email đã tồn tại, cập nhật trạng thái thành 'y'
            query_update = "UPDATE mail_reg_apple_tv_wait SET status = 'Y', code_old = %s WHERE mail = %s"
            self.cursor.execute(query_update, (code_old, mail_wait))
            self.connection.commit()
        else:
            # Nếu email chưa tồn tại, thêm email mới vào cơ sở dữ liệu
            query_insert = "INSERT INTO mail_reg_apple_tv_wait(mail, password, code_old) VALUES (%s, %s, %s)"
            self.cursor.execute(query_insert, (mail_wait, password, code_old))
            self.connection.commit()
       
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

def get_max_card_add():
    f = open ('./config/tool-config.json', "r")
    data = json.loads(f.read())
    f.close()
    return data['TIME_ADD_CARD']

def check_region(browser):
    try: 
        browser.get('https://ip-api.com/')
        WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="codeOutput"]/span[12]')))
        contry_code = browser.find_element(By.XPATH, '//*[@id="codeOutput"]/span[12]').text
        if contry_code != 'US':
            browser.quit()
            return False
 
        return True
    except Exception as e:
        browser.quit()
        return False
    
def generate_random_port():
    return random.randint(49152, 65535)
#cài đặt proxy
option = {
    'proxy': 
        config.PROXY_URL
    
}
# Bắt đầu thao tác
# Đổi instance qua popup login
db_instance = MySQLDatabase()
logging.basicConfig(filename='./logs/errors.log', level=logging.ERROR, format='%(asctime)s - %(message)s',encoding='utf-8')
#State
USE_PROXY = True
RUN_APP = True