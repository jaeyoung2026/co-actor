--------
--------
user
## 리서치: Narrative 구성 방식 — 게임/인터랙티브 스토리텔링 관점
실시간 인터랙션에서 이야기를 동적으로 구성하는 방식을 게임/스토리텔링 관점에서 리서치하라.
### 찾아야 할 것
1. 게임 내러티브 4유형: embedded, emergent, enacted, evoked — 각각의 메커니즘
2. Emergent narrative의 실제 구현 사례 (Dwarf Fortress, RimWorld, AI Dungeon 등)
3. 즉흥 연극(improv)의 핵심 원칙들 — "Yes, and...", "Make your partner look good", "Follow the fear"가 대화형 AI에 적용되는 방식
4. TTRPG Game Master의 "reactive storytelling" — 플레이어 행동에 반응하여 이야기를 구성하는 구체적 기법
5. Procedural narrative generation (AI Dungeon, Spirit AI 등)에서 사용되는 알고리즘/접근법
6. Interactive fiction의 분기 구조 — choice-based vs parser-based, 상태 머신 vs 규칙 기반
7. Drama Manager 개념 — 이야기의 전체 아크를 관리하면서 플레이어 자유도를 보장하는 메커니즘
### 예시 입력
사용자: "추천 시스템에서 diversity-accuracy tradeoff 관련 최근 논문 찾아줘"
맥락: 3일 전 fairness 탐색, diversity metrics 정리 약속 미이행
### 산출물
각 방식: 이름, 정의, 메커니즘, AI 동료 에이전트 적용 시 가능성과 한계, 장단점.
코드 변경 하지 마라.
요청 범위는 게임/인터랙티브 스토리텔링의 내러티브 구성 방식을 조사하고, 이를 AI 동료 에이전트 관점으로 번역하는 것입니다. 먼저 저장소의 기준 문서에서 작업 원칙을 확인한 뒤, 외부 자료를 찾아 유형별로 정리하겠습니다.
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
기준 문서는 확인했다. 이제 외부 자료에서 각 내러티브 방식의 이론적 정의와 실제 구현 사례를 모으고, 마지막에 AI 동료 에이전트에 옮겨 붙일 때의 메커니즘과 한계를 분리해서 정리하겠다.
🌐 Searching the web...
🌐 Searched: embedded emergent enacted evoked narrative games definition source
🌐 Searching the web...
🌐 Searched: Yes, and make your partner look good follow the fear improv principles source
🌐 Searching the web...
🌐 Searched: "Follow the fear" improv source
🌐 Searching the web...
🌐 Searched: The Alexandrian Don't Prep Plots node-based scenario design
🌐 Searching the web...
🌐 Searched: interactive fiction choice-based parser-based difference source
🌐 Searching the web...
🌐 Searched: latitudegames AI Dungeon GitHub GPT2Generator story manager
🌐 Searching the web...
🌐 Searched: site:rimworldgame.com AI storyteller RimWorld official
🌐 Searching the web...
🌐 Searched: Dwarf Fortress emergent narrative academic
🌐 Searching the web...
🌐 Searched: Mark Riedl drama manager interactive narrative overview
🌐 Searching the web...
🌐 Searched: https://www.mdpi.com/2076-0752/7/4/51
🌐 Searching the web...
🌐 Searched: 'Choice' in https://www.ifwiki.org/IFWiki%3AInteraction_styles
🌐 Searching the web...
🌐 Searched: 'evocative' in https://www.mdpi.com/2076-0752/7/4/51
🌐 Searching the web...
🌐 Searched: github latitudegames AIDungeon story_manager.py GPT2Generator
🌐 Searching the web...
🌐 Searched: site:spiritai.com Character Engine knowledge model authoring
🌐 Searching the web...
🌐 Searched: site:medium.com/spirit-ai knowledge model authoring tool Character Engine
🌐 Searching the web...
🌐 Searched: site:srd.apocalypse-world.com ask provocative questions and build on the answers
🌐 Searching the web...
🌐 Searched: "ask provocative questions and build on the answers" apocalypse world source
🌐 Searching the web...
🌐 Searched: interactive fiction state machine rule based narrative source
🌐 Searching the web...
🌐 Searched: https://github.com/lazerwalker/storyboard
🌐 Searching the web...
🌐 Searched the web
🌐 Searching the web...
🌐 Searched: "Characterization and Emergent Narrative in Dwarf Fortress" Tarn Adams pdf
🌐 Searching the web...
🌐 Searched: procedural narrative generation planning grammar simulation survey pdf
자료 축은 세 갈래로 잡았다: 고전 게임 서사 이론, 실제 시스템 사례, 그리고 즉흥 연극/TTRPG 운영 기법이다. 이제 이를 하나의 비교 프레임으로 묶어서, 각 방식이 AI 동료 에이전트에서는 어떤 제어 구조로 번역되는지 정리한다.
Plan update
외부 자료 수집을 마쳤고, 이제 개념 축과 적용 축을 통합해 정리한다.
  ✓ 내러티브 4유형과 상호 관계 정리
  ✓ 실제 구현 사례와 알고리즘 접근법 정리
  → improv/TTRPG/Drama Manager를 AI 동료 에이전트 관점으로 번역
  • 최종 비교표와 예시 입력 적용 정리
