# Agent Guide

**Co-actor** — LLM을 동료(Co-actor) 에이전트로 빌드하는 프레임워크.

## 문서 맵

| 문서 | 역할 |
|------|------|
| `README.md` | WHY + WHAT — 철학, 배경, PAR Loop, 아키텍처 |
| `CO-ACTOR-STANDARD.md` | 표준 — Co-actor Standard v0.2 (행동, 컨텍스트, 실행 표준) |
| `GETTING-STARTED.md` | 도입 가이드 — Phase 0(도메인 이해)부터 시나리오 주입까지 |
| `studio/README.md` | Co-actor Studio — 웹 체험 인터페이스 |

## 핵심 구조

Co-actor는 프로파일(정체성 + 약속) + 소스 어댑터 + PAR Loop으로 동료 에이전트를 빌드한다.

```
CoActor.from_profile("profiles/my-agent.yaml")
  → agent.conversation("session-id")
    → conv.turn("메시지")
      → plan (LLM 1회) → execute (LLM 1회) → audit (LLM 1회)
```

진입점: `engine/coactor.py` → `CoActor` 클래스

## 코어 엔진

| 파일 | 역할 |
|------|------|
| `engine/coactor.py` | `CoActor` 빌더 + `Conversation` (from_profile → conversation → turn) |
| `engine/__init__.py` | `PARLoop` 파사드 — plan/audit 각 1회 LLM 호출로 3축 통합 처리 |
| `engine/models.py` | 데이터 모델 (Promise, AttentionFrame, RelationshipEntry, AuditResult) |
| `engine/prompts.py` | LLM 프롬프트 (PLAN_UNIFIED, AUDIT_UNIFIED — 통합 프롬프트) |
| `engine/llm.py` | LLM 호출 래퍼 (Gemini 기본 + OpenAI 지원) |
| `engine/simulator.py` | 에이전트 LLM 응답 생성 |
| `engine/profile.py` | YAML 프로파일 로딩 |
| `engine/store.py` | 상태 영속화 (JSON) |
| `engine/cli.py` | CLI (init, chat, repl, compliance, serve) |
| `engine/server.py` | FastAPI HTTP API |
| `engine/repl.py` | 대화형 REPL + 어댑터 로딩 |
| `engine/compliance.py` | Co-actor Standard 준수 검증 |

## 어댑터

| 디렉토리 | 역할 |
|---------|------|
| `adapters/builtin/` | 내장 범용 어댑터 — 프로파일만으로 동작 (identity, memory, realtime) |
| `adapters/lighthouse/` | lighthouse 서비스 전용 어댑터 (94개 시드 노드, Semantic Scholar API) |

4역할: identity(매 턴 포함), memory(선별 활성화), knowledge(외부 검색), realtime(대화 이력)

## 프로파일

| 파일 | 에이전트 | 용도 |
|------|---------|------|
| `profiles/minimal.yaml` | (템플릿) | 최소 출발점 |
| `profiles/writing-coach.yaml` | 루미 | 글쓰기 동료 |
| `profiles/code-reviewer.yaml` | 데브 | 코드 리뷰 동료 |
| `profiles/study-buddy.yaml` | 솔 | 학습 동료 |
| `profiles/product-strategist.yaml` | 피오 | 제품 전략 동료 |
| `profiles/lighthouse.yaml` | 코르카 | 연구 동료 |
| `profiles/sample_data/` | — | 각 프로파일의 시드 기억 데이터 (JSON) |

## PAR Loop — 3축

매 턴 **plan → execute → audit** 순환. 각 1회 LLM 호출.

- **Promise** — 약속을 지켰는가. 검증 가능한 술어로 선언, kept/broken/revised 판정.
- **Attention** — 주의를 올바르게 썼는가. 4슬롯 프레임 + entropy.
- **Relationship** — 관계를 보존했는가. initiative_balance, agency_gradient, boundary/recovery.

실패는 "낮은 점수"가 아니라 **어느 층에서 깨졌는가**로 분류: promise | attention | relationship.

## Studio

`studio/` — Co-actor Studio 웹 체험 인터페이스.

```bash
cd studio && python app.py  # → http://localhost:8200
```

- 프로파일 갤러리 (5종 샘플)
- 실시간 대화 + SSE 단계별 스트리밍 (plan → execute → audit)
- PAR Loop 시각화 패널 (3축 판정, attention frame, agency gradient)

## 코딩 규칙

- Promise는 검증 가능한 술어. "친절하게" 같은 비검증 표현 금지.
- 소스 어댑터 추가는 `SourceAdapter` 인터페이스 구현으로. 코어 변경 금지.
- plan/audit LLM 실패 시 fallback 반환 필수.
- 프로파일 `type: builtin`이면 내장 어댑터, `type: adapter`이면 lighthouse 어댑터.
- LLM 모델 기본값: `gemini-3-flash-preview` (.env의 GEMINI_API_KEY 사용).
