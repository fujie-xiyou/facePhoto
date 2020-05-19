import json
from facePhoto.utils.FPDecorator import request_decorator, login_decorator, dump_form_data
from facePhoto.utils.FPExceptions import FormException
from facePhoto.models import Album, Photo


@request_decorator
@dump_form_data
@login_decorator
def create(request, form_data):
    uid = request.session.get('user').get('id')
    album_name = form_data.get('name')
    description = form_data.get('description')
    album = Album(name=album_name, user_id=uid, description=description)
    try:
        album.save()
    except Exception as e:
        raise FormException("创建失败：数据库异常", e)
    return "创建成功"


@request_decorator
@login_decorator
def fetch_user_albums(request):
    uid = request.session.get('user').get('id')
    albums = list(Album.objects.values().filter(user_id=uid))
    for album in albums:
        try:
            photo = Photo.objects.filter(album_id=album.get('id'))[0]
            album['src'] = photo.path
        except IndexError:
            pass
    return albums


@request_decorator
@dump_form_data
@login_decorator
def modify(request, form_data):
    album_id = form_data.get('album_id')
    user_id = request.session.get('user').get('id')
    try:
        album = Album.objects.get(id=album_id, user_id=user_id)
    except Album.DoesNotExist:
        raise FormException('相册不存在')
    name = form_data.get('name')
    if not name:
        raise FormException('名称不能为空')
    album.name = name
    album.description = form_data.get('description')
    album.save()
    return "修改成功"


@request_decorator
@dump_form_data
@login_decorator
def delete(request, form_data):
    album_id = form_data.get('album_id')
    user_id = request.session.get('user').get('id')
    try:
        album = Album.objects.get(id=album_id, user_id=user_id)
    except Album.DoesNotExist:
        raise FormException('相册不存在')
    album.delete()
    return "删除成功"
