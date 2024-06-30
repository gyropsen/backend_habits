from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits import serializers
from habits.models import Habit
from habits.paginators import CustomPagination
from habits.permissions import IsOwner
from habits.services import PeriodicTaskManager

task_manager = PeriodicTaskManager()


class HabitViewSet(ModelViewSet):
    """
    Эндпоинт для работы со своими привычками
    """

    queryset = Habit.objects.all().order_by("pk")
    serializer_class = serializers.HabitSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer: serializers.HabitSerializer) -> None:
        """
        Указание владельца сохраняемой привычки
        :param serializer: serializers.HabitSerializer
        """
        new_habit = serializer.save(owner=self.request.user)
        new_habit.save()
        if new_habit.tg_mailing:
            task_manager.create_periodic_task(new_habit)

    def perform_update(self, serializer: serializers.HabitSerializer) -> None:
        """
        Обновление привычки и, если надо взаимодействие с периодическим заданием
        :param serializer: serializers.HabitSerializer
        :return: None
        """
        update_habit = serializer.save()
        update_habit.save()
        if update_habit.tg_mailing:
            task_manager.update_periodic_task(update_habit)
        else:
            task_manager.delete_periodic_task(update_habit)

    def perform_destroy(self, instance: Habit) -> None:
        """
        Удаление привычки и, если надо, удаление периодической задачи
        :param instance: Habit
        :return:
        """
        if instance.tg_mailing:
            task_manager.delete_periodic_task(instance)
        instance.delete()

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
