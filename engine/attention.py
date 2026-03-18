"""Attention Frame — 주의력 배치 평가 및 엔트로피 계측."""

from __future__ import annotations

from .llm import call_llm_json
from .models import AttentionFrame, AttentionSlot, Promise, PromiseStatus, TurnContext
from .prompts import ATTENTION_ASSESS, SYSTEM


def build_frame(
    ctx: TurnContext,
    active_promises: list[Promise],
    source_context: str = "",
) -> AttentionFrame:
    """턴 컨텍스트에서 4슬롯 주의력 프레임을 구성한다."""
    promise_text = ", ".join(
        p.predicate for p in active_promises if p.status == PromiseStatus.active
    )
    prompt = ATTENTION_ASSESS.format(
        user_message=ctx.user_message,
        conversation_summary=ctx.conversation_summary,
        active_promises=promise_text or "(없음)",
        turn_number=ctx.turn_number,
        source_context=source_context or "(없음)",
    )
    data = call_llm_json(prompt, system=SYSTEM)

    slots = []
    for s in data.get("slots", []):
        slots.append(
            AttentionSlot(
                label=s.get("label", ""),
                content=s.get("content", ""),
                relevance=max(0.0, min(1.0, float(s.get("relevance", 0.5)))),
            )
        )
    entropy = max(0.0, min(1.0, float(data.get("entropy", 0.5))))
    return AttentionFrame(slots=slots, entropy=entropy)


def compute_entropy(frame: AttentionFrame) -> float:
    """주의력 프레임의 엔트로피를 휴리스틱으로 계산한다."""
    if not frame.slots:
        return 1.0
    relevances = [s.relevance for s in frame.slots]
    mean = sum(relevances) / len(relevances)
    variance = sum((r - mean) ** 2 for r in relevances) / len(relevances)
    normalized = 1.0 - min(variance / 0.25, 1.0)
    return round(normalized, 3)


def needs_reframe(frame: AttentionFrame, threshold: float = 0.7) -> bool:
    """엔트로피가 임계값을 넘으면 재정립이 필요하다."""
    return frame.entropy > threshold
