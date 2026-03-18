# Co-actor Engine — 리서치 히스토리

> AI 에이전트가 도구가 아니라 동료(Co-actor)로서 동작하기 위한 실행 표준과 엔진의 탄생 과정.

---

## 1. 문제 인식 (2026-03 초)

lighthouse 유저 테스트에서 핵심 문제가 드러났다: **에이전트가 도구처럼 행동한다.**
- 출력은 정확하지만 함께 일하고 싶지 않은 에이전트
- 프롬프트를 아무리 고쳐도 "동료" 행동이 안정적으로 나오지 않음
- 기존 평가 방식(출력 채점)은 도구의 평가법이지 동료의 점검법이 아님

이 문제 인식이 "대화 정책 엔지니어링" 아이디어로 발전했다.

## 2. 프롬프트 → 정책 전환 (세션91 전반)

코덱스(gpt-5.4)의 교정:
> "프롬프트 개선이 아니라 **행동 계약(behavior contract)** 정의가 먼저다."

이 교정으로 방향이 전환됐다:
- 프롬프트 문장 = 구현 (모델이 바뀌면 깨진다)
- 행동 계약 = 정책 (모델과 독립적)
- 대화 품질의 단위를 "출력 채점"에서 "약속의 순환 건강도"로 재정의

관련 문서: `research/prompt-engineering-strategy.md`

## 3. 핵심 원리 추출 (세션91)

6개 관점 × 2개 에이전트(브로콜리 + 코덱스) = 12개 원리 문서에서 28개 원리 추출.

### 6개 관점
| # | 관점 | 에이전트 | 파일 |
|---|------|---------|------|
| 1 | 순수 과제 (아무 역할 없음) | 브로콜리 | `principles/01-pure-task.md` |
| 2 | 생태학자 | 브로콜리 | `principles/02-ecologist.md` |
| 3 | 첫 번째 원리 사고자 | 브로콜리 | `principles/03-first-principles-broccoli.md` |
| 4 | 시스템 사상가 | 코덱스 | `principles/04-systems-thinker-codex.md` |
| 5 | 인지과학자 | 코덱스 | `principles/05-cognitive-scientist-codex.md` |
| 6 | 첫 번째 원리 사고자 | 코덱스 | `principles/06-first-principles-codex.md` |

### 3개 핵심 축으로 수렴

28개 원리가 반복적으로 같은 구조를 가리켰다:

1. **Promise (약속)** — 시스템의 정체성은 구현이 아니라 약속으로 결정된다
   - 프롬프트 문장 → 검증 가능한 불변식
   - 모델이 바뀌어도 약속이 같으면 같은 동료
2. **Attention (주의력)** — 행동의 질은 능력이 아니라 주의력 배치에 의해 결정된다
   - 컨텍스트 윈도우 = 유한한 주의력 예산
   - "더 많이 아는 것"이 아니라 "지금 무엇을 전면에 올리는가"
3. **Relationship (관계)** — 성과 지표는 단일 출력이 아니라 지속 가능한 협력이다
   - 주도권 균형, 경계 일관성, 오류 후 회복
   - 에이전트는 사용자의 가치 함수를 완전히 알 수 없다

수렴 문서: `principles/00-converged.md`

## 4. 8개 시스템 상상 (세션91)

3개 축 × 4개 관점 × 2개 에이전트 = 8개 시스템 설계.

| # | 이름 | 관점 | 에이전트 | 핵심 메타포 | 파일 |
|---|------|------|---------|-----------|------|
| 1 | Covenant (언약) | 순수 과제 | 브로콜리 | 언약 등록부 + 주의력 탐침 + 관계 원장 | `systems/01-covenant-pure-broccoli.md` |
| 2 | Mycelial Dialogue | 생태학자 | 브로콜리 | 토양(약속) + 균사체(주의력) + 수관(관계) | `systems/02-mycelial-eco-broccoli.md` |
| 3 | (이름 없음) | 첫 번째 원리 | 브로콜리 | Promise Register + Attention Budget + Agency Gradient | `systems/03-first-principles-broccoli.md` |
| 4 | Homeostatic Loop | 시스템 사상가 | 브로콜리 | 항상성 + 시상 필터 + 호혜적 교환 | `systems/04-homeostatic-loop-broccoli.md` |
| 5 | Promise Loop | 순수 과제 | 코덱스 | Promise Ledger + Attention Frame + Relationship Memory | `systems/05-promise-loop-codex.md` |
| 6 | Tidal Ecology | 생태학자 | 코덱스 | 기후층 + 근권층 + 종간층 + 퇴적층 | `systems/06-tidal-ecology-codex.md` |
| 7 | **PAR Loop** | 첫 번째 원리 | 코덱스 | Promise Engine + Attention Allocator + Relationship Regulator | `systems/07-par-loop-codex.md` |
| 8 | PRR Loop | 시스템 사상가 | 코덱스 | 유전자 발현 조절 + 에너지 분포 + 반복 상호작용 | `systems/08-prr-loop-codex.md` |

