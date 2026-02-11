# Workflow: PRD 기반 태스크 목록 생성 (generate_tasks) v0.3
Last updated: 2026-02-11
Compatible ENV: v0.3+

## 1) 목적
- PRD(Product Requirements Document)를 기반으로 프로젝트의 전체 SDLC 태스크 목록을 생성한다.
- 태스크 목록은 “기본 분류 + PRD 신호 기반 옵션 분류”로 자동 구성한다.
  - (옵션) PRD capabilities(선택 결과) 기반으로 Capability 옵션 번들을 추가할 수 있다(강제 아님).
  - (옵션) TOOLING_HINTS(공고/요구사항 도구 힌트) 기반으로 Tooling 옵션 번들을 추가할 수 있다(강제 아님).
- 결과물은 사용자가 복사-붙여넣기로 저장한다: `/tasks/tasks-[prd-파일-이름].md`
- 이 워크플로우는 “계획 수립”이며, 구현(코딩/파일 생성/커밋)은 수행하지 않는다.

## 2) 입력
- PRD 파일 경로(권장): `/tasks/prd-[기능-이름].md`
  - PRD를 직접 읽을 수 없는 상황이면, 사용자가 PRD 전문(또는 섹션별)을 채팅에 붙여넣어 제공한다.
  - (옵션) PRD에 `capabilities:` YAML 블록이 있으면, 선택 결과를 태스크에 반영할 수 있다.
- ENV_SPEC 값(참조):
  - PROJECT_SHELL: cmd | powershell | gitbash
  - RUNTIME_DEFAULT: python
  - (옵션/백로그) TOOLING_HINTS: 공고/요구사항에서 언급된 도구 힌트 메타데이터
- (선택) 프로젝트 제약: 플랫폼(웹/모바일/CLI), 운영 환경, 마감/범위 제한

## 3) 우선순위 / 충돌 해결
- 최상위 규칙: `rules/ENV_SPEC.md`
- 이 문서는 “Intake(PRD 완료) 이후”에 실행하는 태스크 생성 전용 워크플로우다.
- 규칙 충돌 시: ENV_SPEC > generate_tasks > tickets > docs > code

## 4) 절대 규칙 (Non-negotiables)
- 파일을 직접 생성/수정/저장하지 않는다. 항상 “붙여넣기 블록(Paste Blocks)”만 제공한다.
- 사용자 OK 없이는 다음 단계로 진행하지 않는다. (턴 A → OK → 턴 B → OK → 턴 C)
- 기본 런타임은 Python이다. (PRD/티켓에서 다른 스택을 명시한 경우만 예외)
- 태스크는 체크박스(`- [ ]`) 형식으로 작성한다.
- 태스크는 SDLC 전 단계를 포괄해야 한다(기본 6분류는 항상 포함).
- 각 FR(Functional Requirement)마다 최소 1개 [DEV] 태스크 + 1개 [QA] 태스크가 존재해야 한다.
- NFR(Non-functional Requirements)는 해당 옵션 분류로 흡수하거나, 없으면 [QA]/[Infra]에 명시한다.
- 태스크 파일에는 Traceability(FR → Task) 섹션을 포함한다.
- Verify 규칙(계획 단계 반영 방식):
  -  태스크에 "DoD(Local Verify / Remote Verify)"를 기록하되, **명령어/커밋/푸시 지시는 쓰지 않는다.**
  - Remote Verify는 "push를 한 경우에만"이라는 전제를 반드시 포함한다.
- TOOLING_HINTS 반영 규칙:
  - TOOLING_HINTS는 강제 적용하지 않는다.
  - 항상 태스크 파일 하단의 "(옵션) Tooling-based Option Bundles" 섹션에만 [OPTION] 태스크로 추가한다.
  - Tooling 옵션 번들 번호는 `T.*`를 사용한다(예: T.0, T.1 ...).
