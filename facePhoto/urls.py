from django.urls import path, include
from facePhoto.views.home import home
import facePhoto.views.user as user
import facePhoto.views.album as album
import facePhoto.views.photo as photo


photo_patterns = [
    path('upload', photo.upload_photo),
    path('fetch_by_album/<int:album_id>', photo.fetch_by_album),
    path('fetch_user_photo', photo.fetch_user_photo)
]

album_patterns = [
    path('create', album.create),
    path('fetchUserAlbums', album.fetch_user_albums)
]

user_patterns = [
    path('login', user.login),
    path('register', user.register),
    path('currentUser', user.currentUser)
]

api_patterns = [
    path('user/', include(user_patterns)),
    path('album/', include(album_patterns)),
    path('photo/', include(photo_patterns))

]

urlpatterns = [
    path('', home),
    path('api/', include(api_patterns))
]
