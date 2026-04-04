from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import ProtectedError

from .forms import CustomUserCreationForm, CustomUserChangeForm

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "users/login.html"
    success_message = "Вы залогинены"

class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)

class UserListView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"

class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = "Пользователь успешно зарегистрирован"

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:index")
    success_message = "Пользователь успешно изменен"

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения другого пользователя.")
        return redirect("users:index")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:index")
    success_message = "Пользователь успешно удален"

    def test_func(self):
        return self.get_object() == self.request.user

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Невозможно удалить пользователя, потому что он используется")
            return redirect("users:index")