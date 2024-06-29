from celery import shared_task

from habits.services import TelegramBot


@shared_task
def send_message(chat_id: str, text: str) -> None:
    """
    Отправляет сообщение в Telegram
    :param chat_id: id чата, куда будет отправлено
    :param text: текст отправки
    :return: None
    """
    bot = TelegramBot()
    bot.send_request(params={"chat_id": chat_id, "text": text}, method="sendMessage")
