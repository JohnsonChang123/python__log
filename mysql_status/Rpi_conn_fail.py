import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
import json
# 設定資料庫連線資訊
with open('/home/pi/Desktop/NTOU_CSE_LAB403/main/config.json', 'r') as config_file:
    config_data = json.load(config_file)
camera_config = config_data['camera_config']
db_config = config_data['fishDB']

# 連線MySQL資料庫
fishDB = mysql.connector.connect(
  host=db_config['host'],
  user=db_config['user'],
  password=db_config['password'],
  database=db_config['database']
)

# 記錄檔案名稱
log_file_name = 'connection_failure_log.txt'

def log_connection_failure(start_time):
    # 將連不上資料庫的起始日期及時間紀錄在檔案中，保留到整秒
    with open(log_file_name, 'a') as log_file:
        log_file.write(f"{start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def update_failure_time_in_db():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            with open(log_file_name, 'r') as log_file:
                lines = log_file.readlines()
                for line in lines:
                    start_time_str = line.strip()
                    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute(
                        "INSERT INTO Rpi_connection_failures (start_time, end_time) VALUES (%s, %s)",
                        (start_time, end_time)
                    )
            connection.commit()
            cursor.close()
            connection.close()
            print("Connection failure time updated in database.")
            os.remove(log_file_name)
            print(f"Log file {log_file_name} deleted.")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

def check_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to the database")
            if os.path.exists(log_file_name):
                update_failure_time_in_db()
            connection.close()
    except Error:
        if not os.path.exists(log_file_name):
            connection_failure_time = datetime.now()
            log_connection_failure(connection_failure_time)
            print(f"Failed to connect to the database at {connection_failure_time}")

if __name__ == "__main__":
    check_db_connection()