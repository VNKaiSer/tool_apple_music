import datetime
import re
from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import sys
import time 
import random
from faker import Faker
fake = Faker(locale='en_US')
from selenium.webdriver.common.action_chains import ActionChains
import logging
logger = logging.getLogger("Change-password")
logger.setLevel(logging.DEBUG)

WAIT_CHILD = 30
WAIT_START = 60
from const import json
from const import db_instance
from const import datetime, timedelta
# Create handlers for logging to the standard output and a file
stdoutHandler = logging.StreamHandler(stream=sys.stdout)
errHandler = logging.FileHandler("./logs/change-pass.log")

# Set the log levels on the handlers
stdoutHandler.setLevel(logging.DEBUG)
errHandler.setLevel(logging.ERROR)

# Create a log format using Log Record attributes
fmt = logging.Formatter(
    "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
)

# Set the log format on each handler
stdoutHandler.setFormatter(fmt)
errHandler.setFormatter(fmt)

# Add each handler to the Logger object
logger.addHandler(stdoutHandler)
logger.addHandler(errHandler)

LINK_ERR_NO_TRIAL = "https://app.getindex.com/error-status/2201"
ERR_RENEW = "Subscription has expired"
ERR_NOSUB = "Subscription Required"
def delete_message_func(driver : webdriver, data):
        WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.TAG_NAME, 'conversation-list')))
        conversation_list = driver.find_element(By.TAG_NAME, 'conversation-list')
        try:
            while len(conversation_list.find_elements(By.TAG_NAME, 'ion-item-sliding')) > 0:
                WebDriverWait(conversation_list, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'ion-item-sliding')))
                conversation = conversation_list.find_element(By.TAG_NAME, 'ion-item-sliding')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'bulkEditButton')))
                btn_edit = driver.find_element(By.ID, 'bulkEditButton')
                btn_edit.click()
                time.sleep(1)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'sc-button')))
                btns = driver.find_elements(By.TAG_NAME, 'sc-button')
                btns[2].click()
                time.sleep(1)
                btns[1].click()
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'sc-modal')))
                sc_modal = driver.find_element(By.TAG_NAME, "sc-modal")
                WebDriverWait(sc_modal, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'sc-button')))
                btns = sc_modal.find_elements(By.TAG_NAME, 'sc-button')
                btns[1].click()
                time.sleep(5)
                
        except Exception as e:
            print() 

def generate_random_password_index():
    return 'ALi' + fake.password(length=4, special_chars=False, digits=True, upper_case=True, lower_case=True) + '@';

