"""PAR Loop HTTP API — FastAPI."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from . import store
from .models import AuditResult, ConversationState, PlanResult, TurnContext, TurnResult

app = FastAPI(
    title="PAR Loop",
    description="에이전트가 동료(Co-actor)로서 제대로 했는가를 점검하는 엔진",
    version="0.1.0",
)


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
    return {"status": "ok", "engine": "par-loop", "version": "0.1.0"}
