# Co-actor 아키텍처 가이드

> Co-actor를 서비스에 도입할 때의 아키텍처 설계 가이드.
> lighthouse(연구 논문 탐색) 실전 이식 경험에서 도출.

---

## Co-actor가 바꾸는 것

Co-actor를 도입하면 **정책(약속)이 1등 시민이 된다.** 프롬프트에 자유 텍스트로 묻혀 있던 행동 규칙이 검증 가능한 Promise 객체로 독립하고, 매 턴 plan이 구성하고 audit이 검증하는 닫힌 루프가 생긴다.

### 전형적인 LLM 서비스 아키텍처 (도입 전)

```
사용자 메시지
  → 추론 단계: "어떤 도구를 쓸까?" (LLM 또는 규칙)
  → 도구 실행
  → 응답 생성 (LLM, 시스템 프롬프트에 규칙이 자유 텍스트로 포함)
  → 사후 분석 (선택): 대화 상태 기록
  → 저장
```

이 구조의 문제:

1. **정책이 프롬프트에 흩어져 있다** — "선택지를 나열하지 마라"가 시스템 프롬프트 어딘가에 있다. 지켜지는지 검증하지 않는다
2. **도구 선택이 명시적이다** — 추론 단계가 "search를 써라"고 지시. 상황이 복잡해지면 규칙이 폭발한다
3. **피드백 루프가 없다** — 한 턴의 분석 결과가 다음 턴에 영향을 주지 않는다

### Co-actor 도입 후

```
프로파일 ({service}.yaml) — 정책의 단일 원본
  ↓
┌──────────────────────────────────────────────┐
│ PAR Loop (매 턴 순환)                           │
│                                              │
│  plan() ← 약속 스냅샷 + 어댑터 맥락 + 위반 이력  │
│    ↓ 컨텍스트 번들 + agency gradient + 시나리오  │
│  execute() ← 시스템 프롬프트 (약속 주입)         │
│    ↓ 응답 + 도구 결과                           │
│  audit() → 약속 판정 + 도메인 체크리스트 검증     │
│    ↓                                          │
│  state 갱신 → 다음 턴의 plan에 반영             │
└──────────────────────────────────────────────┘
```

---

## 아키텍처 전환 3가지

### 1. 정책의 위치: 프롬프트 → 독립 객체

**전:** 정책이 시스템 프롬프트 텍스트에 묻혀 있다. 변경하려면 코드를 수정하고 배포해야 한다. 지켜지는지 검증할 방법이 없다.

**후:** 정책이 Promise 객체로 독립. YAML 프로파일에 선언하고, plan이 스냅샷하고, execute에 주입하고, audit이 판정한다.

```yaml
# 정책 변경 = YAML 수정. 코드 변경 없음.
permanent_promises:
  - predicate: "검색하지 않은 논문의 인용수를 생성하지 않는다"
    antipattern: '검색 없이 "RoFormer (2021, 인용 4556회)" 같은 수치 제시'
```

이건 인프라에서 설정을 코드에서 분리하는 것과 같은 원리다. 정책 변경의 비용이 배포에서 파일 수정으로 줄어든다.

### 2. 제어 흐름: 명시적 → 선언적

**전:** 추론 단계가 "search를 써라"고 지시 → LLM이 따름. **명령형 제어.**

**후:** plan이 맥락과 약속을 구성 → LLM이 그 위에서 자율 판단. **약속에 의한 간접 제어.**

```
명령형: "사용자가 키워드를 줬으니 search 도구를 사용하라"
선언형: "검색 직후 다음 행동을 밀어붙이지 않는다" (약속)
        → LLM이 상황을 보고 search를 쓸지, 먼저 대화할지 자율 판단
```

도메인이 복잡해질수록 명시적 제어가 불가능해진다. 모든 상황에서 올바른 도구를 선택하는 규칙을 짜는 건 한계가 있다. 약속은 "하면 안 되는 것"만 선언하고, 나머지는 LLM의 판단에 맡긴다. 법이 구체적 행동을 지시하지 않고 경계를 설정하는 것과 같다.

### 3. 피드백 루프: 열린 루프 → 닫힌 루프

**전:** 한 턴의 결과가 다음 턴에 영향 없음. 매 턴 독립.

**후:** audit 위반 → 다음 plan에 전달. 관계 원장 누적. situational promise 생성/정리.

```
턴 N: audit이 "hallucination" 위반 감지
  → 턴 N+1: plan에 "이전 턴 위반: hallucination [major]" 전달
  → plan이 주의력 프레임을 조정
  → execute가 더 보수적으로 응답
```

제어 이론에서 가장 기본적인 개선 — 출력을 측정해서 입력에 되먹인다. Co-actor 도입 전에는 측정(audit) 자체가 없었거나, 측정해도 되먹이지 않았다.

