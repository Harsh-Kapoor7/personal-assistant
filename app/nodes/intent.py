from __future__ import annotations
from typing import Dict
from app.state import AppState
from app.llm.azure_openai import chat

INTENT_SYSTEM = (
    "You classify the user's last utterance into one of: "
    "status_update, plan_day, request_break, idle_detected, smalltalk, summary_request, unknown."
)


def intent_node(state: AppState) -> AppState:
    user = state.last_user_text or ""
    if not user:
        state.intent = "unknown"
        return state

    messages = [
        {"role": "system", "content": INTENT_SYSTEM},
        {"role": "user", "content": user},
    ]
    intent = chat(messages, temperature=0.0, max_tokens=16)
    intent = intent.strip().split()[0].lower()
    allowed = {
        "status_update", "plan_day", "request_break", "idle_detected",
        "smalltalk", "summary_request", "unknown"
    }
    state.intent = intent if intent in allowed else "unknown"
    return state