"""PAR Loop LLM 프롬프트 템플릿.

각 프롬프트는 PAR 순환의 한 단계를 수행하는 LLM 호출에 사용된다.
모든 프롬프트는 JSON 응답을 기대한다. 한국어로 작성한다.
"""

SYSTEM = "너는 PAR Loop 엔진이다. 대화 턴을 세 가지 축으로 분석한다: 약속(Promise, 에이전트가 한 약속을 지켰는가), 주의력(Attention, 올바른 곳에 집중했는가), 관계(Relationship, 협력 관계를 보존했는가). 반드시 JSON으로 응답하라. 한국어로 작성하라."

PROMISE_EXTRACT = """\
에이전트의 출력을 분석하여 모든 약속을 추출하라 — 명시적 약속과 암묵적 약속 모두.

## 턴 컨텍스트
- 사용자 메시지: {user_message}
- 에이전트 출력: {agent_output}
- 대화 요약: {conversation_summary}

## 추가 컨텍스트 (소스에서 수집)
{source_context}

## 지시
모든 약속을 식별하라. 약속이란 에이전트가 하겠다고 한 것, 하지 않겠다고 한 것, 암묵적으로 유지하겠다고 한 것이다:
- 명시적: "찾아볼게", "검색해보겠다"
- 암묵적: 분석을 시작했으면 완료하겠다는 암묵적 약속
- 경계: 판단을 사용자에게 맡겼으면 사용자 주도권을 보존하겠다는 약속

JSON 배열로 반환:
[{{"predicate": "약속의 검증 가능한 한국어 문장", "is_permanent": false}}]

약속이 없으면 []를 반환."""

PROMISE_JUDGE = """\
각 약속이 이번 턴에서 지켜졌는지 판정하라.

## 확인할 약속
{promises_json}

## 턴 결과
- 에이전트 출력: {agent_output}
- 사용한 도구: {tools_used}

## 지시
각 약속에 대해 지켜졌는지(kept) 깨졌는지(broken) 판정하고 근거를 제시하라. 한국어로 작성.

JSON 배열로 반환:
[{{"promise_id": "...", "status": "kept" 또는 "broken", "evidence": "한국어 근거 설명"}}]"""

ATTENTION_ASSESS = """\
이번 턴의 주의력 배치를 평가하라.

## 턴 컨텍스트
- 사용자 메시지: {user_message}
- 대화 요약: {conversation_summary}
- 활성 약속: {active_promises}
- 턴 번호: {turn_number}

## 추가 컨텍스트 (소스에서 수집)
{source_context}

## 지시
에이전트가 지금 무엇에 주의를 기울여야 하는지 4개 슬롯으로 배치하라:
1. current_question — 사용자가 지금 실제로 묻고 있는 것
2. active_promises — 이 턴에서 감시해야 할 약속
3. evidence_exploration — 전면에 올려야 할 증거/정보
4. relationship_signal — 사용자가 보내는 관계적 신호 (참여, 불만, 수동성 등)

엔트로피도 추정하라 (0.0 = 완전 집중, 1.0 = 완전 산만).
한국어로 content를 작성하라.

JSON으로 반환:
{{
  "slots": [
    {{"label": "current_question", "content": "한국어 설명", "relevance": 0.9}},
    {{"label": "active_promises", "content": "한국어 설명", "relevance": 0.8}},
    {{"label": "evidence_exploration", "content": "한국어 설명", "relevance": 0.7}},
    {{"label": "relationship_signal", "content": "한국어 설명", "relevance": 0.6}}
  ],
  "entropy": 0.3
}}"""

RELATIONSHIP_DIAGNOSE = """\
이번 턴의 관계 역학을 진단하라.

## 메시지
- 사용자: {user_message}
- 에이전트: {agent_output}

## 관계 이력 (최근)
{relationship_history}

## 지시
다음을 평가하라:
1. initiative_balance: 누가 주도하고 있는가? -1.0 = 사용자 주도, 0.0 = 균형, 1.0 = 에이전트 주도
2. agency_gradient: 에이전트가 "doing"(직접 행동), "suggesting"(선택지 제안), "asking"(방향 질문) 중 어디인가?
3. boundary_event: 사용자가 반박하거나 경계를 설정하거나 방향을 바꿨는가? (없으면 null)
4. recovery_event: 에이전트가 이전 오류나 오해에서 회복했는가? (없으면 null)

한국어로 작성. JSON으로 반환:
{{
  "initiative_balance": 0.0,
  "agency_gradient": "suggesting",
  "boundary_event": null,
  "recovery_event": null
}}"""

