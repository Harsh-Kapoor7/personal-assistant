from __future__ import annotations
from typing import List, Dict, Any
from app.config import settings
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(
    deployment_name=settings.azure_deployment,
    api_key=settings.azure_api_key,
    api_version=settings.azure_api_version,
    azure_endpoint=settings.azure_endpoint,
)

SYSTEM_COACH = None

def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def init_system_prompt(prompt_text: str):
    global SYSTEM_COACH
    SYSTEM_COACH = prompt_text


def chat(messages: List[Dict[str, str]], temperature: float = 0.3, max_tokens: int = 400) -> str:
    if SYSTEM_COACH:
        messages = [{"role": "system", "content": SYSTEM_COACH}] + messages
    resp = llm.invoke(messages)
    return resp.strip()