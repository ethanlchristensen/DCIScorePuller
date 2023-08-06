from django.contrib import admin

from .models import Post, PostComment, PostLike

admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(PostComment)
