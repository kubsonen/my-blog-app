from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader

from .forms import LoginForm, RegisterForm

from django.contrib.auth.models import User

# authentication imports:
from django.contrib.auth import authenticate, login, logout

import sys



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            _userName = request.POST['login']
            _userPassword = request.POST['password']
            user = authenticate(request, username=_userName, password = _userPassword)

            if user is not None:
                login(request, user)
                return render(request, 'post/posts.html')
                
    else:
        form = LoginForm()

    return render(request, 'userActions/login.html', {'form':form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'userActions/register.html', {'form':form})


def logout_View(request):
    logout(request)
    return render(request, 'post/posts.html')



