import os
import json
import time
import numpy as np
from facePhoto.models import PhotoEmbedding, FaceAlbum, FaceAlbumPhoto, FaceAlbumNameNumber
from facePhoto.settings import PHOTO_DIR_ROOT, FACENET_MODEL_PATH
from face_recognition import FacenetEmbedding, FaceDetection, get_dist
from facePhoto.utils.redis import get_redis_con

facenet_embedding = FacenetEmbedding(FACENET_MODEL_PATH)
face_detection = FaceDetection()


def scan_face():
    redis_con = get_redis_con()
    pending = redis_con.xpending("photos", "face_group")
    if pending['consumers']:
        photos = redis_con.xrange("photos", pending['min'], pending['max'])
    else:
        photos = redis_con.xreadgroup(groupname="face_group",
                                      consumername="face", block=0, streams={"photos": ">"})[0][1]
    print("检测到新照片，开始进行人脸检测...")
    for photo_tup in photos:
        photo = json.loads(photo_tup[1][b"photo_json"].decode())
        image_path = os.path.join(PHOTO_DIR_ROOT, photo["path"])
        # 获取 判断标识 bounding_box crop_image
        image, bboxes, landmarks = face_detection.detect_face(image_path)
        if bboxes.size != 0 or landmarks.size != 0:
            print("照片：{} 包含人脸".format(photo["name"]))
            emb = facenet_embedding.get_embedding(image, bboxes)
            face_albums = FaceAlbum.objects.filter(user_id=photo["user_id"])
            face_album_id = None
            for face_album in face_albums:
                face_album_photos = FaceAlbumPhoto.objects.filter(face_album_id=face_album.id)[:3]
                photo_ids = [photo.photo_id for photo in face_album_photos]
                photo_embeddings = PhotoEmbedding.objects.filter(photo_id__in=photo_ids)
                for photo_embedding in photo_embeddings:
                    db_emb = np.array(json.loads(photo_embedding.embedding))
                    dist = get_dist(emb, db_emb)
                    if dist < 1:
                        face_album_id = face_album.id
                        break
            if not face_album_id:
                fanns = FaceAlbumNameNumber.objects.filter(user_id=photo["user_id"]).all()
                if not fanns:
                    fann = FaceAlbumNameNumber(user_id=photo["user_id"])
                    fann.save()
                else:
                    fann = fanns[0]
                number = fann.number
                fann.number = number + 1
                fann.save()

                face_album = FaceAlbum(user_id=photo["user_id"], name="人物{}".format(number),
                                       description="人物 {} 的人物相册".format(number))
                face_album.save()
                face_album_id = face_album.id
            FaceAlbumPhoto(face_album_id=face_album_id, photo_id=photo["id"]).save()

            emb_str = json.dumps(emb.tolist())
            PhotoEmbedding(user_id=photo["user_id"], photo_id=photo["id"], embedding=emb_str, type=1).save()
        else:
            print("照片：{} 不含人脸".format(photo["name"]))
        redis_con.xack("photos", "face_group", photo_tup[0])
    redis_con.close()
    print("本次人脸检测完成。")


if __name__ == '__main__':
    while True:
        print("开始扫描人脸")
        scan_face()
        print("本次扫描结束")
        time.sleep(1 * 60)
