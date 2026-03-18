"""PAR Loop CLI — 디버그 및 배치 실행."""

from __future__ import annotations

import argparse
import json
import sys

from . import PARLoop
from .models import TurnContext, TurnResult


def main():
    parser = argparse.ArgumentParser(description="PAR Loop CLI")
    sub = parser.add_subparsers(dest="command")

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

    # repl
    repl_p = sub.add_parser("repl", help="대화형 REPL 테스트")
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

    if args.command == "plan":
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


def _read_json(path: str) -> dict:
    if path == "-":
        return json.load(sys.stdin)
    with open(path) as f:
        return json.load(f)


if __name__ == "__main__":
    main()
