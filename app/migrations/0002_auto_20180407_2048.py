# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-07 20:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploads',
            name='file',
            field=models.FileField(upload_to='usrs/'),
        ),
    ]
