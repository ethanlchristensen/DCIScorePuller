from django.contrib import admin
from .models import Post, PostLike, PostComment

admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(PostComment)
