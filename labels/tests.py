from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Label
from statuses.models import Status
from tasks.models import Task

class LabelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.status = Status.objects.create(name='New')
        self.label = Label.objects.create(name="Bug")
        self.client.login(username="testuser", password="pass")

    def test_label_crud(self):
        # Create
        response = self.client.post(reverse("labels:create"), {"name": "Feature"})
        self.assertTrue(Label.objects.filter(name="Feature").exists())

    def test_delete_label_linked_to_task(self):
        task = Task.objects.create(
            name="T", author=self.user, status=self.status, executor=self.user
        )
        task.labels.add(self.label)
        # Удаление защищено логикой во вьюхе
        response = self.client.post(reverse("labels:delete", kwargs={"pk": self.label.id}))
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
        self.assertRedirects(response, reverse("labels:index"))