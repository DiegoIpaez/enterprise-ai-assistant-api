APP_MODULE=app.main:app
HOST=0.0.0.0
PORT=8000

.PHONY: help install run dev shell lint format test

help:
	@echo "Comandos disponibles:"
	@echo "  make install   -> Instala dependencias"
	@echo "  make run       -> Corre FastAPI (prod)"
	@echo "  make dev       -> Corre FastAPI con reload"
	@echo "  make shell     -> Activa el entorno poetry"
	@echo "  make test      -> Ejecuta tests"
	@echo "  make format    -> Formatea el código"

install:
	poetry install

run:
	poetry run uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT)

dev:
	poetry run uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

shell:
	poetry shell

test:
	poetry run pytest

format:
	poetry run black .
