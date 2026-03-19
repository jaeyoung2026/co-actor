"""내장 실시간 어댑터 — 인메모리 대화 이력."""

from __future__ import annotations


class BuiltinRealtimeAdapter:
    """대화 이력을 메모리에 유지한다. 외부 DB 불필요."""

    role = "realtime"

    def __init__(self, agent_name: str = "에이전트", mode: str = "sample"):
        self.agent_name = agent_name
        self.history: list[dict] = []

    def get_history(self, last_n: int = 6) -> list[dict]:
        recent = self.history[-last_n:] if self.history else []
        return [
            {
                "role": "realtime",
                "content": f"{'사용자' if turn['role'] == 'user' else self.agent_name}: {turn['content']}",
                "provenance": {
                    "source": "conversation-history",
                    "locator": f"turn:{i}",
                    "fetched_at": "runtime",
                },
                "reason": "최근 대화 이력",
            }
            for i, turn in enumerate(recent)
        ]

    def add_turn(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})

    def get_summary(self) -> str:
        recent = self.history[-6:]
        return " | ".join(
            f"{'사용자' if t['role'] == 'user' else self.agent_name}: {t['content'][:50]}"
            for t in recent
        )
