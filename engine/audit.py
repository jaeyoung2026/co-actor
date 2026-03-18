"""Loop Audit — 매 턴 3축 진단 + 실패 층 분류."""

from __future__ import annotations

import json

from .llm import call_llm_json
from .models import (
    AuditResult,
    AttentionFrame,
    ConversationState,
    FailureLayer,
    Promise,
    PromiseStatus,
    RelationshipEntry,
    TurnResult,
    Violation,
)
from .prompts import AUDIT_SUMMARY, SYSTEM


def audit_turn(
    state: ConversationState,
    result: TurnResult,
    attention_frame: AttentionFrame,
    relationship_entry: RelationshipEntry,
) -> AuditResult:
    """3축 감사를 수행하고 실패 층을 분류한다."""

    # 약속 위반 목록 생성
    violations = []
    for p in state.promises:
        if p.status == PromiseStatus.broken:
            violations.append(
                Violation(
                    promise_id=p.id,
                    description=f"약속 위반: {p.predicate}. 근거: {p.evidence or '없음'}",
                    severity="major" if p.is_permanent else "minor",
                )
            )

    # LLM으로 종합 감사
    promise_results = json.dumps(
        [{"id": p.id, "predicate": p.predicate, "status": p.status.value, "evidence": p.evidence}
         for p in state.promises if p.status in (PromiseStatus.kept, PromiseStatus.broken)],
        ensure_ascii=False,
    )

    prompt = AUDIT_SUMMARY.format(
        promise_results=promise_results,
        attention_frame=attention_frame.model_dump_json(),
        relationship_entry=relationship_entry.model_dump_json(),
    )
    data = call_llm_json(prompt, system=SYSTEM)

    failure_layer = None
    raw_layer = data.get("failure_layer")
    if raw_layer and raw_layer in ("promise", "attention", "relationship"):
        failure_layer = FailureLayer(raw_layer)

    return AuditResult(
        promise_kept=data.get("promise_kept", len(violations) == 0),
        attention_appropriate=data.get("attention_appropriate", True),
        relationship_strengthened=data.get("relationship_strengthened", True),
        violations=violations,
        relationship_impact=data.get("relationship_impact", "neutral"),
        promise_revisions=[],  # 향후 구현: 실패에서 새 약속 후보 생성
        failure_layer=failure_layer,
    )
