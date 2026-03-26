from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Label, Status, Task


class TasksTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем двух пользователей: автора и "чужого"
        self.author = User.objects.create_user(username='author',
                                               password='pass')
        self.other_user = User.objects.create_user(username='other',
                                                   password='pass')

        # Для задачи обязателен статус
        self.status = Status.objects.create(name='В работе')

        # Создаем тестовую задачу
        self.task = Task.objects.create(
            name='Тестовая задача',
            author=self.author,
            executor=self.author,
            status=self.status
        )
        self.list_url = reverse('tasks_list')
        self.create_url = reverse('task_create')
        self.delete_url = reverse('task_delete', kwargs={'pk': self.task.id})

    # Проверка доступа: только залогиненные видят список
    def test_tasks_list_access(self):
        # Аноним — редирект на логин
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)

        # Залогиненный — успех
        self.client.login(username='author', password='pass')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    # Проверка создания задачи
    def test_create_task(self):
        self.client.login(username='author', password='pass')
        data = {
            'name': 'Новая задача',
            'status': self.status.id,
            'executor': self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Task.objects.filter(name='Новая задача').exists())

    # Проверка удаления: только создатель
    def test_delete_task_by_author(self):
        self.client.login(username='author', password='pass')
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.list_url)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_by_non_author(self):
        # Логинимся под другим пользователем
        self.client.login(username='other', password='pass')
        response = self.client.post(self.delete_url)
        # Должен быть редирект, и задача остаться на месте
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())

        # Проверяем наличие flash-сообщения об ошибке
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("Задачу может удалить только ее автор"
                            in m.message for m in messages))

class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='password')
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


class LabelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='pass')
        self.label = Label.objects.create(name='Bug')
        self.client.login(username='testuser', password='pass')

    def test_label_crud(self):
        # Create
        response = self.client.post(
            reverse('label_create'), {'name': 'Feature'})
        self.assertTrue(Label.objects.filter(name='Feature').exists())
        # Delete protection
        task = Task.objects.create(name='T', status=self.status,
                                   author=self.user, executor=self.user)
        task.labels.add(self.label)
        response = self.client.post(reverse('label_delete',
                                            kwargs={'pk': self.label.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())

    def test_delete_label_linked_to_task(self):
        # Создаем задачу и привязываем метку
        task = Task.objects.create(name='T', author=self.user,
                                   status=self.status, executor=self.user)
        task.labels.add(self.label)

        # Пытаемся удалить метку
        response = self.client.post(reverse('label_delete',
                                            kwargs={'pk': self.label.id}))

        # Проверяем: метка все еще в базе, есть ошибка
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
        self.assertRedirects(response, reverse('labels_list'))

def test_filter_self_tasks(self):
    self.client.login(username='author', password='pass')
    # Задача, где я автор (создана в setUp)
    # Создаем задачу, где автор — другой юзер
    other_user = User.objects.create_user(username='other', password='pass')
    Task.objects.create(name='Other Task', author=other_user,
                        status=self.status)

    # Применяем фильтр "Только свои задачи"
    response = self.client.get(reverse('tasks_list'), {'self_tasks': 'on'})
    self.assertEqual(len(response.context['tasks']), 1)
    self.assertEqual(response.context['tasks'][0].name, 'Тестовая задача')

def test_filter_by_label(self):
    self.client.login(username='author', password='pass')
    response = self.client.get(reverse('tasks_list'),
                               {'labels': self.label.id})
    self.assertContains(response, self.task.name)
