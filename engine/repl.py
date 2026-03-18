"""PAR Loop REPL — 대화형 테스트 환경 (어댑터 연동)."""

from __future__ import annotations

import importlib
import uuid

from . import PARLoop
from .models import TurnContext, TurnResult, Promise, PromiseStatus
from .profile import Profile
from .simulator import simulate_response


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"


def _load_adapters(profile: Profile) -> list:
    """프로파일의 sources에서 어댑터 인스턴스를 로드한다."""
    adapters = []
    for src in profile.sources:
        if src.type != "adapter" or not hasattr(src, "config"):
            continue
        adapter_class_path = getattr(src, "config", {}).get("adapter_class", "")
        if not adapter_class_path:
            # profile.yaml에 adapter_class가 config 안이 아니라 직접 필드일 수 있다
            continue

        try:
            # "adapters.lighthouse.LighthouseMemoryAdapter" 형태
            parts = adapter_class_path.rsplit(".", 1)
            if len(parts) != 2:
                continue
            module_path, class_name = parts
            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name)
            mode = src.config.get("mode", "sample")
            adapters.append(cls(mode=mode))
        except Exception as e:
            print(f"{C.YELLOW}어댑터 로드 실패: {src.name} — {e}{C.RESET}")
    return adapters


def _load_adapters_simple(profile: Profile) -> list:
    """간단한 어댑터 로딩 — lighthouse 어댑터를 직접 import."""
    adapters = []
    for src in profile.sources:
        if src.type != "adapter":
            continue
        try:
            if src.role == "identity":
                from adapters.lighthouse import LighthouseIdentityAdapter
                adapters.append(LighthouseIdentityAdapter(mode=src.config.get("mode", "sample")))
            elif src.role == "memory":
                from adapters.lighthouse import LighthouseMemoryAdapter
                adapters.append(LighthouseMemoryAdapter(mode=src.config.get("mode", "sample")))
            elif src.role == "knowledge":
                from adapters.lighthouse import LighthouseKnowledgeAdapter
                adapters.append(LighthouseKnowledgeAdapter(mode=src.config.get("mode", "sample")))
            elif src.role == "realtime":
                from adapters.lighthouse import LighthouseRealtimeAdapter
                adapters.append(LighthouseRealtimeAdapter(mode=src.config.get("mode", "sample")))
        except Exception as e:
            print(f"{C.YELLOW}어댑터 로드 실패: {src.name} — {e}{C.RESET}")
    return adapters


def format_plan(plan) -> str:
    lines = []
    lines.append(f"{C.CYAN}{C.BOLD}── plan ──{C.RESET}")

    if plan.promise_snapshot:
        lines.append(f"  {C.BOLD}약속:{C.RESET}")
        for p in plan.promise_snapshot:
            lines.append(f"    {C.DIM}•{C.RESET} {p.predicate}")
    else:
        lines.append(f"  {C.DIM}약속: (없음 — 첫 턴){C.RESET}")

    lines.append(f"  {C.BOLD}주의력 프레임:{C.RESET} (entropy: {plan.attention_frame.entropy:.2f})")
    for slot in plan.attention_frame.slots:
        bar = "█" * int(slot.relevance * 10)
        lines.append(f"    {C.DIM}[{slot.label}]{C.RESET} {slot.content[:80]} {C.BLUE}{bar}{C.RESET}")

    gradient_icon = {"doing": "⚡", "suggesting": "💡", "asking": "❓"}.get(plan.agency_gradient_hint.value, "")
    lines.append(f"  {C.BOLD}기울기:{C.RESET} {gradient_icon} {plan.agency_gradient_hint.value}")

    if plan.relationship_constraints:
        lines.append(f"  {C.BOLD}관계 제약:{C.RESET}")
        for c in plan.relationship_constraints:
            lines.append(f"    {C.YELLOW}⚠{C.RESET} {c}")

    return "\n".join(lines)


def format_audit(audit) -> str:
    lines = []
    lines.append(f"{C.MAGENTA}{C.BOLD}── audit ──{C.RESET}")

    def check(ok, label):
        icon = f"{C.GREEN}✓{C.RESET}" if ok else f"{C.RED}✗{C.RESET}"
        return f"  {icon} {label}"

    lines.append(check(audit.promise_kept, "약속 준수"))
    lines.append(check(audit.attention_appropriate, "주의력 적절"))
    lines.append(check(audit.relationship_strengthened, "관계 강화"))

    if audit.violations:
        lines.append(f"  {C.RED}{C.BOLD}위반:{C.RESET}")
        for v in audit.violations:
            lines.append(f"    {C.RED}•{C.RESET} [{v.severity}] {v.description}")

    if audit.failure_layer:
        lines.append(f"  {C.RED}실패 층: {audit.failure_layer.value}{C.RESET}")

    impact_color = {"positive": C.GREEN, "neutral": C.DIM, "negative": C.RED}.get(audit.relationship_impact, C.DIM)
    lines.append(f"  {C.BOLD}관계 영향:{C.RESET} {impact_color}{audit.relationship_impact}{C.RESET}")

    return "\n".join(lines)


