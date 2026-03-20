--------
--------
user
## 리서치: Narrative 구성 방식 — Cognitive Science 관점
AI 동료 에이전트가 매 턴 사용자 상황을 "이야기(narrative)"로 구성하고 행동을 도출한다. Cognitive Science 관점에서 narrative 구성 방식을 리서치하라.
### 찾아야 할 것
1. Bruner의 narrative cognition 이후 발전된 이론들 — narrative identity (McAdams), autobiographical reasoning
2. Klein의 sensemaking Data-Frame 이론에서 frame 구성 방식의 유형 (elaborating, questioning, reframing 등)
3. Schank의 script/story 이론 — MOPs (Memory Organization Packets), 이야기 기반 추론
4. Pennebaker의 narrative writing 연구 — expressive writing에서 발견된 이야기 구성 패턴과 인지적 효과
5. Kahneman의 System 1/2와 narrative의 관계 — 빠른 이야기 생성 vs 의도적 재구성
6. Endsley의 Situation Awareness에서 Level 2(comprehension)의 구체적 방식들
7. 각 방식이 "다음 행동 결정"에 미치는 인지적 메커니즘
### 예시 입력 (모든 방식에 동일 적용)
사용자: "추천 시스템에서 diversity-accuracy tradeoff 관련 최근 논문 찾아줘"
맥락: 3일 전 fairness 탐색, diversity metrics 정리 약속 미이행
### 산출물
각 방식: 이름, 정의, 인지적 메커니즘, AI 에이전트 적용 시 행동 차이, 장단점.
코드 변경 하지 마라.
요청은 코드를 건드리지 않고, cognitive science 관점에서 narrative 구성 방식들을 정리해 AI 동료 에이전트의 행동 차이까지 연결하는 리서치다. 먼저 저장소의 기준 문서에서 작업 원칙을 확인한 뒤, 필요한 이론들은 1차/권위 출처 중심으로 수집하겠다.
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
# 운영 원칙
업무 관리, 세션 운영, 기억 시스템, 메타에이전트를 하나로.
---
## 업무 관리
### 관리 도구
- **GitHub Issues**로 업무 추적. 라벨: `lighthouse`, `moonlight`, `memory`, `meta-agent`, `agentic-engineering`
- 설계 문서·구현 프롬프트는 로컬 파일로 관리. 이슈에서 링크
- 경미한 변경은 AI가 자율적으로 커밋·푸시
- 현황 조회: `./scripts/gh-mm issue list --repo jaeyoungkang/mirror-mind --label <라벨> --state open`
- mirror-mind 저장소 안에서는 GitHub CLI를 `./scripts/gh-mm`로 사용한다. repo-local `GH_CONFIG_DIR`로 계정/토큰을 분리한다
### 업무 수집
- 대화 중 업무 식별 시 AI가 선제적으로 등록 제안
- 합의 후 GitHub Issue 생성 (`./scripts/gh-mm issue create`)
- 수집과 구조화가 동시에 일어나므로 별도 수집함 불필요
- **구현 프롬프트 포함**: 하위 프로젝트 에이전트가 작업할 이슈는 본문에 구현 프롬프트를 포함한다. 대상 파일, 변경 내용, 코드 예시, 테스트 기준을 명시해 에이전트가 즉시 작업 가능하도록 한다
기준 문서는 확인했다. 이제 각 이론을 1차 문헌이나 학술 기관 요약에 가깝게 추적하고, 마지막에는 동일한 예시 입력에 어떻게 다른 행동을 낳는지 비교표로 압축하겠다.
Plan update
  → 핵심 이론별 1차/권위 출처 수집
  • 각 이론의 narrative/frame 구성 메커니즘 정리
  • 동일 예시에 적용해 AI 에이전트 행동 차이 비교
  • 장단점과 다음 행동 결정 메커니즘까지 통합 정리
