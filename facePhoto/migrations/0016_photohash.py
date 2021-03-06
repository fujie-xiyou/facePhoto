# Generated by Django 2.2.12 on 2020-05-13 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facePhoto', '0015_facealbum_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoHash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.IntegerField()),
                ('photo', models.OneToOneField(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='facePhoto.Photo')),
            ],
            options={
                'db_table': 'photo_hash',
            },
        ),
    ]
