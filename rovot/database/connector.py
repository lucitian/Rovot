import mysql.connector as mysql

class DatabaseConnection():
    def __init__(self, host, user, pw, database, port=3306):
        self.host = host
        self.user = user
        self.pw = pw
        self.db = database
        self.port = port
    
    def connect(self):
        return mysql.connect(
            host = self.host,
            user = self.user,
            passwd = self.pw,
            db=self.db,
            port=self.port
        ) 
    
    def execute_command(self, command, input_values):
        uplink = self.connect()

        cursor = uplink.cursor()

        cursor.execute(command, input_values)

        uplink.commit()

        uplink.close()

    def append_row(self, table, **kwargs):
        cols = [x for x in kwargs]
        equated = tuple([kwargs[x] for x in kwargs])
        runner = "INSERT INTO {}(" + "{}, " * len(kwargs) + ") "
        runner = runner + "VALUES (" + "%s, " * len(kwargs) + ")"
        runner = runner.format(table, *cols)
        runner = runner.replace(', )', ')') 
        
        equated = tuple([kwargs[x] for x in kwargs])

        try:
            self.execute_command(runner, equated)
        except Exception as e:
            print(e)
    
    def purge_row(self, table, **kwargs):
        cols = [x for x in kwargs]
        runner = "DELETE FROM {} WHERE " + "{} = ? AND " * len(kwargs) + "!@#"
        runner = runner.format(table, *cols)
        runner = runner.replace("AND !@#", "")

        equated = tuple([kwargs[x] for x in kwargs])

        try:
            self.execute_command(runner, equated)
        except Exception as e:
            print(e)
    
    def fetch_row(self, table, **kwargs):
        if len(kwargs) == 0:
            runner = f"SELECT * FROM {table}"
            uplink = self.connect()
            c = uplink.cursor()
            c.execute(runner, ())
            fetched = c.fetchall()
            return fetched
        
        cols = [x for x in kwargs]
        equated = tuple([kwargs[x] for x in kwargs])
        runner = "SELECT * FROM {} WHERE " + "{} = %s AND " * len(kwargs) + "!@#"
        runner = runner.format(table, *cols)
        runner = runner.replace("AND !@#", "")

        uplink = self.connect()
        c = uplink.cursor()
        c.execute(runner, equated)
        fetched = c.fetchall()
        uplink.close()
        return fetched
    
    def update_data(self, table, column, new_value, **kwargs):
        cols = [x for x in kwargs]
        equated = tuple([new_value] + [kwargs[x] for x in kwargs])
        runner = "UPDATE {} SET {} = %s WHERE ".format(table, column)
        runner = runner + "{} = %s AND " * len(kwargs)
        runner = runner + "!@#"
        runner = runner.replace("AND !@#", "")
        runner = runner.format(*cols)

        try:
            self.execute_command(runner, equated)
        except Exception as e:
            print(e)

import datetime 

db = DatabaseConnection(host="localhost",user="root",pw="root", database="rovot_db")

"""
print(db.fetch_row(
    'user_sentiments',
    id=1
))
"""