---

## 3-Plane과 Co-actor의 관계

Co-actor Standard의 PAR Loop은 agentic-engineering-principles.md의 3-Plane 아키텍처 중 **Agent Plane**에 해당한다.

| Plane | 역할 | Co-actor 대응 |
|-------|------|--------------|
| **Product Plane** | UX 경험 | 스트리밍 응답, 도구 시각화, dev 페이지의 PAR 모니터링 |
| **Agent Plane** | 정책 집행 | **PAR Loop** — plan/execute/audit, 약속 강제, 관계 추적 |
| **Execution Plane** | 비동기 실행 | 도구 실행, 기억 추출, DB 저장, 임베딩 계산 |

Co-actor는 Agent Plane을 교체한다. Product Plane(UI)과 Execution Plane(도구, DB)은 기존 그대로 유지하고, 중간의 오케스트레이션 계층만 PAR Loop으로 바꾼다.

---

## 도입 시 아키텍처 결정 사항

### 결정 1: PAR Loop의 배치

| 선택지 | 장점 | 단점 | 적합한 경우 |
|--------|------|------|------------|
| **서비스 내부 모듈** | 상태 동기화 불필요, 레이턴시 없음 | 서비스 간 공유 불가 | 단일 서비스 (lighthouse) |
| **공유 라이브러리** | 여러 서비스가 같은 PAR 코어 사용 | 버전 관리 필요 | 2~3개 서비스 |
| **독립 서비스** | 완전 분리, 독립 스케일링 | HTTP 오버헤드, 상태 동기화 | 대규모, 이종 기술 스택 |

lighthouse는 **서비스 내부 모듈**을 선택했다. 코어가 `app/server/par/`에 있고, 어댑터가 `app/server/par/adapters/`에 있다. 추후 다른 서비스가 필요하면 코어를 패키지로 추출할 수 있도록 인터페이스(`SourceAdapter`)를 깨끗하게 유지한다.

### 결정 2: LLM 호출 전략

PAR Loop은 턴당 LLM 3회다 (plan + execute + audit). 비용과 레이턴시를 고려해야 한다.

| 전략 | 설명 | lighthouse 적용 |
|------|------|----------------|
| **모델 분리** | plan/audit에 저비용 모델, execute에 고성능 모델 | 현재 전부 Gemini Flash |
| **선택적 실행** | low-risk turn에서 plan/audit 생략 또는 규칙 기반 대체 | 미적용 (향후) |
| **컨텍스트 정제** | 불필요한 맥락을 줄여 토큰 비용 절감 | 어댑터 결과를 trimContent(1200자)으로 제한 |

가장 효과적인 최적화는 LLM 횟수 축소보다 **컨텍스트 정제**다. 어댑터가 필요 없는 맥락을 보내면 plan/execute 모두에서 비용이 증가한다.

### 결정 3: 상태 관리

PARState에 포함되는 것:
- promises (permanent + situational)
- relationship_ledger (턴별 관계 기록)
- attention_history (턴별 주의력 프레임)
- turn_count, last_audit, ultimate_goal, goal_progress

| 전략 | 설명 | lighthouse 적용 |
|------|------|----------------|
| **JSONB 컬럼** | 간단. 한 컬럼에 전체 state | 현재 사용 (`conversations.agent_state`) |
| **별도 테이블** | 약속, 관계를 독립 테이블로 | 규모 커지면 전환 |
| **인메모리 + 스냅샷** | 빠른 접근, 주기적 저장 | Working Context가 이 방식 |

lighthouse는 JSONB로 시작하고, compactPromises(situational 최대 10개)와 relationship_ledger 최근 5개만 plan에 전달하는 방식으로 크기를 관리한다.

### 결정 4: 어댑터 설계

4역할(identity/memory/knowledge/realtime)은 고정이지만, 각 어댑터의 무게가 다르다.

| lighthouse 어댑터 | 무게 | 데이터 소스 | 레이턴시 영향 |
|-------------------|------|------------|-------------|
| IdentityAdapter | 가벼움 | 프로파일 + 시드 노드 | 낮음 |
| MemoryAdapter | 무거움 | pgvector 임베딩 검색 | **높음** (가장 느림) |
| KnowledgeAdapter | 중간 | Working Context + 최근 문서 | 중간 |
| RealtimeAdapter | 가벼움 | 대화 ID + 포커스 문서 | 낮음 |

4개를 `Promise.allSettled`로 병렬 실행하지만, 가장 느린 어댑터가 전체 plan 레이턴시를 결정한다. 대안:
- 타임아웃 설정 (느린 어댑터는 300ms 후 스킵)
- 단순 턴에서는 identity + realtime만 실행 (fast 모드)

