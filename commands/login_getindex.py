from functions import get_index
import json
import time
import sys
from const import db_instance

def check_run_app():
    f = open ('./config/tool-config.json', "r")
    data = json.loads(f.read())
    f.close()
    return data['RUN']

while check_run_app(): 
    print("RUN get index")
    if db_instance.count_account_getindex_store()[0][0] == 0:
        sys.exit()
    
    get_index.login()
    time.sleep(3)

print("STOP")


