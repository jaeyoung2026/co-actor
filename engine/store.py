from __future__ import annotations

from pathlib import Path

from .models import ConversationState


STORE_DIR = Path("~/.par-loop/states/").expanduser()
STORE_DIR.mkdir(parents=True, exist_ok=True)


def _state_path(conversation_id: str) -> Path:
    return STORE_DIR / f"{conversation_id}.json"


def load_state(conversation_id: str) -> ConversationState:
    path = _state_path(conversation_id)
    if not path.exists():
        return ConversationState(conversation_id=conversation_id)
    return ConversationState.model_validate_json(path.read_text(encoding="utf-8"))


def save_state(state: ConversationState) -> None:
    path = _state_path(state.conversation_id)
    path.write_text(
        state.model_dump_json(indent=2),
        encoding="utf-8",
    )


def delete_state(conversation_id: str) -> None:
    path = _state_path(conversation_id)
    if path.exists():
        path.unlink()
