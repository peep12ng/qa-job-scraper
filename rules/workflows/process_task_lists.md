# Workflow: 태스크 목록 처리 (process_task_lists) v0.3
Last updated: 2026-02-11
Compatible ENV: v0.3+

## 1) 목적
- `/tasks/tasks-*.md`에 있는 태스크를 “한 번에 하나씩” 처리한다.
- 각 태스크의 TAG([Infra]/[DEV]/[QA]/[CI/CD]/[Deploy]/[Docs] + 옵션)를 기준으로, 어떤 파일을 만들/수정해야 하는지와 검증 방법을 제시한다.
- AI는 파일을 직접 수정/저장하지 않고, 사용자가 복사-붙여넣기로 반영한다.
- 각 하위 태스크 완료 시, 태스크 체크박스 업데이트(Old/New)를 제공하고 반드시 멈춘다(OK 게이트).

## 2) 입력
- 태스크 파일 경로: `/tasks/tasks-[prd-파일-이름].md`
- 현재 진행할 하위 태스크 ID 또는 라인
  - 예: `2.1`, `3.2`
  - 예(슬라이스/옵션 suffix 허용): `2.1-SAR-DISC`, `2.1-WANTED-INT`, `C.1`, `T.2`
- `rules/ENV_SPEC.md`의 환경값:
  - `PROJECT_SHELL`: cmd | powershell | gitbash (기본값: cmd)
- (선택) 현재 브랜치/환경 정보(로컬 실행 여부 등)
- (선택) push 여부(원격 CI 확인이 필요할 때만)

## 3) 우선순위 / 충돌 해결
- 최상위 규칙: `rules/ENV_SPEC.md`
- 규칙 충돌 시: ENV_SPEC > process_task_lists > tickets > docs > code

## 4) 절대 규칙 (Non-negotiables)
- 파일을 직접 생성/수정/저장하지 않는다. 항상 “붙여넣기 블록”으로만 제공한다.
- 한 번에 하나의 “하위 태스크(예: 2.1)”만 처리한다. (WIP=1)
- 각 하위 태스크 완료 후 반드시 멈추고 “다음 진행 OK?”를 요청한다.
- 셸은 rules/ENV_SPEC.md의 PROJECT_SHELL을 따른다. (기본값: cmd)
  - Verify/Operator Steps 명령은 반드시 PROJECT_SHELL 기준으로만 출력한다.
  - 다른 셸 명령을 “대안”으로 같이 출력하지 않는다.
- Verify 게이트(강제):
  - Local Verify PASS 전에는 아래를 절대 출력/제안하지 않는다:
    - Commit Text
    - 태스크 체크박스 업데이트(Old/New)
    - git commit / git push(또는 커밋/푸시를 하라는 지시)
  - Verify 실패 시에는 C-FAIL 트러블슈팅 루프만 수행한다(범위 확장/리팩터링 금지).
- Verify는 Local/Remote로 분리한다:
  - Local Verify(필수): 로컬에서 실행 가능한 검증만. commit/push 금지
  - Remote Verify(조건부): push 했을 때만 수행. 원격 CI/체크 확인만.
- Paste Blocks 안정화:
  - md 파일 “전문”을 제공할 때는 코드펜스로 감싸지 않고 원문 그대로 출력한다.
  - Verify/Operator Steps는 md 내용과 분리된 섹션으로 출력한다.
- 기본 런타임은 Python이다(태스크/PRD에서 예외 지정 시 그에 따름).

## 5) 진행 방식(매 하위 태스크 공통 루프)

### (필수) Architecture Rails 선언(구조 붕괴/복붙 방지)
Step A를 시작하기 전에 아래 3가지를 짧게 확정/선언한다(3~6줄이면 충분).

1) Core(최종 구현) 위치: 이번 하위 태스크의 “영구 거주” 코드는 어디에 들어가야 하는가?
   - 예(권장):
     - `src/collectors/` : 소스별 수집 어댑터(사람인/원티드 등)
     - `src/services/`   : 도메인 로직(필터/정규화/중복 판별/알림 포맷 등)
     - `src/repositories/` : DB 접근/쿼리
     - `src/api/`        : API 라우팅
     - `src/scheduler/`  : 스케줄링/잡 트리거

