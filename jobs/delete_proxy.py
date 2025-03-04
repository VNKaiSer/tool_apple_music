import mysql.connector
import schedule
import time
from datetime import datetime, timedelta
import os
import dotenv 

dotenv.load_dotenv()

# Hàm kết nối với MySQL
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
USE_PROXY = True
def connect_to_mysql():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Hàm để xóa các dòng sau 10 giây
def delete_old_rows():
    try:
        conn = connect_to_mysql()
        cursor = conn.cursor()

        # Thời gian hiện tại trừ đi 10 giây
        ten_seconds_ago = datetime.now() - timedelta(seconds=10)

        # Câu lệnh SQL để xóa các dòng cũ hơn 10 giây
        delete_query = """
        DELETE FROM proxy_ip
        WHERE create_at < %s
        """
        
        cursor.execute(delete_query, (ten_seconds_ago,))
        conn.commit()
        print(f"{cursor.rowcount} rows deleted.")
        
        cursor.close()
        conn.close()

    except mysql.connector.Error as error:
        print(f"Error: {error}")

# Lập lịch chạy hàm xóa mỗi 10 giây
schedule.every(6).minutes.do(delete_old_rows)

while True:
    schedule.run_pending()
    time.sleep(1)
