import json
import logging
import csv
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RAW_DATA_PATH = Path("data/raw/weather.json")
PROCESSED_DATA_PATH = Path("data/processed/weather.csv")

FEATURES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "windspeed_10m_max",
    "relative_humidity_2m_max",
]


def preprocess_raw():
    with open(RAW_DATA_PATH) as f:
        data = json.load(f)

    daily = data["daily"]
    n = len(daily["time"])

    rows = []
    for i in range(n - 1):
        row = {feature: daily[feature][i] for feature in FEATURES}
        row["rained_tomorrow"] = int(daily["precipitation_sum"][i + 1] > 0)
        rows.append(row)

    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_DATA_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FEATURES + ["rained_tomorrow"])
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f"Processed {len(rows)} rows saved to {PROCESSED_DATA_PATH}")


def preprocess_input(data: dict) -> list:
    return [data[feature] for feature in FEATURES]


if __name__ == "__main__":
    preprocess_raw()
