from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters

from habits import serializers
from habits.models import Habit
from habits.paginators import CustomPagination
from habits.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    """
    Эндпоинт для работы со своими привычками
    """
    queryset = Habit.objects.all().order_by("pk")
    serializer_class = serializers.HabitSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer: serializers.HabitSerializer) -> None:
        """
        Указание владельца сохраняемой привычке
        :param serializer: serializers.HabitSerializer
        """
        new_habit = serializer.save(owner=self.request.user)
        super().perform_create(new_habit)

    def get_queryset(self) -> queryset:
        """
        Получение объектов, где пользователь является владельцем
        :return: Queryset
        """
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def get_permissions(self) -> list:
        """
        Instantiates and returns the create of permissions that this view requires.
        """
        if self.action != "list":
            permission_classes = (IsAuthenticated, IsOwner)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]


class HabitListAPIView(generics.ListAPIView):
    """
    Эндпоинт для получения всех публичных привычек
    """
    queryset = Habit.objects.filter(is_public=True).order_by("pk")
    serializer_class = serializers.HabitSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("is_nice", "related_habit", "period")
    ordering_fields = ("start_time",)
