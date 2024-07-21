from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from users.models import User


class UserTest(TestCase):
    """
    Тест пользователя.
    """
    def setUp(self):
        self.client = Client()
        self.valid_data = {
            'phone': '89987654321',
            'activ_subscription': True,
            'password1': 'test_password',
            'password2': 'test_password',
        }

    def test_register(self):
        """
        Тест регистрации пользователя.
        """
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_form.html')
        self.client.post(reverse('users:register'), data=self.valid_data)
        self.assertEqual(User.objects.count(), 1)

    def test_update_user(self):
        """
        Тест редактирования пользователя.
        """
        self.user_update = User.objects.all().filter(id=self.user.id).first()
        response = self.client.get(reverse_lazy('users:update_user'))
        self.assertEqual(response.status_code, 200)
