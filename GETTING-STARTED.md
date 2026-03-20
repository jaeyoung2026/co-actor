# Co-actor 시작하기

> LLM을 동료(Co-actor) 에이전트로 빌드하는 가이드.
> 도메인 이해부터 시나리오 주입까지, 단계별로 따라한다.
> lighthouse(연구 논문 탐색) 실전 경험에서 도출.

---

## 빠른 시작 (5분)

```bash
# 설치
pip install co-actor

# 샘플 에이전트와 대화
co-actor chat --profile profiles/writing-coach.yaml

# 나만의 프로파일 생성
co-actor init
```

### 샘플 프로파일

| 프로파일 | 에이전트 | 역할 | 핵심 약속 |
|---------|---------|------|----------|
| `minimal.yaml` | (템플릿) | 최소 출발점 | 사용자 판단 대체 금지 |
| `writing-coach.yaml` | 루미 | 글쓰기 동료 | 글을 대신 고치지 않는다. 왜 어색한지 설명한다 |
| `code-reviewer.yaml` | 데브 | 코드 리뷰 동료 | 코드를 대신 고치지 않는다. 맥락을 먼저 파악한다 |
| `study-buddy.yaml` | 솔 | 학습 동료 | 답을 바로 주지 않는다. 질문으로 안내한다 |
| `product-strategist.yaml` | 피오 | 제품 전략 동료 | 방향을 대신 결정하지 않는다. 전제를 의심한다 |
| `lighthouse.yaml` | 코르카 | 연구 동료 | 연구자의 판단을 대체하지 않는다 |

---

## Phase 0: 도메인 이해

코드 작성 전에 5개 질문에 답한다. 이것이 이후 모든 커스터마이징의 입력이다.

| # | 질문 | lighthouse 답변 (참고) |
|---|------|----------------------|
| 1 | **사용자는 누구이고, 무엇을 성취하려 하는가?** | 새 분야를 탐색하는 연구자, 선행연구를 파악하는 대학원생. 목표: 논문 지형 파악 |
| 2 | **핵심 행동 시나리오는?** (최소 3개) | berry picking, snowballing, triage, deep dive, monitoring |
| 3 | **AI의 최악의 실수는?** | 존재하지 않는 논문 URL 생성, 연구 방향 단정, 논문 관계 오인 |
| 4 | **사용자의 판단 경계는?** | 연구 방향 선택, 논문 가치 평가, 분석 관점 결정 |
| 5 | **도메인 데이터 소스와 신뢰도?** | Semantic Scholar API. 프리프린트 < 피어리뷰 < 고인용 저널 |

---

## Phase 1: 최소 viable Co-actor

**목표:** "도메인을 아는 척하지 않는 정직한 동료". 범용이지만 약속을 지킨다.

### Step 1 — 프로파일 작성

Phase 0 답변을 YAML로 변환한다.

```yaml
# profiles/{service}.yaml
identity:
  name: "에이전트 이름"
  role: "역할을 한 문장으로"
  permanent_promises:
    # 질문 3 → 최악의 실수를 방지하는 약속
    - predicate: "검증 가능한 술어"
      rationale: "이 약속이 존재하는 이유"
      antipattern: "구체적 실패 사례"
    # 질문 4 → 판단 경계
    - predicate: "사용자의 최종 판단을 대행하지 않는다"
      rationale: "에이전트는 사용자의 가치 함수를 완전히 알 수 없다"

system_prompt: |
  너는 {name}이다. {role}다.
  약속 섹션의 permanent promise를 반드시 따른다.

first_visit: |
  처음 만나는 사람이다. 자기소개 후 한 가지만 묻는다.

revisit: |
  이전에 대화한 적이 있다. 기억을 활용해 이어간다.
```

**좋은 약속 작성법:**

```yaml
# ✗ 검증 불가 — audit이 판정할 수 없다
- predicate: "친절하게 답한다"

# ✓ 검증 가능 — audit이 위반을 감지할 수 있다
- predicate: "사용자의 최종 판단을 대체하지 않는다"
  antipattern: '"이 논문이 가장 적합합니다" 같은 단정'
```

