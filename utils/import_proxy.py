import os
from db_connect import MySQLDatabase

db_intance = MySQLDatabase()
# def read_txt_files_from_directory(directory):
#     text_data = []
#     for filename in os.listdir(directory):
#         if filename.endswith(".txt"):
#             file_path = os.path.join(directory, filename)
#             with open(file_path, 'r') as file:
#                 data = file.read()
#                 text_data.append(data)
#     return text_data

def process_data(data):
    for line in data.split('\n'):
        if line:
            db_intance.insert_proxy_data(line)

# directory_path = './card'
# text_data_list = read_txt_files_from_directory(directory_path)
# for text_data in text_data_list:
#     process_data(text_data)
    