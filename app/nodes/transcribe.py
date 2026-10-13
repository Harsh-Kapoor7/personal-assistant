from __future__ import annotations
from app.io.audio import listen_once
from app.state import AppState, Turn
from datetime import datetime

def transcribe_node(state: AppState) -> AppState:
    text = listen_once(prompt="You (speak or type):")
    state.last_user_text = text
    state.turns.append(Turn(ts=datetime.now(), role="user", text=text))
    return state