# Generated by Django 4.0.2 on 2022-02-22 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0003_alter_userprofile_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
    ]
