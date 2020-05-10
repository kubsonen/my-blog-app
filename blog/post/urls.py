from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.posts, name='index'),
    path('post/<int:post_id>', views.post, name='post_view'),
    path('post/<int:post_id>/comment', views.post_comment, name='post_comment'),
    path('post/comment/<int:comment_id>/remove', views.post_comment_remove, name='post_comment_remove'),
    path('like/<int:post_id>', views.post_like, name='post_like')
]
