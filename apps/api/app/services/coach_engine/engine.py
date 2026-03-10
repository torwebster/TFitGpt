import re


def classify_intent(message: str, attachments: list, context: dict) -> dict:
    text = message.lower()
    mapping = {
        "meal": ["ate", "meal", "protein", "calories"],
        "workout": ["workout", "bench", "squat", "run", "gym"],
        "symptom": ["pain", "injury", "sore"],
        "schedule": ["today", "schedule", "mins", "minutes", "can only"],
        "goal_update": ["goal", "fat loss", "muscle"],
        "support": ["motivation", "stressed", "help"],
    }
    for intent, keys in mapping.items():
        if any(k in text for k in keys):
            return {"intent": intent, "confidence": 0.8}
    return {"intent": "chat", "confidence": 0.6}


def extract_structured_updates(message: str, attachments: list, context: dict) -> dict:
    text = message.lower()
    updates = {"facts": [], "logs": []}
    pain_match = re.search(r"pain\s*:?\s*([a-zA-Z ]+)\s*(\d+)/10", text)
    if pain_match:
        updates["logs"].append({"type": "symptom", "location": pain_match.group(1).strip(), "severity": int(pain_match.group(2))})
    protein_match = re.search(r"(\d+)g", text)
    if "ate" in text and protein_match:
        updates["logs"].append({"type": "nutrition", "protein": int(protein_match.group(1))})
    if "30 mins" in text or "30 minutes" in text:
        updates["facts"].append({"type": "constraint", "time_available": 30})
    return updates


def build_coach_response(user_context: dict, conversation_context: dict, latest_input: dict) -> dict:
    intent = latest_input["intent"]
    reply = "Got it — logged and updated your context. "
    if intent == "symptom":
        reply += "Given pain signals, I recommend a low-impact session today."
    elif intent == "workout":
        reply += "Nice work. I can adapt tomorrow's load based on this session."
    elif intent == "meal":
        reply += "Great. I’ll tune protein/calorie targets based on this."
    else:
        reply += "Ask me anything about today’s plan or your progress."
    return {"message": reply, "confidence": 0.78, "rationale": f"Intent={intent}"}
