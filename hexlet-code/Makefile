install:
		uv sync

build:
		./build.sh

dev:
		uv run python manage.py runserver

render-start:
		uv run gunicorn task_manager.wsgi:application --bind 0.0.0.0:10000