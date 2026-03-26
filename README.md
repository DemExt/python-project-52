# Hexlet Check - Task Manager

### Ссылка на проект:
https://hexlet-code-b5jd.onrender.com

[![hexlet-check](https://github.com/DemExt/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DemExt/python-project-52/actions/workflows/hexlet-check.yml)

[![SonarQube Cloud](https://sonarcloud.io/images/project_badges/sonarcloud-light.svg)](https://sonarcloud.io/summary/new_code?id=DemExt_python-project-52)

---

## Описание
Это полноценное веб-приложение для управления задачами, написанное на **Django**. Оно позволяет регистрировать пользователей, создавать статусы, метки и задачи, а также фильтровать их по различным параметрам.

### Основные возможности:
*   **Управление пользователями**: Регистрация, аутентификация и редактирование профилей.
*   **Задачи**: Создание, редактирование и удаление задач с указанием исполнителя и статуса.
*   **Статусы и Метки**: Гибкая настройка этапов выполнения и категоризация задач.
*   **Фильтрация**: Поиск задач по статусу, исполнителю, меткам и фильтр "Только свои задачи".
*   **Безопасность**: Доступ к данным только для авторизованных пользователей, защита от удаления связанных данных.
*   **Мониторинг**: Интеграция с сервисом **Rollbar** для отслеживания ошибок в реальном времени.

## Технологии
*   **Python 3.14+**
*   **Django 6.0**
*   **Bootstrap 5** (через django-bootstrap5)
*   **django-filter** (для поиска)
*   **uv / Poetry** (управление зависимостями)
*   **Ruff** (линтер и форматирование кода)
*   **Rollbar** (логирование ошибок)

---

## Установка и запуск

### Предварительные требования
Убедитесь, что у вас установлен [uv](https://github.com) (современная замена pip/poetry).

### 1. Клонирование репозитория

git clone https://github.com/DemExt/python-project-52.git
cd python-project-52

### 2. Установка зависимостей

uv sync

### 3. Настройка переменных окружения

Создайте файл .env в корне и добавьте (опционально для локального запуска):

SECRET_KEY=ваш_секретный_ключ
DATABASE_URL=sqlite:///db.sqlite3
ROLLBAR_ACCESS_TOKEN=ваш_токен

### 4. Выполнение миграций и запуск

uv run python manage.py migrate
uv run python manage.py runserver

Приложение будет доступно по адресу: http://127.0.0.1:8000