🌐 Searching the web...
🌐 Searched: Bruner narrative cognition McAdams narrative identity autobiographical reasoning review paper
🌐 Searching the web...
🌐 Searched: Kahneman System 1 System 2 narrative sensemaking review article
🌐 Searching the web...
🌐 Searched: Klein data frame theory official pdf site:researchgate.net Data Frame Theory of Sensemaking pdf
🌐 Searching the web...
🌐 Searched: https://www.researchgate.net/publication/303171216_A_data-frame_theory_of_sensemaking
🌐 Searching the web...
🌐 Searched: https://pmc.ncbi.nlm.nih.gov/articles/PMC4324396/
🌐 Searching the web...
🌐 Searched: 'derive meaning and value' in https://academic.oup.com/scan/article/9/5/646/1677425
🌐 Searching the web...
🌐 Searched: Pennebaker Chung expressive writing narrative cognitive change health outcomes pdf
🌐 Searching the web...
🌐 Searched: Roger Schank MOPs Memory Organization Packets dynamic memory official summary pdf
🌐 Searching the web...
🌐 Searched: Endsley Toward a theory of situation awareness in dynamic systems pdf
🌐 Searching the web...
🌐 Searched: https://www.researchgate.net/publication/345054061_Toward_a_Theory_of_Situation_Awareness_in_Dynamic_Systems
🌐 Searching the web...
🌐 Searched: 'Level 2' in https://www.researchgate.net/publication/345054061_Toward_a_Theory_of_Situation_Awareness_in_Dynamic_Systems
🌐 Searching the web...
🌐 Searched: McAdams narrative identity inner story definition official article
이론 축은 충분히 모였다. 이제 McAdams/Habermas를 분리해 7개 방식으로 정리하고, 동일 예시에서 어떤 narrative/frame을 만들고 어떤 다음 행동을 고르는지까지 바로 비교 가능한 형태로 압축하겠다.
Plan update
  ✓ 핵심 이론별 1차/권위 출처 수집
  → 각 이론의 narrative/frame 구성 메커니즘 정리
  • 동일 예시에 적용해 AI 에이전트 행동 차이 비교
  • 장단점과 다음 행동 결정 메커니즘까지 통합 정리