**핵심 발견:** 8개 시스템 모두가 같은 3층 순환 구조로 수렴했다. 메타포는 다르지만 구조가 동일.

종합 문서: `systems/00-synthesis.md`

## 5. PAR Loop 엔진 구현 (세션91)

8개 시스템을 종합하여 PAR Loop을 Python으로 구현했다.

- 엔진 코어: plan() → execute() → audit() 순환
- Gemini 기반 LLM 호출 (plan/audit에서 각 1회)
- lighthouse 어댑터 + 시드 데이터 94개 노드
- REPL 대화형 테스트 환경
- Co-actor Standard v0.2 표준 문서
- Compliance Checker (11/11 통과)
- 15개 유닛 테스트 통과

REPL 테스트 (6턴): 38개 약속 생성, 전부 kept, 위반 0건.

## 6. Co-actor Standard v0.2 (세션91)

PAR Loop의 설계를 표준 문서로 정리:

1. **행동 표준**: Promise Protocol + Identity + Attention Protocol + Relationship Protocol
2. **컨텍스트 표준**: Source Role (4역할) + Source Adapter + Persistent Context Capability + Context Window Assembly
3. **실행 표준**: Turn Pipeline (plan→execute→audit) + Observability + Evaluation

최소 준수 프로파일 8항목 정의.

문서: `CO-ACTOR-STANDARD.md`

## 7. lighthouse 이식 (세션92)

Python 프로토타입을 lighthouse(TypeScript)에 이식.

### 주요 결정
- 별도 서비스 X → lighthouse 내부 TS 모듈
- 기존 오케스트레이션(Phase 0~3 + agent-state) 전면 교체
- LLM 3회/턴: plan(1회) + execute(1회) + audit(1회)
- 도구 선택은 약속이 간접 제어 (기존 Phase 0의 shouldUseTool 제거)
- conversationPhase FSM 제거 → 약속의 자연스러운 산물

### 결과
- PAR 코어 14파일 (`app/server/par/`)
- orchestrator.ts 1360줄 → 670줄
- dev 페이지 PAR 3축 시각화
- 문서 9개(2472줄) → 4개(667줄)
- Co-actor Standard 8/8 준수

## 8. 약속 정리 메커니즘 (세션92)

REPL 테스트에서 6턴에 38개 약속이 누적된 문제를 해결:
- permanent 약속: 절대 제거하지 않음
- situational + kept: 제거 (완료된 약속)
- 중복 판정: predicate 앞 30자 동일 → 최신 것만 유지
- active situational: 최대 10개

---

## 타임라인

| 시점 | 사건 |
|------|------|
| 2026-03 초 | lighthouse 유저 테스트 → "에이전트가 도구처럼 행동" 문제 인식 |
| 세션91 (03-18 오전) | 프롬프트 → 정책 전환, 6관점 원리 추출, 3축 수렴, 8개 시스템 상상 |
| 세션91 (03-18 오전) | PAR Loop Python 엔진 v0.1 구현 + Co-actor Standard v0.2 |
| 세션92 (03-18 오후) | lighthouse TS 이식 (6단계), 문서 통합, 리뷰 |

---

## 다음 단계

- 첫 방문/재방문 분기 PAR 통합
- 시나리오 검증 (의도적 위반 테스트)
- 웹 인터페이스 (브라우저에서 REPL 테스트)
- 실전 배포 + 사내 테스트
