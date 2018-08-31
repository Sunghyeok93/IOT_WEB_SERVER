import sqlite3

class DBconnect():

    def __init__(self):
        self.connect = sqlite3.connect('./iot.db', check_same_thread=False)
        self.cursor = self.connect.cursor()

    def insertMessage(self, time, content, sender):
        isRead = 0
        if sender is not "ARTIK":
            isRead = 1
        query = "INSERT INTO Message(time, content, sender, isRead) Values(" + time + "," + content + "," + sender + "," + isRead + ");"
        return self.cursor.execute(query)

    def getMessageNotRead(self):
        query = "SELECT num FROM Message WHERE isRead = 0;"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def modifyMessageIsRead(self, num, isRead):
        query = "UPDATE Message SET isRead = " + isRead + " WHERE num = " + num + ";"
        return 0;    

    def getMessageContent(self, num):
        query = "SELECT content FROM Message WHERE isRead = 0 ORDER BY time LIMIT 1 OFFSET 0;"
        self.cursor.execute(query)
        return self.cursor.fetchone()

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