### 결정 5: 프로파일 구조

```yaml
# 최소 (Phase 1만 쓸 때)
identity:
  name: string
  role: string
  permanent_promises: [...]
system_prompt: string
first_visit: string
revisit: string

# 확장 (Phase 2+)
scenarios:
  classification: [...]            # 시나리오 분류
  audit_domain_checklist: [...]    # 도메인 품질 기준
```

프로파일이 점진적으로 확장 가능하도록 설계한다. scenarios가 없으면 범용으로 동작하고, 추가하면 도메인 특화가 활성화된다. **코드 변경 없이 프로파일만 변경해서 도메인 특화 수준을 조절할 수 있다.**

---

## 기존 서비스에 도입하는 실전 가이드

### Step 1: 오케스트레이터 식별

기존 서비스에서 "LLM에게 시스템 프롬프트를 주고 응답을 받는 곳"을 찾는다. 이것이 교체 대상이다.

lighthouse에서는 `orchestrator.ts`의 Phase 0~3이었다 (1360줄). 이걸 PAR Loop으로 교체했다 (670줄).

### Step 2: 프로파일 작성

GETTING-STARTED.md의 Phase 0 질문에 답하고, 답을 YAML로 변환한다. 이 시점에서 서비스 코드는 건드리지 않는다.

### Step 3: PAR 코어 모듈 추가

```
app/server/par/
  schema.ts           # Zod 스키마
  profile-loader.ts   # YAML 로더
  identity.ts         # 정체성 + permanent promises
  adapter.ts          # SourceAdapter 인터페이스
  plan.ts             # plan()
  audit.ts            # audit()
  prompts.ts          # LLM 프롬프트 빌더
  state.ts            # PARState CRUD
  promise-compaction.ts
```

이 파일들은 서비스 독립적이다. 프로파일과 어댑터만 바꾸면 다른 서비스에서도 쓸 수 있다.

### Step 4: 어댑터 구현

4역할 슬롯을 만든다. 처음에는 빈 것이라도 괜찮다.

```
app/server/par/adapters/
  identity.ts    # 프로파일에서 정체성 로드
  memory.ts      # 빈 배열 → Phase 3에서 도메인 데이터 연결
  knowledge.ts   # 빈 배열 → Phase 3에서 도메인 API 연결
  realtime.ts    # 대화 ID 정도
```

### Step 5: 오케스트레이터 교체

기존 오케스트레이터에서:
1. 시스템 프롬프트 구성 부분을 `buildSystemPromptFromPlan()`으로 교체
2. LLM 호출 전에 `plan()` 추가
3. LLM 호출 후에 `audit()` 추가
4. state 저장 추가

**기존 도구와 UI는 그대로 유지한다.** 도구는 Execution Plane이고, Co-actor는 Agent Plane만 교체한다.

### Step 6: 검증

- `tsc --noEmit` 통과
- 매 턴 plan/audit가 실행되는지 확인
- permanent promise가 execute 시스템 프롬프트에 포함되는지 확인
- audit이 의도적 위반을 감지하는지 확인

---

## lighthouse 이식에서 얻은 교훈

1. **"돌아간다" ≠ "작동한다"** — tsc 통과, 매 턴 실행은 "돌아간다". 데이터가 실제로 흘러서 행동에 영향을 미치는 게 "작동한다". 배선 검증은 별도 단계다
2. **이식은 옮기기가 아니라 새로 짜기** — 기존 기능을 하나하나 포팅하지 말고, 새 골격을 세우고 필요한 것만 연결해라
3. **프로파일을 코드에서 분리하라** — 정책 변경의 비용이 배포에서 파일 수정으로 줄어든다
4. **antipattern이 약속의 품질을 결정한다** — 술어만으로는 audit이 위반을 못 잡는다. 구체적 실패 사례가 있어야 한다
5. **배선 명세를 구현 프롬프트에 포함하라** — 각 데이터의 생성→소비 경로를 명시하면 "입구만 뚫고 출구를 안 뚫는" 실수를 방지한다
6. **구현 직후 리뷰를 돌려라** — codex 리뷰에서 "detected_scenario가 프롬프트 계약에 없다"는 High 이슈를 잡았다

---

## 참고

| 문서 | 역할 |
|------|------|
| `CO-ACTOR-STANDARD.md` | 표준 — 무엇을 지켜야 하는가 |
| `GETTING-STARTED.md` | 시작 가이드 — 어떻게 도입하는가 |
| lighthouse `docs/par-loop.md` | 참조 구현 — 실제로 어떻게 작동하는가 |
| mirror-mind `agentic-engineering-principles.md` | 상위 원칙 — 왜 이렇게 설계하는가 |
