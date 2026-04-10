train:
	docker compose --profile train run --rm train

serve:
	docker compose up

build:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f api

test:
	uv run pytest -v
