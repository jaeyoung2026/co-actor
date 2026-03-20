"""에이전트 시뮬레이터 — Co-actor가 빌드한 에이전트의 LLM 응답 생성."""

from __future__ import annotations

from .llm import call_llm
from .profile import Profile


def build_system_prompt(
    profile: Profile,
    plan_context: str = "",
    is_first_visit: bool = True,
) -> str:
    """프로파일에서 시뮬레이터용 시스템 프롬프트를 구성한다."""
    identity = profile.identity
    promises_text = "\n".join(
        f"  - {p.predicate}" for p in identity.permanent_promises
    )

    # 시스템 프롬프트 우선순위: 루트 system_prompt > agent_simulator.system_prompt > 자동 생성
    base = profile.system_prompt or profile.agent_simulator.system_prompt
    if not base:
        base = f"""너는 {identity.name}이다. {identity.role}.

행동 원칙:
{promises_text}

한국어로 대화한다. ~다 체를 사용한다. 간결하게 답한다."""

    # first_visit / revisit 분기
    if is_first_visit and profile.first_visit:
        base += f"\n\n[상황]\n{profile.first_visit}"
    elif not is_first_visit and profile.revisit:
        base += f"\n\n[상황]\n{profile.revisit}"

    if plan_context:
        base += f"\n\n[Co-actor plan 결과 — 이번 턴에서 참고할 것]\n{plan_context}"

    return base


def simulate_response(
    profile: Profile,
    conversation_history: list[dict],
    plan_context: str = "",
    is_first_visit: bool = True,
) -> str:
    """에이전트 응답을 시뮬레이션한다."""
    system = build_system_prompt(profile, plan_context, is_first_visit)

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
