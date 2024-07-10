from functions import get_index
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
    parser = argparse.ArgumentParser(description="Get index tool")
    parser.add_argument("--actions", nargs='+', choices=["send_message", "delete_message", "change_password","send_and_delete"], help="Choice action")

    args = parser.parse_args()
    while check_run_app():
        print("RUN get index")
        # Thay thế bằng logic kiểm tra tài khoản của bạn
        if "change_password " not in args.actions:    
            if db_instance.count_account_getindex_store()[0][0] == 0:
                print("Has no account")
                sys.exit()
        else:
            if db_instance.count_account_getindex_change_password()[0][0] == 0:
                print("Has no account")
                sys.exit()

        if args.actions:
            for action in args.actions:
                if action == "send_and_delete":
                    get_index.login(send_message=True, delete_message=True)
                elif action == "send_message":
                    get_index.login(send_message=True)
                elif action == "delete_message":
                    get_index.login(delete_message=True)
                elif action == "change_password":
                    get_index.login(change_password=True)

        time.sleep(3)
    print("STOP")
if __name__ == "__main__":
    main()



