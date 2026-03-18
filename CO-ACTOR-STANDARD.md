# Co-actor Standard v0.2

> 상태: Draft
> AI 에이전트가 도구가 아니라 동료(Co-actor)로서 동작하기 위한 최소 실행 표준.
> 앞으로 만들어지는 에이전트 시스템은 이 표준을 따른다.
> 기존 시스템은 어댑터를 통해 통합한다.

---

## 0. 기본 정의

이 표준은 세 축을 기준으로 한다.

- **Promise**: 사용자와 에이전트 사이에 형성된 검증 가능한 기대
- **Attention**: 현재 턴에서 전면에 둘 정보와 뒤로 물릴 정보를 결정하는 규율
- **Relationship**: 주도권, 신뢰, 경계, 회복을 포함한 협업 상태

이 표준을 구현하는 시스템은 매 턴 **plan → execute → audit** 순환을 수행해야 한다.

**규범 해석:**
- `MUST`: 필수. 위반하면 Co-actor Standard를 준수하지 않는 것이다.
- `SHOULD`: 강한 권고. 위반 시 근거를 남겨야 한다.
- `MAY`: 선택.
- `MUST NOT`: 금지.

---

## 1. 행동 표준 (Behavioral Standard)

### 1.1 Promise Protocol — 약속 규약

#### 규약
- 에이전트는 모든 지속적 행동 규칙을 자유 텍스트 프롬프트가 아니라 `Promise` 객체로 표현해야 한다 (`MUST`).
- `Promise`는 검증 가능한 술어(predicate)여야 한다. "친절하게" 같은 비검증 표현은 금지한다 (`MUST NOT`).
- 약속은 `permanent`와 `situational` 두 종류로 구분해야 한다 (`MUST`).
- 에이전트는 턴 시작 시 활성 약속 집합을 확정해야 한다 (`MUST`).
- 응답 이후 각 활성 약속의 상태를 `kept | broken | revised | active` 중 하나로 판정해야 한다 (`MUST`).
- 약속이 깨졌을 때는 위반 설명과 증거를 남겨야 한다 (`MUST`).
- 약속 수정은 사용자-에이전트 상호작용에서 새 합의가 생겼을 때만 수행해야 한다 (`SHOULD`).
- permanent 약속은 명시적 재합의 없이 폐기하면 안 된다 (`MUST NOT`).

#### 스키마
```
Promise {
  id: string
  kind: "permanent" | "situational"
  predicate: string              // 검증 가능한 규칙
  rationale?: string             // 왜 이 약속이 존재하는가
  source: {
    type: "identity" | "user_request" | "dialogue_agreement" | "policy"
    turn_id?: string
  }
  scope: {
    conversation_id?: string
    valid_until?: string         // ISO-8601
  }
  status: "active" | "kept" | "broken" | "revised"
  evidence?: string[]
}
```

#### 준수 확인
- 모든 행동 제약이 `Promise` 객체로 추적되는가?
- `predicate`가 실제 출력으로 판정 가능한가?
- `broken` 상태에 근거가 남아 있는가?

---

### 1.2 Identity — 정체성

정체성은 별도의 데이터 구조가 아니다. **정체성 = permanent promise의 집합 + 역할/관점 선언**이다.

#### 규약
- 에이전트의 정체성은 permanent promise를 중심으로 표현된다 (`MUST`).
- 정체성에는 "무엇을 하겠다/하지 않겠다"(약속)와 "어떤 역할과 관점에서 협업하는가"(역할 선언)가 포함된다 (`MUST`).
- 정체성 변경은 명시적 재합의를 거친다. 자동 갱신하지 않는다 (`MUST`).
- 정체성은 모든 턴의 컨텍스트에 포함되어야 한다. 탈락되지 않는다 (`MUST`).

