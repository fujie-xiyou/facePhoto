from django.db import models
from django.utils.timezone import now


class User(models.Model):
    class Meta:
        db_table = 'user'

    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    mobile = models.CharField(max_length=11)
    password = models.CharField(max_length=35)


class Album(models.Model):
    class Meta:
        db_table = 'album'

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, db_column='uid')
    create_time = models.DateTimeField(default=now)


class Photo(models.Model):
    class Meta:
        db_table = 'photo'

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, db_column='uid')
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE, db_column='aid')
    name = models.CharField(max_length=64)
    path = models.CharField(max_length=100)
    is_analyzed = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=now)


class PhotoEmbedding(models.Model):
    class Meta:
        db_table = 'photo_embedding'
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, db_column='uid')
    photo = models.ForeignKey(to=Photo, on_delete=models.CASCADE, db_column='pid')
    embedding = models.TextField()
    type = models.IntegerField()


class FaceAlbum(models.Model):
    class Meta:
        db_table = 'face_album'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, db_column='uid')


class FaceAlbumNameNumber(models.Model):
    class Meta:
        db_table = 'face_album_name_number'
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, db_column='uid')
    number = models.IntegerField(default=1)


class FaceAlbumPhoto(models.Model):
    class Meta:
        db_table = 'face_album_photo'

    photo = models.ForeignKey(to=Photo, on_delete=models.CASCADE, db_column='pid')
    face_album = models.ForeignKey(to=FaceAlbum, on_delete=models.CASCADE, db_column='face_album_id')
