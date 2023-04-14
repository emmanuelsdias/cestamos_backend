start:
	cd app && uvicorn main:app --reload --host 0.0.0.0 --port 8000

detect-ip-adress:
	ipconfig

init-migrations:
	cd app && alembic init ./migrations

makemigrations:
	cd app && alembic -c ./alembic.ini revision --autogenerate -m "$(name)"

migrate:
	cd app && alembic -c ./alembic.ini upgrade head

unmigrate:
	cd app && alembic -c ./alembic.ini downgrade -1

freeze:
	pip freeze > app/requirements.txt

install:
	pip install -r app/requirements.txt

publish:
	cd app && space push

.PHONY: lint-python
lint-python:
	black . --line-length 90