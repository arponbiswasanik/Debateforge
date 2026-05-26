.PHONY: install install-dev test lint format clean run

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest tests/ -v --cov=debateforge --cov-report=term-missing

lint:
	flake8 debateforge/
	mypy debateforge/

format:
	black debateforge/
	isort debateforge/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

run:
	uvicorn debateforge.api:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	streamlit run frontend/app.py

	