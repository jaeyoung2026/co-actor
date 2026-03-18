"""lighthouse 지식 소스 어댑터 (Semantic Scholar 논문 검색).

sample 모드: 내장 샘플 논문 데이터.
live 모드: Semantic Scholar API 직접 호출. 실패 시 sample 폴백.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

SAMPLE_DIR = Path(__file__).parent / "sample_data"
S2_API = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_FIELDS = "title,abstract,year,authors,citationCount,externalIds"


class LighthouseKnowledgeAdapter:
    """knowledge 역할 소스 어댑터."""

    role = "knowledge"

    def __init__(self, mode: str = "sample"):
        self.mode = mode
        self.papers = []
        # sample 데이터는 항상 로드 (폴백용)
        sample_path = SAMPLE_DIR / "search_results_sample.json"
        if sample_path.exists():
            with open(sample_path, encoding="utf-8") as f:
                self.papers = json.load(f)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        # 너무 짧거나 인사말이면 검색하지 않는다
        if len(query.strip()) < 5 or query.strip().rstrip("?!.") in (
            "안녕", "안녕하세요", "hi", "hello", "ㅎㅇ", "반가워", "네", "응",
        ):
            return []
        if self.mode == "live":
            return self._search_live(query, top_k)
        return self._search_sample(query, top_k)

    def _search_live(self, query: str, top_k: int) -> list[dict]:
        """Semantic Scholar API로 실제 검색. 실패 시 sample 폴백."""
        for attempt in range(3):
            try:
                resp = httpx.get(
                    S2_API,
                    params={"query": query, "limit": top_k, "fields": S2_FIELDS},
                    timeout=15,
                )
                if resp.status_code == 429:
                    time.sleep(2 * (attempt + 1))
                    continue
                resp.raise_for_status()
                data = resp.json()
                return self._parse_s2_response(data, query, top_k)
            except Exception:
                if attempt < 2:
                    time.sleep(2)
                    continue

        # 모든 시도 실패 → sample 폴백
        results = self._search_sample(query, top_k)
        if results:
            results[0]["reason"] = "API 실패 — 샘플 데이터 폴백"
        return results

    def _parse_s2_response(self, data: dict, query: str, top_k: int) -> list[dict]:
        results = []
        for paper in data.get("data", [])[:top_k]:
            title = paper.get("title", "제목 없음")
            year = paper.get("year", "?")
            abstract = (paper.get("abstract") or "")[:200]
            authors = [a.get("name", "") for a in (paper.get("authors") or [])[:3]]
            citations = paper.get("citationCount", 0)
            paper_id = paper.get("paperId", "")

            content = f"[{year}] {title}"
            if authors:
                content += f" — {', '.join(authors)}"
            if abstract:
                content += f"\n  {abstract}"

            results.append({
                "role": "knowledge",
                "content": content,
                "provenance": {
                    "source": "semantic-scholar",
                    "locator": f"https://www.semanticscholar.org/paper/{paper_id}",
                    "fetched_at": _now(),
                },
                "confidence": 0.95,
                "reason": f"Semantic Scholar 검색 (query='{query}')",
                "metadata": {
                    "authors": authors,
                    "citation_count": citations,
                    "year": year,
                    "paper_id": paper_id,
                },
            })
        return results

    def _search_sample(self, query: str, top_k: int) -> list[dict]:
        keywords = query.lower().split()
        scored = []
        for paper in self.papers:
            text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scored.append((score, paper))

        scored.sort(key=lambda x: -x[0])
        results = []
        for score, paper in scored[:top_k]:
            results.append({
                "role": "knowledge",
                "content": f"[{paper['year']}] {paper['title']} — {paper.get('abstract', '')[:150]}",
                "provenance": {
                    "source": "semantic-scholar",
                    "locator": f"paper:{paper.get('id', '')}",
                    "fetched_at": "sample",
                },
                "confidence": 0.9,
                "reason": f"샘플 매칭 (score={score})",
                "metadata": {
                    "authors": paper.get("authors"),
                    "citation_count": paper.get("citation_count"),
                },
            })
        return results


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