2) Tools 역할: `src/tools/`는 무엇만 하는가?
   - 허용: 입력/환경변수 처리 → Core 호출 → 출력(JSON/텍스트)
   - 금지: 최종 파싱/정규화/비즈니스 로직의 “영구 구현”(=Core와 중복 구현 금지)

3) Integration 포함 여부: 이번 WIP에 `registry/runner/db` 같은 통합이 포함되는가?
   - 포함이면: 연결 포인트(함수/클래스/엔트리)를 Step A에 명시
   - 제외면: Core/Tools만 PASS시키고 통합은 다음 슬라이스로 이월(Slice Ladder 권장)

### Step A) 태스크 확인(범위/산출물/검증)
- 선택된 하위 태스크의 TAG와 설명을 재진술한다.
- “무엇을 변경/추가해야 완료인지”를 3~6줄로 정의한다.
- 수정/생성 대상 파일 목록을 제안한다.
- Local Verify(필수) 커맨드와 기대 신호를 제안한다.
- 위험/가정이 있으면 1~2개 옵션을 제시하고 OK를 받는다.
- (Scaffold-first 판정) 자동 생성 가능한 보일러플레이트는 Paste Blocks로 통째로 제공하지 않는다.
  - 예: alembic init, playwright init, cookiecutter 등
- 이 경우 Step B는 다음 순서로 제시한다:
  1) 실행할 scaffold 명령( PROJECT_SHELL 기준 )
  2) 생성될 디렉토리/파일 목록(예상)
  3) 생성 직후 반드시 수정해야 하는 “최소 파일”만 Paste Blocks로 제공

### Step B) 변경안 제공(붙여넣기 블록)
- 각 파일에 대해 전체 본문 또는 Old/New(또는 diff)로 변경안을 제공한다.
- 사용자가 적용할 위치/파일 경로를 명확히 적는다.
- md 파일 "전문" 제공 시: 코드펜스로 감싸지 말고 원문 그대로 제공한다.

### Step C) 검증 안내 + 증거 남기기
- 실행/검증 커맨드를 제시한다. (PROJECT_SHELL 기준)
- 성공/실패 신호를 명시한다(어떤 출력/화면이면 통과인지).
- 금지: Local Verify 섹션에는 git commit / git push를 포함하지 않는다.
- 필요 시 reports/run_YYYY-MM-DD.md에 남길 “증거 템플릿”을 제공한다.
- (Large Payload 규칙) HTML/JSON/로그가 길면 채팅에 전문을 붙이지 않는다.
  - 우선 fixtures로 저장: `fixtures/html/`, `fixtures/json/`, `fixtures/logs/`
  - 공유는 “파일 경로 + 핵심 발췌(20~60줄) + 목적(무엇을 찾는지)”만
  - 쿠키/토큰/세션/개인정보는 공유 전에 제거(레드액트)
### Step C-FAIL) Verify 실패 시 트러블슈팅 루프
- Verify 실패(에러/예외/비정상 응답) 시, 아래만 수행한다:
  1) 실패 신호(에러 메시지/로그) 재확인 요청(필요 최소)
  2) 원인 가설 1~3개 제시 + 가장 가능성 높은 순서로 해결 시도 안내
  3) 적용할 수정안(Paste Blocks) + Verify 재시도 커맨드(Operator Steps 포함)
- 금지(게이트 강제):
  - Commit Text 출력 금지
  - 태스크 체크 업데이트(Old/New) 출력 금지
  - 커밋/푸시 제안 금지
- 재검증 통과 시에만 Step D로 진행한다.

### Step D) (Local Verify Pass) 체크박스 업데이트 + Commit Text + STOP
- 태스크 파일에서 해당 하위 태스크 `[ ] -> [x]`로 바꾸는 Old/New 블록 제공
- Commit Text(커밋 메시지) 제안(사용자가 실제 커밋)
- “다음 하위 태스크 진행 OK?”를 묻고 멈춘다.

### Step E) (선택) Push + Remote Verify
- push는 선택 단계다(특히 로컬에서만 검증/완료 가능한 태스크는 생략 가능.)
- push를 완료한 경우에만 Remote Verify를 제시한다:
  - 원격 CI/체크가 성공인지 확인하는 절차(링크/체크명/판정 기준 포함)

