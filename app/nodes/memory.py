from __future__ import annotations
from datetime import datetime
from app.state import AppState, Turn
from app.memory.db import log_activity

LABEL_MAP = {
    "status_update": "focus",
    "request_break": "personal",
    "idle_detected": "wasted",
}


def memory_node(state: AppState) -> AppState:
    intent = state.intent
    text = state.last_user_text or ""

    label = LABEL_MAP.get(intent, "focus")
    duration = 0

    log_activity(intent=intent, text=text, duration_min=duration, label=label)

    if intent == "status_update":
        state.last_update_ts = datetime.now()

    return state