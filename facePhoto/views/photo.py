import os
import datetime
import logging
import json

from facePhoto.settings import PHOTO_DIR_ROOT
from facePhoto.utils.FPDecorator import request_decorator, login_decorator, dump_form_data
from facePhoto.models import Photo, FaceAlbumPhoto, BlurredPhoto, Album, SimilarityPhotoAlbum, SimilarityPhoto
from facePhoto.utils.FPExceptions import FormException
from facePhoto.utils.redis import get_redis_con
from facePhoto.face.style import style_types, style_transfer, rgb_to_sketch
from facePhoto.face.blurry_photo import is_blurred


@request_decorator
@login_decorator
def upload_photo(request):
    myFile = None
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
    if not myFile:
        return "没有文件"
    path = str(datetime.datetime.timestamp(datetime.datetime.now())) + "-" + myFile.name
    image_path = os.path.join(PHOTO_DIR_ROOT, path)
    destination = open(image_path, 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    album_id = request.POST.get('album_id')
    user_id = request.session.get('user').get('id')
    try:
        Album.objects.get(id=album_id, user_id=user_id)
    except Album.DoesNotExist:
        raise FormException('相册不存在')
    photo = Photo(name=myFile.name, path=path, user_id=user_id, album_id=album_id)
    photo.save()
    redis_con = get_redis_con()
    photo_json = json.dumps(photo.__dict__, default=str)
    redis_con.xadd(name="photos", fields={"photo_json": photo_json})
    redis_con.close()
    if is_blurred(image_path):
        BlurredPhoto(photo_id=photo.id, user_id=user_id).save()
    return "上传结束"


@request_decorator
@login_decorator
def fetch_by_album(request, album_id):
    user_id = request.session.get('user').get('id')
    photos = list(Photo.objects.filter(album_id=album_id, user_id=user_id).values())
    return photos


@request_decorator
@login_decorator
def fetch_user_photo(request):
    uid = request.session.get('user').get('id')
    photos = list(Photo.objects.filter(user_id=uid).values())
    return photos


@request_decorator
@login_decorator
def fetch_by_face_album(request, face_album_id):
    user_id = request.session.get('user').get('id')
    face_album_photos = FaceAlbumPhoto.objects.filter(face_album_id=face_album_id, face_album__user_id=user_id)
    photo_ids = [face_album_photo.photo_id for face_album_photo in face_album_photos]
    photos = list(Photo.objects.filter(id__in=photo_ids).values())
    return photos


@request_decorator
@login_decorator
@dump_form_data
def delete(request, form_data):
    user_id = request.session.get('user').get('id')
    photo_id = int(form_data)
    if not photo_id:
        raise FormException('照片id不合法')
    try:
        photo = Photo.objects.get(id=photo_id, user_id=user_id)
        photo.delete()
        return "删除成功"
    except Photo.DoesNotExist:
        raise FormException('照片不存在')


@request_decorator
@login_decorator
@dump_form_data
def modify(request, form_data):
    photo_id = form_data.get("id")
    new_name = form_data.get("name")
    user_id = request.session.get('user').get('id')
    try:
        photo = Photo.objects.get(id=photo_id, user_id=user_id)
        photo.name = new_name
        photo.save()
    except Photo.DoesNotExist:
        raise FormException('照片不存在')
    return "修改成功"


@request_decorator
@login_decorator
@dump_form_data
def style(request, form_data):
    photo_id = form_data.get('id')
    style_type = form_data.get("style_type")
    user_id = request.session.get('user').get('id')

    try:
        photo = Photo.objects.get(id=photo_id, user_id=user_id)
    except Photo.DoesNotExist:
        raise FormException('照片不存在')
    image_path = PHOTO_DIR_ROOT + photo.path
    if style_type not in style_types:
        raise FormException('参数错误')
    db_path = str(datetime.datetime.timestamp(datetime.datetime.now())) + '-' + style_type + '-' + photo.path
    dst_path = PHOTO_DIR_ROOT + db_path
    if style_type == "sketch":
        try:
            rgb_to_sketch(image_path, dst_path)
            Photo(name=photo.name + '-' + style_type, user_id=photo.user_id,
                  album_id=photo.album_id, path=db_path, is_analyzed=1).save()
            return dst_path
        except Exception as e:
            logging.exception(e)
            raise FormException('服务器异常')
    elif style_type == "grays":
        pass
    elif style_type == "old":
        pass
    else:
        try:
            style_transfer(image_path, dst_path, style_type)
            Photo(name=style_type + '-' + photo.name, user_id=photo.user_id,
                  album_id=photo.album_id, path=db_path, is_analyzed=1).save()
            return db_path
        except Exception as e:
            logging.exception(e)
            raise FormException('服务器异常')


@request_decorator
@login_decorator
def similarity(request):
    user_id = request.session.get('user').get('id')
    sps = SimilarityPhoto.objects.filter(user_id=user_id)
    sps_dict = {}
    for sp in sps:
        l = sps_dict.get(sp.sp_album_id)
        if l:
            l.append(sp.photo_id)
        else:
            sps_dict[sp.sp_album_id] = [sp.photo_id]
    result = []
    for v in sps_dict.values():
        photos = list(Photo.objects.values().filter(id__in=v))
        result.append(photos)
    return result


@request_decorator
@login_decorator
@dump_form_data
def similarity_delete(request, form_data):
    photo_id = form_data.get('photo_id')
    user_id = request.session.get('user').get('id')
    try:
        sp = SimilarityPhoto.objects.get(photo_id=photo_id, user_id=user_id)
    except SimilarityPhoto.DoesNotExist:
        raise FormException('照片不存在')
    try:
        photo = Photo.objects.get(id=photo_id, user_id=user_id)
    except Photo.DoesNotExist:
        raise FormException('照片不存在')
    sp.delete()
    photo.delete()
    sp_count = SimilarityPhoto.objects.filter(sp_album_id=sp.sp_album_id).count()
    if sp_count <= 1:
        try:
            spa = SimilarityPhotoAlbum.objects.get(id=sp.sp_album_id)
        except SimilarityPhotoAlbum.DoesNotExist:
            return "删除成功，且无需删除重复照片集"
        spa.delete()
    return "删除成功"


@request_decorator
@login_decorator
def blurry(request):
    user_id = request.session.get('user').get('id')
    bps = BlurredPhoto.objects.filter(user_id=user_id)
    photo_ids = [bp.photo_id for bp in bps]
    photos = list(Photo.objects.values().filter(id__in=photo_ids))
    return photos


@request_decorator
@login_decorator
@dump_form_data
def unmark_blurry(request, form_data):
    user_id = request.session.get('user').get('id')
    photo_id = int(form_data)
    try:
        bp = BlurredPhoto.objects.get(photo_id=photo_id, user_id=user_id)
    except BlurredPhoto.DoesNotExist:
        raise FormException('照片不存在')
    bp.delete()
    return "操作成功"
