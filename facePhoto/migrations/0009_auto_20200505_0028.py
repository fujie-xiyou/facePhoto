# Generated by Django 2.2.12 on 2020-05-04 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facePhoto', '0008_facealbumphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facealbum',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='photoembedding',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
