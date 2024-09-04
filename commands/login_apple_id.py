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

def main():
    parser = argparse.ArgumentParser(description="Apple ID Login")
    parser.add_argument("--actions", nargs='+', choices=["change_password", "change_country", "change_question","add_card"], help="Choice action")

    args = parser.parse_args()
    while check_run_app():
        print("RUN login APPLE ID")
          
        if db_instance.count_account_apple_id()[0][0] == 0:
            print("Has no account")
            sys.exit()
        if args.actions:
            login_apple_id.login_apple_id()
            for action in args.actions:
                if action == "change_password":
                    login_apple_id.change_password()
                if action == "change_country":
                    login_apple_id.change_region()
                if action == "change_question":
                    login_apple_id.change_question()
                if action == "add_card":
                    login_apple_id.add_card()
                

if __name__ == "__main__":
    main()



