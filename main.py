from __future__ import annotations
from app.graph import build_graph
from app.state import AppState
from app.llm.azure_openai import init_system_prompt, load_prompt
from app.config import settings
import os

PROMPTS_DIR = os.path.join("app", "prompts")


def main():
    system_txt = load_prompt(os.path.join(PROMPTS_DIR, "system_coach.txt"))
    init_system_prompt(system_txt)

    app = build_graph()
    state = AppState()

    print("\n=== Voice-First Strict Coach — Phase-1 (LangGraph + Azure OpenAI) ===\n")
    print("Tip: just type your response if voice is not configured. Ctrl+C to exit.\n")

    while True:
        state = app.invoke(state)


if __name__ == "__main__":
    main()