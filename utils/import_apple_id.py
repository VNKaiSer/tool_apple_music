from commands.const import MySQLDatabase


db_intance = MySQLDatabase()
def process_data(data):
    for line in data.split('\n'):
        if line:
            acc, password, q1, q2, q3 = line.strip().split('|')
            db_intance.insert_account_apple_id(acc, password, q1, q2, q3)
            