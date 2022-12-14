start:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

detect-ip-adress:
	ipconfig

init-migrations:
	alembic init app/migrations

makemigrations:
	alembic -c app/alembic.ini revision --autogenerate -m "$(name)"

migrate:
	alembic -c app/alembic.ini upgrade head

unmigrate:
	alembic -c app/alembic.ini downgrade -1

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt