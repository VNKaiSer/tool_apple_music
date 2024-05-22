print("Đang REG tài khoản Apple TV và thêm thẻ")
import json
import time
from functions import reg_apple_tv as reg


def check_run_app():
    f = open ('./config/tool-config.json', "r")
    data = json.loads(f.read())
    f.close()
    return data['RUN']

while check_run_app():    
    reg.reg_apple_tv()
    time.sleep(3)
