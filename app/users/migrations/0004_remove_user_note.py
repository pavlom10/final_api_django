# Generated by Django 3.2.6 on 2021-08-18 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='note',
        ),
    ]
