"""Co-actor HTTP API — FastAPI."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from . import store
from .models import AuditResult, ConversationState, PlanResult, TurnContext, TurnResult

app = FastAPI(
    title="Co-actor",
    description="LLM을 동료(Co-actor) 에이전트로 빌드하는 프레임워크",
    version="0.2.0",
)


@app.post("/conversations/{conversation_id}/turn")
async def turn(conversation_id: str, ctx: TurnContext):
    """전체 턴 실행: plan → execute → audit."""
    from .coactor import CoActor
    from .profile import load_profile

    # NOTE: 프로덕션에서는 프로파일 경로를 설정으로 관리해야 한다
    from . import PARLoop

    par = PARLoop(conversation_id)
    plan = par.plan(ctx)
    # 이 엔드포인트는 에이전트 응답 생성 없이 plan만 반환
    # 전체 턴(plan+execute+audit)은 CoActor.conversation().turn()을 사용
    return {"plan": plan.model_dump(), "message": "전체 턴 실행은 CoActor API를 사용하세요"}


@app.post("/conversations/{conversation_id}/plan", response_model=PlanResult)
async def plan(conversation_id: str, ctx: TurnContext):
    from . import PARLoop

    par = PARLoop(conversation_id)
    return par.plan(ctx)


@app.post("/conversations/{conversation_id}/audit", response_model=AuditResult)
async def audit(conversation_id: str, ctx: TurnContext, result: TurnResult):
    from . import PARLoop

    par = PARLoop(conversation_id)
    return par.audit(ctx, result)


@app.get("/conversations/{conversation_id}/state", response_model=ConversationState)
async def get_state(conversation_id: str):
    state = store.load_state(conversation_id)
    return state


@app.post("/conversations/{conversation_id}/reset")
async def reset(conversation_id: str):
    store.delete_state(conversation_id)
    return {"status": "reset", "conversation_id": conversation_id}


@app.get("/health")
async def health():
    return {"status": "ok", "engine": "co-actor", "version": "0.2.0"}
