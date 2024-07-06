from commands.const import MySQLDatabase


db_intance = MySQLDatabase()
def process_data(data):
    for line in data.split('\n'):
        if line:
            username, password = line.strip().split('-')
            db_intance.insert_acc_getindex(username, password)