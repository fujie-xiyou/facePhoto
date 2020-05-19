import json
from facePhoto.utils.FPDecorator import request_decorator, login_decorator, dump_form_data
from facePhoto.utils.FPExceptions import FormException
from facePhoto.models import FaceAlbum, FaceAlbumPhoto, Photo


@request_decorator
@login_decorator
def fetch(request):
    uid = request.session.get('user').get('id')
    face_albums = list(FaceAlbum.objects.values().filter(user_id=uid))
    result = []
    for album in face_albums:
        try:
            face_photo = FaceAlbumPhoto.objects.filter(face_album_id=album.get("id"))[0]
            photo = Photo.objects.filter(id=face_photo.photo_id)[0]
            album['src'] = photo.path
            result.append(album)
        except IndexError:
            FaceAlbum.objects.filter(id=album.get("id")).get().delete()
    return result


@request_decorator
@dump_form_data
@login_decorator
def modify(request, form_data):
    face_album_id = form_data.get('album_id')
    user_id = request.session.get('user').get('id')
    try:
        face_album = FaceAlbum.objects.get(id=face_album_id)
    except FaceAlbum.DoesNotExist:
        raise FormException('人物相册不存在')
    if face_album.user_id != user_id:
        raise FormException('无权操作')
    name = form_data.get('name')
    if not name:
        raise FormException('相册名不能为空')
    face_album.name = name
    face_album.description = form_data.get('description')
    face_album.save()
    return "修改成功"
