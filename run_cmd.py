import os 
import threading
import time

def run_command():
    os.system('py ./command/run_check_delete.py')

for i in range(2):
    threading.Thread(target=run_command).start()
    if i < 2:  # Pause after starting each thread, except for the last one
        time.sleep(5)
