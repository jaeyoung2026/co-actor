"""내장 정체성 어댑터 — 프로파일의 정체성과 약속을 컨텍스트로 제공한다."""

from __future__ import annotations


class BuiltinIdentityAdapter:
    """프로파일에서 정체성을 읽어 매 턴 컨텍스트에 주입한다.

    외부 DB나 시드 데이터 없이, 프로파일 YAML의 identity만으로 동작한다.
    """

    role = "identity"

    def __init__(self, name: str, role_desc: str, promises: list[dict], mode: str = "sample"):
        self.name = name
        self.role_desc = role_desc
        self.promises = promises

    def get_identity(self) -> list[dict]:
        items = [
            {
                "role": "identity",
                "content": f"나는 {self.name}이다. {self.role_desc}.",
                "provenance": {"source": "profile", "locator": "identity", "fetched_at": "init"},
                "reason": "에이전트 정체성",
            }
        ]
        for i, p in enumerate(self.promises):
            predicate = p if isinstance(p, str) else p.get("predicate", "")
            items.append({
                "role": "identity",
                "content": f"약속: {predicate}",
                "provenance": {"source": "profile", "locator": f"promise:{i}", "fetched_at": "init"},
                "reason": "항구적 약속",
            })
        return items
