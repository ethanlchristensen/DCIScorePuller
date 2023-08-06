from django.db import models
from django.db.models.fields import TextField, EmailField, IntegerField, DateTimeField
from django.contrib.auth.models import User
from django.utils.timezone import now


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    title = TextField(default='')
    content = TextField(default='')
    user_likes = models.ManyToManyField(User, blank=True, related_name="user_likes")
    user_comments = models.ManyToManyField(User, blank=True, related_name="user_comments")

    def __str__(self):
        return self.title
    
    def get_likes_count(self):
        return self.user_likes.count()
    
    def get_comments_count(self):
        return self.user_comments.count()


class PostLike(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.post}"


class PostComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField

    def __str__(self):
        return f"{self.user} commented on {self.post}"