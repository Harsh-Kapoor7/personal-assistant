from __future__ import annotations
from datetime import datetime
from app.state import AppState, Turn
from app.io.audio import tts_say
from app.llm.azure_openai import chat

CHECKIN_PROMPT = (
    "In one sentence, what are you working on this hour? If none, pick one concrete task now "
    "and give start and expected end times."
)


def speak_node(state: AppState) -> AppState:
    directive = state.coach_directive or "coach_reply"

    if directive == "soft_nudge":
        out = "You've been idle. Let's resume a 25‑minute focus block. What will you work on now?"
    elif directive == "firm_nudge":
        out = "30 minutes idle. Starting a 25‑minute Pomodoro. State your task now."
    elif directive == "enforce_block":
        out = "Commit now: 25‑minute enforced focus starts. Say 'override' only with a reason. What's the task?"
    elif directive == "ack_and_focus":
        out = "Got it. Locking a focus window. Stay with it for 25 minutes."
    elif directive == "grant_short_break":
        out = "Take a short 5‑minute break. Then we resume."
    elif directive == "end_of_day_summary":
        # For brevity in Phase-1, a lightweight response. Phase-2 will aggregate DB.
        out = "Today: tracked focus blocks and updates. We'll add detailed summaries next phase."
    else:
        # Default coach reply / check-in
        messages = [{"role": "user", "content": CHECKIN_PROMPT}]
        out = chat(messages, temperature=0.2, max_tokens=120)

    state.say = out
    state.turns.append(Turn(ts=datetime.now(), role="assistant", text=out))
    tts_say(out)
    state.last_assistant_text = out
    return state