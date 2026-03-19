"""내장 기억 어댑터 — JSON 파일 기반의 간단한 기억 시스템."""

from __future__ import annotations

import json
from pathlib import Path


class BuiltinMemoryAdapter:
    """JSON 파일에서 기억 노드를 로드하고, 키워드 매칭으로 활성화한다.

    시드 데이터 파일(nodes.json)이 없으면 빈 기억으로 시작한다.
    대화 중 add_memory()로 기억을 추가할 수 있다.
    """

    role = "memory"

    def __init__(self, nodes_path: str | None = None, mode: str = "sample"):
        self.nodes: list[dict] = []
        if nodes_path and Path(nodes_path).exists():
            with open(nodes_path, encoding="utf-8") as f:
                self.nodes = json.load(f)

    def query(self, query: str, top_k: int = 5) -> list[dict]:
        if not self.nodes or len(query) < 3:
            return []

        keywords = query.lower().split()
        scored = []
        for node in self.nodes:
            content = node.get("content", "").lower()
            score = sum(1 for kw in keywords if kw in content)
            if score > 0:
                scored.append((score, node))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [
            {
                "role": "memory",
                "content": node.get("content", ""),
                "provenance": {
                    "source": "builtin-memory",
                    "locator": f"node:{node.get('id', i)}",
                    "fetched_at": "runtime",
                },
                "confidence": min(score / max(len(keywords), 1), 1.0),
                "reason": f"키워드 매칭 (score={score})",
            }
            for i, (score, node) in enumerate(scored[:top_k])
        ]

    def add_memory(self, content: str, memory_type: str = "fact") -> None:
        """대화 중 새 기억을 추가한다."""
        self.nodes.append({
            "id": f"runtime-{len(self.nodes)}",
            "type": memory_type,
            "content": content,
        })
