APP_MODULE=src.main:app
HOST=0.0.0.0
PORT=8000

.PHONY: help install run dev shell lint format test setup-hooks

help:
	@echo "Comandos disponibles:"
	@echo "  make install   -> Instala dependencias y configura Git Hooks"
	@echo "  make run       -> Corre FastAPI (prod)"
	@echo "  make dev       -> Corre FastAPI con reload"
	@echo "  make lint      -> Revisa el código con Ruff"
	@echo "  make format    -> Formatea el código con Ruff"

install:
	poetry install
	@make setup-hooks

setup-hooks:
	@echo "Configurando Git Hooks (Ruff + Commitizen)..."
	poetry run pre-commit install
	poetry run pre-commit install --hook-type commit-msg
	@echo "Hooks instalados correctamente!"

run:
	poetry run uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT)

dev:
	poetry run uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

format:
	poetry run ruff format .

lint:
	poetry run ruff check .

lint-fix:
	poetry run ruff check . --fix

show:
	poetry show --tree