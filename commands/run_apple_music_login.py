from functions import login_apple_music as music
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
    parser = argparse.ArgumentParser(description="Tool login music")
    parser.add_argument("--actions", nargs='+', choices=["login_check", "login_delete", "login_add"], help="Choice action")

    args = parser.parse_args()
    while check_run_app():
        print("RUN apple music")
        if db_instance.count_account_music_store()[0][0] == 0:
            print("Has no account")
            sys.exit()

        if args.actions:
            for action in args.actions:
                if action == "login_check":
                    music.run(run_check=True) 
                elif action == "login_delete":
                    music.run(run_delete=True)
                elif action == "login_add":
                    music.run()
                
        time.sleep(3)
    print("STOP")
if __name__ == "__main__":
    main()
