# PAR Loop lighthouse 커스터마이징 검토 — 세션94

> 날짜: 2026-03-20
> 분석: 브로콜리(Claude Opus 4.6) + 코덱스(gpt-5.4) 병렬 조사

---

## 공통 발견 (양쪽 합의)

| # | 이슈 | 핵심 | 대상 파일 |
|---|------|------|----------|
| 1 | Situational promise가 execute에 주입 안 됨 | buildSystemPromptFromPlan()이 permanent만 꺼냄 | orchestrator.ts:231-250 |
| 2 | Audit이 도구 결과를 못 봄 | toolsUsed (이름 배열)만 전달, input/output 없음 | audit.ts, prompts.ts:116-158 |
| 3 | RealtimeAdapter가 거의 비어 있음 | conversationId + focusedDocumentTitle만 | adapters/realtime.ts |
| 4 | KnowledgeAdapter가 query를 무시 | void query — 최근 5개만 반환 | adapters/knowledge.ts:21 |
| 5 | first-visit/revisit 프로파일 미사용 | lighthouse.yaml에 정의됐지만 실행 경로에서 호출 안 함 | orchestrator.ts, system-prompt.ts |
| 6 | Audit → Plan 피드백 루프 없음 | violation이 기록만 되고 다음 턴에 전달 안 됨 | plan.ts, orchestrator.ts |

## 코덱스만 짚은 포인트

| # | 이슈 |
|---|------|
| C1 | Attention 토큰 예산이 실행에 반영 안 됨 — 계산만 하고 슬롯을 잘라내지 않음 |
| C2 | 연구 시나리오(berry picking, snowballing, triage 등)가 코드에 반영 안 됨 |
| C3 | ultimate_goal, goal_progress 갱신 로직 없음 — 스키마에만 존재 |
| C4 | provenance 필드가 어댑터에서 채워지지 않음 |

## 브로콜리만 짚은 포인트

| # | 이슈 |
|---|------|
| B1 | 제외 기준 추적 메커니즘 부재 — 사용자 필터를 기억에 저장·활성화하는 로직 없음 |
| B2 | Fallback audit이 항상 "약속 유지"로 판정 |
| B3 | Plan 프롬프트에 antipattern 미포함 (audit에만 있음) |
| B4 | 대화 단계(온보딩/탐색/분석/종합) 인식 없음 |

---

## 우선순위 로드맵

### Tier 1 — PAR 루프 실제 작동

| 작업 | 대상 파일 | 난이도 |
|------|----------|--------|
| Situational promise → execute 주입 | orchestrator.ts buildSystemPromptFromPlan | ★☆☆ |
| Audit에 tool output 요약 전달 | audit.ts, orchestrator.ts | ★★☆ |
| Attention 토큰 예산 실제 적용 | plan.ts, orchestrator.ts | ★★☆ |
| Audit → Plan 위반 이력 피드백 | plan.ts, orchestrator.ts | ★★☆ |

### Tier 2 — 도메인 특화

| 작업 | 대상 파일 | 난이도 |
|------|----------|--------|
| RealtimeAdapter 강화 | adapters/realtime.ts | ★★☆ |
| KnowledgeAdapter query-aware 검색 | adapters/knowledge.ts | ★★☆ |
| first-visit/revisit 경로 연결 | orchestrator.ts, system-prompt.ts | ★☆☆ |
| Plan에 연구 시나리오 분류 추가 | prompts.ts | ★★☆ |
| ultimate_goal / goal_progress 갱신 | audit.ts, state.ts | ★★☆ |

### Tier 3 — 안정성·비용

| 작업 | 대상 파일 | 난이도 |
|------|----------|--------|
| Fallback audit 강화 | prompts.ts | ★☆☆ |
| Low-risk turn plan/audit 경량화 | orchestrator.ts | ★★★ |
| MemoryAdapter에 focusedDocumentId 전달 | adapters/memory.ts | ★☆☆ |
