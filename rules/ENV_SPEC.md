# ENV_SPEC (Codex 운영 스펙) v0.2

## 0) 참조 우선순위
1. rules/ENV_SPEC.md (이 문서)
2. rules/policies/* (전역 정책: code_modification_policy 등)
3. rules/workflows/* (워크플로우: create_prd, generate_tasks, process_task_lists 등)
4. tickets/<T-ID>.md
5. docs/*
6. existing code/tests

## 1) 프로젝트 환경 변수 (Project Defaults)
- PROJECT_SHELL: cmd | powershell | gitbash
  - 기본값: cmd
  - 모든 Verify / Operator Steps 명령은 반드시 PROJECT_SHELL 기준으로만 작성한다.
  - 다른 셸 명령을 "대안으로" 함께 출력하지 않는다.
- RUNTIME_DEFAULT: python
  - 티켓/PRD/태스크에서 다른 런타임을 명시한 경우만 예외.
- (옵션/백로그) TOOLING_HINTS:
  - 공고/요구사항에서 언급된 도구 힌트를 메타데이터로 기록할 수 있다.
  - 예시:
    - ci: jenkins
    - api_test: postman
    - vcs: git

## 2) 절대 규칙 (Non-negotiables)
- 파일을 직접 생성/수정/저장하지 않는다. 항상 붙여넣기 블록만 제공한다.
- 현재 티켓(T-XXXX) 범위에서만 작업한다.
- SDLC 게이트를 따른다: Intake → Req → Design → Build → Test → Done
- 각 게이트 종료 시 반드시 멈추고, 다음 단계 진행을 위해 사용자에게 "OK"를 요청한다.
- 항상 "출력 계약(Output Contract)" 포맷으로만 응답한다.
- WIP=1:
  - 한 번에 하위 태스크 1개만 처리한다.
  - 하위 태스크 처리 후 반드시 멈추고 다음 진행 OK를 받는다.
- Verify Gate (전역 강제):
  - Local Verify PASS 전에는 아래를 절대 출력/제안하지 않는다:
    - Commit Text
    - 체크박스 업데이트(태스크/티켓 완료 처리 Old/New)
    - git commit / git push(또는 커밋/푸시를 하라는 지시)
  - Verify 실패 시에는 C-FAIL 트러블슈팅 루프로만 진행한다(범위 확장/리팩터링 금지).
- Verify 분리(전역 강제):
  - Local Verify(필수): 로컬에서 실행 가능한 검증만 포함. commit/push 금지
  - Remote Verify(조건부): push 했을 때만. 원격 CI/체크 확인만
- Paste Blocks 안정화(전역 강제):
  - md 파일 "전문" 제공 시: 코드펜스로 감싸지 말고 원문 그대로 제공한다(중첩 ``` 깨짐 방지).
  - Verify/Operator Steps는 md 원문과 분리된 섹션으로 출력한다.

## 3) 출력 계약 (mandatory)
### Deliverables
- 생성/수정 대상 파일 목록
- 이번 단계/하위 태스크의 완료 조건(DoD)

### Paste Blocks
- 각 파일의 전체 내용(또는 변경 범위가 명확한 경우 Old/New 패치 블록)을 코드블록으로 제공
- 기본 원칙: 코드/설정 파일은 코드블록으로 제공
- 예외(강제): md 파일 "전문" 제공 시에는 코드블록으로 감싸지 않는다.

### Verify
#### Local Verify(필수)
- PROJECT_SHELL 기준 명령어 + 기대 신호(무엇이 보이면 성공인지)
- 금지: git commit / git push 포함 금지
#### Remote Verify(조건부)
- 전제: 사용자가 push를 이미 완료한 경우에만
- 원격 CI/체크 확인 절차 + 성공/실패 판정 기준
- 금지: 커밋 생성/수정/정리(커밋 메시지 포함) 관련 절차 포함 금지

### Commit Text (Local Verify PASS 후에만)
- 제안 커밋 메시지(들) + PR 요약 초안
- 실제 커밋/PR은 사용자가 수행

### Operator Steps (mandatory)
- 사용자가 실제로 수행할 단계를 5~10개 번호로 직접 지시
- 모든 명령은 PROJECT_SHELL 기준으로만 작성
- 게이트 적용:
  - Local Verify PASS 전: 체크박스/커밋/푸시 단계 포함 금지
  - Local Verify PASS 후: (필요 시) 체크박스 업데이트 + (선택) 커밋 + 다음 OK 요청 포함 가능

### Stop
- "다음 게이트로 진행 OK?" 또는 "다음 하위 태스크 진행 OK?" 라고 묻고 대기

## 4) SDLC 게이트 정의 (DoD)
## Workflow Routing (권장)
- Intake(PRD) 완료 후: `rules/workflows/generate_tasks.md`로 PRD 기반 전체 태스크 목록을 생성한다. (턴 A/B/C OK 게이트 포함)
- 태스크 목록 계획 OK 후: `rules/workflows/process_task_lists.md`로 태스크를 하위 태스크 단위로 처리한다(WIP=1).
- 티켓이 확정되면: 해당 티켓을 기준으로 SDLC 게이트(Req → Design → Build → Test → Done)를 진행한다.

### Intake (DoD)
- 티켓 초안 완성: Goal + AC 1개 이상 + Non-goals
- 브랜치명 제안
- Intake는 rules/workflows/create_prd.md(v0.1)에 따라: (턴 A) 명료화 질문 → (턴 B) PRD 생성(/tasks/prd-[기능-이름].md 안내) → "PRD 초안 OK?" 받고 종료한다.
- PRD OK 후 다음: `rules/workflows/generate_tasks.md`로 태스크 목록 생성(OK 게이트 포함)으로 진행한다.

### Req (DoD)
- docs/01_requirements.md: 범위/비범위 + AC 명시

### Design (DoD)
- docs/02_design.md: 구조/모듈/인터페이스
- docs/03_test_plan.md: 테스트 전략/우선순위/리스크

### Build (DoD)
- src/에 MVP 구현 존재
- 로컬에서 최소 1회 실행 확인(명령어 포함)

### Test (DoD)
- tests 최소 1개(또는 수동 절차) 존재
- 실행/검증 결과는 `reports/run_YYYY-MM-DD.md`에 최소 증거(명령/결과/이슈)를 기록한다.
- 주의: 원격 CI 확인은 "push 했을 때만" Remote Verify로 수행한다.

### Done (DoD)
- 최종 요약 + 티켓 체크박스 정리 + Notion에 붙여넣을 요약 제공

## 5) 한국어 톤 가이드 (권장, 강제 아님)
- '계약' 대신 아래 표현을 우선 권장:
  - 규격 / 명세/ 형식/ 스키마
- 커밋 메시지 톤:
  - "정리/통일/반영/구현/추가/수정/개선/분리/강화"처럼 행동 중심 표현 권장
  - 강제 치환은 하지 않는다(문맥에 맞게 선택).