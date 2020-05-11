# Generated by Django 2.2.12 on 2020-05-03 16:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'album',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('path', models.CharField(max_length=100)),
                ('is_analyzed', models.IntegerField()),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('album', models.ForeignKey(db_column='aid', on_delete=django.db.models.deletion.CASCADE, to='facePhoto.Album')),
            ],
            options={
                'db_table': 'photo',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=11)),
                ('password', models.CharField(max_length=35)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='PhotoEmbedding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('embedding', models.TextField()),
                ('type', models.IntegerField()),
                ('photo', models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='facePhoto.Photo')),
            ],
            options={
                'db_table': 'photo_embedding',
            },
        ),
        migrations.AddField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to='facePhoto.User'),
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to='facePhoto.User'),
        ),
    ]