# Generated by Django 4.2.3 on 2023-08-05 21:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0003_rename_likes_post_like_count_post_user_likes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="user_likes",
            field=models.ManyToManyField(
                blank=True, related_name="user_likes", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
