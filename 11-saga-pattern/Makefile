.PHONY: install test run clean

install:
	pip install -r requirements.txt

format:
	isort src tests
	black src tests
	
test:
	PYTHONPATH=. pytest -v -s

run:
	PYTHONPATH=. python3 src/main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
