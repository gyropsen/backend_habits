from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Класс отображения привычки в админке
    """

    list_display = (
        "pk",
        "action",
        "tg_mailing",
        "place",
    )
