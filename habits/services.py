import json
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import requests
from config import settings
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class TelegramBot:
    def __init__(self):
        self.token = settings.BOT_TOKEN
        self.host = settings.BOT_HOST

    def send_request(self, params: dict[str, str], method: str) -> None:
        print("send_request", params)
        url = f"{self.host}{self.token}/{method}"
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Status code: {response.status_code}\n"
                  f"Data: {response.text}")


class PeriodicTaskManager:
    @staticmethod
    def create_periodic_task(habit) -> None:
        # Создаем интервал для повтора
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=habit.period,
            period=IntervalSchedule.DAYS,
        )

        # Создаем задачу для повторения
        task, created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name=f'{habit.pk} periodic task',
            task='habits.tasks.send_message',
            args=json.dumps([habit.owner.telegram_id,
                             f'{habit.action} at {habit.start_time} in {habit.place}']),
            start_time=habit.start_time
        )
        return task if task else created

    def update_periodic_task(self, update_habit):
        active_task: PeriodicTask = self.create_periodic_task(update_habit)
        if active_task.start_time.time != update_habit.start_time.time:
            active_task.start_time = datetime.combine(active_task.start_time.date(), update_habit.start_time.time(),
                                                      tzinfo=update_habit.start_time.tzinfo)
        active_task.save()

    @staticmethod
    def delete_periodic_task(instance):
        try:
            active_task = PeriodicTask.objects.get(name=f'{instance.pk} periodic task')
        except ObjectDoesNotExist:
            return
        else:
            active_task.delete()
