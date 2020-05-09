from datetime import datetime

from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render

from post.dtos import PostDTO
from post.models import Post, Like
from post.util import cut_text


def convert_post_to_dto(p, req, cut):
    dto = PostDTO()
    dto.id = p.id

    if cut:
        dto.tittle = cut_text(p.title, 20)
        dto.content = cut_text(p.content, 200)
    else:
        dto.tittle = p.title
        dto.content = p.content

    dto.author = p.author.first_name + ' ' + p.author.last_name
    dto.create_date = p.createDate

    current_user = req.user
    authenticated = req.user.is_authenticated

    password = p.postPassword
    if password is None or len(password) == 0:
        dto.password_required = False
    else:
        dto.password_required = True

    if authenticated:
        try:
            like = Like.objects.get(post=p, author=current_user)
        except Like.DoesNotExist:
            like = None
        if like is not None:
            dto.like = like.like
        else:
            dto.like = False

    return dto


def posts(request):
    search_text = request.GET.get('search-text', '')
    ps = Post.objects.all()
    ps_dto = []
    authenticated = request.user.is_authenticated

    for p in ps:
        ps_dto.append(convert_post_to_dto(p, request, True))

    context = {'search_text': search_text, 'blog_dto_posts': ps_dto, 'user_logged_in': authenticated}
    return render(request, 'post/posts.html', context)


def post(request, post_id):
    p = Post.objects.get(id=post_id)
    p_dto = convert_post_to_dto(p, request, False)
    authenticated = request.user.is_authenticated
    # likes = Like.objects.filter(post=p).aggregate(Count('id'))
    likes = Like.objects.filter(post=p, like=True).count()
    context = {'blog_dto_post': p_dto, 'user_logged_in': authenticated, 'count_of_likes': likes}
    return render(request, 'post/post.html', context)


def post_like(request, post_id):
    current_user = request.user
    like = request.GET.get('like')

    if like is None:
        next_action = True
    elif like == 'true':
        next_action = True
    elif like == 'false':
        next_action = False

    p = Post.objects.get(id=post_id)

    try:
        like = Like.objects.get(post=p, author=current_user)
    except Like.DoesNotExist:
        like = None

    if like is None:
        like = Like(post=p, author=current_user, like=next_action, data=datetime.now())
        like.save()
    else:
        like.like = next_action
        like.data = datetime.now()
        like.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
