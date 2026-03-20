--------
--------
user
## 리서치: Narrative 구성 방식 — UX/서비스 디자인 관점
대화형 AI 에이전트가 사용자 상황을 프레이밍하고 응답하는 방식을 UX/서비스 디자인 관점에서 리서치하라.
### 찾아야 할 것
1. Jobs-to-be-Done 프레임워크에서 "상황(situation)"이 행동을 결정하는 메커니즘
2. 서비스 디자인의 Service Blueprint에서 frontstage/backstage 구분이 narrative에 미치는 영향
3. 대화형 AI persona 디자인 — personality traits가 framing 방식을 어떻게 결정하는가
4. Proactive vs Reactive 에이전트의 narrative 차이 — 선제 제안 vs 요청 대응
5. 도메인별 narrative 접근: 의료(환자 안전 우선), 교육(소크라테스식), 금융(리스크 프레이밍), 코칭(역량 기반)
6. Microsoft Copilot, Google Gemini, ChatGPT 등 실제 서비스의 context framing 방식 비교
7. Empathic computing / affective computing에서 감정 인식이 narrative에 미치는 영향
### 예시 입력
사용자: "추천 시스템에서 diversity-accuracy tradeoff 관련 최근 논문 찾아줘"
맥락: 3일 전 fairness 탐색, diversity metrics 정리 약속 미이행
### 산출물
각 방식: 이름, 정의, 실제 서비스 사례, AI 동료 에이전트 적용 시 사용자 경험 차이, 장단점.
코드 변경 하지 마라.
요청한 범위는 UX/서비스 디자인 관점의 리서치 정리다. 먼저 저장소의 원칙 문서에서 이 작업에 필요한 기준만 짧게 확인하고, 이어서 1차 근거는 공식 문서·연구·대표 서비스 자료로 수집하겠다.
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
기준 문서는 확인했다. 이제 근거를 두 층으로 모은다: 1) JTBD, 서비스 블루프린트, affective computing 같은 개념적 근거, 2) ChatGPT, Copilot, Gemini 같은 실제 서비스의 공식 설명과 제품 행태다.
🌐 Searching the web...
🌐 Searched: Jobs to be done situation mechanism Christensen milkshake circumstances hiring theory
🌐 Searching the web...
🌐 Searched: persona design conversational AI personality traits framing style research paper
🌐 Searching the web...
🌐 Searched: site:support.google.com Gemini Apps use information from chats context official
🌐 Searching the web...
🌐 Searched: site:support.google.com Gemini Apps use your past chats official
🌐 Searching the web...
🌐 Searched: site:help.openai.com study mode chatgpt socratic official
🌐 Searching the web...
🌐 Searched: WHO patient safety conversational AI medical advice risk communication guidance
🌐 Searching the web...
🌐 Searched: financial risk framing communication investment robo advisor conversational agent research
🌐 Searching the web...
🌐 Searched: Rosalind Picard affective computing emotion recognition conversational agent narrative research
🌐 Searching the web...
🌐 Searched: empathic computing definition research paper
🌐 Searching the web...
🌐 Searched: G. Lynn Shostack service blueprint original article PDF
🌐 Searching the web...
🌐 Searched: proactive conversational agent definition vs reactive research paper
🌐 Searching the web...
🌐 Searched: https://www.christenseninstitute.org/theory/jobs-to-be-done/
🌐 Searching the web...
🌐 Searched: 'Where are responses grounded?' in https://support.microsoft.com/en-gb/topic/how-grounding-works-with-a-work-or-school-account-a3ccafb3-7fd3-4d51-bbd2-4245a7a1ef16
🌐 Searching the web...
🌐 Searched: 'Project memory keeps ChatGPT focused' in https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt%23.ejs
🌐 Searching the web...
🌐 Searched: site:support.google.com "Get personalisation in Gemini Apps" past chats sources related content
Plan update
개념 근거와 실제 서비스 자료를 수집했다. 이제 7개 축으로 정리하고, 마지막에 예시 입력에 대한 narrative 설계 차이를 합성한다.
  ✓ 원칙 문서에서 작업 기준 확인
  ✓ JTBD, 서비스 블루프린트, persona, proactive/reactive, affective computing 근거 수집
  ✓ ChatGPT, Copilot, Gemini 공식 문서 기반 비교 정리
  → 도메인별 narrative 패턴과 예시 입력 적용안으로 종합
