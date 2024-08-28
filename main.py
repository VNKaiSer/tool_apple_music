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
from concurrent.futures import ThreadPoolExecutor
from enums.apple_music_login_enum import AppleMusicLogin
sys.path.append('./commands')
from commands.const import *
# DEFINE 
send_message_var = None
delete_message_var = None
change_password_var = None
send_and_delete_var = None
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
        query = "SELECT user, password, card_add FROM mail WHERE exception = 'Done'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def export_error_id(self, error):
        query = None
        if error == 'country':
            query = "SELECT user, password, card_add,country FROM mail WHERE country IS NOT NULL"
            self.cursor.execute(query)
        elif error == 'all':
            query = "SELECT user, password,card_add, exception FROM mail"
            self.cursor.execute(query) 
        else:
            query = "SELECT user, password,card_add FROM mail WHERE exception = %s"
            self.cursor.execute(query, (error,))

        result = self.cursor.fetchall()
        self.connection.commit()
        return result

    def export_pay_success(self):
        query = "SELECT card_number, day, year, ccv FROM pay"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def analysis_pay_scusess(self):
        query = "SELECT card_number, `day`,`year`, ccv, number_use FROM pay WHERE number_use >= 1"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def export_error_pay(self, error):
        query = "SELECT card_number, `day`, `year`, number_use,exception FROM pay WHERE exception = %s"
        self.cursor.execute(query, (error,))

        result = self.cursor.fetchall()
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
        
    def analysis_acc_getindex(self):
        query = "SELECT user_name, password,ex, phone FROM get_index_tool WHERE is_running = 'Y' order by ex desc"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def analysis_acc_getindex_change_password(self):
        query = "SELECT user_name, password,ex FROM IndexChangePass WHERE is_running = 'Y' order by ex desc"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
        
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
from utils import import_acc_getindex
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
def add_getindex(change_password = False):
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                import_acc_getindex.process_data(change_password ,content)
                messagebox.showinfo("Thành công", "Thêm dữ liệu thành công")
                
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
def login_apple_music_run(combo , option: StringVar):
    def run(option):
        if option == AppleMusicLogin.CHECK.value:
            print("Login check")
            subprocess.Popen("py ./commands/run_apple_music_login.py --actions login_check")
            
        elif option == AppleMusicLogin.DELETE.value:
            print("Login delete")
            subprocess.Popen("py ./commands/run_apple_music_login.py --actions login_delete")
            
        elif option == AppleMusicLogin.ADD.value:
            print("Login add")
            subprocess.Popen("py ./commands/run_apple_music_login.py --actions login_add")
        else:
            return
            
            
    
    time_run = int(combo.get())
    with ThreadPoolExecutor(max_workers=time_run) as executor:
        for i in range(time_run):
            executor.submit(run(option.get()))
            time.sleep(10)
    root.deiconify()
    
def run_apple_music_login():
    dialog = tk.Toplevel(root)
    dialog.title("Nhập số lượng tab")

    label = ttk.Label(dialog, text="Chọn số lượng tab cần chạy:")
    label.pack(padx=10, pady=10)

    combo = ttk.Combobox(dialog, values=list(range(10, 31)))
    combo.pack(padx=10, pady=10)
    combo.current(0)

    option_var = tk.StringVar(value="Login check")
    
    run_check_option = ttk.Radiobutton(dialog, text="Login check", variable=option_var, value=AppleMusicLogin.CHECK.value)
    run_check_option.pack(anchor='w',padx=10, pady=5)
    
    run_delete_option = ttk.Radiobutton(dialog, text="Login delete", variable=option_var, value=AppleMusicLogin.DELETE.value)
    run_delete_option.pack(anchor='w',padx=10, pady=5)

    run_add_option = ttk.Radiobutton(dialog, text="Login add", variable=option_var, value=AppleMusicLogin.ADD.value)
    run_add_option.pack(anchor='w',padx=10, pady=5)
    
    confirm_button = ttk.Button(dialog, text="Xác nhận", command=lambda:login_apple_music_run(combo, option_var))
    confirm_button.pack(anchor='w',padx=10, pady=10)

