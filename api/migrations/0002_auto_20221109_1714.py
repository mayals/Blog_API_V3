# Generated by Django 3.2.16 on 2022-11-09 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='user_permissions',
        ),
    ]
