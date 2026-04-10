import logging
import os
import psycopg2
from contextlib import asynccontextmanager
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from src.utils import load_model
from src.preprocess import preprocess_input

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    logger.info("DB initialized")
    yield


app = FastAPI(lifespan=lifespan)
model = load_model()


def get_db_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=5432,
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        database=os.environ["POSTGRES_DB"],
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            features FLOAT8[],
            prediction INT,
            timestamp TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


class PredictionRequest(BaseModel):
    temperature_2m_max: float
    temperature_2m_min: float
    windspeed_10m_max: float
    relative_humidity_2m_max: float


class PredictionResponse(BaseModel):
    prediction: int
    probability: list


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    features = preprocess_input(req.model_dump())

    prediction = int(model.predict([features])[0])
    probability = model.predict_proba([features])[0].tolist()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO predictions (features, prediction, timestamp) VALUES (%s, %s, %s)",
        (features, prediction, datetime.now())
    )
    conn.commit()
    conn.close()

    logger.info(f"Prediction: {prediction}, features: {features}")

    return PredictionResponse(prediction=prediction, probability=probability)
