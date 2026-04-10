import json
import logging
from datetime import date, timedelta
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RAW_DATA_PATH = Path("data/raw/weather.json")

LATITUDE = 40.7128   # New York City
LONGITUDE = -74.0060

EXPECTED_FIELDS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "windspeed_10m_max",
    "relative_humidity_2m_max",
]


def _validate(data: dict):
    assert "daily" in data, "Missing 'daily' key in API response"
    daily = data["daily"]
    for field in EXPECTED_FIELDS:
        assert field in daily, f"Missing field: {field}"
    lengths = [len(daily[f]) for f in EXPECTED_FIELDS]
    assert len(set(lengths)) == 1, f"Field length mismatch: {lengths}"
    logger.info(f"Data validation passed: {lengths[0]} days, {len(EXPECTED_FIELDS)} fields")


def fetch_weather():
    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=365)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max",
            "relative_humidity_2m_max",
        ],
        "timezone": "America/New_York",
    }

    logger.info(f"Fetching weather data from {start_date} to {end_date}...")
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    _validate(data)

    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RAW_DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Raw data saved to {RAW_DATA_PATH}")


if __name__ == "__main__":
    fetch_weather()