def change_password_func(driver: webdriver, data, send_delete_change_pass = False):
    driver.get("https://app.getindex.com/accountSettings") 
    actions = ActionChains(driver)
    WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, "ion-item-group")))
    form_update_pass = driver.find_elements(By.TAG_NAME, "ion-item-group")
    actions.move_to_element(form_update_pass[1]).perform()
    print(len(form_update_pass))
    WebDriverWait(form_update_pass[1], WAIT_CHILD).until(EC.visibility_of_element_located((By.TAG_NAME, "ion-input")))
    labels = form_update_pass[1].find_elements(By.TAG_NAME, "ion-input")
   
   
        
    actions.move_to_element(labels[0]).click().perform()
    new_pass = generate_random_password_index()
    logger.info(f'Change password: {new_pass} for user: {data["username"]}, old_pass: {data["password"]}')
    time.sleep(0.3)
    driver.switch_to.active_element.send_keys(data['password'])
    time.sleep(0.3)
    
    actions.move_to_element(labels[1]).click().perform()
    time.sleep(0.3)
    driver.switch_to.active_element.send_keys(new_pass)
    time.sleep(0.3)
    
    actions.move_to_element(labels[2]).click().perform()
    time.sleep(0.3)
    driver.switch_to.active_element.send_keys(new_pass)
    time.sleep(1)
    driver.switch_to.default_content()
    
    # Nhấn nút save
    WebDriverWait(driver, WAIT_CHILD).until(EC.visibility_of_element_located((By.TAG_NAME, "ion-header")))
    header = driver.find_elements(By.TAG_NAME, "ion-header")[1]
    WebDriverWait(header, WAIT_CHILD).until(EC.visibility_of_element_located((By.TAG_NAME, "ion-button")))
    btns = header.find_elements(By.TAG_NAME, "ion-button")
    btns[1].click()
    
    try: 
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'sc-modal')))
        sc_modal = driver.find_element(By.TAG_NAME, "sc-modal")
        WebDriverWait(sc_modal, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-title')))
        modal_title = sc_modal.find_element(By.CLASS_NAME, "modal-title")
        print(modal_title.text)
        if modal_title.text == "Well, That Didn't Work...":
            if send_delete_change_pass == False:
                db_instance.result_acc_getindex_change_password(data['username'], "Didnt Work")
            driver.quit()
            return
    except Exception as e:
        print()
    logger.info(f'Change password: SUCCESS {new_pass} for user: {data["username"]}')
    if send_delete_change_pass == False:
        db_instance.change_password_get_index(data['username'], new_pass)
    else: 
        db_instance.change_password_get_index_i(data['username'], new_pass)
    driver.quit()
    return
def generate_phone_number():
    area_codes = [
        205, 251, 256, 334, 659, 938, 907, 480, 520, 602, 623, 928,
        479, 501, 870, 209, 213, 279, 310, 341, 350, 408, 415,
        424, 442, 510, 530, 559, 562, 619, 626, 628, 650, 657, 661,
        669, 707, 714, 747, 760, 805, 818, 820, 831, 840, 858, 909,
        916, 925, 949, 951, 303, 719, 720, 970, 983, 203, 475, 860,
        959, 239, 305, 321, 352, 386, 407, 448, 561, 656, 689, 727,
        754, 772, 786, 813, 850, 863, 904, 941, 954, 229, 404, 470,
        478, 678, 706, 762, 770, 912, 943
    ]
    area_code = random.choice(area_codes)
    central_office_code = random.randint(200, 999)
    line_number = random.randint(1000, 9999)
    return f"{area_code}{central_office_code}{line_number}"
def random_message():
    return 'ALiCheck' + fake.password(length=4, special_chars=False, digits=True, upper_case=True, lower_case=True)

def extract_date(text):
    match = re.search(r"\b\w+ \d{1,2}, \d{4} \d{1,2}:\d{2} \wM\b", text)
    if match:
        date_str = match.group(0)
        date_obj = datetime.strptime(date_str, "%b %d, %Y %I:%M %p")
        return date_obj.strftime("%d/%m/%Y")
    return None

def getData(change_pass):
    if not change_pass:
        acc_get = db_instance.get_acc_get_index()
        time.sleep(2)
    else:
        acc_get = db_instance.get_acc_get_index_change_password()
        time.sleep(2)
    if acc_get == '':
        return None
    username = acc_get[1]
    password = acc_get[2]
    return username, password
def send_message_func(driver: webdriver, username, data, send_and_delete = False, change_password = False):
    assigned_number = ""
    # Kiểm tra no sent text
    time_reload = 0
    while assigned_number == "":
        try:
            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'assigned-number')))
            assigned_number = driver.find_element(By.CLASS_NAME, 'assigned-number').text
            print(assigned_number)
        except:
            time_reload += 1
            driver.refresh()
            if time_reload == 2:
                db_instance.update_rerun_acc_get_index(username)
                driver.quit()
                return
    
    driver.switch_to.default_content()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
    driver.get("https://app.getindex.com/conversation/empty") 
    
    time_reload = 0
    after_assigned_number = ""
    while after_assigned_number == "":
        try:
            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'assigned-number')))
            after_assigned_number = driver.find_element(By.CLASS_NAME, 'assigned-number').text
            phone = re.sub(r'\D', '', after_assigned_number)
            db_instance.update_phone_acc_getindex(username, phone);
            assigned_number = re.sub(r'\D', '', assigned_number)    
            print(assigned_number)
            after_assigned_number = re.sub(r'\D', '', after_assigned_number)
            print(after_assigned_number)
            if assigned_number != after_assigned_number:
                db_instance.result_acc_getindex(username, "no sent text")
                driver.quit()
                return
        except:
            time_reload += 1
            driver.refresh()
            if time_reload == 2:
                db_instance.update_rerun_acc_get_index(username)
                driver.quit()
                return
        
        
    try:
        # Gửi tin nhắn
        
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
        input_phone = driver.find_element(By.TAG_NAME, "input")    
        input_phone_func(input_phone, data)
    except Exception as e:
        current_url = driver.current_url
        if current_url == LINK_ERR_NO_TRIAL:
            db_instance.result_acc_getindex(username, "NoTrial")
            driver.quit()
            return
        db_instance.result_acc_getindex(username, current_url)
        driver.quit()
        return
    
    # Kiểm tra số điện thoại có đúng k
    # while True:
    #     try:
    #         time.sleep(1)
    #         WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'textarea')))
    #         input_message = driver.find_element(By.TAG_NAME, "textarea")
    #         time.sleep(1)
    #         input_message.clear()
    #         input_message.send_keys(' ')
    #         WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'sc-chat-error-message')))
    #         sc_chat_error_message = driver.find_element(By.TAG_NAME, "sc-chat-error-message")
    #         WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
    #         input_phone = driver.find_element(By.TAG_NAME, "input") 
    #         time.sleep(1) 
    #         input_phone_func(input_phone, data)
    #     except:
    #         break
    
    # Kiểm tra lỗi Nosub 
    try:
        WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'textarea')))
        input_message = driver.find_element(By.TAG_NAME, "textarea")
        time.sleep(1)
        input_message.clear()
        input_message.send_keys(random_message())
        time.sleep(0.5)
        input_message.send_keys(Keys.ENTER)
    except:
        db_instance.update_rerun_acc_get_index(username)
    
    # Kiểm tra trường hợp hỗ trợ
    try:
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'sc-modal')))
        sc_modal = driver.find_element(By.TAG_NAME, "sc-modal")
        WebDriverWait(sc_modal, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-title')))
        modal_title = sc_modal.find_element(By.CLASS_NAME, "modal-title")
        print(modal_title.text)
        if modal_title.text == "Well, That Didn't Work...":
            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/ion-app/ion-modal/sc-modal/div/div/div/div/div[2]/p')))
            sc_chat_error_message = driver.find_element(By.XPATH, '/html/body/app-root/ion-app/ion-modal/sc-modal/div/div/div/div/div[2]/p')
            if sc_chat_error_message.text == "Sorry, something didn't go through. If the problem persists, please contact support.":
                db_instance.result_acc_getindex(username, "Didnt Work")
                driver.quit()
                return
            else:
                if change_password:
                    db_instance.update_rerun_acc_get_index_change_password(username)
                    driver.quit()
                    return
                else :
                    db_instance.update_rerun_acc_get_index(username)
                    driver.quit()
                    return
        
        db_instance.result_acc_getindex(username, modal_title.text)
        driver.quit()
        return
    except:
        print('')
    
    if send_and_delete:
        delete_message_func(driver, data)
    db_instance.result_acc_getindex(username, "done")
    if change_password:
        change_password_func(driver, data, True)
    else:
        driver.quit()
    return

def input_phone_func(input_phone, data):
    time.sleep(1)
    input_phone.send_keys(generate_phone_number())
    time.sleep(0.3)
    input_phone.send_keys(Keys.ENTER)
    time.sleep(1)
    
def login(change_password = False, send_message = False, delete_message = False, check_live = False, send_and_delete = False, send_delete_change_pass = False):
    data = None
    try:
        tmp = getData(change_password)
        if tmp is None:
            print("No acc! Input more acc.")
            return
        
        username, password = tmp
        data = {
            "username": username,
            "password": password,
            # "phone_send": generate_phone_number(),
        }
        logger.info(data)
        print(data)
        
        random_port = random.randint(20620,20644)
        #random_proxy = [
        #     {
        #     'proxy': {
        #         'https': 'https://adz56789:Zxcv123123=5@gate.dc.smartproxy.com:20000',
        #         'http': 'http://adz56789@Zxcv123123=5@gate.dc.smartproxy.com:20000',
        #         'no_proxy': 'localhost,127.0.0.1'
        #     },
        #     'mitm_http2': False
        # },
        # {'proxy': {'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225'}, 'mitm_http2': False}
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
        # {'proxy': {'https': 'https://zteam6789:Zxcv123123=5@gate.dc.smartproxy.com:20000'}, 'mitm_http2': False},
        # {'proxy': {
        #             'https': f'https://hermes.p.shifter.io:{random_port}',
        #             'http': f'http://hermes.p.shifter.io:{random_port}',
        #             'no_proxy': 'localhost,127.0.0.1'
        #         }, 'mitm_http2': False}
        # ]
        # proxy = random.choice(random_proxy)
        proxy = f'pallas.p.shifter.io:{random_port}'
        chrome_options = Options()
        # chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--allow-insecure-localhost')
        # chrome_options.add_argument('--ignore-ssl-errors=yes')
        # chrome_options.add_argument('--log-level=3')  # Selenium log level
        chrome_options.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(
            
            options=chrome_options,
            #seleniumwire_options=proxy,
            # service_log_path=os.path.devnull  # Chuyển hướng log của ChromeDriver
        )
        
        driver.get("https://messages.sideline.com/login")
        
        # Mở tab mới
        try:
            root_tab = driver.current_window_handle
            driver.execute_script("window.open('https://www.google.com', '_blank');")
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)
            driver.switch_to.window(root_tab)
        except Exception as e:
            if change_password:
                db_instance.update_rerun_acc_get_index_change_password(username)
                driver.quit()
                return
            else :
                db_instance.update_rerun_acc_get_index(username)
                driver.quit()
                return
        
        
        time_reload = 0
        while True:
            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
            app_root = driver.find_element(By.TAG_NAME, 'app-root')
            inputs = app_root.find_elements(By.TAG_NAME, "input")
            inputs[0].send_keys(data["username"])
            time.sleep(0.5)
            inputs[1].send_keys(data["password"])
            time.sleep(1)
            inputs[1].send_keys(Keys.ENTER)
            try:
                WebDriverWait(app_root, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'error-message')))
                wrong_password = driver.find_element(By.CLASS_NAME, 'error-message').text
                if wrong_password != "":
                    if not change_password:
                        # db_instance.result_acc_getindex(username, "sai pass")
                        print(wrong_password)
                    else:
                        print(wrong_password)
                        # db_instance.result_acc_getindex_change_password(username, "sai pass")
                    driver.quit()
                    return
            except Exception as e:
                print()
            try:    
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'sc-modal')))
                sc_modal = driver.find_element(By.TAG_NAME, "sc-modal")
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-title')))
                modal_title = driver.find_element(By.CLASS_NAME, "modal-title")
                print(modal_title.text)
                ex = modal_title.text
                if ex == "Well, That Didn't Work...":
                    if time_reload == 0:
                        time_reload = time_reload + 1
                        driver.execute_script("location.reload();")
                    else:
                        if not change_password:
                            print("rerun")
                            # db_instance.update_rerun_acc_get_index(username)
                        else:
                            print("rerun")
                            # db_instance.update_rerun_acc_get_index_change_password(username)
                if ex == "Business Registration Incomplete":
                    print("no sub")
                    if not change_password:
                        print("no sub")
                        # db_instance.result_acc_getindex(username, "no sub")
                    else:
                        print("no sub")
                        # db_instance.result_acc_getindex_change_password(username, "no sub")
                    driver.quit()
                    return
                if ex == "Subscription Required":
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/ion-app/main/top-bar/sc-info-bar/div/div/span')))
                    sub_text = driver.find_element(By.XPATH, '/html/body/app-root/ion-app/main/top-bar/sc-info-bar/div/div/span').text
                    if not change_password:
                        print("no sub " + extract_date(sub_text))
                        # db_instance.result_acc_getindex(username, "suspended " + extract_date(sub_text))
                    else:
                        print("no sub " + extract_date(sub_text))
                        # db_instance.result_acc_getindex_change_password(username, "no sub " + extract_date(sub_text))
                    driver.quit()
                    return
            except Exception as e:
                break
        
        try:
            action = ActionChains(driver)
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'number-expired')))
            frame_number_expired = driver.find_element(By.TAG_NAME, 'number-expired')
            print(frame_number_expired)
            WebDriverWait(frame_number_expired, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'button')))
            btn = frame_number_expired.find_element(By.TAG_NAME, 'button')
            action.move_to_element(btn).perform()
            time.sleep(0.5)
            btn.click()
            time.sleep(5)
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'number-selection')))
            frame_number_selection = driver.find_element(By.TAG_NAME, 'number-selection')
            spans = frame_number_selection.find_elements(By.TAG_NAME, 'span')
            print(len(spans))
            for span in spans:
                action.move_to_element(span).perform()
            time.sleep(0.5)
            btn = frame_number_selection.find_element(By.TAG_NAME, 'button')
            action.move_to_element(btn).perform()
            btn.click()
            time.sleep(5)
        except Exception as e:
            print()
            
        if check_live:
            db_instance.result_acc_getindex(username, "live")
            driver.quit()
            return        
        if change_password:
            change_password_func(driver, data)
        if delete_message:
            delete_message_func(driver,data)
        if send_and_delete:
            send_message_func(driver, username, data, send_and_delete)
            return
        if send_message:
            send_message_func(driver, username, data)
        if send_delete_change_pass:
            send_message_func(driver, username, data, send_and_delete=True, change_password=True)
        
    except Exception as e:
        if not change_password:
            db_instance.update_rerun_acc_get_index(username)
        else:
            db_instance.update_rerun_acc_get_index_change_password(username)

login(send_message=True)