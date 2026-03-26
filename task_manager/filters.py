import django_filters
from django import forms
from django.contrib.auth.models import User

from .models import Label, Status, Task


class TaskFilter(django_filters.FilterSet):
    # Фильтр "Только свои задачи" (чекбокс)
    self_tasks = django_filters.BooleanFilter(
        widget=forms.CheckboxInput,
        method='filter_self_tasks',
        label='Только свои задачи'
    )

    # Стандартные фильтры с точными подписями
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус'
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель'
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка'
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
