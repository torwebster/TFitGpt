from dataclasses import dataclass


@dataclass
class ReadinessResult:
    score: int
    reasons: list[str]


@dataclass
class TargetsResult:
    steps: int
    protein_g: int
    calories: int
    reasons: list[str]


@dataclass
class TrainingPlanResult:
    intensity: str
    session: str
    reasons: list[str]


def compute_readiness(context: dict) -> ReadinessResult:
    score = 70
    reasons = []
    if context.get("sleep_score", 70) < 50:
        score -= 20
        reasons.append("Low sleep score reduced readiness")
    if context.get("pain_severity", 0) >= 6:
        score -= 25
        reasons.append("High pain severity triggered conservative mode")
    if context.get("high_load_last_2_days", False):
        score -= 10
        reasons.append("Recent high load caused deload recommendation")
    return ReadinessResult(score=max(20, min(score, 95)), reasons=reasons)


def compute_targets(context: dict) -> TargetsResult:
    steps = max(4000, min(12000, context.get("steps_yesterday", 6000) + 500))
    protein = 140
    calories = 2200
    reasons = ["Baseline targets applied"]
    if context.get("protein_low_yesterday"):
        protein += 20
        reasons.append("Protein was low yesterday, bumped protein target")
    goal = context.get("goal", "maintenance")
    if goal == "fat_loss":
        calories = 2000
        reasons.append("Fat-loss goal set moderate deficit")
    elif goal == "muscle_gain":
        calories = 2400
        reasons.append("Muscle gain goal set slight surplus")
    return TargetsResult(steps=steps, protein_g=protein, calories=calories, reasons=reasons)


def compute_training_plan(context: dict) -> TrainingPlanResult:
    minutes = context.get("time_available", 45)
    intensity = "moderate"
    session = f"{minutes} min full-body strength"
    reasons = ["Default session chosen"]
    if context.get("pain_severity", 0) >= 6 or context.get("sleep_score", 70) < 50:
        intensity = "low"
        session = f"{minutes} min low-impact mobility + zone 2 walk"
        reasons.append("Recovery mode due to pain/sleep signals")
    if context.get("high_load_last_2_days"):
        intensity = "low"
        reasons.append("Deloaded after high recent load")
    return TrainingPlanResult(intensity=intensity, session=session, reasons=reasons)


def build_daily_plan(context: dict) -> dict:
    readiness = compute_readiness(context)
    targets = compute_targets(context)
    training = compute_training_plan(context)
    actions = [
        f"Training: {training.session}",
        f"Steps target: {targets.steps}",
        f"Protein target: {targets.protein_g}g",
        f"Calories target: {targets.calories}",
    ]
    return {
        "readiness": readiness.score,
        "actions": actions,
        "why": readiness.reasons + targets.reasons + training.reasons,
        "confidence": 0.85 if readiness.reasons else 0.7,
    }
