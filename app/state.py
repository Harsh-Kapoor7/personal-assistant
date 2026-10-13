from __future__ import annotations
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

IntentType = Literal[
    "status_update", "plan_day", "request_break", "idle_detected",
    "smalltalk", "summary_request", "unknown"
]

class Turn(BaseModel):
    ts: datetime
    role: Literal["user", "assistant"]
    text: str

class AppState(BaseModel):
    # Conversation
    last_user_text: Optional[str] = None
    last_assistant_text: Optional[str] = None
    turns: List[Turn] = Field(default_factory=list)

    # Control
    intent: IntentType = "unknown"
    action: Optional[str] = None

    # Memory hooks
    write_activity: Optional[Dict[str, Any]] = None  # structured activity row
    coach_directive: Optional[str] = None

    # Timers
    last_update_ts: Optional[datetime] = None

    # Output speech
    say: Optional[str] = None