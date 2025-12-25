.PHONY: install up down test clean lint

install:
	pip install -r requirements.txt

up:
	docker compose up -d

down:
	docker compose down --volumes

test:
	PYTHONPATH=. pytest -v -s

lint:
	flake8 src/ tests/
	PYTHONPATH=. mypy src/
	black --check .
	isort --check-only .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
