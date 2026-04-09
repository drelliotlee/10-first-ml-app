import logging
import psycopg2
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    logger.info("DB initialized")
    yield


app = FastAPI(lifespan=lifespan)
model = joblib.load("models/model.pkl")


def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="iris_db",
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
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class PredictionResponse(BaseModel):
    prediction: int
    probability: list


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    features = [
        req.sepal_length,
        req.sepal_width,
        req.petal_length,
        req.petal_width,
    ]

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
