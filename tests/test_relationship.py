"""Relationship Ledger 로직 테스트 (LLM 호출 없음)."""

from par_loop.models import AgencyGradient, RelationshipEntry
from par_loop.relationship import compute_agency_hint, generate_constraints


def test_hint_empty_ledger():
    assert compute_agency_hint([]) == AgencyGradient.suggesting


def test_hint_agent_dominated():
    """에이전트가 주도하면 질문으로 후퇴."""
    ledger = [
        RelationshipEntry(turn=i, initiative_balance=0.5, agency_gradient=AgencyGradient.doing)
        for i in range(5)
    ]
    assert compute_agency_hint(ledger) == AgencyGradient.asking


def test_hint_user_dominated():
    """사용자가 주도하면 제안으로 전진."""
    ledger = [
        RelationshipEntry(turn=i, initiative_balance=-0.5, agency_gradient=AgencyGradient.asking)
        for i in range(5)
    ]
    assert compute_agency_hint(ledger) == AgencyGradient.suggesting


def test_constraints_agent_over_steering():
    ledger = [
        RelationshipEntry(turn=i, initiative_balance=0.6, agency_gradient=AgencyGradient.doing)
        for i in range(3)
    ]
    constraints = generate_constraints(ledger)
    assert len(constraints) >= 2  # 과도한 주도 + 연속 doing


def test_constraints_boundary_event():
    ledger = [
        RelationshipEntry(
            turn=1, initiative_balance=0.0, agency_gradient=AgencyGradient.suggesting,
            boundary_event="사용자가 '그건 아닌 것 같다'고 함",
        )
    ]
    constraints = generate_constraints(ledger)
    assert any("경계" in c for c in constraints)
