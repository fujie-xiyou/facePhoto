import django
import time

from facePhoto.face.src.similarity import hash_String, Difference
django.setup()

from facePhoto.models import Photo, PhotoHash, SimilarityPhotoAlbum, SimilarityPhoto
from facePhoto.settings import PHOTO_DIR_ROOT


def photo_hash():
    init_ph = PhotoHash.objects.all().only('photo_id')
    photo_ids = [ph.photo_id for ph in init_ph]
    photos = Photo.objects.exclude(id__in=photo_ids)
    for photo in photos:
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


if __name__ == '__main__':
    while True:
        print("开始扫描重复照片")
        photo_hash()
        print("本次扫描结束")
        time.sleep(1 * 60)
