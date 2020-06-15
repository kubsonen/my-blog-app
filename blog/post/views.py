from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from post.dtos import PostDTO, CommentDTO
from post.forms import CommentForm, PasswordForm
from post.models import Post, Like, Comment, Images
from post.util import cut_text
from django.core.paginator import Paginator


def convert_post_to_dto(p, req, cut):
    dto = PostDTO()
    dto.id = p.id

    if p.postImages:
        dto.mainImage = p.postImages.url
    else:
        dto.mainImage = 'https://bulma.io/images/placeholders/96x96.png'

    if p.miniature:
        dto.miniature = p.miniature.url
    else:
        dto.miniature = 'https://bulma.io/images/placeholders/96x96.png'

    if cut:
        dto.tittle = cut_text(p.title, 20)
        dto.content = cut_text(p.content, 200)
    else:
        dto.tittle = p.title
        dto.content = p.content

    dto.author = p.author.first_name + ' ' + p.author.last_name
    if dto.author is None or len(dto.author.strip()) == 0:
        dto.author = p.author.username

    dto.create_date = p.createDate

    tags = []
    for t in p.tag.all():
        tags.append(t.content)
    dto.tags = tags

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

        if p.authentications:
            for a in p.authentications.all():
                if a.id == current_user.id:
                    dto.unlock = True

    return dto


def convert_comment_to_dto(c):
    dto = CommentDTO()
    dto.id = c.id
    dto.author = c.author.first_name + ' ' + c.author.last_name
    if dto.author is None or len(dto.author.strip()) == 0:
        dto.author = c.author.username
    dto.create_date = c.date
    dto.content = c.content
    return dto


def posts(request):
    search_text = request.GET.get('search-text', '')
    ps = Post.objects.all()
    ps_dto = []
    authenticated = request.user.is_authenticated

    for p in ps:
        if search_text:
            search_text = search_text.lower()
            if search_text in p.author.first_name.lower() or search_text in p.title.lower() or search_text in p.content.lower():
                ps_dto.append(convert_post_to_dto(p, request, True))
        else:
            ps_dto.append(convert_post_to_dto(p, request, True))
            
    paginator = Paginator(ps_dto, 1)
    page_number = request.GET.get('page')
    page_obj = {}
    if paginator:
        page_obj = paginator.get_page(page_number)

    context = {
        'search_text': search_text,
        'blog_dto_posts': ps_dto,
        'user_logged_in': authenticated,
        'page_obj': page_obj
    }

    return render(request, 'post/posts.html', context)


def post(request, post_id):
    p = Post.objects.get(id=post_id)
    p_dto = convert_post_to_dto(p, request, False)
    current_user = request.user
    authenticated = current_user.is_authenticated
    likes = Like.objects.filter(post=p, like=True).count()

    comments = Comment.objects.filter(post=p)
    comment_dtos = []
    for c in comments:
        dto = convert_comment_to_dto(c)
        dto.my_own = False
        if authenticated and c.author.id == current_user.id:
            dto.my_own = True
        comment_dtos.append(dto)

    context = {'blog_dto_post': p_dto, 'user_logged_in': authenticated, 'count_of_likes': likes,
               'comments': comment_dtos, 'comment_count': len(comments)}

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


def post_comment(request, post_id):
    p = Post.objects.get(id=post_id)
    current_user = request.user

    if not current_user.is_authenticated:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = Comment(post=p, author=current_user, date=datetime.now(), content=form.cleaned_data['comment'])
            c.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def post_comment_remove(request, comment_id):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    c = Comment.objects.get(id=comment_id)
    if c.author.id == current_user.id:
        c.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def post_password(request, post_id):
    current_user = request.user
    referrer = request.META.get('HTTP_REFERER');
    referrer = referrer.replace('user-not-login', '').replace('wrong-post-password', '').replace('?', '')

    if not current_user.is_authenticated:
        return HttpResponseRedirect(referrer + '?user-not-login')

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            p = Post.objects.get(id=post_id)
            input_password = form.cleaned_data['password']
            if p.postPassword == input_password:
                p.authentications.add(current_user)
            else:
                return HttpResponseRedirect(referrer + '?wrong-post-password')

    return HttpResponseRedirect('/post/' + str(post_id))
