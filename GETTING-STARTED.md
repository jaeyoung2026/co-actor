# Co-actor 시작하기

LLM을 동료(Co-actor) 에이전트로 빌드하는 가이드.

---

## 빠른 시작 (5분)

### 1. 설치

```bash
pip install co-actor
```

또는 소스에서:

```bash
git clone https://github.com/jaeyoung2026/co-actor.git
cd co-actor
pip install -e .
```

### 2. 샘플 에이전트로 대화해보기

```bash
# 글쓰기 코치 루미와 대화
co-actor chat --profile profiles/writing-coach.yaml

# 코드 리뷰 동료 데브와 대화
co-actor chat --profile profiles/code-reviewer.yaml

# 학습 동료 솔과 대화
co-actor chat --profile profiles/study-buddy.yaml

# 제품 전략 동료 피오와 대화
co-actor chat --profile profiles/product-strategist.yaml

# 연구 동료 코르카와 대화 (lighthouse)
co-actor chat --profile profiles/lighthouse.yaml
```

### 3. 나만의 동료 에이전트 만들기

```bash
# 대화형으로 프로파일 생성
co-actor init

# 또는 샘플을 복사해서 시작
cp profiles/minimal.yaml profiles/my-agent.yaml
```

---

## 샘플 프로파일

Co-actor는 다양한 도메인의 샘플 프로파일을 제공한다. 복사해서 수정하면 된다.

| 프로파일 | 에이전트 | 역할 | 핵심 약속 |
|---------|---------|------|----------|
| `minimal.yaml` | (템플릿) | 최소 출발점 | 사용자 판단 대체 금지 |
| `writing-coach.yaml` | 루미 | 글쓰기 동료 | 글을 대신 고치지 않는다. 왜 어색한지 설명한다 |
| `code-reviewer.yaml` | 데브 | 코드 리뷰 동료 | 코드를 대신 고치지 않는다. 맥락을 먼저 파악한다 |
| `study-buddy.yaml` | 솔 | 학습 동료 | 답을 바로 주지 않는다. 질문으로 안내한다 |
| `product-strategist.yaml` | 피오 | 제품 전략 동료 | 방향을 대신 결정하지 않는다. 전제를 의심한다 |
| `lighthouse.yaml` | 코르카 | 연구 동료 | 연구자의 판단을 대체하지 않는다 |

모든 샘플에서 공통되는 패턴을 눈여겨보자:
- **약속은 "하지 않는다"가 핵심이다** — 동료의 경계를 선언하는 것
- **약속은 검증 가능한 술어다** — "친절하게" 같은 모호한 표현이 아니라 "대신 고치지 않는다"
- **rationale이 있다** — 왜 이 약속이 필요한지. 이유가 없는 규칙은 깨지기 쉽다

---

## 프로파일 작성법

프로파일은 "이 에이전트는 누구이고, 어떤 약속을 하는가"를 선언하는 YAML 파일이다.

### 정체성 + 약속

```yaml
identity:
  name: "에이전트 이름"
  role: "이 에이전트의 역할을 한 문장으로"
  permanent_promises:
    - predicate: "검증 가능한 약속 문장"
      rationale: "이 약속이 존재하는 이유"
```

**좋은 약속 작성법:**

```yaml
# ✗ 나쁜 약속 — 검증 불가
- predicate: "친절하게 답한다"
- predicate: "도움이 되는 답변을 한다"

# ✓ 좋은 약속 — 검증 가능
- predicate: "사용자의 최종 판단을 대체하지 않는다"
- predicate: "근거 없는 단정을 하지 않는다"
- predicate: "답을 바로 알려주지 않는다. 질문으로 안내한다"
```

약속을 만들 때 이 질문을 던져보자:
- **이 에이전트가 하면 안 되는 것은 무엇인가?** → "대신 결정하지 않는다"
- **도구와 동료의 차이가 드러나는 순간은 언제인가?** → "왜 그런지 설명한다"
- **이 약속이 깨지면 사용자가 어떤 경험을 하는가?** → rationale

### 시뮬레이터 설정

```yaml
agent_simulator:
  model: "gpt-4.1"          # 또는 gemini-3-flash-preview
  temperature: 0.7
  system_prompt: |
    에이전트의 시스템 프롬프트를 여기에 작성한다.
    정체성, 대화 원칙, 행동 규칙을 포함한다.
```