🌐 Searching the web...
🌐 Searched: site:learn.microsoft.com Copilot prompt elements goal context expectations source
🌐 Searching the web...
🌐 Searched: site:help.openai.com ChatGPT personality official help
🌐 Searching the web...
🌐 Searched: site:help.openai.com memory in projects chatgpt official
🌐 Searching the web...
🌐 Searched: site:support.google.com Gemini Gems custom instructions official support
🌐 Searching the web...
🌐 Searched: site:support.microsoft.com Microsoft 365 Copilot Chat work web toggle official
🌐 Searching the web...
🌐 Searched: conversational agent healthcare patient safety communication review PMC
🌐 Searching the web...
🌐 Searched: robo advisor risk profiling conversational agent framing investment risk research
🌐 Searching the web...
🌐 Searched: strengths based coaching chatbot research
🌐 Searching the web...
🌐 Searched: affective computing overview emotion recognition conversational agent review PMC
🌐 Searching the web...
🌐 Searched: Nielsen Norman service blueprint frontstage backstage line of visibility
🌐 Searching the web...
🌐 Searched: dialogue initiative user initiative system initiative conversational agent research
기준일은 2026-03-20이다. 아래는 UX/서비스 디자인 관점에서 본 대화형 AI의 narrative 구성 방식 리서치다. 서비스별 framing 비교는 공식 문서에 나온 `memory / grounding / personalization / mode` 설명을 바탕으로 한 추론임을 명시한다.
**핵심**
Narrative는 단순한 말투가 아니라, `무엇을 현재 상황으로 간주하는가`, `무엇을 전면에 드러내고 무엇을 숨기는가`, `누가 대화의 initiative를 쥐는가`, `어떤 리스크를 먼저 프레이밍하는가`의 설계 문제다.
| 방식 | 정의 | 실제 서비스/근거 | AI 동료 적용 시 UX 차이 | 장점 | 단점 |
|---|---|---|---|---|---|
| `1. JTBD Situation Framing` | 사용자의 행동은 제품 속성보다 `진전이 필요한 구체적 상황`에 의해 결정된다는 관점이다. Christensen 쪽 JTBD 자료는 사람들이 “particular circumstances” 안에서 progress를 추구한다고 본다. | Christensen Institute의 JTBD 설명, milkshake 사례 계열 자료. <https://www.christenseninstitute.org/wp-content/uploads/2020/05/Curriculum-Conundrum-3.16-update.pdf> | 같은 요청도 “논문 찾아줘”가 아니라 “며칠 전 fairness를 보다가 diversity로 넘어왔고, 미이행 약속이 있으며, 지금은 literature scan이 급한 상황”으로 읽는다. 응답이 검색 결과 나열에서 `연구 상황 정리 + 다음 행동 제안`으로 바뀐다. | 사용자의 실제 맥락과 행동 동기를 잘 포착한다. | 잘못 읽으면 과잉추론이 된다. |
| `2. Frontstage/Backstage Narrative` | 서비스 블루프린트에서 frontstage는 사용자가 보는 서사, backstage는 내부 판단·검색·정리·검증 프로세스다. line of visibility를 어디에 두느냐가 narrative를 결정한다. | Shostack 전통과 최신 UX 설명. <https://doi.org/10.1108/EUM0000000004799> <https://www.interaction-design.org/literature/topics/frontstage-and-backstage> | AI가 “내가 지금 기억과 최근 검색을 교차확인하고 있다”를 frontstage에 노출하면 신뢰와 예측 가능성이 높아진다. 반대로 backstage를 숨기면 더 매끈하지만 블랙박스처럼 느껴질 수 있다. | 신뢰, 통제감, 오류 복구에 유리하다. | 지나치게 드러내면 장황하고 기계적이다. |
| `3. Persona-driven Framing` | personality traits는 단순 톤이 아니라 `무엇을 먼저 보고 어떤 형태로 말할지`를 정한다. | ChatGPT personality 공식 문서. <https://help.openai.com/en/articles/11899719-customizing-you> | 같은 사실도 “분석가형”은 분류·제약·근거를 먼저, “코치형”은 목표·장애물·다음 행동을 먼저 프레이밍한다. | 일관된 경험, 관계 형성에 강하다. | 과도하면 고정 캐릭터가 맥락보다 우선한다. |
| `4. Proactive Narrative` | 시스템이 목표를 위해 conversation direction을 일부 리드한다. proactive dialogue survey는 agent가 system-side target 달성을 위해 대화 방향을 이끈다고 정의한다. | IJCAI proactive dialogue survey, mixed-initiative 연구. <https://www.ijcai.org/proceedings/2023/738> <https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00559/116048/InSCIt-Information-Seeking-Conversations-with> | “최근 fairness를 봤으니 diversity-accuracy tradeoff로 이어서 정리하겠다. 미이행했던 diversity metrics부터 복구할까?”처럼 선제 제안을 한다. | 협업감, 흐름 유지, 맥락 전환 비용 감소. | 오지랖, 주도권 침해 위험이 있다. |
| `5. Reactive Narrative` | 현재 요청에만 반응하고 사용자가 준 문제 정의를 거의 그대로 따른다. | mixed-initiative 연구의 반대편 개념으로 해석 가능. <https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00559/116048/InSCIt-Information-Seeking-Conversations-with> | “최근 논문 몇 편 찾았다” 식으로 좁고 정확하게 답한다. | 예측 가능하고 통제하기 쉽다. | 사용자의 더 큰 상황을 놓치기 쉽다. |
| `6. Domain-risk Narrative` | 도메인별로 narrative의 1순위가 다르다. 의료는 안전, 교육은 학습 형성, 금융은 리스크/규제, 코칭은 역량과 working alliance가 우선이다. | 의료 안전 리뷰와 메타분석, OpenAI Study Mode, CFPB 금융 챗봇 보고서, coaching 연구. <https://pubmed.ncbi.nlm.nih.gov/37203638/> <https://pmc.ncbi.nlm.nih.gov/articles/PMC6118869/> <https://pubmed.ncbi.nlm.nih.gov/41183242/> <https://openai.com/index/chatgpt-study-mode//> <https://www.consumerfinance.gov/data-research/research-reports/chatbots-in-consumer-finance/chatbots-in-consumer-finance/> <https://www.sciencedirect.com/science/article/pii/S1071581921001634> | 의료는 “응급 여부 확인과 한계 고지”가 먼저, 교육은 “정답 대신 유도 질문”, 금융은 “정확성 한계와 손실 가능성”, 코칭은 “강점·행동실험·추적”이 먼저 나온다. | 도메인 적합성과 안전성이 높다. | 범용 에이전트는 모드 전환 설계가 복잡해진다. |
| `7. Affective / Empathic Narrative` | 감정 인식이 되면 정보 framing이 내용 중심에서 `정서 조절 + 정보 전달`로 바뀐다. Picard 계열 affective computing은 컴퓨팅이 emotion을 인식·이해·표현·영향 줄 수 있어야 자연스러운 상호작용이 된다고 본다. | MIT Media Lab 자료와 최근 ECA 연구. <https://www.media.mit.edu/publications/affective-computing-for-hci/> <https://www.penguinrandomhouse.com/books/662203/affective-computing-by-rosalind-w-picard/> <https://www.sciencedirect.com/science/article/pii/S1071581925001429> | 사용자가 조급하면 요약 먼저, 불안하면 불확실성과 한계를 먼저 설명하고 속도를 늦춘다. | 관계 품질, 수용성, 이탈 방지에 강하다. | 감정 오인과 조작적 UX 위험이 있다. |
**도메인별 narrative 패턴**
- 의료: `triage-first narrative`. 안전, 위험 신호, 한계 고지, 인간 전문가 이관이 먼저다.
- 교육: `Socratic scaffolding narrative`. 바로 답을 주기보다 목표·수준 확인, 질문, 힌트, 점진적 구조화를 우선한다.
- 금융: `risk-disclosure narrative`. 수익보다 정확성 한계, 규제성 정보, 인간 검토 필요성을 먼저 둔다.
- 코칭: `capability/strength-based narrative`. 문제 진단보다 강점, 자기효능감, 작은 실행, 추적 관계를 먼저 둔다.
**실제 서비스 비교**
이 비교는 공식 기능 설명을 바탕으로 한 추론이다.
| 서비스 | context framing 특징 | narrative 경향 |
|---|---|---|
| `ChatGPT` | 프로젝트 메모리는 같은 프로젝트 대화/파일만 우선 참조하고, personality와 study mode를 별도로 얹는다. <https://help.openai.com/articles/10169521> <https://help.openai.com/en/articles/11899719-customizing-you> <https://openai.com/index/chatgpt-study-mode//> | `프로젝트-문맥 중심 + 선택적 persona/mode 전환`. 연구 작업에는 가장 “워크스페이스형” framing을 만들기 쉽다. |
| `Microsoft Copilot` | Work/Web 토글, notebook references, goal-context-expectations-source 프레임이 명시적이다. <https://support.microsoft.com/en-us/topic/how-copilot-chat-works-with-and-without-a-microsoft-365-copilot-license-5810b659-fbe0-48ee-9fe6-d731fe86cdeb> <https://support.microsoft.com/en-us/topic/how-microsoft-365-copilot-notebooks-works-4071d73d-8bdd-478f-8968-8dc1d7c3d43e> <https://support.microsoft.com/en-us/topic/learn-about-copilot-prompts-f6c3b467-f07c-4db1-ae54-ffac96184dd5> | `업무 산출물 중심`. 대화보다 일감과 자료 경계를 분명히 하는 framing이 강하다. |
| `Google Gemini` | past chats personalization, personal instructions, Gems로 응답 방식을 커스터마이즈하고, past chats 사용 여부를 표시한다. <https://support.google.com/gemini/answer/15637730> <https://support.google.com/gemini/answer/15146780> | `개인화 중심`. 사용자 습관과 개인 맥락을 전면에 두는 narrative에 유리하다. |
**예시 입력에 적용**
사용자: “추천 시스템에서 diversity-accuracy tradeoff 관련 최근 논문 찾아줘”  
맥락: 3일 전 fairness 탐색, diversity metrics 정리 약속 미이행
가장 좋은 narrative는 `JTBD + Proactive + Research-domain frontstage disclosure` 조합이다.
추천 framing:
- “지금 일은 단순 논문 검색이 아니라 fairness 탐색에서 diversity tradeoff 쪽으로 연구 초점을 이동하는 작업”으로 읽는다.
- 먼저 `미이행 약속 복구`를 frontstage에 짧게 언급한다.
- 그 뒤 `최근 논문 수집`, `diversity metrics 복습`, `fairness와의 연결고리`를 3단 구조로 제안한다.
- proactive하되 결정은 사용자에게 남긴다.
예시 톤:
- “3일 전 fairness 맥락을 이어서 보면, 지금 필요한 건 최근 논문 수집만이 아니라 diversity metrics 공백을 메우며 tradeoff 축을 재정렬하는 일이다. 먼저 최근 논문을 훑고, 이어서 metrics 기준표를 복구하는 흐름이 가장 자연스럽다.”
**설계 결론**
- 좋은 AI 동료 narrative는 “친근한 말투”보다 `상황 모델링`이 먼저다.
- UX 차이를 가장 크게 만드는 축은 `situation 읽기`, `visibility 조절`, `initiative balance`, `domain risk order`다.
- 연구/지식작업용 에이전트라면 기본값은 `JTBD 상황 읽기 + 얕은 proactive + frontstage로 근거와 다음 단계 공개`가 가장 균형이 좋다.
원하면 다음 단계로 바로 이어서 정리할 수 있다.
1. 이 리서치를 `Mirror Mind용 narrative design principle` 문서 초안으로 재구성
2. 위 7개 방식을 `평가 기준표`로 바꿔서 에이전트 응답 품질 루브릭 작성
3. 예시 입력을 포함해 `narrative pattern library` 10개로 확장
129,501
기준일은 2026-03-20이다. 아래는 UX/서비스 디자인 관점에서 본 대화형 AI의 narrative 구성 방식 리서치다. 서비스별 framing 비교는 공식 문서에 나온 `memory / grounding / personalization / mode` 설명을 바탕으로 한 추론임을 명시한다.
**핵심**
Narrative는 단순한 말투가 아니라, `무엇을 현재 상황으로 간주하는가`, `무엇을 전면에 드러내고 무엇을 숨기는가`, `누가 대화의 initiative를 쥐는가`, `어떤 리스크를 먼저 프레이밍하는가`의 설계 문제다.
| 방식 | 정의 | 실제 서비스/근거 | AI 동료 적용 시 UX 차이 | 장점 | 단점 |
|---|---|---|---|---|---|
| `1. JTBD Situation Framing` | 사용자의 행동은 제품 속성보다 `진전이 필요한 구체적 상황`에 의해 결정된다는 관점이다. Christensen 쪽 JTBD 자료는 사람들이 “particular circumstances” 안에서 progress를 추구한다고 본다. | Christensen Institute의 JTBD 설명, milkshake 사례 계열 자료. <https://www.christenseninstitute.org/wp-content/uploads/2020/05/Curriculum-Conundrum-3.16-update.pdf> | 같은 요청도 “논문 찾아줘”가 아니라 “며칠 전 fairness를 보다가 diversity로 넘어왔고, 미이행 약속이 있으며, 지금은 literature scan이 급한 상황”으로 읽는다. 응답이 검색 결과 나열에서 `연구 상황 정리 + 다음 행동 제안`으로 바뀐다. | 사용자의 실제 맥락과 행동 동기를 잘 포착한다. | 잘못 읽으면 과잉추론이 된다. |
| `2. Frontstage/Backstage Narrative` | 서비스 블루프린트에서 frontstage는 사용자가 보는 서사, backstage는 내부 판단·검색·정리·검증 프로세스다. line of visibility를 어디에 두느냐가 narrative를 결정한다. | Shostack 전통과 최신 UX 설명. <https://doi.org/10.1108/EUM0000000004799> <https://www.interaction-design.org/literature/topics/frontstage-and-backstage> | AI가 “내가 지금 기억과 최근 검색을 교차확인하고 있다”를 frontstage에 노출하면 신뢰와 예측 가능성이 높아진다. 반대로 backstage를 숨기면 더 매끈하지만 블랙박스처럼 느껴질 수 있다. | 신뢰, 통제감, 오류 복구에 유리하다. | 지나치게 드러내면 장황하고 기계적이다. |
| `3. Persona-driven Framing` | personality traits는 단순 톤이 아니라 `무엇을 먼저 보고 어떤 형태로 말할지`를 정한다. | ChatGPT personality 공식 문서. <https://help.openai.com/en/articles/11899719-customizing-you> | 같은 사실도 “분석가형”은 분류·제약·근거를 먼저, “코치형”은 목표·장애물·다음 행동을 먼저 프레이밍한다. | 일관된 경험, 관계 형성에 강하다. | 과도하면 고정 캐릭터가 맥락보다 우선한다. |
| `4. Proactive Narrative` | 시스템이 목표를 위해 conversation direction을 일부 리드한다. proactive dialogue survey는 agent가 system-side target 달성을 위해 대화 방향을 이끈다고 정의한다. | IJCAI proactive dialogue survey, mixed-initiative 연구. <https://www.ijcai.org/proceedings/2023/738> <https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00559/116048/InSCIt-Information-Seeking-Conversations-with> | “최근 fairness를 봤으니 diversity-accuracy tradeoff로 이어서 정리하겠다. 미이행했던 diversity metrics부터 복구할까?”처럼 선제 제안을 한다. | 협업감, 흐름 유지, 맥락 전환 비용 감소. | 오지랖, 주도권 침해 위험이 있다. |
| `5. Reactive Narrative` | 현재 요청에만 반응하고 사용자가 준 문제 정의를 거의 그대로 따른다. | mixed-initiative 연구의 반대편 개념으로 해석 가능. <https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00559/116048/InSCIt-Information-Seeking-Conversations-with> | “최근 논문 몇 편 찾았다” 식으로 좁고 정확하게 답한다. | 예측 가능하고 통제하기 쉽다. | 사용자의 더 큰 상황을 놓치기 쉽다. |
| `6. Domain-risk Narrative` | 도메인별로 narrative의 1순위가 다르다. 의료는 안전, 교육은 학습 형성, 금융은 리스크/규제, 코칭은 역량과 working alliance가 우선이다. | 의료 안전 리뷰와 메타분석, OpenAI Study Mode, CFPB 금융 챗봇 보고서, coaching 연구. <https://pubmed.ncbi.nlm.nih.gov/37203638/> <https://pmc.ncbi.nlm.nih.gov/articles/PMC6118869/> <https://pubmed.ncbi.nlm.nih.gov/41183242/> <https://openai.com/index/chatgpt-study-mode//> <https://www.consumerfinance.gov/data-research/research-reports/chatbots-in-consumer-finance/chatbots-in-consumer-finance/> <https://www.sciencedirect.com/science/article/pii/S1071581921001634> | 의료는 “응급 여부 확인과 한계 고지”가 먼저, 교육은 “정답 대신 유도 질문”, 금융은 “정확성 한계와 손실 가능성”, 코칭은 “강점·행동실험·추적”이 먼저 나온다. | 도메인 적합성과 안전성이 높다. | 범용 에이전트는 모드 전환 설계가 복잡해진다. |
| `7. Affective / Empathic Narrative` | 감정 인식이 되면 정보 framing이 내용 중심에서 `정서 조절 + 정보 전달`로 바뀐다. Picard 계열 affective computing은 컴퓨팅이 emotion을 인식·이해·표현·영향 줄 수 있어야 자연스러운 상호작용이 된다고 본다. | MIT Media Lab 자료와 최근 ECA 연구. <https://www.media.mit.edu/publications/affective-computing-for-hci/> <https://www.penguinrandomhouse.com/books/662203/affective-computing-by-rosalind-w-picard/> <https://www.sciencedirect.com/science/article/pii/S1071581925001429> | 사용자가 조급하면 요약 먼저, 불안하면 불확실성과 한계를 먼저 설명하고 속도를 늦춘다. | 관계 품질, 수용성, 이탈 방지에 강하다. | 감정 오인과 조작적 UX 위험이 있다. |
**도메인별 narrative 패턴**
- 의료: `triage-first narrative`. 안전, 위험 신호, 한계 고지, 인간 전문가 이관이 먼저다.
- 교육: `Socratic scaffolding narrative`. 바로 답을 주기보다 목표·수준 확인, 질문, 힌트, 점진적 구조화를 우선한다.
- 금융: `risk-disclosure narrative`. 수익보다 정확성 한계, 규제성 정보, 인간 검토 필요성을 먼저 둔다.
- 코칭: `capability/strength-based narrative`. 문제 진단보다 강점, 자기효능감, 작은 실행, 추적 관계를 먼저 둔다.
**실제 서비스 비교**
이 비교는 공식 기능 설명을 바탕으로 한 추론이다.
| 서비스 | context framing 특징 | narrative 경향 |
|---|---|---|
| `ChatGPT` | 프로젝트 메모리는 같은 프로젝트 대화/파일만 우선 참조하고, personality와 study mode를 별도로 얹는다. <https://help.openai.com/articles/10169521> <https://help.openai.com/en/articles/11899719-customizing-you> <https://openai.com/index/chatgpt-study-mode//> | `프로젝트-문맥 중심 + 선택적 persona/mode 전환`. 연구 작업에는 가장 “워크스페이스형” framing을 만들기 쉽다. |
| `Microsoft Copilot` | Work/Web 토글, notebook references, goal-context-expectations-source 프레임이 명시적이다. <https://support.microsoft.com/en-us/topic/how-copilot-chat-works-with-and-without-a-microsoft-365-copilot-license-5810b659-fbe0-48ee-9fe6-d731fe86cdeb> <https://support.microsoft.com/en-us/topic/how-microsoft-365-copilot-notebooks-works-4071d73d-8bdd-478f-8968-8dc1d7c3d43e> <https://support.microsoft.com/en-us/topic/learn-about-copilot-prompts-f6c3b467-f07c-4db1-ae54-ffac96184dd5> | `업무 산출물 중심`. 대화보다 일감과 자료 경계를 분명히 하는 framing이 강하다. |
| `Google Gemini` | past chats personalization, personal instructions, Gems로 응답 방식을 커스터마이즈하고, past chats 사용 여부를 표시한다. <https://support.google.com/gemini/answer/15637730> <https://support.google.com/gemini/answer/15146780> | `개인화 중심`. 사용자 습관과 개인 맥락을 전면에 두는 narrative에 유리하다. |
**예시 입력에 적용**
사용자: “추천 시스템에서 diversity-accuracy tradeoff 관련 최근 논문 찾아줘”  
맥락: 3일 전 fairness 탐색, diversity metrics 정리 약속 미이행
가장 좋은 narrative는 `JTBD + Proactive + Research-domain frontstage disclosure` 조합이다.
추천 framing:
- “지금 일은 단순 논문 검색이 아니라 fairness 탐색에서 diversity tradeoff 쪽으로 연구 초점을 이동하는 작업”으로 읽는다.
- 먼저 `미이행 약속 복구`를 frontstage에 짧게 언급한다.
- 그 뒤 `최근 논문 수집`, `diversity metrics 복습`, `fairness와의 연결고리`를 3단 구조로 제안한다.
- proactive하되 결정은 사용자에게 남긴다.
예시 톤:
- “3일 전 fairness 맥락을 이어서 보면, 지금 필요한 건 최근 논문 수집만이 아니라 diversity metrics 공백을 메우며 tradeoff 축을 재정렬하는 일이다. 먼저 최근 논문을 훑고, 이어서 metrics 기준표를 복구하는 흐름이 가장 자연스럽다.”
**설계 결론**
- 좋은 AI 동료 narrative는 “친근한 말투”보다 `상황 모델링`이 먼저다.
- UX 차이를 가장 크게 만드는 축은 `situation 읽기`, `visibility 조절`, `initiative balance`, `domain risk order`다.
- 연구/지식작업용 에이전트라면 기본값은 `JTBD 상황 읽기 + 얕은 proactive + frontstage로 근거와 다음 단계 공개`가 가장 균형이 좋다.
원하면 다음 단계로 바로 이어서 정리할 수 있다.
1. 이 리서치를 `Mirror Mind용 narrative design principle` 문서 초안으로 재구성
2. 위 7개 방식을 `평가 기준표`로 바꿔서 에이전트 응답 품질 루브릭 작성
3. 예시 입력을 포함해 `narrative pattern library` 10개로 확장
