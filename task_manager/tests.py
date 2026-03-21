from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.models import Status

class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.status = Status.objects.create(name='Новый')
        self.list_url = reverse('statuses_list')
        self.create_url = reverse('status_create')
        self.update_url = reverse('status_update', args=[self.status.id])
        self.delete_url = reverse('status_delete', args=[self.status.id])

    def test_access_denied_for_anonymous(self):
        # Проверяем, что неавторизованного редиректит на логин
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)

    def test_status_list(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)

    def test_status_create(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.create_url, {'name': 'В работе'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='В работе').exists())

    def test_status_update(self):
        self.client.login(username='testuser', password='password')
        self.client.post(self.update_url, {'name': 'Завершен'})
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Завершен')

    def test_status_delete(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())