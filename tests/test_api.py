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


# test_predict belongs in CI as an integration test — it requires a real DB
# connection (host=db) which only resolves inside Docker's network.
