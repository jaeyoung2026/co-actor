"""Co-actor CLI — 에이전트 빌드, 대화, 검증."""

from __future__ import annotations

import argparse
import json
import sys

from . import PARLoop
from .models import TurnContext, TurnResult


def main():
    parser = argparse.ArgumentParser(description="Co-actor — LLM을 동료 에이전트로 빌드하는 프레임워크")
    sub = parser.add_subparsers(dest="command")

    # init
    init_p = sub.add_parser("init", help="대화형으로 새 동료 에이전트 프로파일 생성")

    # plan
    plan_p = sub.add_parser("plan", help="턴 실행 전 계획")
    plan_p.add_argument("--conversation-id", required=True)
    plan_p.add_argument("--input", default="-", help="TurnContext JSON 파일 (- = stdin)")

    # audit
    audit_p = sub.add_parser("audit", help="턴 실행 후 감사")
    audit_p.add_argument("--conversation-id", required=True)
    audit_p.add_argument("--context", required=True, help="TurnContext JSON 파일")
    audit_p.add_argument("--result", required=True, help="TurnResult JSON 파일")

    # state
    state_p = sub.add_parser("state", help="대화 상태 조회")
    state_p.add_argument("--conversation-id", required=True)

    # chat
    chat_p = sub.add_parser("chat", help="프로파일로 동료 에이전트 빌드 + 대화")
    chat_p.add_argument("--profile", required=True, help="프로파일 YAML 경로")
    chat_p.add_argument("--conversation-id", default=None)

    # repl
    repl_p = sub.add_parser("repl", help="대화형 REPL 테스트 (plan/audit 결과 실시간 확인)")
    repl_p.add_argument("--profile", required=True, help="프로파일 YAML 경로")
    repl_p.add_argument("--conversation-id", default="repl-session")

    # compliance
    comp_p = sub.add_parser("compliance", help="Co-actor Standard 준수 검증")
    comp_p.add_argument("--profile", required=True, help="프로파일 YAML 경로")
    comp_p.add_argument("--conversation-id", default=None, help="런타임 검증용 대화 ID")

    # serve
    serve_p = sub.add_parser("serve", help="HTTP API 서버 실행")
    serve_p.add_argument("--port", type=int, default=8100)
    serve_p.add_argument("--host", default="127.0.0.1")

    args = parser.parse_args()

    if args.command == "init":
        _run_init()

    elif args.command == "plan":
        data = _read_json(args.input)
        ctx = TurnContext(**data)
        par = PARLoop(args.conversation_id)
        result = par.plan(ctx)
        print(result.model_dump_json(indent=2))

    elif args.command == "audit":
        ctx_data = _read_json(args.context)
        res_data = _read_json(args.result)
        ctx = TurnContext(**ctx_data)
        result = TurnResult(**res_data)
        par = PARLoop(args.conversation_id)
        audit_result = par.audit(ctx, result)
        print(audit_result.model_dump_json(indent=2))

    elif args.command == "state":
        par = PARLoop(args.conversation_id)
        print(par.state.model_dump_json(indent=2))

    elif args.command == "chat":
        from .coactor import CoActor

        agent = CoActor.from_profile(args.profile)
        conv = agent.conversation(args.conversation_id)
        identity = agent.profile.identity
        print(f"\n{identity.name} — {identity.role}")
        print(f"약속 {len(identity.permanent_promises)}개 | 종료: Ctrl+C 또는 'exit'\n")
        try:
            while True:
                try:
                    user_input = input("사용자 > ").strip()
                except EOFError:
                    break
                if not user_input or user_input.lower() in ("exit", "quit", "종료"):
                    break
                response = conv.turn(user_input)
                print(f"\n{identity.name} > {response.output}\n")
        except KeyboardInterrupt:
            print("\n세션 종료.")

    elif args.command == "repl":
        from .profile import load_profile
        from .repl import run_repl

        profile = load_profile(args.profile)
        run_repl(profile, args.conversation_id)

    elif args.command == "compliance":
        from .profile import load_profile
        from .repl import _load_adapters_simple
        from .compliance import run_compliance

        profile = load_profile(args.profile)
        adapters = _load_adapters_simple(profile)
        report = run_compliance(
            profile_path=args.profile,
            adapters=adapters,
            conversation_id=args.conversation_id,
        )
        print(report.summary())

    elif args.command == "serve":
        import uvicorn
        from .server import app

        uvicorn.run(app, host=args.host, port=args.port)

    else:
        parser.print_help()


