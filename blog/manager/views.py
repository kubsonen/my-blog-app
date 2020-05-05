from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("Hello my manager dashboard")


def post(request):
    return HttpResponse("Post list")


def post_form(request):
    return HttpResponse("Post form")
