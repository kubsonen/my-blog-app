from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name='index'),
    path('post/<int:post_id>', views.post, name='post_view')
]
