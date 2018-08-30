import sqlite3

class DBconnect():

    def __init__(self):
        self.connect = sqlite3.connect('./iot.db', check_same_thread=False)
        self.cursor = self.connect.cursor()

    def insertMessage(self, time, content, sender):
        query = "INSERT INTO Message(time, content, sender) Values(" + time + "," + content + "," + sender + ");"
        return self.cursor.execute(query)

    
    def insertImage(self, time, path, size):
        query = "INSERT INTO Image (time, path, size) VALUES ('" + time + "','" + path + "','" + size + "');"
        return self.cursor.execute(query)

    
    def selectMessage(self):
        query = "SELECT * FROM Message"
        self.cursor.execute(query)
        return self.cursor.fetchall()


    def selectPhoto(self):
        query = "SELECT * FROM Image"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_newest_img(self):
        query = 'SELECT time, path, size FROM Image ORDER BY time DESC LIMIT 1 OFFSET 0;'
        self.cursor.execute(query)
        return self.cursor.fetchone()
