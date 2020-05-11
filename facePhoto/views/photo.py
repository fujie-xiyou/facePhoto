import os
import datetime
from facePhoto.settings import PHOTO_DIR_ROOT
from facePhoto.utils.FPDecorator import request_decorator, login_decorator, dump_form_data
from facePhoto.models import Photo, FaceAlbumPhoto
from facePhoto.utils.FPExceptions import FormException



@request_decorator
@login_decorator
def upload_photo(request):
    myFile = None
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
    if not myFile:
        return "没有文件"
    path = str(datetime.datetime.timestamp(datetime.datetime.now())) + "-" + myFile.name
    destination = open(os.path.join(PHOTO_DIR_ROOT, path), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    album_id = request.POST.get('album_id')
    user_id = request.session.get('user').get('id')
    photo = Photo(name=myFile.name, path=path, user_id=user_id, album_id=album_id)
    photo.save()
    return "上传结束"


@request_decorator
@login_decorator
def fetch_by_album(request, album_id):
    photos = list(Photo.objects.filter(album_id=album_id).values())
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
    face_album_photos = FaceAlbumPhoto.objects.filter(face_album_id=face_album_id)
    photo_ids = [face_album_photo.photo_id for face_album_photo in face_album_photos]
    photos = list(Photo.objects.filter(id__in=photo_ids).values())
    return photos


@request_decorator
@login_decorator
@dump_form_data
def delete(request, form_data):
    user = request.session.get('user')
    photo_id = int(form_data)
    if not photo_id:
        raise FormException('照片id不合法')
    try:
        photo = Photo.objects.get(id=photo_id)
        if photo.user_id != user.get('id'):
            raise FormException('无权操作')
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
        photo = Photo.objects.get(id=photo_id)
        if photo.user_id != user_id:
            raise FormException('无权限操作')
        photo.name = new_name
        photo.save()
    except Photo.DoesNotExist:
        raise FormException('照片不存在')