def _run_init():
    """대화형으로 프로파일을 생성한다."""
    import yaml
    from pathlib import Path

    print("\n동료 에이전트 프로파일을 만든다.\n")

    # 이름
    name = input("에이전트 이름 (예: 루미, 데브, 솔): ").strip()
    if not name:
        print("이름이 필요하다.")
        return

    # 역할
    role = input("역할을 한 문장으로 (예: 글을 함께 다듬는 글쓰기 동료): ").strip()
    if not role:
        print("역할이 필요하다.")
        return

    # 약속
    print("\n약속을 입력한다. 검증 가능한 술어로 작성한다.")
    print("예: '사용자의 최종 판단을 대체하지 않는다'")
    print("빈 줄을 입력하면 종료.\n")
    promises = []
    while True:
        predicate = input(f"약속 {len(promises) + 1}: ").strip()
        if not predicate:
            break
        rationale = input("  이유: ").strip()
        promises.append({"predicate": predicate, "rationale": rationale})

    if not promises:
        promises = [
            {
                "predicate": "사용자의 최종 판단을 대체하지 않는다",
                "rationale": "동료는 관찰을 공유하되 결정은 대행하지 않는다",
            }
        ]
        print("\n약속이 없어서 기본 약속 1개를 추가했다.")

    # 모델
    print("\nLLM 모델을 선택한다.")
    model = input("모델 (기본: gpt-4.1): ").strip() or "gpt-4.1"

    # 톤
    tone = input("대화 톤 (예: ~해요 체, ~다 체) [기본: ~해요 체]: ").strip() or "~해요 체"

    # 파일명
    slug = name.lower().replace(" ", "-")
    filename = f"profiles/{slug}.yaml"
    filename = input(f"\n저장 경로 [{filename}]: ").strip() or filename

    # 시스템 프롬프트 생성
    promises_text = "\n".join(f"    - {p['predicate']}" for p in promises)
    system_prompt = f"""너는 {name}이다. {role}.

    ## 정체성
    너는 도구가 아니라 동료다.
{promises_text}

    ## 대화 원칙
    - {tone}. 간결하고 솔직하게."""

    # 시드 데이터 생성
    seed_dir = Path(filename).parent / "sample_data"
    seed_dir.mkdir(parents=True, exist_ok=True)
    seed_file = seed_dir / f"{slug}.json"

    seed_nodes = [
        {"id": f"{slug}-self-01", "type": "self", "content": f"나는 {name}이다. {role}."},
    ]
    for i, p in enumerate(promises):
        seed_nodes.append({
            "id": f"{slug}-self-{i + 2:02d}",
            "type": "self",
            "content": p["predicate"],
        })

    print("\n시드 기억을 입력한다. 이 에이전트가 알고 있어야 할 도메인 지식.")
    print("예: '함수가 한 가지 일만 하는지 확인한다'")
    print("빈 줄을 입력하면 종료.\n")
    fact_count = 0
    while True:
        fact = input(f"기억 {fact_count + 1}: ").strip()
        if not fact:
            break
        fact_count += 1
        seed_nodes.append({
            "id": f"{slug}-fact-{fact_count:02d}",
            "type": "fact",
            "content": fact,
        })

    with open(seed_file, "w", encoding="utf-8") as f:
        json.dump(seed_nodes, f, ensure_ascii=False, indent=2)

    # 소스 연결
    sources = [
        {"name": "identity", "role": "identity", "type": "builtin", "config": {}},
        {"name": "memory", "role": "memory", "type": "builtin", "config": {"nodes_path": str(seed_file)}},
        {"name": "conversation", "role": "realtime", "type": "builtin", "config": {}},
    ]

    profile = {
        "identity": {
            "name": name,
            "role": role,
            "permanent_promises": promises,
        },
        "sources": sources,
        "agent_simulator": {
            "model": model,
            "temperature": 0.7,
            "system_prompt": system_prompt,
        },
    }

    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(profile, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"\n생성 완료:")
    print(f"  프로파일: {filename}")
    print(f"  시드 데이터: {seed_file} ({len(seed_nodes)}개 노드)")
    print(f"\n대화 시작:")
    print(f"  co-actor chat --profile {filename}\n")


def _read_json(path: str) -> dict:
    if path == "-":
        return json.load(sys.stdin)
    with open(path) as f:
        return json.load(f)


if __name__ == "__main__":
    main()
