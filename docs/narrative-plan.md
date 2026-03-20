# Narrative Plan — 이야기 구성 기반 plan 재설계

> plan이 시나리오를 "분류"하는 대신 이 턴의 "이야기"를 구성한다.
> 검증 후 Co-actor Standard에 반영 예정.

---

## 핵심 아이디어

인간 동료는 상대의 상황을 이야기로 이해한다. "재영이 지금 새 분야에 진입하려고 하는데, 아직 핵심 논문을 못 찾아서 키워드를 바꿔가며 탐색 중이다." 이 이야기에서 다음 행동이 자연스럽게 흘러나온다.

현재 plan은 이야기를 만들지 않는다. 사전 정의된 5개 시나리오 중 하나로 **분류**한다. 분류는 정보를 버리고, 이야기는 정보를 연결한다.

### 분류 vs 이야기

```
분류: detected_scenario = "berry_picking"
  → 정보: "키워드를 바꿔가며 탐색 중" (나머지 맥락 소실)

이야기: "이 연구자는 추천 시스템에서 다양성 문제를 풀려고 한다.
  transformer 기반 접근을 탐색하려는데 아직 핵심 논문을 못 찾았다.
  지난번 contrastive learning 관심과 연결될 수 있다.
  지금은 방향이 열려 있으니 키워드를 해석해서 제안하되 확정하지 않겠다."
  → 정보: 목표 + 현재 상태 + 과거 맥락 + 에이전트의 판단 근거
```

이야기는 다양한 인풋(사용자 메시지, 기억, 맥락, 약속)을 정합성 있는 하나의 서사로 엮는다. 이건 인간의 자연스러운 사고 방식이다.

---

## 현재 plan 구조

```
입력: userMessage + activePromises + recentRelationship + contextItems + scenarios
  ↓
LLM (generateObject)
  ↓
출력 (구조화 JSON):
  attention_frame: { slots, entropy }
  agency_gradient_hint: doing|suggesting|asking
  relationship_constraints: string[]
  detected_scenario: string  ← 분류
```

plan LLM에게 "분류하라, 프레임을 잡아라"고 요청한다. 이야기를 구성하라고 하지 않는다.

---

## 제안: Narrative Plan

### plan의 내부 과정을 바꾼다

```
입력: userMessage + activePromises + recentRelationship + contextItems
  ↓
Step 1: 이야기 구성 (narrative)
  "이 연구자는 ~한 상황이고, ~를 원하고, 내가 할 수 있는 건 ~이다"
  ↓
Step 2: 이야기에서 행동 추출
  attention_frame, agency_gradient, relationship_constraints
  ↓
출력:
  narrative: string          ← 이 턴의 이야기 (1~3문장)
  attention_frame: { ... }
  agency_gradient_hint: ...
  relationship_constraints: [...]
```

### 핵심 변경: narrative 필드 추가

plan 출력에 `narrative` 필드를 추가한다. 이 필드는:

1. **plan LLM이 구조화 출력을 만들기 전에 먼저 이야기를 구성하도록 유도**한다
2. **execute 시스템 프롬프트에 주입**되어, LLM이 "내가 왜 이렇게 행동하는가"를 안다
3. **dev 페이지에서 시각화**되어, 디버깅 시 "plan이 상황을 어떻게 이해했는가"를 볼 수 있다
4. **audit에 전달**되어, "이야기와 실제 행동이 일관되는가"를 검증할 수 있다

### 시나리오의 역할 변화

시나리오는 사라지지 않는다. 역할이 바뀐다:

- **전:** 시나리오가 행동을 결정한다 (berry_picking → suggesting)
- **후:** 시나리오는 이야기의 **어휘**다. plan LLM이 이야기를 구성할 때 참고하는 도메인 용어.

```
시나리오 분류 체계 (이야기 구성 시 참고):
- berry_picking: 키워드를 바꿔가며 탐색, 방향 유동적
- snowballing: 특정 논문에서 인용 추적
- ...

이 용어를 사용해서 이야기를 구성하되, 반드시 하나에 맞출 필요는 없다.
여러 패턴이 섞여 있거나 새로운 패턴이면 그대로 서술하라.
```

이러면 사전 정의에 없는 시나리오도 자연스럽게 처리된다. "이 연구자는 berry picking을 하다가 갑자기 특정 논문의 방법론에 꽂혀서 deep dive로 전환하려 한다" — 이건 분류로는 표현 불가능하지만 이야기로는 자연스럽다.

### situational promise도 이야기에서 나온다

현재: 시나리오 감지 → 해당 시나리오의 사전 정의된 situational_promises 주입
제안: 이야기 구성 → 이야기에서 "이번 턴에서 특히 지켜야 할 것"을 추출

