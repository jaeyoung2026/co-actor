"""PAR Loop — Promise·Attention·Relationship 순환으로 에이전트 동료 품질을 점검하는 엔진."""

from __future__ import annotations

from . import attention, promise, relationship, store
from .audit import audit_turn
from .models import (
    AgencyGradient,
    AuditResult,
    ConversationState,
    PlanResult,
    TurnContext,
    TurnResult,
)


class PARLoop:
    """PAR Loop 파사드. plan() → 에이전트 실행 → audit() 순환."""

    def __init__(self, conversation_id: str, adapters: list | None = None):
        self.conversation_id = conversation_id
        self.state = store.load_state(conversation_id)
        self.adapters = adapters or []

    def _collect_source_context(self, query: str) -> str:
        """어댑터에서 소스 컨텍스트를 수집한다."""
        if not self.adapters:
            return ""

        parts = []
        for adapter in self.adapters:
            role = getattr(adapter, "role", "unknown")
            try:
                if hasattr(adapter, "get_identity"):
                    # identity 어댑터: 항상 전체 반환 (쿼리 무관)
                    items = adapter.get_identity()
                elif hasattr(adapter, "query"):
                    items = adapter.query(query, top_k=3)
                elif hasattr(adapter, "search"):
                    items = adapter.search(query, top_k=3)
                elif hasattr(adapter, "get_history"):
                    items = adapter.get_history(last_n=4)
                else:
                    continue

                for item in items:
                    content = item.get("content", "") if isinstance(item, dict) else str(item)
                    parts.append(f"[{role}] {content}")
            except Exception:
                continue

        return "\n".join(parts) if parts else ""

    def plan(self, ctx: TurnContext) -> PlanResult:
        """턴 실행 전: 약속 스냅샷 + 주의력 프레임 + 관계 제약 + 기울기 힌트."""
        active_promises = [
            p for p in self.state.promises
            if p.status.value == "active"
        ]

        source_context = self._collect_source_context(ctx.user_message)

        frame = attention.build_frame(ctx, active_promises, source_context)
        gradient_hint = relationship.compute_agency_hint(self.state.relationship_ledger)
        constraints = relationship.generate_constraints(self.state.relationship_ledger)

        return PlanResult(
            promise_snapshot=active_promises,
            attention_frame=frame,
            relationship_constraints=constraints,
            agency_gradient_hint=gradient_hint,
        )

    def audit(self, ctx: TurnContext, result: TurnResult) -> AuditResult:
        """턴 실행 후: 약속 준수 + 주의력 적절성 + 관계 영향 + 실패 층 분류."""
        source_context = self._collect_source_context(ctx.user_message)

        # 1. 에이전트 출력에서 새 약속 추출
        new_promises = promise.extract_promises(ctx, result.agent_output, source_context)
        self.state.promises.extend(new_promises)

        # 2. 약속 판정
        self.state.promises = promise.judge_promises(self.state.promises, result)

        # 3. 주의력 프레임 (사후 평가용)
        active = [p for p in self.state.promises if p.status.value == "active"]
        frame = attention.build_frame(ctx, active, source_context)
        self.state.attention_history.append(frame)

        # 4. 관계 진단
        rel_entry = relationship.diagnose_turn(
            ctx, result, self.state.relationship_ledger,
        )
        self.state.relationship_ledger.append(rel_entry)

        # 5. 종합 감사
        audit_result = audit_turn(self.state, result, frame, rel_entry)
        self.state.last_audit = audit_result
        self.state.turn_count = ctx.turn_number

        # 6. 상태 저장
        store.save_state(self.state)

        return audit_result


__all__ = [
    "PARLoop",
    "TurnContext",
    "TurnResult",
    "PlanResult",
    "AuditResult",
    "AgencyGradient",
    "ConversationState",
]
