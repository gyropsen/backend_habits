from rest_framework import generics

from habits.models import Habit
from habits import serializers


class HabitListAPIView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = serializers.HabitSerializer

    def perform_create(self, serializer):
        new_habit = serializer.save(owner=self.request.user)
        super().perform_create(new_habit)
