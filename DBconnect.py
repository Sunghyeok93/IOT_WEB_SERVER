import sqlite3

class DBconnect():

    def __init__():
        con = sqlite3.connect('./test.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM PhoneBook')
        for row in cur:
            print(row)

