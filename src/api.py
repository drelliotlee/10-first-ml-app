import logging
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
model = joblib.load("models/model.pkl")


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

    logger.info(f"Prediction: {prediction}, features: {features}")

    return PredictionResponse(prediction=prediction, probability=probability)
