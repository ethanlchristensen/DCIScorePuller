# Generated by Django 4.2.3 on 2023-08-05 18:45

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                ("key", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("title", models.TextField(default="")),
                ("content", models.TextField(default="")),
                ("likes", models.IntegerField(default=0)),
                ("comments", models.IntegerField(default=0)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
