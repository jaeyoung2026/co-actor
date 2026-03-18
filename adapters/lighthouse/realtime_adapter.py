"""lighthouse 실시간 컨텍스트 어댑터 (대화 이력).

sample 모드: 내장 샘플 대화.
live 모드: 실제 대화 세션에서 로드 (향후 구현).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


SAMPLE_DIR = Path(__file__).parent / "sample_data"


class LighthouseRealtimeAdapter:
    """realtime 역할 소스 어댑터."""

    role = "realtime"

    def __init__(self, mode: str = "sample", preload: bool = False):
        self.mode = mode
        self._history: list[dict] = []
        # preload=True일 때만 샘플 대화를 미리 로드 (테스트용)
        # 기본은 빈 상태로 시작 — 새 세션
        if mode == "sample" and preload:
            with open(SAMPLE_DIR / "conversation_sample.json", encoding="utf-8") as f:
                self._history = json.load(f)

    def get_history(self, last_n: int = 6) -> list[dict]:
        """최근 대화 이력을 ContextItem 형태로 반환한다."""
        recent = self._history[-last_n:]
        results = []
        for i, msg in enumerate(recent):
            role_label = "사용자" if msg["role"] == "user" else "코르카"
            results.append({
                "role": "realtime",
                "content": f"{role_label}: {msg['content']}",
                "provenance": {
                    "source": "conversation-history",
                    "locator": f"turn:{len(self._history) - len(recent) + i}",
                    "fetched_at": "runtime",
                },
                "reason": "최근 대화 이력",
            })
        return results

    def add_turn(self, role: str, content: str):
        """대화 턴을 추가한다."""
        self._history.append({"role": role, "content": content})

    def get_summary(self) -> str:
        """대화 요약을 반환한다."""
        recent = self._history[-6:]
        return " | ".join(
            f"{'사용자' if m['role'] == 'user' else '코르카'}: {m['content'][:50]}"
            for m in recent
        )
