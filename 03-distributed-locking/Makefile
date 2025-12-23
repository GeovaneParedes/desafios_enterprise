.PHONY: install format check run test clean

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

format:
	python3 -m isort .
	python3 -m black .

check:
	python3 -m isort . --check
	python3 -m black . --check

run:
	python3 -m uvicorn main:app --reload

# Vamos criar esse script no próximo passo
test:
	python3 test_concurrency.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
