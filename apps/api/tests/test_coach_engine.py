from app.services.coach_engine.engine import classify_intent, extract_structured_updates


def test_intent_symptom():
    out = classify_intent("pain: achilles 6/10", [], {})
    assert out["intent"] == "symptom"


def test_extract_symptom_and_time_constraint():
    out = extract_structured_updates("pain: achilles 6/10 and I can only do 30 mins", [], {})
    assert out["logs"][0]["severity"] == 6
    assert out["facts"][0]["time_available"] == 30
