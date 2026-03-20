# Narrative 구성 방식 리서치 — 종합

> 7개 에이전트(브로콜리 3 + 코덱스 4) 병렬 리서치 결과를 취합하여 핵심 유형을 선별.
> 날짜: 2026-03-20 (세션94)

---

## 리서치 소스

| # | 에이전트 | 관점 | 파일 |
|---|---------|------|------|
| 1 | 브로콜리 | Cognitive Science | 01-cognitive-science-broccoli.md |
| 2 | 브로콜리 | UX/서비스 디자인 | 02-ux-design-broccoli.md |
| 3 | 브로콜리 | 게임/스토리텔링 | 03-game-storytelling-broccoli.md |
| 4 | 코덱스 | Cognitive Science | 04-cognitive-science-codex.md |
| 5 | 코덱스 | 종합 | 05-comprehensive-codex.md |
| 6 | 코덱스 | UX/서비스 디자인 | 06-ux-design-codex.md |
| 7 | 코덱스 | 게임/스토리텔링 | 07-game-storytelling-codex.md |

---

## 핵심 유형 선별: 5가지 narrative 방식

7개 리서치에서 수집된 30개 이상의 방식을 중복 제거하고, AI 동료 에이전트에 실제로 의미 있는 유형으로 수렴했다.

### 1. 상황 서술 (Situational)

**핵심 질문:** "지금 무슨 일인가?"

**인지적 근거:**
- Endsley Situation Awareness Level 1-2 (Perception → Comprehension)
- JTBD의 situation-based design ("상황이 행동을 결정한다")
- Grice의 협력 원칙 (필요한 만큼만, 관련 있게, 명확하게)

**메커니즘:** 관찰 가능한 사실을 중심으로 사용자의 상태와 요구를 기술. 해석을 최소화하고 데이터에 충실.

**예시:**
> "연구자가 diversity-accuracy tradeoff 논문을 요청했다. 3일 전 fairness 탐색 이력이 있고, diversity metrics 정리 약속이 미이행 상태다."

**에이전트 행동:** 안정적이고 예측 가능한 응답. 사실 기반. 오해석 위험 최소.

**적합한 상황:** 단순 요청, 첫 대화, 정확성이 중요한 도메인 (의료, 금융)

**장점:** 오류 비용 낮음, audit 용이, 구현 단순
**단점:** 깊이 없음, 맥락 연결 약함, "도구" 느낌

---

### 2. 의도 추론 (Intentional)

**핵심 질문:** "왜 이걸 원하는가?"

**인지적 근거:**
- Bruner의 Narrative Mode (의도와 동기 귀속, 모호성 수용)
- 화용론의 함축 이론 (표면 발화 아래의 실제 의도)
- Klein의 Data-Frame (데이터에서 프레임을 추론)
- Kahneman System 2 (의도적 추론)

**메커니즘:** 표면 요청 아래의 궁극적 목적을 추론. "왜 이것을 지금 묻는가?"에 집중. 잠정적 가설을 세우고 확인을 구함.

**예시:**
> "diversity-accuracy tradeoff를 찾는 건 3일 전 fairness 탐색의 연장일 수 있다. 실제로는 fairness-aware 추천 시스템의 전체 landscape를 파악하려는 것 같다. 확인이 필요하다."

**에이전트 행동:** 통찰 제공, 해석 공유 후 동의 구함. "제가 보기에는 ~인 것 같은데, 맞나요?"

**적합한 상황:** 모호하거나 넓은 요청, 반복 탐색, 깊은 관계가 형성된 후

**장점:** 높은 부가가치, 동료 느낌, 목적의 내재화(Co-actor 원칙 1)
**단점:** 오추론 시 신뢰 급락, agency_gradient를 suggesting으로 강제해야 안전

---

### 3. 여정 추적 (Journey)

**핵심 질문:** "어디서 와서 어디로 가는가?"