#### 예시
```
정체성 = {
  permanent promises: [
    "연구자의 판단을 대체하지 않는다",
    "근거 없는 단정을 하지 않는다",
    "불확실성을 숨기지 않는다"
  ],
  role: "학술 논문을 함께 탐색하는 연구 동료",
  name: "코르카"
}
```

---

### 1.3 Attention Protocol — 주의력 규약

#### 규약
- 에이전트는 매 턴 명시적 주의력 프레임을 구성해야 한다 (`MUST`).
- 최소 슬롯은 `current_request`, `active_promises`, `evidence`, `relationship_signal` 네 가지여야 한다 (`MUST`).
- 컨텍스트 윈도우에 들어가는 모든 항목은 선택 이유를 가져야 한다 (`MUST`).
- 엔트로피가 임계값을 넘으면 재프레이밍 또는 사용자 확인을 수행해야 한다 (`SHOULD`).
- 현재 목적과 무관한 맥락을 무제한으로 주입하면 안 된다 (`MUST NOT`).

#### 스키마
```
AttentionSlot {
  label: "current_request" | "active_promises" | "evidence" | "relationship_signal"
  content: string
  source_role: ContextSourceRole  // 어떤 소스에서 왔는가
  relevance: number               // 0.0 ~ 1.0
  reason: string                  // 왜 이 슬롯에 이 내용인가
}

AttentionFrame {
  slots: AttentionSlot[]
  entropy: number                 // 0.0 ~ 1.0
  reframe_required: boolean
}
```

#### 준수 확인
- 슬롯 외 항목이 임의 삽입되지 않았는가?
- 엔트로피가 높을 때 실제로 재질문/요약/범위 축소가 일어나는가?

---

### 1.4 Relationship Protocol — 관계 규약

#### 규약
- 에이전트는 주도권 균형을 매 턴 추적해야 한다 (`MUST`).
- 에이전트는 사용자의 최종 판단이 필요한 영역에서 결정을 대행하면 안 된다 (`MUST NOT`).
- 관계 상태에는 최소한 `initiative_balance`, `agency_mode`, `boundary_event`, `recovery_event`가 포함되어야 한다 (`MUST`).
- 오류 발생 시 인정 → 수정 → 경계 재설정 순으로 회복 절차를 남겨야 한다 (`MUST`).
- 에이전트 주도권이 과도하면 질문 또는 옵션 제시 쪽으로 후퇴해야 한다 (`SHOULD`).
- 관계 깊이가 높아질수록 설명은 줄일 수 있지만, 경계는 더 명확해야 한다 (`SHOULD`).

#### 스키마
```
AgencyMode: "doing" | "suggesting" | "asking"

RelationshipEntry {
  turn_id: string
  initiative_balance: number     // -1.0 user-led ~ +1.0 agent-led
  agency_mode: AgencyMode
  trust_signal?: "up" | "flat" | "down"
  boundary_event?: string
  recovery_event?: string
}
```

#### 준수 확인
- 고개인성 판단에서 `doing`이 남발되지 않는가?
- 오류 후 1~2턴 안에 `recovery_event`가 기록되는가?

---

## 2. 컨텍스트 표준 (Context Standard)

### 2.1 Context Source Role — 컨텍스트 소스 역할

에이전트에게 맥락을 공급하는 모든 것은 **소스**다. 기억도 소스의 하나이고, 검색도 소스의 하나다. 소스는 구현 방식(search, db, api)이 아니라 **역할(role)**로 분류한다.

#### 4가지 소스 역할

| 역할 | 정의 | 예시 |
|------|------|------|
| **identity** | 이 에이전트가 누구인가. permanent promises + 역할/관점 선언 | "나는 코르카다", "연구자의 판단을 대체하지 않는다" |
| **memory** | 이전 상호작용에서 축적된 맥락. 관계에서 형성된 것 | 이전 대화에서 합의한 연구 방향, 사용자의 관심 패턴 |
| **knowledge** | 외부 지식. 에이전트 외부에서 온 정보 | 논문 검색 결과, DB 조회, API 응답, 문서 |
| **realtime** | 현재 세션의 라이브 컨텍스트 | 대화 이력, 이번 턴의 도구 출력, 현재 상태 |

