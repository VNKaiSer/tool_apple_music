import random
from functions import login_apple_id

import json
import time
import sys
from const import *
import argparse

def check_run_app():
    f = open ('./config/tool-config.json', "r")
    data = json.loads(f.read())
    f.close()
    return data['RUN']

def getData():
    acc_get = db_instance.get_acc_apple_id()
    time.sleep(2)
    if acc_get == '':
        return None
    acc, password, q1, q2, q3 = acc_get[1], acc_get[2], acc_get[3], acc_get[4], acc_get[5]
    
    return acc, password, q1, q2, q3

def main():
    parser = argparse.ArgumentParser(description="Apple ID Login")
    parser.add_argument("--actions", nargs='+', choices=["change_password", "change_country", "change_question","add_card"], help="Choice action")

    args = parser.parse_args()
    while check_run_app():
        print("RUN login APPLE ID")
          
        if db_instance.count_account_apple_id()[0][0] == 0:
            print("Has no account")
            sys.exit()
            
        tmp = getData()
        if tmp is None:
            print("No acc! Input more acc.")
            return
        acc, password, q1, q2, q3 = tmp
        try:
            data = {
                "email" : acc,
                "password" : password,
                "question" : {
                    "school" : q1,
                    "dream" : q2,
                    "parent" : q3
                }
            }
            print(data)
        
        except:
            print("error")
        random_port = random.randint(9000, 9050)
        random_proxy = [
        {
            'proxy':  
                {
                    'https': 'https://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
                    'http': 'http://brd-customer-hl_d346dd25-zone-static-country-us:jmkokxul20oa@brd.superproxy.io:22225',
                    'no_proxy': 'localhost,127.0.0.1'
                },
            'port': generate_random_port()
        
        },
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
        ]
        proxy = random.choice(random_proxy)
        
        
        
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--log-level=3')  # Selenium log level
        
        driver = webdriver.Chrome(
            options=chrome_options,
            seleniumwire_options=proxy,
            # service_log_path=os.path.devnull  # Chuyển hướng log của ChromeDriver
        )
        if args.actions:
            try:
                login_apple_id.login_apple_id(data, driver)
                for action in args.actions:
                    if action == "change_password":
                        login_apple_id.change_password(data, driver)
                    if action == "change_country":
                        login_apple_id.change_region(driver)
                    if action == "change_question":
                        login_apple_id.change_security_question(data, driver)
                    if action == "add_card":
                        login_apple_id.add_card(data, driver)
                    db_instance.update_data(table_name="apple_id_login", set_values={"ex" : "done"}, where_values="acc = " + str(acc))
            except Exception as e:
                db_instance.update_rerun_acc_apple_id(acc)
                driver.quit()
                return
                
                

if __name__ == "__main__":
    main()



