# Generated by Django 4.2.3 on 2023-08-05 21:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_alter_post_user_likes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="like_count",
        ),
    ]