.PHONY: install format lint run-api run-worker clean

install:
	pip install -r requirements.txt

format:
	python3 -m isort .
	python3 -m black .

# Roda a API (Produtor)
run-api:
	python3 -m uvicorn producer:app --reload --port 8000

# Roda o Worker (Consumidor)
run-worker:
	python3 worker.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
