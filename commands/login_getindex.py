from functions import get_index
import json
import time


def check_run_app():
    f = open ('./config/tool-config.json', "r")
    data = json.loads(f.read())
    f.close()
    return data['RUN']

while check_run_app(): 
    print("Đang chạy get index")
    print(check_run_app())   
    get_index.login()
    time.sleep(3)
    
print("Đã dừng ")
