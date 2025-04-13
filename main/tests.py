from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class AuthenticationTests(TestCase):
    def setUp(self):
        # Создаем пользователя для тестов
        self.user = User.objects.create_user(username='testuser', password='12345', email='test@example.com')

    def test_login_valid_user(self):
        # Тестирование логина с правильными данными
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_user(self):
        # Тестирование логина с неправильным паролем
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)

    def test_access_restricted_page_with_login(self):
        # Тестирование доступа к защищенной странице с логином
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('car_list'))
        self.assertEqual(response.status_code, 200)

    def test_access_restricted_page_without_login(self):
        # Тестирование доступа к защищенной странице без логина
        response = self.client.get(reverse('car_list'))
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект на страницу входа
