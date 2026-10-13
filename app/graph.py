from __future__ import annotations
from langgraph.graph import StateGraph
from app.state import AppState
from app.nodes.transcribe import transcribe_node
from app.nodes.intent import intent_node
from app.nodes.coach import coach_node
from app.nodes.memory import memory_node
from app.nodes.speak import speak_node


def build_graph():
    g = StateGraph(AppState)

    g.add_node("transcribe", transcribe_node)
    g.add_node("intent", intent_node)
    g.add_node("coach", coach_node)
    g.add_node("memory", memory_node)
    g.add_node("speak", speak_node)

    g.set_entry_point("transcribe")

    g.add_edge("transcribe", "intent")
    g.add_edge("intent", "coach")
    g.add_edge("coach", "memory")
    g.add_edge("memory", "speak")
    g.add_edge("speak", "transcribe")  # keep the loop running

    app = g.compile()
    return app