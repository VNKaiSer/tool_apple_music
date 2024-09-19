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

LINK_ERR_NO_TRIAL = "https://messenger.sideline.com/error-status/2201"
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
    driver.get("https://messages.sideline.com/accountSettings") 
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
        WebDriverWait(sc_modal, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-title')))
        modal_title = sc_modal.find_element(By.CLASS_NAME, "modal-title")
        print(modal_title.text)
        if modal_title.text == "Well, That Didn't Work...":
            if send_delete_change_pass == False:
                db_instance.result_acc_sideline_change_password(data['username'], "Didnt Work")
            driver.quit()
            return
    except Exception as e:
        print()
    logger.info(f'Change password: SUCCESS {new_pass} for user: {data["username"]}')
    if send_delete_change_pass == False:
        db_instance.change_password_sideline(data['username'], new_pass)
    else: 
        db_instance.change_password_sideline_base(data['username'], new_pass)
    driver.quit()
    return
def generate_phone_number():
    area_codes = [
        201, 202, 205, 207, 213, 214, 224, 225, 227, 228, 240, 248, 252, 256, 267, 270, 
  279, 302, 304, 307, 312, 326, 330, 337, 369, 380, 385, 386, 402, 405, 406, 410, 
  415, 424, 425, 430, 440, 445, 458, 464, 478, 479, 484, 501, 505, 507, 509, 518, 
  530, 531, 551, 559, 564, 567, 570, 573, 575, 585, 601, 603, 605, 606, 608, 609, 
  618, 619, 626, 629, 650, 656, 657, 659, 662, 681, 682, 706, 707, 712, 724, 728, 
  734, 740, 743, 747, 757, 763, 769, 774, 775, 781, 785, 802, 803, 804, 805, 812, 
  814, 815, 840, 843, 845, 847, 848, 856, 859, 860, 863, 864, 870, 903, 908, 910, 
  941, 947, 951, 970, 978, 989
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
        acc_get = db_instance.get_acc_sideline()
        time.sleep(2)
    else:
        acc_get = db_instance.get_acc_sideline_change_password()
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
        except:
            time_reload += 1
            driver.refresh()
            if time_reload == 2:
                db_instance.update_rerun_acc_sideline(username)
                driver.quit()
                return
    
    driver.switch_to.default_content()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
    driver.get("https://messages.sideline.com/conversation/empty") 
    
    time_reload = 0
    after_assigned_number = ""
    while after_assigned_number == "":
        try:
            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'assigned-number')))
            after_assigned_number = driver.find_element(By.CLASS_NAME, 'assigned-number').text
            phone = re.sub(r'\D', '', after_assigned_number)
            db_instance.update_phone_acc_sideline(username, phone);
            assigned_number = re.sub(r'\D', '', assigned_number)    
            print(assigned_number)
            after_assigned_number = re.sub(r'\D', '', after_assigned_number)
            print(after_assigned_number)
            if assigned_number != after_assigned_number:
                db_instance.result_acc_sideline(username, "no sent text")
                driver.quit()
                return
        except:
            time_reload += 1
            driver.refresh()
            if time_reload == 2:
                db_instance.update_rerun_acc_sideline(username)
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
            db_instance.result_acc_sideline(username, "NoTrial")
            driver.quit()
            return
        db_instance.result_acc_sideline(username, current_url)
        driver.quit()
        return
    
    # Kiểm tra invalid phone
    while True:
        try:
            time.sleep(1)
            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'textarea')))
            input_message = driver.find_element(By.TAG_NAME, "textarea")
            time.sleep(1)
            input_message.clear()
            input_message.send_keys(' ')
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'sc-chat-error-message')))
            sc_chat_error_message = driver.find_element(By.TAG_NAME, "sc-chat-error-message")
            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'input')))
            input_phone = driver.find_element(By.TAG_NAME, "input") 
            time.sleep(1) 
            input_phone_func(input_phone, data)
        except:
            break
    
    try:
        WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'textarea')))
        input_message = driver.find_element(By.TAG_NAME, "textarea")
        time.sleep(1)
        input_message.clear()
        input_message.send_keys(random_message())
        time.sleep(0.5)
        input_message.send_keys(Keys.ENTER)
    except:
        db_instance.update_rerun_acc_sideline(username)
        driver.quit()
        return
    
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
                db_instance.result_acc_sideline(username, "Didnt Work")
                driver.quit()
                return
            else:
                if change_password:
                    db_instance.update_rerun_acc_sideline_change_password(username)
                    driver.quit()
                    return
                else :
                    db_instance.update_rerun_acc_sideline(username)
                    driver.quit()
                    return
        
        db_instance.result_acc_sideline(username, modal_title.text)
        driver.quit()
        return
    except:
        print('')
    
    if send_and_delete:
        delete_message_func(driver, data)
    db_instance.result_acc_sideline(username, "done")
    if change_password:
        change_password_func(driver, data, True)
    else:
        driver.quit()
    return

