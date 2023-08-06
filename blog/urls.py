from django.urls import path

from .views import *

urlpatterns = [
    path("blog/", view=home, name="blog-home"),
    path("blog/post/like/<int:post_id>", view=like_unlike_post, name="like-post"),
    path("blog/post/unlike/<int:post_id>", view=like_unlike_post, name="unlike-post"),
    path("blog/post/create", view=create_post, name="create-post"),
    path("blog/post/delete/<int:post_id>", view=delete_post, name="delete-post"),
    path("blog/post/update/<int:post_id>", view=update_post, name="update-post"),
]