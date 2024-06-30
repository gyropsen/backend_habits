from datetime import datetime

from django.urls import reverse
from django_celery_beat.models import PeriodicTask
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_user = User.objects.create(
            telegram_id="12345",
            chat_id="12345",
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

        self.client.force_authenticate(user=self.test_user)
        self.test_habit = Habit.objects.create(
            owner=self.test_user,
            action="walk",
            place="street",
            start_time="2024-06-30T14:54:00+03:00",
            tg_mailing=True,
        )

    def test_create_habit_and_periodic_task(self):
        """
        Тестирование создания привычки и периодической задачи
        """
        url = reverse("habits:my_habits-list")
        data = {
            "start_time": "2024-06-30T14:54:00+03:00",
            "action": "read the books",
            "place": "home",
            "tg_mailing": True,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        habit = response.json()
        self.assertEqual(habit.get("action"), data["action"])
        self.test_periodic_task = PeriodicTask.objects.get(name=f"{habit.get("id")} periodic task")
        self.assertEqual(self.test_periodic_task.start_time, datetime.fromisoformat(data["start_time"]))

    def test_get_habits_list(self):
        """
        Тестирование получения списка своих привычек
        """
        url = reverse("habits:my_habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habits_list = response.json()
        self.assertEqual(habits_list.get("results")[0].get("action"), self.test_habit.action)

    def test_get_habit(self):
        """
        Тестирование получения привычки
        """
        url = reverse("habits:my_habits-detail", args=(self.test_habit.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit = response.json()
        self.assertEqual(habit.get("action"), self.test_habit.action)

    def test_update_habit(self):
        """
        Тестирование обновления привычки
        """
        url = reverse("habits:my_habits-detail", args=(self.test_habit.pk,))
        data = {"tg_mailing": False}
        response = self.client.patch(url, data=data)
        habit = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(habit.get("tg_mailing"), data["tg_mailing"])

    def test_delete_habit(self):
        """
        Тестирование удаления привычки
        """
        url = reverse("habits:my_habits-detail", args=(self.test_habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
