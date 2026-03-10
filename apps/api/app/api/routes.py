from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.db.base import Base
from app.db.session import engine
from app.models.models import (
    User, Profile, DailyMetrics, Plan, MessageIngest, ConversationThread, CoachMessage,
    SymptomLog, NutritionLog, ContextEvent, MemoryItem
)
from app.schemas.schemas import ProfileCreate, MessageInput, TodayPlanRequest
from app.services.adaptive_engine.engine import build_daily_plan
from app.services.coach_engine.engine import classify_intent, extract_structured_updates, build_coach_response

router = APIRouter()

Base.metadata.create_all(bind=engine)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/auth/google/callback")
def auth_google(email: str, name: str | None = None, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        user = User(email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
    return {"user_id": user.id, "email": user.email}


@router.post("/profile/{user_id}")
def upsert_profile(user_id: int, payload: ProfileCreate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    profile = db.scalar(select(Profile).where(Profile.user_id == user_id))
    if not profile:
        profile = Profile(user_id=user_id)
        db.add(profile)
    profile.goals = payload.goals
    profile.injuries = payload.injuries
    profile.equipment = payload.equipment
    profile.schedule = payload.schedule
    profile.preferences = payload.preferences
    db.commit()
    return {"ok": True}


@router.post("/today-plan")
def today_plan(req: TodayPlanRequest, db: Session = Depends(get_db)):
    profile = db.scalar(select(Profile).where(Profile.user_id == req.user_id))
    if not profile:
        raise HTTPException(status_code=400, detail="Complete onboarding first")
    symptom = db.scalar(select(SymptomLog).where(SymptomLog.user_id == req.user_id).order_by(SymptomLog.timestamp.desc()))
    context = {
        "goal": profile.goals[0] if profile.goals else "maintenance",
        "sleep_score": 65,
        "steps_yesterday": 6000,
        "pain_severity": symptom.severity if symptom else 0,
        "time_available": profile.schedule.get("today_minutes", 45),
        "protein_low_yesterday": True,
        "high_load_last_2_days": False,
    }
    plan_data = build_daily_plan(context)
    plan = Plan(user_id=req.user_id, day=date.today(), plan_json=plan_data, rationale=plan_data["why"], confidence=plan_data["confidence"])
    db.add(plan)
    db.commit()
    return plan_data


@router.post("/coach/message")
def coach_message(payload: MessageInput, db: Session = Depends(get_db)):
    intent = classify_intent(payload.text, payload.attachments, {})
    updates = extract_structured_updates(payload.text, payload.attachments, {})

    ingest = MessageIngest(
        user_id=payload.user_id,
        raw_text=payload.text,
        provider=payload.channel,
        provider_message_id="",
        parsed_status="parsed",
        intent=intent["intent"],
        extracted_facts=updates,
    )
    db.add(ingest)

    if intent["intent"] == "symptom":
        for log in updates.get("logs", []):
            if log.get("type") == "symptom":
                db.add(SymptomLog(user_id=payload.user_id, pain_location=log.get("location"), severity=log.get("severity", 0), notes=payload.text))

    for fact in updates.get("facts", []):
        db.add(ContextEvent(user_id=payload.user_id, event_type=fact.get("type", "fact"), payload=fact))
        db.add(MemoryItem(user_id=payload.user_id, type="long_term", content=fact, importance=2, source="message"))

    thread = db.scalar(select(ConversationThread).where(ConversationThread.user_id == payload.user_id, ConversationThread.channel == payload.channel))
    if not thread:
        thread = ConversationThread(user_id=payload.user_id, channel=payload.channel)
        db.add(thread)
        db.flush()

    response = build_coach_response({}, {}, {"intent": intent["intent"]})
    db.add(CoachMessage(thread_id=thread.id, role="user", content=payload.text, channel=payload.channel, attachments={"items": payload.attachments}))
    db.add(CoachMessage(thread_id=thread.id, role="assistant", content=response["message"], channel=payload.channel, response_metadata=response))
    db.commit()

    return {"intent": intent, "updates": updates, "response": response}


@router.post("/webhooks/slack")
def slack_event(event: dict, db: Session = Depends(get_db)):
    if event.get("bot_id") or (event.get("text") or "").startswith("TFit:"):
        return {"ignored": True}
    msg_id = event.get("client_msg_id", "")
    existing = db.scalar(select(MessageIngest).where(MessageIngest.provider == "slack", MessageIngest.provider_message_id == msg_id))
    if existing:
        return {"deduped": True}
    db.add(MessageIngest(user_id=event.get("user_id", 1), raw_text=event.get("text", ""), provider="slack", provider_message_id=msg_id, parsed_status="new", intent="chat", extracted_facts={}))
    db.commit()
    return {"ok": True}


@router.post("/webhooks/discord")
def discord_event(event: dict, db: Session = Depends(get_db)):
    if event.get("author", {}).get("bot"):
        return {"ignored": True}
    msg_id = str(event.get("id", ""))
    existing = db.scalar(select(MessageIngest).where(MessageIngest.provider == "discord", MessageIngest.provider_message_id == msg_id))
    if existing:
        return {"deduped": True}
    db.add(MessageIngest(user_id=event.get("user_id", 1), raw_text=event.get("content", ""), provider="discord", provider_message_id=msg_id, parsed_status="new", intent="chat", extracted_facts={}))
    db.commit()
    return {"ok": True}
