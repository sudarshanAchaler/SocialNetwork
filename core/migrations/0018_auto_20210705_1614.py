# Generated by Django 3.1.3 on 2021-07-05 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20210705_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='no_of_Followers',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='no_of_Following',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='no_of_Posts',
        ),
    ]
