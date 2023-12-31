# Generated by Django 4.2.3 on 2023-08-05 03:00

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Competition",
            fields=[
                ("key", models.AutoField(primary_key=True, serialize=False)),
                (
                    "competition_name",
                    models.TextField(default="No Competition Name Provided"),
                ),
                (
                    "competition_name_original",
                    models.TextField(default="No Original Competition Name Provided"),
                ),
                (
                    "competition_date",
                    models.DateField(default=django.utils.timezone.now),
                ),
                ("competition_date_as_string", models.TextField(default="")),
            ],
        ),
        migrations.CreateModel(
            name="ContAchvTotal",
            fields=[
                ("key", models.AutoField(primary_key=True, serialize=False)),
                (
                    "cont",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
                ),
                (
                    "achv",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
                ),
                (
                    "total",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Corp",
            fields=[
                ("key", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.TextField(default="No Corp Name Provided")),
            ],
        ),
        migrations.CreateModel(
            name="GeneralEffect",
            fields=[
                ("key", models.AutoField(primary_key=True, serialize=False)),
                (
                    "general_effect_total",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Music",
            fields=[
                ("key", models.AutoField(primary_key=True, serialize=False)),
                (
                    "music_total",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
                ),
                (
                    "music_analysis_one",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="music_analysis_one",
                        to="pull.contachvtotal",
                    ),
                ),
                (
                    "music_analysis_two",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="music_analysis_two",
                        to="pull.contachvtotal",
                    ),
                ),
                (
                    "music_brass",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="music_brass",
                        to="pull.contachvtotal",
                    ),
                ),
                (
                    "music_percussion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="music_percussion",
                        to="pull.contachvtotal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RepPerfTotal",
            fields=[
                ("key", models.AutoField(primary_key=True, serialize=False)),
                (
                    "rep",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
                ),
                (
                    "perf",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
                ),
                (
                    "total",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Visual",
            fields=[
                ("key", models.AutoField(primary_key=True, serialize=False)),
                (
                    "visual_total",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
                ),
                (
                    "color_guard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="color_guard",
                        to="pull.contachvtotal",
                    ),
                ),
                (
                    "visual_analysis",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="visual_analysis",
                        to="pull.contachvtotal",
                    ),
                ),
                (
                    "visual_proficiency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="visual_proficiency",
                        to="pull.contachvtotal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Show",
            fields=[
                ("key", models.AutoField(primary_key=True, serialize=False)),
                (
                    "total_score",
                    models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
                ),
                (
                    "competition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="competition",
                        to="pull.competition",
                    ),
                ),
                (
                    "corp",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="corp",
                        to="pull.corp",
                    ),
                ),
                (
                    "general_effect",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="general_effect",
                        to="pull.generaleffect",
                    ),
                ),
                (
                    "music",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="music",
                        to="pull.music",
                    ),
                ),
                (
                    "visual",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="visual",
                        to="pull.visual",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="generaleffect",
            name="general_effect_one_one",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="general_effect_one_one",
                to="pull.repperftotal",
            ),
        ),
        migrations.AddField(
            model_name="generaleffect",
            name="general_effect_one_two",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="general_effect_one_two",
                to="pull.repperftotal",
            ),
        ),
        migrations.AddField(
            model_name="generaleffect",
            name="general_effect_two_one",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="general_effect_two_one",
                to="pull.repperftotal",
            ),
        ),
        migrations.AddField(
            model_name="generaleffect",
            name="general_effect_two_two",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="general_effect_two_two",
                to="pull.repperftotal",
            ),
        ),
    ]
