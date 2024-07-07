from functions import get_index
import json
import time
import sys

def check_run_app():
    f = open ('./config/tool-config.json', "r")
    data = json.loads(f.read())
    f.close()
    return data['RUN']

while check_run_app(): 
    print("RUN get index")
    get_index.login()
    time.sleep(3)

print("STOP")
sys.exit()

