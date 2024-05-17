from functions import reg_apple_id as reg
import json
import time
print("Đang đăng ký tài khoản Apple Music")
def check_run_app():
    f = open ('./config/tool-config.json', "r")
    data = json.loads(f.read())
    f.close()
    return data['RUN']

while check_run_app(): 
    reg.reg_apple_music(False, False)
    time.sleep(3)