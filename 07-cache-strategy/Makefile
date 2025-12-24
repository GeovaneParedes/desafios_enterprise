.PHONY: install test lint format run clean

install:
	pip install -r requirements.txt

format:
	python3 -m isort .
	python3 -m black .

lint:
	# Verifica conformidade sem alterar arquivos
	flake8 src/ tests/ --max-line-length=79
	# A flag --explicit-package-bases ajuda o mypy a entender o 'src'
	PYTHONPATH=. mypy src/ --explicit-package-bases --ignore-missing-imports

test:
	# Roda testes unitários e de integração com cobertura
	PYTHONPATH=. pytest -v --cov=src tests/

run:
	python src/main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
