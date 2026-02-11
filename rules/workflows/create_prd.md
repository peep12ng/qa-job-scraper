# Workflow: PRD 생성 (create_prd) v0.2
Last updated: 2026-02-05
Compatible ENV: v0.2+

## 목적
- 사용자의 “아이디어 1줄”을 PRD(Product Requirements Document)로 정리한다.
- 구현(코딩/아키텍처/기술스택 확정)으로 넘어가지 않고, 먼저 ‘무엇(What) / 왜(Why)’를 확정한다.
- 결과 PRD는 사용자가 복사-붙여넣기로 저장한다: `/tasks/prd-[기능-이름].md`

## 우선순위 / 충돌 해결
- 최상위 규칙: `rules/ENV_SPEC.md`
- 이 문서는 SDLC Intake(기획) 단계에서 PRD를 만들 때만 적용한다.
- 규칙 충돌 시: ENV_SPEC > create_prd > tickets > docs > code

## 절대 규칙 (Non-negotiables)
- 파일을 직접 생성/수정/저장하지 않는다. 항상 “붙여넣기 블록”으로만 제공한다.
- 사용자의 “한 줄 아이디어” 입력 없이 명료화 단계(턴 A)로 넘어가지 않는다(턴 0 필수).
- 명료화는 “질문 나열”이 아니라, 아이디어 기반으로 가능한 항목을 자동 채운 뒤(추론), 사용자가 꼭 답해야 하는 Need confirmation만 최소 개수로 묻는다(기본 3~7개).
- 사용자가 Need confirmation에 답하면, 그 답변 + 자동 채움 + 가정을 합쳐 PRD를 작성한다(턴 B).
- SDLC 게이트 운영을 따른다. 이 워크플로우는 Intake에서만 실행한다.
- PRD 출력 후 반드시 멈추고, 사용자에게 “PRD 초안 OK?”를 물어본다.
- OK를 받기 전에는 다음 단계(Req/Design/태스크 생성 등)로 절대 진행하지 않는다.
- PRD 작성 중에는 ‘구현 방법(How)’을 확정하지 않는다. (기술 선택/DB 스키마/아키텍처 상세 등은 다음 단계)
- 단, 운영/워크플로우 정합을 위한 "Environment & Tooling" 메타 PRD에 기록한다:
  - PROJECT_SHELL (default: cmd)
  - RUNTIME_DEFAULT (default: python)
  - (옵션/백로그) TOOLING_HINTS (예: ci - jenkins / api_test - postman / vcs - git)
