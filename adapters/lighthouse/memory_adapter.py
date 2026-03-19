"""lighthouse 기억 시스템 어댑터.

sample 모드: adapters/lighthouse/sample_data/nodes_sample.json에서 로드.
live 모드: 외부 기억 시스템의 nodes.json + activate.py 연동.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


SAMPLE_DIR = Path(__file__).parent / "sample_data"


class LighthouseMemoryAdapter:
    """memory 역할 소스 어댑터."""

    role = "memory"

    def __init__(self, mode: str = "sample", live_nodes_path: Optional[str] = None):
        self.mode = mode
        if mode == "sample":
            with open(SAMPLE_DIR / "nodes_sample.json", encoding="utf-8") as f:
                all_nodes = json.load(f)
            # self 타입은 identity adapter가 담당. 여기서는 fact만.
            self.nodes = [n for n in all_nodes if n.get("type") != "self"]
        elif mode == "live" and live_nodes_path:
            with open(live_nodes_path, encoding="utf-8") as f:
                self.nodes = json.load(f)
        else:
            self.nodes = []

    def query(self, query: str, top_k: int = 5) -> list[dict]:
        """쿼리와 관련된 기억 노드를 반환한다."""
        # 너무 짧은 쿼리는 스킵
        if len(query.strip()) < 5:
            return []
        keywords = query.lower().split()
        scored = []
        for node in self.nodes:
            content = node.get("content", "").lower()
            score = sum(1 for kw in keywords if kw in content)
            if score > 0:
                scored.append((score, node))

        scored.sort(key=lambda x: -x[0])
        results = []
        for score, node in scored[:top_k]:
            results.append({
                "role": "memory",
                "content": node.get("content", ""),
                "provenance": {
                    "source": "lighthouse-memory",
                    "locator": f"node:{node.get('id', '')}",
                    "fetched_at": "runtime",
                },
                "confidence": min(1.0, score / max(len(keywords), 1)),
                "reason": f"키워드 매칭 (score={score})",
                "metadata": {
                    "type": node.get("type"),
                    "session": node.get("session"),
                    "encoding_depth": node.get("encoding_depth"),
                },
            })
        return results

    def get_all(self) -> list[dict]:
        """전체 노드 목록 반환 (디버그용)."""
        return self.nodes
