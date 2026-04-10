# 10-first-ml-app

A minimal ML inference service built with FastAPI, scikit-learn, and PostgreSQL. The focus is MLOps scaffolding, not ML complexity.

## Stack

- **API** — FastAPI + uvicorn
- **Model** — scikit-learn LogisticRegression on the iris dataset
- **Database** — PostgreSQL (logs predictions)
- **Packaging** — uv
- **Containers** — Docker + Docker Compose

## Quickstart

```bash
# 1. Clone and set up environment
cp .env.example .env  # fill in values

# 2. Train the model
make train

# 3. Start the API and database
make serve

# 4. Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

Or open `http://localhost:8000/docs` for the interactive Swagger UI.

## Commands

| Command | Description |
|---|---|
| `make train` | Run training container, save model to `models/` |
| `make serve` | Start API + database |
| `make build` | Start with image rebuild |
| `make down` | Stop all containers |
| `make logs` | Follow API logs |
| `make test` | Run pytest |

## Project Structure

```
├── src/
│   ├── api.py        # FastAPI endpoints
│   ├── train.py      # Training script
│   └── utils.py      # Shared helpers
├── tests/
│   └── test_api.py   # API tests
├── models/           # Trained model (gitignored)
├── Dockerfile.api
├── Dockerfile.train
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## Architecture

Three containers:
- `iris-api` — serves predictions on port 8000, reads model from `models/` volume
- `iris-db` — PostgreSQL, stores prediction logs
- `iris-train` — runs training script, writes model to `models/` volume (profile: train)
