"""CoActor — LLM을 동료 에이전트로 빌드하는 최상위 API."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from . import PARLoop
from .models import (
    AuditResult,
    PlanResult,
    Promise,
    PromiseStatus,
    TurnContext,
    TurnResult,
)
from .profile import Profile, load_profile
from .repl import _load_adapters_simple
from .simulator import simulate_response


@dataclass
class TurnResponse:
    """한 턴의 결과: 에이전트 출력 + plan + audit."""

    output: str
    plan: PlanResult
    audit: AuditResult


class Conversation:
    """하나의 대화 세션. plan → execute → audit 루프를 자동 수행한다."""

    def __init__(
        self,
        conversation_id: str,
        profile: Profile,
        par: PARLoop,
        realtime_adapter=None,
    ):
        self.conversation_id = conversation_id
        self.profile = profile
        self.par = par
        self.realtime_adapter = realtime_adapter
        self.history: list[dict] = []
        self.turn_number = 0
        self.is_first_visit = True  # 첫 방문 여부 추적

    def _prepare_turn(self, user_message: str):
        """턴 준비: 히스토리 업데이트 + TurnContext 생성."""
        self.turn_number += 1
        self.history.append({"role": "user", "content": user_message})
        if self.realtime_adapter:
            self.realtime_adapter.add_turn("user", user_message)

        summary = (
            self.realtime_adapter.get_summary()
            if self.realtime_adapter
            else " | ".join(
                f"{'사용자' if m['role'] == 'user' else self.profile.identity.name}: {m['content'][:50]}"
                for m in self.history[-6:]
            )
        )

        return TurnContext(
            conversation_id=self.conversation_id,
            turn_number=self.turn_number,
            user_message=user_message,
            conversation_summary=summary,
        )

    def step_plan(self, ctx: TurnContext) -> PlanResult:
        """1단계: plan."""
        return self.par.plan(ctx)

    def step_execute(self, ctx: TurnContext, plan: PlanResult) -> str:
        """2단계: LLM 응답 생성."""
        plan_context = (
            f"주의력: {', '.join(s.label + '=' + s.content[:30] for s in plan.attention_frame.slots)}\n"
            f"기울기: {plan.agency_gradient_hint.value}"
        )
        if plan.relationship_constraints:
            plan_context += f"\n제약: {'; '.join(plan.relationship_constraints)}"

        source_ctx = self.par._collect_source_context(ctx.user_message)
        if source_ctx:
            plan_context += f"\n\n[참고할 소스 컨텍스트]\n{source_ctx}"

        agent_output = simulate_response(
            self.profile,
            self.history,
            plan_context,
            is_first_visit=self.is_first_visit,
        )

        # 첫 응답 이후 재방문으로 전환
        if self.is_first_visit:
            self.is_first_visit = False

        self.history.append({"role": "assistant", "content": agent_output})
        if self.realtime_adapter:
            self.realtime_adapter.add_turn("assistant", agent_output)

        return agent_output

    def step_audit(self, ctx: TurnContext, agent_output: str) -> AuditResult:
        """3단계: audit."""
        result = TurnResult(
            conversation_id=self.conversation_id,
            turn_number=self.turn_number,
            agent_output=agent_output,
            tools_used=[],
        )
        return self.par.audit(ctx, result)

    def turn(self, user_message: str) -> TurnResponse:
        """한 턴을 실행한다: plan → execute → audit."""
        ctx = self._prepare_turn(user_message)
        plan = self.step_plan(ctx)
        agent_output = self.step_execute(ctx, plan)
        audit = self.step_audit(ctx, agent_output)
        return TurnResponse(output=agent_output, plan=plan, audit=audit)


class CoActor:
    """LLM을 동료(Co-actor) 에이전트로 빌드하는 최상위 클래스.

    사용법:
        agent = CoActor.from_profile("profiles/my-agent.yaml")
        conv = agent.conversation("session-001")
        response = conv.turn("안녕, 논문 찾아줘")
        print(response.output)
        print(response.audit.promise_kept)
    """

    def __init__(self, profile: Profile):
        self.profile = profile
        self.adapters = _load_adapters_simple(profile)

    @classmethod
    def from_profile(cls, path: str) -> "CoActor":
        """YAML 프로파일에서 동료 에이전트를 빌드한다."""
        profile = load_profile(path)
        return cls(profile)

    def conversation(self, conversation_id: str | None = None) -> Conversation:
        """새 대화 세션을 시작한다."""
        if conversation_id is None:
            conversation_id = f"session-{uuid.uuid4().hex[:8]}"

        par = PARLoop(conversation_id, adapters=self.adapters, profile=self.profile)

        # permanent promises 등록
        for pc in self.profile.identity.permanent_promises:
            par.state.promises.append(
                Promise(
                    id=str(uuid.uuid4())[:8],
                    predicate=pc.predicate,
                    source_turn=0,
                    is_permanent=True,
                    status=PromiseStatus.active,
                )
            )

        # realtime 어댑터 찾기
        realtime_adapter = None
        for a in self.adapters:
            if getattr(a, "role", "") == "realtime":
                realtime_adapter = a
                break

        return Conversation(
            conversation_id=conversation_id,
            profile=self.profile,
            par=par,
            realtime_adapter=realtime_adapter,
        )