def apple_id_tool():
    dialog = tk.Toplevel(root)
    dialog.title("Nhập số lượng tab")

    label = ttk.Label(dialog, text="Chọn số lượng tab cần chạy:")
    label.pack(anchor='w', padx=10, pady=5)

    global combo
    combo = ttk.Combobox(dialog, values=list(range(10, 31)))
    combo.pack(anchor='w', padx=10, pady=5)
    combo.current(0)

    change_secury_question_var = tk.BooleanVar()
    change_secury_question_checkbox = ttk.Checkbutton(dialog, text="Đổi câu hỏi bảo mật", variable=change_secury_question_var)
    change_secury_question_checkbox.pack(anchor='w', padx=10, pady=5)
    
    change_region_var = tk.BooleanVar()
    change_region_checkbox = ttk.Checkbutton(dialog, text="Đổi quốc gia", variable=change_region_var)
    change_region_checkbox.pack(anchor='w', padx=10, pady=5)

    change_password_var = tk.BooleanVar()
    change_password_checkbox = ttk.Checkbutton(dialog, text="Đổi mật khẩu", variable=change_password_var)
    change_password_checkbox.pack(anchor='w', padx=10, pady=5)
    
    add_payment_var = tk.BooleanVar()
    add_payment_checkbox = ttk.Checkbutton(dialog, text="Add thẻ", variable=add_payment_var)
    add_payment_checkbox.pack(anchor='w', padx=10, pady=5)

    confirm_button = ttk.Button(dialog, text="Xác nhận", command=lambda: get_index(combo, change_secury_question_var, change_region_var, change_password_var, add_payment_var))
    confirm_button.pack(anchor='w', padx=10, pady=10)
    
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
            data_export = db_instance.export_error_id(err) if err != "done" else db_instance.analysis_id_scusess()
            if file_path:
                with open(file_path, 'w') as file:
                    for data in data_export:
                        if len(data) >= 4:
                            file.write(data[0] + '|' + data[1] + '|' + (data[2] if data[2] != None else 'non_add') +'|' +(data[3] if data[3] != None else 'non_nuse') + '\n')
                        else:
                            file.write(data[0] + '|' + data[1] + '|' + (data[2] if data[2] != None else 'non_add') +'|' + err + '\n')
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
    label = Label(analysis_frame, text="Chọn keyword muốn xuất:", font=("Arial", 20), bg="white")
    label.pack(pady=5)
    options = ["Diss", "UnLock", "add sup", "2FA", "SaiPass","country","all","done"]

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
def export_acc_getindex(change_password):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                for data in db_instance.analysis_acc_getindex() if change_password == False else db_instance.analysis_acc_getindex_change_password ():
                    ex = "Unknown" if data[2] is None else  data[2] 
                    file.write(data[0] + '|' + data[1] + '|' + str(data[3])+ '|' + ex + '\n')
                messagebox.showinfo("Thông báo", "Xuất dữ liệu thành công")
                subprocess.Popen(['notepad.exe', file_path])
    except Exception as e:
        print(e)
        messagebox.showerror("Thông báo", "Error: Xuất dữ liệu thất bại")
        
