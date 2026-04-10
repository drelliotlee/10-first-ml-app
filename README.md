# 10-first-ml-app

A minimal ML pipeline that predicts whether it will rain tomorrow in NYC, built to practice MLOps scaffolding. The focus is pipeline structure and tooling, not ML complexity.

## Stack

- **API** — FastAPI + uvicorn
- **Model** — scikit-learn LogisticRegression
- **Data** — Open-Meteo historical weather API (NYC)
- **Database** — PostgreSQL (logs predictions)
- **Packaging** — uv
- **Containers** — Docker + Docker Compose

## Pipeline

```
make ingest → make preprocess → make train → make serve
```

| Stage | Script | Description |
|---|---|---|
| Ingest | `src/ingest.py` | Fetch NYC weather history from Open-Meteo, save to `data/raw/` |
| Preprocess | `src/preprocess.py` | Build feature matrix + labels, save to `data/processed/` |
| Train | `src/train.py` | Train binary classifier, save to `models/` |
| Serve | `src/api.py` | FastAPI inference endpoint + prediction logging |

## Quickstart

```bash
# 1. Set up environment
make setup  # copies .env.example → .env and runs uv sync

# 2. Run the pipeline
make ingest
make preprocess
make train

# 3. Start the API
make serve

# 4. Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature_2m_max": 25.0,
    "temperature_2m_min": 15.0,
    "windspeed_10m_max": 10.0,
    "relative_humidity_2m_max": 80.0
  }'
```

Or open `http://localhost:8000/docs` for the interactive Swagger UI.

## Commands

| Command | Description |
|---|---|
| `make setup` | Copy `.env.example` and install dependencies |
| `make ingest` | Fetch raw weather data |
| `make preprocess` | Build processed dataset |
| `make train` | Train model (runs in Docker) |
| `make serve` | Start API + database |
| `make test` | Run pytest locally |
| `make down` | Stop all containers |
| `make clean` | Stop containers and wipe volumes |
| `make logs` | Follow API logs |
| `make shell-api` | Shell into API container |
| `make shell-db` | psql into database |

## Project Structure

```
├── src/
│   ├── ingest.py       # Fetch raw data from Open-Meteo
│   ├── preprocess.py   # Build features and labels (shared by train + serve)
│   ├── train.py        # Training script
│   ├── api.py          # FastAPI endpoints
│   └── utils.py        # Shared helpers (model load/save)
├── tests/
│   ├── test_api.py
│   ├── test_ingest.py
│   └── test_preprocess.py
├── data/
│   ├── raw/            # Immutable — never modified after ingest
│   └── processed/      # Built from raw, safe to regenerate
├── models/             # Trained model artifact (gitignored)
├── Dockerfile.api
├── Dockerfile.train
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## Architecture

Three containers:

- `rain-api` — serves predictions on port 8000, reads model from `models/` volume
- `rain-db` — PostgreSQL, stores prediction logs
- `rain-train` — one-shot training container, writes model to `models/` volume (profile: train)

## Future Extensions

- **CI/CD** — GitHub Actions running integration tests (real HTTP calls, full stack) on every push
- **Data quality** — Great Expectations checkpoints between pipeline stages to catch bad data before training
- **Experiment tracking** — MLflow or Weights & Biases for logging metrics, parameters, and model versions per run
- **Model evaluation** — precision, recall, F1, confusion matrix; accuracy alone is misleading for imbalanced classes
- **Scheduled retraining** — Airflow or Prefect orchestrating the full pipeline on a cron schedule
- **Prediction monitoring** — daily prediction job stores outcomes in DB; ground truth ingested 1 day later; drift detection compares predictions vs actuals every 30 days and triggers retraining if accuracy degrades
