from django.contrib.auth.models import User
from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Имя")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метка"

class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Имя")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               related_name='tasks', verbose_name="Статус")
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name='authored_tasks',
                               verbose_name="Автор")
    executor = models.ForeignKey(User, on_delete=models.PROTECT,
                                 related_name='executed_tasks',
                                 verbose_name="Исполнитель",
                                 null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(Label, blank=True, related_name='tasks',
                                    verbose_name='Метки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задача"
