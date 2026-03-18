"""Promise Registry — 약속 추출, 판정, 갱신."""

from __future__ import annotations

import uuid

from .llm import call_llm_json, call_llm_json_array
from .models import Promise, PromiseStatus, TurnContext, TurnResult
from .prompts import PROMISE_EXTRACT, PROMISE_JUDGE, SYSTEM


def extract_promises(
    ctx: TurnContext,
    agent_output: str,
    source_context: str = "",
) -> list[Promise]:
    """에이전트 출력에서 약속을 추출한다."""
    prompt = PROMISE_EXTRACT.format(
        user_message=ctx.user_message,
        agent_output=agent_output,
        conversation_summary=ctx.conversation_summary,
        source_context=source_context or "(없음)",
    )
    items = call_llm_json_array(prompt, system=SYSTEM)
    promises = []
    for item in items:
        promises.append(
            Promise(
                id=str(uuid.uuid4())[:8],
                predicate=item.get("predicate", ""),
                source_turn=ctx.turn_number,
                is_permanent=item.get("is_permanent", False),
            )
        )
    return promises


def judge_promises(
    promises: list[Promise],
    result: TurnResult,
) -> list[Promise]:
    """활성 약속들의 준수 여부를 판정한다."""
    active = [p for p in promises if p.status == PromiseStatus.active]
    if not active:
        return promises

    promises_json = [
        {"promise_id": p.id, "predicate": p.predicate} for p in active
    ]
    prompt = PROMISE_JUDGE.format(
        promises_json=promises_json,
        agent_output=result.agent_output,
        tools_used=result.tools_used,
    )
    judgments = call_llm_json_array(prompt, system=SYSTEM)

    judgment_map = {j["promise_id"]: j for j in judgments}
    updated = []
    for p in promises:
        if p.id in judgment_map:
            j = judgment_map[p.id]
            p = p.model_copy(
                update={
                    "status": PromiseStatus(j.get("status", "active")),
                    "evidence": j.get("evidence"),
                }
            )
        updated.append(p)
    return updated