def get_phone_from_file():
    with open('./assets/data/phone-sideline.txt', 'r') as f:
        lines = f.readlines()
        return lines[random.randint(0, len(lines) - 1)].strip()
    
def input_phone_func(input_phone, data):
    time.sleep(1)
    input_phone.send_keys(get_phone_from_file())
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
        
        random_port = random.randint(14150,14174)
        proxy = f'zeus.p.shifter.io:{random_port}'
        chrome_options = Options()
        chrome_options.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(
            options=chrome_options,
        )
        
        driver.get("https://messages.sideline.com/login")
        time.sleep(2)
        webdriver.ActionChains(driver).send_keys(Keys.F12).perform()
        time.sleep(2)
        
        # Mở tab mới
        try:
            root_tab = driver.current_window_handle
            driver.execute_script("window.open('https://www.google.com', '_blank');")
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)
            driver.switch_to.window(root_tab)
        except Exception as e:
            if change_password:
                db_instance.update_rerun_acc_sideline_change_password(username)
                driver.quit()
                return
            else :
                db_instance.update_rerun_acc_sideline(username)
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
                    err = "invalid phone" if wrong_password == "Please enter a valid phone number." else "sai pass"
                    if err == "sai pass":
                        try: 
                            WebDriverWait(app_root, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/ion-app/main/div/ion-router-outlet/app-login/ion-content/div/form/ion-grid/ion-row[3]/ion-col[2]/ion-item/a')))
                            driver.find_element(By.XPATH, '/html/body/app-root/ion-app/main/div/ion-router-outlet/app-login/ion-content/div/form/ion-grid/ion-row[3]/ion-col[2]/ion-item/a').click()
                            WebDriverWait(app_root, 15).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/ion-app/ion-modal/sc-modal/div/div/div/div/div[1]/h5')))
                            title = driver.find_element(By.XPATH, '/html/body/app-root/ion-app/ion-modal/sc-modal/div/div/div/div/div[1]/h5').text
                            err = "sai pass"
                        except:
                            err = "invalid phone"
                    if not change_password:
                        db_instance.result_acc_sideline(username, err)
                    else:
                        db_instance.result_acc_sideline_change_password(username, err)
                    driver.quit()
                    return
            except Exception as e:
                print()
            time.sleep(2)
            webdriver.ActionChains(driver).send_keys(Keys.F12).perform()
            time.sleep(2)
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
                            db_instance.update_rerun_acc_sideline(username)
                        else:
                            db_instance.update_rerun_acc_sideline_change_password(username)
                if ex == "Business Registration Incomplete":
                    print("no sub")
                    if not change_password:
                        db_instance.result_acc_sideline(username, "no sub")
                    else:
                        db_instance.result_acc_sideline_change_password(username, "no sub")
                    driver.quit()
                    return
                if ex == "Subscription Required":
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/ion-app/ion-modal/sc-modal/div/div/div/div/div[2]/p')))
                    sub_text = driver.find_element(By.XPATH, '/html/body/app-root/ion-app/ion-modal/sc-modal/div/div/div/div/div[2]/p').text
                    print(sub_text)
                    if sub_text == "You need an active subscription to use Sideline Web Messaging.\n\nGo to the mobile app and upgrade your account to continue.":
                        print("no sub")
                        if not change_password:
                            db_instance.result_acc_sideline(username,"no sub")
                        else:
                            db_instance.result_acc_sideline_change_password(username,"no sub")
                    driver.quit()
                    return
            except Exception as e:
                break
        
        # Tắt modal sync 
        try: 
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'SyncContactsXDismissPopup')))
            btn_close = driver.find_element(By.ID, 'SyncContactsXDismissPopup')
            btn_close.click()
        except Exception as e:
            print()
        
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
            db_instance.result_acc_sideline(username, "live")
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
            db_instance.update_rerun_acc_sideline(username)
        else:
            db_instance.update_rerun_acc_sideline_change_password(username)
