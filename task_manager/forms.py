from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Label, Status, Task


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]


class CustomUserCreationForm(UserCreationForm):
    # Явно добавляем поля, чтобы задать им правильные русские подписи
    first_name = forms.CharField(label="Имя", required=True, max_length=150)
    last_name = forms.CharField(label="Фамилия", required=True, max_length=150)

    # Переопределяем пароль для подсказки
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Пароль должен содержать не менее 3 символов.",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password and len(password) < 3:
            raise ValidationError(
                "Пароль должен содержать не менее 3 символов."
            )
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Если пароль введен, он обязан совпадать с подтверждением
        if password1 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    password = None

    first_name = forms.CharField(label="Имя", required=True, max_length=150)
    last_name = forms.CharField(label="Фамилия", required=True, max_length=150)

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        required=False,  # Сделаем необязательным, если пароль не меняется
        help_text="Пароль должен содержать не менее 3 символов.",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password and len(password) < 3:
            raise ValidationError(
                "Пароль должен содержать не менее 3 символов."
            )
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Если пользователь начал вводить новый пароль, проверяем совпадение
        if password1 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)  # Хэшируем пароль, если он введен
        if commit:
            user.save()
        return user


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["name"]


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
