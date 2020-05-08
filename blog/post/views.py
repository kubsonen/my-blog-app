from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def posts(request):
    search_text = request.GET.get('search-text', '')
    context = {'search_text': search_text}
    return render(request, 'post/posts.html', context)


def post(request, post_id):
    return render(request, 'post/post.html')