```
이야기: "연구자가 검색 결과를 아직 소화하지 않은 상태인데 추가 키워드를 제안하려 한다.
  지금은 결과 해석에 집중하고, 새 검색은 사용자가 원할 때만."

→ situational promise 추출:
  "이번 턴에서 새로운 검색을 먼저 제안하지 않는다"
```

이건 사전 정의된 템플릿이 아니라, **이야기에서 자연스럽게 도출된 약속**이다.

---

## 구현 계획

### Phase A: plan 프롬프트에 narrative 요청 추가

1. plan 출력 스키마에 `narrative: z.string()` 추가
2. PLAN_SYSTEM에 "먼저 이 턴의 이야기를 1~3문장으로 구성하라" 지시 추가
3. 예시 JSON에 narrative 필드 포함
4. execute 시스템 프롬프트에 narrative 섹션 추가

**검증:** dev 페이지에서 narrative가 표시되는지, 이야기가 맥락을 잘 반영하는지 확인

### Phase B: 시나리오를 분류에서 어휘로 전환

1. plan 프롬프트의 시나리오 섹션을 "분류하라"에서 "참고 어휘"로 변경
2. detected_scenario를 optional로 유지 (이야기의 부산물)
3. situational promise를 시나리오 템플릿 대신 narrative에서 추출하도록 변경

**검증:** 사전 정의에 없는 상황에서도 적절한 이야기가 구성되는지

### Phase C: audit에서 narrative 일관성 검증

1. audit 입력에 narrative 추가
2. "에이전트의 실제 행동이 plan의 이야기와 일관되는가" 검증 항목 추가
3. 일관성 위반 시 attention failure로 분류

**검증:** narrative와 실제 행동이 다른 경우를 audit이 잡는지

### Phase D: Co-actor Standard 반영

lighthouse에서 검증된 후:
1. Co-actor Standard에 narrative plan 개념 추가
2. GETTING-STARTED에 narrative plan 작성법 추가
3. plan 프롬프트 가이드라인에 "이야기 구성 우선" 원칙 추가

---

## Phase B-2: 이야기의 연속성과 변경점 추적

narrative는 한 번에 완성되지 않는다. 턴이 진행되면서 이어지고, 중대한 변경점(turning point)이 생길 때 주목해야 한다.

### 현재 한계

Phase A에서는 매 턴 narrative를 처음부터 만든다. 이전 턴의 이야기를 이어받지 않는다. 인간 동료라면 "아까 여기까지 왔는데, 이제 이쪽으로 가는구나"라고 이어가지, 매번 처음부터 파악하지 않는다.

### 설계

```
PARState에 추가:
  current_narrative: string | null

plan 입력:
  이전 이야기: state.current_narrative
  이번 턴 입력: userMessage + 어댑터 맥락

plan 출력:
  narrative: "이전 이야기를 이어받아 갱신한 이야기"
  narrative_delta: "continuation" | "minor_update" | "turning_point"
  turning_point_description: string (있을 때만)

persist:
  state.current_narrative = planResult.narrative
  if turning_point → trace layer에 기록
```

### 변경점(turning point)의 의미

- 탐색 방향 전환: "diversity → fairness"
- 목표 변경: "survey → 특정 논문 심화"
- 관계 변화: "에이전트 주도 → 사용자 주도로 전환"

turning point는 기억 시스템의 trace layer와 합류한다. trace가 "결정과 발견의 흐름"을 기록하는 층인데, narrative의 turning point가 정확히 이것이다.

### 검증 시점

Phase A를 사내 테스트에서 검증한 후. "plan narrative가 매번 비슷한 이야기를 반복한다"는 패턴이 보이면 — 그게 연속성이 필요하다는 신호다.

---

## Narrative와 PAR 3축의 관계

narrative가 단순한 추가 필드가 아니라 PAR 3축을 관통하는 상위 개념이 될 수 있다.

### 이야기가 각 축에 미치는 영향

**Promise ← narrative: 이야기가 약속을 만든다**

```
narrative: "연구자가 검색 결과 20편을 아직 소화하지 못한 상태다."
→ situational promise: "이번 턴에서 새로운 검색을 먼저 제안하지 않는다"
```

시나리오 템플릿의 사전 정의 약속보다 이야기에서 자연스럽게 도출된 약속이 맥락에 맞다. 같은 berry_picking이라도 상황이 다르면 필요한 약속이 다르다.

**Attention ← narrative: 이야기가 초점을 정한다**

```
narrative: "연구자가 특정 논문에 꽂혔다. 이전 검색 결과는 배경으로 물려야 한다."
→ attention_frame: 해당 논문 relevance 0.95, 검색 결과 relevance 0.3
```

**Relationship ← narrative: 이야기가 관계를 읽는다**

