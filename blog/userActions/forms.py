from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    login = forms.CharField(label="login")
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(UserCreationForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'input',  'placeholder':'E-mail'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input', 'placeholder':'Password' }, render_value=True))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input', 'placeholder':'Repeat password'}, render_value=True))
    class Meta:
        model=User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class':'input', 'placeholder':'Login'}),
        }

