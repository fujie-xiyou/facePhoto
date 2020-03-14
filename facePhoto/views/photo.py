import os
import datetime
from facePhoto.settings import PHOTO_DIR_ROOT
from facePhoto.utils.FPDecorator import request_decorator, login_decorator, dump_form_data
from facePhoto.models import Photo


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
