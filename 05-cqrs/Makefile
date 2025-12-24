.PHONY: install format run clean

install:
	pip install -r requirements.txt

format:
	python3 -m isort .
	python3 -m black .

run:
	python3 -m uvicorn main:app --reload --port 8000

clean:
	rm -f enterprise_store.db
	find . -type d -name "__pycache__" -exec rm -rf {} +