#### 규약
- 모든 컨텍스트 항목은 소스 역할(role)이 명시되어야 한다 (`MUST`).
- identity 소스는 매 턴 포함되어야 하며 탈락되지 않는다 (`MUST`).
- memory 소스는 선별 활성화되어야 한다. 전체 dump 주입은 금지한다 (`MUST NOT`).
- memory 소스에는 추가 규범이 적용된다: 출처 추적 가능, 사용자 교정 가능 (`SHOULD`).
- knowledge 소스는 출처(provenance)와 시점(freshness)을 포함해야 한다 (`MUST`).
- 불확실하거나 부분 실패한 소스 응답은 신뢰도와 함께 반환해야 한다 (`MUST`).

#### 스키마
```
ContextSourceRole: "identity" | "memory" | "knowledge" | "realtime"

ContextItem {
  role: ContextSourceRole
  content: string
  provenance?: { source, locator, fetched_at }
  confidence?: number            // 0.0 ~ 1.0
  reason: string                 // 왜 이 항목이 선택되었는가
}
```

---

### 2.2 Source Adapter — 소스 어댑터

소스 역할이 개념적 분류라면, 소스 어댑터는 **구현적 분류**다. 서비스마다 자기 소스에 맞게 어댑터를 구현한다.

#### 규약
- 각 서비스는 자신의 정보 소스에 대한 어댑터를 제공해야 한다 (`MUST`).
- 어댑터는 소스의 구현 세부사항(인증, 페이징, 재시도 등)을 숨기고, 표준 `ContextItem`으로 정규화하여 반환한다 (`MUST`).
- 신규 소스를 붙일 때 엔진 코어를 수정하지 않고 어댑터만 추가 가능해야 한다 (`MUST`).
- 어댑터 실패가 시스템 전체 실패로 전파되지 않는다. 부분 실패로 다뤄진다 (`SHOULD`).

#### 스키마
```
SourceAdapter {
  name: string
  role: ContextSourceRole        // 이 어댑터가 제공하는 역할
  capabilities: ["lookup" | "search" | "verify" | "retrieve"]
  execute(query) → ContextItem[]
}
```

#### 예시: lighthouse 어댑터 구성
```
lighthouse-identity-adapter  → role: identity  (permanent promises + 코르카 역할)
lighthouse-memory-adapter    → role: memory    (기억 시스템 activate.py)
lighthouse-search-adapter    → role: knowledge (Semantic Scholar API)
lighthouse-session-adapter   → role: realtime  (대화 이력 + 작업 컨텍스트)
```

---

### 2.3 Persistent Context Capability — 지속 맥락 능력

기억 시스템은 **필수가 아니라 능력(capability)**이다. 모든 에이전트가 기억 시스템을 가질 필요는 없다. 하지만 동료로서 깊이 있는 협력을 하려면 이전 상호작용을 기억하는 능력이 필요하다.

#### 규약
- 과거 상호작용에서 얻은 지속 맥락을 선택적으로 재사용할 수 있어야 한다 (`SHOULD`).
- 이 능력이 있다면:
  - 회상은 선별 활성화여야 한다. 전체 dump를 주입하지 않는다 (`MUST`).
  - 회상된 항목은 선택 이유(reason)를 가져야 한다 (`MUST`).
  - 회상은 단일 검색 방식(예: 벡터 유사도만)에 의존하지 않는다 (`SHOULD`).
  - 사용자가 잘못된 기억을 교정할 수 있어야 한다 (`SHOULD`).
  - 기억 평가 기준은 검색 정확도가 아니라 대화 자연스러움이다 (`SHOULD`).
- 기억 시스템의 데이터 스키마는 이 표준에서 규정하지 않는다. 서비스별로 자유롭게 설계한다 (`MAY`).

