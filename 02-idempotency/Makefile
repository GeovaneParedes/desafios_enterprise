.PHONY: install format check run test clean

# Instalação de dependências
install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

# Formatação automática (modifica os arquivos)
format:
	python3 -m isort .
	python3 -m black .

# Apenas verifica a formatação (bom para CI/CD, não altera nada)
check:
	python3 -m isort . --check
	python3 -m black . --check

# Roda a API localmente
run:
	python3 -m uvicorn main:app --reload

# Executa o script de teste de idempotência
test:
	python3 test_idempotency.py

# Limpeza de arquivos temporários (__pycache__, etc)
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
