from app.services.adaptive_engine.engine import compute_readiness, compute_targets, compute_training_plan, build_daily_plan


def test_readiness_reduces_with_sleep_and_pain():
    result = compute_readiness({"sleep_score": 40, "pain_severity": 7})
    assert result.score <= 30
    assert result.reasons


def test_targets_adjust_for_goal_and_protein():
    result = compute_targets({"goal": "fat_loss", "protein_low_yesterday": True, "steps_yesterday": 3000})
    assert result.calories == 2000
    assert result.protein_g == 160
    assert result.steps >= 4000


def test_training_deload_with_pain():
    result = compute_training_plan({"pain_severity": 8, "time_available": 30})
    assert result.intensity == "low"
    assert "mobility" in result.session


def test_build_daily_plan_shape():
    result = build_daily_plan({"goal": "muscle_gain"})
    assert "actions" in result
    assert isinstance(result["confidence"], float)
