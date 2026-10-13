from __future__ import annotations
from datetime import datetime, timedelta
from app.config import settings
from app.state import AppState


def coach_policy(state: AppState) -> str:
    now = datetime.now()
    last = state.last_update_ts or (now - timedelta(minutes=999))
    idle_min = (now - last).total_seconds() / 60.0

    if state.intent in {"idle_detected"} or idle_min >= settings.idle_soft_min:
        if idle_min < settings.idle_firm_min:
            return "soft_nudge"
        elif idle_min < settings.idle_enforce_min:
            return "firm_nudge"
        else:
            return "enforce_block"

    if state.intent == "status_update":
        return "ack_and_focus"

    if state.intent == "request_break":
        return "grant_short_break"

    if state.intent == "summary_request":
        return "end_of_day_summary"

    return "coach_reply"


def coach_node(state: AppState) -> AppState:
    directive = coach_policy(state)
    state.action = directive
    state.coach_directive = directive
    return state