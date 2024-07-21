from django.contrib.auth.models import AbstractUser
from django.db import models

from publications.models import NULLABLE


class User(AbstractUser):
    """
    Модель пользователя.
    """
    username = None
    phone = models.CharField(unique=True, verbose_name='Телефон')
    email = models.EmailField(max_length=20, verbose_name='Почта', **NULLABLE)
    country = models.CharField(max_length=20, verbose_name='Страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatars', verbose_name='Аватар', **NULLABLE)
    activ_subscription = models.BooleanField(default=False, verbose_name='Активация подписки')
    key = models.CharField(max_length=6, verbose_name='Ключ', **NULLABLE)
    pay_id = models.CharField(max_length=300, verbose_name='ID оплаты', **NULLABLE)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
