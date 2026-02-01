.PHONY: install up down run clean

install:
	pip install -r requirements.txt

up:
	docker compose up -d

down:
	docker compose down

run:
	PYTHONPATH=. python3 src/app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