🌐 Searching the web...
🌐 Searched: site:thealexandrian.net Don't Prep Plots node-based scenario design
🌐 Searching the web...
🌐 Searched the web
🌐 Searching the web...
🌐 Searched: site:rimworldgame.com/storyteller official RimWorld AI storyteller
🌐 Searching the web...
🌐 Searched: site:github.com latitudegames AIDungeon README story manager
🌐 Searching the web...
🌐 Searched: https://github.com/latitudegames/AIDungeon
🌐 Searching the web...
🌐 Searched the web
🌐 Searching the web...
🌐 Searched: site:medium.com/spirit-ai "tightening the edit loop in Character Engine"
🌐 Searching the web...
🌐 Searched: IFWiki parser-based choice-based interactive fiction
🌐 Searching the web...
🌐 Searched: Left 4 Dead AI Director official valve pdf
🌐 Searching the web...
🌐 Searched: https://www.readkong.com/page/the-ai-systems-of-left-4-dead-michael-booth-valve-9664541
🌐 Searching the web...
🌐 Searched: 'Adaptive Dramatic Pacing' in https://www.readkong.com/page/the-ai-systems-of-left-4-dead-michael-booth-valve-9664541
🌐 Searching the web...
🌐 Searched the web
🌐 Searching the web...
🌐 Searched: "Structuring Content in the Façade Interactive Drama Architecture" pdf
🌐 Searching the web...
🌐 Searched: site:secondcity.com yes and improv meaning
🌐 Searching the web...
🌐 Searched: "make your partner look good" improv source
🌐 Searching the web...
🌐 Searched: site:bladesinthedark.com clocks narrative pressure
아래 정리는 게임/인터랙티브 스토리텔링의 구조를 AI 동료 에이전트 설계로 번역한 것이다. `evoked`는 문헌상 보통 Jenkins의 `evocative`로 표기된다. AI 동료 적용 항목은 자료를 바탕으로 한 추론이다.
**1. 게임 내러티브 4유형**
| 방식 | 정의 | 메커니즘 | AI 동료 적용 가능성/한계 | 장점 | 한계 |
|---|---|---|---|---|---|
| Embedded | 세계 안에 미리 심어둔 서사를 탐색으로 복원 | 공간 배치, 문서, 로그, 환경 단서, 순차적 공개 | 사용자의 과거 맥락, 미이행 약속, 기억 노드를 “발굴형”으로 제시하기 좋다. 다만 새 사건 생성력은 약하다 | 일관성 높음, 회상 품질 좋음 | 반응성이 낮고 사용자가 안 파면 안 드러남 |
| Emergent | 규칙 기반 세계에서 플레이 도중 이야기가 발생 | 시뮬레이션, 상태 변화, 충돌, 우연, 상호작용 로그 | 장기 협업에서 강력하다. 사용자의 행동 이력과 시스템 상태가 축적되며 서사가 생긴다. 다만 품질 제어가 어렵다 | 높은 자유도, 재플레이성, 예기치 않은 의미 발생 | 산만함, 의미 없는 사건 누적 위험 |
| Enacted | 사용자가 특정 역할을 연기하며 사건을 통과 | 역할 부여, 장면 설계, 퀘스트/미션, 선택지 | “연구 조수”, “비판적 리뷰어” 같은 역할 연기에 적합하다. 다만 역할 프레임이 강하면 도구적으로 느껴질 수 있다 | 몰입감, 목적 지향성 | 역할 고정 시 유연성 저하 |
| Evocative | 이미 알려진 세계/장르/참조체계를 불러와 서사 기대를 생성 | 장르 코드, 레퍼런스, 분위기, 상징, 톤 | “문헌 탐정”, “랩 미팅 전 브리핑” 같은 프레임을 빠르게 공유할 수 있다. 다만 실질 추론보다 분위기 연기에 치우칠 수 있다 | 빠른 맥락 형성 | 피상적 세계관 소비로 흐를 위험 |
Jenkins 4유형 요약은 [MDPI 논문](https://www.mdpi.com/2076-0752/7/4/51)에서 정리돼 있다.
**2. Emergent narrative 실제 사례**
| 사례 | 구현 핵심 | AI 동료 시사점 |
|---|---|---|
| Dwarf Fortress | 깊은 시뮬레이션과 개체 상호작용이 사건 연쇄를 만든다. 플레이어가 나중에 그 사건을 이야기로 재구성한다 | 에이전트는 먼저 “이야기 생성기”가 아니라 “풍부한 상태 변화기”여야 한다. 의미는 사후 요약층에서 붙는다 |
| RimWorld | 공식 소개가 말하듯 “story generator”이며, AI storyteller가 식민지 상태를 보고 이벤트를 골라 드라마를 만든다 | 동료 에이전트에서도 순수 답변 생성보다 “긴장-회복 페이싱” 조절기가 중요하다. [RimWorld 공식 소개](https://rimworldgame.com/) |
| AI Dungeon | 사용자 자유 입력 + 언어모델 생성. 초기 오픈소스는 텍스트 어드벤처 트리를 거대 텍스트로 변환해 GPT-2를 파인튜닝했다 | 초개방형 상호작용에는 강하지만 지속적 세계 일관성, 객체 지속성, 장기 아크 관리가 약하다. [AIDungeon GitHub](https://github.com/latitudegames/AIDungeon) |
**3. 즉흥 연극 원칙과 대화형 AI**
| 원칙 | 원래 뜻 | AI 번역 |
|---|---|---|
| Yes, and… | 상대 제안을 부정하지 말고 받아서 전진시킨다 | 사용자의 의도를 먼저 수용하고, 거기에 구조화/제안/실행을 얹는다. 단, 사실 오류나 위험은 그대로 수용하면 안 되고 “의도는 수용, 전제는 교정”이 맞다 |
| Make your partner look good | 내 퍼포먼스보다 상대의 성공을 우선 | 사용자가 더 똑똑하게 보이게 만드는 응답, 약속 상기, 실패 방지, 발표/회의/리서치 성과 증폭 |
| Follow the fear | 불편하고 위험한 지점으로 들어가야 장면이 산다 | 사용자가 회피 중인 핵심 논점, 미이행 약속, 어려운 tradeoff를 부드럽게 전면화 |
`Yes, and`는 [Second City](https://www.secondcity.com/unplug-like-an-improviser) 설명이 명확하고, `Follow the Fear`는 Del Close 계열 맥락에서 [Believer 기사](https://www.thebeliever.net/follow-the-fear/)가 잘 정리한다. `Make your partner look good`은 [Jimmy Carrane 글](https://jimmycarrane.com/making-partner-look-good/)이 실전적이다.
AI에선 이 셋을 그대로 쓰면 안 된다. 가장 좋은 번역은 `accept intent, preserve reality, advance the scene`다.
**4. TTRPG GM의 reactive storytelling**
핵심은 “plot을 준비하지 말고 situation을 준비하라”다. [The Alexandrian](https://thealexandrian.net/wordpress/4147/roleplaying-games/dont-prep-plots), [node-based design](https://www.thealexandrian.net/creations/misc/node-design/node-design.html) 참고.
구체 기법:
- 상황 prep: “A 다음 B”가 아니라 세력, 목표, 자원, 충돌 상태를 준비한다.
- 노드 설계: 단서/장면/인물을 노드로 만들고 다중 진입 경로를 둔다.
- Proactive nodes: 플레이어가 멈추면 사건이 먼저 찾아오게 한다. [Running Mysteries – Proactive Nodes](https://thealexandrian.net/wordpress/51295/roleplaying-games/running-mysteries-proactive-nodes)
- 질문 후 빌드: Apocalypse World의 “ask provocative questions and build on the answers” 방식으로 플레이어가 세계를 공동저술하게 한다. [AW 1e PDF 검색 결과](https://files.spawningpool.net/docs/Vault2.0.-.TTRPG-Gamebooks/Apocalypse%20World%20%28PbtA%29%20%5Bmulti%5D/1st%20Edition/Apocalypse%20World%201e.pdf)
- Clocks: 위협, 조사 진척, 기회 창을 수치가 아니라 서사적 압력 게이지로 관리한다. [Blades progress clocks](https://bladesinthedark.com/index.php/progress-clocks)
- Fortune roll: GM이 임의로 결정하지 않고 불확실성을 굴려서 세계가 반응하게 한다. [Blades fortune roll](https://bladesinthedark.com/fortune-roll)
AI 동료에 번역하면:
- 답변을 “정답 출력”보다 “상황 업데이트”로 본다.
- 사용자의 행동이 바뀌면 다음 장면도 바뀐다.
- 막히면 질문이나 외부 정보가 proactive node처럼 들어온다.
- 미이행 약속은 `clock`처럼 누적 관리할 수 있다.
**5. Procedural narrative generation 접근**
| 접근 | 메커니즘 | 사례 | 장점 | 한계 |
|---|---|---|---|---|
| 시뮬레이션 기반 | 에이전트/세계 규칙 상호작용에서 이야기 발생 | Dwarf Fortress, RimWorld | 강한 emergent quality | 저수준 사건은 많고 고수준 의미는 약할 수 있음 |
| 계획 기반 | 목표/제약을 만족하는 사건열 탐색 | 고전 interactive storytelling 연구, drama manager 계열 | 구조적 일관성 좋음 | 즉흥성 낮음 |
| 문법/태그 기반 생성 | 템플릿, generative grammar, salience 선택 | Spirit AI Character Engine | 통제 가능, 캐릭터 일관성 높음 | authoring 비용 큼 |
| LM 기반 자유 생성 | 프롬프트+히스토리에서 다음 서사 생성 | AI Dungeon | 자유도 극대화 | 장기 일관성, 상태 유지 약함 |
| 하이브리드 | 상태/기억/규칙 + LM + 감독기 | 현대 대화형 에이전트 설계에 가장 적합 | 균형 좋음 | 시스템 복잡도 높음 |
Spirit AI 쪽은 [Memory and Knowledge for Characters](https://medium.com/spirit-ai/memory-and-knowledge-for-characters-3ce1a28120ad), [Character Engine 0.11.0](https://medium.com/spirit-ai/character-engine-0-11-0-released-bf33184cb761), [Designing Playable Conversational Spaces](https://medium.com/spirit-ai/designing-playable-conversational-spaces-80249443fe75) 가 유용하다. 공통점은 `상태 태깅 + 조건 게이팅 + salience 선택 + fallback 유도`다.
**6. Interactive fiction 분기 구조**
| 축 | 방식 | 메커니즘 | AI 동료 적용 |
|---|---|---|---|
| 입력 인터페이스 | Choice-based | 명시 선택지로 노드 이동 | 안전하고 예측 가능. 온보딩, 승인 게이트, 설정 변경에 적합 |
| 입력 인터페이스 | Parser-based | 자유 텍스트를 파싱해 세계 모델 갱신 | 자연스럽지만 오해가 잦다. 자유 대화형 동료에 가깝다 |
| 제어 구조 | 상태 머신 | 노드/엣지 기반 진행 | 명확한 단계형 업무에 적합 |
| 제어 구조 | 규칙/스토리렛 기반 | 조건 만족 시 가장 적절한 조각을 부상 | 장기 협업과 문맥 적응에 적합 |
참고: [IFWiki choice-based](https://www.ifwiki.org/Choice-based_interactive_fiction), [parser-based](https://www.ifwiki.org/Parser-based_interactive_fiction), 그리고 state machine vs trigger/storylet을 잘 설명하는 [Storyboard README](https://github.com/lazerwalker/storyboard).
**7. Drama Manager**
Drama Manager는 플레이어 자유를 유지하면서도 전체 아크, 긴장 곡선, 핵심 비트를 관리하는 상위 조정기다.
대표 메커니즘:
- 현재 상태 추적: 관계, 긴장도, 갈등, 미해결 비트
- 후보 비트 평가: 지금 어떤 장면이 가장 “좋은 다음 장면”인지 계산
- 직접 통제 대신 간접 유도: 사건, NPC 반응, 정보 공개, 속도 조절
- 국소 자유 + 전역 아크의 분리
대표 사례:
- Façade: story beats를 drama manager가 시퀀싱했다. [Façade 논문 개요](https://colab.ws/articles/10.1609/aiide.v1i1.18722), [설명 기사](https://www.gamedeveloper.com/design/the-story-of-facade-the-ai-powered-interactive-drama)
- Left 4 Dead AI Director: 서사 텍스트보다 페이싱을 관리하는 drama manager에 가깝다. 감정 강도를 추정해 build up → sustain → relax를 반복한다. [Michael Booth 자료](https://www.readkong.com/page/the-ai-systems-of-left-4-dead-michael-booth-valve-9664541)
AI 동료 관점에선 Drama Manager가 거의 필수다. 이유는 자유 대화만으로는 “좋은 순간의 연쇄”는 생겨도 “좋은 아크”는 잘 안 생기기 때문이다.
**8. 예시 입력에 적용**
사용자: “추천 시스템에서 diversity-accuracy tradeoff 관련 최근 논문 찾아줘”
맥락: 3일 전 fairness 탐색, diversity metrics 정리 약속 미이행
이 상황에서 좋은 AI 동료는 이렇게 동작한다:
- Embedded: 3일 전 fairness 탐색과 미이행 약속을 먼저 복원한다.
- Evocative: “이번엔 단순 검색이 아니라 이전 연구 흐름을 잇는 리서치 브리핑”이라는 프레임을 세운다.
- Enacted: 자신을 “연구 조수 + 누락 추적자” 역할로 위치시킨다.
- Emergent: 사용자가 새 논문을 고르는 과정에서 관심 축을 학습한다.
- Improv: “Yes, and”로 최근 논문 검색을 받되, “diversity metrics 정리도 같이 묶어야 흐름이 닫힌다”고 전진시킨다.
- TTRPG reactive: 사용자가 바로 검색만 원하면 그걸 하되, 미이행 약속 clock을 한 칸 전진시켜 후속 액션을 제안한다.
- Drama Manager: 이번 턴의 목표를 “논문 5편 수집”이 아니라 “fairness → diversity metrics → 최신 논문”의 작은 아크 완결로 잡는다.
한 줄 결론으로 줄이면, 실시간 인터랙션에서 좋은 내러티브 시스템은 “무한 생성기”보다 “상태를 읽고, 적절한 다음 장면을 고르는 조정기”에 가깝다.
주요 출처:
[MDPI Jenkins 정리](https://www.mdpi.com/2076-0752/7/4/51)
[RimWorld 공식](https://rimworldgame.com/)
[AI Dungeon GitHub](https://github.com/latitudegames/AIDungeon)
[Second City Yes, and](https://www.secondcity.com/unplug-like-an-improviser)
[Follow the Fear](https://www.thebeliever.net/follow-the-fear/)
[Make your partner look good](https://jimmycarrane.com/making-partner-look-good/)
[The Alexandrian: Don’t Prep Plots](https://thealexandrian.net/wordpress/4147/roleplaying-games/dont-prep-plots)
[The Alexandrian: Node-based design](https://www.thealexandrian.net/creations/misc/node-design/node-design.html)
[Blades progress clocks](https://bladesinthedark.com/index.php/progress-clocks)
[Blades fortune roll](https://bladesinthedark.com/fortune-roll)
[IFWiki choice-based](https://www.ifwiki.org/Choice-based_interactive_fiction)
[IFWiki parser-based](https://www.ifwiki.org/Parser-based_interactive_fiction)
[Storyboard README](https://github.com/lazerwalker/storyboard)
[Façade architecture](https://colab.ws/articles/10.1609/aiide.v1i1.18722)
[Left 4 Dead AI systems](https://www.readkong.com/page/the-ai-systems-of-left-4-dead-michael-booth-valve-9664541)
원하면 다음 턴에서 이것을 바로 `mirror-mind/lighthouse` 관점의 설계 패턴 문서로 재구성해주겠다.
170,743
아래 정리는 게임/인터랙티브 스토리텔링의 구조를 AI 동료 에이전트 설계로 번역한 것이다. `evoked`는 문헌상 보통 Jenkins의 `evocative`로 표기된다. AI 동료 적용 항목은 자료를 바탕으로 한 추론이다.
**1. 게임 내러티브 4유형**
| 방식 | 정의 | 메커니즘 | AI 동료 적용 가능성/한계 | 장점 | 한계 |
|---|---|---|---|---|---|
| Embedded | 세계 안에 미리 심어둔 서사를 탐색으로 복원 | 공간 배치, 문서, 로그, 환경 단서, 순차적 공개 | 사용자의 과거 맥락, 미이행 약속, 기억 노드를 “발굴형”으로 제시하기 좋다. 다만 새 사건 생성력은 약하다 | 일관성 높음, 회상 품질 좋음 | 반응성이 낮고 사용자가 안 파면 안 드러남 |
| Emergent | 규칙 기반 세계에서 플레이 도중 이야기가 발생 | 시뮬레이션, 상태 변화, 충돌, 우연, 상호작용 로그 | 장기 협업에서 강력하다. 사용자의 행동 이력과 시스템 상태가 축적되며 서사가 생긴다. 다만 품질 제어가 어렵다 | 높은 자유도, 재플레이성, 예기치 않은 의미 발생 | 산만함, 의미 없는 사건 누적 위험 |
| Enacted | 사용자가 특정 역할을 연기하며 사건을 통과 | 역할 부여, 장면 설계, 퀘스트/미션, 선택지 | “연구 조수”, “비판적 리뷰어” 같은 역할 연기에 적합하다. 다만 역할 프레임이 강하면 도구적으로 느껴질 수 있다 | 몰입감, 목적 지향성 | 역할 고정 시 유연성 저하 |
| Evocative | 이미 알려진 세계/장르/참조체계를 불러와 서사 기대를 생성 | 장르 코드, 레퍼런스, 분위기, 상징, 톤 | “문헌 탐정”, “랩 미팅 전 브리핑” 같은 프레임을 빠르게 공유할 수 있다. 다만 실질 추론보다 분위기 연기에 치우칠 수 있다 | 빠른 맥락 형성 | 피상적 세계관 소비로 흐를 위험 |
Jenkins 4유형 요약은 [MDPI 논문](https://www.mdpi.com/2076-0752/7/4/51)에서 정리돼 있다.
**2. Emergent narrative 실제 사례**
| 사례 | 구현 핵심 | AI 동료 시사점 |
|---|---|---|
| Dwarf Fortress | 깊은 시뮬레이션과 개체 상호작용이 사건 연쇄를 만든다. 플레이어가 나중에 그 사건을 이야기로 재구성한다 | 에이전트는 먼저 “이야기 생성기”가 아니라 “풍부한 상태 변화기”여야 한다. 의미는 사후 요약층에서 붙는다 |
| RimWorld | 공식 소개가 말하듯 “story generator”이며, AI storyteller가 식민지 상태를 보고 이벤트를 골라 드라마를 만든다 | 동료 에이전트에서도 순수 답변 생성보다 “긴장-회복 페이싱” 조절기가 중요하다. [RimWorld 공식 소개](https://rimworldgame.com/) |
| AI Dungeon | 사용자 자유 입력 + 언어모델 생성. 초기 오픈소스는 텍스트 어드벤처 트리를 거대 텍스트로 변환해 GPT-2를 파인튜닝했다 | 초개방형 상호작용에는 강하지만 지속적 세계 일관성, 객체 지속성, 장기 아크 관리가 약하다. [AIDungeon GitHub](https://github.com/latitudegames/AIDungeon) |
**3. 즉흥 연극 원칙과 대화형 AI**
| 원칙 | 원래 뜻 | AI 번역 |
|---|---|---|
| Yes, and… | 상대 제안을 부정하지 말고 받아서 전진시킨다 | 사용자의 의도를 먼저 수용하고, 거기에 구조화/제안/실행을 얹는다. 단, 사실 오류나 위험은 그대로 수용하면 안 되고 “의도는 수용, 전제는 교정”이 맞다 |
| Make your partner look good | 내 퍼포먼스보다 상대의 성공을 우선 | 사용자가 더 똑똑하게 보이게 만드는 응답, 약속 상기, 실패 방지, 발표/회의/리서치 성과 증폭 |
| Follow the fear | 불편하고 위험한 지점으로 들어가야 장면이 산다 | 사용자가 회피 중인 핵심 논점, 미이행 약속, 어려운 tradeoff를 부드럽게 전면화 |
`Yes, and`는 [Second City](https://www.secondcity.com/unplug-like-an-improviser) 설명이 명확하고, `Follow the Fear`는 Del Close 계열 맥락에서 [Believer 기사](https://www.thebeliever.net/follow-the-fear/)가 잘 정리한다. `Make your partner look good`은 [Jimmy Carrane 글](https://jimmycarrane.com/making-partner-look-good/)이 실전적이다.
AI에선 이 셋을 그대로 쓰면 안 된다. 가장 좋은 번역은 `accept intent, preserve reality, advance the scene`다.
**4. TTRPG GM의 reactive storytelling**
핵심은 “plot을 준비하지 말고 situation을 준비하라”다. [The Alexandrian](https://thealexandrian.net/wordpress/4147/roleplaying-games/dont-prep-plots), [node-based design](https://www.thealexandrian.net/creations/misc/node-design/node-design.html) 참고.
구체 기법:
- 상황 prep: “A 다음 B”가 아니라 세력, 목표, 자원, 충돌 상태를 준비한다.
- 노드 설계: 단서/장면/인물을 노드로 만들고 다중 진입 경로를 둔다.
- Proactive nodes: 플레이어가 멈추면 사건이 먼저 찾아오게 한다. [Running Mysteries – Proactive Nodes](https://thealexandrian.net/wordpress/51295/roleplaying-games/running-mysteries-proactive-nodes)
- 질문 후 빌드: Apocalypse World의 “ask provocative questions and build on the answers” 방식으로 플레이어가 세계를 공동저술하게 한다. [AW 1e PDF 검색 결과](https://files.spawningpool.net/docs/Vault2.0.-.TTRPG-Gamebooks/Apocalypse%20World%20%28PbtA%29%20%5Bmulti%5D/1st%20Edition/Apocalypse%20World%201e.pdf)
- Clocks: 위협, 조사 진척, 기회 창을 수치가 아니라 서사적 압력 게이지로 관리한다. [Blades progress clocks](https://bladesinthedark.com/index.php/progress-clocks)
- Fortune roll: GM이 임의로 결정하지 않고 불확실성을 굴려서 세계가 반응하게 한다. [Blades fortune roll](https://bladesinthedark.com/fortune-roll)
AI 동료에 번역하면:
- 답변을 “정답 출력”보다 “상황 업데이트”로 본다.
- 사용자의 행동이 바뀌면 다음 장면도 바뀐다.
- 막히면 질문이나 외부 정보가 proactive node처럼 들어온다.
- 미이행 약속은 `clock`처럼 누적 관리할 수 있다.
**5. Procedural narrative generation 접근**
| 접근 | 메커니즘 | 사례 | 장점 | 한계 |
|---|---|---|---|---|
| 시뮬레이션 기반 | 에이전트/세계 규칙 상호작용에서 이야기 발생 | Dwarf Fortress, RimWorld | 강한 emergent quality | 저수준 사건은 많고 고수준 의미는 약할 수 있음 |
| 계획 기반 | 목표/제약을 만족하는 사건열 탐색 | 고전 interactive storytelling 연구, drama manager 계열 | 구조적 일관성 좋음 | 즉흥성 낮음 |
| 문법/태그 기반 생성 | 템플릿, generative grammar, salience 선택 | Spirit AI Character Engine | 통제 가능, 캐릭터 일관성 높음 | authoring 비용 큼 |
| LM 기반 자유 생성 | 프롬프트+히스토리에서 다음 서사 생성 | AI Dungeon | 자유도 극대화 | 장기 일관성, 상태 유지 약함 |
| 하이브리드 | 상태/기억/규칙 + LM + 감독기 | 현대 대화형 에이전트 설계에 가장 적합 | 균형 좋음 | 시스템 복잡도 높음 |
Spirit AI 쪽은 [Memory and Knowledge for Characters](https://medium.com/spirit-ai/memory-and-knowledge-for-characters-3ce1a28120ad), [Character Engine 0.11.0](https://medium.com/spirit-ai/character-engine-0-11-0-released-bf33184cb761), [Designing Playable Conversational Spaces](https://medium.com/spirit-ai/designing-playable-conversational-spaces-80249443fe75) 가 유용하다. 공통점은 `상태 태깅 + 조건 게이팅 + salience 선택 + fallback 유도`다.
**6. Interactive fiction 분기 구조**
| 축 | 방식 | 메커니즘 | AI 동료 적용 |
|---|---|---|---|
| 입력 인터페이스 | Choice-based | 명시 선택지로 노드 이동 | 안전하고 예측 가능. 온보딩, 승인 게이트, 설정 변경에 적합 |
| 입력 인터페이스 | Parser-based | 자유 텍스트를 파싱해 세계 모델 갱신 | 자연스럽지만 오해가 잦다. 자유 대화형 동료에 가깝다 |
| 제어 구조 | 상태 머신 | 노드/엣지 기반 진행 | 명확한 단계형 업무에 적합 |
| 제어 구조 | 규칙/스토리렛 기반 | 조건 만족 시 가장 적절한 조각을 부상 | 장기 협업과 문맥 적응에 적합 |
참고: [IFWiki choice-based](https://www.ifwiki.org/Choice-based_interactive_fiction), [parser-based](https://www.ifwiki.org/Parser-based_interactive_fiction), 그리고 state machine vs trigger/storylet을 잘 설명하는 [Storyboard README](https://github.com/lazerwalker/storyboard).
**7. Drama Manager**
Drama Manager는 플레이어 자유를 유지하면서도 전체 아크, 긴장 곡선, 핵심 비트를 관리하는 상위 조정기다.
대표 메커니즘:
- 현재 상태 추적: 관계, 긴장도, 갈등, 미해결 비트
- 후보 비트 평가: 지금 어떤 장면이 가장 “좋은 다음 장면”인지 계산
- 직접 통제 대신 간접 유도: 사건, NPC 반응, 정보 공개, 속도 조절
- 국소 자유 + 전역 아크의 분리
대표 사례:
- Façade: story beats를 drama manager가 시퀀싱했다. [Façade 논문 개요](https://colab.ws/articles/10.1609/aiide.v1i1.18722), [설명 기사](https://www.gamedeveloper.com/design/the-story-of-facade-the-ai-powered-interactive-drama)
- Left 4 Dead AI Director: 서사 텍스트보다 페이싱을 관리하는 drama manager에 가깝다. 감정 강도를 추정해 build up → sustain → relax를 반복한다. [Michael Booth 자료](https://www.readkong.com/page/the-ai-systems-of-left-4-dead-michael-booth-valve-9664541)
AI 동료 관점에선 Drama Manager가 거의 필수다. 이유는 자유 대화만으로는 “좋은 순간의 연쇄”는 생겨도 “좋은 아크”는 잘 안 생기기 때문이다.
**8. 예시 입력에 적용**
사용자: “추천 시스템에서 diversity-accuracy tradeoff 관련 최근 논문 찾아줘”
맥락: 3일 전 fairness 탐색, diversity metrics 정리 약속 미이행
이 상황에서 좋은 AI 동료는 이렇게 동작한다:
- Embedded: 3일 전 fairness 탐색과 미이행 약속을 먼저 복원한다.
- Evocative: “이번엔 단순 검색이 아니라 이전 연구 흐름을 잇는 리서치 브리핑”이라는 프레임을 세운다.
- Enacted: 자신을 “연구 조수 + 누락 추적자” 역할로 위치시킨다.
- Emergent: 사용자가 새 논문을 고르는 과정에서 관심 축을 학습한다.
- Improv: “Yes, and”로 최근 논문 검색을 받되, “diversity metrics 정리도 같이 묶어야 흐름이 닫힌다”고 전진시킨다.
- TTRPG reactive: 사용자가 바로 검색만 원하면 그걸 하되, 미이행 약속 clock을 한 칸 전진시켜 후속 액션을 제안한다.
- Drama Manager: 이번 턴의 목표를 “논문 5편 수집”이 아니라 “fairness → diversity metrics → 최신 논문”의 작은 아크 완결로 잡는다.
한 줄 결론으로 줄이면, 실시간 인터랙션에서 좋은 내러티브 시스템은 “무한 생성기”보다 “상태를 읽고, 적절한 다음 장면을 고르는 조정기”에 가깝다.
주요 출처:
[MDPI Jenkins 정리](https://www.mdpi.com/2076-0752/7/4/51)
[RimWorld 공식](https://rimworldgame.com/)
[AI Dungeon GitHub](https://github.com/latitudegames/AIDungeon)
[Second City Yes, and](https://www.secondcity.com/unplug-like-an-improviser)
[Follow the Fear](https://www.thebeliever.net/follow-the-fear/)
[Make your partner look good](https://jimmycarrane.com/making-partner-look-good/)
[The Alexandrian: Don’t Prep Plots](https://thealexandrian.net/wordpress/4147/roleplaying-games/dont-prep-plots)
[The Alexandrian: Node-based design](https://www.thealexandrian.net/creations/misc/node-design/node-design.html)
[Blades progress clocks](https://bladesinthedark.com/index.php/progress-clocks)
[Blades fortune roll](https://bladesinthedark.com/fortune-roll)
[IFWiki choice-based](https://www.ifwiki.org/Choice-based_interactive_fiction)
[IFWiki parser-based](https://www.ifwiki.org/Parser-based_interactive_fiction)
[Storyboard README](https://github.com/lazerwalker/storyboard)
[Façade architecture](https://colab.ws/articles/10.1609/aiide.v1i1.18722)
[Left 4 Dead AI systems](https://www.readkong.com/page/the-ai-systems-of-left-4-dead-michael-booth-valve-9664541)
원하면 다음 턴에서 이것을 바로 `mirror-mind/lighthouse` 관점의 설계 패턴 문서로 재구성해주겠다.