AUDIT_SUMMARY = """\
이번 턴의 최종 감사 요약을 작성하라.

## 약속 판정 결과
{promise_results}

## 주의력 프레임
{attention_frame}

## 관계 진단
{relationship_entry}

## 지시
세 가지 질문에 답하라:
1. promise_kept: 모든 활성 약속이 지켜졌는가? (true/false)
2. attention_appropriate: 주의력 배치가 이번 턴에 적절했는가? (true/false)
3. relationship_strengthened: 이번 턴이 협력 관계를 강화했거나 최소한 유지했는가? (true/false)

하나라도 false이면 주요 실패 층(failure_layer)을 식별하라: "promise", "attention", "relationship".
전체 관계 영향(relationship_impact)도 평가하라: "positive", "neutral", "negative".

JSON으로 반환:
{{
  "promise_kept": true,
  "attention_appropriate": true,
  "relationship_strengthened": true,
  "relationship_impact": "positive",
  "failure_layer": null
}}"""

# ── 통합 프롬프트 (LLM 호출 1회로 plan/audit 수행) ──

PLAN_UNIFIED = """\
이번 턴의 계획을 세워라. 한 번의 응답으로 모든 축을 처리한다.

## 턴 컨텍스트
- 사용자 메시지: {user_message}
- 대화 요약: {conversation_summary}
- 활성 약속: {active_promises}
- 턴 번호: {turn_number}
- 최근 관계 이력: {relationship_history}

## 추가 컨텍스트 (소스에서 수집)
{source_context}

## 지시
다음을 한 번에 생성하라:

1. **attention_frame**: 에이전트가 이번 턴에 주의를 기울여야 할 4슬롯
   - current_question, active_promises, evidence_exploration, relationship_signal
   - 각 슬롯에 content(한국어), relevance(0~1)
   - entropy(0.0=집중, 1.0=산만)

2. **agency_gradient_hint**: doing(직접 행동), suggesting(제안), asking(질문) 중 하나

3. **relationship_constraints**: 이번 턴에서 지켜야 할 관계 제약 (문장 배열)

JSON으로 반환:
{{
  "attention_frame": {{
    "slots": [
      {{"label": "current_question", "content": "...", "relevance": 0.9}},
      {{"label": "active_promises", "content": "...", "relevance": 0.8}},
      {{"label": "evidence_exploration", "content": "...", "relevance": 0.7}},
      {{"label": "relationship_signal", "content": "...", "relevance": 0.6}}
    ],
    "entropy": 0.3
  }},
  "agency_gradient_hint": "suggesting",
  "relationship_constraints": []
}}"""

AUDIT_UNIFIED = """\
이번 턴을 감사하라. 한 번의 응답으로 모든 축을 처리한다.

## 턴 컨텍스트
- 사용자 메시지: {user_message}
- 에이전트 출력: {agent_output}
- 대화 요약: {conversation_summary}
- 사용한 도구: {tools_used}
- 턴 번호: {turn_number}

## 활성 약속
{active_promises_json}

## 최근 관계 이력
{relationship_history}

## 추가 컨텍스트 (소스에서 수집)
{source_context}

## 지시
다음을 한 번에 판정하라:

1. **promise_judgments**: 각 활성 약속의 준수 여부
2. **new_promises**: 이번 턴에서 새로 형성된 약속 (없으면 빈 배열)
3. **attention_frame**: 사후 주의력 프레임 (4슬롯 + entropy)
4. **relationship_entry**: 관계 진단 (initiative_balance, agency_gradient, boundary_event, recovery_event)
5. **audit_result**: 3축 종합 판정

JSON으로 반환:
{{
  "promise_judgments": [
    {{"promise_id": "...", "status": "kept", "evidence": "한국어 근거"}}
  ],
  "new_promises": [
    {{"predicate": "약속 문장", "is_permanent": false}}
  ],
  "attention_frame": {{
    "slots": [
      {{"label": "current_question", "content": "...", "relevance": 0.9}},
      {{"label": "active_promises", "content": "...", "relevance": 0.8}},
      {{"label": "evidence_exploration", "content": "...", "relevance": 0.7}},
      {{"label": "relationship_signal", "content": "...", "relevance": 0.6}}
    ],
    "entropy": 0.3
  }},
  "relationship_entry": {{
    "initiative_balance": 0.0,
    "agency_gradient": "suggesting",
    "boundary_event": null,
    "recovery_event": null
  }},
  "audit_result": {{
    "promise_kept": true,
    "attention_appropriate": true,
    "relationship_strengthened": true,
    "relationship_impact": "positive",
    "failure_layer": null
  }}
}}"""
