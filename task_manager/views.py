from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    StatusForm,
    TaskForm,
)
from .models import Label, Status, Task


# Главная
def index(request):
    return render(request, "index.html")


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    success_message = "Вы залогинены"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)


class UserListView(ListView):
    model = User
    template_name = "users_list.html"
    context_object_name = "users"


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = "create.html"
    success_url = reverse_lazy("login")
    success_message = "Пользователь успешно зарегистрирован"


class UserUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = CustomUserChangeForm
    template_name = "update.html"
    success_url = reverse_lazy("users_list")
    success_message = "Пользователь успешно изменен"

    def test_func(self):
        return self.get_object() == self.request.user

    def form_valid(self, form):
        # Сохраняем форму (и новый пароль)
        response = super().form_valid(form)
        # Обновляем хеш сессии, чтобы юзера не выкинуло из системы
        update_session_auth_hash(self.request, form.instance)
        return response

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для изменения")
        return redirect("users_list")


class UserDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = User
    template_name = "delete.html"
    success_url = reverse_lazy("users_list")
    success_message = "Пользователь успешно удален"

    def test_func(self):
        return self.get_object() == self.request.user

    # чтобы при попытке удалить чужой профиль был редирект с ошибкой:
    def handle_no_permission(self):
        messages.error(
            self.request, "У вас нет прав для изменения другого пользователя."
        )
        return redirect("users_list")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                "Невозможно удалить пользователя, потому что он используется",
            )
            return redirect("users_list")


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses_list")
    success_message = "Статус успешно создан"


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses_list")
    success_message = "Статус успешно изменен"


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses_list")
    success_message = "Статус успешно удален"

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Невозможно удалить статус")
            return redirect("statuses_list")


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/show.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks_list")
    success_message = "Задача успешно создана"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks_list")
    success_message = "Задача успешно изменена"


class TaskDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks_list")
    success_message = "Задача успешно удалена"

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect("tasks_list")


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    fields = ["name"]
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels_list")
    success_message = "Метка успешно создана"


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ["name"]
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels_list")
    success_message = "Метка успешно изменена"


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels_list")
    success_message = "Метка успешно удалена"

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasks.exists():  # Проверка связи "многие ко многим"
            messages.error(request, "Невозможно удалить метку")
            return redirect("labels_list")
        return super().post(request, *args, **kwargs)