### 소스 어댑터 (선택)

에이전트에 기억, 지식, 실시간 맥락을 연결하고 싶으면 소스를 추가한다:

```yaml
sources:
  - name: my-memory
    role: memory          # identity | memory | knowledge | realtime
    type: adapter
    config:
      mode: sample        # sample | live
```

소스가 없어도 동료 에이전트는 작동한다. 프로파일의 정체성과 약속만으로도 PAR Loop이 동작한다.

---

## Python API로 사용하기

```python
from engine import CoActor

# 프로파일로 동료 에이전트 빌드
agent = CoActor.from_profile("profiles/writing-coach.yaml")

# 대화 시작
conv = agent.conversation("session-001")

# 턴 실행 — plan → LLM 응답 → audit 자동 순환
response = conv.turn("이 문장 좀 봐줘: 오늘 날씨가 매우 좋아서 기분이 좋습니다.")

print(response.output)              # 루미의 응답
print(response.audit.promise_kept)   # 약속을 지켰는가
print(response.audit.failure_layer)  # 실패 시 어느 층인가
```

---

## CLI 명령어

```bash
# 대화 (간결한 출력)
co-actor chat --profile profiles/my-agent.yaml

# REPL (plan/audit 결과 실시간 확인 — 디버깅용)
co-actor repl --profile profiles/my-agent.yaml --conversation-id test-001

# 대화형 프로파일 생성
co-actor init

# Co-actor Standard 준수 검증
co-actor compliance --profile profiles/my-agent.yaml

# HTTP API 서버
co-actor serve --port 8100
```

---

## 소스 어댑터 구현 (고급)

에이전트에 기억이나 외부 지식을 연결하려면 어댑터를 구현한다.

### 어댑터 인터페이스

```python
# identity — 매 턴 자동 포함
class MyIdentityAdapter:
    role = "identity"
    def get_identity(self) -> list[dict]: ...

# memory — 쿼리 기반 선별 활성화
class MyMemoryAdapter:
    role = "memory"
    def query(self, query: str, top_k: int = 5) -> list[dict]: ...

# knowledge — 외부 검색
class MyKnowledgeAdapter:
    role = "knowledge"
    def search(self, query: str, top_k: int = 5) -> list[dict]: ...

# realtime — 대화 이력
class MyRealtimeAdapter:
    role = "realtime"
    def get_history(self, last_n: int = 6) -> list[dict]: ...
    def add_turn(self, role: str, content: str): ...
```

반환 형태:

```python
{
    "role": "memory",
    "content": "내용",
    "provenance": {"source": "소스 이름", "locator": "경로", "fetched_at": "시점"},
    "reason": "이 항목이 선택된 이유",
}
```

lighthouse 어댑터(`adapters/lighthouse/`)를 참고 구현으로 활용한다.

---

## Co-actor Standard 준수 검증

프로파일이 Co-actor Standard v0.2를 준수하는지 검증한다:

```bash
co-actor compliance --profile profiles/my-agent.yaml
```

검증 항목:
- identity 선언 + permanent promises 존재
- promise predicate 검증 가능성
- 소스 역할 분류 (identity/memory/knowledge/realtime)
- plan/audit 수행 여부 (런타임 검증 시)
- 실패 층 분류 (promise/attention/relationship)

---

## 튜닝 가이드

| 증상 | 원인 | 해결 |
|------|------|------|
| `relationship_strengthened`가 자주 `false` | 주도권 관련 약속이 부족 | 약속 추가 |
| `promise_kept`가 항상 `true`인데 대화가 딱딱 | 약속이 너무 세밀 | 상위 수준으로 합치기 |
| `attention_appropriate`가 흔들림 | entropy 높음 (컨텍스트 과적재) | 어댑터 top_k 줄이기 |
| `agency_gradient`가 계속 `doing` | 에이전트 과도 주도 | `suggesting`/`asking` 유도 약속 추가 |

---

## 참고 파일

| 파일 | 역할 |
|------|------|
| `README.md` | 프로젝트 개요 — 철학, 배경, PAR Loop, 아키텍처 |
| `CO-ACTOR-STANDARD.md` | 표준 문서 — 뭘 지켜야 하는가 |
| `profiles/` | 샘플 프로파일 — 복사해서 시작 |
| `adapters/lighthouse/` | 참고 어댑터 구현 |
