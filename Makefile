.PHONY: setup test ingest preprocess train serve down clean logs restart ps shell-api shell-db

# ── Local (no containers required) ───────────────────────────────────────────

setup:
	cp .env.example .env
	uv sync

test:
	uv run pytest -v

# ── Pipeline (one-shot, run in order: ingest → preprocess → train) ───────────
# ingest and preprocess run locally; train runs in Docker for reproducibility

ingest:
	uv run python -m src.ingest

preprocess:
	uv run python -m src.preprocess

train:
	docker compose --profile train run --rm train

# ── Serve (long-running containers) ──────────────────────────────────────────

serve:
	docker compose up --build

down:
	docker compose down

clean:
	docker compose down -v

# ── Debugging (requires containers to be up via make serve) ───────────────────

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
