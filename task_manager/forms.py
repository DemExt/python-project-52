from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Status, Task, Label

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

class CustomUserCreationForm(UserCreationForm):
    # Явно добавляем поля, чтобы задать им правильные русские подписи
    first_name = forms.CharField(label="Имя", required=True)
    last_name = forms.CharField(label="Фамилия", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        # Порядок полей в форме
        fields = ("first_name", "last_name", "username")

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        # Django по умолчанию использует SelectMultiple для ManyToManyField, 
        # но мы можем явно это указать для уверенности:
        widgets = {
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['labels'].label = "Метки"