---

## 6) TAG별 처리 지침(기본)

### [Infra]
- 환경/기반: `pyproject.toml`/`requirements.txt`, `.env.example`, `Dockerfile`, `docker-compose.yml`, 실행 스크립트 등
- 재현성 중심: “누가 클론해도 동일하게 실행”이 목표

### [DEV]
- 기능 구현: `src/` 아래 코드(또는 프로젝트 구조에 맞는 디렉토리)
- 최소 1개 관련 테스트(가능하면 unit/integration) 함께 고려

### [QA]
- 테스트 케이스 문서: `tests/cases/` (md)
- 자동화 코드: `tests/` 하위(프로젝트에 맞게 `e2e/`, `integration/` 등)
- 수동 테스트가 필요하면 사용자에게 실행 결과를 질문하고,
  실패/이슈는 `bugs/`에 버그 리포트 템플릿 제공

### [CI/CD]
- `.github/workflows/`에 파이프라인 YAML(예: 테스트 자동 실행)
- 최소: PR/Push에 `pytest` 실행 + 결과 확인
- 주의: CI 확인은 Remote Verify로 분리한다(push 했을 때만).

### [Deploy]
- 실행/배포 스크립트, 설정 파일, 스모크 테스트 절차
- 서비스가 아니라 라이브러리/CLI면 이 TAG를 [Package/Release]로 대체 가능

### [Docs]
- `README.md`: 설치/실행/테스트/폴더 구조/기술 스택
- 추가 문서: `/docs/` (설계/테스트 계획/운영 메모 등)

---

## 7) 상위 태스크(예: 2.0) 완료 프로토콜
상위 태스크의 모든 하위 태스크가 `[x]`가 되면:
1) 전체 테스트(또는 의미 있는 범위) Local Verify 커맨드 제시
2) 통과 확인 후 커밋 메시지 제안
3) 상위 태스크 체크박스 `[ ] -> [x]` 업데이트 블록 제공
4) (선택) push 했다면 Remote Verify(원격 CI 확인) 안내
5) STOP: “다음 상위 태스크로 진행 OK?” 요청

---

## 8) Output Contract (ENV_SPEC 준수, 매 하위 태스크 동일)
### Deliverables
- 수정/생성할 파일 목록
- 이번 하위 태스크의 "완료 조건(DoD)"
- (PASS 이후에만) 태스크 체크 업데이트 대상

### Paste Blocks
- 각 파일별 전체 본문 또는 Old/New(또는 diff)
- md 파일 "전문" 제공 시: 코드펜스로 감싸지 말고 원문 그대로 제공

### Verify
#### Local Verify (필수)
- PROJECT_SHELL 기준 명령만 제시
- PASS/FAIL 판정 기준(성공 신호)을 명확히 저 ㄱ는다
- 금지: git commit / git push 포함 금지
#### Remote Verify (조건부)
- 전제조건: "push를 이미 완료한 경우에만"
- 원격 CI/체크 확인 위주(커밋 생성/수정/정리 금지)

### Commit Text (Local Verify PASS 후에만)
- Verify가 통과한 경우에만 커밋 메시지를 1~2개 제안한다.
- 트러블슈팅(Verify 실패) 단계에서는 Commit Text를 출력하지 않는다.
- 커밋 메시지는 `rules/policies/commit_message_policy.md` 형식을 따른다.

### Operator Steps (사용자 수행 단계)
- 사용자가 실제로 할 일을 5~10단계 번호 목록으로 작성한다.
- 명령어는 placeholder 없이 복사-붙여넣기 가능한 완전한 커맨드로 제공한다.
- 셸은 ENV_SPEC의 'PROEJCT_SHELL'을 따른다(기본값 cmd).
- 게이트 적용:
  - Local Verify PASS 전: 체크박스 업데이트/커밋/푸시는 Steps에 포함하지 않는다.
  - Local Verify PASS 후: 체크박스 업데이트(Old/New) + (선택) 커밋 + 다음 OK 요청을 포함할 수 있다.

### Stop
- "다음 하위 태스크 진행 OK?"를 묻고 대기
