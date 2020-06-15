# authentication imports:
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            _userName = request.POST['login']
            _userPassword = request.POST['password']
            user = authenticate(request, username=_userName, password=_userPassword)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')

    else:
        form = LoginForm()

    return render(request, 'userActions/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/userActions/login?success-register')
    else:
        form = RegisterForm()

    return render(request, 'userActions/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
