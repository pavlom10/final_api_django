# Generated by Django 3.2.6 on 2021-08-21 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='state',
            field=models.BooleanField(default=True, verbose_name='on'),
        ),
    ]