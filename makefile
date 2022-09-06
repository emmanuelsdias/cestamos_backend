start:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

detect-ip-adress:
	ipconfig

makemigrations:
	alembic -c alembic.ini revision --autogenerate -m "$(name)"

migrate:
	alembic upgrade head

unmigrate:
	alembic -c app/alembic.ini downgrade -1