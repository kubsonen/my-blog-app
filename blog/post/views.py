from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from post.dtos import PostDTO
from post.models import Post
from post.util import cut_text


def posts(request):
    search_text = request.GET.get('search-text', '')
    ps = Post.objects.all()
    ps_dto = []
    for p in ps:
        dto = PostDTO()
        dto.id = p.id
        dto.tittle = cut_text(p.title, 20)
        dto.content = cut_text(p.content, 200)
        dto.author = p.author.first_name + ' ' + p.author.last_name
        dto.create_date = p.createDate
        ps_dto.append(dto)

    context = {'search_text': search_text, 'blog_dto_posts': ps_dto}
    return render(request, 'post/posts.html', context)


def post(request, post_id):
    return render(request, 'post/post.html')
