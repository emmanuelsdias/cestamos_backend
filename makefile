start:
	cd app && uvicorn main:app --reload --host 0.0.0.0 --port 8000

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
	pip freeze > app/requirements.txt

install:
	pip install -r app/requirements.txt

publish:
	space push