import json
def handle_onpen_tool():
    with open('./config/tool-config.json', 'r+') as f:
        data = json.load(f)
        RUN_APP = data['RUN']
        
        if RUN_APP == False:
            RUN_APP = True
            data['RUN'] = RUN_APP
            f.seek(0)  # Đặt con trỏ tệp về đầu
            f.write(json.dumps(data, indent=4))  # Ghi dữ liệu mới
            f.truncate()  # Xóa nội dung còn lại nếu có
            messagebox.showinfo("Thông báo", "Mở tool thành công hãy thực hiện chức năng")
        else: 
            RUN_APP = False
            data['RUN'] = RUN_APP
            f.seek(0)  # Đặt con trỏ tệp về đầu
            f.write(json.dumps(data, indent=4))  # Ghi dữ liệu mới
            f.truncate()  # Xóa nội dung còn lại nếu có
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
        # while True:
        if choice == 0:
            subprocess.Popen("py ./commands/reg_music.py")
        elif choice == 1:
            subprocess.Popen("py ./commands/reg_music_add.py")
        else:
            subprocess.Popen("py ./commands/reg_music_add_apple.py") 

    def on_click_reg_apple_music():
        num_tabs = int(spinbox.get())
        selected_function = selected_value.get()
        
        with ThreadPoolExecutor(max_workers=num_tabs) as executor:
            for i in range(num_tabs):
                time.sleep(10)
                executor.submit(run, options.index(selected_function))
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
def run_app_tv():
    def run(choice):
        # while True:
        if choice == 0:
            subprocess.Popen("py ./commands/tv_login_check.py")
        elif choice == 1:
            subprocess.Popen("py ./commands/tv_login_delete.py")
        else:
            subprocess.Popen("py ./commands/tv_login.py") 

    def on_click_reg_apple_music():
        num_tabs = int(spinbox.get())
        selected_function = selected_value.get()
        
        with ThreadPoolExecutor(max_workers=num_tabs) as executor:
            for i in range(num_tabs):
                time.sleep(10)
                executor.submit(run, options.index(selected_function))
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
    options = ["Login check", "Login delete", "Login add"]

    selected_value = StringVar(analysis_frame)
    selected_value.set(options[0])

    option_menu = OptionMenu(analysis_frame, selected_value, *options)
    option_menu.pack(pady=7)

    submit_btn = Button(analysis_frame, text="Chạy", command=on_click_reg_apple_music)
    submit_btn.pack(pady=10)
def get_index(send_message_var, delete_message_var, change_password_var, check_live_var, send_and_delete_var):
    def run(send_message_var, delete_message_var, change_password_var, check_live_var,send_and_delete_var):
        if send_message_var.get() and delete_message_var.get() :
            print("send and delete")
            subprocess.Popen("py ./commands/login_getindex.py --actions send_and_delete")
            
        elif send_message_var.get():
            print("send message")
            subprocess.Popen("py ./commands/login_getindex.py --actions send_message")
            
        elif delete_message_var.get():
            print("delete message")
            subprocess.Popen("py ./commands/login_getindex.py --actions delete_message")
        elif send_and_delete_var.get() and change_password_var.get():
            print("send and delete and change password")
            subprocess.Popen("py ./commands/login_getindex.py --actions send_delete_change_pass")
        elif change_password_var.get():
            print("change password")
            subprocess.Popen("py ./commands/login_getindex.py --actions change_password")
        elif check_live_var.get():
            print("check live")
            subprocess.Popen("py ./commands/login_getindex.py --actions check_live")
        elif send_and_delete_var.get():
            print("send and delete")
            subprocess.Popen("py ./commands/login_getindex.py --actions delete_after_send")
        else:
            return
            
            
    
    time_run = int(combo.get())
    with ThreadPoolExecutor(max_workers=time_run) as executor:
        for i in range(time_run):
            executor.submit(run(send_message_var, delete_message_var, change_password_var, check_live_var,send_and_delete_var))
            time.sleep(10)
    root.deiconify()
    
    
def reg_apple_tv():
    def run():
        subprocess.Popen("py ./commands/reg_apple_tv_add.py")

    def on_click_reg_apple_tv():
        num_tabs = int(spinbox.get())
        selected_function = selected_value.get()
        
        with ThreadPoolExecutor(max_workers=num_tabs) as executor:
            for i in range(num_tabs):
                executor.submit(run)
                time.sleep(10)
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
    options = ["Tạo"]

    selected_value = StringVar(analysis_frame)
    selected_value.set(options[0])

    option_menu = OptionMenu(analysis_frame, selected_value, *options)
    option_menu.pack(pady=7)

    submit_btn = Button(analysis_frame, text="Chạy", command=on_click_reg_apple_tv)
    submit_btn.pack(pady=10)

# def 

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
def handle_proxy():
    global USE_PROXY
    if USE_PROXY == True:
        USE_PROXY = False
        messagebox.showinfo("Thông báo", "Tắt proxy thành công")
    else:
        USE_PROXY = True
        messagebox.showinfo("Thông báo", "Mở proxy thành công")
        
import tkinter as tk
def center_window(window):
    # Lấy kích thước của màn hình
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Tính toán vị trí của cửa sổ Toplevel để nằm chính giữa màn hình
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Đặt vị trí của cửa sổ
    window.geometry(f"+{x}+{y}")

def handle_add_card():
    # Tạo cửa sổ con
    add_card_window = tk.Toplevel(root)
    add_card_window.title("Nhập số lần add thẻ")
    
    # Đặt cửa sổ con ở giữa màn hình
    center_window(add_card_window)

    # Tạo nhãn hướng dẫn
    label = tk.Label(add_card_window, text="Nhập số lần add thẻ:")
    label.pack(pady=10)

    # Tạo ô nhập
    entry = tk.Entry(add_card_window)
    entry.pack(pady=5)

    # Hàm xác nhận
    def on_confirm():
        try:
            # Lấy giá trị từ ô nhập
            user_input = int(entry.get())
            f = open('./config/tool-config.json', 'r')
            data = json.load(f)
            f.close()
            data['TIME_ADD_CARD'] = user_input
            f = open('./config/tool-config.json', 'w')
            f.seek(0)  # Đặt con trỏ tệp về đầu
            f.write(json.dumps(data, indent=4))  # Ghi dữ liệu mới
            f.truncate()  # Xóa nội dung còn lại nếu có
            f.close()
            # Hiển thị thông báo với giá trị nhập vào
            messagebox.showinfo("Xác nhận", f"Số lần add thẻ: {user_input}")
            add_card_window.destroy()  # Đóng cửa sổ con sau khi xác nhận
        except ValueError:
            # Hiển thị thông báo lỗi nếu giá trị nhập vào không phải là số
            messagebox.showerror("Lỗi", "Vui lòng nhập một số hợp lệ")

    # Tạo nút xác nhận
    button = tk.Button(add_card_window, text="Xác nhận", command=on_confirm)
    button.pack(pady=20)
    
from tkinter import ttk
def show_dialog():
    dialog = tk.Toplevel(root)  
    dialog.title("Nhập số lượng tab")

    label = ttk.Label(dialog, text="Chọn số lượng tab cần chạy:")
    label.pack(padx=10, pady=10)

    # Combobox cho phép chọn số từ 10-30
    global combo
    combo = ttk.Combobox(dialog, values=list(range(10, 31)))
    combo.pack(padx=10, pady=10)
    combo.current(0)

    # Checkbox for "Xoá tin nhắn"
    global delete_message_var
    delete_message_var = tk.BooleanVar()
    delete_message_checkbox = ttk.Checkbutton(dialog, text="Xoá tin nhắn", variable=delete_message_var)
    delete_message_checkbox.pack(anchor='w',padx=10, pady=5)
    
    global send_message_var
    send_message_var = tk.BooleanVar()
    send_message_checkbox = ttk.Checkbutton(dialog, text="Gửi tin nhắn", variable=send_message_var)
    send_message_checkbox.pack(anchor='w',padx=10, pady=5)

    # Checkbox for "Đổi mật khẩu"
    global change_password_var
    change_password_var = tk.BooleanVar()
    change_password_checkbox = ttk.Checkbutton(dialog, text="Đổi mật khẩu", variable=change_password_var)
    change_password_checkbox.pack(anchor='w',padx=10, pady=5)
    
    global check_live_var
    check_live_var = tk.BooleanVar()
    check_live_checkbox = ttk.Checkbutton(dialog, text="Check live", variable=check_live_var)
    check_live_checkbox.pack(anchor='w',padx=10, pady=5)
    
    global send_and_delete_var 
    send_and_delete_var = tk.BooleanVar()
    send_and_delete_checkbox = ttk.Checkbutton(dialog, text="Gửi xong xoá", variable=send_and_delete_var)
    send_and_delete_checkbox.pack(anchor='w',padx=10, pady=5)

    confirm_button = ttk.Button(dialog, text="Xác nhận", command=lambda:get_index(send_message_var,delete_message_var, change_password_var, check_live_var,send_and_delete_var))
    confirm_button.pack(padx=10, pady=10)


