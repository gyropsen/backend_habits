from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def test_registration_user(self):
        """
        Тестирование регистрации пользователя
        """
        url = reverse("users:registration")
        data = {"telegram_id": "12345", "chat_id": "12345", "password": "12345"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        super().tearDown()
        for user in User.objects.all():
            user.delete()
