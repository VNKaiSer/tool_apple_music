from functions import login_apple_id

import json
import time
import sys
from const import db_instance
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
        if args.actions:
            login_apple_id.login_apple_id(data)
            for action in args.actions:
                if action == "change_password":
                    login_apple_id.change_password(data)
                if action == "change_country":
                    login_apple_id.change_region()
                if action == "change_question":
                    login_apple_id.change_question(data)
                if action == "add_card":
                    login_apple_id.add_card(data)
                

if __name__ == "__main__":
    main()



