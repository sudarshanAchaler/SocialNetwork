# Generated by Django 3.1.3 on 2021-06-27 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210627_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='pro_pic',
        ),
    ]