기준: 2026-03-20에 학술/권위 출처를 확인해 정리했다. 아래는 AI 동료 에이전트가 매 턴 사용자 상황을 “이야기”로 구성할 때 참고할 수 있는 7개 인지과학 프레임이다.
**핵심 비교**
1. **Narrative Identity (McAdams)**  
정의: 사람은 과거 기억, 현재 역할, 미래 지향을 엮어 “나는 어떤 사람인가”라는 통합적 자기 이야기를 만든다. Bruner의 narrative mode를 개인 정체성 수준으로 확장한 접근이다.  
인지적 메커니즘: 사건 자체보다 사건의 의미, 주제, 가치, 장기적 자기연속성을 구성한다. 행동 선택은 “이 사용자의 장기 서사에 맞는가”를 기준으로 정렬된다.  
AI 적용 시 행동 차이: 예시 입력에서는 사용자를 “추천 시스템을 책임 있게 파고드는 연구자”로 읽고, 3일 전 fairness 탐색과 diversity metrics 약속 미이행을 하나의 연속 서사로 묶는다. 그래서 단순 논문 검색보다 “이번엔 diversity-accuracy와 fairness continuity를 함께 회수”하는 행동을 택한다.  
다음 행동 결정 메커니즘: identity-consistent next step 선택. 즉, 사용자의 연구 정체성에 맞는 과업 복구와 장기 목표 정렬이 우선된다.  
장점: 장기 관계, 개인화, 약속 복구에 강하다.  
단점: 현재 요청보다 과도하게 “사용자 이야기”를 읽어 넣으면 오해와 과잉해석 위험이 있다.  
출처: McAdams의 narrative identity 개관, McAdams & McLean의 integrative review, autobiographical reasoning 관련 신경/발달 연구 [1][2][3].
2. **Autobiographical Reasoning (Habermas, Bluck, McLean 계열)**  
정의: 과거 사건과 현재 자기를 연결하며 “이 경험이 나를 어떻게 바꾸었는가”를 추론하는 과정이다. narrative identity의 핵심 연산으로 볼 수 있다.  
인지적 메커니즘: causal link, stability link, change link, lesson extraction을 통해 기억을 해석 가능한 이야기로 바꾼다.  
AI 적용 시 행동 차이: 예시에서는 “3일 전 fairness 탐색”과 “metrics 정리 약속 미이행” 사이에 미완결 link를 만든다. 따라서 다음 행동은 최근 요청을 처리하면서 동시에 “미이행 약속을 회수하는 정리 섹션”을 붙이는 쪽으로 간다.  
다음 행동 결정 메커니즘: unresolved past episode를 현재 의사결정에 연결해 repair action을 유도한다.  
장점: 약속 추적, 회고, 관계 연속성에 좋다.  
단점: 데이터가 희소하면 억지 causal story를 만들 수 있다.  
출처: Habermas/Bluck 계열 autobiographical reasoning 정의와 McLean 계열 meaning-making/coherence 연구 [3][4].
3. **Data-Frame Sensemaking (Klein)**  
정의: 사람은 데이터를 frame에 맞추고, 맞지 않으면 frame을 수정한다. sensemaking은 “data를 frame에 넣기”와 “frame을 data에 맞게 바꾸기”의 왕복이다.  
인지적 메커니즘: frame elaborating, questioning, preserving, comparing, reframing이 핵심이다. 즉, 현재 이해 틀을 늘리거나, 의심하거나, 유지하거나, 다른 틀과 비교하거나, 아예 재구성한다.  
AI 적용 시 행동 차이: 예시에서는 초기 frame이 “사용자는 최신 diversity-accuracy 논문 탐색을 원한다”일 수 있다. 그런데 fairness 이력과 약속 미이행 데이터가 들어오면, frame을 “단순 최신 논문 검색”에서 “기존 공정성 조사와 연결된 추천시스템 평가 프레임 정리”로 reframing할 수 있다.  
다음 행동 결정 메커니즘: anomaly-driven frame revision. 현재 frame이 충분한지 점검하고, 부족하면 검색 쿼리·출력 구조·질문을 바꾼다.  
장점: 동적 상황 적응, 예외 처리, 실전 의사결정에 강하다.  
단점: frame 선택 품질이 낮으면 그럴듯하지만 틀린 이야기로 굳어질 수 있다.  
출처: Klein의 sensemaking 및 data-frame theory 요약 [5][6].
4. **Script/Story Theory, MOPs (Schank)**  
정의: 사람은 반복적 상황을 script로, 더 추상적 반복 패턴을 MOPs로 저장하고, 새 상황을 여기에 맞춰 이해하고 추론한다.  
인지적 메커니즘: story understanding은 개별 사실 나열이 아니라 “어떤 전형적 에피소드인가”를 빠르게 분류하는 과정이다. 기억 구조가 다음 기대 행동을 제약한다.  
AI 적용 시 행동 차이: 예시를 “research assistant script” 또는 “literature review repair script”로 분류한다. 그러면 다음 행동은 자연히 정형화된다: 범위 확인 → 최신 논문 검색 → diversity metric 분류 → fairness와 tension 맵핑 → 후속 읽기 큐 제안.  
다음 행동 결정 메커니즘: script completion. 현재 장면이 어떤 story slot에 있는지 보고 다음 slot action을 채운다.  
장점: 속도, 일관성, 워크플로 자동화에 강하다.  
단점: 새로운 문제를 낡은 script에 억지로 끼우는 rigidity가 있다.  
출처: Schank & Abelson의 script/plans 이론, Schank의 dynamic memory/MOP 계열 설명 [7][8].
5. **Expressive Writing / Narrative Construction (Pennebaker)**  
정의: 사람은 감정 사건을 글로 쓰며 점차 더 조직된 이야기로 바꾸고, 그 과정에서 인지적 재구성과 건강/적응 효과가 나타날 수 있다.  
인지적 메커니즘: 단순 감정 배출보다, 시간에 따라 causal words와 insight words가 늘고 더 일관된 이야기 구조가 생길 때 효과가 커진다. 핵심은 “정서 + 인지적 재구성”의 결합이다.  
AI 적용 시 행동 차이: 예시처럼 미이행 약속이 있을 때 에이전트는 단순 사과보다 “지난 fairness 탐색과 이번 diversity-accuracy 요청을 연결해 현재 연구 질문을 재구성”하는 짧은 메타서술을 붙일 수 있다.  
다음 행동 결정 메커니즘: affect regulation through structured retelling. 이야기를 구조화해 인지 부하와 미해결감을 줄이고 다음 탐색 행동을 쉽게 만든다.  
장점: 혼란 정리, 회고, 실패 복구, 사용자와의 의미 정렬에 좋다.  
단점: 정보 탐색처럼 외부 사실 정확성이 중요한 작업에서는 치료적 서사가 과도하면 산만해질 수 있다.  
출처: Pennebaker 계열 expressive writing 메커니즘과 cognitive-processing word 변화 연구 [9][10].
6. **System 1 / System 2 and Narrative (Kahneman 계열)**  
정의: System 1은 빠르고 자동적이며 즉각 서사를 만든다. System 2는 느리고 숙고적이며 그 서사를 점검·재구성한다.  
인지적 메커니즘: 사람은 빈칸을 빠르게 메우는 “coherent story”를 선호한다. 이후 System 2가 개입해야 대안 가설 비교, 근거 점검, 검색 전략 수정이 가능하다.  
AI 적용 시 행동 차이: 예시에서 빠른 서사는 “최근 diversity-accuracy 논문 몇 개 찾으면 된다”다. 느린 재구성은 “recent의 기간 정의가 필요하고, fairness 과거 맥락이 검색 쿼리에 영향을 줄 수 있으며, diversity metric taxonomy까지 포함해야 한다”로 바뀐다.  
다음 행동 결정 메커니즘: default fast story 생성 후 deliberate override. 즉, 초안 서사를 만들고 검증 루프를 한 번 더 돈다.  
장점: 속도와 품질의 균형을 설계하기 쉽다.  
단점: System 1이 강하면 성급한 프레이밍이 고착되고, System 2를 과도하게 돌리면 응답이 느려진다.  
출처: Kahneman의 fast/slow thinking 해설과 후속 철학적 정리 [11].
7. **Situation Awareness Level 2: Comprehension (Endsley)**  
정의: Level 1은 요소 지각, Level 2는 그 의미의 이해, Level 3는 미래 상태 예측이다. Level 2는 단순 관찰이 아니라 목표·모델·상황을 통합해 “지금 무슨 뜻인가”를 만드는 단계다.  
인지적 메커니즘: 현재 목표가 mental model 선택을 이끌고, model이 상황 요소를 의미 있는 패턴으로 묶는다. mismatch가 나면 목표나 계획, 모델을 수정한다.  
AI 적용 시 행동 차이: 예시에서 Level 1은 “recent papers 요청, fairness 이력, 미이행 약속”을 읽는 것이다. Level 2는 이를 “사용자는 추천시스템 평가 축을 통합하려 한다”로 이해하는 것이다. 그러면 Level 3에서 “논문 검색 후 metric map과 fairness 연결축을 제시해야 한다”가 나온다.  
다음 행동 결정 메커니즘: goal-directed comprehension. 현재 목표에 비추어 어떤 요소가 의미 있는지 묶고, 그 이해를 바탕으로 plan을 고른다.  
장점: 실시간 작업 관리, 우선순위화, 다음 행동 예측에 강하다.  
단점: 사용자 내면 서사보다 task-state 이해에 치우치기 쉽다.  
출처: Endsley의 원 논문과 situation model 설명 [12].
**예시 입력에 대한 행동 차이 요약**
- Narrative Identity: “이 사용자는 책임 있는 추천시스템 연구자다”로 읽고, fairness-diversity를 하나의 연구 서사로 묶는다.
- Autobiographical Reasoning: “3일 전 약속 미이행”을 현재 요청과 연결해 복구 행동을 우선한다.
- Data-Frame: 현재 frame이 좁다고 보면 “최신 논문 검색”에서 “평가축 재프레이밍”으로 바꾼다.
- Script/MOPs: 전형적 literature-review script를 호출해 단계형 워크플로로 진행한다.
- Pennebaker: 혼란/미완결감을 짧은 메타서술로 정리하고 탐색 동기를 재구성한다.
- System 1/2: 빠른 초안 서사를 만든 뒤, 기간 정의·검색 기준·맥락 누락을 재검토한다.
- Endsley L2: 현재 요소들을 목표 중심으로 통합 해석해, 바로 실행 가능한 조사 계획으로 변환한다.
**실무적 결론**
AI 동료 에이전트의 narrative 구성은 하나로 고정하기보다 계층화하는 편이 낫다.  
1. 기본 온라인 추론은 `Endsley L2 + Klein Data-Frame`으로 돌린다. 현재 의미 파악과 frame 수정에 가장 직접적이다.  
2. 장기 관계와 약속 복구는 `Narrative Identity + Autobiographical Reasoning`으로 얹는다. 사용자 연속성과 미이행 과업 복구에 유리하다.  
3. 실행 템플릿은 `Schank script/MOPs`로 제공한다. 반복 업무 자동화에 좋다.  
4. 메타 리플렉션이나 실패 복구 문구는 `Pennebaker`를 약하게 사용한다.  
5. 품질 통제는 `System 1/2`로 둔다. 빠른 이야기 생성 후 한 번 의도적 재구성을 걸어 성급한 서사화를 막는다.
소스:
[1] https://www.sesp.org/files/The_stories_we_live_by.pdf  
[2] https://journals.sagepub.com/doi/10.1177/0963721413475622  
[3] https://academic.oup.com/scan/article/9/5/646/1677425  
[4] https://pmc.ncbi.nlm.nih.gov/articles/PMC4324396/  
[5] https://www.researchgate.net/publication/228844079_Making_Sense_of_Sensemaking_1_Alternative_Perspectives  
[6] https://www.researchgate.net/publication/242269422_Data-Frame_Theory_of_Sensemaking  
[7] https://www.taylorfrancis.com/chapters/mono/10.4324/9780203781036-4/4-plans-roger-schank-robert-abelson  
[8] https://mitpress.mit.edu/9780262691161/dynamic-memory/  
[9] https://pmc.ncbi.nlm.nih.gov/articles/PMC4345899/  
[10] https://www.apa.org/pubs/books/4317256  
[11] https://link.springer.com/article/10.1007/s10670-019-00128-z  
[12] https://www.researchgate.net/publication/210198492_Endsley_MR_Toward_a_Theory_of_Situation_Awareness_in_Dynamic_Systems_Human_Factors_Journal_371_32-64
원하면 다음 단계로 바로 이어서, 이 7개를 바탕으로 `AI 동료 에이전트용 narrative synthesis 설계 패턴`까지 정리해주겠다.
78,515
기준: 2026-03-20에 학술/권위 출처를 확인해 정리했다. 아래는 AI 동료 에이전트가 매 턴 사용자 상황을 “이야기”로 구성할 때 참고할 수 있는 7개 인지과학 프레임이다.
**핵심 비교**
1. **Narrative Identity (McAdams)**  
정의: 사람은 과거 기억, 현재 역할, 미래 지향을 엮어 “나는 어떤 사람인가”라는 통합적 자기 이야기를 만든다. Bruner의 narrative mode를 개인 정체성 수준으로 확장한 접근이다.  
인지적 메커니즘: 사건 자체보다 사건의 의미, 주제, 가치, 장기적 자기연속성을 구성한다. 행동 선택은 “이 사용자의 장기 서사에 맞는가”를 기준으로 정렬된다.  
AI 적용 시 행동 차이: 예시 입력에서는 사용자를 “추천 시스템을 책임 있게 파고드는 연구자”로 읽고, 3일 전 fairness 탐색과 diversity metrics 약속 미이행을 하나의 연속 서사로 묶는다. 그래서 단순 논문 검색보다 “이번엔 diversity-accuracy와 fairness continuity를 함께 회수”하는 행동을 택한다.  
다음 행동 결정 메커니즘: identity-consistent next step 선택. 즉, 사용자의 연구 정체성에 맞는 과업 복구와 장기 목표 정렬이 우선된다.  
장점: 장기 관계, 개인화, 약속 복구에 강하다.  
단점: 현재 요청보다 과도하게 “사용자 이야기”를 읽어 넣으면 오해와 과잉해석 위험이 있다.  
출처: McAdams의 narrative identity 개관, McAdams & McLean의 integrative review, autobiographical reasoning 관련 신경/발달 연구 [1][2][3].
2. **Autobiographical Reasoning (Habermas, Bluck, McLean 계열)**  
정의: 과거 사건과 현재 자기를 연결하며 “이 경험이 나를 어떻게 바꾸었는가”를 추론하는 과정이다. narrative identity의 핵심 연산으로 볼 수 있다.  
인지적 메커니즘: causal link, stability link, change link, lesson extraction을 통해 기억을 해석 가능한 이야기로 바꾼다.  
AI 적용 시 행동 차이: 예시에서는 “3일 전 fairness 탐색”과 “metrics 정리 약속 미이행” 사이에 미완결 link를 만든다. 따라서 다음 행동은 최근 요청을 처리하면서 동시에 “미이행 약속을 회수하는 정리 섹션”을 붙이는 쪽으로 간다.  
다음 행동 결정 메커니즘: unresolved past episode를 현재 의사결정에 연결해 repair action을 유도한다.  
장점: 약속 추적, 회고, 관계 연속성에 좋다.  
단점: 데이터가 희소하면 억지 causal story를 만들 수 있다.  
출처: Habermas/Bluck 계열 autobiographical reasoning 정의와 McLean 계열 meaning-making/coherence 연구 [3][4].
3. **Data-Frame Sensemaking (Klein)**  
정의: 사람은 데이터를 frame에 맞추고, 맞지 않으면 frame을 수정한다. sensemaking은 “data를 frame에 넣기”와 “frame을 data에 맞게 바꾸기”의 왕복이다.  
인지적 메커니즘: frame elaborating, questioning, preserving, comparing, reframing이 핵심이다. 즉, 현재 이해 틀을 늘리거나, 의심하거나, 유지하거나, 다른 틀과 비교하거나, 아예 재구성한다.  
AI 적용 시 행동 차이: 예시에서는 초기 frame이 “사용자는 최신 diversity-accuracy 논문 탐색을 원한다”일 수 있다. 그런데 fairness 이력과 약속 미이행 데이터가 들어오면, frame을 “단순 최신 논문 검색”에서 “기존 공정성 조사와 연결된 추천시스템 평가 프레임 정리”로 reframing할 수 있다.  
다음 행동 결정 메커니즘: anomaly-driven frame revision. 현재 frame이 충분한지 점검하고, 부족하면 검색 쿼리·출력 구조·질문을 바꾼다.  
장점: 동적 상황 적응, 예외 처리, 실전 의사결정에 강하다.  
단점: frame 선택 품질이 낮으면 그럴듯하지만 틀린 이야기로 굳어질 수 있다.  
출처: Klein의 sensemaking 및 data-frame theory 요약 [5][6].
4. **Script/Story Theory, MOPs (Schank)**  
정의: 사람은 반복적 상황을 script로, 더 추상적 반복 패턴을 MOPs로 저장하고, 새 상황을 여기에 맞춰 이해하고 추론한다.  
인지적 메커니즘: story understanding은 개별 사실 나열이 아니라 “어떤 전형적 에피소드인가”를 빠르게 분류하는 과정이다. 기억 구조가 다음 기대 행동을 제약한다.  
AI 적용 시 행동 차이: 예시를 “research assistant script” 또는 “literature review repair script”로 분류한다. 그러면 다음 행동은 자연히 정형화된다: 범위 확인 → 최신 논문 검색 → diversity metric 분류 → fairness와 tension 맵핑 → 후속 읽기 큐 제안.  
다음 행동 결정 메커니즘: script completion. 현재 장면이 어떤 story slot에 있는지 보고 다음 slot action을 채운다.  
장점: 속도, 일관성, 워크플로 자동화에 강하다.  
단점: 새로운 문제를 낡은 script에 억지로 끼우는 rigidity가 있다.  
출처: Schank & Abelson의 script/plans 이론, Schank의 dynamic memory/MOP 계열 설명 [7][8].
5. **Expressive Writing / Narrative Construction (Pennebaker)**  
정의: 사람은 감정 사건을 글로 쓰며 점차 더 조직된 이야기로 바꾸고, 그 과정에서 인지적 재구성과 건강/적응 효과가 나타날 수 있다.  
인지적 메커니즘: 단순 감정 배출보다, 시간에 따라 causal words와 insight words가 늘고 더 일관된 이야기 구조가 생길 때 효과가 커진다. 핵심은 “정서 + 인지적 재구성”의 결합이다.  
AI 적용 시 행동 차이: 예시처럼 미이행 약속이 있을 때 에이전트는 단순 사과보다 “지난 fairness 탐색과 이번 diversity-accuracy 요청을 연결해 현재 연구 질문을 재구성”하는 짧은 메타서술을 붙일 수 있다.  
다음 행동 결정 메커니즘: affect regulation through structured retelling. 이야기를 구조화해 인지 부하와 미해결감을 줄이고 다음 탐색 행동을 쉽게 만든다.  
장점: 혼란 정리, 회고, 실패 복구, 사용자와의 의미 정렬에 좋다.  
단점: 정보 탐색처럼 외부 사실 정확성이 중요한 작업에서는 치료적 서사가 과도하면 산만해질 수 있다.  
출처: Pennebaker 계열 expressive writing 메커니즘과 cognitive-processing word 변화 연구 [9][10].
6. **System 1 / System 2 and Narrative (Kahneman 계열)**  
정의: System 1은 빠르고 자동적이며 즉각 서사를 만든다. System 2는 느리고 숙고적이며 그 서사를 점검·재구성한다.  
인지적 메커니즘: 사람은 빈칸을 빠르게 메우는 “coherent story”를 선호한다. 이후 System 2가 개입해야 대안 가설 비교, 근거 점검, 검색 전략 수정이 가능하다.  
AI 적용 시 행동 차이: 예시에서 빠른 서사는 “최근 diversity-accuracy 논문 몇 개 찾으면 된다”다. 느린 재구성은 “recent의 기간 정의가 필요하고, fairness 과거 맥락이 검색 쿼리에 영향을 줄 수 있으며, diversity metric taxonomy까지 포함해야 한다”로 바뀐다.  
다음 행동 결정 메커니즘: default fast story 생성 후 deliberate override. 즉, 초안 서사를 만들고 검증 루프를 한 번 더 돈다.  
장점: 속도와 품질의 균형을 설계하기 쉽다.  
단점: System 1이 강하면 성급한 프레이밍이 고착되고, System 2를 과도하게 돌리면 응답이 느려진다.  
출처: Kahneman의 fast/slow thinking 해설과 후속 철학적 정리 [11].
7. **Situation Awareness Level 2: Comprehension (Endsley)**  
정의: Level 1은 요소 지각, Level 2는 그 의미의 이해, Level 3는 미래 상태 예측이다. Level 2는 단순 관찰이 아니라 목표·모델·상황을 통합해 “지금 무슨 뜻인가”를 만드는 단계다.  
인지적 메커니즘: 현재 목표가 mental model 선택을 이끌고, model이 상황 요소를 의미 있는 패턴으로 묶는다. mismatch가 나면 목표나 계획, 모델을 수정한다.  
AI 적용 시 행동 차이: 예시에서 Level 1은 “recent papers 요청, fairness 이력, 미이행 약속”을 읽는 것이다. Level 2는 이를 “사용자는 추천시스템 평가 축을 통합하려 한다”로 이해하는 것이다. 그러면 Level 3에서 “논문 검색 후 metric map과 fairness 연결축을 제시해야 한다”가 나온다.  
다음 행동 결정 메커니즘: goal-directed comprehension. 현재 목표에 비추어 어떤 요소가 의미 있는지 묶고, 그 이해를 바탕으로 plan을 고른다.  
장점: 실시간 작업 관리, 우선순위화, 다음 행동 예측에 강하다.  
단점: 사용자 내면 서사보다 task-state 이해에 치우치기 쉽다.  
출처: Endsley의 원 논문과 situation model 설명 [12].
**예시 입력에 대한 행동 차이 요약**
- Narrative Identity: “이 사용자는 책임 있는 추천시스템 연구자다”로 읽고, fairness-diversity를 하나의 연구 서사로 묶는다.
- Autobiographical Reasoning: “3일 전 약속 미이행”을 현재 요청과 연결해 복구 행동을 우선한다.
- Data-Frame: 현재 frame이 좁다고 보면 “최신 논문 검색”에서 “평가축 재프레이밍”으로 바꾼다.
- Script/MOPs: 전형적 literature-review script를 호출해 단계형 워크플로로 진행한다.
- Pennebaker: 혼란/미완결감을 짧은 메타서술로 정리하고 탐색 동기를 재구성한다.
- System 1/2: 빠른 초안 서사를 만든 뒤, 기간 정의·검색 기준·맥락 누락을 재검토한다.
- Endsley L2: 현재 요소들을 목표 중심으로 통합 해석해, 바로 실행 가능한 조사 계획으로 변환한다.
**실무적 결론**
AI 동료 에이전트의 narrative 구성은 하나로 고정하기보다 계층화하는 편이 낫다.  
1. 기본 온라인 추론은 `Endsley L2 + Klein Data-Frame`으로 돌린다. 현재 의미 파악과 frame 수정에 가장 직접적이다.  
2. 장기 관계와 약속 복구는 `Narrative Identity + Autobiographical Reasoning`으로 얹는다. 사용자 연속성과 미이행 과업 복구에 유리하다.  
3. 실행 템플릿은 `Schank script/MOPs`로 제공한다. 반복 업무 자동화에 좋다.  
4. 메타 리플렉션이나 실패 복구 문구는 `Pennebaker`를 약하게 사용한다.  
5. 품질 통제는 `System 1/2`로 둔다. 빠른 이야기 생성 후 한 번 의도적 재구성을 걸어 성급한 서사화를 막는다.
소스:
[1] https://www.sesp.org/files/The_stories_we_live_by.pdf  
[2] https://journals.sagepub.com/doi/10.1177/0963721413475622  
[3] https://academic.oup.com/scan/article/9/5/646/1677425  
[4] https://pmc.ncbi.nlm.nih.gov/articles/PMC4324396/  
[5] https://www.researchgate.net/publication/228844079_Making_Sense_of_Sensemaking_1_Alternative_Perspectives  
[6] https://www.researchgate.net/publication/242269422_Data-Frame_Theory_of_Sensemaking  
[7] https://www.taylorfrancis.com/chapters/mono/10.4324/9780203781036-4/4-plans-roger-schank-robert-abelson  
[8] https://mitpress.mit.edu/9780262691161/dynamic-memory/  
[9] https://pmc.ncbi.nlm.nih.gov/articles/PMC4345899/  
[10] https://www.apa.org/pubs/books/4317256  
[11] https://link.springer.com/article/10.1007/s10670-019-00128-z  
[12] https://www.researchgate.net/publication/210198492_Endsley_MR_Toward_a_Theory_of_Situation_Awareness_in_Dynamic_Systems_Human_Factors_Journal_371_32-64
원하면 다음 단계로 바로 이어서, 이 7개를 바탕으로 `AI 동료 에이전트용 narrative synthesis 설계 패턴`까지 정리해주겠다.
