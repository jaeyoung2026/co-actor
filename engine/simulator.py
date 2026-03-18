"""에이전트 시뮬레이터 — REPL에서 에이전트 역할을 수행하는 LLM 호출."""

from __future__ import annotations

from .llm import call_llm
from .profile import Profile


def build_system_prompt(profile: Profile, plan_context: str = "") -> str:
    """프로파일에서 시뮬레이터용 시스템 프롬프트를 구성한다."""
    identity = profile.identity
    promises_text = "\n".join(
        f"  - {p.predicate}" for p in identity.permanent_promises
    )

    base = profile.agent_simulator.system_prompt
    if not base:
        base = f"""너는 {identity.name}이다. {identity.role}.

행동 원칙:
{promises_text}

한국어로 대화한다. ~다 체를 사용한다. 간결하게 답한다."""

    if plan_context:
        base += f"\n\n[Co-actor Engine plan 결과 — 이번 턴에서 참고할 것]\n{plan_context}"

    return base


def simulate_response(
    profile: Profile,
    conversation_history: list[dict],
    plan_context: str = "",
) -> str:
    """에이전트 응답을 시뮬레이션한다."""
    system = build_system_prompt(profile, plan_context)

    # 대화 이력을 프롬프트로 변환
    history_text = ""
    for msg in conversation_history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            history_text += f"\n사용자: {content}"
        else:
            history_text += f"\n{profile.identity.name}: {content}"

    prompt = f"{history_text}\n\n{profile.identity.name}:"

    response = call_llm(
        prompt=prompt,
        system=system,
        model=profile.agent_simulator.model,
        temperature=profile.agent_simulator.temperature,
    )
    return response
