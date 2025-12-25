.PHONY: install test run-server run-sender clean

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=. pytest -v -s

run-server:
	PYTHONPATH=. python3 src/receiver.py

run-sender:
	PYTHONPATH=. python3 src/sender.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
