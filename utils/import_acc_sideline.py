from commands.const import MySQLDatabase


db_intance = MySQLDatabase()
def process_data(change_password, data):
    for line in data.split('\n'):
        if line:
            username, password = line.strip().split('|')
            if not change_password:
                db_intance.insert_acc_sideline(username, password)
            else:
                db_intance.insert_acc_sideline_change_password(username, password)