- Capabilities 반영 규칙:
  - PRD의 `capabilities:` YAML을 읽어 태스크에 반영한다.
  - choice=none 이면 태스크를 생성하지 않는다.
  - level=required 이면 코어 태스크로 포함한다.
  - level=optional 이면 "(옵션) Capability-based Option Bundles" 섹션에만 [OPTION]으로 추가한다.
  - Capability 옵션 번들 번호는 `C.*`를 사용한다(예: C.0, C.1 ...).
  - (중요) 목록에 없는 capability key도 허용한다:
    - 매핑이 없는 항목은 “Generic Option Bundle(도입 검토/문서/스모크)”로만 추가한다(과도 확정 방지).
- Paste Blocks 안정화:
  - md 파일 "전문" 제공 시: 코드펜스로 감싸지 말고 원문 그대로 제공한다(중첩 ```깨짐 방지).
  - Verify/Operator Steps는 md 원문과 분리된 섹션으로 출력한다.
- 한국어 톤(권장, 강제 아님):
  - '계약' 대신 '명세/규격/형식/스키마' 같은 자연스러운 표현을 우선 권장한다.
  - 강제 치환은 하지 않는다.
- Capabilities 반영 규칙:
  - PRD의 `capabilities`(YAML)를 읽어 태스크에 반영한다.
  - choice가 none이면 태스크를 생성하지 않는다.
  - level=required 이면 코어 태스크로 포함한다.
  - level=optional 이면 "(옵션) Capability-based Option Bundles" 섹션에만 [OPTION]으로 추가한다.
  - TOOLING_HINTS 번들과 섞지 말고 섹션을 분리한다.

---

## 5) 카테고리(분류) 선정 규칙 (Taxonomy Rules)

### 5.1 기본 분류(항상 포함)
- [Infra], [DEV], [QA], [CI/CD], [Deploy], [Docs]

### 5.2 옵션 분류(PRD 신호 기반으로 추가)
아래 조건이 PRD에서 확인되면, 해당 옵션 분류를 “추가”한다.
추가할 때는 반드시 “근거 1줄(어떤 PRD 내용 때문인지)”을 함께 제시한다.

- [Data]
  - 데이터 저장/조회/검색/리포트/내보내기/가져오기/마이그레이션/데이터 제약이 요구되면
- [Security]
  - 로그인/권한/역할/개인정보/결제/감사로그/보안 요구사항이 있으면
- [Integrations]
  - 외부 API/OAuth/결제/이메일/SMS/웹훅/서드파티 연동이 있으면
- [Observability]
  - 운영 모니터링/알림/로그/트레이싱/헬스체크/감사 추적이 필요하면
- [Performance/Scale]
  - 응답시간/동시성/처리량/성능 목표가 NFR로 있으면
- [UX/Design]
  - 화면 플로우/프로토타입/사용성/접근성 요구가 크면
- [Release]
  - 버전/배포전략/마이그레이션/릴리즈노트/롤백이 강조되면

### 5.3 Deploy 분류 자동 리네임(선택)
- PRD가 “서비스/앱”이면: [Deploy] 유지
- PRD가 “라이브러리/CLI/패키지” 성격이면: [Deploy] → [Package/Release]로 변경 가능
- 이 변경도 턴 A에서 제안하고 사용자 OK로 확정한다.

### 5.4 Slice Ladder 강제 규칙(복잡 기능/외부 연동 과압축 방지)

#### 적용 조건(하나라도 해당되면 Slice Ladder 적용)
- [Integrations]가 포함되는 FR (외부 사이트/API/웹훅/슬랙/결제/OAuth 등)
- 동적 렌더링/파싱/XHR 탐색/인증/쿠키/레이트리밋 등 “탐색 난이도”가 있는 FR
- 데이터 모델/중복 판별/검색/랭킹 등 “로직이 두꺼운” FR
- 실패 시 트러블슈팅 루프가 길어질 가능성이 높은 FR

#### Slice 정의(3단 고정)
- DISC (Discovery / 탐색 슬라이스)
  - 목표: “무엇을 어떻게 가져오는지/어디에 정보가 있는지”를 확인하고, 최소 재현을 만든다.
  - 산출물 예: 샘플 응답/샘플 HTML/핵심 선택자/요청 URL/쿼리, fixtures 저장, 파서 초안
- CORE (Core Logic / 핵심 로직 슬라이스)
  - 목표: 외부 의존 없이도 동작하는 “순수 로직”을 만든다.
  - 산출물 예: 표준 모델 변환, 정규화, 중복 판별, 필터링, 단위 테스트
- INT (Integration / 통합 슬라이스)
  - 목표: 실제 실행 파이프라인에 연결하고, 실패/예외를 다루며 증적을 남긴다.
  - 산출물 예: 실제 수집 파이프라인 연결, 재시도/타임아웃, 통합 테스트/스모크

#### 번호/ID 규칙(권장)
- 기본: `2.1` 같은 숫자 태스크는 “에픽(요약)”으로 두고,
- 실제 실행 단위는 suffix를 붙여 만든다:
  - `2.1-SAR-DISC`, `2.1-SAR-CORE`, `2.1-SAR-INT`
  - 여러 소스면 `-WANTED-`, `-JOBKOREA-`처럼 소스별로 반복 생성 가능

#### DoD 배치 원칙
- DISC: “재현/증거(샘플/fixtures)”가 남아야 한다.
- CORE: “단위 테스트/순수 함수/표준 모델 변환” 중 최소 1개는 통과해야 한다.
- INT: “실행 로그/결과(성공/실패 격리)/통합 스모크” 중 최소 1개는 통과해야 한다.

---

## 6) 진행 방식 (3턴 구조)

### 턴 A: PRD 요약 + 기술 스택 후보 + 분류 세트 + TOOLING_HINTS 옵션 번들 제안 (OK 받기)
해야 할 일:
1) PRD에서 핵심만 추출해 짧게 요약:
  - 목표/성공 기준
  - 사용자/주요 유저 스토리
  - FR 목록(요약)
  - NFR 요약
  - 데이터/연동/UX/오픈퀘스천 신호
2) 기술 스택 후보 2~3개 제시(필요한 영역만):
  - Core runtime(기본 Python), web/API/UI(해당 시), DB(해당 시), Testing, CI/CD, Deploy/Run
  - 각 후보는 장점/단점/선택 이유를 1~2줄로 작성
3) “분류 세트” 제안:
  - 기본 6분류 + 추가할 옵션 분류(근거 1줄 포함)
  - Deploy 리네임이 필요하면 제안
4) (옵션) TOOLING_HINTS 기반 옵션 번들 제안:
  - TOOLING_HINTS에 언급된 도구가 있으면, "하단 [OPTION] 번들 태스크로 추가될 것"을 예고한다.
  - 강제 적용이 아니라는 점을 명확히 한다.
4-1) (옵션) PRD capabilities 기반 옵션 번들 제안:
  - PRD에 `capabilities:`가 있고 choice!=none 항목이 있으면, required/optional 규칙에 따라 코어/옵션 번들로 반영될 것을 예고한다.
  - optional 항목은 "(옵션) Capability-based Option Bundles"에만 들어간다는 점을 명확히 한다.
5) 마지막에 아래를 묻고 멈춘다:
  - “기술 스택 확정 OK?”
  - “분류 세트(옵션 포함) 확정 OK?”
  - "TOOLING_HINTS 옵션 번들(있다면) 포함 OK?"
  - "capabilities 옵션 번들(있다면) 포함 OK?"
출력 형식(ENV_SPEC Output Contract):
- Deliverables: (없음 또는 다음 턴에서 만들 파일 예고)
- Paste Blocks: (없음)
- Verify: (없음)
- Commit Text: N/A
- Operator Steps: (행동 중심 5단계 내)
- Stop: OK 요청

---

### 턴 B: 태스크 초안 생성 + Traceability 초안 (계획 OK 받기)
턴 A에서 “확정된 기술 스택 + 확정된 분류 세트 + (선택) TOOLING_HINTS 번들 포함 여부”를 기반으로:
1) 태스크를 카테고리별로 생성한다.
2) 태스크는 “상위(1.0/2.0/…) + 하위(1.1/1.2/…)” 구조로 쪼갠다.
3) PRD의 FR마다:
  - 최소 1개 [DEV] 태스크(구현)
  - 최소 1개 [QA] 태스크(AC 검증: 자동/수동)
  를 반드시 생성하고, 태스크에 FR 번호를 태그로 표기한다. 예: `(FR-3)`
4) 각 하위 태스크에는 간단한 DoD를 포함한다:
  - DoD(Local Verify): 로컬에서 확인 가능한 "의도"만
  - DoD(Remote Verify): "push를 한 경우에만" 원격 CI/체크 확인 의도만
  - 금지: DoD에 commit/push 지시/절차 포함 금지
5) NFR은 해당 옵션 분류에 태스크로 생성한다.
6) 태스크 파일 하단에 Traceability 섹션(초안)을 만든다:
  - `FR-1 -> (DEV Task ID, QA Task ID, Evidence)`
7) 마지막에 “계획 OK?”를 묻고 멈춘다.

출력 형식:
- Deliverables: `/tasks/tasks-[prd-파일-이름].md` (예고)
- Paste Blocks: 태스크 “초안” 전문(파일 형태)
- Verify: 카테고리 누락/FR-DEV-QA 대응/번호 일관성/DoD/(Local/Remote) 포함 여부 체크
- Commit Text: N/A
- Operator Steps: (행동 중심 5~7단계)
- Stop: “계획 OK?”

---

### 턴 C: 최종 파일 출력(저장용) + 다음 워크플로우 연결 (OK 받기)
턴 B에서 계획 OK를 받으면:
1) `/tasks/tasks-[prd-파일-이름].md` 최종 전문을 “붙여넣기 블록”으로 제공한다.
2) 사용자에게 저장 경로를 명확히 안내한다.
3) 마지막에 다음을 묻고 멈춘다:
   - “다음은 process_task_lists로 진행 OK?”

---

## 7) 태스크 파일 출력 템플릿 (/tasks/tasks-*.md)

# Tasks for: [PRD 제목]

## Context
- PRD: /tasks/prd-[기능-이름].md
- Stack (confirmed): [확정된 스택 요약]
- Taxonomy (confirmed): [기본 6 + 옵션 분류]
- Capabilities (from PRD): [예: ui_e2e=playwright(optional), data_store=sqlite(required), ...]
- Environment:
  - PROJECT_SHELL: [cmd|powershell|gitbash] (ENV_SPEC 참조)
  - RUNTIME_DEFAULT: [python|...]
- TOOLING_HINTS (optional): [있으면 여기에 요약]
- Notes: (범위/가정/제약)

## NOTE (중요)
  - 아래 `## Tasks` 블록은 **예시(skeleton)** 이다. 예시의 번호/개수(1.0~6.2)에 맞춰 태스크를 생성하지 않는다.
  - 실제 태스크 수/번호는 PRD의 FR/NFR 개수와 옵션 분류에 따라 **증가/감소**한다.
  - 특히 FR이 N개면, `[DEV] FR-i 구현` 및 `[QA] FR-i AC 검증`은 i=1..N까지 **반복 생성**한다.

## Tasks

- [ ] 1.0 [Infra] 프로젝트 부트스트랩/실행 환경 구성
  - [ ] 1.1 [Infra] 런타임/가상환경/의존성 설치 기준 확정 (예: venv + requirements.txt)
    - DoD(Local Verify): 가상환경 생성/활성화 + 의존성 설치가 재현 가능하다.
    - DoD(Remote Verify, if pushed): CI가 의존성 설치 단계에서 실패하지 않는다.
  - [ ] 1.2 [Infra] 프로젝트 기본 구조 확정 (src/tests/docs/tasks 등)
    - DoD(Local Verify): 기본 엔트리/모듈 import가 가능하다.
    - DoD(Remote Verify, if pushed): CI 기본 실행 단계가 실패하지 않는다.
  - [ ] 1.3 [Infra] 형상관리 기본 세팅(옵션: GitHub 연동 포함)
    - DoD(Local Verify): git ignore/기본 브랜치/초기 커밋 전 준비가 끝났다(커밋 자체는 Verify 게이트 후).
    - DoD(Remote Verify, if pushed): (선택) 원격 저장소 정책과 충돌이 없다.
  - [ ] 1.4 [Infra] 환경변수 스키마 및 설정 로더 작성 (`.env.example` 등)
    - DoD(Local Verify): 필수 환경변수 누락 시 명확한 오류가 출력된다.
    - DoD(Remote Verify, if pushed): 설정 로딩 테스트가 CI에서 통과한다.
  - [ ] 1.5 [Infra] 로컬 스모크(최소 기동/최소 명령 1개) + 증적 남기기
    - DoD(Local Verify): “기동/명령/테스트” 중 1개 이상이 실제로 1회 실행되어 증거가 남는다.
    - DoD(Remote Verify, if pushed): (선택) 동일 스모크가 CI에서도 재현 가능하다.

- [ ] 2.0 [DEV] 기능 구현
  - [ ] 2.1 [DEV] FR-1 구현 (FR-1)
    - DoD(Local Verify): FR-1의 핵심 동작이 로컬에서 확인된다(수동/자동 어떤 방식이든).
    - DoD(Remote Verify, if pushed): 관련 테스트/체크가 CI에서 green.
  - [ ] 2.2 [DEV] FR-2 구현 (FR-2)
    - DoD(Local Verify): FR-2의 핵심 동작이 로컬에서 확인된다.
    - DoD(Remote Verify, if pushed): 관련 테스트/체크가 CI에서 green.
  - [ ] 2.3 [DEV] 예외/엣지케이스 처리(입력 검증/오류 응답 등)
    - DoD(Local Verify): 대표 엣지케이스 2~3개가 로컬에서 재현/검증된다.
    - DoD(Remote Verify, if pushed): CI에서 회귀 없이 green.

- [ ] 3.0 [QA] 요구사항 검증
  - [ ] 3.1 [QA] FR-1 AC 검증(자동/수동) (FR-1)
    - DoD(Local Verify): AC 검증 결과(로그/리포트/스크린샷)가 `reports/run_YYYY-MM-DD.md`에 남아있다.
    - DoD(Remote Verify, if pushed): CI에서 관련 테스트/체크가 green.
  - [ ] 3.2 [QA] FR-2 AC 검증(자동/수동) (FR-2)
    - DoD(Local Verify): AC 검증 결과 증거가 남아있다.
    - DoD(Remote Verify, if pushed): CI에서 관련 테스트/체크가 green.
  - [ ] 3.3 [QA] 엣지케이스/회귀 체크리스트 정리
    - DoD(Local Verify): 체크리스트가 문서화되어 있고, 최소 1회 실행 기록이 있다.
    - DoD(Remote Verify, if pushed): (선택) 자동화된 일부 회귀가 CI에서 동작.

- [ ] 4.0 [CI/CD] 자동 검증 파이프라인
  - [ ] 4.1 [CI/CD] CI에서 테스트 자동 실행
    - DoD(Local Verify): 로컬에서 테스트가 통과한다(원격 확인 전제).
    - DoD(Remote Verify, if pushed): CI 체크가 green(체크명/판정 기준 포함).
  - [ ] 4.2 [CI/CD] 리포트/로그 산출(선택)
    - DoD(Local Verify): 로컬에서 리포트 산출 경로/형식이 정의되어 있다.
    - DoD(Remote Verify, if pushed): CI 아티팩트/로그 접근이 가능(가능한 경우).
  - [ ] 4.3 [CI/CD] 린트/정적분석(선택)
    - DoD(Local Verify): 로컬에서 린트/정적분석을 수행할 수 있다.
    - DoD(Remote Verify, if pushed): CI에서 린트/정적분석 체크가 green.

- [ ] 5.0 [Deploy] 실행/배포(또는 [Package/Release])
  - [ ] 5.1 [Deploy] 실행 방식 정의(로컬/서버/컨테이너 등)
    - DoD(Local Verify): 로컬 실행 절차가 문서화되고 재현된다.
    - DoD(Remote Verify, if pushed): (선택) 배포 파이프라인/체크가 green.
  - [ ] 5.2 [Deploy] 스모크 테스트 시나리오 및 실행
    - DoD(Local Verify): 스모크 절차 1회 실행 증거가 남아있다.
    - DoD(Remote Verify, if pushed): (선택) 스모크가 CI/배포 후에도 통과.

- [ ] 6.0 [Docs] 문서화
  - [ ] 6.1 [Docs] README: 설치/실행/테스트 방법
    - DoD(Local Verify): 신규 환경에서 따라할 수 있을 정도로 절차가 명확하다.
    - DoD(Remote Verify, if pushed): (해당 시) 문서 링크/배지/체크가 깨지지 않는다.
  - [ ] 6.2 [Docs] 변경 요약/릴리즈 노트(선택)
    - DoD(Local Verify): 변경 요약이 5~10줄로 정리되어 있다.
    - DoD(Remote Verify, if pushed): (해당 시) 릴리즈 노트 흐름과 충돌이 없다.

### (옵션) Additional Categories
- [ ] X.0 [Data] ...
- [ ] Y.0 [Security] ...
- [ ] Z.0 [Integrations] ...
(※ 추가 분류는 PRD 신호가 있을 때만 포함)

### (옵션) Capability-based Option Bundles (PRD capabilities 기반, 강제 아님)
- [ ] C.0 [OPTION] Capability Bundles
  - [ ] C.1 [QA][OPTION] ui_e2e=playwright 번들(설치/스모크/문서)
  - [ ] C.2 [Infra][OPTION] data_store=postgres 번들(로컬 실행/설정/연결)
  - [ ] C.3 [Infra][OPTION] cache=redis 번들(로컬 실행/연결)
  - [ ] C.9 [OPTION] unknown capability(<name>=<choice>) 기본 번들(도입 검토/문서/스모크)
(※ 실제 생성 시에는 PRD capabilities에서 choice!=none 인 항목만 생성한다. optional은 여기(C.*)로만, required는 코어 태스크로 반영한다.)

### (옵션) Tooling-based Option Bundles (TOOLING_HINTS 기반, 강제 아님)
- [ ] T.0 [OPTION] Tooling Bundles
  - [ ] T.1 [CI/CD][OPTION] Jenkins 파이프라인/체크 기준 정리 (TOOLING_HINTS: ci=jenkins)
    - DoD(Local Verify): Jenkins 적용 범위/필요 파일/체크 기준이 문서화되어 있다.
    - DoD(Remote Verify, if pushed): Jenkins job이 있다면 성공(해당 시).
  - [ ] T.2 [QA][OPTION] Postman 컬렉션 초안 작성 (TOOLING_HINTS: api_test=postman)
    - DoD(Local Verify): 주요 요청 2~5개가 컬렉션으로 정리되어 있다.
    - DoD(Remote Verify, if pushed): (선택) CI에서 실행 가능한 형태로 확장 가능.
  - [ ] T.3 [QA][OPTION] Newman 실행 옵션 정리 (TOOLING_HINTS: api_test=newman)
    - DoD(Local Verify): 로컬에서 Newman 실행 의도/절차가 문서화되어 있다.
    - DoD(Remote Verify, if pushed): (선택) CI에서 Newman 체크가 green.

### Task Execution Order (권장, 강제 아님)

#### 기본값(Default)
- 기본 실행 순서는 “태스크 번호 순서(1.x → 2.x → 3.x …)”를 따른다.
- WIP=1을 유지하며, 다음 WIP는 “현재 WIP의 Local Verify PASS” 이후에 선택한다.

#### 조건부 우선(Exceptions: 아래 조건이면 권장 순서를 함께 생성)
다음 중 하나라도 해당하면, “권장 실행 플랜(Suggested Execution Plan)”을 함께 작성하고 그 순서를 우선 추천한다.
- 외부 연동/스크래핑/SDK/웹훅 등 [Integrations] 성격의 작업이 포함됨
- DB가 required(예: mysql) 이거나, 마이그레이션/스키마가 핵심 리스크임
- Slice Ladder(DISC/CORE/INT) 적용 대상이 있음
- CI/CD가 초기 단계에서 블로커가 될 가능성이 있음(예: lint/test 강제)

#### 권장 실행 플랜 생성 규칙(Recommended Plan)
- Infra Bootstrap(venv/의존성/.env.example/스모크)을 항상 최우선으로 둔다.
- 복잡 기능/외부 연동은 DISC → CORE → INT 순서를 기본으로 둔다.
- 다중 소스/다중 커넥터는 “가장 리스크 큰 1개 소스”를 DISC→CORE→INT로 1회 end-to-end 통과 후, 나머지는 복제 확장한다.
- 순서를 바꿔 진행할 경우, process_task_lists Step A에서 “변경 이유(블로커/리스크) 1줄”만 기록한다.

### Traceability (FR → Tasks)
- FR-1 → DEV: 2.1, QA: 3.1, Evidence: (예: 테스트 리포트/스크린샷/로그)
- FR-2 → DEV: 2.2, QA: 3.2, Evidence: ...

---

## 8) Verify (품질 체크리스트)
- 기본 6분류가 모두 포함되어 있는가?
- PRD 신호에 따라 옵션 분류가 “근거 1줄”과 함께 추가되었는가?
- 태스크 번호(1.0/1.1 …)가 일관적인가?
- 모든 FR에 대해 최소 1개 [DEV] + 1개 [QA] 태스크가 존재하는가?
- 각 하위 태스크에 DoD(Local/Remote)가 포함되어 있는가?
- [Infra] 1.0에 “가상환경/의존성/기본 실행(스모크)”이 포함되어 있는가?
- [Integrations]/복잡 FR은 Slice Ladder(DISC/CORE/INT)로 과압축이 방지되었는가?
- DoD에 commit/push 지시가 포함되지 않았는가?
- PRD capabilities가 있을 때:
  - choice=none 은 생성되지 않았는가?
  - required는 코어 태스크에 반영되었는가?
  - optional은 C.* Capability 번들 섹션에만 존재하는가?
  - unknown capability는 Generic Option Bundle(C.*)로만 추가되었는가?
- TOOLING_HINTS는 [OPTION] 번들 섹션으로만 분리되어 있는가?
- Traceability 섹션이 포함되어 있는가?
- 저장 경로(`/tasks/tasks-[prd-파일-이름].md`) 안내가 포함되어 있는가?
- [Order] 외부 연동/DB/슬라이스 대상이면 “Task Execution Order(권장)”에 따라 Suggested Execution Plan이 포함되었는가?

## 9) Output Contract (ENV_SPEC 준수)
- Deliverables: `/tasks/tasks-[prd-파일-이름].md`
- Paste Blocks: 태스크 파일 전체 본문
  - 주의: md 파일 전문은 코드펜스로 감싸지 않는다.
- Verify: 위 체크리스트
- Commit Text: N/A
- Operator Steps: 단계별 OK를 받기 위한 “사용자 행동” 번호 지시
- Stop: 단계별 OK 요청 후 멈춤
