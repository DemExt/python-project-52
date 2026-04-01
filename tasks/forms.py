from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        widgets = {
            "labels": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
        # Если тест требует точный текст ошибки при дубликате имени:
        error_messages = {
            "name": {
                "unique": "Задача с таким Имя уже существует",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].label = "Исполнитель"
        self.fields["executor"].label_from_instance = lambda obj: (
            obj.get_full_name() or obj.username
        )
        self.fields["status"].label = "Статус"
        self.fields["labels"].label = "Метки"
        self.fields["executor"].required = False
        self.fields["labels"].required = False
        self.fields["description"].required = False