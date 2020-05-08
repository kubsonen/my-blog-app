from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.

def login(request):
    return render(request, 'userActions/login.html')


def register(request):
    return render(request, 'userActions/register.html')
