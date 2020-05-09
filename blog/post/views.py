from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from post.models import Post


def posts(request):
    search_text = request.GET.get('search-text', '')
    ps = Post.objects.all()
    context = {'search_text': search_text, 'blog_posts': ps}
    return render(request, 'post/posts.html', context)


def post(request, post_id):
    return render(request, 'post/post.html')
