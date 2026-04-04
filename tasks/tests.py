from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status

from .models import Task


class TasksTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(
            username="author", password="pass")
        self.other_user = User.objects.create_user(
            username="other", password="pass")
        self.status = Status.objects.create(name="В работе")
        self.label = Label.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Тестовая задача",
            author=self.author,
            executor=self.author,
            status=self.status,
        )
        self.task.labels.add(self.label)

        self.list_url = reverse("tasks:list")
        self.create_url = reverse("tasks:create")
        self.delete_url = reverse("tasks:delete", kwargs={"pk": self.task.id})

    def test_tasks_list_access(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username="author", password="pass")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        self.client.login(username="author", password="pass")
        data = {
            "name": "Новая", "status": self.status.id,
            "executor": self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertRedirects(response, self.list_url)
        self.assertTrue(Task.objects.filter(name="Новая").exists())

    def test_delete_task_by_author(self):
        self.client.login(username="author", password="pass")
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.list_url)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_filter_by_label(self):
        self.client.login(username="author", password="pass")
        response = self.client.get(self.list_url, {"labels": self.label.id})
        self.assertContains(response, self.task.name)
