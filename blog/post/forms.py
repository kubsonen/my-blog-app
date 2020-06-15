from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea())


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.Textarea())
