APP_MODULE=src.main:app
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

show:
	poetry show --tree

lint:
	poetry run ruff check .

lint-fix:
	poetry run ruff check . --fix