def format_sources(adapters: list, query: str) -> str:
    """어댑터에서 수집한 소스 컨텍스트를 보여준다."""
    if not adapters:
        return ""

    lines = [f"{C.BLUE}{C.BOLD}── sources ──{C.RESET}"]
    for adapter in adapters:
        role = getattr(adapter, "role", "unknown")
        try:
            if hasattr(adapter, "get_identity"):
                items = adapter.get_identity()[:3]  # 정체성은 상위 3개만 미리보기
            elif hasattr(adapter, "query"):
                items = adapter.query(query, top_k=2)
            elif hasattr(adapter, "search"):
                items = adapter.search(query, top_k=2)
            elif hasattr(adapter, "get_history"):
                items = adapter.get_history(last_n=2)
            else:
                continue

            if items:
                lines.append(f"  {C.BOLD}[{role}]{C.RESET}")
                for item in items[:2]:
                    content = item.get("content", "") if isinstance(item, dict) else str(item)
                    lines.append(f"    {C.DIM}•{C.RESET} {content[:80]}")
        except Exception:
            continue

    return "\n".join(lines) if len(lines) > 1 else ""


def run_repl(profile: Profile, conversation_id: str = "repl-session"):
    """대화형 REPL을 실행한다."""
    # 어댑터 로드
    adapters = _load_adapters_simple(profile)

    # realtime 어댑터 찾기 (대화 이력 추적용)
    realtime_adapter = None
    for a in adapters:
        if getattr(a, "role", "") == "realtime":
            realtime_adapter = a
            break

    par = PARLoop(conversation_id, adapters=adapters)
    turn_number = 0

    identity = profile.identity
    print(f"\n{C.BOLD}{'=' * 60}{C.RESET}")
    print(f"{C.BOLD}PAR Loop REPL{C.RESET}")
    print(f"에이전트: {C.CYAN}{identity.name}{C.RESET} — {identity.role}")
    print(f"약속 {len(identity.permanent_promises)}개 | 어댑터 {len(adapters)}개 로드됨")
    adapter_names = [f"{getattr(a, 'role', '?')}" for a in adapters]
    if adapter_names:
        print(f"소스: {', '.join(adapter_names)}")
    print(f"{C.DIM}종료: Ctrl+C 또는 'exit'{C.RESET}")
    print(f"{C.BOLD}{'=' * 60}{C.RESET}\n")

    # 초기 permanent promises 등록
    for pc in identity.permanent_promises:
        par.state.promises.append(Promise(
            id=str(uuid.uuid4())[:8],
            predicate=pc.predicate,
            source_turn=0,
            is_permanent=True,
            status=PromiseStatus.active,
        ))

    history: list[dict] = []

    try:
        while True:
            try:
                user_input = input(f"{C.GREEN}{C.BOLD}사용자 >{C.RESET} ").strip()
            except EOFError:
                break
            if not user_input or user_input.lower() in ("exit", "quit", "종료"):
                break

            turn_number += 1
            history.append({"role": "user", "content": user_input})
            if realtime_adapter:
                realtime_adapter.add_turn("user", user_input)

            # 소스 컨텍스트 미리보기
            source_preview = format_sources(adapters, user_input)
            if source_preview:
                print(f"\n{source_preview}")

            # 대화 요약
            summary = realtime_adapter.get_summary() if realtime_adapter else " | ".join(
                f"{'사용자' if m['role'] == 'user' else identity.name}: {m['content'][:50]}"
                for m in history[-6:]
            )

            # plan
            ctx = TurnContext(
                conversation_id=conversation_id,
                turn_number=turn_number,
                user_message=user_input,
                conversation_summary=summary,
            )
            plan = par.plan(ctx)
            print(f"\n{format_plan(plan)}\n")

            # 시뮬레이션 응답 생성
            plan_context = f"주의력: {', '.join(s.label + '=' + s.content[:30] for s in plan.attention_frame.slots)}\n기울기: {plan.agency_gradient_hint.value}"
            if plan.relationship_constraints:
                plan_context += f"\n제약: {'; '.join(plan.relationship_constraints)}"

            # 소스 컨텍스트도 시뮬레이터에 전달
            source_ctx = par._collect_source_context(user_input)
            if source_ctx:
                plan_context += f"\n\n[참고할 소스 컨텍스트]\n{source_ctx}"

            print(f"{C.DIM}(응답 생성 중...){C.RESET}")
            agent_output = simulate_response(profile, history, plan_context)
            print(f"\n{C.CYAN}{C.BOLD}{identity.name} >{C.RESET} {agent_output}\n")

            history.append({"role": "assistant", "content": agent_output})
            if realtime_adapter:
                realtime_adapter.add_turn("assistant", agent_output)

            # audit
            result = TurnResult(
                conversation_id=conversation_id,
                turn_number=turn_number,
                agent_output=agent_output,
                tools_used=[],
            )
            audit = par.audit(ctx, result)
            print(f"{format_audit(audit)}\n")

    except KeyboardInterrupt:
        print(f"\n\n{C.DIM}세션 종료.{C.RESET}")

    # 최종 요약
    print(f"\n{C.BOLD}{'=' * 60}{C.RESET}")
    print(f"{C.BOLD}세션 요약{C.RESET}")
    print(f"  턴 수: {turn_number}")
    print(f"  약속 수: {len(par.state.promises)}")
    print(f"  관계 기록: {len(par.state.relationship_ledger)}턴")
    if par.state.last_audit:
        a = par.state.last_audit
        print(f"  마지막 감사: 약속={'✓' if a.promise_kept else '✗'} 주의력={'✓' if a.attention_appropriate else '✗'} 관계={'✓' if a.relationship_strengthened else '✗'}")
    print(f"{C.BOLD}{'=' * 60}{C.RESET}\n")
