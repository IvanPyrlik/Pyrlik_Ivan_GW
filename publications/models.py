from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

NULLABLE = {'blank': True, 'null': True}


class Publication(models.Model):
    """
    Модель публикации.
    """
    name = models.CharField(max_length=250, verbose_name='Наименование')
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='publications/images', verbose_name='Изображение', **NULLABLE)
    publication_date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    paid_publication = models.BooleanField(default=False, verbose_name='Платная публикация')
    is_active = models.BooleanField(default=True, verbose_name='Активность публикации')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name="Владелец публикации")

    def save(self, *args, **kwargs):
        if not self.owner:
            self.owner = get_user_model().objects.get(is_active=True)
        else:
            self.owner = self.owner
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.image} {self.content}'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
