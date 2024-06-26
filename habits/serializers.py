from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import (DurationValidator, HabitNiceValidator, RelatedHabitValidator,
                               SimultaneousSelectionValidator)


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = (
            RelatedHabitValidator(field="related_habit"),
            SimultaneousSelectionValidator(fields=("related_habit", "reward")),
            HabitNiceValidator(fields=("related_habit", "reward")),
            DurationValidator(field="duration"),
        )
