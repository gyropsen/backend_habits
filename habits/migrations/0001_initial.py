# Generated by Django 5.0.6 on 2024-06-27 19:17

import datetime

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Habit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("place", models.CharField(help_text="select place", max_length=256, verbose_name="place")),
                (
                    "start_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now, help_text="select start time", verbose_name="start_time"
                    ),
                ),
                ("action", models.TextField(help_text="select action", max_length=2048, verbose_name="action")),
                ("is_nice", models.BooleanField(default=False, help_text="select nice", verbose_name="is_nice")),
                (
                    "period",
                    models.IntegerField(
                        choices=[(1, "once every 1 days"), (7, "once every 7 days")],
                        default=1,
                        help_text="select period",
                        verbose_name="period",
                    ),
                ),
                (
                    "reward",
                    models.CharField(
                        blank=True, help_text="select reward", max_length=256, null=True, verbose_name="reward"
                    ),
                ),
                (
                    "duration",
                    models.DurationField(
                        default=datetime.timedelta(seconds=120), help_text="select duration", verbose_name="duration"
                    ),
                ),
                ("is_public", models.BooleanField(default=False, help_text="select public", verbose_name="is_public")),
            ],
            options={
                "verbose_name": "habit",
                "verbose_name_plural": "habits",
            },
        ),
    ]
