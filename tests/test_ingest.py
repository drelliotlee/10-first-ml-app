import pytest
from src.ingest import _validate


VALID_DATA = {
    "daily": {
        "time": ["2024-01-01", "2024-01-02"],
        "temperature_2m_max": [10.0, 12.0],
        "temperature_2m_min": [5.0, 6.0],
        "precipitation_sum": [0.0, 2.5],
        "windspeed_10m_max": [15.0, 20.0],
        "relative_humidity_2m_max": [80.0, 75.0],
    }
}


def test_validate_passes_on_valid_data():
    _validate(VALID_DATA)


def test_validate_fails_when_daily_key_missing():
    with pytest.raises(AssertionError, match="Missing 'daily' key"):
        _validate({})


def test_validate_fails_when_field_missing():
    data = {"daily": {"time": ["2024-01-01"], "temperature_2m_max": [10.0]}}
    with pytest.raises(AssertionError, match="Missing field"):
        _validate(data)


def test_validate_fails_on_length_mismatch():
    data = {
        "daily": {
            "time": ["2024-01-01", "2024-01-02"],
            "temperature_2m_max": [10.0, 12.0],
            "temperature_2m_min": [5.0],
            "precipitation_sum": [0.0, 2.5],
            "windspeed_10m_max": [15.0, 20.0],
            "relative_humidity_2m_max": [80.0, 75.0],
        }
    }
    with pytest.raises(AssertionError, match="length mismatch"):
        _validate(data)
