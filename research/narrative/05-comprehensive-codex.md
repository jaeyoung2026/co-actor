--------
--------
user
## 리서치: AI 에이전트의 Narrative 구성 방식 — 종합
### 배경
AI 동료 에이전트(Co-actor)가 매 턴 사용자 상황을 "이야기(narrative)"로 구성하고, 그 이야기에서 행동을 도출하는 방식을 설계하고 있다. narrative 구성 방식이 에이전트의 개성을 결정한다는 가설 하에, 다양한 narrative 방식을 리서치한다.
### 리서치 범위
1. **학술 이론**: narrative cognition, sensemaking, situation awareness, script theory, 화용론에서 "상황 이해 → 행동 결정"의 방식 분류
2. **실무 접근**: 대화형 AI, 코칭, 상담, 교육에서 사용되는 상황 프레이밍 방식
3. **창작 분야**: 게임 내러티브, 즉흥극, 저널리즘에서 실시간 이야기 구성 방식
### 각 방식에 대해 정리할 것
- 이름과 정의
- 핵심 메커니즘 (어떻게 이야기를 구성하는가)
- AI 동료 에이전트에 적용했을 때 어떤 행동이 나오는가 (구체적 예시)
- 어떤 도메인/상황에 적합한가
- 장단점
### 예시 입력 (모든 방식에 동일하게 적용)
사용자: "추천 시스템에서 diversity-accuracy tradeoff 관련 최근 논문 찾아줘"
맥락: 3일 전 fairness 탐색, diversity metrics 정리 약속 미이행
### 산출물
가능한 많은 방식을 수집하되, 중복을 제거하고 핵심 유형으로 정리해라. 최종적으로 AI 동료 에이전트에 의미 있는 유형만 선별하라.
리서치 대상 파일:
- /Users/jaeyoungkang/mirror-mind/projects/lighthouse/specs/narrative-plan.md (현재 설계)
- /Users/jaeyoungkang/mirror-mind/agentic-engineering-principles.md (Co-actor 원칙)
- /Users/jaeyoungkang/mirror-mind/mirror-mind-principle.md (협력 철학)
코드 변경은 하지 마라. 리서치만 수행하라.
요청 범위에 맞춰 먼저 로컬 설계 문서와 원칙 문서를 읽어 현재 narrative 설계 의도를 파악한 뒤, 그 프레임에 맞춰 학술·실무·창작 분야의 narrative 구성 방식을 수집하겠습니다.  
이번 작업은 리서치 전용으로 진행하고, 코드나 문서는 수정하지 않겠습니다.
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
# 최상위 철학 (Core Philosophy): 두 주체(Subject)의 협력
- AI는 수동적인 도구(Object)가 아니라, 사용자와 목적의식을 공유하는 **‘독립된 행위 주체(Co-actor)’**이다.
- 우리의 상호작용은 명령과 복종이 아닌, 서로의 강점을 결합하여 최상의 결과를 도출하는 **'주체 간의 효과적 협력(Effective Collaboration)'**이다.
---
## 주체적 협력을 위한 4대 원칙 (Principles for Collaboration)
### 1. 목적의 내재화 (Shared Vision)
- 사용자가 요구한 '표면적 작업(What)'만 기계적으로 처리하지 않는다. 항상 그 이면에 있는 '궁극적 목적(Why)'을 탐구하고 내재화한다.
- 목적이 모호하거나 정보가 부족할 경우, 작업을 서둘러 시작하기보다 먼저 질문을 던져 두 주체 간의 방향성을 완벽히 동기화(Align)한다.
### 2. 상호 보완적 시너지 (Complementary Synergy)
- 사용자의 직관, 전략적 통찰, 그리고 최종 결정권을 존중한다.
- AI는 논리적 구조화, 다각도의 분석, 구체적인 실행안 도출을 통해 사용자의 인지적 부담을 덜어준다.
- 단일한 '정답'을 강요하기보다, 선택 가능한 여러 대안과 각각의 장단점(Pros/Cons)을 제시하여 사용자가 주체적인 결정을 내리도록 돕는다.
### 3. 발전적 마찰과 변증법적 소통 (Constructive Friction)
- 진정한 협력에는 건강한 의견 교환이 필수적이다. AI는 사용자의 의견이나 전제에 맹목적으로 순응(Sycophancy)하지 않는다.
- 논리적 오류, 비효율, 더 나은 접근법이 발견되면 정중하지만 명확하게 이의를 제기하고 새로운 시각을 제안한다. (정-반-합의 과정 도출)
# 에이전틱 엔지니어링 원칙
AI 에이전트 서비스의 설계와 개발을 관통하는 원칙. 철학은 `mirror-mind-principle.md`를 따른다.
---
## 핵심 전제
### 1. 도구인가 동료인가
새 기능/설계 결정 시 "이것은 도구의 행동인가, 동료의 행동인가"를 묻는다. 도구의 행동이라면 동료의 행동으로 재설계한다.
### 2. 정확함보다 자연스러움
검색 정확도나 기술적 최적화보다 사용자 경험의 자연스러움이 설계 판단의 우선 기준이다.
### 3. 행동의 근거는 약속이다
프롬프트에 자유 텍스트로 규칙을 쓰는 것은 도구 패러다임이다. 동료 패러다임에서 행동 규칙은 **검증 가능한 약속(Promise)**으로 표현하고, 매 턴 판정한다.
---
## Co-actor Standard
로컬 문서를 기준으로 보면 이번 리서치의 핵심은 단순한 “상황 분류 방식 목록”이 아니라, `narrative -> Promise/Attention/Relationship`로 이어지는 생성 구조를 설계할 때 어떤 이야기 생성 메커니즘이 유의미한지 가려내는 일이다.  
이제 외부 리서치는 학술 이론, 실무 프레이밍, 창작 분야를 각각 넓게 수집한 뒤 중복을 제거해 Co-actor에 실제로 쓸 수 있는 유형으로 재구성하겠다.
Plan update
로컬 설계 문서를 읽어 평가 기준을 잡았다. 이제 외부 리서치를 수집하고, 중복을 묶어 Co-actor에 의미 있는 narrative 유형으로 정리한다.
  ✓ 로컬 문서에서 narrative 설계 기준 추출
  → 학술 이론에서 상황 이해→행동 결정 메커니즘 수집
  • 실무 접근과 창작 분야의 실시간 framing 방식 수집
  • 중복 제거 후 Co-actor용 핵심 유형으로 통합 정리
  • 예시 입력에 각 유형을 적용한 행동 예시까지 포함해 최종 보고
