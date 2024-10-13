from functions import sideline
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
    parser = argparse.ArgumentParser(description="Sideline tool")
    parser.add_argument("--actions", nargs='+', choices=["send_message", "delete_message", "change_password","send_and_delete", "check_live", "delete_after_send","send_delete_change_pass"], help="Choice action")

    args = parser.parse_args()
    while check_run_app():
        print("RUN Sideline tool")
        if "change_password" not in args.actions:    
            if db_instance.count_account_sideline_store()[0][0] == 0:
                print("Has no account")
                sys.exit()
        else:
            if db_instance.count_account_sideline_change_password()[0][0] == 0:
                print("Has no account")
                sys.exit()

        if args.actions:
            for action in args.actions:
                if action == "send_and_delete":
                    sideline.login(send_message=True, delete_message=True)
                elif action == "send_message":
                    sideline.login(send_message=True)
                elif action == "delete_message":
                    sideline.login(delete_message=True)
                elif action == "change_password":
                    sideline.login(change_password=True)
                elif action == "check_live":
                    sideline.login(check_live=True)
                elif action == "delete_after_send":
                    sideline.login(send_message=True, send_and_delete=True) 
                elif action == "send_delete_change_pass":
                    sideline.login(send_delete_change_pass=True)  
                

        time.sleep(3)
    print("STOP")
if __name__ == "__main__":
    main()



