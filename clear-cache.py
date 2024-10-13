import os
import shutil
import schedule
import time

def clear_temp_folder():
    temp_folder = os.getenv('TEMP')
    print(f"Đang xóa tất cả các tệp và thư mục trong thư mục tạm thời: {temp_folder}")
    for root, dirs, files in os.walk(temp_folder):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Đã xóa tệp: {file_path}")
            except Exception as e:
                print(f"Không thể xóa tệp {file_path}: {e}")
        for dir in dirs:
            try:
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)
                print(f"Đã xóa thư mục: {dir_path}")
            except Exception as e:
                print(f"Không thể xóa thư mục {dir_path}: {e}")

# Lên lịch chạy clear_temp_folder mỗi 5 phút
schedule.every(10).seconds.do(clear_temp_folder)

print("Đang chờ để thực hiện nhiệm vụ...")

while True:
    schedule.run_pending()
    time.sleep(1)