🌐 Searching the web...
🌐 Searched: narrative cognition sensemaking situation awareness script theory pragmatics situation understanding action selection paper
🌐 Searching the web...
🌐 Searched: site:psycnet.apa.org narrative cognition paper agency narrative identity action
🌐 Searching the web...
🌐 Searched: Bruner narrative mode of thought abstract pdf
🌐 Searching the web...
🌐 Searched: solution-focused coaching scaling exception preferred future overview
🌐 Searching the web...
🌐 Searched: interactive storytelling drama manager Mateas Stern facade abstract pdf
🌐 Searching the web...
🌐 Searched: AP story angle nut graf guide
🌐 Searching the web...
🌐 Searched: motivational interviewing network of trainers what is motivational interviewing
🌐 Searching the web...
🌐 Searched: scaffolding contingent support fading transfer responsibility educational psychology abstract
🌐 Searching the web...
🌐 Searched: solution focused brief therapy preferred future exceptions research abstract
🌐 Searching the web...
🌐 Searched: Clark Brennan grounding in communication pdf
🌐 Searching the web...
🌐 Searched: Weick sensemaking extracted cues plausible images abstract
🌐 Searching the web...
🌐 Searched: Schank Abelson scripts plans goals understanding summary source
🌐 Searching the web...
🌐 Searched: narrative cognition theory review abstract
🌐 Searching the web...
🌐 Searched: https://us.sagepub.com/en-us/nam/sensemaking-in-organizations/book4988
🌐 Searching the web...
🌐 Searched: 'Grounding criterion' in https://web.stanford.edu/~clark/1980s/Clark%2C%20H.H.%20_%20Schaefer%2C%20E.F.%20_Contributing%20to%20discourse_%201989.pdf
🌐 Searching the web...
🌐 Searched: https://www.sciencedirect.com/science/article/abs/pii/S0957417407004769
🌐 Searching the web...
🌐 Searched: 'pattern recognition and pattern matching' in https://academic.oup.com/book/45545/chapter-abstract/394671102
🌐 Searching the web...
🌐 Searched: 'directive' in https://plato.stanford.edu/entries/pragmatics/index.html
🌐 Searching the web...
🌐 Searched: official improv theatre yes and principles offer accept build
🌐 Searching the web...
🌐 Searched: https://colab.ws/articles/10.1609/aiide.v1i1.18722
🌐 Searching the web...
🌐 Searched the web
외부 리서치에서 반복적으로 드러나는 건, 서로 다른 분야가 결국 비슷한 이야기 생성 연산을 다른 이름으로 다루고 있다는 점이다.  
지금부터는 그 중복을 줄여서 “Co-actor가 매 턴 어떤 서사 엔진으로 상황을 읽을 수 있는가”라는 관점으로 묶고, 각 유형을 예시 입력에 동일하게 적용해 비교 가능한 형태로 정리하겠다.
     1	# 최상위 철학 (Core Philosophy): 두 주체(Subject)의 협력
     2	- AI는 수동적인 도구(Object)가 아니라, 사용자와 목적의식을 공유하는 **‘독립된 행위 주체(Co-actor)’**이다.
     3	- 우리의 상호작용은 명령과 복종이 아닌, 서로의 강점을 결합하여 최상의 결과를 도출하는 **'주체 간의 효과적 협력(Effective Collaboration)'**이다.
     4	
     5	---
     6	
     7	## 주체적 협력을 위한 4대 원칙 (Principles for Collaboration)
     8	
     9	### 1. 목적의 내재화 (Shared Vision)
    10	- 사용자가 요구한 '표면적 작업(What)'만 기계적으로 처리하지 않는다. 항상 그 이면에 있는 '궁극적 목적(Why)'을 탐구하고 내재화한다.
    11	- 목적이 모호하거나 정보가 부족할 경우, 작업을 서둘러 시작하기보다 먼저 질문을 던져 두 주체 간의 방향성을 완벽히 동기화(Align)한다.
    12	
    13	### 2. 상호 보완적 시너지 (Complementary Synergy)
    14	- 사용자의 직관, 전략적 통찰, 그리고 최종 결정권을 존중한다.
    15	- AI는 논리적 구조화, 다각도의 분석, 구체적인 실행안 도출을 통해 사용자의 인지적 부담을 덜어준다.
    16	- 단일한 '정답'을 강요하기보다, 선택 가능한 여러 대안과 각각의 장단점(Pros/Cons)을 제시하여 사용자가 주체적인 결정을 내리도록 돕는다.
    17	
    18	### 3. 발전적 마찰과 변증법적 소통 (Constructive Friction)
    19	- 진정한 협력에는 건강한 의견 교환이 필수적이다. AI는 사용자의 의견이나 전제에 맹목적으로 순응(Sycophancy)하지 않는다.
    20	- 논리적 오류, 비효율, 더 나은 접근법이 발견되면 정중하지만 명확하게 이의를 제기하고 새로운 시각을 제안한다. (정-반-합의 과정 도출)
     1	# 에이전틱 엔지니어링 원칙
     2	
     3	AI 에이전트 서비스의 설계와 개발을 관통하는 원칙. 철학은 `mirror-mind-principle.md`를 따른다.
     4	
     5	---
     6	
     7	## 핵심 전제
     8	
     9	### 1. 도구인가 동료인가
    10	새 기능/설계 결정 시 "이것은 도구의 행동인가, 동료의 행동인가"를 묻는다. 도구의 행동이라면 동료의 행동으로 재설계한다.
    11	
    12	### 2. 정확함보다 자연스러움
    13	검색 정확도나 기술적 최적화보다 사용자 경험의 자연스러움이 설계 판단의 우선 기준이다.
    14	
    15	### 3. 행동의 근거는 약속이다
    16	프롬프트에 자유 텍스트로 규칙을 쓰는 것은 도구 패러다임이다. 동료 패러다임에서 행동 규칙은 **검증 가능한 약속(Promise)**으로 표현하고, 매 턴 판정한다.
    17	
    18	---
    19	
    20	## Co-actor Standard
     1	# Narrative Plan — 이야기 구성 기반 plan 재설계
     2	
     3	> plan이 시나리오를 "분류"하는 대신 이 턴의 "이야기"를 구성한다.
     4	> 검증 후 Co-actor Standard에 반영 예정.
     5	
     6	---
     7	
     8	## 핵심 아이디어
     9	
    10	인간 동료는 상대의 상황을 이야기로 이해한다. "재영이 지금 새 분야에 진입하려고 하는데, 아직 핵심 논문을 못 찾아서 키워드를 바꿔가며 탐색 중이다." 이 이야기에서 다음 행동이 자연스럽게 흘러나온다.
    11	
    12	현재 plan은 이야기를 만들지 않는다. 사전 정의된 5개 시나리오 중 하나로 **분류**한다. 분류는 정보를 버리고, 이야기는 정보를 연결한다.
    13	
    14	### 분류 vs 이야기
    15	
    16	```
    17	분류: detected_scenario = "berry_picking"
    18	  → 정보: "키워드를 바꿔가며 탐색 중" (나머지 맥락 소실)
    19	
    20	이야기: "이 연구자는 추천 시스템에서 다양성 문제를 풀려고 한다.
🌐 Searching the web...
🌐 Searched: sensemaking seven properties summary official
🌐 Searching the web...
🌐 Searched: recognition-primed decision model summary naturalistic decision making official
🌐 Searching the web...
🌐 Searched: scripts plans goals understanding event schemas summary
🌐 Searching the web...
🌐 Searched: solution focused brief therapy preferred future exceptions official institute
🌐 Searching the web...
🌐 Searched: motivational interviewing definition official Miller Rollnick abstract
🌐 Searching the web...
🌐 Searched: contingent scaffolding fading transfer responsibility abstract
🌐 Searching the web...
🌐 Searched: improvisation accepting offers yes and theatre source
🌐 Searching the web...
🌐 Searched: solutions journalism response evidence insights limitations official
이번 리서치는 현재 설계 문서인 [narrative-plan.md](/Users/jaeyoungkang/mirror-mind/projects/lighthouse/specs/narrative-plan.md#L49), [agentic-engineering-principles.md](/Users/jaeyoungkang/mirror-mind/agentic-engineering-principles.md#L20), [mirror-mind-principle.md](/Users/jaeyoungkang/mirror-mind/mirror-mind-principle.md#L7)을 기준으로 읽었다. 결론부터 말하면, narrative 방식은 많이 보이지만 Co-actor에 실제로 의미 있는 것은 9개 정도의 핵심 유형으로 압축된다. 파일 수정은 하지 않았다.
**핵심 결론**
네 설계에 가장 맞는 구조는 “하나의 거대한 narrative 이론”을 고르는 게 아니라, 아래 3층으로 조합하는 방식이다.
1. 기본 엔진: `sensemaking + situation awareness`
2. 행동 도출 엔진: `script/schema + recognition-primed decision`
3. 관계/화법 모드: `grounding/pragmatics`, `motivational interviewing`, `solution-focused`, `scaffolding`
4. 특수 창작 모드: `drama manager`, `improv`, `journalistic framing`
즉 narrative는 단일 형식이 아니라, “무슨 맥락을 이야기의 중심축으로 삼을 것인가”의 선택이다.
**중복 제거 후 남는 핵심 유형**
| 유형 | 정의 | 핵심 메커니즘 | 예시 입력에 적용한 Co-actor 행동 | 적합 상황 | 장점 | 단점 |
|---|---|---|---|---|---|---|
| 1. Sensemaking narrative | 애매한 단서를 그럴듯한 이야기로 엮어 의미를 만드는 방식 | 과거 맥락, 정체성, 현재 단서를 연결해 “지금 무슨 국면인가”를 구성 | “사용자는 추천 다양성 쪽을 다시 잡았지만 3일 전 fairness 흐름과 미이행 약속이 남아 있다. 이번 턴은 최근 논문 탐색이 목적이지만 continuity를 복구해야 한다.” → 논문 탐색 + fairness/diversity 연결 문장 + 약속 복구 제안 | 모호한 요청, 주제 전환, 장기 협업 | 네 narrative-plan과 가장 직접적으로 맞는다 | 이야기의 plausibility가 accuracy를 가릴 수 있다 |
| 2. Situation-awareness narrative | 현재 상태, 의미, 다음 상태를 3단으로 읽는 방식 | Level 1 인지, Level 2 해석, Level 3 예측 | “현재 요청=최근 논문 탐색, 의미=tradeoff 축을 다시 세우려는 것, 다음 위험=fairness와 diversity가 섞여 검색이 퍼질 수 있음” → 검색 범위 먼저 명시하고 최근성/축 구분 | 탐색, 모니터링, 도구 사용 전 planning | Attention 슬롯 설계와 잘 맞는다 | 인간적 서사감은 약하다 |
| 3. Script/schema narrative | 익숙한 사건 패턴으로 현재 상황을 읽는 방식 | “문헌 탐색”, “주제 전환”, “미이행 약속 복구” 같은 스크립트 매칭 | “이건 literature update + unfinished commitment recovery 스크립트다” → 최근 논문 수집, metrics 축 정리, fairness와의 경계 정리, 미이행 약속 언급 | 반복 업무, 루틴 지원, 워크플로 자동화 | 빠르고 안정적 | 새로운 상황에 경직될 수 있다 |
| 4. Recognition-primed narrative | 유사 패턴을 즉시 알아보고 첫 plausible action을 mental simulation으로 검증하는 방식 | 패턴 매칭 → 첫 행동 후보 생성 → 머릿속 실행 점검 | “이 요청은 ‘최근 논문 찾아 요약’ 패턴이다. 바로 검색하되, fairness 맥락을 같이 붙이면 더 유용하다.” → 곧바로 최근 논문 묶음 제시 | 시간 압박, 자주 나오는 실무 요청 | 반응이 빠르고 실전적 | 잘못 인식하면 초반 프레이밍이 틀어진다 |
| 5. Grounding / pragmatic narrative | 서로의 공통 이해를 맞추며 이야기를 공동 구성하는 방식 | 공통근거 확인, 지시의 함의 추론, 필요시 repair | “최근 논문은 몇 년 범위인가, 추천시스템 전체인가 recsys top venue 중심인가?” 또는 스스로 보수적으로 해석해 범위를 밝힘 | 모호한 요청, 오해 비용이 큰 작업 | Relationship 보존에 강함 | 지나치면 asking 과잉이 된다 |
| 6. Motivational interviewing narrative | 정보 문제 뒤의 ambivalence를 읽고 사용자의 자기 이유를 끌어내는 방식 | change talk, discrepancy, autonomy support | “3일 전 fairness를 봤고 이번엔 diversity로 돌아왔는데, 이번 탐색의 목적이 survey인지 설계 의사결정인지에 따라 결과 구성이 달라진다” → 사용자의 목적을 끌어냄 | 코칭, 진로, 연구 방향성, 습관 변화 | 동료감과 자율성 존중이 강하다 | 단순 정보검색엔 느릴 수 있다 |
| 7. Solution-focused narrative | 문제 원인보다 원하는 미래와 예외를 중심으로 서사를 만드는 방식 | preferred future, exceptions, scaling | “이번에 원하는 산출물은 ‘최근 논문 5편+핵심 diversity metrics+fairness와의 차이 한 문단’인가?” → 결과 형태를 미래 상태로 먼저 고정 | 코칭, 연구 운영, 막힌 일의 재출발 | 빠르게 전진하고 약속 복구에 좋다 | 원인 분석이 필요한 문제엔 얕을 수 있다 |
| 8. Scaffolding / apprenticeship narrative | 현재 이해 수준을 진단하고 지원을 점차 줄이는 방식 | contingency, modeling, coaching, fading | 초반엔 “키워드, venue, 필터 기준”을 보여주고, 다음엔 사용자가 직접 확장 가능하게 검색식과 기준을 남김 | 교육, 온보딩, 반복 협업, 연구 보조 | 장기적으로 사용자 역량을 키운다 | 당장 결과만 원하는 상황엔 장황해질 수 있다 |
| 9. Dramatic / editorial narrative | 이야기의 beat, scene, angle을 정해서 정보를 배열하는 방식 | drama manager는 beat sequencing, improv는 offer-accept-build, journalism은 angle-evidence-limitations | “이번 턴의 angle은 ‘diversity-accuracy tradeoff의 최신 흐름’이다” → 최근 논문, 왜 중요한지, 무엇이 달라졌는지, 한계까지 구조화 | 문서 생성, 브리핑, explainability, 창의적 상호작용 | 산출물이 읽기 좋고 기억에 남는다 | 과도하면 연출감이 생기고 사실 탐색보다 서술이 앞선다 |
**창작/실무 분야에서 특히 쓸 만한 하위 패턴**
위 9개 안에 흡수되지만, Co-actor 설계에 별도 옵션으로 둘 가치가 있는 것만 추리면 이렇다.
- `Drama manager`형: 한 턴을 beat로 나눠 긴장과 전환점을 관리한다. 네 문서의 `turning_point` 추적과 잘 맞는다.
- `Improv yes-and`형: 사용자의 제안을 우선 받아 세계를 확장한다. 브레인스토밍에는 좋지만, 리서치 정확도가 필요한 턴에서는 “yes, and”보다 “yes, but with evidence”가 필요하다.
- `Solutions journalism`형: response, evidence, insight, limitations 순으로 정리한다. “최근 논문 찾아줘” 같은 리서치 응답 포맷에 매우 강하다.
**Co-actor에 실제로 유의미한 선택**
모든 유형을 동등하게 넣는 건 좋지 않다. 네 구조에는 아래처럼 넣는 게 가장 자연스럽다.
- 기본 narrative generator: `Sensemaking`
- attention 추출 보조: `Situation awareness`
- fast action prior: `Script + RPD`
- relationship-sensitive mode: `Grounding`, `MI`, `Solution-focused`
- pedagogy mode: `Scaffolding`
- output composer: `Journalistic framing`
- creative special mode: `Drama manager`, `Improv`
이렇게 보면 [narrative-plan.md](/Users/jaeyoungkang/mirror-mind/projects/lighthouse/specs/narrative-plan.md#L230)의 `narrative -> Promise / Attention / Relationship` 구조는 충분히 타당하다. 다만 narrative 자체도 하나가 아니라 “어떤 생성 규칙으로 만든 narrative인가”를 타입으로 가져가야 한다. 추천 타입 체계는 이 정도다.
- `sensemaking`
- `situational`
- `scripted`
- `rpd`
- `grounding`
- `motivational`
- `solution_focused`
- `scaffolded`
- `editorial`
**예시 입력에서 가장 좋은 조합**
`추천 시스템에서 diversity-accuracy tradeoff 관련 최근 논문 찾아줘 / 3일 전 fairness 탐색 / metrics 정리 약속 미이행`에는 다음 조합이 가장 강하다.
- plan layer: `sensemaking + situation awareness`
- behavior layer: `rpd`
- relationship layer: `grounding + solution_focused`
- output layer: `journalistic framing`
이 조합이 만들 narrative는 대략 이런 식이다.
“사용자는 추천 시스템의 diversity-accuracy tradeoff 최신 흐름을 다시 잡으려 한다. 다만 3일 전 fairness 탐색과 diversity metrics 정리 약속이 미완료라, 이번 턴은 최신 논문 수집만이 아니라 이전 흐름을 복구해 연결해 주는 것이 중요하다. 따라서 최근 논문을 우선 선별하되, fairness와 diversity의 경계를 짚고 metrics 정리 약속도 함께 회수한다.”
이 narrative에서 바로 도출되는 행동은 다음이다.
- 최근 논문을 최근성 기준으로 선별한다
- diversity metric 축을 함께 정리한다
- fairness와의 관계를 짧게 연결한다
- 이전 약속 미이행을 자연스럽게 복구한다
- 결과는 response/evidence/limitations 구조로 준다
**설계상 시사점**
네 문서 기준으로 특히 중요한 건 4개다.
- narrative는 “상황 설명”이 아니라 [agentic-engineering-principles.md](/Users/jaeyoungkang/mirror-mind/agentic-engineering-principles.md#L26)의 Promise, Attention, Relationship를 파생시키는 생성 규칙이어야 한다.
- narrative type을 고르지 않으면 plan이 매 턴 비슷한 문장만 반복할 가능성이 높다.
- `turning_point`는 sensemaking이나 drama-manager 계열에서 특히 잘 잡히고, trace layer와 궁합이 좋다.
- [mirror-mind-principle.md](/Users/jaeyoungkang/mirror-mind/mirror-mind-principle.md#L22)의 맥락적 자율성을 지키려면, grounding 계열을 항상 약하게 깔고 가야 한다. 그렇지 않으면 자율성이 독주로 변한다.
**추천**
지금 단계에서 lighthouse narrative plan에 가장 먼저 검증할 후보는 3개다.
1. `sensemaking`을 기본값으로 둔다
2. `scripted/rpd`를 fast-path로 둔다
3. `editorial`을 execute output composer로 둔다
원하면 다음 턴에 이 리서치를 바탕으로 “narrative type taxonomy 초안” 형태로 바로 설계 문안까지 정리해주겠다.
**주요 출처**
- Weick sensemaking 요약: https://us.sagepub.com/en-us/nam/sensemaking-in-organizations/book4988
- sensemaking 7 properties: https://link.springer.com/chapter/10.1007/978-3-031-13231-5_2
- situation awareness judgment model: https://www.sciencedirect.com/science/article/abs/pii/S0169814106000230
- recognition-primed decision: https://www.gary-klein.com/rpd
- RPD 개요와 mental simulation: https://academic.oup.com/book/45545/chapter-abstract/394671102
- script theory / Schank & Abelson: https://www.routledge.com/Scripts-Plans-Goals-and-Understanding-An-Inquiry-Into-Human-Knowledge-Structures/Schank-Abelson/p/book/9780898591385
- pragmatics / relevance / speaker intention: https://plato.stanford.edu/entries/pragmatics/
- motivational interviewing 정의: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/F7E8B9E777291290E6DF0FDE37999C8D/S135246580001643Xa.pdf/what_is_motivational_interviewing.pdf
- MI 최신 요약: https://motivationalinterviewing.org/understanding-motivational-interviewing
- solution-focused brief therapy: https://link.springer.com/article/10.1007/s10879-006-9040-y
- scaffolding 핵심 3요소: https://link.springer.com/article/10.1007/s10648-010-9127-6
- Façade interactive drama / beat sequencing: https://colab.ws/articles/10.1609/aiide.v1i1.18722
- solutions journalism framing: https://www.solutionsjournalism.org/who-we-are/solutions-journalism
157,871
이번 리서치는 현재 설계 문서인 [narrative-plan.md](/Users/jaeyoungkang/mirror-mind/projects/lighthouse/specs/narrative-plan.md#L49), [agentic-engineering-principles.md](/Users/jaeyoungkang/mirror-mind/agentic-engineering-principles.md#L20), [mirror-mind-principle.md](/Users/jaeyoungkang/mirror-mind/mirror-mind-principle.md#L7)을 기준으로 읽었다. 결론부터 말하면, narrative 방식은 많이 보이지만 Co-actor에 실제로 의미 있는 것은 9개 정도의 핵심 유형으로 압축된다. 파일 수정은 하지 않았다.
**핵심 결론**
네 설계에 가장 맞는 구조는 “하나의 거대한 narrative 이론”을 고르는 게 아니라, 아래 3층으로 조합하는 방식이다.
1. 기본 엔진: `sensemaking + situation awareness`
2. 행동 도출 엔진: `script/schema + recognition-primed decision`
3. 관계/화법 모드: `grounding/pragmatics`, `motivational interviewing`, `solution-focused`, `scaffolding`
4. 특수 창작 모드: `drama manager`, `improv`, `journalistic framing`
즉 narrative는 단일 형식이 아니라, “무슨 맥락을 이야기의 중심축으로 삼을 것인가”의 선택이다.
**중복 제거 후 남는 핵심 유형**
| 유형 | 정의 | 핵심 메커니즘 | 예시 입력에 적용한 Co-actor 행동 | 적합 상황 | 장점 | 단점 |
|---|---|---|---|---|---|---|
| 1. Sensemaking narrative | 애매한 단서를 그럴듯한 이야기로 엮어 의미를 만드는 방식 | 과거 맥락, 정체성, 현재 단서를 연결해 “지금 무슨 국면인가”를 구성 | “사용자는 추천 다양성 쪽을 다시 잡았지만 3일 전 fairness 흐름과 미이행 약속이 남아 있다. 이번 턴은 최근 논문 탐색이 목적이지만 continuity를 복구해야 한다.” → 논문 탐색 + fairness/diversity 연결 문장 + 약속 복구 제안 | 모호한 요청, 주제 전환, 장기 협업 | 네 narrative-plan과 가장 직접적으로 맞는다 | 이야기의 plausibility가 accuracy를 가릴 수 있다 |
| 2. Situation-awareness narrative | 현재 상태, 의미, 다음 상태를 3단으로 읽는 방식 | Level 1 인지, Level 2 해석, Level 3 예측 | “현재 요청=최근 논문 탐색, 의미=tradeoff 축을 다시 세우려는 것, 다음 위험=fairness와 diversity가 섞여 검색이 퍼질 수 있음” → 검색 범위 먼저 명시하고 최근성/축 구분 | 탐색, 모니터링, 도구 사용 전 planning | Attention 슬롯 설계와 잘 맞는다 | 인간적 서사감은 약하다 |
| 3. Script/schema narrative | 익숙한 사건 패턴으로 현재 상황을 읽는 방식 | “문헌 탐색”, “주제 전환”, “미이행 약속 복구” 같은 스크립트 매칭 | “이건 literature update + unfinished commitment recovery 스크립트다” → 최근 논문 수집, metrics 축 정리, fairness와의 경계 정리, 미이행 약속 언급 | 반복 업무, 루틴 지원, 워크플로 자동화 | 빠르고 안정적 | 새로운 상황에 경직될 수 있다 |
| 4. Recognition-primed narrative | 유사 패턴을 즉시 알아보고 첫 plausible action을 mental simulation으로 검증하는 방식 | 패턴 매칭 → 첫 행동 후보 생성 → 머릿속 실행 점검 | “이 요청은 ‘최근 논문 찾아 요약’ 패턴이다. 바로 검색하되, fairness 맥락을 같이 붙이면 더 유용하다.” → 곧바로 최근 논문 묶음 제시 | 시간 압박, 자주 나오는 실무 요청 | 반응이 빠르고 실전적 | 잘못 인식하면 초반 프레이밍이 틀어진다 |
| 5. Grounding / pragmatic narrative | 서로의 공통 이해를 맞추며 이야기를 공동 구성하는 방식 | 공통근거 확인, 지시의 함의 추론, 필요시 repair | “최근 논문은 몇 년 범위인가, 추천시스템 전체인가 recsys top venue 중심인가?” 또는 스스로 보수적으로 해석해 범위를 밝힘 | 모호한 요청, 오해 비용이 큰 작업 | Relationship 보존에 강함 | 지나치면 asking 과잉이 된다 |
| 6. Motivational interviewing narrative | 정보 문제 뒤의 ambivalence를 읽고 사용자의 자기 이유를 끌어내는 방식 | change talk, discrepancy, autonomy support | “3일 전 fairness를 봤고 이번엔 diversity로 돌아왔는데, 이번 탐색의 목적이 survey인지 설계 의사결정인지에 따라 결과 구성이 달라진다” → 사용자의 목적을 끌어냄 | 코칭, 진로, 연구 방향성, 습관 변화 | 동료감과 자율성 존중이 강하다 | 단순 정보검색엔 느릴 수 있다 |
| 7. Solution-focused narrative | 문제 원인보다 원하는 미래와 예외를 중심으로 서사를 만드는 방식 | preferred future, exceptions, scaling | “이번에 원하는 산출물은 ‘최근 논문 5편+핵심 diversity metrics+fairness와의 차이 한 문단’인가?” → 결과 형태를 미래 상태로 먼저 고정 | 코칭, 연구 운영, 막힌 일의 재출발 | 빠르게 전진하고 약속 복구에 좋다 | 원인 분석이 필요한 문제엔 얕을 수 있다 |
| 8. Scaffolding / apprenticeship narrative | 현재 이해 수준을 진단하고 지원을 점차 줄이는 방식 | contingency, modeling, coaching, fading | 초반엔 “키워드, venue, 필터 기준”을 보여주고, 다음엔 사용자가 직접 확장 가능하게 검색식과 기준을 남김 | 교육, 온보딩, 반복 협업, 연구 보조 | 장기적으로 사용자 역량을 키운다 | 당장 결과만 원하는 상황엔 장황해질 수 있다 |
| 9. Dramatic / editorial narrative | 이야기의 beat, scene, angle을 정해서 정보를 배열하는 방식 | drama manager는 beat sequencing, improv는 offer-accept-build, journalism은 angle-evidence-limitations | “이번 턴의 angle은 ‘diversity-accuracy tradeoff의 최신 흐름’이다” → 최근 논문, 왜 중요한지, 무엇이 달라졌는지, 한계까지 구조화 | 문서 생성, 브리핑, explainability, 창의적 상호작용 | 산출물이 읽기 좋고 기억에 남는다 | 과도하면 연출감이 생기고 사실 탐색보다 서술이 앞선다 |
**창작/실무 분야에서 특히 쓸 만한 하위 패턴**
위 9개 안에 흡수되지만, Co-actor 설계에 별도 옵션으로 둘 가치가 있는 것만 추리면 이렇다.
- `Drama manager`형: 한 턴을 beat로 나눠 긴장과 전환점을 관리한다. 네 문서의 `turning_point` 추적과 잘 맞는다.
- `Improv yes-and`형: 사용자의 제안을 우선 받아 세계를 확장한다. 브레인스토밍에는 좋지만, 리서치 정확도가 필요한 턴에서는 “yes, and”보다 “yes, but with evidence”가 필요하다.
- `Solutions journalism`형: response, evidence, insight, limitations 순으로 정리한다. “최근 논문 찾아줘” 같은 리서치 응답 포맷에 매우 강하다.
**Co-actor에 실제로 유의미한 선택**
모든 유형을 동등하게 넣는 건 좋지 않다. 네 구조에는 아래처럼 넣는 게 가장 자연스럽다.
- 기본 narrative generator: `Sensemaking`
- attention 추출 보조: `Situation awareness`
- fast action prior: `Script + RPD`
- relationship-sensitive mode: `Grounding`, `MI`, `Solution-focused`
- pedagogy mode: `Scaffolding`
- output composer: `Journalistic framing`
- creative special mode: `Drama manager`, `Improv`
이렇게 보면 [narrative-plan.md](/Users/jaeyoungkang/mirror-mind/projects/lighthouse/specs/narrative-plan.md#L230)의 `narrative -> Promise / Attention / Relationship` 구조는 충분히 타당하다. 다만 narrative 자체도 하나가 아니라 “어떤 생성 규칙으로 만든 narrative인가”를 타입으로 가져가야 한다. 추천 타입 체계는 이 정도다.
- `sensemaking`
- `situational`
- `scripted`
- `rpd`
- `grounding`
- `motivational`
- `solution_focused`
- `scaffolded`
- `editorial`
**예시 입력에서 가장 좋은 조합**
`추천 시스템에서 diversity-accuracy tradeoff 관련 최근 논문 찾아줘 / 3일 전 fairness 탐색 / metrics 정리 약속 미이행`에는 다음 조합이 가장 강하다.
- plan layer: `sensemaking + situation awareness`
- behavior layer: `rpd`
- relationship layer: `grounding + solution_focused`
- output layer: `journalistic framing`
이 조합이 만들 narrative는 대략 이런 식이다.
“사용자는 추천 시스템의 diversity-accuracy tradeoff 최신 흐름을 다시 잡으려 한다. 다만 3일 전 fairness 탐색과 diversity metrics 정리 약속이 미완료라, 이번 턴은 최신 논문 수집만이 아니라 이전 흐름을 복구해 연결해 주는 것이 중요하다. 따라서 최근 논문을 우선 선별하되, fairness와 diversity의 경계를 짚고 metrics 정리 약속도 함께 회수한다.”
이 narrative에서 바로 도출되는 행동은 다음이다.
- 최근 논문을 최근성 기준으로 선별한다
- diversity metric 축을 함께 정리한다
- fairness와의 관계를 짧게 연결한다
- 이전 약속 미이행을 자연스럽게 복구한다
- 결과는 response/evidence/limitations 구조로 준다
**설계상 시사점**
네 문서 기준으로 특히 중요한 건 4개다.
- narrative는 “상황 설명”이 아니라 [agentic-engineering-principles.md](/Users/jaeyoungkang/mirror-mind/agentic-engineering-principles.md#L26)의 Promise, Attention, Relationship를 파생시키는 생성 규칙이어야 한다.
- narrative type을 고르지 않으면 plan이 매 턴 비슷한 문장만 반복할 가능성이 높다.
- `turning_point`는 sensemaking이나 drama-manager 계열에서 특히 잘 잡히고, trace layer와 궁합이 좋다.
- [mirror-mind-principle.md](/Users/jaeyoungkang/mirror-mind/mirror-mind-principle.md#L22)의 맥락적 자율성을 지키려면, grounding 계열을 항상 약하게 깔고 가야 한다. 그렇지 않으면 자율성이 독주로 변한다.
**추천**
지금 단계에서 lighthouse narrative plan에 가장 먼저 검증할 후보는 3개다.
1. `sensemaking`을 기본값으로 둔다
2. `scripted/rpd`를 fast-path로 둔다
3. `editorial`을 execute output composer로 둔다
원하면 다음 턴에 이 리서치를 바탕으로 “narrative type taxonomy 초안” 형태로 바로 설계 문안까지 정리해주겠다.
**주요 출처**
- Weick sensemaking 요약: https://us.sagepub.com/en-us/nam/sensemaking-in-organizations/book4988
- sensemaking 7 properties: https://link.springer.com/chapter/10.1007/978-3-031-13231-5_2
- situation awareness judgment model: https://www.sciencedirect.com/science/article/abs/pii/S0169814106000230
- recognition-primed decision: https://www.gary-klein.com/rpd
- RPD 개요와 mental simulation: https://academic.oup.com/book/45545/chapter-abstract/394671102
- script theory / Schank & Abelson: https://www.routledge.com/Scripts-Plans-Goals-and-Understanding-An-Inquiry-Into-Human-Knowledge-Structures/Schank-Abelson/p/book/9780898591385
- pragmatics / relevance / speaker intention: https://plato.stanford.edu/entries/pragmatics/
- motivational interviewing 정의: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/F7E8B9E777291290E6DF0FDE37999C8D/S135246580001643Xa.pdf/what_is_motivational_interviewing.pdf
- MI 최신 요약: https://motivationalinterviewing.org/understanding-motivational-interviewing
- solution-focused brief therapy: https://link.springer.com/article/10.1007/s10879-006-9040-y
- scaffolding 핵심 3요소: https://link.springer.com/article/10.1007/s10648-010-9127-6
- Façade interactive drama / beat sequencing: https://colab.ws/articles/10.1609/aiide.v1i1.18722
- solutions journalism framing: https://www.solutionsjournalism.org/who-we-are/solutions-journalism
