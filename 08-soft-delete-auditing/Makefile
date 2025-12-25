.PHONY: install test lint clean up down format

install:
	pip install -r requirements.txt

up:
	docker compose up -d

down:
	docker compose down

test:
	pytest

# Adicionei o comando format para rodar black e isort juntos
format:
	black .
	isort .

lint:
	flake8 src/ tests/
	mypy src/
	black --check .
	isort --check-only .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
