from functions import reg_apple_id as reg
import json
import time
print("Đang đăng ký tài khoản Apple Music và thêm thẻ và apple id")
def check_run_app():
    f = open ('./config/tool-config.json', "r")
    data = json.loads(f.read())
    f.close()
    return data['RUN']
time.sleep(15)
while check_run_app():    
    reg.reg_apple_music(True, True)
    time.sleep(3)