from django.contrib.auth.models import User
from django.db import models
from PIL import Image


class Profile(models.Model):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"

    VISIBILITY_CHOICES = ((PUBLIC, "Public"), (PRIVATE, "Private"))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")
    visibility = models.CharField(max_length=10, default="PRIVATE", choices=VISIBILITY_CHOICES)
    bio = models.TextField(default="")

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
