from django.db import models
from django.contrib.auth import get_user_model
from statuses.models import Status
from labels.models import Label

User = get_user_model()

class Task(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Имя")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="tasks", verbose_name="Статус")
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_tasks", verbose_name="Автор")
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasks", verbose_name="Исполнитель")
    labels = models.ManyToManyField(Label, related_name="tasks", blank=True, verbose_name="Метки")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name