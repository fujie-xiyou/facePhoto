from django.urls import path, include
from facePhoto.views.home import home
from facePhoto.views import user, album, photo, face_album


photo_patterns = [
    path('upload', photo.upload_photo),
    path('fetch_by_album/<int:album_id>', photo.fetch_by_album),
    path('fetch_user_photo', photo.fetch_user_photo),
    path('fetch_by_face_album/<int:face_album_id>', photo.fetch_by_face_album),
    path('delete', photo.delete),
    path('modify', photo.modify),
    path('style', photo.style),
    path('similarity', photo.similarity),
    path('similarity/delete', photo.similarity_delete),
    path('blurry', photo.blurry),
    path('blurry/unmark', photo.unmark_blurry)
]

album_patterns = [
    path('create', album.create),
    path('fetchUserAlbums', album.fetch_user_albums),
    path('delete', album.delete),
    path('modify', album.modify),
]

user_patterns = [
    path('login', user.login),
    path('register', user.register),
    path('currentUser', user.currentUser),
    path('logout', user.logout)
]

face_album_patterns = [
    path('fetch', face_album.fetch),
    path('modify', face_album.modify)
]


api_patterns = [
    path('user/', include(user_patterns)),
    path('album/', include(album_patterns)),
    path('photo/', include(photo_patterns)),
    path('face_album/', include(face_album_patterns))

]

urlpatterns = [
    path('', home),
    path('api/', include(api_patterns))
]
