from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class SimultaneousSelectionValidator:
    def __init__(self, fields: tuple[str, str]):
        self.fields = fields

    def __call__(self, value):
        if not (None in [value.get(f) for f in self.fields]):
            raise serializers.ValidationError(
                "Simultaneous selection of an associated habit and indication of a reward")
