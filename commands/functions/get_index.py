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
from selenium_stealth import stealth
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
from const import set_proxy
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
        WebDriverWait(sc_modal, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-title')))
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
        201, 202, 203, 205, 206, 207, 208, 209, 213, 214, 215, 216, 217, 218, 219, 220, 
  223, 224, 225, 227, 228, 229, 231, 234, 240, 248, 251, 252, 253, 254, 256, 260, 
  262, 267, 269, 270, 272, 276, 279, 281, 301, 302, 303, 304, 307, 308, 309, 310, 
  312, 313, 314, 315, 317, 318, 319, 320, 325, 326, 330, 331, 332, 334, 336, 337, 
  341, 346, 347, 350, 351, 352, 360, 361, 380, 385, 386, 401, 402, 404, 405, 406, 
  407, 408, 409, 410, 412, 413, 414, 415, 417, 419, 423, 424, 425, 430, 432, 434, 
  435, 440, 442, 443, 445, 448, 458, 470, 472, 475, 478, 479, 480, 484, 501, 502, 
  504, 505, 507, 508, 509, 510, 512, 513, 515, 516, 517, 518, 520, 530, 531, 539, 
  540, 541, 551, 559, 561, 562, 563, 564, 567, 570, 571, 573, 574, 575, 580, 585, 
  586, 601, 603, 605, 606, 607, 608, 609, 610, 614, 615, 616, 617, 618, 619, 620, 
  623, 626, 629, 630, 631, 636, 640, 641, 650, 651, 656, 657, 659, 661, 662, 667, 
  669, 678, 681, 689, 701, 704, 706, 707, 708, 712, 713, 714, 715, 716, 717, 719, 
  720, 724, 727, 731, 732, 734, 737, 740, 743, 747, 754, 757, 760, 762, 763, 765, 
  769, 772, 773, 774, 775, 779, 781, 785, 786, 802, 803, 804, 805, 806, 810, 812, 
  813, 814, 815, 816, 818, 828, 830, 831, 832, 835, 838, 839, 840, 843, 845, 848, 
  850, 856, 858, 859, 860, 862, 863, 864, 865, 870, 872, 878, 903, 904, 906, 908, 
  909, 910, 912, 913, 914, 915, 917, 918, 919, 920, 925, 928, 929, 930, 931, 936, 
  937, 938, 940, 941, 943, 945, 949, 951, 954, 956, 959, 970, 971, 973, 978, 979, 
  980, 984, 985, 986, 989
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
    
    while True:
        try:
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
        except:
            continue
    
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
        time.sleep(10)
        delete_message_func(driver, data)
    db_instance.result_acc_getindex(username, "done")
    if change_password:
        change_password_func(driver, data, True)
    else:
        driver.quit()
    return

def get_phone_from_file():
    with open('./assets/data/phone-index.txt', 'r') as f:
        lines = f.readlines()
        return lines[random.randint(0, len(lines) - 1)].strip()

def input_phone_func(input_phone, data):
    time.sleep(1)
    input_phone.send_keys(get_phone_from_file())
    time.sleep(0.3)
    input_phone.send_keys(Keys.ENTER)
    time.sleep(1)
def choice_user_agents():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    ]
    return random.choice(user_agents)
