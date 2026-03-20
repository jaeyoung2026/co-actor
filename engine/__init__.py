"""Co-actor Engine — LLM을 동료(Co-actor) 에이전트로 빌드하고, PAR Loop으로 매 턴 조율·검증한다."""

from __future__ import annotations

import json
import uuid

from . import relationship, store
from .llm import call_llm_json
from .models import (
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
from .prompts import SYSTEM, PLAN_UNIFIED, AUDIT_UNIFIED


class PARLoop:
    """PAR Loop 파사드. plan() → 에이전트 실행 → audit() 순환. 각 1회 LLM 호출."""

    def __init__(self, conversation_id: str, adapters: list | None = None, profile=None):
        self.conversation_id = conversation_id
        self.state = store.load_state(conversation_id)
        self.adapters = adapters or []
        self.profile = profile  # Profile 객체 (시나리오, antipattern 등 참조용)

    def _collect_source_context(self, query: str) -> str:
        """어댑터에서 소스 컨텍스트를 수집한다."""
        if not self.adapters:
            return ""

        parts = []
        for adapter in self.adapters:
            role = getattr(adapter, "role", "unknown")
            try:
                if hasattr(adapter, "get_identity"):
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
        """턴 실행 전: LLM 1회 호출로 주의력 프레임 + 관계 제약 + 기울기 힌트 생성."""
        active_promises = [
            p for p in self.state.promises
            if p.status.value == "active"
        ]

        source_context = self._collect_source_context(ctx.user_message)
        promise_text = ", ".join(p.predicate for p in active_promises) or "(없음)"

        history_text = json.dumps(
            [e.model_dump() for e in self.state.relationship_ledger[-5:]],
            ensure_ascii=False,
        ) if self.state.relationship_ledger else "[]"

        # 시나리오 섹션 생성
        scenarios_section = ""
        if self.profile and self.profile.scenarios.classification:
            lines = ["## 시나리오 분류 (현재 사용자 행동에 해당하는 시나리오를 detected_scenario에 적어라)"]
            for sc in self.profile.scenarios.classification:
                promises_str = f" | 약속: {'; '.join(sc.situational_promises)}" if sc.situational_promises else ""
                lines.append(f"- {sc.name}: {sc.signal} (기본 기울기: {sc.agency_default}){promises_str}")
            scenarios_section = "\n".join(lines)

        prompt = PLAN_UNIFIED.format(
            user_message=ctx.user_message,
            conversation_summary=ctx.conversation_summary,
            active_promises=promise_text,
            turn_number=ctx.turn_number,
            relationship_history=history_text,
            source_context=source_context or "(없음)",
            scenarios_section=scenarios_section,
        )

        try:
            data = call_llm_json(prompt, system=SYSTEM)
        except Exception:
            data = {}

        # 시나리오 감지 → 상황 약속 자동 주입
        detected = data.get("detected_scenario")
        if detected and self.profile and self.profile.scenarios.classification:
            for sc in self.profile.scenarios.classification:
                if sc.name == detected:
                    for sp in sc.situational_promises:
                        # 이미 동일한 약속이 없으면 추가
                        existing = {p.predicate for p in self.state.promises}
                        if sp not in existing:
                            self.state.promises.append(Promise(
                                id=str(uuid.uuid4())[:8],
                                predicate=sp,
                                source_turn=ctx.turn_number,
                                is_permanent=False,
                                status=PromiseStatus.active,
                            ))
                    break

        # 주의력 프레임 파싱
        frame_data = data.get("attention_frame", {})
        slots = []
        for s in frame_data.get("slots", []):
            slots.append(AttentionSlot(
                label=s.get("label", ""),
                content=s.get("content", ""),
                relevance=max(0.0, min(1.0, float(s.get("relevance", 0.5)))),
            ))
        if not slots:
            slots = [AttentionSlot(
                label="current_question",
                content=ctx.user_message[:200],
                relevance=1.0,
            )]
        frame = AttentionFrame(
            slots=slots,
            entropy=max(0.0, min(1.0, float(frame_data.get("entropy", 0.5)))),
        )

        # 기울기 — LLM 결과 우선, 없으면 휴리스틱
        gradient_raw = data.get("agency_gradient_hint", "")
        try:
            gradient_hint = AgencyGradient(gradient_raw)
        except ValueError:
            gradient_hint = relationship.compute_agency_hint(self.state.relationship_ledger)

        # 관계 제약 — LLM 결과 + 휴리스틱 병합
        constraints = data.get("relationship_constraints", [])
        if not constraints:
            constraints = relationship.generate_constraints(self.state.relationship_ledger)

        return PlanResult(
            promise_snapshot=active_promises,
            attention_frame=frame,
            relationship_constraints=constraints,
            agency_gradient_hint=gradient_hint,
            detected_scenario=data.get("detected_scenario"),
        )

    def audit(self, ctx: TurnContext, result: TurnResult) -> AuditResult:
        """턴 실행 후: LLM 1회 호출로 약속 판정 + 주의력 + 관계 진단 + 종합 감사."""
        source_context = self._collect_source_context(ctx.user_message)

        active = [p for p in self.state.promises if p.status.value == "active"]

        # antipattern을 포함한 약속 JSON 생성
        active_items = []
        for p in active:
            item = {"promise_id": p.id, "predicate": p.predicate}
            # profile에서 antipattern 찾기
            if self.profile:
                for pc in self.profile.identity.permanent_promises:
                    if pc.predicate == p.predicate and pc.antipattern:
                        item["antipattern"] = pc.antipattern
                        break
            active_items.append(item)

        active_json = json.dumps(active_items, ensure_ascii=False)

        history_text = json.dumps(
            [e.model_dump() for e in self.state.relationship_ledger[-5:]],
            ensure_ascii=False,
        ) if self.state.relationship_ledger else "[]"

        # 도메인 체크리스트 섹션 생성
        domain_checklist_section = ""
        if self.profile and self.profile.scenarios.audit_domain_checklist:
            lines = ["## 도메인 품질 체크리스트 (추가 위반 감지, 위반 시 violations에 포함)"]
            for item in self.profile.scenarios.audit_domain_checklist:
                lines.append(f"- {item}")
            domain_checklist_section = "\n".join(lines)

        prompt = AUDIT_UNIFIED.format(
            user_message=ctx.user_message,
            agent_output=result.agent_output,
            conversation_summary=ctx.conversation_summary,
            tools_used=result.tools_used,
            turn_number=ctx.turn_number,
            active_promises_json=active_json,
            relationship_history=history_text,
            source_context=source_context or "(없음)",
            domain_checklist_section=domain_checklist_section,
        )

        try:
            data = call_llm_json(prompt, system=SYSTEM)
        except Exception:
            data = {}

        # 1. 약속 판정 적용
        judgment_map = {
            j["promise_id"]: j
            for j in data.get("promise_judgments", [])
        }
        updated_promises = []
        for p in self.state.promises:
            if p.id in judgment_map:
                j = judgment_map[p.id]
                p = p.model_copy(update={
                    "status": PromiseStatus(j.get("status", "active")),
                    "evidence": j.get("evidence"),
                })
            updated_promises.append(p)
        self.state.promises = updated_promises

        # 2. 새 약속 추가
        for np in data.get("new_promises", []):
            self.state.promises.append(Promise(
                id=str(uuid.uuid4())[:8],
                predicate=np.get("predicate", ""),
                source_turn=ctx.turn_number,
                is_permanent=np.get("is_permanent", False),
            ))

        # 3. 주의력 프레임 파싱
        frame_data = data.get("attention_frame", {})
        slots = []
        for s in frame_data.get("slots", []):
            slots.append(AttentionSlot(
                label=s.get("label", ""),
                content=s.get("content", ""),
                relevance=max(0.0, min(1.0, float(s.get("relevance", 0.5)))),
            ))
        frame = AttentionFrame(
            slots=slots,
            entropy=max(0.0, min(1.0, float(frame_data.get("entropy", 0.5)))),
        )
        self.state.attention_history.append(frame)

        # 4. 관계 진단 파싱
        rel_data = data.get("relationship_entry", {})
        try:
            gradient = AgencyGradient(rel_data.get("agency_gradient", "suggesting"))
        except ValueError:
            gradient = AgencyGradient.suggesting

        rel_entry = RelationshipEntry(
            turn=ctx.turn_number,
            initiative_balance=max(-1.0, min(1.0, float(rel_data.get("initiative_balance", 0.0)))),
            agency_gradient=gradient,
            boundary_event=rel_data.get("boundary_event"),
            recovery_event=rel_data.get("recovery_event"),
        )
        self.state.relationship_ledger.append(rel_entry)

        # 5. 종합 감사 결과
        audit_data = data.get("audit_result", {})
        violations = []
        for p in self.state.promises:
            if p.status == PromiseStatus.broken:
                violations.append(Violation(
                    promise_id=p.id,
                    description=f"약속 위반: {p.predicate}. 근거: {p.evidence or '없음'}",
                    severity="major" if p.is_permanent else "minor",
                ))

        failure_layer = None
        raw_layer = audit_data.get("failure_layer")
        if raw_layer and raw_layer in ("promise", "attention", "relationship"):
            failure_layer = FailureLayer(raw_layer)

        audit_result = AuditResult(
            promise_kept=audit_data.get("promise_kept", len(violations) == 0),
            attention_appropriate=audit_data.get("attention_appropriate", True),
            relationship_strengthened=audit_data.get("relationship_strengthened", True),
            violations=violations,
            relationship_impact=audit_data.get("relationship_impact", "neutral"),
            promise_revisions=[],
            failure_layer=failure_layer,
        )

        self.state.last_audit = audit_result
        self.state.turn_count = ctx.turn_number
        store.save_state(self.state)

        return audit_result


from .coactor import CoActor, Conversation, TurnResponse

__all__ = [
    "CoActor",
    "Conversation",
    "TurnResponse",
    "PARLoop",
    "TurnContext",
    "TurnResult",
    "PlanResult",
    "AuditResult",
    "AgencyGradient",
    "ConversationState",
]
