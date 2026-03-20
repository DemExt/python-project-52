from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    # Явно добавляем поля, чтобы задать им правильные русские подписи
    first_name = forms.CharField(label="Имя", required=True)
    last_name = forms.CharField(label="Фамилия", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        # Порядок полей в форме
        fields = ("first_name", "last_name", "username")