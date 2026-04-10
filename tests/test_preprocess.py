from src.preprocess import preprocess_input, FEATURES


def test_preprocess_input_returns_correct_order():
    data = {
        "temperature_2m_max": 25.0,
        "temperature_2m_min": 15.0,
        "windspeed_10m_max": 10.0,
        "relative_humidity_2m_max": 80.0,
    }
    result = preprocess_input(data)
    assert result == [data[f] for f in FEATURES]


def test_preprocess_input_length_matches_features():
    data = {f: 1.0 for f in FEATURES}
    result = preprocess_input(data)
    assert len(result) == len(FEATURES)


def test_preprocess_input_missing_feature_raises():
    data = {f: 1.0 for f in FEATURES}
    del data[FEATURES[0]]
    try:
        preprocess_input(data)
        assert False, "Expected KeyError"
    except KeyError:
        pass
