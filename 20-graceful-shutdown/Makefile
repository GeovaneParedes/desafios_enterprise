.PHONY: install run clean

install:
	pip install -r requirements.txt

run:
	PYTHONPATH=. python3 src/worker.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