```
narrative: "내가 최근 3턴 동안 점점 더 주도적으로 나갔다. 주도권을 돌려줘야 한다."
→ agency_gradient: asking
→ situational promise: "이번 턴에서 방향을 제안하지 않고 연구자에게 묻는다"
```

### 구조 전환

```
현재:
  Promise ─┐
  Attention ┼─ 독립 계산 → JSON 출력
  Relationship ─┘

궁극:
  입력(맥락, 기억, 관계 이력, 기존 약속)
    → narrative (통합 서사)
      → Promise 도출
      → Attention 추출
      → Relationship 해석
```

3축이 narrative의 파생물이 되는 구조. **narrative가 생성의 1등 시민이고, 3축은 narrative의 구조화된 추출물.**

### 검증에서의 3축 유지

narrative가 생성 과정을 통합하더라도, **검증에서는 3축을 독립적으로 유지**한다. "어느 층에서 실패했는가"를 분류하는 것이 3축의 본래 가치다.

```
생성: narrative → {Promise, Attention, Relationship} 도출
검증: 3축 독립 판정 유지 (실패 분류를 위해)
```

narrative만 있으면 "이야기와 행동이 불일치한다"는 건 알지만, "promise 위반인가 attention 실패인가 relationship 손상인가"를 구분하기 어렵다. audit의 실패 층 분류는 그대로 필요하다.

### Co-actor Standard에 미치는 영향

현재 Standard가 "plan은 3축을 독립적으로 계산한다"인데, narrative 중심으로 바뀌면 "plan은 이야기를 구성하고, 이야기에서 3축을 추출한다"가 된다. 이건 Standard의 핵심 파이프라인 변경이므로, lighthouse에서 충분히 검증한 후 반영해야 한다.

---

## 더 먼 미래: 이야기의 연속성

턴 단위 이야기 → 세션 단위 이야기 → 사용자 단위 이야기.

기억 시스템이 하는 일이 사실 이것이다: 과거의 이야기 조각들을 보관하고, 현재 턴에서 관련된 조각을 활성화해서 이번 턴의 이야기에 엮는 것.

```
이번 턴의 이야기 = 현재 입력 + 활성화된 과거 이야기 조각 + 에이전트의 자기 이해
```

기억이 제공하는 건 데이터가 아니라 **이야기의 재료**다.

---

## Narrative Modes — 검토 결과와 결정

### 5가지 유형
리서치에서 도출된 핵심 유형: situational, intentional, journey, tension, relational.
상세: `specs/research/narrative/00-synthesis.md`

### 태깅 시스템 검토 (브로콜리 + 코덱스 병렬 검토)

**결정: narrative_modes 태깅을 도입하지 않는다.**

이유:
1. "이야기를 만들어놓고 다시 분류하는 건, narrative-plan의 핵심 철학과 모순" (브로콜리)
2. LLM 태깅이 일관되지 않는다 — 같은 narrative에 실행마다 다른 mode 조합
3. audit이 "이 mode가 맞았는가"를 판정할 객관적 기준이 없다
4. 기억 시스템과의 연결 스키마가 미설계
5. 과적합 위험 — decay 메커니즘 없이 초기 신호로 패턴 고정

### 대안: 사후 분석

```
실시간 (plan): narrative 자유 텍스트만 생성. 태깅 안 함.
사후 (세션 종료 후): narrative 텍스트들을 배치 분석하여 패턴 발견.
```

5가지 유형은 **리서치에서 도출된 분석 어휘**로 남긴다. plan LLM에게 태깅을 시키지 않되, 사후 분석에서 "이 대화에서 어떤 유형이 효과적이었는가"를 파악하는 데 사용한다.

### 개성의 발현

프로파일의 weights로 개성을 선언하는 방식은 보류. 대신:
- narrative 자유 텍스트의 **스타일이 자연스럽게 축적**되는 것이 개성
- 프로파일의 system_prompt + permanent_promises + first_visit/revisit이 초기 성향을 결정
- 사용자와의 상호작용에서 narrative 패턴이 기억으로 축적되어 개인화

---

## 근거

- 인간의 사고는 본질적으로 서사적이다 (Narrative Cognition). 흩어진 정보를 인과적 이야기로 엮어서 이해한다.
- 동료 관계에서 "상대의 상황을 이해한다"는 것은 분류가 아니라 이야기 구성이다.
- LLM은 분류보다 서사 구성에 강하다. 구조화 출력을 강제하면 분류기가 되지만, 먼저 이야기를 쓰게 하면 더 풍부한 맥락 이해를 보여준다.
- Co-actor 원칙의 "목적의 내재화"가 바로 이것이다 — 표면 요청 뒤의 궁극적 목적을 이야기로 구성하는 것.
