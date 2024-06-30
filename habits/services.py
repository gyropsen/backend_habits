import json
from datetime import datetime

import requests
from django.core.exceptions import ObjectDoesNotExist
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from config import settings
from habits.models import Habit


class TelegramBot:
    """
    Класс для работы с ботом
    """

    def __init__(self):
        """
        Инициализация
        """
        self.token = settings.BOT_TOKEN
        self.host = settings.BOT_HOST

    def send_request(self, params: dict[str, str], method: str) -> bool:
        """
        Отправка запроса
        :param params: параметры в запросе
        :param method: метод запроса
        :return: None
        """
        url = f"{self.host}{self.token}/{method}"
        response = requests.get(url, params=params)
        # В зависимости от кода ошибки вернуть True или False
        if response.status_code != 200:
            print(f"Status code: {response.status_code}\n" f"Data: {response.text}")
            return False
        else:
            return True


class PeriodicTaskManager:
    """
    Класс для работы с периодическими задачами
    """

    @staticmethod
    def create_periodic_task(habit: Habit) -> None:
        """
        Создание периодической задачи
        :param habit: Habit
        :return: None
        """
        # Создаем интервал для повтора
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=habit.period,
            period=IntervalSchedule.DAYS,
        )

        # Создаем задачу для повторения
        task, created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name=f"{habit.pk} periodic task",
            task="habits.tasks.send_message",
            args=json.dumps(
                [habit.owner.telegram_id, habit.pk, f"{habit.action} at {habit.start_time} in {habit.place}"]
            ),
            start_time=habit.start_time,
        )
        return task if task else created

    def update_periodic_task(self, update_habit: Habit) -> None:
        """
        Обновление периодической задачи
        :param update_habit: Обновляемая привычка
        :return: None
        """
        # Если при создании привычки не создана задача и пользователь хочет создать задачу, то создаем ее
        active_task: PeriodicTask = self.create_periodic_task(update_habit)
        # Если время менялось, то обновляем время задачи
        if active_task.start_time.time != update_habit.start_time.time:
            active_task.start_time = datetime.combine(
                active_task.start_time.date(), update_habit.start_time.time(), tzinfo=update_habit.start_time.tzinfo
            )
        active_task.save()

    @staticmethod
    def delete_periodic_task(instance: Habit) -> None:
        """
        Удаление периодической задачи
        :param instance: Habit
        :return: None
        """
        try:
            # Найти задачу
            active_task = PeriodicTask.objects.get(name=f"{instance.pk} periodic task")
        except ObjectDoesNotExist:
            # Если задачи нет, то ничего не делаем
            return
        else:
            # Если задача есть, то удаляем ее
            active_task.delete()
