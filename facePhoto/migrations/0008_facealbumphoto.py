# Generated by Django 2.2.12 on 2020-05-04 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facePhoto', '0007_facealbum'),
    ]

    operations = [
        migrations.CreateModel(
            name='FaceAlbumPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('face_album', models.ForeignKey(db_column='face_album_id', on_delete=django.db.models.deletion.CASCADE, to='facePhoto.FaceAlbum')),
                ('photo', models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='facePhoto.Photo')),
            ],
            options={
                'db_table': 'face_album_photo',
            },
        ),
    ]
