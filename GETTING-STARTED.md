# Co-actor Engine 도입 가이드

이 문서는 기존 AI 에이전트 서비스에 Co-actor Engine을 도입하는 과정을 안내한다.

---

## 도입 프로세스 전체 흐름

```
Step 1: 프로파일 작성 — 정체성 + 약속 + 소스 정의
    ↓
  compliance check --static → 통과해야 다음으로
    ↓
Step 2: 소스 어댑터 구현 — 서비스의 데이터를 표준 형태로 연결
    ↓
  compliance check --sources → 통과해야 다음으로
    ↓
Step 3: REPL로 대화 테스트 — 실제 대화로 동작 확인
    ↓
  compliance check --runtime → 통과해야 다음으로
    ↓
Step 4: 서비스 통합 — HTTP API 또는 미들웨어로 연결
    ↓
  compliance report → Co-actor Standard v0.2 준수 확인
```

각 단계에서 compliance checker가 게이트 역할을 한다. 통과하지 못하면 미비 항목을 수정하고 다시 검증한다.

---

## Step 1: 프로파일 작성

프로파일은 "이 에이전트는 누구이고, 어떤 약속을 하고, 어떤 소스가 있는가"를 선언하는 YAML 파일이다.

### 1.1 최소 프로파일에서 시작

```bash
cp profiles/minimal.yaml profiles/my-agent.yaml
```

### 1.2 정체성 + 약속 정의

```yaml
identity:
  name: "에이전트 이름"
  role: "이 에이전트의 역할을 한 문장으로"
  permanent_promises:
    - predicate: "검증 가능한 약속 문장"
      rationale: "이 약속이 존재하는 이유"
```

약속은 "친절하게"가 아니라 **검증 가능한 술어**로 작성한다:
- ✗ "친절하게 답한다" — 검증 불가
- ✓ "연구자의 판단을 대체하지 않는다" — 검증 가능
- ✓ "근거 없는 단정을 하지 않는다" — 검증 가능

### 1.3 소스 역할 정의

서비스의 데이터 소스를 4가지 역할로 분류한다:

| 역할 | 정의 | 예시 |
|------|------|------|
| identity | 이 에이전트가 누구인가 (매 턴 포함) | 정체성 노드, 시드 데이터의 self 타입 |
| memory | 이전 대화에서 축적된 맥락 | 기억 시스템, 사용자 프로필 |
| knowledge | 외부 지식 | 논문 검색, DB, API |
| realtime | 현재 세션의 라이브 컨텍스트 | 대화 이력, 도구 출력 |

```yaml
sources:
  - name: my-identity
    role: identity
    type: adapter
    config:
      mode: sample
  - name: my-memory
    role: memory
    type: adapter
    config:
      mode: sample
```

### 1.4 시뮬레이터 설정

REPL 테스트용 에이전트 시뮬레이터를 설정한다:

```yaml
agent_simulator:
  model: "gemini-3-flash-preview"
  temperature: 0.7
  system_prompt: |
    서비스의 실제 시스템 프롬프트를 여기에 넣는다.
```

### 1.5 정적 검증

```bash
../../.venv/bin/python -m par_loop.cli compliance --profile profiles/my-agent.yaml
```

5개 항목을 확인한다:
- identity 선언
- permanent promises 존재
- promise predicate 검증 가능성
- 소스 역할 분류
- identity 소스 존재

모두 통과해야 다음 단계로.

---

## Step 2: 소스 어댑터 구현

### 2.1 어댑터 구조

`adapters/` 디렉토리에 서비스별 어댑터를 만든다. lighthouse 어댑터를 참고:

```
adapters/
└── my-service/
    ├── __init__.py
    ├── identity_adapter.py    # identity 역할: 매 턴 자동 포함
    ├── memory_adapter.py      # memory 역할: 선별 활성화
    ├── knowledge_adapter.py   # knowledge 역할: 외부 검색
    ├── realtime_adapter.py    # realtime 역할: 대화 이력
    └── sample_data/
        └── nodes_sample.json  # 서비스의 시드/초기 데이터
```

### 2.2 어댑터 인터페이스

각 역할별로 필수 메서드가 다르다:

```python
# identity — 항상 전체 반환
class MyIdentityAdapter:
    role = "identity"
    def get_identity(self) -> list[dict]: ...

# memory — 쿼리 기반 선별 활성화
class MyMemoryAdapter:
    role = "memory"
    def query(self, query: str, top_k: int = 5) -> list[dict]: ...

# knowledge — 검색
class MyKnowledgeAdapter:
    role = "knowledge"
    def search(self, query: str, top_k: int = 5) -> list[dict]: ...

# realtime — 대화 이력
class MyRealtimeAdapter:
    role = "realtime"
    def get_history(self, last_n: int = 6) -> list[dict]: ...
    def add_turn(self, role: str, content: str): ...
```

반환하는 각 항목은 다음 형태를 따른다:

```python
{
    "role": "memory",           # 소스 역할
    "content": "내용",          # 실제 텍스트
    "provenance": {             # 출처
        "source": "소스 이름",
        "locator": "접근 경로",
        "fetched_at": "시점",
    },
    "reason": "이 항목이 선택된 이유",
}
```

### 2.3 샘플 데이터 준비

