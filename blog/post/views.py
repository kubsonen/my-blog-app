from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def posts(request):
    page = request.GET.get('page', '')
    context = {}
    return render(request, 'post/posts.html')


def post(request, post_id):
    return render(request, 'post/post.html')
