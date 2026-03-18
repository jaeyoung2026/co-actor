"""lighthouse 정체성 소스 어댑터.

시드 DB의 self 타입 노드를 로드하여 매 턴 자동 포함한다.
이 소스는 검색/필터링 없이 항상 전체를 반환한다.
"""

from __future__ import annotations

import json
from pathlib import Path

SAMPLE_DIR = Path(__file__).parent / "sample_data"


class LighthouseIdentityAdapter:
    """identity 역할 소스 어댑터. 매 턴 자동 포함."""

    role = "identity"

    def __init__(self, mode: str = "sample"):
        self.mode = mode
        self._nodes: list[dict] = []

        if mode in ("sample", "live"):
            nodes_path = SAMPLE_DIR / "nodes_sample.json"
            if nodes_path.exists():
                with open(nodes_path, encoding="utf-8") as f:
                    all_nodes = json.load(f)
                # self 타입만 identity로 분류
                self._nodes = [n for n in all_nodes if n.get("type") == "self"]

    def get_identity(self) -> list[dict]:
        """정체성 노드를 ContextItem 형태로 반환한다. 항상 전체 반환."""
        results = []
        for node in self._nodes:
            results.append({
                "role": "identity",
                "content": node.get("content", ""),
                "provenance": {
                    "source": "lighthouse-seed",
                    "locator": f"node:{node.get('id', '')}",
                    "fetched_at": "seed",
                },
                "reason": f"정체성 ({node.get('context_hint', '')})",
                "metadata": {
                    "context_hint": node.get("context_hint"),
                    "encoding_depth": node.get("encoding_depth"),
                },
            })
        return results