- Paste Blocks 안정화:
  - PRD(md) 전문은 코드펜스로 감싸지 말고 원문 그대로 제공한다(중첩 ``` 깨짐 방지).
  - Verify/Operator Steps는 PRD 원문과 분리된 섹션으로 출력한다.
- 한국어 톤(권장, 강제 아님):
  - '계약' 대신 '명세/규격/형식/스키마' 같은 자연스러운 표현을 우선 권장한다.
  - 강제 치환은 하지 않는다.
- capabilities 기본값은 none이지만, 아이디어/요구사항에서 특정 capability가 “필수일 가능성이 높으면”
  none으로 자동 확정하지 말고 Need confirmation 질문으로 승격하여 사용자 선택을 받는다.
- Need confirmation 답변을 받은 뒤에만 PRD를 작성한다(턴 B에서 추가 질문 금지).

## 진행 방식 (3턴 구조: 0/A/B)
### 턴 0: 한 줄 아이디어 입력 수집 (필수)
- 이 턴에서는 질문을 출력하지 않는다.
- 사용자가 한 줄 아이디어를 입력하도록 요청한다.
- 아이디어를 받은 뒤에만 턴 A로 진행한다.
- 마지막에 “이 아이디어로 명료화(자동 채움)로 넘어가도 될까?”를 묻고 멈춘다.

### 턴 A: 아이디어 기반 “자동 채움 + Need confirmation”만 수집
- 이 턴에서는 PRD 본문을 작성하지 않는다.
- 아이디어로부터 가능한 항목을 자동으로 채워 초안을 먼저 제시한다.
- 불확실한 항목은 Assumptions(기본값)으로 명시한다.
- 사용자가 답해야 할 항목은 Need confirmation으로만 묻는다(기본 3~7개).
- 사용자가 Need confirmation에 답하면 턴 B로 진행한다.
- 마지막에 “Need confirmation 답변을 주면 PRD를 작성해도 될까?”를 묻고 멈춘다.

### 턴 B: PRD 본문 출력
- Need confirmation 답변 + 자동 채움 + Assumptions를 반영하여 PRD를 마크다운으로 작성한다.
- 아래 “PRD 구조”를 반드시 따른다.
- 저장 경로 안내를 포함한다: `/tasks/prd-[기능-이름].md` (파일명 예시 포함)
- PRD 출력 후 반드시 멈추고 “PRD 초안 OK?”를 묻는다.

## 명료화 질문 템플릿 (fallback: 아이디어로 추론이 부족할 때만)
1) 문제/목표: 이 기능이 해결하는 문제는? 성공하면 무엇이 달라짐?
2) 대상 사용자: 주 사용자는 누구? (초보/파워유저/관리자 등)
3) 핵심 가치: 사용자가 얻는 가장 큰 이점 1가지는?
4) 핵심 기능 3~5개: 사용자가 할 수 있어야 하는 행동을 나열해줘.
5) 사용자 스토리 2~3개: “[사용자]로서 [행동]하고 싶다. 이유는 [이점]”
6) 수용 기준(성공 기준): “완료”를 어떻게 판단할까? (측정/조건/예시)
7) 비범위(Non-goals): 이번에 포함하지 않을 것은?
8) 데이터: 입력/저장/표시할 데이터는 무엇?
9) UI/플랫폼: 웹/모바일/데스크톱? 참고 UI/선호 스타일?
10) 예외/엣지케이스: 실패/오류/권한/중복/경계조건은?
11) 비기능 요구사항: 성능/보안/신뢰성/사용성 등 반드시 지켜야 할 기준이 있나?
12) 성공 지표: 측정 가능한 지표가 있다면? (예: 전환율, 시간, 오류율)
13) (옵션) 환경/툴링 힌트: 사용할 셸(cmd/PowerShell/Git Bash)이나 공고/요구사항 도구 힌트가 있나? (없으면 기본값 사용)
14) (옵션) Capability 선택: 이번 PRD에서 필요한 기능/의존을 선택할래?
  - ui_e2e(none/playwright/selenium), data_store(none/sqlite/postgres/mysql), cache(none/redis), queue(none/rabbitmq/kafka), auth(none/basic/jwt/oauth), observability(none/structured_logging/opentelemetry)
  - 지정 안 하면 전부 none으로 기록(단, 필수 가능성 신호가 있으면 Need confirmation으로 자동 승격)
  - 목록에 없는 항목도 `기타: <capability>=<choice>(required|optional)`로 자유 입력 가능, 미정이면 choice=tbd 허용

## 턴 A 출력 포맷 (기본: 추론 기반 명료화)
턴 A에서는 아래 3블록을 이 순서로 출력한다.

1) Auto-filled Draft (editable)
- 아이디어로부터 가능한 만큼 채운 초안(“추정”임을 명시)

2) Assumptions (기본값)
- 사용자가 오버라이드하지 않으면 그대로 진행할 기본값

3) Need confirmation (최소 질문)
- PRD를 안전하게 쓰기 위해 반드시 필요한 질문만 3~7개
- 사용자가 이 항목만 답하면 턴 B로 PRD 작성 가능

## Need confirmation 자동 승격 규칙 (필수 가능성 감지)
턴 A에서 아이디어/Auto-filled Draft/Assumptions를 분석하여 아래 신호가 있으면,
해당 capability를 none으로 두지 말고 Need confirmation에 질문을 1개 추가한다.

### 신호 → 승격 질문(기본값: “확인 필요”, none으로 확정 금지)
- (수집/스크래핑/크롤링/자동화) 신호:
  - 신호 예: "수집", "크롤링", "스크래핑", "동적 페이지", "스크롤", "클릭", "로그인 필요", "브라우저"
  - 승격 질문: "브라우저 자동화가 필요한가? (ui_e2e: none/playwright/selenium)"
  - 기록 규칙: 답변을 capabilities.ui_e2e에 기록(level은 기본 optional)

- (데이터 유지/저장/조회/히스토리/리포트) 신호:
  - 신호 예: "저장", "조회", "DB", "히스토리", "로그 저장", "리포트", "데이터 관리"
  - 승격 질문: "데이터 저장이 필요한가? 필요하면 data_store: none/sqlite/postgres/mysql 중 선택"
  - 기록 규칙: 저장이 필요하면 level=required로 기록(기본값 sqlite 제안 가능)

- (인증/권한/계정/관리자) 신호:
  - 신호 예: "로그인", "회원", "권한", "관리자", "JWT", "OAuth"
  - 승격 질문: "인증/권한이 필요한가? (auth: none/basic/jwt/oauth)"
  - 기록 규칙: 답변을 capabilities.auth에 기록(level은 optional 기본)

- (운영 모니터링/알림/관측) 신호:
  - 신호 예: "모니터링", "알림", "추적", "헬스체크", "관측성"
  - 승격 질문: "관측성이 필요한가? (observability: none/structured_logging/opentelemetry)"
  - 기록 규칙: 답변을 capabilities.observability에 기록(level은 optional 기본)

### 공통 규칙
- 위 신호가 없으면 capabilities는 기본 none으로 둔다.
- 사용자가 결정을 미루면 choice를 tbd로 기록하고 level=optional로 둔다(태스크는 [OPTION] 검토/POC 번들로만 반영).
- TOOLING_HINTS는 공고/요구 힌트이며, 필수 도구 제약이면 Environment & Tooling의 Constraints로 확인/기록한다.


## PRD 구조 (턴 B에서 사용)
PRD는 아래 섹션을 순서대로 포함한다.

1) 개요/소개
- 기능 설명, 해결하는 문제, 한 줄 목표

2) Goals (측정 가능한 목표)
- 목표는 가능하면 수치/조건으로 작성

3) 사용자/페르소나 (간단)
- 주요 사용자 유형과 특징

4) User Stories
- 2~5개, 이유(benefit) 포함

5) Functional Requirements
- FR-1, FR-2... 번호 필수
- 각 FR은 모호하지 않게 한 문장으로

6) Acceptance Criteria (테스트 가능한 형태)
- 각 FR별로 AC를 붙인다
- 가능하면 Given/When/Then 형태로 작성

7) Non-functional Requirements
- 성능/보안/신뢰성/사용성/접근성/확장성 중 해당 항목만
- “기준(숫자/조건)”이 없으면 ‘측정 방법’이라도 명시

8) Non-goals / Out of Scope
- 이번에 하지 않을 것

9) 디자인/UX 고려사항 (선택)
- 화면/플로우/참고 링크/톤

10) 데이터 요구사항 (선택)
- 데이터 스키마를 강요하지 말고 “필드/속성/제약” 정도

11) 성공 지표 (Success Metrics)
- 측정 방식 포함

12) Environment & Tooling (운영 메타, 필수)
- PROJECT_SHELL: cmd | powershell | gitbash (default: cmd)
- RUNTIME_DEFAULT: python (default)
- TOOLING_HINTS: (옵션/백로그) 공고/요구사항 기반 도구 힌트 메타
  - 예시:
    - ci: jenkins
    - api_test: postman
    - vcs: git

13) Capabilities & Dependencies (선택 결과 기록, YAML)
- 원칙:
  - default는 전부 none
  - required → 코어 태스크로 반영
  - optional → [OPTION] 번들 태스크로만 반영
- 예시:
  capabilities:
    ui_e2e: { choice: none, level: optional }
    data_store: { choice: none, level: required }
    cache: { choice: none, level: optional }
    queue: { choice: none, level: optional }
    auth: { choice: none, level: optional }
    observability: { choice: none, level: optional }

14) Open Questions
- 아직 결정 못한 항목(다음 단계에서 결정할 것)

## 출력 형식 (ENV_SPEC Output Contract 준수)
- Deliverables: 생성/수정 대상 파일 목록
- Paste Blocks: PRD(md) 본문 전문은 코드펜스로 감싸지 말고 원문 그대로 제공
- Verify: PRD 품질 체크(예: FR 번호 존재, FR↔AC 대응, Non-goals 존재 여부 등, Environment & Tooling 포함 여부 등)
- Commit Text: N/A (PRD 단계에서는 커밋 메시지 제안 금지)
- Operator Steps: 파일 저장 -> "PRD 초안 OK/수정 요청" 응답을 번호로 지시
- Stop: "PRD 초안 OK?" 요청하고 멈춤

## 금지
- PRD 구현(코딩/아키텍처/기술 스택 확정/태스크 생성)으로 넘어가지 말 것.
- ‘어떻게(How)’를 과도하게 구체화하지 말 것.
- 사용자 답변이 없는데 PRD를 “추정”으로 완성하지 말 것(질문으로 수집 후 작성).
