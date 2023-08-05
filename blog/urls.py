from django.urls import path

from .views import *

urlpatterns = [
    path("blog/", view=home, name="blog-home"),
    path("blog/like/<int:post_id>", view=like_unlike_post, name="like-post"),
    path("blog/unlike/<int:post_id>", view=like_unlike_post, name="unlike-post"),
]