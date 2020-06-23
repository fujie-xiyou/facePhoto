import json

import django
import time
from easydict import EasyDict
from facePhoto.face.similarity import hash_String, Difference
from facePhoto.utils.redis import get_redis_con

django.setup()

from facePhoto.models import PhotoHash, SimilarityPhotoAlbum, SimilarityPhoto
from facePhoto.settings import PHOTO_DIR_ROOT


def photo_hash():
    redis_con = get_redis_con()
    pending = redis_con.xpending("photos", "similarity_group")
    if pending['consumers']:
        photos = redis_con.xrange("photos", pending['min'], pending['max'])
    else:
        photos = redis_con.xreadgroup(groupname="similarity_group",
                                      consumername="face", block=0, streams={"photos": ">"})[0][1]
    print("检测到新照片，开始进行重复照片检测...")
    for photo_tup in photos:
        photo = EasyDict(json.loads(photo_tup[1][b"photo_json"].decode()))
        image_path = PHOTO_DIR_ROOT + photo.path
        hash = hash_String(image_path)
        print("id: {} hash: {}".format(photo.id, hash))
        photo_hashs = PhotoHash.objects.filter(user_id=photo.user_id)
        for ph in photo_hashs:
            d = Difference(hash, ph.hash)
            print("{} {} 相似度 {}".format(photo.id, ph.photo_id, d))
            if d < 5:
                try:
                    sp = SimilarityPhoto.objects.get(photo_id=ph.photo_id)
                except SimilarityPhoto.DoesNotExist:
                    spam = SimilarityPhotoAlbum(user_id=photo.user_id)
                    spam.save()
                    sp = SimilarityPhoto(photo_id=ph.photo_id, user_id=photo.user_id, sp_album_id=spam.id)
                    sp.save()

                SimilarityPhoto(photo_id=photo.id, user_id=photo.user_id, sp_album_id=sp.sp_album_id).save()
                break
        PhotoHash(photo_id=photo.id, user_id=photo.user_id, hash=hash).save()
        redis_con.xack("photos", "similarity_group", photo_tup[0])
    redis_con.close()
    print("本次重复检测完成。")


if __name__ == '__main__':
    while True:
        print("开始扫描重复照片")
        photo_hash()
        print("本次扫描结束")
        time.sleep(1 * 60)
