# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os
# Create your models here.


def file_path(instance, filename):
    dir_path = '/'.join(['uploads', str(instance.bookid)])
    path = '/'.join(['media', dir_path])
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    file_path = os.path.join(dir_path, filename)
    return file_path


class Uploads(models.Model):
    bookid = models.IntegerField()
    file = models.FileField(upload_to=file_path)
    filename = models.CharField(max_length = 255)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)
    
    def __str__(self):
        return "{}, {}".format(self.bookid, self.filename)