def handle_user_trick_get_index():
    def confirm_choice(choice):
        with open('./config/tool-config.json', 'r+') as f:
            data = json.load(f)
            print(choice)
            if choice == "1":
                data['GET_INDEX_TRICK'] = True
                f.seek(0)  # Đặt con trỏ tệp về đầu
                f.write(json.dumps(data, indent=4))  # Ghi dữ liệu mới
                f.truncate()  # Xóa nội dung còn lại nếu có
                messagebox.showinfo("Thông báo", "Đã cấu hình sử dụng trick")
            else: 
                data['GET_INDEX_TRICK'] = False
                f.seek(0)  # Đặt con trỏ tệp về đầu
                f.write(json.dumps(data, indent=4))  # Ghi dữ liệu mới
                f.truncate()  # Xóa nội dung còn lại nếu có
                messagebox.showinfo("Thông báo", "Huỷ cấu hình sử dụng trick")
                
    dialog = tk.Toplevel(root)  
    dialog.title("Cài đặt trick cho getindex")
    
    # Tạo biến để lưu giá trị lựa chọn
    choice_var = tk.StringVar(value="Option1")
    
    # Tạo Radiobuttons
    radio1 = tk.Radiobutton(dialog, text="Dùng trick", variable=choice_var, value="1")
    radio2 = tk.Radiobutton(dialog, text="Không", variable=choice_var, value="2")
    
    # Đặt vị trí cho các Radiobuttons
    radio1.pack(anchor=tk.W, padx=10, pady=5)
    radio2.pack(anchor=tk.W, padx=10, pady=5)
    
    # Tạo nút xác nhận
    confirm_button = tk.Button(dialog, text="Xác nhận", command=lambda: confirm_choice(choice_var.get()))
    confirm_button.pack(pady=10)

    

    # dialog.destroy()

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
add_data_menu.add_command(label='Thêm acc getindex', command=lambda:add_getindex(change_password=False))
add_data_menu.add_command(label='Thêm acc getindex change_pass', command=lambda:add_getindex(change_password=True))

featuremenu = Menu(menu)
menu.add_cascade(label='Chức năng', menu=featuremenu)
featuremenu.add_command(label='Tool login apple music', command=run_apple_music_login)
featuremenu.add_separator()
featuremenu.add_command(label='Reg apple music', command=reg_apple_music)
featuremenu.add_separator()
featuremenu.add_command(label='Reg apple tv', command=reg_apple_tv)
featuremenu.add_separator()
featuremenu.add_command(label='Tv login', command=run_app_tv)
featuremenu.add_separator()
featuremenu.add_command(label='Get index tool', command=show_dialog)
featuremenu.add_separator()
featuremenu.add_command(label='Apple id tool', command=apple_id_tool)

analysis_menu = Menu(menu)
menu.add_cascade(label='Thống kê', menu=analysis_menu)
analysis_menu.add_command(label='Xuất id theo keyword', command=open_analysis)
analysis_menu.add_command(label='Xuất thẻ thành công', command=export_success_pay)
analysis_menu.add_command(label='Xuất thẻ thất bại', command=open_error_pay)
analysis_menu.add_command(label='Xuất thẻ thẻ login check', command=export_login_check_id)
analysis_menu.add_command(label='Xuất thẻ thẻ login delete', command=export_login_delete_id)
analysis_menu.add_separator()

analysis_menu.add_command(label='Xuất acc getindex', command=lambda:export_acc_getindex(change_password=False))
analysis_menu.add_command(label='Xuất acc getindex change_pass', command=lambda:export_acc_getindex(change_password=True))

setting_menu = Menu(menu)
menu.add_cascade(label='Cài đặt', menu=setting_menu)
setting_menu.add_command(label='Mở/Đóng tool', command=handle_onpen_tool)
setting_menu.add_separator()
setting_menu.add_command(label='Bật/Tắt proxy', command=handle_proxy)
setting_menu.add_command(label='Số lần add thẻ', command=handle_add_card)
setting_menu.add_command(label='Trick GetIndex', command=handle_user_trick_get_index)


exit_menu = Menu(menu)
menu.add_cascade(label='Exit', menu=exit_menu)
exit_menu.add_command(label='Exit', command=close_app)

mainloop()


