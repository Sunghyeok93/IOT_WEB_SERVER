import time
from base_camera import BaseCamera
from DBconnect import DBconnect


class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
        files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    conn = DBconnect()


    @staticmethod
    def frames():
        while True:
            time.sleep(1) # 조절하셈
            yield Camera.get_newest_img()

    @staticmethod
    def get_newest_img():
        image = Camera.conn.select_newest_img()
        if image is None:
            raise FileNotFoundError('image not found')
        return open(image['path'], 'rb').read()