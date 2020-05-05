from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='manager'),
    path('post', views.post, name='post_list'),
    path('post-form', views.post_form, name='post_form')
]
