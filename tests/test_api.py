from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

SAMPLE_INPUT = {
    "temperature_2m_max": 25.0,
    "temperature_2m_min": 15.0,
    "windspeed_10m_max": 10.0,
    "relative_humidity_2m_max": 80.0,
}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_returns_valid_response():
    response = client.post("/predict", json=SAMPLE_INPUT)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert data["prediction"] in [0, 1]
    assert len(data["probability"]) == 2