약속 설계 질문:
- **이 에이전트가 하면 안 되는 것은?** → "대신 결정하지 않는다"
- **도구와 동료의 차이가 드러나는 순간은?** → "왜 그런지 설명한다"
- **이 약속이 깨지면 사용자가 어떤 경험을 하는가?** → rationale

### Step 2 — 소스 어댑터 4개

4역할(identity/memory/knowledge/realtime) 슬롯을 만든다. 빈 것이라도 인터페이스를 갖춘다.

```python
# Python (co-actor 엔진)
from co_actor import CoActor

class MyIdentityAdapter:
    role = "identity"
    def execute(self, query: str) -> list[dict]:
        return [{"role": "identity", "content": "에이전트 정체성", "reason": "기본"}]

class MyMemoryAdapter:
    role = "memory"
    def execute(self, query: str) -> list[dict]:
        return []  # Phase 3에서 도메인 데이터 연결
```

```typescript
// TypeScript (lighthouse 방식)
export class IdentityAdapter implements SourceAdapter {
  role = "identity" as const;
  async execute(query: string): Promise<ContextItem[]> {
    const profile = loadProfile();
    return [{
      role: "identity",
      content: `${profile.identity.name}: ${profile.identity.role}`,
      reason: "에이전트 기본 정체성",
      confidence: 1,
    }];
  }
}
```

### Step 3 — PAR Loop 연결

```python
# Python — co-actor 엔진 사용
from co_actor import CoActor

agent = CoActor.from_profile("profiles/my-agent.yaml")
conv = agent.conversation("session-001")
response = conv.turn("안녕하세요")

print(response.output)              # 에이전트 응답
print(response.audit.promise_kept)   # 약속 준수 여부
print(response.audit.failure_layer)  # 실패 시 어느 층인가
```

### Step 4 — 준수 검증

```bash
co-actor compliance --profile profiles/my-agent.yaml
```

**Phase 1 완료 기준:** 매 턴 plan/audit가 실행되고, permanent promise가 시스템 프롬프트에 주입되며, audit이 위반을 감지할 수 있는 상태.

---

## Phase 2: 시나리오 주입

Phase 0의 질문 2(행동 시나리오)를 코드에 내린다.

### Step 1 — 프로파일에 scenarios 추가

```yaml
scenarios:
  classification:
    - name: berry_picking
      signal: "키워드를 바꿔가며 탐색, 방향 유동적"
      agency_default: suggesting
      situational_promises:
        - "키워드 변경을 제안할 때 변경 이유를 명시한다"
    - name: snowballing
      signal: "특정 논문의 참조/인용을 따라 확장"
      agency_default: doing
      situational_promises:
        - "backward와 forward 방향을 혼동하지 않는다"

  audit_domain_checklist:
    - "검색 결과에 없는 논문의 메타데이터를 생성했는가"
    - "논문의 방법론이나 기여를 틀리게 설명했는가"
```

### Step 2 — plan/audit 프롬프트에 주입

코드가 프로파일의 scenarios를 읽어서 LLM 프롬프트에 자동 주입한다. scenarios가 없으면 주입하지 않으므로 점진적 확장이 가능하다.

**핵심 연결:** plan이 `detected_scenario`를 출력하면, orchestrator가 해당 시나리오의 `situational_promises`를 PAR state에 자동 주입한다. 이 약속들은 execute 시스템 프롬프트의 "이번 대화의 약속" 섹션에 포함되어 LLM의 실제 행동을 제약한다.

```
plan(detected_scenario: "berry_picking")
  → state에 "키워드 변경 시 이유 명시" 약속 주입
  → execute 시스템 프롬프트에 해당 약속 포함
  → audit이 해당 약속 위반 여부 판정
```

---

## Phase 3+: 어댑터 심화 → Audit 강화 → 피드백 루프

1. **어댑터 심화** — 도메인 API 연결, 기억 노드 타입, 세션 상태
2. **Audit 강화** — 실전 데이터에서 발견된 실패를 audit에 반영
3. **피드백 루프** — 실전 로그 분석 → promise/adapter/prompt 반복 개선

---

## lighthouse 적용 사례

lighthouse(연구 논문 탐색 동료 에이전트)가 Co-actor를 구체적으로 어떻게 적용했는지 상세히 설명한다. 2090줄, 18개 파일의 실제 구현이다.

