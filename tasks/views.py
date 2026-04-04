from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


def index(request):
    return render(request, "index.html")

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
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно создана"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно изменена"


class TaskDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks:list")
    success_message = "Задача успешно удалена"

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect("tasks:list")
