from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import TextField


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    title = TextField(default="")
    content = TextField(default="")
    user_likes = models.ManyToManyField(User, blank=True, related_name="user_likes")
    user_comments = models.ManyToManyField(User, blank=True, related_name="user_comments")

    def __str__(self):
        return self.title

    def get_likes_count(self):
        return self.user_likes.count()

    def get_comments_count(self):
        return PostComment.objects.filter(post=self).count()


class PostLike(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.post}"


class PostComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(default="")
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} commented on {self.post}"
