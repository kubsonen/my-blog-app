from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Images(models.Model):
    # path = models.TextField(max_length=200)
    path = models.ImageField(upload_to='images/')
    date = models.DateField()
    name = models.TextField(max_length=200)


class Tag(models.Model):
    content = models.TextField(max_length=50)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    createDate = models.DateField()
    content = models.TextField()
    title = models.TextField(max_length=200)
    postStatus = models.TextField(max_length=50, null=True, blank=True)
    postType = models.TextField(max_length=50, null=True, blank=True)
    postPassword = models.TextField(max_length=50, null=True, blank=True)
    miniature = models.ImageField(upload_to='images/')
    postImages = models.ImageField(upload_to='images/', blank=True)
    tag = models.ManyToManyField(Tag)
    authentications = models.ManyToManyField(User, related_name='authentications', blank=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.TextField(max_length=300)


class Category(models.Model):
    content = models.TextField(max_length=50)
    posts = models.ManyToManyField(Post)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField()
    data = models.DateField()
