.PHONY: install run-app run-kube clean

install:
	pip install -r requirements.txt

run-app:
	PYTHONPATH=. python3 src/app.py

run-kube:
	PYTHONPATH=. python3 src/kube_simulator.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
