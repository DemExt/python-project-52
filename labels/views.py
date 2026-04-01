from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Label

class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/index.html"
    context_object_name = "labels"

class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    fields = ["name"]
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels:index")
    success_message = "Метка успешно создана"

class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ["name"]
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels:index")
    success_message = "Метка успешно изменена"

class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels:index")
    success_message = "Метка успешно удалена"

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        # Проверяем, привязана ли метка к какой-либо задаче
        if label.tasks.exists(): 
            messages.error(request, "Невозможно удалить метку, потому что она используется")
            return redirect("labels:index")
        return super().post(request, *args, **kwargs)