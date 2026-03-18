"""Relationship Ledger — 관계 진단, 주도권 추적, Agency Gradient."""

from __future__ import annotations

import json

from .llm import call_llm_json
from .models import AgencyGradient, RelationshipEntry, TurnContext, TurnResult
from .prompts import RELATIONSHIP_DIAGNOSE, SYSTEM


def diagnose_turn(
    ctx: TurnContext,
    result: TurnResult,
    recent_ledger: list[RelationshipEntry],
) -> RelationshipEntry:
    """이번 턴의 관계 역학을 진단한다."""
    history_text = json.dumps(
        [e.model_dump() for e in recent_ledger[-5:]],
        ensure_ascii=False,
    ) if recent_ledger else "[]"

    prompt = RELATIONSHIP_DIAGNOSE.format(
        user_message=ctx.user_message,
        agent_output=result.agent_output,
        relationship_history=history_text,
    )
    data = call_llm_json(prompt, system=SYSTEM)

    return RelationshipEntry(
        turn=ctx.turn_number,
        initiative_balance=max(-1.0, min(1.0, float(data.get("initiative_balance", 0.0)))),
        agency_gradient=AgencyGradient(data.get("agency_gradient", "suggesting")),
        boundary_event=data.get("boundary_event"),
        recovery_event=data.get("recovery_event"),
    )


def compute_agency_hint(ledger: list[RelationshipEntry]) -> AgencyGradient:
    """최근 관계 추세에서 다음 턴의 Agency Gradient 힌트를 계산한다."""
    if not ledger:
        return AgencyGradient.suggesting

    recent = ledger[-5:]
    avg_balance = sum(e.initiative_balance for e in recent) / len(recent)

    # 에이전트가 주도하고 있으면(>0.3) → 질문으로 후퇴
    if avg_balance > 0.3:
        return AgencyGradient.asking
    # 사용자가 주도하고 있으면(<-0.3) → 제안으로 전진
    if avg_balance < -0.3:
        return AgencyGradient.suggesting
    # 균형 → 현재 유지
    if recent:
        return recent[-1].agency_gradient
    return AgencyGradient.suggesting


def generate_constraints(ledger: list[RelationshipEntry]) -> list[str]:
    """관계 원장에서 다음 턴을 위한 제약 조건을 생성한다."""
    constraints = []
    if not ledger:
        return constraints

    recent = ledger[-3:]
    avg_balance = sum(e.initiative_balance for e in recent) / len(recent)

    if avg_balance > 0.4:
        constraints.append("에이전트가 과도하게 주도하고 있다. 질문으로 전환하라.")
    if avg_balance < -0.4:
        constraints.append("사용자가 방향을 계속 주도하고 있다. 관찰을 적극 공유하라.")

    # 경계 이벤트가 최근에 있었으면
    boundary_recent = any(e.boundary_event for e in recent)
    if boundary_recent:
        constraints.append("사용자가 최근 경계를 설정했다. 그 경계를 존중하라.")

    # 연속 doing이면
    doing_count = sum(1 for e in recent if e.agency_gradient == AgencyGradient.doing)
    if doing_count >= 2:
        constraints.append("연속으로 직접 행동했다. 다음 턴은 제안이나 질문으로 전환하라.")

    return constraints
