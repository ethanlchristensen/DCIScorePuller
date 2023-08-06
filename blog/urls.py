from django.urls import path

from .views import (home, like_unlike_post, create_post,
                    delete_post, update_post, view_post,
                    add_comment, update_comment, get_comment_data_modal,
                    delete_comment)

urlpatterns = [
    path("blog/", view=home, name="blog-home"),
    path("blog/post/like/<int:post_id>", view=like_unlike_post, name="like-post"),
    path("blog/post/unlike/<int:post_id>", view=like_unlike_post, name="unlike-post"),
    path("blog/post/create", view=create_post, name="create-post"),
    path("blog/post/<int:post_id>/delete", view=delete_post, name="delete-post"),
    path("blog/post/<int:post_id>/update", view=update_post, name="update-post"),
    path("blog/post/<int:post_id>/view", view=view_post, name="view-post"),
    path("blog/post/<int:post_id>/comment/add", view=add_comment, name="add-comment"),
    path("blog/post/<int:post_id>/comment/<int:comment_id>/get/modalData", view=get_comment_data_modal, name="get-modal-data"),
    path("blog/post/<int:post_id>/comment/<int:comment_id>/update", view=update_comment, name="update-comment"),
    path("blog/post/<int:post_id>/comment/<int:comment_id>/delete", view=delete_comment, name="delete-comment"),
]
