# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ["title","timestamp","update"]
    list_display_links = ["update"]
    list_editable = ["title"]
    search_fields = ["title","content"]
    list_filter = ["update","timestamp"]

admin.site.register(Post, PostAdmin)