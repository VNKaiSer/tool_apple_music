import mysql.connector
class MySQLDatabase:
    def __init__(self, ):
        self.connection = mysql.connector.connect(
            host= "159.65.2.46",
            user="kaiser",
            password="r!8R%OMm@=H{cVH6LZpqV]nye1G",
            database="apple_music"
        )
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        column_str = ', '.join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_str})"
        self.cursor.execute(query)
        self.connection.commit()

    def insert_credit_card_data(self, credit_card_data):
        card_number, expiration_month, expiration_year, cvv = credit_card_data.strip().split('|')
        if len(expiration_year) < 4:
            expiration_year = '20' + expiration_year
        query = "INSERT INTO pay (card_number, day, year, ccv) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (card_number, expiration_month, expiration_year, cvv))
        self.connection.commit()

    def insert_apple_music_id(self, id_data):
        parts = id_data.strip().split('-')
        account = '-'.join(parts[:-1])
        password = parts[-1]
        query = "INSERT INTO mail (user, password) VALUES (%s, %s)"
        self.cursor.execute(query, (account, password))
        self.connection.commit()
        pass
    def analysis_id_scusess(self):
        query = "SELECT m.user , m.password, p.card_number, p.`day`, p.`year`, p.ccv FROM mail m INNER JOIN pay p ON m.card_add = p.card_number"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print(result)
        return result

    def export_error_id(self, error):
        query = None
        if error == 'country':
            query = "SELECT user, password, country FROM mail WHERE country IS NOT NULL"
            self.cursor.execute(query)
        else:
            query = "SELECT user, password FROM mail WHERE exception = %s"
            self.cursor.execute(query, (error,))

        result = self.cursor.fetchall()
        print(result)
        return result
    
    def insert_acc_getindex(self, username, password):
        query = "INSERT IGNORE INTO get_index_tool(user_name, password) VALUES (%s, %s)"
        self.cursor.execute(query, (username, password))
        self.connection.commit()
    

    def close(self):
        self.connection.close()
        
# db_intance = MySQLDatabase()
# for data in db_intance.export_error_id("country"):
#     try:
#         print(data[0] + '|' + data[1] + '|' +data[2])
#     except:
#         print(data[0] + '|' + data[1] + "|UnLock")
        
# for data in db_intance.analysis_id_scusess():
#     print(data[0]+'|'+data[1]+'|'+data[2]+'|'+data[3]+'|'+data[4]+'|'+data[5])