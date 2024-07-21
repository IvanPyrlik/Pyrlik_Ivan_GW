from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from publications.models import Publication
from users.models import User


class PublicationViewTest(TestCase):
    """
    Тест публикаций.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(phone='89987654321', password='123qw456er')
        self.client.force_login(self.user)

    def test_create_pub(self):
        """
        Тест создания публикации.
        """
        response = self.client.get(reverse('publications:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publications/publication_form.html')
        data = {
            'name': 'Test',
            'content': 'Text test',
        }
        response = self.client.post(reverse('publications:create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('publications:list'))
        self.assertEqual(Publication.objects.all().filter(owner_id=self.user).first().name, 'Test')

    def test_list(self):
        """
        Тест списка.
        """
        response = self.client.get(reverse('publications:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Publication.objects.count(), 1)

    def test_update(self):
        """
        Тест редактирования публикации.
        """
        self.pub_update = Publication.objects.all().filter(owner_id=self.user).first()
        response = self.client.get(reverse_lazy('publications:update', kwargs={'pk': self.pub_update.id}))
        self.assertEqual(response.status_code, 200)
        data = {'name': 'Update test',
                'content': 'Update text test'}
        response = self.client.post(reverse('publications:update', kwargs={'pk': self.pub_update.id}), data=data)
        self.assertEqual(response.status_code, 302)
        self.pub_update.refresh_from_db()
        self.assertEqual(self.pub_update.name, 'Update test')
        self.assertEqual(self.pub_update.content, 'Update text test')

    def test_user_public(self):
        """
        Тест просмотра публикаций пользователя.
        """
        response = self.client.get(reverse_lazy('publications:user_public'))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        """
        Тест удаления публикации.
        """
        self.pub_delete = Publication.objects.all().filter(owner_id=self.user).first()
        response = self.client.get(reverse_lazy('publications:delete', kwargs={'pk': self.pub_delete.id}))
        self.assertEqual(response.status_code, 200)
        self.client.delete(reverse_lazy('publications:delete', kwargs={'pk': self.pub_update.id}))
        self.assertEqual(Publication.objects.count(), 0)
        self.pub_delete.refresh_from_db()
