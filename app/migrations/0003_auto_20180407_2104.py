# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-07 21:04
from __future__ import unicode_literals

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180407_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploads',
            name='file',
            field=models.FileField(upload_to=app.models.file_path),
        ),
    ]
