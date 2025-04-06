# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()  # Создаем экземпляр APIClient для отправки запросов
        self.url = reverse('register')  # Это URL для регистрации, который вы используете в приложении

    def test_user_registration(self):
        # Данные для отправки на сервер (можно менять в зависимости от того, как настроен API)
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "mypassword"
        }

        # Отправляем POST-запрос на сервер
        response = self.client.post(self.url, data, format='json')

        # Проверяем, что статус код ответа - 201 (это значит, что пользователь был успешно создан)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Также можно добавить проверку, чтобы убедиться, что данные возвращаются корректно
        self.assertEqual(response.data['username'], 'testuser')