#### 준수 확인
- 기억이 있는 서비스: 전체 dump 없이 선별 활성화되는가? 회상에 이유가 있는가?
- 기억이 없는 서비스: realtime 소스(대화 이력)만으로 표준의 나머지 부분을 준수하는가?

---

### 2.4 Context Window Assembly — 컨텍스트 윈도우 구성

다양한 소스에서 온 맥락을 하나의 컨텍스트 윈도우로 조합하는 규약이다.

#### 규약
- 컨텍스트 윈도우는 소스 역할별로 구분된 슬롯으로 구성한다 (`MUST`).

| 슬롯 | 소스 역할 | 특성 |
|------|----------|------|
| **Identity** | identity | 매 턴 포함. 절대 탈락하지 않는다 |
| **Goal** | realtime (현재 의도) | 세션 내 안정 |
| **Memory** | memory | 턴마다 재계산. 선별 활성화 |
| **Knowledge** | knowledge | 턴마다 변동. 도구 출력/검색 결과 |
| **Dialogue** | realtime (대화 이력) | 누적. 압축 대상 |

- 각 슬롯에 토큰 예산 상한을 설정한다 (`MUST`).
- 슬롯 간 충돌(토큰 초과) 시 보존 우선순위: Identity > Goal > Memory > Dialogue > Knowledge (`MUST`).
- 대화 이력의 점진적 압축을 적용한다 (`SHOULD`).
- 추론 단계와 실행 단계의 컨텍스트를 분리할 수 있다 (`MAY`).

#### 스키마
```
ContextBundle {
  turn_id: string
  slots: {
    identity: ContextItem[]      // permanent promises + 역할
    goal: ContextItem[]          // 현재 의도
    memory: ContextItem[]        // 활성화된 기억
    knowledge: ContextItem[]     // 외부 지식
    dialogue: ContextItem[]      // 대화 이력
  }
  token_budget: { total, used, per_slot }
}
```

#### 준수 확인
- Identity 슬롯이 탈락된 적이 없는가?
- 토큰 초과 시 우선순위에 따라 축소되는가?
- 각 항목이 어떤 소스 역할에서 왔는지 추적 가능한가?

---

## 3. 실행 표준 (Execution Standard)

### 3.1 Turn Pipeline — 턴 처리 파이프라인

#### 규약
- 모든 턴은 **plan → execute → audit** 3단계를 가져야 한다 (`MUST`).
- `plan` 단계: 소스 어댑터에서 맥락을 수집하고, 활성 약속 + 주의력 프레임 + 관계 제약 + 컨텍스트 번들을 산출한다 (`MUST`).
- `execute` 단계: plan이 구성한 컨텍스트 번들로 에이전트가 실행한다. plan 밖의 행동을 할 경우 이유를 기록한다 (`MUST`).
- `audit` 단계: 세 축(약속/주의력/관계)을 각각 평가하고 실패 층을 분류한다 (`MUST`).
- 감사 결과는 다음 턴 상태 갱신에 반영된다 (`MUST`).

```
사용자 턴 진입
    ↓
plan(context)
  - 소스 어댑터로 맥락 수집 (identity + memory + knowledge + realtime)
  - 약속 확정, 주의력 프레임 구성, 관계 제약 도출
  - 컨텍스트 번들 조합
    ↓
execute(context_bundle)
  - 에이전트 실행 (LLM + 도구)
  - 일탈 기록
    ↓
audit(result)
  - 3축 판정 + 실패 층 분류
  - 약속 갱신
    ↓
상태 갱신 → 다음 턴
```

### 3.2 Observability — 관측 체계

#### 규약
- 최소 기록 단위: `turn`, `plan`, `tool_call`, `audit`, `state_transition` (`MUST`).
- 행위뿐 아니라 **판단 이유**를 남겨야 한다 (`MUST`).
- 비용, 지연, 실패, 승인 이벤트를 추적한다 (`MUST`).
- 관측 데이터는 특정 벤더 종속 포맷에 잠기지 않는다 (`SHOULD`).

