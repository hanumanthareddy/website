# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model
from .forms import PostForm
from comments.forms import CommentForm
from comments.models import Comment
from .models import Post
def post_list(request):
    queryset_list = Post.objects.all().order_by('-timestamp')
    query = request.GET.get("q")

    paginator = Paginator(queryset_list, 5)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    if query:
        queryset = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
            ).distinct()
    context = {
            "object_list" : queryset
    }
    return render(request, "index.html", context)


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect('/')
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
            "form" : form,
    }
    return render(request, "create_post.html", context)

def post_details(request, id=None):
    instance = get_object_or_404(Post, id=id)
    initial_data = {
        "content_type" : instance.get_content_type,
        "object_id" : instance.id
    }
    comment_form = CommentForm(request.POST or None, request.FILES or None, initial=initial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get('object_id')
        content_data = comment_form.cleaned_data.get("content")
        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data
        )
        return HttpResponseRedirect('/')
    comments = instance.comments 
    context = {
        "instance" : instance,
        "title" : instance.title,
        "comments" : comments,
        "comment_form" : comment_form
    }
    return render(request, "post_details.html", context)

def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect('/')
    context = {
            "form" : form,
            "instance" : instance,
            "title" : instance.title,
    }
    return render(request, "update_post.html", context)

def post_delete(request):
    return HttpResponse("<h1>delete</h1>")
