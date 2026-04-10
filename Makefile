.PHONY: setup test ingest preprocess train serve down clean logs restart ps shell-api shell-db

# ── Local (no containers required) ───────────────────────────────────────────

setup:
	cp .env.example .env
	uv sync

# ── One-shot containers (spin up, run, exit) ──────────────────────────────────
# Pipeline steps run in order: ingest → preprocess → train
# test spins up its own isolated container with dev deps included

test:
	docker compose --profile test run --rm test

ingest:
	uv run python -m src.ingest

preprocess:
	uv run python -m src.preprocess

train:
	docker compose --profile train run --rm train

# ── Serve (long-running containers) ──────────────────────────────────────────

ingest:
	uv run python -m src.ingest

preprocess:
	uv run python -m src.preprocess

train:
	docker compose --profile train run --rm train

# ── Serve (long-running containers) ──────────────────────────────────────────
# Use build the first time or after code changes. Use serve after that.

serve:
	docker compose up --build

down:
	docker compose down

clean:
	docker compose down -v

# ── Debugging (requires containers to be up via make serve or make build) ─────

logs:
	docker compose logs -f api

restart:
	docker compose restart api

ps:
	docker compose ps

shell-api:
	docker exec -it rain-api bash

shell-db:
	docker exec -it rain-db psql -U postgres -d rain_db
