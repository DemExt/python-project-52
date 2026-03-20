from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import CustomUserCreationForm 

# Главная
def index(request):
    return render(request, 'index.html')

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = "Вы залогинены"

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)

class UserListView(ListView):
    model = User
    # Твой путь к файлу
    template_name = 'users_list.html' 
    context_object_name = 'users'

class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'create.html'
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован"

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'update.html'
    success_url = reverse_lazy('users_list')
    success_message = "Пользователь успешно изменен"

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения")
        return redirect('users_list')

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('users_list')
    success_message = "Пользователь успешно удален"

    def test_func(self):
        return self.get_object() == self.request.user