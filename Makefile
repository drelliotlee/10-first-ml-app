setup:
	cp .env.example .env
	uv sync

train:
	docker compose --profile train run --rm train

serve:
	docker compose up

build:
	docker compose up --build

down:
	docker compose down

clean:
	docker compose down -v

logs:
	docker compose logs -f api

restart:
	docker compose restart api

ps:
	docker compose ps

test:
	uv run pytest -v

shell-api:
	docker exec -it rain-api bash

shell-db:
	docker exec -it rain-db psql -U postgres -d rain_db
