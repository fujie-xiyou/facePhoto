# Generated by Django 2.2.12 on 2020-05-05 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facePhoto', '0014_auto_20200505_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='facealbum',
            name='description',
            field=models.CharField(default='暂无描述', max_length=100),
            preserve_default=False,
        ),
    ]