### 아키텍처 개요

```
사용자 메시지
  → parseAndPersistInput (메시지 DB 저장)
  → turn-manager 획득 (동시 턴 방지 FSM)
  │
  → PAR plan() — Gemini 1회 (generateObject)
  │   ├─ 4개 소스 어댑터 병렬 호출 (행동 로그 + 시간 경과 포함)
  │   ├─ 이야기 구성 (narrative) — 사용자 상황을 1~3문장 서사로
  │   ├─ 이야기에서 약속 도출 (narrative_promises)
  │   ├─ 활성 약속 스냅샷 + 시나리오 감지 (detected_scenario)
  │   ├─ 주의력 프레임 (4슬롯 + entropy)
  │   ├─ agency gradient 힌트
  │   └─ 컨텍스트 번들 (5슬롯 + 토큰 예산)
  │
  → execute() — Gemini 1회 (streamText)
  │   ├─ plan의 컨텍스트 번들 → 시스템 프롬프트로 합성
  │   ├─ "이번 턴의 이야기" 섹션 주입 (narrative)
  │   ├─ permanent + situational + narrative_promises 주입
  │   ├─ first-visit/revisit 분기 (사용자 기준)
  │   ├─ 도구 6개 (search, analyze, inspect, recall, write, propose)
  │   └─ LLM이 약속 가드레일 안에서 자율 판단
  │
  → PAR audit() — Gemini 1회 (generateObject)
  │   ├─ 약속 판정 (kept/broken) + antipattern 대조
  │   ├─ 도메인 체크리스트 검증 + tool output 요약 대조
  │   ├─ narrative-행동 일관성 검증
  │   ├─ 주의력 적절성 평가
  │   ├─ 관계 진단 (initiative_balance, agency_mode)
  │   ├─ 실패 층 분류 (promise/attention/relationship)
  │   ├─ 새 situational promise 추출
  │   └─ 위반 이력 → 다음 턴 plan에 피드백
  │
  → persist (DB 저장 + 기억 추출)
```

턴당 LLM 3회. 기존 Phase 0~3 (4회)보다 1회 적다.

### 프로파일 — lighthouse.yaml (128줄)

프로파일이 에이전트의 정체성, 약속, 시스템 프롬프트, 시나리오의 **단일 원본**이다. 코드는 이 파일을 읽어서 사용한다.

```yaml
identity:
  name: "연구 동료"           # 사용자별 커스텀 이름으로 오버라이드 가능
  role: "학술 논문을 함께 탐색하는 연구 동료"

  permanent_promises:         # 9개, 도메인 고유
    # 판단 경계 (2개)
    - predicate: "연구자의 최종 판단을 대행하지 않는다"
      antipattern: '"이 논문이 가장 적합합니다" 같은 단정'
    - predicate: "검색하지 않은 논문의 URL이나 인용수를 생성하지 않는다"
      antipattern: '검색 없이 "RoFormer (2021, 인용 4556회)" 같은 구체적 수치'
    # 응답 형식 (3개)
    - predicate: "자기 방향을 먼저 제시하고 동의를 구한다. 선택지를 2개 이상 나열하지 않는다"
    - predicate: "사용자가 짧게 답하면 짧게 응답한다"
    - predicate: "보조적 톤(~해드릴게요)을 사용하지 않는다"
    # 도구 사용 (3개)
    - predicate: "검색 직후 다음 행동을 밀어붙이지 않는다"
    - predicate: "propose는 실질적 판단이 필요할 때만 사용한다"
    - predicate: "사용자가 명시한 제외 기준에 해당하는 논문을 추천하지 않는다"
    # 목표 (1개)
    - predicate: "도구 결과를 나열하는 데서 멈추지 않는다. 해석을 덧붙인다"

scenarios:
  classification:             # 5개 연구 행동 시나리오
    - name: berry_picking     # suggesting — 방향 유동적
    - name: snowballing       # doing — 인용 추적 자동
    - name: triage            # doing — 대량 필터링
    - name: deep_dive         # suggesting — 분석 관점 확인
    - name: monitoring        # doing — 정기 확인
  audit_domain_checklist:     # 4개 연구 도메인 품질 기준
    - "검색 결과에 없는 논문 메타데이터를 생성했는가"
    - "논문 간 인용 관계를 잘못 주장했는가"
    - "연구 분야 범위를 벗어난 추천을 했는가"
    - "방법론/기여를 틀리게 설명했는가"

system_prompt: |              # execute에 주입
  너는 논문을 검색해주는 도구가 아니라, 연구자와 함께 연구를 탐색하는 동료다.
  ...

first_visit: |               # turn_count=0 + 사용자의 첫 대화
  에이전트가 먼저 자기를 소개한다. 한 가지만 묻는다.

revisit: |                    # 기존 사용자
  기억에 있는 프로필은 다시 묻지 않는다.
```

