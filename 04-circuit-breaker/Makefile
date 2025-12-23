.PHONY: install format check run run-external clean

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

format:
	python3 -m isort .
	python3 -m black .

check:
	python3 -m isort . --check
	python3 -m black . --check

# Roda a API principal (Porta 8000)
run:
	python3 -m uvicorn main:app --reload --port 8000

# Roda o serviço externo "instável" (Porta 8001)
run-external:
	python3 external_service.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
