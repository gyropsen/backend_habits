from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from config import settings

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    PERIOD_CHOICES = (
        (1, "once every 1 days"),
        (7, "once every 7 days"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("owner"),
        **NULLABLE,
        help_text=_("select user"),
        related_name="habits",
    )
    place = models.CharField(max_length=256, verbose_name=_("place"), help_text=_("select place"))
    start_time = models.DateTimeField(
        default=timezone.now, verbose_name=_("start_time"), help_text=_("select start time")
    )
    action = models.TextField(max_length=2048, verbose_name=_("action"), help_text=_("select action"))
    is_nice = models.BooleanField(default=False, verbose_name=_("is_nice"), help_text=_("select nice"))
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name=_("related_habit"),
        help_text=_("select related_habit"),
    )
    period = models.IntegerField(
        default=1, choices=PERIOD_CHOICES, verbose_name=_("period"), help_text=_("select period")
    )
    reward = models.CharField(max_length=256, help_text=_("select reward"), **NULLABLE, verbose_name=_("reward"))
    duration = models.DurationField(
        default=timezone.timedelta(seconds=120), verbose_name=_("duration"), help_text=_("select duration")
    )
    is_public = models.BooleanField(default=False, verbose_name=_("is_public"), help_text=_("select public"))
    tg_mailing = models.BooleanField(default=False, verbose_name=_("tg_mailing"), help_text=_("select tg_mailing"))

    class Meta:
        verbose_name = _("habit")
        verbose_name_plural = _("habits")

    def __str__(self):
        return f"{self.action} at {self.start_time} in {self.place}"