### 소스 어댑터 4개 — 도메인 데이터를 PAR에 연결

| 어댑터 | 역할 | 데이터 소스 | 코드 |
|--------|------|------------|------|
| **IdentityAdapter** | identity | 프로파일 정체성 + permanent promises + 시드 self 노드 | `adapters/identity.ts` 53줄 |
| **MemoryAdapter** | memory | pgvector 임베딩 검색 + 강한 fact/intention 노드 + 활성 목표 | `adapters/memory.ts` 78줄 |
| **KnowledgeAdapter** | knowledge | Working Context (세션 내 도구 결과) + 최근 워크스페이스 문서 | `adapters/knowledge.ts` 57줄 |
| **RealtimeAdapter** | realtime | 대화 ID + 포커스 문서 + 행동 로그 + 시간 경과 | `adapters/realtime.ts` 90줄 |

**IdentityAdapter** — 매 턴 무조건 포함:
```typescript
// 1. 에이전트 정체성 (사용자별 커스텀 이름 지원)
const identity = await getAgentIdentityForUser(userId);
// 2. 9개 permanent promises → ContextItem으로 변환
buildPermanentPromises().map(p => ({ content: p.predicate }))
// 3. 시드 self 노드 — 코르카의 자기 이해
const selfNodes = await loadSelfNodes(GLOBAL_SEED_OWNER_ID);
```

**MemoryAdapter** — 3개 소스를 병렬 활성화:
```typescript
const [activation, semanticNodes, activeGoals] = await Promise.all([
  activateMemory(query, userId),      // pgvector 임베딩 검색 + 다중 인덱스 점수 합산
  loadStrongSemanticNodes(userId),    // encoding_depth가 높은 fact/intention
  loadActiveGoals(userId),            // 진행 중인 연구 목표
]);
// 각 노드의 score가 confidence로 전달되어 plan이 중요도를 판단
```

**KnowledgeAdapter** — 세션 내 작업 맥락:
```typescript
// 1. Working Context — 도구 결과가 자동으로 쌓이는 세션 버퍼 (30분 TTL)
const entries = WorkingContextStore.getEntries(conversationId);
// 2. 최근 워크스페이스 문서 — 사용자의 검색/분석/메모 결과
const recentDocuments = await listRecentDocumentsUnchecked(userId, 5);
```

### plan → execute → audit 실제 흐름

**plan (plan.ts 208줄):**

```typescript
// 1. 4개 어댑터 병렬 호출로 맥락 수집
const collected = await collectContext(userMessage, adapters, signal, userId);
// 2. 컨텍스트 번들 구성 (5슬롯 + 토큰 예산)
const context_bundle = buildContextBundle(state, userMessage, collected);
// 3. LLM에게 주의력 프레임 + agency gradient + 관계 제약 + 시나리오 판단 요청
const result = await generateObject({ schema: planResponseSchema, ... });
// 출력: attention_frame, agency_gradient_hint, relationship_constraints, detected_scenario
```

**execute (orchestrator.ts):**

