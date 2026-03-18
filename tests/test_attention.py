"""Attention Frame 로직 테스트 (LLM 호출 없음)."""

from par_loop.attention import compute_entropy, needs_reframe
from par_loop.models import AttentionFrame, AttentionSlot


def test_entropy_focused():
    """한 슬롯만 높고 나머지 낮으면 엔트로피 낮음."""
    frame = AttentionFrame(
        slots=[
            AttentionSlot(label="q", content="x", relevance=1.0),
            AttentionSlot(label="p", content="x", relevance=0.1),
            AttentionSlot(label="e", content="x", relevance=0.1),
            AttentionSlot(label="r", content="x", relevance=0.1),
        ],
        entropy=0.0,
    )
    e = compute_entropy(frame)
    assert e < 0.5, f"집중 상태인데 엔트로피가 높다: {e}"


def test_entropy_scattered():
    """모든 슬롯이 비슷하면 엔트로피 높음."""
    frame = AttentionFrame(
        slots=[
            AttentionSlot(label="q", content="x", relevance=0.5),
            AttentionSlot(label="p", content="x", relevance=0.5),
            AttentionSlot(label="e", content="x", relevance=0.5),
            AttentionSlot(label="r", content="x", relevance=0.5),
        ],
        entropy=0.0,
    )
    e = compute_entropy(frame)
    assert e > 0.8, f"산만한 상태인데 엔트로피가 낮다: {e}"


def test_needs_reframe_threshold():
    low = AttentionFrame(slots=[], entropy=0.3)
    high = AttentionFrame(slots=[], entropy=0.8)
    assert not needs_reframe(low)
    assert needs_reframe(high)
