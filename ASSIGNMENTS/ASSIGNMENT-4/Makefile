.PHONY: help install lint test coverage security run docker-build docker-up docker-down backup restore

help:
	@echo "Smart Campus Facility Platform - Automation Commands"
	@echo "  make install        Install project dependencies"
	@echo "  make lint           Run Ruff code quality check"
	@echo "  make test           Run all unit, integration, and regression tests"
	@echo "  make coverage       Execute test suite with coverage report generation"
	@echo "  make security       Execute Bandit and Pip-audit security checks"
	@echo "  make run            Start local development Uvicorn server"
	@echo "  make smoke          Execute deployment smoke test suite"
	@echo "  make backup         Create timestamped SQLite database snapshot"
	@echo "  make restore        Restore database and verify foreign key integrity"
	@echo "  make docker-build   Build production Docker container image"
	@echo "  make docker-up      Start container stack via Docker Compose"
	@echo "  make docker-down    Stop Docker Compose containers"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

lint:
	ruff check app tests

test:
	python -m pytest tests -v

coverage:
	python -m pytest tests -v --cov=app --cov-report=html:docs/evidence/coverage-report --cov-report=xml:docs/evidence/coverage.xml --cov-report=term --junitxml=docs/evidence/test-results.xml

security:
	bandit -r app -f json -o docs/evidence/security-scan.json
	pip-audit -r requirements.txt -f json -o docs/evidence/dependency-audit.json

run:
	uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

smoke:
	python scripts/smoke_test.py

backup:
	python scripts/backup.py

restore:
	python scripts/restore.py

docker-build:
	docker build -t campus-platform:latest .

docker-up:
	docker compose up -d

docker-down:
	docker compose down
