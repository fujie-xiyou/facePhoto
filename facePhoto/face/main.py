import django
import threading

django.setup()

from facePhoto.face.scan_face import scan_face
from facePhoto.face.hash import photo_hash


class FaceThread(threading.Thread):
    def run(self) -> None:
        print("人脸检测模块启动完成。")
        while True:
            scan_face()


class HashThread(threading.Thread):
    def run(self) -> None:
        print("重复照片检测模块启动完成。")
        while True:
            photo_hash()


if __name__ == '__main__':
    face_thread = FaceThread()
    hash_thread = HashThread()

    face_thread.start()
    hash_thread.start()

    face_thread.join()
    hash_thread.join()