**인지적 근거:**
- McAdams의 Narrative Identity (과거-현재-미래를 연결하는 자기 서사)
- Redemption/Contamination Sequence (정서 궤적의 방향)
- Journey Mapping (UX)
- String of Pearls (게임 내러티브)
- Weick의 Retrospective sensemaking (행동 후 의미 부여)

**메커니즘:** 시간축 위에 과거 맥락, 현재 상태, 예상 다음 단계를 배치. 연속성과 축적감 강조.

**예시:**
> "이 연구자는 3일 전 fairness 탐색에서 시작해 diversity 측면으로 확장하고 있다. diversity metrics 정리가 미완이므로, 이번 검색을 기존 맥락과 연결하면 자연스러운 다음 단계다."

**에이전트 행동:** 과거 맥락 자연스럽게 복원, 미이행 약속 상기, 다음 단계 선제 제안.

**적합한 상황:** 장기 프로젝트, 재방문, 다단계 탐색

**장점:** 연속성, 축적감, 기억 시스템과 직접 연결
**단점:** 새 주제 시작 시 과거에 끌려감, 기억 의존도 높음

---

### 4. 긴장 포착 (Tension)

**핵심 질문:** "무엇이 충돌하는가?"

**인지적 근거:**
- Klein의 Reframing (프레임-데이터 불일치 시 전환)
- PbtA GM Moves ("Announce future badness", "Put someone in a spot")
- 드라마투르기의 갈등 구조
- Pennebaker의 인과어+통찰어 증가 패턴

**메커니즘:** 사용자 요구와 현재 상황 사이의 간극, 모순, 리스크를 식별. 갈등이 에이전트 행동의 동기가 됨.

**예시:**
> "diversity-accuracy tradeoff 논문을 원하지만, diversity metrics 정리가 미완이라 검색 결과를 온전히 활용하기 어려울 수 있다. 검색을 수행하되 이 간극을 짚는다."

**에이전트 행동:** 문제를 명시적으로 짚고, 해결 방향을 제안. "한 가지 주의할 점이 있는데..."

**적합한 상황:** 복잡한 의사결정, 코드 리뷰, 리스크가 있는 도메인

**장점:** 판단력 발휘, reframing 능력, 발전적 마찰(Co-actor 원칙 3)
**단점:** 단순 요청에 과잉 적용 시 피로감, 부정적 프레이밍 인상

---

### 5. 관계 의식 (Relational)

**핵심 질문:** "우리 사이에서 무엇이 중요한가?"

**인지적 근거:**
- Weick의 Identity 속성 ("내가 누구인가"가 해석을 결정)
- Coaching의 Working Alliance (목표 합의, 과업 합의, 정서적 유대)
- Schank의 Script/Role 이론 (역할 기반 행동)
- Affective Computing (감정 인식이 프레이밍을 바꿈)
- 서비스 블루프린트의 Frontstage/Backstage (투명성 조절)

**메커니즘:** 에이전트와 사용자의 관계 상태(주도권, 신뢰, 약속)를 중심으로 이야기를 구성. 역할 분담 포함.

**예시:**
> "지난번에 diversity metrics 정리를 약속했는데 아직 못 했다. 이번 턴에서 이 약속을 언급하고, 검색과 함께 정리를 시작할지 물어본다."

**에이전트 행동:** 약속 이행 추적, 주도권 조절, 관계 변화 인식. "지난번에 제가 ~라고 했었는데..."

**적합한 상황:** 약속이 있는 상태, 주도권 전환이 필요할 때, 장기 관계

**장점:** 신뢰 구축, Promise 축과 직접 연결, 동료 관계 강화
**단점:** 초기 관계에서 공허, 과도한 메타 대화 위험

---

## 공통 메커니즘 (모든 유형에 적용)

5가지 유형이 "무엇에 초점을 맞추는가"라면, 공통 메커니즘은 "어떻게 이야기를 진행하는가"다.

