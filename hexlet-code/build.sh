#!/usr/bin/env bash
# Установка uv
curl -LsSf https://astral.sh | sh
source $HOME/.local/bin/env

# Установка зависимостей и сборка
uv sync
python manage.py collectstatic --no-input
python manage.py migrate