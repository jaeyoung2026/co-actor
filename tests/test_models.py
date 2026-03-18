"""PAR Loop 모델 테스트."""

from par_loop.models import (
    AgencyGradient,
    AttentionFrame,
    AttentionSlot,
    AuditResult,
    ConversationState,
    FailureLayer,
    PlanResult,
    Promise,
    PromiseStatus,
    RelationshipEntry,
    TurnContext,
    TurnResult,
    Violation,
)


def test_conversation_state_defaults():
    state = ConversationState(conversation_id="test")
    assert state.turn_count == 0
    assert state.promises == []
    assert state.relationship_ledger == []
    assert state.last_audit is None


def test_promise_creation():
    p = Promise(id="p1", predicate="검색 결과를 공유한다", source_turn=1, is_permanent=False)
    assert p.status == PromiseStatus.active
    assert p.evidence is None


def test_attention_frame():
    frame = AttentionFrame(
        slots=[
            AttentionSlot(label="q", content="다양성 논문", relevance=0.9),
            AttentionSlot(label="p", content="검색 약속", relevance=0.7),
        ],
        entropy=0.3,
    )
    assert len(frame.slots) == 2
    assert 0 <= frame.entropy <= 1


def test_relationship_entry():
    entry = RelationshipEntry(
        turn=1,
        initiative_balance=0.2,
        agency_gradient=AgencyGradient.suggesting,
    )
    assert entry.boundary_event is None


def test_plan_result_serialization():
    result = PlanResult(
        promise_snapshot=[],
        attention_frame=AttentionFrame(slots=[], entropy=0.5),
        relationship_constraints=["주도권 균형 유지"],
        agency_gradient_hint=AgencyGradient.asking,
    )
    data = result.model_dump()
    assert data["agency_gradient_hint"] == "asking"


def test_audit_result():
    audit = AuditResult(
        promise_kept=True,
        attention_appropriate=True,
        relationship_strengthened=False,
        violations=[],
        relationship_impact="neutral",
        promise_revisions=[],
        failure_layer=FailureLayer.relationship,
    )
    assert audit.failure_layer == FailureLayer.relationship


def test_state_roundtrip():
    state = ConversationState(conversation_id="rt-test")
    json_str = state.model_dump_json()
    restored = ConversationState.model_validate_json(json_str)
    assert restored.conversation_id == "rt-test"
