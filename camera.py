import time
from base_camera import BaseCamera
from DBconnect import DBconnect


class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
        files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""

    @staticmethod
    def frames():
        while True:
            time.sleep(1) # 조절하셈
            yield Camera.get_newest_img()

    @staticmethod
    def get_newest_img():
        conn = DBconnect()
        conn.insertImage(str(123456), 'abc.png', "123")
        query = 'SELECT time, path, size FROM Image ORDER BY time DESC LIMIT 1 OFFSET 0;'
        image = conn.cursor.execute(query).fetchone()
        print(image['path'])
        if image is None:
            raise FileNotFoundError('image not found')
        return open(image['path'], 'rb').read()