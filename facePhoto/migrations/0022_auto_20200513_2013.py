# Generated by Django 2.2.12 on 2020-05-13 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facePhoto', '0021_auto_20200513_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photohash',
            name='hash',
            field=models.BigIntegerField(max_length=30),
        ),
    ]
