from django.contrib import admin
from django.urls import include, path

from tasks.views import index  # Главная страница теперь живет в tasks
from users.views import UserLoginView, UserLogoutView  # Импорт логина/логаута

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    # Подключаем маршруты каждого приложения
    path("users/", include("users.urls")),
    path("statuses/", include("statuses.urls")),
    path("labels/", include("labels.urls")),
    path("tasks/", include("tasks.urls")),
    # Маршруты аутентификации (обычно на верхнем уровне)
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
