import sqlite3



class DBconnect():

    def __init__(self):
        self.connect = sqlite3.connect('./iot.db')


    def insertMessage(time, content, sender):
        cursor = self.connect.cursor()
        query = "INSERT INTO Message(time, content, sender) Values(" + time + "," + content + "," + sender + ");"
        return cursor.execute(query)

    
    def insertImage(time, path, size):
        cursor = self.connect.cursor()
        query = "INSERT INTO Image(time, path, size) Values(" + time + "," + path + "," + size + ");"
        return cursor.execute(query)

    
    def selectMessage():
        cursor = self.connect.cursor()
        query = "SELECT * FROM Message"
        cursor.execute(query)
        return cursor.fetchall()


    def selectMessage():
        cursor = self.connect.cursor()
        query = "SELECT * FROM Image"
        cursor.execute(query)
        return cursor.fetchall()

