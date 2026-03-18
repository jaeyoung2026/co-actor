"""LLM 호출 래퍼 — Gemini (기본) + OpenAI 지원."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

_env_loaded = False
DEFAULT_MODEL = "gemini-3-flash-preview"


def _ensure_env() -> None:
    global _env_loaded
    if _env_loaded:
        return

    _env_loaded = True
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def _is_gemini(model: str) -> bool:
    return model.startswith("gemini")


def call_llm(
    prompt: str,
    system: str = "",
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    timeout: int = 120,
) -> str:
    _ensure_env()

    if _is_gemini(model):
        return _call_gemini(prompt, system, model, temperature)
    else:
        return _call_openai(prompt, system, model, temperature, timeout)


def _call_gemini(
    prompt: str,
    system: str,
    model: str,
    temperature: float,
) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client()

    contents = []
    if system:
        contents.append(types.Content(
            role="user",
            parts=[types.Part(text=f"[System instruction]\n{system}\n[End system instruction]")],
        ))
        contents.append(types.Content(
            role="model",
            parts=[types.Part(text="understood")],
        ))
    contents.append(types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    ))

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=temperature,
        ),
    )
    return (response.text or "").strip()


def _call_openai(
    prompt: str,
    system: str,
    model: str,
    temperature: float,
    timeout: int,
) -> str:
    from openai import OpenAI

    client = OpenAI()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        timeout=timeout,
    )
    return (response.choices[0].message.content or "").strip()


def call_llm_json(prompt: str, system: str = "", model: str = DEFAULT_MODEL) -> dict:
    text = call_llm(prompt=prompt, system=system, model=model)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"JSON object response not found in: {text[:200]}")
    return json.loads(match.group())


def call_llm_json_array(prompt: str, system: str = "", model: str = DEFAULT_MODEL) -> list:
    text = call_llm(prompt=prompt, system=system, model=model)
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        raise ValueError(f"JSON array response not found in: {text[:200]}")
    return json.loads(match.group())
