import sqlite3

class DBconnect():

    def __init__(self):
        self.connect = sqlite3.connect('./iot.db', check_same_thread=False, isolation_level=None)
        self.cursor = self.connect.cursor()

    def insertMessage(self, time, content, sender, isRead):
        query = "INSERT INTO Message(time, content, sender, isRead) Values('" + time + "','" + content + "','" + sender + "'," + str(isRead) + ");"
        print(query)
        return self.cursor.execute(query)

    def getMessageNotRead(self):
        query = "SELECT num FROM Message WHERE isRead = 0;"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def modifyMessageIsRead(self, num, isRead):
        query = "UPDATE Message SET isRead = " + str(isRead) + " WHERE num = " + str(num) + ";"
        self.cursor.execute(query)
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

    def search_content(self, table, content):
        query=""
        if table == "Message":
            query = "SELECT * FROM Message WHERE content LIKE '%" +content + "%';"
        else: # Image
            query = "SELECT * FROM Message WHERE time LIKE '%" +    content + "%';"
        self.cursor.execute(query)
        return self.cursor.fetchall()

