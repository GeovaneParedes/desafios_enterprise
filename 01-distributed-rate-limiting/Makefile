.PHONY: install format run test

install:
	pip install -r requirements.txt

format:
	# Usar 'python -m' é mais seguro que chamar o binário direto
	python3 -m isort .
	python3 -m black .

run:
	python3 -m uvicorn main:app --reload

test:
	python3 test_stress.py
