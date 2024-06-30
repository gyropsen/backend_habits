from celery import shared_task

from habits.models import Habit
from habits.services import PeriodicTaskManager, TelegramBot

bot = TelegramBot()
task_manager = PeriodicTaskManager()


@shared_task
def send_message(telegram_id: str, habit_pk: str, text: str) -> None:
    """
    Отправляет сообщение в Telegram
    :param telegram_id: Telegram ID
    :param habit_pk: Идентификатор привычки
    :param text: Текст сообщения
    :return: None
    """
    status: bool = bot.send_request(params={"chat_id": telegram_id, "text": text}, method="sendMessage")
    # Если сообщение не отправлено, то удалить периодическую задачу
    if not status:
        habit = Habit.objects.get(pk=habit_pk)
        habit.tg_mailing = False
        habit.save()
        task_manager.delete_periodic_task(habit)
