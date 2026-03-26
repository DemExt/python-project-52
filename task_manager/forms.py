from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms
from .models import Status, Task, Label

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

class CustomUserCreationForm(UserCreationForm):
    # Явно добавляем поля, чтобы задать им правильные русские подписи
    first_name = forms.CharField(label="Имя", required=True, max_length=150)
    last_name = forms.CharField(label="Фамилия", required=True, max_length=150)

    # Переопределяем пароль для подсказки
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Пароль должен содержать не менее 3 символов."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password and len(password) < 3:
            raise ValidationError("Пароль должен содержать не менее 3 символов.")
        return password

class CustomUserChangeForm(UserChangeForm):
    password = None 
    
    first_name = forms.CharField(label="Имя", required=True, max_length=150)
    last_name = forms.CharField(label="Фамилия", required=True, max_length=150)

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        required=False, # Сделаем необязательным, если пароль не меняется
        help_text="Ваш пароль должен содержать не менее 3 символов."
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password and len(password) < 3:
            raise ValidationError("Пароль должен содержать не менее 3 символов.")
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password) # Хэшируем пароль, если он введен
        if commit:
            user.save()
        return user

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
        # Если тест требует точный текст ошибки при дубликате имени:
        error_messages = {
            'name': {
                'unique': "Задача с таким Имя уже существует",
            },
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].required = False
        self.fields['labels'].required = False
        self.fields['description'].required = False