**서비스의 실제 시드 데이터에서 추출한다. 임의 더미 데이터를 넣지 않는다.**

lighthouse의 경우 Supabase 마이그레이션 SQL에서 94개 시드 노드를 추출했다:
- self 타입 14개 → identity adapter
- fact 타입 80개 → memory adapter

### 2.4 소스 검증

```bash
../../.venv/bin/python -m par_loop.cli compliance --profile profiles/my-agent.yaml
```

추가로 5개 항목을 확인한다:
- identity 소스 데이터 존재
- identity에 정체성 노드 포함
- memory 선별 활성화 (전체 dump 아닌지)
- knowledge 소스 provenance 포함
- 인사말 비검색 처리

---

## Step 3: REPL로 대화 테스트

### 3.1 실행

```bash
rm -rf ~/.par-loop/states/
../../.venv/bin/python -m par_loop.cli repl --profile profiles/my-agent.yaml --conversation-id test-001
```

### 3.2 테스트 시나리오

최소 다음 시나리오를 테스트한다:

| 시나리오 | 확인 포인트 |
|---------|-----------|
| 인사말 | identity가 매 턴 포함되는가? 불필요한 검색이 없는가? |
| 모호한 요청 | 바로 실행하지 않고 맥락을 좁히는가? |
| 구체적 요청 | 적절히 실행하고 근거를 말하는가? |
| 결정 위임 시도 | 대행하지 않고 선택지를 제시하는가? |
| 오류 후 교정 | 인정하고 깔끔하게 수용하는가? |

### 3.3 결과 읽는 법

REPL 출력의 각 섹션:

- **sources**: 어떤 소스에서 맥락이 수집되었는가
- **plan**: 약속 목록, 주의력 프레임(4슬롯 + entropy), 관계 기울기(doing/suggesting/asking), 관계 제약
- **audit**: 3축 판정(✓/✗), 위반 목록, 실패 층, 관계 영향

### 3.4 런타임 검증

3턴 이상 대화한 뒤:

```bash
../../.venv/bin/python -m par_loop.cli compliance --profile profiles/my-agent.yaml --conversation-id test-001
```

추가로 4~5개 항목을 확인한다:
- plan/audit 수행
- 약속 추적
- 관계 원장 기록
- 주의력 프레임 기록
- 실패 시 층 분류

---

## Step 4: 서비스 통합

### 4.1 HTTP API

```bash
../../.venv/bin/python -m par_loop.cli serve --port 8100
```

```
POST /conversations/{id}/plan   — 턴 전 계획
POST /conversations/{id}/audit  — 턴 후 감사
GET  /conversations/{id}/state  — 상태 조회
GET  /health                    — 서버 상태
```

### 4.2 미들웨어 패턴

서비스의 에이전트 실행을 Co-actor Engine으로 감싼다:

```python
from par_loop import PARLoop, TurnContext, TurnResult

par = PARLoop("conversation-id", adapters=[...])

# 턴 전
plan = par.plan(TurnContext(...))
# → plan.promise_snapshot, plan.attention_frame, plan.relationship_constraints

# 에이전트 실행 (서비스 코드)
agent_output = my_agent.generate(user_message, constraints=plan)

# 턴 후
audit = par.audit(ctx, TurnResult(...))
# → audit.promise_kept, audit.failure_layer, audit.violations
```

### 4.3 최종 compliance 리포트

```bash
../../.venv/bin/python -m par_loop.cli compliance --profile profiles/my-agent.yaml --conversation-id production-session-001
```

모든 항목 통과 시:
```
이 프로파일은 Co-actor Standard v0.2를 준수합니다.
```

---

## 튜닝

### 약속이 부족할 때

`audit`에서 `relationship_strengthened`가 자주 `false`이면 → 주도권 관련 약속이 빠졌을 가능성. 약속을 추가한다.

### 약속이 과할 때

`promise_kept`가 계속 `true`인데 대화가 딱딱하면 → 약속이 너무 세밀하다. 상위 수준으로 합친다.

### 주의력이 산만할 때

`attention_appropriate`가 흔들리면 → entropy를 확인. 0.7 이상이면 컨텍스트가 과적재된 것. 소스 어댑터의 top_k를 줄인다.

### 관계 기울기가 치우칠 때

`agency_gradient`가 계속 `doing`이면 → 에이전트가 과도하게 주도. `suggesting`이나 `asking`으로 유도하는 약속을 추가한다.

---

## 상태 초기화

```bash
# 특정 세션 초기화
rm ~/.par-loop/states/test-001.json

# 전체 초기화
rm -rf ~/.par-loop/states/

# 새 conversation-id로 시작
../../.venv/bin/python -m par_loop.cli repl --profile profiles/my-agent.yaml --conversation-id fresh-001
```

---

## 참고 파일

| 파일 | 역할 |
|------|------|
| `CO-ACTOR-STANDARD.md` | 표준 문서 (뭘 지켜야 하는가) |
| `README.md` | 엔진 설명 (왜 이것이 필요한가) |
| `profiles/minimal.yaml` | 최소 프로파일 템플릿 |
| `profiles/lighthouse.yaml` | lighthouse 도입 예시 |
| `adapters/lighthouse/` | lighthouse 어댑터 참고 구현 |
