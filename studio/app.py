"""Co-actor Studio — Co-actor 프레임워크 체험 웹 앱."""

from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# co-actor 엔진 경로 추가
CO_ACTOR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CO_ACTOR_ROOT))

load_dotenv(CO_ACTOR_ROOT / ".env")

from engine.coactor import CoActor, TurnResponse
from engine.profile import load_profile

app = FastAPI(title="Co-actor Studio", version="0.1.0")

STATIC_DIR = Path(__file__).parent / "static"
PROFILES_DIR = CO_ACTOR_ROOT / "profiles"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ── 프로파일 목록 ──

PROFILE_META = {
    "writing-coach": {"emoji": "✍️", "color": "#E8B4B8", "description": "글을 함께 다듬는 글쓰기 동료"},
    "code-reviewer": {"emoji": "🔍", "color": "#A8D8EA", "description": "PR을 함께 검토하는 코드 리뷰 동료"},
    "study-buddy": {"emoji": "📚", "color": "#B5EAD7", "description": "새로운 개념을 함께 이해하는 학습 동료"},
    "product-strategist": {"emoji": "🎯", "color": "#FFD6A5", "description": "제품 기획을 함께 고민하는 전략 동료"},
    "lighthouse": {"emoji": "🔭", "color": "#C7CEEA", "description": "학술 논문을 함께 탐색하는 연구 동료"},
}

# ── 세션 관리 ──

sessions: dict[str, CoActor] = {}
conversations: dict[str, object] = {}


class TurnRequest(BaseModel):
    session_id: str
    message: str


class ProfileInfo(BaseModel):
    slug: str
    name: str
    role: str
    emoji: str
    color: str
    description: str
    promises: list[str]


# ── API ──

@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/api/profiles")
async def list_profiles() -> list[ProfileInfo]:
    result = []
    for yaml_file in sorted(PROFILES_DIR.glob("*.yaml")):
        slug = yaml_file.stem
        if slug == "minimal":
            continue
        try:
            profile = load_profile(str(yaml_file))
            meta = PROFILE_META.get(slug, {"emoji": "🤖", "color": "#DDD", "description": profile.identity.role})
            result.append(ProfileInfo(
                slug=slug,
                name=profile.identity.name,
                role=profile.identity.role,
                emoji=meta["emoji"],
                color=meta["color"],
                description=meta["description"],
                promises=[p.predicate for p in profile.identity.permanent_promises],
            ))
        except Exception:
            continue
    return result


@app.post("/api/session/start")
async def start_session(slug: str):
    yaml_path = PROFILES_DIR / f"{slug}.yaml"
    if not yaml_path.exists():
        raise HTTPException(404, f"프로파일 없음: {slug}")

    session_id = uuid.uuid4().hex[:12]
    agent = CoActor.from_profile(str(yaml_path))
    conv = agent.conversation(session_id)
    sessions[session_id] = agent
    conversations[session_id] = conv

    return {
        "session_id": session_id,
        "agent_name": agent.profile.identity.name,
        "agent_role": agent.profile.identity.role,
        "promises": [p.predicate for p in agent.profile.identity.permanent_promises],
    }


def _serialize_plan(plan):
    return {
        "promises": [p.predicate for p in plan.promise_snapshot],
        "attention": [
            {"label": s.label, "content": s.content[:100], "relevance": s.relevance}
            for s in plan.attention_frame.slots
        ],
        "entropy": plan.attention_frame.entropy,
        "gradient": plan.agency_gradient_hint.value,
        "constraints": plan.relationship_constraints,
        "detected_scenario": plan.detected_scenario,
    }


def _serialize_audit(audit):
    return {
        "promise_kept": audit.promise_kept,
        "attention_appropriate": audit.attention_appropriate,
        "relationship_strengthened": audit.relationship_strengthened,
        "failure_layer": audit.failure_layer.value if audit.failure_layer else None,
        "violations": [
            {"description": v.description, "severity": v.severity}
            for v in audit.violations
        ] if audit.violations else [],
        "relationship_impact": audit.relationship_impact,
    }


@app.post("/api/turn")
async def turn_sse(req: TurnRequest):
    from fastapi.responses import StreamingResponse

    conv = conversations.get(req.session_id)
    if not conv:
        raise HTTPException(404, "세션 없음")

    def generate():
        # 1단계: plan
        yield f"data: {json.dumps({'step': 'plan', 'status': 'started'})}\n\n"
        try:
            ctx = conv._prepare_turn(req.message)
            plan = conv.step_plan(ctx)
            yield f"data: {json.dumps({'step': 'plan', 'status': 'done', 'data': _serialize_plan(plan)})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'step': 'plan', 'status': 'error', 'error': str(e)})}\n\n"
            return

        # 2단계: execute
        yield f"data: {json.dumps({'step': 'execute', 'status': 'started'})}\n\n"
        try:
            agent_output = conv.step_execute(ctx, plan)
            yield f"data: {json.dumps({'step': 'execute', 'status': 'done', 'data': {'output': agent_output}})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'step': 'execute', 'status': 'error', 'error': str(e)})}\n\n"
            return

        # 3단계: audit
        yield f"data: {json.dumps({'step': 'audit', 'status': 'started'})}\n\n"
        try:
            audit = conv.step_audit(ctx, agent_output)
            yield f"data: {json.dumps({'step': 'audit', 'status': 'done', 'data': _serialize_audit(audit), 'turn_number': conv.turn_number})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'step': 'audit', 'status': 'error', 'error': str(e)})}\n\n"

        yield f"data: {json.dumps({'step': 'complete'})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    print("\n  Co-actor Studio")
    print("  http://localhost:8200\n")
    uvicorn.run(app, host="127.0.0.1", port=8200)
