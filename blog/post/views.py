from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def index(request):
    page = request.GET.get('page', '')
    template = loader.get_template('post/posts.html')
    context = {}
    return render(request, 'post/posts.html')


def post(request, post_id):
    return HttpResponse("Hello my post %d" % post_id)
