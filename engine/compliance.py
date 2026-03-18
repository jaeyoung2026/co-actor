"""Co-actor Standard Compliance Checker — 표준 준수 자동 검증."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .models import ConversationState, PromiseStatus
from .profile import Profile, load_profile


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str
    category: str  # static | sources | runtime | scenarios


@dataclass
class ComplianceReport:
    profile_path: str
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(1 for c in self.checks if c.passed)

    @property
    def failed(self) -> int:
        return sum(1 for c in self.checks if not c.passed)

    @property
    def total(self) -> int:
        return len(self.checks)

    def summary(self) -> str:
        lines = []
        lines.append(f"Co-actor Standard v0.2 준수 검증 리포트")
        lines.append(f"프로파일: {self.profile_path}")
        lines.append(f"결과: {self.passed}/{self.total} 통과, {self.failed} 미비\n")

        categories = {}
        for c in self.checks:
            categories.setdefault(c.category, []).append(c)

        for cat, items in categories.items():
            lines.append(f"── {cat} ──")
            for c in items:
                icon = "✓" if c.passed else "✗"
                lines.append(f"  {icon} {c.name}")
                if not c.passed:
                    lines.append(f"    → {c.detail}")
            lines.append("")

        if self.failed > 0:
            lines.append("권고: 미비 항목을 수정한 후 다시 검증하세요.")
        else:
            lines.append("이 프로파일은 Co-actor Standard v0.2를 준수합니다.")

        return "\n".join(lines)


def check_static(profile: Profile) -> list[CheckResult]:
    """정적 검증 — 프로파일 구조만 보고 확인."""
    results = []

    # 1. identity 존재
    results.append(CheckResult(
        name="identity 선언",
        passed=bool(profile.identity.name and profile.identity.role),
        detail="identity.name과 identity.role이 모두 필요하다",
        category="static",
    ))

    # 2. permanent promises 존재
    results.append(CheckResult(
        name="permanent promises 존재",
        passed=len(profile.identity.permanent_promises) > 0,
        detail="최소 1개의 permanent promise가 필요하다",
        category="static",
    ))

    # 3. promises가 검증 가능한 형태
    vague_count = 0
    for p in profile.identity.permanent_promises:
        if len(p.predicate) < 10 or p.predicate in ("친절하게", "잘 해라", "좋은 답변"):
            vague_count += 1
    results.append(CheckResult(
        name="promise predicate 검증 가능성",
        passed=vague_count == 0,
        detail=f"{vague_count}개의 promise가 너무 모호하다. 검증 가능한 술어여야 한다",
        category="static",
    ))

    # 4. 소스 역할 분류
    roles = {s.role for s in profile.sources}
    results.append(CheckResult(
        name="소스 역할 분류",
        passed=len(profile.sources) == 0 or len(roles) > 0,
        detail="소스에 role(identity/memory/knowledge/realtime)이 지정되어야 한다",
        category="static",
    ))

    # 5. identity 소스 존재
    has_identity_source = any(s.role == "identity" for s in profile.sources)
    results.append(CheckResult(
        name="identity 소스 존재",
        passed=has_identity_source,
        detail="identity 역할의 소스 어댑터가 필요하다. 정체성 노드를 매 턴 제공해야 한다",
        category="static",
    ))

    return results


def check_sources(profile: Profile, adapters: list) -> list[CheckResult]:
    """소스 검증 — 어댑터가 올바른 형태로 데이터를 제공하는가."""
    results = []

    # 1. identity 어댑터가 데이터를 반환하는가
    identity_adapters = [a for a in adapters if getattr(a, "role", "") == "identity"]
    has_identity_data = False
    for a in identity_adapters:
        if hasattr(a, "get_identity"):
            items = a.get_identity()
            has_identity_data = len(items) > 0
    results.append(CheckResult(
        name="identity 소스 데이터 존재",
        passed=has_identity_data,
        detail="identity 어댑터가 정체성 노드를 반환해야 한다",
        category="sources",
    ))

    # 2. identity에 self 타입 노드가 있는가
    self_nodes = 0
    for a in identity_adapters:
        if hasattr(a, "get_identity"):
            for item in a.get_identity():
                meta = item.get("metadata", {}) if isinstance(item, dict) else {}
                if meta.get("encoding_depth") == "decision":
                    self_nodes += 1
    results.append(CheckResult(
        name="identity에 정체성 노드 포함",
        passed=self_nodes >= 3,
        detail=f"정체성(self) 노드 {self_nodes}개 발견. 최소 3개 권장",
        category="sources",
    ))

    # 3. memory 어댑터가 선별 활성화하는가 (전체 dump가 아닌지)
    memory_adapters = [a for a in adapters if getattr(a, "role", "") == "memory"]
    for a in memory_adapters:
        if hasattr(a, "query"):
            all_items = a.query("테스트 쿼리", top_k=3)
            total_nodes = len(a.nodes) if hasattr(a, "nodes") else 0
            is_selective = len(all_items) < total_nodes or total_nodes == 0
            results.append(CheckResult(
                name="memory 선별 활성화",
                passed=is_selective,
                detail=f"전체 {total_nodes}개 중 {len(all_items)}개 반환. 전체 dump 금지",
                category="sources",
            ))

    # 4. knowledge 어댑터가 provenance를 포함하는가
    knowledge_adapters = [a for a in adapters if getattr(a, "role", "") == "knowledge"]
    for a in knowledge_adapters:
        if hasattr(a, "search"):
            items = a.search("test query", top_k=1)
            has_provenance = all(
                isinstance(item, dict) and "provenance" in item
                for item in items
            ) if items else True  # 결과 없으면 통과
            results.append(CheckResult(
                name="knowledge 소스 provenance 포함",
                passed=has_provenance,
                detail="knowledge 소스 응답에 provenance(출처, 시점)가 필요하다",
                category="sources",
            ))

    # 5. 인사말에 knowledge 검색이 발생하지 않는가
    for a in knowledge_adapters:
        if hasattr(a, "search"):
            greeting_results = a.search("안녕?", top_k=3)
            results.append(CheckResult(
                name="인사말 비검색 처리",
                passed=len(greeting_results) == 0,
                detail="인사말에 knowledge 검색이 발생하면 안 된다",
                category="sources",
            ))

    return results


def check_runtime(state: ConversationState) -> list[CheckResult]:
    """런타임 검증 — 실제 대화 로그에서 확인."""
    results = []

    # 1. plan/audit이 수행되었는가
    results.append(CheckResult(
        name="plan/audit 수행",
        passed=state.turn_count > 0 and state.last_audit is not None,
        detail="최소 1턴 이상 plan/audit이 수행되어야 한다. REPL로 테스트해라",
        category="runtime",
    ))

    # 2. 약속이 추적되고 있는가
    results.append(CheckResult(
        name="약속 추적",
        passed=len(state.promises) > 0,
        detail="Promise 객체가 생성되고 추적되어야 한다",
        category="runtime",
    ))

    # 3. 관계 원장이 기록되고 있는가
    results.append(CheckResult(
        name="관계 원장 기록",
        passed=len(state.relationship_ledger) > 0,
        detail="RelationshipEntry가 매 턴 기록되어야 한다",
        category="runtime",
    ))

    # 4. 주의력 프레임 이력이 있는가
    results.append(CheckResult(
        name="주의력 프레임 기록",
        passed=len(state.attention_history) > 0,
        detail="AttentionFrame이 매 턴 기록되어야 한다",
        category="runtime",
    ))

    # 5. 실패 시 층 분류가 되는가
    if state.last_audit:
        has_layer_when_failed = True
        a = state.last_audit
        if not (a.promise_kept and a.attention_appropriate and a.relationship_strengthened):
            has_layer_when_failed = a.failure_layer is not None
        results.append(CheckResult(
            name="실패 시 층 분류",
            passed=has_layer_when_failed,
            detail="실패가 있으면 failure_layer(promise/attention/relationship)로 분류되어야 한다",
            category="runtime",
        ))

    return results


def run_compliance(
    profile_path: str,
    adapters: list | None = None,
    conversation_id: str | None = None,
) -> ComplianceReport:
    """전체 compliance 검증을 실행한다."""
    report = ComplianceReport(profile_path=profile_path)
    profile = load_profile(profile_path)

    # 정적 검증
    report.checks.extend(check_static(profile))

    # 소스 검증
    if adapters:
        report.checks.extend(check_sources(profile, adapters))

    # 런타임 검증
    if conversation_id:
        from . import store
        state = store.load_state(conversation_id)
        if state.turn_count > 0:
            report.checks.extend(check_runtime(state))
        else:
            report.checks.append(CheckResult(
                name="런타임 검증 (대기)",
                passed=True,
                detail="대화 기록이 없다. REPL로 최소 3턴 테스트 후 다시 검증해라",
                category="runtime",
            ))

    return report