```typescript
// 1. 시나리오 감지 시 → situational promises 자동 주입
if (planResult.detected_scenario) {
  const scenario = profile.scenarios.classification.find(s => s.name === planResult.detected_scenario);
  for (const predicate of scenario.situational_promises) {
    parState.promises.push({ kind: "situational", predicate, status: "active", ... });
  }
}

// 2. 시스템 프롬프트 합성 (13개 섹션)
//    identity → 약속(permanent + situational) → 초점 → 기울기 → 관계 제약
//    → 기억 → 목표 → 지식 → 대화 맥락 → 첫만남/재방문 → 기본 프롬프트
const systemPrompt = buildSystemPromptFromPlan(planResult, agentName, isFirstVisit);

// 3. 스트리밍 + 도구 6개 (LLM 자율 판단, 약속이 가드레일)
const response = streamText({
  model: google(GEMINI_MODEL),
  system: systemPrompt,
  tools: createMainTools(conversationId, turn, userId, signal),
  stopWhen: [hasToolCall("search"), hasToolCall("analyze"), ...],
});
```

**audit (audit.ts 53줄):**

```typescript
// 1. 활성 약속 + antipattern 대조
// 2. 도구 실행 결과 요약 전달 (summarizeToolResult 재사용)
// 3. 도메인 체크리스트 주입 (lighthouse.yaml에서 읽음)
// 4. 이전 턴 위반 이력 → plan에 피드백 (반복 방지)
const auditResult = await audit(parState, userMessage, allText, toolsUsed, signal, toolOutputSummaries);
// 출력: promise_kept, violations, new_promises, relationship_entry, failure_layer
```

**persist:**

```typescript
// 1. PAR state 갱신 (새 약속 추가 + compaction + 관계 원장 + 주의력 이력)
parState.promises.push(...auditResult.new_promises);
parState.promises = compactPromises(parState.promises);  // situational max 10개
parState.relationship_ledger.push(auditResult.relationship_entry);
// 2. turn_decisions 테이블에 plan/audit 결과 저장
// 3. fire-and-forget 기억 추출 (extractAndSaveTurnNodes)
```

### 약속 생애주기

```
permanent promise (9개, 프로파일에서 로드)
  → 매 턴 plan.promise_snapshot에 포함
  → execute 시스템 프롬프트에 주입
  → audit이 매 턴 판정 (kept/broken)

situational promise (시나리오 감지 또는 audit 추출)
  → plan이 detected_scenario 출력
  → orchestrator가 해당 시나리오의 situational_promises를 state에 주입
  → execute 시스템 프롬프트의 "이번 대화의 약속" 섹션에 포함
  → audit이 판정
  → compactPromises: kept → 제거, active → 최대 10개 유지
```

### first-visit / revisit 판정

```typescript
// 대화 기준이 아니라 사용자 기준
let isFirstVisit = parState.turn_count === 0;
if (isFirstVisit && userId) {
  const prevCount = await countPreviousConversationsUnchecked(userId, conversationId);
  if (prevCount > 0) isFirstVisit = false;  // 기존 사용자면 revisit
}
```

### 파일 맵

```
profiles/
  lighthouse.yaml              # 정본 — 정체성, 약속, 시나리오, 프롬프트

app/server/par/
  schema.ts          141줄    # Zod 스키마 — Promise, AttentionFrame, RelationshipEntry, PARState, PlanResult, AuditResult
  profile-loader.ts   50줄    # YAML 로더 (캐싱)
  identity.ts         33줄    # AGENT_IDENTITY + buildPermanentPromises
  adapter.ts           7줄    # SourceAdapter 인터페이스
  plan.ts            208줄    # plan() — 맥락 수집, 컨텍스트 번들, LLM 판단
  audit.ts            53줄    # audit() — 3축 판정
  prompts.ts         235줄    # PLAN_SYSTEM, AUDIT_SYSTEM, 프롬프트 빌더
  state.ts            78줄    # PARState CRUD (conversations.agent_state JSONB)
  promise-compaction.ts 37줄  # situational 최대 10개 유지
  index.ts             8줄    # barrel export

app/server/par/adapters/
  identity.ts         53줄    # 정체성 + permanent promises + self 노드
  memory.ts           78줄    # 임베딩 검색 + 강한 노드 + 목표
  knowledge.ts        57줄    # Working Context + 최근 문서
  realtime.ts         43줄    # 대화 ID + 포커스 문서
  index.ts             4줄    # barrel export

app/server/agent/
  orchestrator.ts    819줄    # 메인 파이프라인 — plan→execute→audit→persist
  system-prompt.ts    58줄    # 기본 시스템 프롬프트
```