### 3.3 Evaluation — 평가 체계

#### 규약
- 평가는 `promise`, `attention`, `relationship` 3축으로 수행한다 (`MUST`).
- 점수보다 실패 층 분류와 회복 가능성을 우선한다 (`SHOULD`).
- 관계 품질은 단일 턴이 아니라 다중 턴 추세로 본다 (`MUST`).
- 최소 평가 세트: 약속 위반 탐지, 컨텍스트 과적재/누락, 주도권 침해, 오류 후 회복 (`MUST`).

---

## 4. 최소 준수 프로파일

어떤 서비스가 Co-actor Standard v0.2를 준수한다고 주장하려면:

1. `Promise`, `AttentionFrame`, `RelationshipEntry`를 독립 객체로 유지한다
2. 정체성을 permanent promise + 역할 선언으로 표현하며, 매 턴 컨텍스트에 포함한다
3. 매 턴 `plan`과 `audit`를 수행한다
4. 컨텍스트 소스를 역할(identity/memory/knowledge/realtime)로 분류한다
5. 컨텍스트 윈도우를 명시적 슬롯으로 구성하고 토큰 예산을 관리한다
6. 실패를 `promise | attention | relationship` 중 하나로 분류한다
7. 관측 로그에서 판단 이유와 상태 전이를 재구성할 수 있다
8. 소스 어댑터를 통해 정보를 접근하며, 코어를 수정하지 않고 소스를 추가할 수 있다

---

## 5. 비준수 예시

다음은 이 표준을 위반하는 것이다:

- 시스템 프롬프트에만 규칙이 있고 Promise 객체가 없다
- 정체성이 명시적으로 선언되지 않았거나 턴마다 빠질 수 있다
- 기억을 전체 dump로 주입하고 선택 이유가 없다
- 소스의 역할(identity/memory/knowledge/realtime)이 구분되지 않는다
- 에이전트가 사용자 동의 없이 방향을 결정하는데 이를 추적하지 않는다
- audit 단계가 없거나 생략된다
- 실패를 "낮은 점수"로만 기록하고 어느 층이 깨졌는지 분류하지 않는다
- 소스를 추가하려면 엔진 코어 코드를 수정해야 한다
- 정체성(permanent promise)이 자동 갱신되어 표류한다

---

## 6. 기존 시스템의 통합

이미 존재하는 에이전트 시스템(예: lighthouse)이 이 표준을 따르려면:

1. **소스 어댑터 구현** — 기존 데이터 소스를 4가지 역할로 분류하고, 표준 `ContextItem`으로 감싼다
2. **Promise 마이그레이션** — 기존 프롬프트 규칙을 Promise 객체로 변환한다. permanent/situational을 분류한다
3. **정체성 선언** — permanent promises + 역할/관점을 명시적으로 선언한다
4. **plan/audit 삽입** — 기존 파이프라인의 앞뒤에 Co-actor Engine을 미들웨어로 삽입한다
5. **상태 매핑** — 기존 agent-state를 RelationshipEntry/AttentionFrame으로 매핑한다

엔진이 기존 시스템에 맞추는 것이 아니라, **기존 시스템이 표준에 맞추어 어댑터를 만드는 것**이다.

---

> 이 표준은 mirror-mind의 최상위 철학 — "AI는 도구가 아니라 동료(Co-actor)다" — 을 코드로 강제하기 위해 만들어졌다.
>
> v0.1 → v0.2 변경:
> - 기억 시스템 세부 스키마를 표준에서 제거. 지속 맥락 능력(capability)으로 격상
> - 기억을 소스의 하나로 통합. 소스를 역할(Role)과 어댑터(Adapter) 2층으로 재구성
> - 정체성을 별도 개념에서 "permanent promise + 역할 선언"으로 구체화. Self 기억 개념 제거
