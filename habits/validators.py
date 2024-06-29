from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class SimultaneousSelectionValidator:
    def __init__(self, fields: tuple[str, str]):
        self.fields = fields

    def __call__(self, value: dict):
        if not (None in [value.get(f) for f in self.fields]):
            raise serializers.ValidationError(
                _("Simultaneous selection of an associated habit and indication of a reward")
            )


class DurationValidator:
    def __init__(self, field: str):
        self.field = field

    def __call__(self, value: dict):
        duration = value.get(self.field)
        if duration:
            if value.get(self.field) > timedelta(seconds=120):
                raise serializers.ValidationError(_("Duration more than 120 seconds"))


class RelatedHabitValidator:
    def __init__(self, field: str):
        self.field = field

    def __call__(self, value: dict):
        related_habit = value.get(self.field)
        if related_habit:
            if related_habit.is_nice:
                raise serializers.ValidationError(_("Habit is nice"))


class HabitNiceValidator:
    def __init__(self, fields: tuple[str, str]):
        self.fields = fields

    def __call__(self, value: dict):
        for i, field in enumerate([value.get(f) for f in self.fields]):
            if field:
                raise serializers.ValidationError(_(f"A nice habit has a {self.fields[i]}"))