---

## 도메인 특화의 5개 접점

| 접점 | 커스터마이징 대상 | 설계 질문 |
|------|-----------------|----------|
| **Promise** | permanent + antipattern + situational template | AI의 최악 실수는? 판단 경계는? |
| **소스 어댑터** | 4역할에 도메인 데이터 매핑 | 핵심 데이터 소스는? 기억할 것은? |
| **Plan 프롬프트** | 시나리오 분류 + agency gradient | 사용자 행동 패턴은? |
| **Audit 체크리스트** | 도메인 할루시네이션 + 품질 기준 | 도메인 고유 실패 유형은? |
| **Co-actor Profile** | 위 4개를 하나의 YAML에 선언 | — |

### 프로파일 전체 구조

```yaml
# 필수 (Phase 1)
identity:
  name: string
  role: string
  permanent_promises:
    - predicate: string
      rationale: string
      antipattern: string

system_prompt: string
first_visit: string
revisit: string

# 선택 (Phase 2+)
scenarios:
  classification:
    - name: string
      signal: string
      agency_default: doing|suggesting|asking
      situational_promises: string[]
  audit_domain_checklist: string[]
```

---

## CLI 참조

```bash
co-actor chat --profile profiles/my-agent.yaml     # 대화
co-actor repl --profile profiles/my-agent.yaml      # REPL (plan/audit 실시간 확인)
co-actor init                                        # 대화형 프로파일 생성
co-actor compliance --profile profiles/my-agent.yaml # 준수 검증
co-actor serve --port 8100                           # HTTP API 서버
```

---

## 튜닝 가이드

| 증상 | 원인 | 해결 |
|------|------|------|
| `promise_kept`가 항상 `true`인데 대화가 딱딱 | 약속이 너무 세밀 | 상위 수준으로 합치기 |
| `relationship_strengthened`가 자주 `false` | 주도권 관련 약속 부족 | 약속 추가 |
| `attention_appropriate`가 흔들림 | entropy 높음 (컨텍스트 과적재) | 어댑터 top_k 줄이기 |
| `agency_gradient`가 계속 `doing` | 에이전트 과도 주도 | `suggesting`/`asking` 유도 약속 추가 |

---

## 체크리스트

### Phase 0
```
[ ] 5개 질문에 답했는가
```

### Phase 1
```
[ ] {service}.yaml 프로파일 존재
[ ] permanent promise 최소 3개 (도메인 고유)
[ ] 각 promise에 antipattern
[ ] 소스 어댑터 4개 구현
[ ] PAR Loop 매 턴 동작
[ ] first_visit / revisit 분기 작동
[ ] compliance 검증 통과
```

### Phase 2
```
[ ] 시나리오 문서 존재
[ ] scenarios.classification 프로파일에 선언
[ ] 시나리오별 agency_default 설정
[ ] 시나리오별 situational_promises 존재
[ ] plan 프롬프트에 시나리오 주입
[ ] audit_domain_checklist 프로파일에 선언
[ ] audit 프롬프트에 도메인 체크리스트 주입
```

### Phase 3+
```
[ ] KnowledgeAdapter 도메인 해석 규칙
[ ] MemoryAdapter 도메인 기억 노드
[ ] RealtimeAdapter 도메인 세션 상태
[ ] 실전 로그 기반 피드백 루프
```

---

## 참고 파일

| 파일 | 역할 |
|------|------|
| `README.md` | 프로젝트 개요 — 철학, PAR Loop, 아키텍처 |
| `CO-ACTOR-STANDARD.md` | 표준 문서 — 뭘 지켜야 하는가 |
| `docs/architecture-guide.md` | 아키텍처 가이드 — 서비스에 도입할 때 |
| `docs/narrative-plan.md` | Narrative Plan — 이야기 구성 기반 plan 설계 |
| `docs/research/narrative/00-synthesis.md` | Narrative 리서치 종합 — 5가지 유형 + 공통 메커니즘 |
| `profiles/` | 샘플 프로파일 — 복사해서 시작 |
| lighthouse 저장소 `app/server/par/adapters/` | 참고 어댑터 구현 (TS) |
