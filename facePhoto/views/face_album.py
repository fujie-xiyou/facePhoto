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

