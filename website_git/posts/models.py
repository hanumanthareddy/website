# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
# Create your models here.
# MVC architecture

class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.FileField(null=True)
    content = models.TextField()
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title
    
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance)
        return content_type
