VENV ?= .venv
PYTHON ?= python3
APP_MODULE ?= app:app
HOST ?= 0.0.0.0
PORT ?= 8000

.PHONY: setup dev run db-up db-down db-logs test clean

$(VENV)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	touch $(VENV)/bin/activate

setup: $(VENV)/bin/activate

dev:
	./scripts/dev.sh HOST=$(HOST) PORT=$(PORT) APP_MODULE=$(APP_MODULE)

run: setup
	$(VENV)/bin/uvicorn $(APP_MODULE) --reload --host $(HOST) --port $(PORT)

db-up:
	docker compose up -d db

db-down:
	docker compose down

db-logs:
	docker compose logs -f db

test: setup
	$(VENV)/bin/pytest

clean:
	rm -rf $(VENV)
