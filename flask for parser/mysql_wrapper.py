import mysql.connector

class UseDataBase():
    configuration = {'host': '127.0.0.1',
                     'user': 'tylorNixon',
                     'password': '9python9',
                     'database': 'parserDB',}
    def create_connection(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor
    def query_insert(self, *args):
        self.cursor.execute(*args)
    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()