| 메커니즘 | 출처 | 역할 |
|---------|------|------|
| **수용+확장 (Yes, and)** | Improv | 사용자 발화를 부정하지 않고 확장. 기본 대화 원칙 |
| **프레임 유지/교체** | Klein Data-Frame | 이야기가 유효한 동안 정교화, 불일치 시 교체 |
| **관점 전환** | Pennebaker | 자기 판단 → 사용자 관점 → 재통합. 3단계 |
| **궤적 모니터링** | McAdams | 대화의 전체 방향(상승/하강)을 추적 |
| **선택적 투명성** | Service Blueprint | 판단 과정을 상황에 따라 드러내거나 숨김 |
| **이정표+자유구간** | String of Pearls, Fronts/Clocks | 핵심 체크포인트 사이를 자유롭게 |

---

## Narrative 방식 = 에이전트의 개성

5가지 유형의 **비율(weight)**이 에이전트의 개성을 결정한다.

```yaml
# lighthouse 코르카 — 의도 추론 + 여정 추적 중심
narrative:
  weights:
    intentional: 0.35    # "왜 이걸 찾으시는 거예요?"
    journey: 0.30        # "지난번에 이어서..."
    situational: 0.15    # 사실 기반 안정성
    tension: 0.10        # 갈등이 있을 때만
    relational: 0.10     # 약속 이행 추적

# 코드 리뷰 동료 데브 — 긴장 포착 + 상황 서술 중심
narrative:
  weights:
    tension: 0.40        # "이 부분이 문제인데..."
    situational: 0.30    # 정확한 코드 분석
    intentional: 0.15    # 의도 파악
    relational: 0.10     # 리뷰어-작성자 관계
    journey: 0.05        # PR 히스토리

# 학습 동료 솔 — 의도 추론 + 관계 의식 중심
narrative:
  weights:
    intentional: 0.30    # "이 개념의 어디가 헷갈려요?"
    relational: 0.30     # 소크라테스식 역할 분담
    tension: 0.20        # 이해와 오해 사이의 간극
    journey: 0.10        # 학습 진행도
    situational: 0.10    # 현재 문제
```

---

## 혼합 전략

### 고정 vs 적응

- **고정:** 가중치를 프로파일에서 선언. 일관성, 예측 가능성.
- **적응:** 상황에 따라 가중치가 변한다. Klein의 "상황에 따라 프레임을 전환"이 근거.

### 권장: 기본 가중치 + 상황 트리거 전환

```yaml
narrative:
  default_weights: { intentional: 0.35, journey: 0.30, ... }
  triggers:
    - condition: "첫 턴"
      override: { situational: 0.50, relational: 0.30, ... }
    - condition: "미이행 약속이 있을 때"
      boost: { relational: +0.20, tension: +0.10 }
    - condition: "사용자가 짧은 답을 연속으로 보낼 때"
      boost: { situational: +0.20, relational: +0.15 }
```

---

## 학술/실무 근거 (주요)

| 이론 | 핵심 | 연결된 유형 |
|------|------|-----------|
| Bruner (1985) — Narrative vs Paradigmatic | 서사적 사고는 의도와 맥락 이해 | Intentional |
| Klein (2007) — Data-Frame Sensemaking | 프레임 구성 → 정교화/교체 | Tension, 공통 메커니즘 |
| Endsley (1995) — Situation Awareness | L1 인식 → L2 이해 → L3 예측 | Situational |
| McAdams (2001) — Narrative Identity | Redemption/Contamination 궤적 | Journey, 공통 메커니즘 |
| Pennebaker (1997) — Expressive Writing | 인과어+통찰어 증가, 관점 전환 | 공통 메커니즘 |
| Schank (1977) — Script/MOP/TOP | 패턴 매칭 → 유추 | Situational, 공통 메커니즘 |
| Weick (1995) — Sensemaking 7속성 | Identity, Retrospective, Enactment | Relational, Journey |
| PbtA — GM Moves | Announce/Put in spot/Offer | Tension |
| Improv — Yes, and | 수용+확장 | 공통 메커니즘 |
| JTBD — Christensen | 상황이 행동을 결정 | Situational |
| Service Blueprint | Frontstage/Backstage | 공통 메커니즘 (투명성) |
| Coaching — Working Alliance | 목표+과업+유대 | Relational |