def login(change_password = False, send_message = False, delete_message = False, check_live = False, send_and_delete = False, send_delete_change_pass = False):
    data = None
    try:
        random_port = random.randint(16405,16429)
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
        proxy1 = f'atlas.p.shifter.io'
        proxy2= f'hades.p.shifter.io'
        proxy = random.choice([proxy1, proxy2])
        port = db_instance.get_port_proxy(proxy)
        
        if port == 0:
            if not change_password:
                db_instance.update_rerun_acc_get_index(username)
                return
            else:
                db_instance.update_rerun_acc_get_index_change_password(username)
                return    
        proxy = f'{proxy}:{port}'
        time.sleep(5)
        chrome_options = Options()
        # chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--allow-insecure-localhost')
        # chrome_options.add_argument('--ignore-ssl-errors=yes')
        # chrome_options.add_argument('--log-level=3')  # Selenium log level
        user_agent = choice_user_agents()
        chrome_options.add_argument(f'--proxy-server={proxy}')
        chrome_options.add_argument('--disable-webrtc')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Tắt phát hiện Selenium
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(
            options=chrome_options,
            #seleniumwire_options=proxy,
            # service_log_path=os.path.devnull  # Chuyển hướng log của ChromeDriver
        )
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
        # kiểm tra ip 
        try:
            driver.get("https://api.ipify.org/?format=json")

            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
            body_text = driver.find_element("tag name", "body").text

            ip_data = json.loads(body_text)
            current_ip = ip_data['ip']
            
            # Kiểm tra ip hiện tại trên db 
            ip_is_exist = db_instance.check_and_insert_proxy(current_ip)
            if ip_is_exist == False:
                driver.quit()
                return
        except Exception as e:
            driver.quit()
            return
        time.sleep(2)
        
        driver.get("https://app.getindex.com/login")
        root_tab = driver.current_window_handle
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
        
        # Mở tab mới
        # try:
        #     root_tab = driver.current_window_handle
        #     driver.execute_script("window.open('https://www.google.com', '_blank');")
        #     driver.switch_to.window(driver.window_handles[1])
        #     time.sleep(3)
        #     # driver.close()
        #     driver.switch_to.window(root_tab)
        # except Exception as e:
        #     if change_password:
        #         db_instance.update_rerun_acc_get_index_change_password(username)
        #         driver.quit()
        #         return
        #     else :
        #         db_instance.update_rerun_acc_get_index(username)
        #         driver.quit()
        #         return
        time.sleep(2)
        #Nhấn vào logo
        try: 
            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/ion-app/main/app-header/sc-header/ion-header/ion-toolbar/ion-grid/ion-row/ion-col[1]/ion-item/ion-img')))
            logo = driver.find_element(By.XPATH, '/html/body/app-root/ion-app/main/app-header/sc-header/ion-header/ion-toolbar/ion-grid/ion-row/ion-col[1]/ion-item/ion-img')
            action = ActionChains(driver)
            action.move_to_element(logo).perform()
            action.click(logo).perform()
            time.sleep(2)
            driver.implicitly_wait(5)
            time.sleep(5)
            driver.switch_to.window(root_tab)
            time.sleep(2)
        except:
            pass
            
        #     print('Đã click')
        #     # Chờ tab mới mở ra
        #     driver.implicitly_wait(5)
        #     time.sleep(5)
        #     driver.switch_to.window(root_tab)
        #     time.sleep(2)
        #     # # Chuyển qua tab mới
        #     # new_tab = [tab for tab in driver.window_handles if tab != root_tab][0]
        #     # driver.switch_to.window(new_tab)

        #     # # Đóng tab mới
        #     # driver.close()
        #     # driver.switch_to.window(driver.window_handles[1])
        #     # driver.close()
        #     # driver.switch_to.window(root_tab)
        # except:
        #     if change_password:
        #         db_instance.update_rerun_acc_get_index_change_password(username)
        #         driver.quit()
        #         return
        #     else :
        #         db_instance.update_rerun_acc_get_index(username)
        #         driver.quit()
        #         return
        
        
        time_reload = 0
        while True:
            # if time_reload == 1:
            #     WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
            #     WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/ion-app/main/app-header/sc-header/ion-header/ion-toolbar/ion-grid/ion-row/ion-col[1]/ion-item/ion-img')))
            #     logo = driver.find_element(By.XPATH, '/html/body/app-root/ion-app/main/app-header/sc-header/ion-header/ion-toolbar/ion-grid/ion-row/ion-col[1]/ion-item/ion-img')
            #     logo.click()
            #     time.sleep(2)
            #     driver.switch_to.window(root_tab)
            #     time.sleep(2)
            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
            app_root = driver.find_element(By.TAG_NAME, 'app-root')
            inputs = app_root.find_elements(By.TAG_NAME, "input")
            actions = ActionChains(driver)
            actions.move_to_element(inputs[0]).perform()
            time.sleep(random.uniform(2, 5))
            for key in data["username"]:
                inputs[0].send_keys(key)
                time.sleep(0.3)
            time.sleep(random.uniform(2, 5))
            for key in data["password"]:
                inputs[1].send_keys(key)
                time.sleep(0.3)
            time.sleep(random.uniform(2, 5))
            inputs[1].send_keys(Keys.ENTER)
            
            # for tab in driver.window_handles:
            #     if tab != root_tab:
            #         driver.switch_to.window(tab)
            #         driver.close()
            #         driver.switch_to.window(root_tab)
            #         time.sleep(2)
            try:
                WebDriverWait(app_root, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'error-message')))
                wrong_password = driver.find_element(By.CLASS_NAME, 'error-message').text
                if wrong_password != "":
                    if check_live == False:
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
                    else:
                        err = "sai pass"
                    if not change_password:
                        db_instance.result_acc_getindex(username, err)
                    else:
                        db_instance.result_acc_getindex_change_password(username, err)
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
                        time.sleep(5)
                        continue
                    else:
                        if not change_password:
                            db_instance.update_rerun_acc_get_index(username)
                        else:
                            db_instance.update_rerun_acc_get_index_change_password(username)
                        driver.quit()
                        return
                elif ex == "Business Registration Incomplete":
                    if not change_password:
                        db_instance.result_acc_getindex(username, "complete bussiness")
                    else:
                        db_instance.result_acc_getindex_change_password(username, "complete bussiness")
                    driver.quit()
                    return
                elif ex == "Subscription Required":
                    try:
                        if check_live == True:
                            # Tắt model
                            WebDriverWait(app_root, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/ion-app/ion-modal/sc-modal/div/div/div/div/div[1]/sc-icon/button')))
                            driver.find_element(By.XPATH, '/html/body/app-root/ion-app/ion-modal/sc-modal/div/div/div/div/div[1]/sc-icon/button').click()
                            time.sleep(5)
                            # Điền tk mk 
                            WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
                            app_root = driver.find_element(By.TAG_NAME, 'app-root')
                            inputs = app_root.find_elements(By.TAG_NAME, "input")
                            inputs[0].send_keys(data["username"])
                            time.sleep(0.5)
                            inputs[1].send_keys(data["password"])
                            time.sleep(1)     
                            # Nhấn nút quên mk
                            WebDriverWait(app_root, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/ion-app/main/div/ion-router-outlet/app-login/ion-content/div/form/ion-grid/ion-row[3]/ion-col[2]/ion-item/a')))
                            driver.find_element(By.XPATH, '/html/body/app-root/ion-app/main/div/ion-router-outlet/app-login/ion-content/div/form/ion-grid/ion-row[3]/ion-col[2]/ion-item/a').click()
                            WebDriverWait(app_root, 15).until(EC.visibility_of_element_located((By.XPATH, '/html/body/app-root/ion-app/ion-modal/sc-modal/div/div/div/div/div[1]/h5')))
                            title = driver.find_element(By.XPATH, '/html/body/app-root/ion-app/ion-modal/sc-modal/div/div/div/div/div[1]/h5').text
                            if title == "Reset Password": 
                                if not change_password:
                                    db_instance.result_acc_getindex(username, "Nosub-sent ok")
                                else:
                                    db_instance.result_acc_getindex_change_password(username, "Nosub-sent ok")
                                driver.quit()
                                return
                            if title == "Well, That Didn't Work...":
                                if not change_password:
                                    db_instance.result_acc_getindex(username, "no sent")
                                else:
                                    db_instance.result_acc_getindex_change_password(username, "no sent")
                                driver.quit()
                                return
                            if not change_password:
                                db_instance.result_acc_getindex(username, title)
                            else:
                                db_instance.result_acc_getindex_change_password(username, title)
                            driver.quit()
                            return
                        else:
                            if not change_password:
                                db_instance.result_acc_getindex(username, "no sub")
                            else:
                                db_instance.result_acc_getindex_change_password(username, "no sub")
                            driver.quit()
                            return
                    except:
                        print("no sub")  
                else:
                    if change_password:
                        db_instance.result_acc_getindex_change_password(username, ex)
                    else:
                        db_instance.result_acc_getindex(username, ex)
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
            try:
                WebDriverWait(driver, WAIT_START).until(EC.visibility_of_element_located((By.TAG_NAME, 'app-root')))
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'assigned-number')))
                assigned_number = driver.find_element(By.CLASS_NAME, 'assigned-number').text
                phone = re.sub(r'\D', '', assigned_number)
                db_instance.update_phone_acc_getindex(username, phone);
                db_instance.result_acc_getindex(username, "live")
                driver.quit()
                return 
            except:
                if not change_password:
                    db_instance.update_rerun_acc_get_index(username)
                else:
                    db_instance.update_rerun_acc_get_index_change_password(username)
                driver.quit()
                return       
        if change_password:
            change_password_func(driver, data)
        if delete_message:
            time.sleep(10)
            delete_message_func(driver,data)
        if send_and_delete:
            send_message_func(driver, username, data, send_and_delete)
            return
        if send_message:
            send_message_func(driver, username, data)
        if send_delete_change_pass:
            send_message_func(driver, username, data, send_and_delete=True, change_password=True)
        
    except Exception as e:
        print(e)
