from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_vertical_slice_flow():
    auth = client.post("/auth/google/callback", params={"email": "a@b.com", "name": "A"}).json()
    user_id = auth["user_id"]
    profile = client.post(f"/profile/{user_id}", json={
        "goals": ["fat_loss"],
        "injuries": ["achilles"],
        "equipment": ["dumbbells"],
        "schedule": {"today_minutes": 30},
        "preferences": {"style": "concise"}
    })
    assert profile.status_code == 200
    today = client.post("/today-plan", json={"user_id": user_id})
    assert today.status_code == 200
    msg = client.post("/coach/message", json={"user_id": user_id, "text": "pain: achilles 6/10", "attachments": [], "channel": "web"})
    assert msg.status_code == 200
    assert msg.json()["intent"]["intent"] == "symptom"
