from pydantic import BaseModel, Field
from typing import Any


class ProfileCreate(BaseModel):
    goals: list[str] = Field(default_factory=list)
    injuries: list[str] = Field(default_factory=list)
    equipment: list[str] = Field(default_factory=list)
    schedule: dict[str, Any] = Field(default_factory=dict)
    preferences: dict[str, Any] = Field(default_factory=dict)


class MessageInput(BaseModel):
    user_id: int
    text: str
    attachments: list[dict[str, Any]] = Field(default_factory=list)
    channel: str = "web"


class TodayPlanRequest(BaseModel):
    user_id: int
